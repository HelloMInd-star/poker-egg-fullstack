import { create } from 'zustand';

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
  pingInterval: null,

  // 连接游戏
  connectToGame: (gameId, playerId) => {
    const { socket, disconnectGame } = get();
    
    // 如果有旧连接，先断开
    if (socket) {
      disconnectGame();
    }

    // 确定WebSocket URL：优先使用环境变量，否则使用当前host（支持代理）
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = import.meta.env.VITE_WS_URL || `${wsProtocol}//${window.location.host}`;
    const wsUrl = `${wsHost}/ws/${gameId}`;
    
    console.log('连接WebSocket:', wsUrl);

    // 创建原生WebSocket连接
    const newSocket = new WebSocket(wsUrl);

    newSocket.onopen = () => {
      console.log('WebSocket 连接成功');
      set({ isConnected: true, currentGameId: gameId, playerId });
      
      // 发送心跳保持连接
      const interval = setInterval(() => {
        if (newSocket.readyState === WebSocket.OPEN) {
          newSocket.send(JSON.stringify({ type: 'ping' }));
        }
      }, 30000);
      set({ pingInterval: interval });
    };

    newSocket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const { type, data } = message;
        
        switch (type) {
          case 'pong':
            // 心跳响应，忽略
            break;
          case 'game_state':
            set({ gameState: data || message });
            break;
          case 'action_result':
            console.log('行动结果:', data);
            break;
          case 'ai_action':
            console.log('AI行动:', data);
            break;
          case 'system_message':
            console.log('系统消息:', data);
            break;
          case 'player_joined':
            console.log('玩家加入:', data);
            break;
          case 'chat':
            console.log('聊天消息:', data);
            break;
          case 'hand_over':
            console.log('牌局结束:', data);
            break;
          case 'error':
            set({ error: data?.message || '连接错误' });
            console.error('WebSocket错误:', data);
            break;
          default:
            console.log('收到消息:', message);
        }
      } catch (e) {
        console.error('解析WebSocket消息失败:', e);
      }
    };

    newSocket.onerror = (error) => {
      console.error('WebSocket错误:', error);
      set({ error: 'WebSocket连接错误' });
    };

    newSocket.onclose = () => {
      console.log('WebSocket 断开连接');
      const { pingInterval } = get();
      if (pingInterval) {
        clearInterval(pingInterval);
      }
      set({ isConnected: false, pingInterval: null });
    };

    set({ socket: newSocket });
    return newSocket;
  },

  // 断开游戏
  disconnectGame: () => {
    const { socket, pingInterval } = get();
    if (pingInterval) {
      clearInterval(pingInterval);
    }
    if (socket) {
      socket.close();
    }
    set({ 
      socket: null, 
      isConnected: false, 
      currentGameId: null,
      gameState: null,
      playerId: null,
      pingInterval: null
    });
  },

  // 发送消息
  _sendMessage: (message) => {
    const { socket, isConnected } = get();
    if (!socket || !isConnected) {
      console.error('未连接到游戏');
      return;
    }
    if (socket.readyState !== WebSocket.OPEN) {
      console.error('WebSocket未就绪');
      return;
    }
    socket.send(JSON.stringify(message));
  },

  // 发送行动
  sendAction: (action, amount = 0) => {
    const { playerId } = get();
    get()._sendMessage({
      type: 'action',
      data: {
        player_id: playerId,
        action: action,
        amount: amount
      }
    });
  },

  // 发送聊天消息
  sendChat: (message) => {
    get()._sendMessage({
      type: 'chat',
      data: {
        player_name: 'Player',
        message: message
      }
    });
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
