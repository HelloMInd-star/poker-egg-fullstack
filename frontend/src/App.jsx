import React, { useState, useEffect } from 'react';
import { HashRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Layout, Menu, Button, Space, Card, Typography, Modal, Form, Input, Select, message } from 'antd';
import { 
  HomeOutlined, 
  TrophyOutlined, 
  UserOutlined,
  PlusOutlined,
  LoginOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import PokerTable from './components/PokerTable/PokerTable';
import { SixDimPanel, GameInfoPanel } from './components/Dashboard/Dashboard';
import SideDrawer from './components/SideDrawer/SideDrawer';
import AnalysisPanel from './components/AnalysisPanel/AnalysisPanel';
import GameLobby from './components/GameLobby/GameLobby';
import MidnightTavern from './components/MidnightTavern/MidnightTavern';
import Profile from './components/Profile/Profile';
import Stats from './components/Stats/Stats';
import { useGameStore, apiFetch, API_BASE } from './store/gameStore';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Title, Text } = Typography;

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [loginModalVisible, setLoginModalVisible] = useState(false);
  const [registerModalVisible, setRegisterModalVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const { 
    gameState, 
    setGameState, 
    socket, 
    setSocket,
    connectToGame,
    disconnectGame,
    currentGameId,
    setCurrentGameId,
    playerId: gamePlayerId
  } = useGameStore();

  // 启动时从localStorage恢复登录态
  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (token && savedUser) {
      try {
        const u = JSON.parse(savedUser);
        setUser(u);
        setIsLoggedIn(true);
      } catch (e) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const handleLogin = async (values) => {
    setLoading(true);
    try {
      const response = await apiFetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      
      if (response.ok) {
        const data = await response.json();
        const userData = data.user;
        setIsLoggedIn(true);
        setUser(userData);
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(userData));
        message.success('登录成功！');
        setLoginModalVisible(false);
      } else {
        let errMsg = '登录失败，请检查用户名和密码';
        try {
          const err = await response.json();
          if (err.detail || err.error) errMsg = err.detail || err.error;
        } catch (_) {}
        message.error(errMsg);
      }
    } catch (error) {
      console.error(error);
      message.error('网络错误，请稍后重试');
    }
    setLoading(false);
  };

  const handleRegister = async (values) => {
    setLoading(true);
    try {
      const response = await apiFetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      
      if (response.ok) {
        message.success('注册成功！请登录');
        setRegisterModalVisible(false);
        setLoginModalVisible(true);
      } else {
        let errMsg = '注册失败，请检查信息';
        try {
          const err = await response.json();
          if (err.detail || err.error) errMsg = err.detail || err.error;
        } catch (_) {}
        message.error(errMsg);
      }
    } catch (error) {
      message.error('网络错误，请稍后重试');
    }
    setLoading(false);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    disconnectGame();
    message.success('已退出登录');
  };

  // MVP fix: tablePlayerId 优先使用gameStore中的playerId（后端createGame/joinGame返回的真实id），
  // 其次使用登录用户的id，不再使用'player1'这种硬编码fallback
  const tablePlayerId = gamePlayerId || user?.id || null;

  return (
    <HashRouter>
      <Layout className="app-layout">
        <Header className="app-header">
          <div className="header-left">
            <Link to="/" className="logo-link">
              <span className="logo">♠️ Poker Face Arena</span>
            </Link>
          </div>
          
          <Menu theme="dark" mode="horizontal" className="header-menu" selectedKeys={[]}>
            <Menu.Item key="home" icon={<HomeOutlined />}>
              <Link to="/">牌桌</Link>
            </Menu.Item>
            <Menu.Item key="lobby" icon={<PlusOutlined />}>
              <Link to="/lobby">大厅</Link>
            </Menu.Item>
            <Menu.Item key="tavern" icon={<span style={{ marginRight: 4 }}>🍸</span>}>
              <Link to="/tavern">午夜酒馆</Link>
            </Menu.Item>
            <Menu.Item key="stats" icon={<TrophyOutlined />}>
              <Link to="/stats">战绩</Link>
            </Menu.Item>
            <Menu.Item key="profile" icon={<UserOutlined />}>
              <Link to="/profile">个人</Link>
            </Menu.Item>
          </Menu>

          <div className="header-right">
            {isLoggedIn ? (
              <Space>
                <Button 
                  type="text" 
                  ghost
                  onClick={() => window.open(import.meta.env.BASE_URL + 'easter-egg.html', '_blank')}
                  style={{ color: '#a78bfa', fontSize: '16px', padding: '4px 8px' }}
                  title="🎯 查看经典彩蛋"
                >
                  🥚
                </Button>
                
                <Text style={{ color: '#fff' }}>
                  👋 {user?.username || '玩家'}
                </Text>
                <Button 
                  type="primary" 
                  ghost 
                  icon={<LogoutOutlined />}
                  onClick={handleLogout}
                >
                  退出
                </Button>
              </Space>
            ) : (
              <Space>
                <Button 
                  type="text" 
                  ghost
                  onClick={() => window.open(import.meta.env.BASE_URL + 'easter-egg.html', '_blank')}
                  style={{ color: '#a78bfa', fontSize: '16px', padding: '4px 8px' }}
                  title="🎯 查看经典彩蛋"
                >
                  🥚
                </Button>
                
                <Button 
                  type="default" 
                  ghost
                  onClick={() => setLoginModalVisible(true)}
                >
                  登录
                </Button>
                <Button 
                  type="primary"
                  onClick={() => setRegisterModalVisible(true)}
                >
                  注册
                </Button>
              </Space>
            )}
          </div>
        </Header>

        <Content className="app-content">
          <Routes>
            <Route path="/" element={
              <div className="home-page fade-in">
                {gameState ? (
                  <div className="game-container">
                    <div className="game-table-zone">
                      <PokerTable
                        gameState={gameState}
                        playerId={tablePlayerId}
                      />
                    </div>
                    <div className="game-panels">
                      <AnalysisPanel gameState={gameState} playerId={tablePlayerId} />
                    </div>
                    <SideDrawer items={[
                      { key: 'six', icon: '📐', label: '局势', title: '六维局势',
                        content: <SixDimPanel gameState={gameState} playerId={tablePlayerId} /> },
                      { key: 'info', icon: '📋', label: '信息', title: '牌局信息',
                        content: <GameInfoPanel gameState={gameState} playerId={tablePlayerId} /> }
                    ]} />
                  </div>
                ) : (
                  <div className="welcome-section">
                    <Card className="welcome-card">
                      <div className="welcome-hero">
                        <div className="welcome-hero-text">
                      <div className="welcome-icon">♠️</div>
                      <Title level={1} className="welcome-title">
                        ♠️♥️ Poker Face Arena ♦️♣️
                      </Title>
                      <Text className="welcome-subtitle">
                        扑克人格竞技场 · MBTI × Kelly × 三层AI
                      </Text>
                      <div className="welcome-divider" />
                      <Space size="large" className="welcome-actions">
                        <Button
                          type="primary"
                          size="large"
                          onClick={async () => {
                            const pool = ['INTJ','ENTJ','ENTP','ESTP','ESFP','ISTP','ENFP','ISFJ','INFJ','ISTJ'];
                            const pick = pool[Math.floor(Math.random() * pool.length)];
                            try {
                              await useGameStore.getState().createGame('玩家' + Math.floor(Math.random() * 900 + 100), 'medium', pick);
                            } catch (e) {
                              message.error('快速开局失败：' + (e.message || '网络错误'));
                            }
                          }}
                        >
                          ⚡ 快速对战 · 随机人格AI
                        </Button>
                        <Button 
                          size="large"
                          onClick={() => {
                            window.location.hash = '#/lobby';
                          }}
                        >
                          🎯 开始游戏
                        </Button>
                        <Button 
                          size="large"
                          onClick={() => window.location.hash = '#/stats'}
                        >
                          📊 查看战绩
                        </Button>
                        <Button 
                          size="large"
                          ghost
                          onClick={() => window.open(import.meta.env.BASE_URL + 'easter-egg.html', '_blank')}
                          style={{ color: '#a78bfa' }}
                        >
                          🥚 彩蛋
                        </Button>
                      </Space>
                        </div>
                        <div className="welcome-hero-art">
                          <img
                            src={import.meta.env.BASE_URL + 'arena/host_suit_poker.jpg'}
                            alt="午夜酒馆主理人 · 酒与牌"
                            className="welcome-hero-img"
                          />
                          <div className="welcome-hero-caption">🍸 主理人已就位 · 酒与牌都备好了</div>
                        </div>
                      </div>
                    </Card>

                    <div className="features-grid">
                      <Card className="feature-card">
                        <div className="feature-icon">🤖</div>
                        <Title level={4}>AI陪练</Title>
                        <Text>3个难度级别，从新手到高手</Text>
                      </Card>
                      <Card className="feature-card">
                        <div className="feature-icon">📊</div>
                        <Title level={4}>凯利公式</Title>
                        <Text>蒙特卡洛真胜率 × 最优仓位实时计算</Text>
                      </Card>
                      <Card className="feature-card">
                        <div className="feature-icon">🎯</div>
                        <Title level={4}>表理映射</Title>
                        <Text>博弈状态六维局势可视化</Text>
                      </Card>
                    </div>
                  </div>
                )}
              </div>
            } />
            <Route path="/lobby" element={<GameLobby />} />
            <Route path="/tavern" element={<MidnightTavern />} />
            <Route path="/stats" element={<Stats />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </Content>

        <Footer className="app-footer">
          <Text type="secondary">
            © 2026 Poker Face Arena · Made with ❤️ by Hello.Mind-star (Y.MINE)
          </Text>
        </Footer>
      </Layout>

      {/* 登录弹窗 */}
      <Modal
        title="🔐 登录"
        open={loginModalVisible}
        onCancel={() => setLoginModalVisible(false)}
        footer={null}
        className="auth-modal"
      >
        <Form onFinish={handleLogin} layout="vertical">
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>
          <Form.Item
            name="password"
            label="密码"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password placeholder="请输入密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              登录
            </Button>
          </Form.Item>
          <div style={{ textAlign: 'center' }}>
            <Text type="secondary">
              还没有账号？ 
              <Button type="link" onClick={() => {
                setLoginModalVisible(false);
                setRegisterModalVisible(true);
              }}>
                立即注册
              </Button>
            </Text>
          </div>
        </Form>
      </Modal>

      {/* 注册弹窗 */}
      <Modal
        title="📝 注册"
        open={registerModalVisible}
        onCancel={() => setRegisterModalVisible(false)}
        footer={null}
        className="auth-modal"
      >
        <Form onFinish={handleRegister} layout="vertical">
          <Form.Item
            name="username"
            label="用户名"
            rules={[
              { required: true, message: '请输入用户名' },
              { min: 3, message: '用户名至少3个字符' }
            ]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>
          <Form.Item
            name="email"
            label="邮箱"
            rules={[
              { required: true, message: '请输入邮箱' },
              { type: 'email', message: '请输入有效的邮箱地址' }
            ]}
          >
            <Input placeholder="请输入邮箱" />
          </Form.Item>
          <Form.Item
            name="password"
            label="密码"
            rules={[
              { required: true, message: '请输入密码' },
              { min: 6, message: '密码至少6个字符' }
            ]}
          >
            <Input.Password placeholder="请输入密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              注册
            </Button>
          </Form.Item>
          <div style={{ textAlign: 'center' }}>
            <Text type="secondary">
              已有账号？ 
              <Button type="link" onClick={() => {
                setRegisterModalVisible(false);
                setLoginModalVisible(true);
              }}>
                立即登录
              </Button>
            </Text>
          </div>
        </Form>
      </Modal>
    </HashRouter>
  );
}

export default App;
