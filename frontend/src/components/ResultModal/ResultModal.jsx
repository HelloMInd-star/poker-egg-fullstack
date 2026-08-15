import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MODAL_DATA } from './modalData';
import './ResultModal.css';

/**
 * 对局结果弹窗 · 涂鸦贴纸风 + 淡紫霓虹发光边框
 * 清冷高级午夜酒馆氛围，无赌场夸张特效
 * type: 'win' | 'push' | 'fold' | 'raise' | 'trial'
 * trialStats: { risk: '保守'|'均衡'|'激进', avgCoef: '0.75' }（仅 trial 需要）
 */
const ResultModal = ({ type, open, onClose, trialStats }) => {
  const data = type ? MODAL_DATA[type] : null;

  return (
    <AnimatePresence>
      {open && data && (
        <motion.div
          className="rm-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <motion.div
            className={`rm-card rm-${type}`}
            initial={{ opacity: 0, scale: 0.92, y: 18 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={{ type: 'spring', stiffness: 280, damping: 24 }}
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-label={data.tag}
          >
            {/* 边角轻微涂鸦线条装饰 */}
            <span className="rm-doodle rm-doodle-tl" aria-hidden="true">✦</span>
            <span className="rm-doodle rm-doodle-tr" aria-hidden="true">⚡</span>
            <span className="rm-doodle rm-doodle-bl" aria-hidden="true">⌁</span>
            <span className="rm-doodle rm-doodle-br" aria-hidden="true">✦</span>

            <div className="rm-body">
              <div className="rm-avatar">
                <img src={import.meta.env.BASE_URL + data.image} alt={data.tag} />
              </div>

              <div className="rm-content">
                <span className="rm-tag">{data.tag}</span>
                <h3 className="rm-title">{data.title}</h3>
                <svg className="rm-underline" viewBox="0 0 120 8" preserveAspectRatio="none" aria-hidden="true">
                  <path d="M2 5 Q 20 1, 40 4 T 78 4 T 118 3" fill="none" stroke="rgba(192,132,252,0.75)" strokeWidth="2" strokeLinecap="round" />
                </svg>

                {type === 'trial' ? (
                  <>
                    <div className="rm-trial-stats">
                      <div className="rm-trial-row">
                        <span className="rm-trial-label">你的风险偏好</span>
                        <b className="rm-trial-value">【{trialStats?.risk || '均衡'}】</b>
                      </div>
                      <div className="rm-trial-row">
                        <span className="rm-trial-label">平均凯利修正系数</span>
                        <b className="rm-trial-value">×{trialStats?.avgCoef ?? '1.00'}</b>
                      </div>
                    </div>
                    <p className="rm-slogan">{data.slogan}</p>
                  </>
                ) : (
                  <p className="rm-text">{data.body}</p>
                )}

                <button type="button" className="rm-btn" onClick={onClose}>
                  {data.button}
                </button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ResultModal;
