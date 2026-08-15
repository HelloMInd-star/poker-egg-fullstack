import React, { useState, useMemo, useEffect, useRef } from 'react';
import { Button, Space, Card, Tag, Tooltip, Modal, Slider } from 'antd';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ThunderboltOutlined,
  FireOutlined,
  SafetyOutlined,
  TrophyOutlined
} from '@ant-design/icons';
import { useGameStore } from '../../store/gameStore';
import ResultModal from '../ResultModal/ResultModal';
import './PokerTable.css';

const PokerTable = ({ gameState, playerId }) => {
  const [raiseAmount, setRaiseAmount] = useState(40);
  const [showRaiseModal, setShowRaiseModal] = useState(false);
  const [resultModal, setResultModal] = useState(null); // 'win'|'push'|'fold'|'raise'|'trial'
  const prevHandOverRef = useRef(false);
  const { sendAction, isConnected, recordDecision, decisions } = useGameStore();

  // 试炼总结统计：风险偏好 = 实际投入 / 修正建议 的均值分档
  const trialStats = useMemo(() => {
    const ratios = decisions.filter(d => d.ratio !== null && d.ratio !== undefined).map(d => d.ratio);
    const avgRatio = ratios.length ? ratios.reduce((a, b) => a + b, 0) / ratios.length : 0;
    const avgCoef = decisions.length
      ? decisions.reduce((a, b) => a + (b.coef || 1), 0) / decisions.length
      : 1;
    let risk = '均衡';
    if (!ratios.length || avgRatio < 0.6) risk = '保守';
    else if (avgRatio > 1.4) risk = '激进';
    return { risk, avgCoef: avgCoef.toFixed(2) };
  }, [decisions]);

  // 摊牌结果弹窗：胜利 / 平局（分池）/ 有人打光 → 试炼结束
  useEffect(() => {
    if (!gameState) return;
    const wasOver = prevHandOverRef.current;
    const isOver = !!gameState.hand_over;
    if (isOver && !wasOver) {
      const winners = gameState.winners || (gameState.winner ? [gameState.winner] : []);
      const meName = gameState.players?.find(p => p.id === playerId)?.name;
      const iWon = winners.some(w =>
        (w.id && w.id === playerId) ||
        (w.player_id && w.player_id === playerId) ||
        (meName && w.name === meName)
      );
      const someoneBusted = (gameState.players || []).some(p => (p.chips ?? 1) <= 0);
      if (iWon && winners.length > 1) {
        setResultModal('push');
      } else if (iWon) {
        setResultModal('win');
      }
      if (someoneBusted) {
        setTimeout(() => setResultModal('trial'), iWon ? 2000 : 600);
      }
    }
    prevHandOverRef.current = isOver;
  }, [gameState, playerId]);

  if (!gameState) {
    return (
      <Card className="poker-table-container">
        <div className="empty-state">
          <span className="empty-icon">♠️</span>
          <p>等待游戏开始...</p>
          <p className="empty-hint">请在大厅创建或加入游戏</p>
        </div>
      </Card>
    );
  }

  const { players, board, pot, stage, hand_over, current_player, current_bet = 0, small_blind = 10, big_blind = 20 } = gameState;
  
  const me = players?.find(p => p.id === playerId);
  const isMyTurn = !!(me && 
    !hand_over && 
    players?.[current_player]?.id === playerId &&
    !me.folded &&
    !me.all_in);

  // 计算我需要的call金额
  const myCallAmount = me ? Math.max(0, current_bet - (me.bet || 0)) : 0;
  const canCheck = isMyTurn && myCallAmount === 0;

  const aiPlayers = players?.filter(p => p.is_ai || p.isAI) || [];

  // 最小加注增量（至少大盲）
  const minRaiseTotal = myCallAmount + big_blind;
  const maxRaise = me?.chips || 0;

  const handleAction = (action, amount = 0) => {
    if (!isMyTurn) return;
    // 决策记录：弃牌立即给结果弹窗，跟注/全下静默记录
    if (action === 'fold') {
      recordDecision('fold', 0);
      setResultModal('fold');
    } else if (action === 'call') {
      recordDecision('call', myCallAmount);
    } else if (action === 'allin') {
      recordDecision('allin', me?.chips || 0);
    }
    sendAction(action, amount);
  };

  const handleConfirmRaise = () => {
    if (!isMyTurn) return;
    // raise action的amount是加注增量（超出call的部分）
    let inc = raiseAmount - myCallAmount;
    if (inc < big_blind) inc = big_blind;
    recordDecision('raise', raiseAmount);
    sendAction('raise', inc);
    setShowRaiseModal(false);
    setResultModal('raise');
  };

  const renderCard = (card, index) => {
    if (!card) {
      return (
        <div key={index} className="card-slot">
          <span>?</span>
        </div>
      );
    }
    return (
      <motion.div
        key={index}
        className={`card ${card.color}`}
        initial={{ scale: 0, rotate: -180, y: -50 }}
        animate={{ scale: 1, rotate: 0, y: 0 }}
        transition={{ delay: index * 0.1, type: 'spring', stiffness: 200 }}
      >
        <span className="card-rank">{card.rank}</span>
        <span className="card-suit">{card.suit}</span>
        <span className="card-rank-bottom">{card.rank}</span>
      </motion.div>
    );
  };

  // 根据玩家数量计算座位角度：1v1两人对坐，多人均匀分布
  const playerCount = players?.length || 2;
  const getSeatStyle = (index) => {
    const angleStep = 360 / Math.max(playerCount, 2);
    const angle = index * angleStep - 90; // 从顶部开始
    return {
      position: 'absolute',
      left: '50%',
      top: '50%',
      transform: `rotate(${angle}deg) translateY(-200px) rotate(-${angle}deg) translate(-50%, -50%)`
    };
  };

  const renderPlayer = (player, index) => {
    const isCurrent = players[current_player]?.id === player.id;
    const isMe = player.id === playerId;
    const isAI = player.is_ai;
    const isActive = !player.folded && !player.all_in;

    // 仅我自己的手牌可见（AI和他人看背面）
    const showCards = isMe || (player.hole_cards && player.folded);

    return (
      <div 
        key={player.id}
        className={`player-seat ${isCurrent ? 'active' : ''} ${isMe ? 'me' : ''} ${player.folded ? 'folded' : ''}`}
        style={getSeatStyle(index)}
      >
        <div className="player-avatar">
          {isAI ? '🤖' : (isMe ? '🧑‍💻' : '👤')}
          {isCurrent && <div className="active-indicator">●</div>}
        </div>
        <div className="player-info">
          <div className="player-name">
            {player.name}
            {player.is_sb && <Tag color="geekblue" style={{marginInline: 4}}>SB</Tag>}
            {player.is_bb && <Tag color="magenta" style={{marginInline: 4}}>BB</Tag>}
            {player.is_dealer && !player.is_bb && <Tag color="gold" style={{marginInline: 4}}>D</Tag>}
            {isAI && (
              <Tag color="purple" size="small">AI</Tag>
            )}
            {isMe && <Tag color="blue" style={{marginInline: 4}}>你</Tag>}
          </div>
          <div className="player-chips">💰 {player.chips}</div>
          {player.bet > 0 && <div className="player-bet">下注: {player.bet}</div>}
          {player.folded && <Tag color="red">弃牌</Tag>}
          {player.all_in && <Tag color="orange">ALL IN</Tag>}
        </div>
        {isActive && player.hole_cards?.length === 2 && (
          <div className="player-cards">
            {showCards ? player.hole_cards.map((card, i) => (
              <div key={i} className={`card-small ${card.color}`}>
                <span>{card.rank}{card.suit}</span>
              </div>
            )) : (
              <>
                <div className="card-small card-back"><span>🂠</span></div>
                <div className="card-small card-back"><span>🂠</span></div>
              </>
            )}
          </div>
        )}
      </div>
    );
  };

  const getStageTag = () => {
    const stageMap = {
      preflop: { label: 'PREFLOP', color: 'blue' },
      flop: { label: 'FLOP', color: 'cyan' },
      turn: { label: 'TURN', color: 'purple' },
      river: { label: 'RIVER', color: 'orange' },
      showdown: { label: 'SHOWDOWN', color: 'red' }
    };
    return stageMap[stage] || stageMap.preflop;
  };

  const stageInfo = getStageTag();

  return (
    <div className="poker-table-container">
      <div className="poker-table">
        {/* 午夜酒馆荷官 */}
        <div className="dealer-seat">
          <div className="dealer-avatar">
            <img src={import.meta.env.BASE_URL + 'characters/dealer.jpg'} alt="午夜酒馆荷官" />
          </div>
          <span className="dealer-label">荷官 · 午夜酒馆</span>
        </div>

        <div className="table-stage">
          <Tag color={stageInfo.color} className="stage-tag">{stageInfo.label}</Tag>
          {hand_over && <Tag color="gold">牌局结束</Tag>}
          <Tag color="default">盲注 {small_blind}/{big_blind}</Tag>
        </div>

        <div className="table-pot">
          <span className="pot-icon">🪙</span>
          <span className="pot-amount">{pot}</span>
          <span className="pot-label">底池</span>
        </div>

        <div className="player-seats">
          {players?.map((player, index) => renderPlayer(player, index))}
        </div>

        <div className="board-cards">
          {board?.length > 0 ? (
            board.map((card, index) => renderCard(card, index))
          ) : (
            <div className="board-empty">
              <span>等待发牌...</span>
            </div>
          )}
        </div>

        {!hand_over && (
          <div className="action-buttons">
            {isMyTurn ? (
              <Space size="middle">
                <Button className="action-btn fold" onClick={() => handleAction('fold')}>弃牌</Button>
                {canCheck ? (
                  <Button className="action-btn" onClick={() => handleAction('check')}>过牌</Button>
                ) : (
                  <Button className="action-btn call" onClick={() => handleAction('call')}>
                    跟注 {myCallAmount}
                  </Button>
                )}
                <Button className="action-btn raise" onClick={() => {
                  setRaiseAmount(Math.min(minRaiseTotal, maxRaise));
                  setShowRaiseModal(true);
                }}>加注</Button>
                <Button className="action-btn allin" onClick={() => handleAction('allin')}>ALL IN</Button>
              </Space>
            ) : (
              <div className="waiting-message">
                {hand_over ? '牌局结束' : '等待对手行动...'}
                {players && players[current_player]?.is_ai && (
                  <span className="ai-thinking">🤖 AI思考中...</span>
                )}
              </div>
            )}
          </div>
        )}

        {hand_over && gameState.winner && (
          <div className="hand-result">
            <TrophyOutlined className="result-icon" />
            <span className="result-text">
              {gameState.winner.name} 赢得底池！
            </span>
          </div>
        )}

        {hand_over && (
          <div className="hand-over-actions">
            <button
              type="button"
              className="trial-end-btn"
              onClick={() => setResultModal('trial')}
            >
              🏁 查看本局试炼总结
            </button>
          </div>
        )}
      </div>

      {/* 对局结果弹窗（胜利/平局/弃牌/加注/试炼结束） */}
      <ResultModal
        type={resultModal}
        open={!!resultModal}
        onClose={() => setResultModal(null)}
        trialStats={trialStats}
      />

      <Modal
        title="加注"
        open={showRaiseModal}
        onCancel={() => setShowRaiseModal(false)}
        onOk={handleConfirmRaise}
        okText={`加注到 ${raiseAmount}`}
        cancelText="取消"
        className="raise-modal"
      >
        <div className="raise-content" style={{padding: '10px 0'}}>
          <div className="raise-presets" style={{marginBottom: 16, display: 'flex', gap: 8, flexWrap: 'wrap'}}>
            <Button onClick={() => setRaiseAmount(Math.min(minRaiseTotal, maxRaise))}>最小加注</Button>
            <Button onClick={() => setRaiseAmount(Math.min(myCallAmount + big_blind * 2, maxRaise))}>2x BB</Button>
            <Button onClick={() => setRaiseAmount(Math.min(Math.floor(pot * 0.5) + myCallAmount, maxRaise))}>1/2池</Button>
            <Button onClick={() => setRaiseAmount(Math.min(pot + myCallAmount, maxRaise))}>底池</Button>
            <Button onClick={() => setRaiseAmount(maxRaise)}>ALL IN</Button>
          </div>
          <Slider
            min={minRaiseTotal}
            max={maxRaise}
            value={raiseAmount}
            onChange={setRaiseAmount}
            step={big_blind}
          />
          <div style={{textAlign: 'center', marginTop: 8}}>
            <b>加注到: {raiseAmount}</b> (需额外支付 {Math.max(0, raiseAmount - (me?.bet || 0))})
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default PokerTable;
