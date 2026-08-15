import { create } from 'zustand';

// ============ API / WS 基础URL配置 ============
// MVP fix: 统一 API/WS base URL 构造，VITE_API_URL 优先，否则相对路径；
// 去掉尾斜杠避免重复拼接 /ws/ 或 /api/

/** 构造API base URL（不带尾斜杠） */
function getApiBase() {
  const fromEnv = import.meta.env.VITE_API_URL;
  if (fromEnv) return fromEnv.replace(/\/+$/, '');
  // 同域部署（Nginx/Docker/代理）使用空串作为相对路径
  return '';
}

/** 构造WS base URL（不带尾斜杠，ws/wss协议） */
function getWsBase() {
  const fromEnv = import.meta.env.VITE_WS_URL;
  if (fromEnv) return fromEnv.replace(/\/+$/, '');
  // 根据API base推导：如果API是http(s)://host，则WS对应ws(s)://host
  const apiBase = getApiBase();
  if (apiBase) {
    return apiBase.replace(/^http/, 'ws');
  }
  // 根据当前页面协议推导
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}`;
}

const API_BASE = getApiBase();
const WS_BASE = getWsBase();

// fetch helper：自动加API前缀
async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };
  const token = localStorage.getItem('token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  const resp = await fetch(url, { ...options, headers });
  return resp;
}

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
  lastAiAction: null,
  pingInterval: null,
  apiBase: API_BASE,
  wsBase: WS_BASE,

  // 连接游戏
  connectToGame: (gameId, playerId) => {
    const { disconnectGame } = get();
    if (get().socket) {
      disconnectGame();
    }

    // 正确拼接WS URL：wsBase 可能是 wss://xxx 或空；避免重复 /ws
    const wsUrl = `${WS_BASE}/ws/${gameId}`;
    console.log('连接WebSocket:', wsUrl);

    const newSocket = new WebSocket(wsUrl);

    newSocket.onopen = () => {
      console.log('WebSocket 连接成功');
      set({ isConnected: true, currentGameId: gameId, playerId });
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
            break;
          case 'game_state':
            // 后端 broadcast game_state 时 data 是真正的 state
            set({ gameState: data || message });
            break;
          case 'action_result':
            console.log('行动结果:', data);
            break;
          case 'ai_action':
            console.log('AI行动:', data);
            // 记录AI最近行动（含人格化决策理由 reason），供分析面板展示
            set({ lastAiAction: data });
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
      if (pingInterval) clearInterval(pingInterval);
      set({ isConnected: false, pingInterval: null });
    };

    set({ socket: newSocket });
    return newSocket;
  },

  disconnectGame: () => {
    const { socket, pingInterval } = get();
    if (pingInterval) clearInterval(pingInterval);
    if (socket) socket.close();
    set({ 
      socket: null, 
      isConnected: false, 
      currentGameId: null,
      gameState: null,
      playerId: null,
      pingInterval: null
    });
  },

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

  sendAction: (action, amount = 0) => {
    const { playerId } = get();
    if (!playerId) {
      console.error('playerId 未设置');
      return;
    }
    get()._sendMessage({
      type: 'action',
      data: {
        player_id: playerId,
        action: action,
        amount: amount
      }
    });
  },

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
  createGame: async (playerName, aiDifficulty = 'medium', aiPersonality = null) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiFetch('/api/game/create', {
        method: 'POST',
        body: JSON.stringify({
          player_name: playerName,
          ai_difficulty: aiDifficulty,
          ai_personality: aiPersonality
        })
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`创建游戏失败: ${errText}`);
      }

      const data = await response.json();
      const payload = data.data || data;
      const { game_id, player_id } = payload;
      
      // 连接到游戏
      get().connectToGame(game_id, player_id);
      
      // 自动开始游戏
      await get().startGame(game_id);
      
      set({ isLoading: false });
      return { gameId: game_id, playerId: player_id };
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  joinGame: async (gameId, playerName) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiFetch(`/api/game/${gameId}/join`, {
        method: 'POST',
        body: JSON.stringify({ player_name: playerName })
      });

      if (!response.ok) {
        throw new Error('加入游戏失败');
      }

      const data = await response.json();
      const payload = data.data || data;
      const { player_id } = payload;
      
      get().connectToGame(gameId, player_id);
      
      set({ isLoading: false });
      return { playerId: player_id };
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  startGame: async (gameId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiFetch(`/api/game/${gameId}/start`, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('开始游戏失败');
      }

      const data = await response.json();
      const payload = data.data || data;
      set({ gameState: payload, isLoading: false });
      return data;
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  fetchStats: async (playerId) => {
    try {
      const response = await apiFetch(`/api/stats/${playerId}`);
      if (response.ok) {
        const data = await response.json();
        set({ stats: data.data });
        return data.data;
      }
    } catch (error) {
      console.error('获取统计数据失败:', error);
    }
  },

  clearError: () => set({ error: null }),
}));

export { apiFetch, API_BASE, WS_BASE };
