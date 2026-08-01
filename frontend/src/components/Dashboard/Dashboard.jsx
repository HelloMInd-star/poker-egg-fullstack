import React from 'react';
import { Card, Progress, Tag, Space, Statistic, Row, Col } from 'antd';
import { 
  RiseOutlined, 
  FallOutlined, 
  WarningOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import { motion } from 'framer-motion';
import './Dashboard.css';

const Dashboard = ({ gameState }) => {
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

  // 模拟数据（实际应从游戏状态计算）
  const kellyIndex = Math.random() * 0.5 + 0.1;
  const winRate = Math.random() * 0.4 + 0.3;
  const tension = Math.random() * 0.8 + 0.2;
  const dcf = Math.random() * 0.3 - 0.1;

  const getKellyStatus = (value) => {
    if (value > 0.3) return { color: '#22c55e', text: '高', icon: <RiseOutlined /> };
    if (value > 0.15) return { color: '#fbbf24', text: '中', icon: <WarningOutlined /> };
    return { color: '#fca5a5', text: '低', icon: <FallOutlined /> };
  };

  const kellyStatus = getKellyStatus(kellyIndex);

  return (
    <div className="dashboard-container">
      <Card className="dashboard-card" title="📐 凯利仪表盘">
        <div className="kelly-display">
          <div className="kelly-value">
            <span className="kelly-number">{(kellyIndex * 100).toFixed(1)}%</span>
            <Tag color={kellyStatus.color === '#22c55e' ? 'success' : 'warning'}>
              {kellyStatus.icon} {kellyStatus.text}
            </Tag>
          </div>
          <Progress 
            percent={kellyIndex * 100} 
            strokeColor={{
              '0%': '#22c55e',
              '50%': '#fbbf24',
              '100%': '#ef4444'
            }}
            showInfo={false}
            size="small"
          />
          <div className="kelly-label">最优仓位</div>
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

      <Card className="dashboard-card bridge-panel" title="🔮 表理映射 · 里">
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
            <span className="bridge-value">{(Math.random() * 0.5 + 0.2).toFixed(2)}</span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">📉 折价预警</span>
            <span className={`bridge-value ${dcf < -0.05 ? 'bad' : 'good'}`}>
              {(dcf * 100).toFixed(1)}%
            </span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">💹 期望值</span>
            <span className="bridge-value good">+{(Math.random() * 2 + 0.5).toFixed(1)}</span>
          </div>
          <div className="bridge-item">
            <span className="bridge-label">🎯 安全边际</span>
            <span className="bridge-value good">{(Math.random() * 20 + 10).toFixed(0)}%</span>
          </div>
        </div>
      </Card>

      <Card className="dashboard-card" title="📋 牌局信息">
        <div className="info-list">
          <div className="info-item">
            <span className="info-label">底池</span>
            <span className="info-value">🪙 {gameState.pot}</span>
          </div>
          <div className="info-item">
            <span className="info-label">阶段</span>
            <span className="info-value">
              <Tag color="purple">{gameState.stage?.toUpperCase()}</Tag>
            </span>
          </div>
          <div className="info-item">
            <span className="info-label">玩家数</span>
            <span className="info-value">{gameState.players?.length || 0}</span>
          </div>
          <div className="info-item">
            <span className="info-label">AI对手</span>
            <span className="info-value">
              {gameState.players?.filter(p => p.is_ai).length || 0} 个
            </span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
