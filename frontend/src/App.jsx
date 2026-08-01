import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Layout, Menu, Button, Space, Card, Typography, Modal, Form, Input, Select, message } from 'antd';
import { 
  HomeOutlined, 
  TrophyOutlined, 
  UserOutlined,
  SettingOutlined,
  PlusOutlined,
  LoginOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import io from 'socket.io-client';
import PokerTable from './components/PokerTable/PokerTable';
import Dashboard from './components/Dashboard/Dashboard';
import GameLobby from './components/GameLobby/GameLobby';
import Profile from './components/Profile/Profile';
import Stats from './components/Stats/Stats';
import { useGameStore } from './store/gameStore';
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
    setCurrentGameId
  } = useGameStore();

  // 登录处理
  const handleLogin = async (values) => {
    setLoading(true);
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      
      if (response.ok) {
        const data = await response.json();
        setIsLoggedIn(true);
        setUser(data.user);
        localStorage.setItem('token', data.access_token);
        message.success('登录成功！');
        setLoginModalVisible(false);
      } else {
        message.error('登录失败，请检查用户名和密码');
      }
    } catch (error) {
      message.error('网络错误，请稍后重试');
    }
    setLoading(false);
  };

  // 注册处理
  const handleRegister = async (values) => {
    setLoading(true);
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });
      
      if (response.ok) {
        message.success('注册成功！请登录');
        setRegisterModalVisible(false);
        setLoginModalVisible(true);
      } else {
        message.error('注册失败，请检查信息');
      }
    } catch (error) {
      message.error('网络错误，请稍后重试');
    }
    setLoading(false);
  };

  // 退出登录
  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    localStorage.removeItem('token');
    disconnectGame();
    message.success('已退出登录');
  };

  return (
    <BrowserRouter>
      <Layout className="app-layout">
        <Header className="app-header">
          <div className="header-left">
            <Link to="/" className="logo-link">
              <span className="logo">♠️ Poker Egg</span>
            </Link>
          </div>
          
          <Menu theme="dark" mode="horizontal" className="header-menu">
            <Menu.Item key="home" icon={<HomeOutlined />}>
              <Link to="/">牌桌</Link>
            </Menu.Item>
            <Menu.Item key="lobby" icon={<PlusOutlined />}>
              <Link to="/lobby">大厅</Link>
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
                {/* 🎯 彩蛋按钮 - 已登录时显示 */}
                <Button 
                  type="text" 
                  ghost
                  onClick={() => window.open('/easter-egg.html', '_blank')}
                  style={{ 
                    color: '#a78bfa',
                    fontSize: '16px',
                    padding: '4px 8px'
                  }}
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
                {/* 🎯 彩蛋按钮 - 未登录时也显示 */}
                <Button 
                  type="text" 
                  ghost
                  onClick={() => window.open('/easter-egg.html', '_blank')}
                  style={{ 
                    color: '#a78bfa',
                    fontSize: '16px',
                    padding: '4px 8px'
                  }}
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
                    <PokerTable 
                      gameState={gameState} 
                      playerId={user?.id || 'player1'}
                    />
                    <Dashboard gameState={gameState} />
                  </div>
                ) : (
                  <div className="welcome-section">
                    <Card className="welcome-card">
                      <div className="welcome-icon">♠️</div>
                      <Title level={1} className="welcome-title">
                        Y.Mine · Poker Egg
                      </Title>
                      <Text className="welcome-subtitle">
                        德州扑克 · 凯利公式 · AI陪练
                      </Text>
                      <div className="welcome-divider" />
                      <Space size="large" className="welcome-actions">
                        <Button 
                          type="primary" 
                          size="large"
                          onClick={() => {
                            if (!isLoggedIn) {
                              message.warning('请先登录');
                              setLoginModalVisible(true);
                              return;
                            }
                            window.location.href = '/lobby';
                          }}
                        >
                          🎯 开始游戏
                        </Button>
                        <Button 
                          size="large"
                          onClick={() => window.location.href = '/stats'}
                        >
                          📊 查看战绩
                        </Button>
                        {/* 🎯 首页也加一个彩蛋入口 */}
                        <Button 
                          size="large"
                          ghost
                          onClick={() => window.open('/easter-egg.html', '_blank')}
                          style={{ color: '#a78bfa' }}
                        >
                          🥚 彩蛋
                        </Button>
                      </Space>
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
                        <Text>实时计算最优投注比例</Text>
                      </Card>
                      <Card className="feature-card">
                        <div className="feature-icon">🎯</div>
                        <Title level={4}>表理映射</Title>
                        <Text>博弈状态可视化分析</Text>
                      </Card>
                    </div>
                  </div>
                )}
              </div>
            } />
            <Route path="/lobby" element={<GameLobby />} />
            <Route path="/stats" element={<Stats />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </Content>

        <Footer className="app-footer">
          <Text type="secondary">
            © 2024 Poker Egg · Made with ❤️ by HelloMind-star
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
    </BrowserRouter>
  );
}

export default App;
