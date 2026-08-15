import React, { useState, useMemo, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Tag } from 'antd';
import {
  INTRO_LINES,
  QUESTIONS,
  FINAL_LINES,
  DRINKS,
  TRAIT_REPORTS,
  TAVERN_STORAGE_KEY,
} from './tavernData';
import './MidnightTavern.css';

const BASE = import.meta.env.BASE_URL;
const TYPES = ['INTJ', 'INTP', 'ENTJ', 'ENTP'];

// 观测倾向：得分最高者；平分时不单方面判定，返回 null 交给选酒页
function computeSuggested(scores) {
  const max = Math.max(...TYPES.map((t) => scores[t]));
  const leaders = TYPES.filter((t) => scores[t] === max);
  return leaders.length === 1 ? leaders[0] : null;
}

export default function MidnightTavern() {
  const navigate = useNavigate();
  const [stage, setStage] = useState('intro'); // intro | quiz | drinks | result
  const [qIndex, setQIndex] = useState(0);
  const [scores, setScores] = useState({ INTJ: 0, INTP: 0, ENTJ: 0, ENTP: 0 });
  const [picked, setPicked] = useState(null); // 当前高亮的选项（用于动画过渡）
  const [result, setResult] = useState(null);

  // 进入页面时恢复历史结果（允许直接查看上次结算）
  useEffect(() => {
    try {
      const saved = localStorage.getItem(TAVERN_STORAGE_KEY);
      if (saved) setResult(JSON.parse(saved));
    } catch (_) {}
  }, []);

  const suggested = useMemo(() => computeSuggested(scores), [scores]);

  const handleAnswer = (type) => {
    if (picked) return; // 动画过渡期间锁定，防止连点丢分
    setPicked(type);
    setTimeout(() => {
      setScores((prev) => ({ ...prev, [type]: prev[type] + 1 }));
      setPicked(null);
      if (qIndex < QUESTIONS.length - 1) {
        setQIndex(qIndex + 1);
      } else {
        setStage('drinks');
      }
    }, 380);
  };

  const handleChooseDrink = (drink) => {
    const profile = {
      mbti: drink.type,
      drinkName: drink.name,
      drinkNameEn: drink.nameEn,
      drinkImage: drink.image,
      kellyMode: drink.kellyMode,
      kellyCoefficient: drink.kellyCoefficient,
      scores,
      suggested,
      timestamp: Date.now(),
    };
    localStorage.setItem(TAVERN_STORAGE_KEY, JSON.stringify(profile));
    setResult(profile);
    setStage('result');
  };

  const restart = () => {
    setScores({ INTJ: 0, INTP: 0, ENTJ: 0, ENTP: 0 });
    setQIndex(0);
    setStage('intro');
  };

  return (
    <div className="tavern-page">
      <div className="tavern-bg" />
      <div className="tavern-inner">

        {stage === 'intro' && (
          <div className="tavern-stage fade-in">
            <div className="tavern-scene-wrap">
              <img src={`${BASE}tavern/scene.jpg`} alt="午夜酒馆" className="tavern-scene-img" />
              <div className="tavern-scene-mask" />
            </div>
            <div className="tavern-eyebrow">MIDNIGHT TAVERN</div>
            <h1 className="tavern-title">午夜酒馆・决策者试炼</h1>
            <div className="tavern-divider" />
            <div className="tavern-prose">
              {INTRO_LINES.map((line, i) => (
                <p key={i} className="tavern-line" style={{ animationDelay: `${0.35 * i}s` }}>
                  {line}
                </p>
              ))}
            </div>
            <Button
              size="large"
              className="tavern-cta"
              style={{ animationDelay: `${0.35 * INTRO_LINES.length}s` }}
              onClick={() => setStage('quiz')}
            >
              推门入座 · 开始试炼
            </Button>
            {result && (
              <div className="tavern-history" style={{ animationDelay: '2.4s' }}>
                上次试炼：{result.mbti}｜{result.drinkName}｜修正系数 ×{result.kellyCoefficient}
                <Button type="link" className="tavern-link" onClick={() => setStage('result')}>
                  查看结算卡 →
                </Button>
              </div>
            )}
          </div>
        )}

        {stage === 'quiz' && (
          <div className="tavern-stage fade-in" key={qIndex}>
            <div className="tavern-progress">
              {QUESTIONS.map((q, i) => (
                <span key={q.key} className={`tavern-dot ${i < qIndex ? 'done' : ''} ${i === qIndex ? 'active' : ''}`}>
                  {q.tag}
                </span>
              ))}
            </div>
            <h2 className="tavern-q-title">{QUESTIONS[qIndex].title}</h2>
            <p className="tavern-q-scene">{QUESTIONS[qIndex].scene}</p>
            <div className="tavern-options">
              {QUESTIONS[qIndex].options.map((opt) => (
                <button
                  key={opt.label}
                  className={`tavern-option ${picked === opt.type ? 'picked' : ''}`}
                  onClick={() => handleAnswer(opt.type)}
                >
                  <span className="tavern-option-label">{opt.label}</span>
                  <span className="tavern-option-text">{opt.text}</span>
                </button>
              ))}
            </div>
            <div className="tavern-q-count">{qIndex + 1} / {QUESTIONS.length}</div>
          </div>
        )}

        {stage === 'drinks' && (
          <div className="tavern-stage fade-in">
            <div className="tavern-eyebrow">THE FINAL CALL</div>
            <h2 className="tavern-title-sm">终章・选酒</h2>
            <div className="tavern-prose">
              {FINAL_LINES.map((line, i) => (
                <p key={i} className="tavern-line" style={{ animationDelay: `${0.25 * i}s` }}>
                  {line}
                </p>
              ))}
            </div>
            <div className="tavern-drinks">
              {DRINKS.map((d) => (
                <div
                  key={d.type}
                  className={`tavern-drink-card ${suggested === d.type ? 'suggested' : ''}`}
                  onClick={() => handleChooseDrink(d)}
                >
                  {suggested === d.type && (
                    <div className="tavern-suggest-badge">酒馆窥见的倾向</div>
                  )}
                  <div className="tavern-drink-img-wrap">
                    <img src={`${BASE}tavern/${d.image}`} alt={`${d.name} ${d.nameEn}`} className="tavern-drink-img" />
                  </div>
                  <div className="tavern-drink-body">
                    <div className="tavern-drink-name">
                      {d.name} <span className="tavern-drink-en">{d.nameEn}</span>
                    </div>
                    <Tag className="tavern-drink-type">{d.type}</Tag>
                    <p className="tavern-drink-desc">{d.desc}</p>
                    <p className="tavern-drink-kelly">凯利模式：{d.kellyMode}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {stage === 'result' && result && (
          <div className="tavern-stage fade-in">
            <div className="tavern-eyebrow">YOUR POUR TONIGHT</div>
            <h2 className="tavern-title-sm">结算・今夜归属</h2>

            {/* 分享卡（可截图保存） */}
            <div className="tavern-share-card" id="tavern-share-card">
              <img
                src={`${BASE}tavern/${result.drinkImage}`}
                alt={result.drinkName}
                className="tavern-share-img"
              />
              <div className="tavern-share-overlay">
                <div className="tavern-share-brand">午夜酒馆・决策者试炼</div>
                <div className="tavern-share-drink">{result.drinkName} <span>{result.drinkNameEn}</span></div>
                <div className="tavern-share-mbti">{result.mbti}</div>
                <div className="tavern-share-kelly">凯利修正系数 ×{result.kellyCoefficient}</div>
                <div className="tavern-share-mode">{result.kellyMode}</div>
              </div>
            </div>
            <div className="tavern-share-hint">📸 可截图保存：调酒师人物分享卡</div>

            {/* 结算明细 */}
            <div className="tavern-result-grid">
              <div className="tavern-result-block">
                <div className="tavern-result-label">匹配心智人格</div>
                <div className="tavern-result-value">{result.mbti}</div>
                {result.suggested && result.suggested !== result.mbti && (
                  <div className="tavern-result-note">酒馆观测倾向为 {result.suggested}，你选择了忠于内心</div>
                )}
              </div>
              <div className="tavern-result-block">
                <div className="tavern-result-label">专属凯利风险修正系数</div>
                <div className="tavern-result-value tavern-gold">×{result.kellyCoefficient}</div>
                <div className="tavern-result-note">凯利模式：{result.kellyMode}</div>
              </div>
            </div>

            <div className="tavern-report">
              <div className="tavern-result-label">决策者特质报告</div>
              {TRAIT_REPORTS[result.mbti].map((p, i) => (
                <p key={i}>{p}</p>
              ))}
            </div>

            <div className="tavern-sync-note">
              ✅ 修正系数已全局同步至 Poker Face Arena 模拟器
            </div>

            <div className="tavern-result-actions">
              <Button size="large" className="tavern-cta" onClick={() => navigate('/')}>
                进入 Poker Face Arena · 系数已生效
              </Button>
              <Button size="large" ghost className="tavern-ghost-btn" onClick={restart}>
                重新试炼
              </Button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
