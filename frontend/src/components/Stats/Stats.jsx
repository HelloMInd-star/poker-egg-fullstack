import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Progress, Table, Tag, Select, DatePicker } from 'antd';
import { 
  TrophyOutlined, 
  RiseOutlined, 
  FallOutlined, 
  ThunderboltOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './Stats.css';

const { RangePicker } = DatePicker;
const { Option } = Select;

const Stats = () => {
  const [timeRange, setTimeRange] = useState('week');
  const [loading, setLoading] = useState(false);

  // 模拟数据
  const statsData = {
    totalGames: 156,
    winGames: 78,
    loseGames: 72,
    drawGames: 6,
    winRate: 50,
    totalProfit: 1850,
    avgProfit: 11.86,
    maxWin: 340,
    maxLoss: -120,
    biggestPot: 680,
    handsPerGame: 12.5,
    bestHand: 'Straight Flush',
    worstHand: 'High Card'
  };

  // 趋势数据
  const trendData = [
    { date: '周一', games: 5, wins: 3, profit: 120 },
    { date: '周二', games: 8, wins: 4, profit: 80 },
    { date: '周三', games: 6, wins: 2, profit: -40 },
    { date: '周四', games: 10, wins: 6, profit: 200 },
    { date: '周五', games: 7, wins: 3, profit: 60 },
    { date: '周六', games: 12, wins: 8, profit: 320 },
    { date: '周日', games: 9, wins: 5, profit: 150 }
  ];

  // 手牌分布数据
  const handDistribution = [
    { name: '对子', value: 35 },
    { name: '两对', value: 25 },
    { name: '三条', value: 15 },
    { name: '顺子', value: 10 },
    { name: '同花', value: 8 },
    { name: '葫芦', value: 5 },
    { name: '其他', value: 2 }
  ];

  const COLORS = ['#a78bfa', '#818cf8', '#6366f1', '#4f46e5', '#7c3aed', '#6d28d9', '#5b21b6'];

  // 最近对局
  const recentGames = [
    { id: 1, date: '2024-01-05', opponent: 'AI Bot', result: 'win', profit: 120, hand: 'Straight' },
    { id: 2, date: '2024-01-05', opponent: 'AI Bot', result: 'lose', profit: -50, hand: 'High Card' },
    { id: 3, date: '2024-01-04', opponent: 'AI Bot', result: 'win', profit: 80, hand: 'Two Pair' },
    { id: 4, date: '2024-01-04', opponent: 'AI Bot', result: 'win', profit: 200, hand: 'Flush' },
    { id: 5, date: '2024-01-03', opponent: 'AI Bot', result: 'lose', profit: -30, hand: 'One Pair' }
  ];

  const columns = [
    {
      title: '日期',
      dataIndex: 'date',
      key: 'date'
    },
    {
      title: '对手',
      dataIndex: 'opponent',
      key: 'opponent'
    },
    {
      title: '结果',
      dataIndex: 'result',
      key: 'result',
      render: (result) => (
        <Tag color={result === 'win' ? 'success' : 'error'}>
          {result === 'win' ? '🟢 胜利' : '🔴 失败'}
        </Tag>
      )
    },
    {
      title: '赢利',
      dataIndex: 'profit',
      key: 'profit',
      render: (profit) => (
        <span style={{ color: profit > 0 ? '#22c55e' : '#fca5a5' }}>
          {profit > 0 ? '+' : ''}{profit}
        </span>
      )
    },
    {
      title: '手牌',
      dataIndex: 'hand',
      key: 'hand',
      render: (hand) => <Tag color="purple">{hand}</Tag>
    }
  ];

  return (
    <div className="stats-page">
      <div className="stats-header">
        <h2>📊 战绩统计</h2>
        <div className="stats-controls">
          <Select 
            value={timeRange} 
            onChange={setTimeRange}
            style={{ width: 120 }}
          >
            <Option value="day">今日</Option>
            <Option value="week">本周</Option>
            <Option value="month">本月</Option>
            <Option value="all">全部</Option>
          </Select>
          <RangePicker />
        </div>
      </div>

      {/* 概览卡片 */}
      <Row gutter={[16, 16]} className="stats-overview">
        <Col xs={12} sm={6}>
          <Card className="stat-card">
            <Statistic 
              title="总对局" 
              value={statsData.totalGames} 
              prefix={<ThunderboltOutlined />}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card className="stat-card">
            <Statistic 
              title="胜率" 
              value={statsData.winRate} 
              suffix="%" 
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#22c55e' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card className="stat-card">
            <Statistic 
              title="总赢利" 
              value={statsData.totalProfit} 
              prefix={statsData.totalProfit > 0 ? '+' : ''}
              valueStyle={{ color: statsData.totalProfit > 0 ? '#22c55e' : '#fca5a5' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card className="stat-card">
            <Statistic 
              title="最大底池" 
              value={statsData.biggestPot} 
              prefix="🪙"
            />
          </Card>
        </Col>
      </Row>

      {/* 图表 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <Card className="chart-card" title="📈 趋势分析">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="date" stroke="rgba(255,255,255,0.3)" />
                <YAxis stroke="rgba(255,255,255,0.3)" />
                <Tooltip 
                  contentStyle={{ 
                    background: '#1a1333', 
                    border: '1px solid rgba(167,139,250,0.2)',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Line type="monotone" dataKey="games" stroke="#a78bfa" name="对局数" />
                <Line type="monotone" dataKey="wins" stroke="#22c55e" name="胜场" />
                <Line type="monotone" dataKey="profit" stroke="#fbbf24" name="赢利" />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card className="chart-card" title="🎯 手牌分布">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={handDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {handDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    background: '#1a1333', 
                    border: '1px solid rgba(167,139,250,0.2)',
                    borderRadius: '8px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      {/* 详细统计 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} md={12}>
          <Card className="stats-detail" title="📊 详细数据">
            <div className="detail-grid">
              <div className="detail-item">
                <span className="detail-label">总对局</span>
                <span className="detail-value">{statsData.totalGames}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">胜场</span>
                <span className="detail-value win">{statsData.winGames}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">负场</span>
                <span className="detail-value lose">{statsData.loseGames}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">平局</span>
                <span className="detail-value">{statsData.drawGames}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">最大胜局</span>
                <span className="detail-value win">+{statsData.maxWin}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">最大败局</span>
                <span className="detail-value lose">{statsData.maxLoss}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">平均每局</span>
                <span className="detail-value">{statsData.avgProfit}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">最佳手牌</span>
                <span className="detail-value">{statsData.bestHand}</span>
              </div>
            </div>
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card className="stats-detail" title="🏆 成就">
            <div className="achievement-list">
              <div className="achievement-item">
                <CheckCircleOutlined style={{ color: '#22c55e' }} />
                <span>首次胜利</span>
                <Tag color="gold">2024-01-01</Tag>
              </div>
              <div className="achievement-item">
                <CheckCircleOutlined style={{ color: '#22c55e' }} />
                <span>10连胜</span>
                <Tag color="gold">2024-01-03</Tag>
              </div>
              <div className="achievement-item">
                <CheckCircleOutlined style={{ color: '#22c55e' }} />
                <span>赢得 500 筹码</span>
                <Tag color="gold">2024-01-04</Tag>
              </div>
              <div className="achievement-item">
                <CheckCircleOutlined style={{ color: '#22c55e' }} />
                <span>击败困难AI</span>
                <Tag color="gold">2024-01-05</Tag>
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 最近对局 */}
      <Card className="recent-games" title="📋 最近对局">
        <Table 
          columns={columns} 
          dataSource={recentGames}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  );
};

export default Stats;
