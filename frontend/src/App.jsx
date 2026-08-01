import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, Button, Space, Card, Typography } from 'antd';
import { 
  HomeOutlined, 
  TrophyOutlined, 
  UserOutlined,
  SettingOutlined 
} from '@ant-design/icons';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Title, Text } = Typography;

function App() {
  const [gameState, setGameState] = useState(null);

  return (
    <BrowserRouter>
      <Layout className="app-layout">
        <Header className="app-header">
          <div className="header-left">
            <span className="logo">♠️ Poker Egg</span>
          </div>
          <Menu theme="dark" mode="horizontal" className="header-menu">
            <Menu.Item key="home" icon={<HomeOutlined />}>
              <Link to="/">牌桌</Link>
            </Menu.Item>
            <Menu.Item key="stats" icon={<TrophyOutlined />}>
              <Link to="/stats">战绩</Link>
            </Menu.Item>
            <Menu.Item key="profile" icon={<UserOutlined />}>
              <Link to="/profile">个人</Link>
            </Menu.Item>
          </Menu>
          <div className="header-right">
            <Button type="primary" ghost>登录</Button>
          </div>
        </Header>

        <Content className="app-content">
          <Routes>
            <Route path="/" element={
              <div className="home-page">
                <Card className="welcome-card">
                  <Title level={2}>♠️ 欢迎来到 Poker Egg</Title>
                  <Text type="secondary">
                    德州扑克AI陪练平台 · 实时凯利指数 · 智能对手
                  </Text>
                  <Space style={{ marginTop: 20 }}>
                    <Button type="primary" size="large">
                      开始游戏
                    </Button>
                    <Button size="large">观战</Button>
                  </Space>
                </Card>
                
                <div className="features-grid">
                  <Card className="feature-card">
                    <Title level={4}>🤖 AI陪练</Title>
                    <Text>3个难度级别，从新手到高手</Text>
                  </Card>
                  <Card className="feature-card">
                    <Title level={4}>📊 凯利公式</Title>
                    <Text>实时计算最优投注比例</Text>
                  </Card>
                  <Card className="feature-card">
                    <Title level={4}>🎯 表理映射</Title>
                    <Text>博弈状态可视化分析</Text>
                  </Card>
                </div>
              </div>
            } />
            <Route path="/stats" element={<div>战绩统计</div>} />
            <Route path="/profile" element={<div>个人中心</div>} />
          </Routes>
        </Content>

        <Footer className="app-footer">
          <Text type="secondary">
            © 2024 Poker Egg · Made with ❤️
          </Text>
        </Footer>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
