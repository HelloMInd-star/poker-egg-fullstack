import React, { useMemo } from 'react';
import { Card, Progress, Tag, Space, Statistic, Row, Col, Tooltip } from 'antd';
import { 
  RiseOutlined, 
  FallOutlined, 
  WarningOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import { motion } from 'framer-motion';
import './Dashboard.css';

const Dashboard = ({ gameState, playerId }) => {
  if (!gameState) {
    return (
      <Card className="dashboard-container">
        <div className="dashboard-empty">
          <span>📊</span>
          <p>等待游戏数据...</p>
        </div>
      </Card>
    );
  }

  // 从gameState里计算出真实可用的基础数据；其余高级指标暂为Demo
  const me = gameState.players?.find(p => p.id === playerId);
  const myChips = me?.chips ?? 0;
  const myBet = me?.bet ?? 0;
  const pot = gameState.pot ?? 0;
  const stage = gameState.stage || 'preflop';
  const activePlayers = gameState.players?.filter(p => !p.folded).length ?? 0;

  // Demo 数值（未来接入真实胜率/凯利时替换）
  const kellyIndex = useMemo(() => 0.25, [gameState.id, stage]);
  const winRate = useMemo(() => 0.45, [gameState.id, stage]);
  const tension = useMemo(() => 0.5, [gameState.id, stage]);
  const dcf = useMemo(() => -0.05, [gameState.id, stage]);

  const getKellyStatus = (value) => {
    if (value > 0.3) return { color: 'success', text: '高', icon: <RiseOutlined /> };
    if (value > 0.15) return { color: 'warning', text: '中', icon: <WarningOutlined /> };
    return { color: 'default', text: '低', icon: <FallOutlined /> };
  };

  const kellyStatus = getKellyStatus(kellyIndex);

  return (
    <div className="dashboard-container">
      <Card 
        className="dashboard-card" 
        title={
          <Space>
            <span>📐 凯利仪表盘</span>
            <Tooltip title="Demo 数据：凯利/胜率等高级指标暂为占位，将接入真实胜率计算">
              <Tag color="orange" style={{marginLeft: 8}}><InfoCircleOutlined /> Demo</Tag>
            </Tooltip>
          </Space>
        }
      >
        <div className="kelly-display">
          <div className="kelly-value">
            <span className="kelly-number">{(kellyIndex * 100).toFixed(1)}%</span>
            <Tag color={kellyStatus.color}>
              {kellyStatus.icon} {kellyStatus.text}
            </Tag>
          </div>
          <Progress 
            percent={kellyIndex * 100} 
            strokeColor={{ '0%': '#22c55e', '50%': '#fbbf24', '100%': '#ef4444' }}
            showInfo={false}
            size="small"
          />
          <div className="kelly-label">最优仓位 <span style={{color: '#999', fontSize: 12}}>（Demo）</span></div>
        </div>

        <div className="metrics-grid">
          <div className="metric-item">
            <span className="metric-label">📈 胜率</span>
            <span className="metric-value win">{(winRate * 100).toFixed(0)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">⚡ 博弈张力</span>
            <span className="metric-value tension">{(tension * 100).toFixed(0)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">⚠️ DCF折价</span>
            <span className={`metric-value ${dcf < 0 ? 'bad' : 'good'}`}>
              {(dcf * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </Card>

      <Card 
        className="dashboard-card bridge-panel" 
        title={
          <Space>
            <span>🔮 表理映射 · 里</span>
            <Tag color="orange"><InfoCircleOutlined /> Demo</Tag>
          </Space>
        }
      >
        <div className="bridge-grid">
          <div className="bridge-item">
            <span className="bridge-label">🧠 凯利映射</span>
            <span className="bridge-value">{(kellyIndex * 100).toFixed(1)}%</span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">📊 博弈势能</span>
            <span className="bridge-value">{(tension * 100).toFixed(0)}%</span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">🔄 波动率</span>
            <span className="bridge-value">0.35</span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">📉 折价预警</span>
            <span className={`bridge-value ${dcf < -0.05 ? 'bad' : 'good'}`}>
              {(dcf * 100).toFixed(1)}%
            </span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">💹 期望值</span>
            <span className="bridge-value good">+1.2</span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">🎯 安全边际</span>
            <span className="bridge-value good">15%</span>
          </div>
        </div>
      </Card>

      <Card className="dashboard-card" title="📋 牌局信息">
        <div className="info-list">
          <div className="info-item">
            <span className="info-label">我的筹码</span>
            <span className="info-value">🪙 {myChips}</span>
          </div>
          <div className="info-item">
            <span className="info-label">底池</span>
            <span className="info-value">🪙 {pot}</span>
          </div>
          <div className="info-item">
            <span className="info-label">本轮下注</span>
            <span className="info-value">🪙 {myBet}</span>
          </div>
          <div className="info-item">
            <span className="info-label">阶段</span>
            <span className="info-value">
              <Tag color="purple">{stage?.toUpperCase()}</Tag>
            </span>
          </div>
          <div className="info-item">
            <span className="info-label">活跃玩家</span>
            <span className="info-value">{activePlayers} 人</span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
