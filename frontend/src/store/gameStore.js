import { create } from 'zustand';
import { io } from 'socket.io-client';

export const useGameStore = create((set, get) => ({
  // 状态
  gameState: null,
  socket: null,
  currentGameId: null,
  playerId: null,
  isConnected: false,
  isLoading: false,
  error: null,
  history: [],
  stats: null,

  // 连接游戏
  connectToGame: (gameId, playerId) => {
    const { socket, disconnectGame } = get();
    
    // 如果有旧连接，先断开
    if (socket) {
      disconnectGame();
    }

    // 创建新连接
    const newSocket = io(import.meta.env.VITE_WS_URL || 'ws://localhost:5000', {
      path: `/ws/${gameId}`,
      transports: ['websocket'],
      autoConnect: true,
    });

    newSocket.on('connect', () => {
      console.log('WebSocket 连接成功');
      set({ isConnected: true, currentGameId: gameId, playerId });
    });

    newSocket.on('game_state', (data) => {
      set({ gameState: data.data || data });
    });

    newSocket.on('action_result', (data) => {
      console.log('行动结果:', data);
      // 可以添加通知
    });

    newSocket.on('ai_action', (data) => {
      console.log('AI行动:', data);
    });

    newSocket.on('system_message', (data) => {
      console.log('系统消息:', data);
    });

    newSocket.on('hand_over', (data) => {
      console.log('牌局结束:', data);
    });

    newSocket.on('error', (data) => {
      set({ error: data.data?.message || '连接错误' });
      console.error('WebSocket错误:', data);
    });

    newSocket.on('disconnect', () => {
      set({ isConnected: false });
      console.log('WebSocket 断开连接');
    });

    set({ socket: newSocket });
    return newSocket;
  },

  // 断开游戏
  disconnectGame: () => {
    const { socket } = get();
    if (socket) {
      socket.disconnect();
      socket.close();
    }
    set({ 
      socket: null, 
      isConnected: false, 
      currentGameId: null,
      gameState: null,
      playerId: null
    });
  },

  // 发送行动
  sendAction: (action, amount = 0) => {
    const { socket, playerId, currentGameId } = get();
    if (!socket || !isConnected) {
      console.error('未连接到游戏');
      return;
    }

    socket.send(JSON.stringify({
      type: 'action',
      data: {
        player_id: playerId,
        action: action,
        amount: amount
      }
    }));
  },

  // 发送聊天消息
  sendChat: (message) => {
    const { socket, playerId } = get();
    if (!socket || !isConnected) {
      console.error('未连接到游戏');
      return;
    }

    socket.send(JSON.stringify({
      type: 'chat',
      data: {
        player_name: 'Player',
        message: message
      }
    }));
  },

  // 创建游戏
  createGame: async (playerName, aiDifficulty = 'medium') => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('/api/game/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          player_name: playerName,
          ai_difficulty: aiDifficulty
        })
      });

      if (!response.ok) {
        throw new Error('创建游戏失败');
      }

      const data = await response.json();
      const { game_id, player_id } = data.data;
      
      // 连接到游戏
      get().connectToGame(game_id, player_id);
      
      set({ isLoading: false });
      return { gameId: game_id, playerId: player_id };
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // 加入游戏
  joinGame: async (gameId, playerName) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`/api/game/${gameId}/join`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          player_name: playerName
        })
      });

      if (!response.ok) {
        throw new Error('加入游戏失败');
      }

      const data = await response.json();
      const { player_id } = data.data;
      
      // 连接到游戏
      get().connectToGame(gameId, player_id);
      
      set({ isLoading: false });
      return { playerId: player_id };
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // 开始游戏
  startGame: async (gameId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`/api/game/${gameId}/start`, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('开始游戏失败');
      }

      const data = await response.json();
      set({ gameState: data.data, isLoading: false });
      return data;
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // 获取统计数据
  fetchStats: async (playerId) => {
    try {
      const response = await fetch(`/api/stats/${playerId}`);
      if (response.ok) {
        const data = await response.json();
        set({ stats: data.data });
        return data.data;
      }
    } catch (error) {
      console.error('获取统计数据失败:', error);
    }
  },

  // 重置错误
  clearError: () => set({ error: null }),
}));
