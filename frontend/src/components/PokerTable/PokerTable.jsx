import React, { useState, useEffect } from 'react';
import { Button, Space, Card, Tag, Tooltip, Modal } from 'antd';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ThunderboltOutlined, 
  FireOutlined, 
  SafetyOutlined,
  TrophyOutlined 
} from '@ant-design/icons';
import { useGameStore } from '../../store/gameStore';
import './PokerTable.css';

const PokerTable = ({ gameState, playerId }) => {
  const [selectedAction, setSelectedAction] = useState(null);
  const [raiseAmount, setRaiseAmount] = useState(20);
  const [showRaiseModal, setShowRaiseModal] = useState(false);
  const { sendAction, isConnected } = useGameStore();

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

  const { players, board, pot, stage, hand_over, current_player } = gameState;
  
  // 获取当前玩家
  const currentPlayer = players?.find(p => p.id === playerId);
  const isMyTurn = currentPlayer && 
    !hand_over && 
    players[current_player]?.id === playerId &&
    !currentPlayer.folded &&
    !currentPlayer.all_in;

  // 获取AI玩家
  const aiPlayers = players?.filter(p => p.is_ai) || [];

  // 处理行动
  const handleAction = (action, amount = 0) => {
    if (!isMyTurn) {
      return;
    }
    sendAction(action, amount);
    setSelectedAction(action);
  };

  // 渲染卡牌
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

  // 渲染玩家
  const renderPlayer = (player, index) => {
    const isCurrent = players[current_player]?.id === player.id;
    const isMe = player.id === playerId;
    const isAI = player.is_ai;
    const isActive = !player.folded && !player.all_in;

    return (
      <div 
        key={player.id}
        className={`player-seat ${isCurrent ? 'active' : ''} ${isMe ? 'me' : ''}`}
        style={{ 
          position: 'absolute',
          transform: `rotate(${index * 72}deg) translateY(-180px) rotate(-${index * 72}deg)`
        }}
      >
        <div className="player-avatar">
          {isAI ? '🤖' : (isMe ? '🧑‍💻' : '👤')}
          {isCurrent && <div className="active-indicator">●</div>}
        </div>
        <div className="player-info">
          <div className="player-name">
            {player.name}
            {isAI && (
              <Tag color="purple" size="small">
                AI {player.ai_difficulty}
              </Tag>
            )}
            {isMe && <Tag color="blue">你</Tag>}
          </div>
          <div className="player-chips">💰 {player.chips}</div>
          {player.bet > 0 && <div className="player-bet">下注: {player.bet}</div>}
          {player.folded && <Tag color="red">弃牌</Tag>}
          {player.all_in && <Tag color="orange">ALL IN</Tag>}
        </div>
        {isActive && player.hole_cards?.length === 2 && (
          <div className="player-cards">
            {player.hole_cards.map((card, i) => (
              <div key={i} className={`card-small ${card.color}`}>
                <span>{card.rank}{card.suit}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  // 获取阶段标签
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
      {/* 牌桌 */}
      <div className="poker-table">
        {/* 阶段标识 */}
        <div className="table-stage">
          <Tag color={stageInfo.color} className="stage-tag">
            {stageInfo.label}
          </Tag>
          {hand_over && <Tag color="gold">牌局结束</Tag>}
        </div>

        {/* 底池 */}
        <div className="table-pot">
          <span className="pot-icon">🪙</span>
          <span className="pot-amount">{pot}</span>
          <span className="pot-label">底池</span>
        </div>

        {/* 玩家座位 */}
        <div className="player-seats">
          {players?.map((player, index) => renderPlayer(player, index))}
        </div>

        {/* 公共牌区 */}
        <div className="board-cards">
          {board?.length > 0 ? (
            board.map((card, index) => renderCard(card, index))
          ) : (
            <div className="board-empty">
              <span>等待发牌...</span>
            </div>
          )}
        </div>

        {/* 玩家行动按钮 */}
        {!hand_over && (
          <div className="action-buttons">
            {isMyTurn ? (
              <Space size="middle">
                <Button 
                  className="action-btn fold"
                  onClick={() => handleAction('fold')}
                >
                  弃牌
                </Button>
                <Button 
                  className="action-btn call"
                  onClick={() => handleAction('call')}
                >
                  跟注
                </Button>
                <Button 
                  className="action-btn raise"
                  onClick={() => setShowRaiseModal(true)}
                >
                  加注
                </Button>
                <Button 
                  className="action-btn allin"
                  onClick={() => handleAction('allin')}
                >
                  ALL IN
                </Button>
              </Space>
            ) : (
              <div className="waiting-message">
                {hand_over ? '牌局结束' : '等待对手行动...'}
                {aiPlayers.some(p => !p.folded) && (
                  <span className="ai-thinking">🤖 AI思考中...</span>
                )}
              </div>
            )}
          </div>
        )}

        {/* 牌局结果 */}
        {hand_over && gameState.winner && (
          <div className="hand-result">
            <TrophyOutlined className="result-icon" />
            <span className="result-text">
              {gameState.winner.name} 赢得 {gameState.winner.chips} 筹码!
            </span>
          </div>
        )}
      </div>

      {/* 加注弹窗 */}
      <Modal
        title="加注"
        open={showRaiseModal}
        onCancel={() => setShowRaiseModal(false)}
        footer={null}
        className="raise-modal"
      >
        <div className="raise-content">
          <div className="raise-presets">
            <Button onClick={() => setRaiseAmount(20)}>20</Button>
            <Button onClick={() => setRaiseAmount(40)}>40</Button>
            <Button onClick={() => setRaiseAmount(80)}>80</Button>
            <Button onClick={() => setRaiseAmount(160)}>160</Button>
          </div>
          <div className="raise-custom">
            <input 
              type="number" 
              value={raiseAmount}
              onChange={(e) => setRaiseAmount(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="自定义金额"
              className="raise-input"
            />
          </div>
          <Button 
            type="primary" 
            block
            onClick={() => {
              handleAction('raise', raiseAmount);
              setShowRaiseModal(false);
            }}
          >
            确认加注 {raiseAmount}
          </Button>
        </div>
      </Modal>
    </div>
  );
};

export default PokerTable;
