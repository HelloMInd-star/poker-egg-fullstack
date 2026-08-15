import React, { useState, useEffect } from 'react';
import { Card, Avatar, Statistic, Row, Col, Table, Button, Space, Tabs } from 'antd';
import { 
  UserOutlined, 
  TrophyOutlined, 
  WalletOutlined, 
  BarChartOutlined,
  SettingOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import { useGameStore } from '../../store/gameStore';
import './Profile.css';

const { TabPane } = Tabs;

const Profile = () => {
  const { stats, fetchStats } = useGameStore();
  const [loading, setLoading] = useState(true);

  // 模拟用户数据
  const user = {
    username: 'Player',
    email: 'player@example.com',
    chips: 2850,
    totalHands: 156,
    handsWon: 78,
    winRate: 50,
    joinDate: '2026-08-10'
  };

  useEffect(() => {
    // 获取统计数据
    const loadStats = async () => {
      setLoading(true);
      await fetchStats('player1');
      setLoading(false);
    };
    loadStats();
  }, []);

  const columns = [
    {
      title: '日期',
      dataIndex: 'date',
      key: 'date'
    },
    {
      title: '牌局',
      dataIndex: 'hands',
      key: 'hands'
    },
    {
      title: '结果',
      dataIndex: 'result',
      key: 'result',
      render: (result) => (
        <span style={{ color: result === 'win' ? '#22c55e' : '#fca5a5' }}>
          {result === 'win' ? '🟢 胜利' : '🔴 失败'}
        </span>
      )
    },
    {
      title: '变化',
      dataIndex: 'change',
      key: 'change',
      render: (change) => (
        <span style={{ color: change > 0 ? '#22c55e' : '#fca5a5' }}>
          {change > 0 ? '+' : ''}{change}
        </span>
      )
    }
  ];

  // 模拟历史数据
  const mockHistory = [
    { date: '2026-08-10', hands: 12, result: 'win', change: 150 },
    { date: '2026-08-11', hands: 8, result: 'lose', change: -80 },
    { date: '2026-08-12', hands: 15, result: 'win', change: 200 },
    { date: '2026-08-13', hands: 5, result: 'lose', change: -40 },
    { date: '2026-08-14', hands: 10, result: 'win', change: 120 }
  ];

  return (
    <div className="profile-page">
      <Row gutter={[24, 24]}>
        <Col xs={24} md={8}>
          <Card className="profile-card">
            <div className="profile-avatar">
              <Avatar size={80} icon={<UserOutlined />} />
              <h2>{user.username}</h2>
              <p className="profile-email">{user.email}</p>
              <div className="profile-join-date">
                加入于 {user.joinDate}
              </div>
            </div>
            <div className="profile-stats">
              <div className="stat-item">
                <WalletOutlined />
                <span className="stat-number">{user.chips}</span>
                <span className="stat-label">筹码</span>
              </div>
              <div className="stat-item">
                <TrophyOutlined />
                <span className="stat-number">{user.handsWon}</span>
                <span className="stat-label">胜场</span>
              </div>
              <div className="stat-item">
                <BarChartOutlined />
                <span className="stat-number">{user.winRate}%</span>
                <span className="stat-label">胜率</span>
              </div>
            </div>
            <div className="profile-actions">
              <Button icon={<SettingOutlined />}>设置</Button>
              <Button icon={<LogoutOutlined />} danger>退出登录</Button>
            </div>
          </Card>
        </Col>

        <Col xs={24} md={16}>
          <Card className="profile-card">
            <Tabs defaultActiveKey="history">
              <TabPane tab="📊 对局历史" key="history">
                <Table 
                  columns={columns} 
                  dataSource={mockHistory}
                  rowKey="date"
                  pagination={{ pageSize: 5 }}
                />
              </TabPane>
              <TabPane tab="📈 统计数据" key="stats">
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <Card className="stat-card">
                      <Statistic 
                        title="总对局" 
                        value={user.totalHands} 
                        prefix={<BarChartOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card className="stat-card">
                      <Statistic 
                        title="胜率" 
                        value={user.winRate} 
                        suffix="%" 
                        prefix={<TrophyOutlined />}
                        valueStyle={{ color: '#22c55e' }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card className="stat-card">
                      <Statistic 
                        title="总赢利" 
                        value={user.chips - 1000} 
                        prefix={user.chips > 1000 ? '+' : ''}
                        valueStyle={{ color: user.chips > 1000 ? '#22c55e' : '#fca5a5' }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card className="stat-card">
                      <Statistic 
                        title="最大连胜" 
                        value={5} 
                        prefix={<TrophyOutlined />}
                      />
                    </Card>
                  </Col>
                </Row>
              </TabPane>
              <TabPane tab="⚙️ 设置" key="settings">
                <div className="settings-section">
                  <h3>偏好设置</h3>
                  <p>这里可以设置游戏偏好、音效、主题等</p>
                </div>
              </TabPane>
            </Tabs>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Profile;
