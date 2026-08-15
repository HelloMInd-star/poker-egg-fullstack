import React, { useEffect, useState, useRef } from 'react';
import { useGameStore } from '../../store/gameStore';
import './AnalysisPanel.css';

const STAGE_CN = {
  preflop: '翻牌前', flop: '翻牌圈', turn: '转牌圈', river: '河牌圈', showdown: '摊牌'
};
const ACTION_CN = {
  fold: '弃牌', check: '过牌', call: '跟注', raise: '加注', allin: '全下'
};

/**
 * Kelly 实时决策面板
 * 真胜率（蒙特卡洛逐街重算）× 牌型识别 × 底池赔率 × Kelly 注额
 * + 人格 AI 的决策理由（可解释陪练核心）
 */
const AnalysisPanel = ({ gameState, playerId }) => {
  const { apiBase, currentGameId, lastAiAction } = useGameStore();
  const [analysis, setAnalysis] = useState(null);
  const timerRef = useRef(null);

  const me = gameState?.players?.find(p => p.id === playerId);
  const stage = gameState?.stage;
  const pot = gameState?.pot;
  const handOver = gameState?.hand_over;
  const myCardsKey = (me?.hole_cards || []).map(c => c.rank + c.suit).join('');
  const boardKey = (gameState?.board || []).map(c => c.rank + c.suit).join('');
  const betKey = gameState?.current_bet || 0;
  const chipsKey = me?.chips || 0;

  useEffect(() => {
    if (!currentGameId || !playerId || !me || me.folded || handOver) return;
    if ((me.hole_cards || []).length < 2) return;
    // 防抖 300ms：一局内多次状态广播时合并请求
    clearTimeout(timerRef.current);
    timerRef.current = setTimeout(async () => {
      try {
        const resp = await fetch(
          `${apiBase}/api/game/${currentGameId}/analysis?player_id=${playerId}`
        );
        const json = await resp.json();
        if (json.success) setAnalysis(json.data);
      } catch (e) {
        console.warn('分析拉取失败:', e);
      }
    }, 300);
    return () => clearTimeout(timerRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentGameId, playerId, stage, myCardsKey, boardKey, pot, betKey, chipsKey, handOver]);

  if (!me || (me.hole_cards || []).length < 2) return null;

  const winPct = analysis ? Math.round(analysis.win_rate * 100) : null;
  const oddsPct = analysis ? Math.round(analysis.pot_odds * 100) : null;
  const kellyPct = analysis ? Math.round(analysis.kelly_fraction * 100) : null;
  // Kelly 封顶 50%，进度条按 0-50% 映射
  const kellyBarWidth = analysis ? Math.min(100, (analysis.kelly_fraction / 0.5) * 100) : 0;

  const suggestionClass = analysis?.suggestion || 'check';

  return (
    <div className="analysis-panel">
      <div className="analysis-header">
        <span className="analysis-icon">🧠</span>
        <span className="analysis-title">Kelly 决策面板</span>
        {stage && <span className="analysis-stage">{STAGE_CN[stage] || stage}</span>}
      </div>

      {/* 手牌识别：我是什么牌 */}
      <div className="analysis-hand">
        <span className="hand-label">我的手牌</span>
        <span className="hand-cards">
          {(me.hole_cards || []).map((c, i) => (
            <span key={i} className={`mini-card ${c.color}`}>{c.rank}{c.suit}</span>
          ))}
        </span>
        <span className="hand-name">{analysis?.hand_name || '分析中…'}</span>
      </div>

      {/* 蒙特卡洛真胜率 */}
      <div className="analysis-winrate">
        <div className="winrate-number">
          {winPct !== null ? <>{winPct}<span className="pct">%</span></> : '…'}
        </div>
        <div className="winrate-label">蒙特卡洛胜率 · 逐街实时重算</div>
      </div>

      {/* 赔率 + Kelly */}
      <div className="analysis-grid">
        <div className="grid-item">
          <div className="grid-value">{oddsPct !== null ? `${oddsPct}%` : '…'}</div>
          <div className="grid-label">底池赔率</div>
        </div>
        <div className="grid-item">
          <div className="grid-value gold">
            {analysis ? `${analysis.kelly_amount}` : '…'}
          </div>
          <div className="grid-label">Kelly 建议注额{kellyPct !== null ? ` (${kellyPct}%)` : ''}</div>
        </div>
      </div>

      {/* Kelly 仓位条 */}
      {analysis && (
        <div className="kelly-bar-track">
          <div className="kelly-bar-fill" style={{ width: `${kellyBarWidth}%` }} />
        </div>
      )}

      {/* 综合建议 */}
      {analysis && (
        <div className={`analysis-suggestion ${suggestionClass}`}>
          💡 {analysis.suggestion_text}
        </div>
      )}

      {/* 人格 AI 决策理由（可解释陪练） */}
      {lastAiAction && lastAiAction.reason && (
        <div className="ai-reason">
          <span className="ai-reason-head">
            🤖 {lastAiAction.player} · {ACTION_CN[lastAiAction.action] || lastAiAction.action}
          </span>
          <span className="ai-reason-text">“{lastAiAction.reason}”</span>
        </div>
      )}
    </div>
  );
};

export default AnalysisPanel;
