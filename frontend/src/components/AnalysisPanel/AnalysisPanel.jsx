import React, { useEffect, useState, useRef } from 'react';
import { Switch } from 'antd';
import { useGameStore } from '../../store/gameStore';
import './AnalysisPanel.css';

const STAGE_CN = {
  preflop: '翻牌前', flop: '翻牌圈', turn: '转牌圈', river: '河牌圈', showdown: '摊牌'
};
const ACTION_CN = {
  fold: '弃牌', check: '过牌', call: '跟注', raise: '加注', allin: '全下'
};

const TAVERN_KEY = 'midnight_tavern_profile';

/** 读取午夜酒馆人格档案（L1 酒馆页写入的同源 localStorage） */
const readTavernProfile = () => {
  try {
    const raw = localStorage.getItem(TAVERN_KEY);
    if (!raw) return null;
    const p = JSON.parse(raw);
    const coef = Number(p?.kellyCoefficient);
    if (!coef || coef <= 0 || coef > 2) return null;
    return { ...p, kellyCoefficient: coef };
  } catch {
    return null;
  }
};

/** BB 码量梯度（大盲倍数 → 战略档位） */
const BB_TIERS = [
  { max: 10, name: '危险超短码', cls: 'critical', tip: 'Push/Fold 模式：只打全下或弃牌，拒绝平跟纠缠' },
  { max: 20, name: '极短码', cls: 'short', tip: '抢盲为王：放宽全下范围抢盲，避免小注消耗' },
  { max: 40, name: '短码', cls: 'short', tip: '简化决策：翻前加注即倾向套池，少打翻后街' },
  { max: 80, name: '中码', cls: 'mid', tip: '标准打法：位置与牌力双线估值，注意控制底池' },
  { max: 150, name: '标准深码', cls: 'deep', tip: '深码博弈：隐含赔率优先，利用位置多打翻后' },
  { max: Infinity, name: '超深码', cls: 'deep', tip: '超深码慎战：坚果潜力牌升值、顶对贬值，控池第一' },
];
const bbTierOf = (bb) => BB_TIERS.find(t => bb < t.max) || BB_TIERS[BB_TIERS.length - 1];

/**
 * Kelly 实时决策面板
 * 真胜率（蒙特卡洛逐街重算）× 牌型识别 × 底池赔率 × Kelly 注额
 * L2：原始 Kelly（黄）vs 人格修正 Kelly（电光紫，系数来自午夜酒馆）
 *     + 启用人格修正开关 + BB 码量梯度自动识别与战略提示
 */
const AnalysisPanel = ({ gameState, playerId }) => {
  const { apiBase, currentGameId, lastAiAction } = useGameStore();
  const [analysis, setAnalysis] = useState(null);
  const [tavern, setTavern] = useState(readTavernProfile);
  const [kellyAdjustOn, setKellyAdjustOn] = useState(true);
  const timerRef = useRef(null);

  const me = gameState?.players?.find(p => p.id === playerId);
  const stage = gameState?.stage;
  const pot = gameState?.pot;
  const handOver = gameState?.hand_over;
  const myCardsKey = (me?.hole_cards || []).map(c => c.rank + c.suit).join('');
  const boardKey = (gameState?.board || []).map(c => c.rank + c.suit).join('');
  const betKey = gameState?.current_bet || 0;
  const chipsKey = me?.chips || 0;

  // 酒馆档案可能在游戏间隙更新（去酒馆重测后回到牌桌）
  useEffect(() => {
    const sync = () => setTavern(readTavernProfile());
    window.addEventListener('storage', sync);
    window.addEventListener('focus', sync);
    return () => {
      window.removeEventListener('storage', sync);
      window.removeEventListener('focus', sync);
    };
  }, []);

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

  // L2 人格修正：修正注额 = 原始 Kelly × 酒馆系数
  const coef = tavern?.kellyCoefficient;
  const hasTavern = typeof coef === 'number';
  const kellyAdjActive = hasTavern && kellyAdjustOn && !!analysis;
  const adjAmount = kellyAdjActive ? Math.round(analysis.kelly_amount * coef) : null;
  const adjPct = kellyAdjActive && kellyPct !== null ? Math.round(kellyPct * coef) : null;

  // L2 BB 码量梯度
  const bigBlind = gameState?.big_blind || 20;
  const bbCount = me.chips / bigBlind;
  const tier = bbTierOf(bbCount);

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

      {/* 底池赔率 / 原始 Kelly / 修正 Kelly / BB 码量 */}
      <div className="analysis-grid">
        <div className="grid-item">
          <div className="grid-value">{oddsPct !== null ? `${oddsPct}%` : '…'}</div>
          <div className="grid-label">底池赔率</div>
        </div>
        <div className="grid-item">
          <div className="grid-value gold">
            {analysis ? `${analysis.kelly_amount}` : '…'}
          </div>
          <div className="grid-label">原始 Kelly{kellyPct !== null ? ` (${kellyPct}%)` : ''}</div>
        </div>
        <div className={`grid-item kelly-adj-item${kellyAdjActive ? '' : ' off'}`}>
          <div className="grid-value violet">{kellyAdjActive ? `${adjAmount}` : '—'}</div>
          <div className="grid-label">人格修正 Kelly{adjPct !== null ? ` (${adjPct}%)` : ''}</div>
        </div>
        <div className="grid-item bb-item">
          <div className="grid-value bb">
            {bbCount.toFixed(0)}<span className="bb-unit">BB</span>
          </div>
          <div className="grid-label">码量梯度 · {tier.name}</div>
        </div>
      </div>

      {/* BB 梯度战略提示 */}
      <div className={`bb-tip ${tier.cls}`}>
        🪙 {bbCount.toFixed(0)} BB · {tier.name} — {tier.tip}
      </div>

      {/* 午夜酒馆人格修正开关 */}
      {hasTavern ? (
        <div className="tavern-adjust">
          <div className="tavern-adjust-row">
            <Switch
              size="small"
              checked={kellyAdjustOn}
              onChange={setKellyAdjustOn}
            />
            <span className="tavern-adjust-name">启用人格修正 ×{coef}</span>
          </div>
          <div className="tavern-adjust-src">
            修正系数来自午夜酒馆{tavern.drinkName ? ` · ${tavern.drinkName}` : ''}{tavern.mbti ? ` · ${tavern.mbti}` : ''}
          </div>
        </div>
      ) : (
        <div className="tavern-adjust empty" onClick={() => { window.location.hash = '#/tavern'; }}>
          🍸 尚未建立人格档案 — 前往午夜酒馆完成决策者试炼，解锁专属凯利修正
        </div>
      )}

      {/* Kelly 仓位条：原始（金）+ 修正（电光紫） */}
      {analysis && (
        <>
          <div className="kelly-bar-track">
            <div className="kelly-bar-fill" style={{ width: `${kellyBarWidth}%` }} />
          </div>
          {kellyAdjActive && (
            <div className="kelly-bar-track adj">
              <div className="kelly-bar-fill adj" style={{ width: `${Math.min(100, kellyBarWidth * coef)}%` }} />
            </div>
          )}
        </>
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
