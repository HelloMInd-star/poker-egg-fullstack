import React from 'react';
import { Card, Tag } from 'antd';
import { useGameStore } from '../../store/gameStore';
import './Dashboard.css';

const STAGE_CN = {
  preflop: '翻牌前', flop: '翻牌圈', turn: '转牌圈', river: '河牌圈', showdown: '摊牌'
};

/** 读取午夜酒馆人格修正系数（无档案返回 null） */
const readCoef = () => {
  try {
    const p = JSON.parse(localStorage.getItem('midnight_tavern_profile') || 'null');
    const c = Number(p?.kellyCoefficient);
    return c > 0 && c <= 2 ? c : null;
  } catch {
    return null;
  }
};

/**
 * 局势面板 · 六维局势 + 牌局信息
 * 全部为真实数据：胜率/赔率/凯利来自后端蒙特卡洛分析接口，
 * 修正凯利 = 原始 × 午夜酒馆人格系数，码量与张力由 gameState 实时推导
 */
const Dashboard = ({ gameState, playerId }) => {
  const { lastAnalysis } = useGameStore();

  if (!gameState) {
    return (
      <Card className="dashboard-card panel-card">
        <div className="dashboard-empty">
          <span>📊</span>
          <p>等待游戏数据...</p>
        </div>
      </Card>
    );
  }

  const me = gameState.players?.find(p => p.id === playerId);
  const myChips = me?.chips ?? 0;
  const myBet = me?.bet ?? 0;
  const pot = gameState.pot ?? 0;
  const stage = gameState.stage || 'preflop';
  const bigBlind = gameState.big_blind || 20;
  const activePlayers = gameState.players?.filter(p => !p.folded) || [];

  // 真实推导：码量 BB 与博弈张力（底池占活跃总筹码比）
  const bbCount = myChips / bigBlind;
  const activeChips = activePlayers.reduce((s, p) => s + (p.chips || 0), 0);
  const tension = pot + activeChips > 0 ? pot / (pot + activeChips) : 0;

  // 分析接口真值
  const winPct = lastAnalysis ? Math.round(lastAnalysis.win_rate * 100) : null;
  const oddsPct = lastAnalysis ? Math.round(lastAnalysis.pot_odds * 100) : null;
  const kellyPct = lastAnalysis ? Math.round(lastAnalysis.kelly_fraction * 100) : null;
  const coef = readCoef();
  const adjPct = kellyPct !== null && coef ? Math.round(kellyPct * coef) : null;

  const six = [
    { icon: '📈', label: '蒙特卡洛胜率', value: winPct !== null ? `${winPct}%` : '…', cls: 'violet' },
    { icon: '⚖️', label: '底池赔率', value: oddsPct !== null ? `${oddsPct}%` : '…', cls: 'cyan' },
    { icon: '📐', label: '原始凯利', value: kellyPct !== null ? `${kellyPct}%` : '…', cls: 'gold' },
    { icon: '🧬', label: '人格修正凯利', value: adjPct !== null ? `${adjPct}%` : '—', cls: 'violet' },
    { icon: '🪙', label: '我的码量', value: `${bbCount.toFixed(0)}BB`, cls: 'gold' },
    { icon: '⚡', label: '博弈张力', value: `${Math.round(tension * 100)}%`, cls: 'pink' },
  ];

  return (
    <>
      {/* 六维局势卡 */}
      <Card className="dashboard-card panel-card six-card" title={<span>📐 六维局势</span>}>
        <div className="six-grid">
          {six.map((it) => (
            <div key={it.label} className="six-item">
              <span className={`six-value ${it.cls}`}>{it.value}</span>
              <span className="six-label">{it.icon} {it.label}</span>
            </div>
          ))}
        </div>
        <div className="six-foot">
          {coef
            ? `修正系数 ×${coef} · 来自午夜酒馆人格档案`
            : '未建立人格档案 · 修正凯利待解锁'}
        </div>
      </Card>

      {/* 牌局信息卡 */}
      <Card className="dashboard-card panel-card" title={<span>📋 牌局信息</span>}>
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
              <Tag color="purple">{STAGE_CN[stage] || stage}</Tag>
            </span>
          </div>
          <div className="info-item">
            <span className="info-label">活跃玩家</span>
            <span className="info-value">{activePlayers.length} 人</span>
          </div>
          <div className="info-item">
            <span className="info-label">盲注</span>
            <span className="info-value">{gameState.small_blind ?? 10}/{bigBlind}</span>
          </div>
        </div>
      </Card>
    </>
  );
};

export default Dashboard;
