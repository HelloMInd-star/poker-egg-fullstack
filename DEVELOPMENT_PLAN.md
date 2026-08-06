# 🎯 PokerEgg · 金融思维训练平台 — 完整开发方案

> 定位：以德州扑克为载体的**行为金融学实战训练系统**
> 核心卖点：凯利公式仓位管理 + 行为偏误实时纠正 + AI导师个性化教学
> Slogan：**用打扑克的时间，学会投资的本质**

---

## 📋 目录

1. [产品定位与目标](#1-产品定位与目标)
2. [总体架构升级](#2-总体架构升级)
3. [阶段一：MVP（1周，3人日）— AI决策可解释化](#3-阶段一mvp1周3人日-ai决策可解释化)
4. [阶段二：V1（2周，5人日）— 行为偏误检测系统](#4-阶段二v12周5人日-行为偏误检测系统)
5. [阶段三：V2（1个月，10人日）— 关卡教程 + 自适应AI](#5-阶段三v21个月10人日-关卡教程--自适应ai)
6. [阶段四：V3（长期，2~3个月）— CFR纳什AI + LLM导师](#6-阶段四v3长期23个月cfr纳什ai--llm导师)
7. [测试策略](#7-测试策略)
8. [部署与运维](#8-部署与运维)
9. [风险评估与应对](#9-风险评估与应对)
10. [文件改动总清单](#10-文件改动总清单)

---

## 1. 产品定位与目标

### 1.1 目标用户（按优先级）
| 用户分层 | 特征 | 核心痛点 | 付费意愿 |
|----------|------|----------|---------|
| **P0 · 金融系学生** | 211/985 金融、经济、金工专业 | 课堂学了凯利公式、前景理论，但不知道怎么用 | ⭐⭐⭐⭐⭐ |
| **P1 · 新手投资者** | 入市<2年，亏多赚少 | 追涨杀跌、被套死扛，但不知道为什么错 | ⭐⭐⭐⭐ |
| **P2 · 扑克爱好者** | 打德州但不系统 | 想提升技术，同时觉得能迁移到投资 | ⭐⭐⭐ |
| **P3 · 企业培训** | 券商、基金新员工培训 | 需要可量化的投资决策训练工具 | ⭐⭐⭐⭐⭐ (高客单价) |

### 1.2 成功指标（分阶段）
| 阶段 | 指标 | 目标值 |
|------|------|--------|
| MVP | 玩家停留时长 | > 8 分钟（纯娱乐扑克约3~5分钟） |
| V1 | 单局复盘阅读率 | > 60%（点击"查看详细分析"） |
| V2 | 关卡完成率 | > 40%（从第1关打到第5关） |
| V3 | 付费转化率 | > 5%（免费用户 → 付费解锁全部关卡） |

---

## 2. 总体架构升级

### 2.1 架构图（升级后）
```
┌───────────────────────────────────────────────────────────────┐
│                          前端层 (React 18)                       │
│  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌───────────────┐   │
│  │ PokerTable│ │ TeachingPanel│ │ 关卡系统 │ │ 行为画像 Dashboard │   │
│  │  (原有)  │ │   (新增)     │ │  (新增)  │ │   (改造原有)  │   │
│  └────┬─────┘ └──────┬───────┘ └────┬─────┘ └───────┬───────┘   │
│       └──────────────┴──────────────┴────────────────┘           │
│                         │ Zustand Store (改造)                    │
│              新增: decisionQueue / biasReports / lessonProgress  │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP + WebSocket
┌────────────────────────────┴──────────────────────────────────────┐
│                       后端层 (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │                      API 路由层 (app.py 扩展)              │     │
│  │  /api/ai/explain    /api/behavior/analyze                │     │
│  │  /api/lessons/*     /api/profile/behavior                │     │
│  └──────────────────────┬───────────────────────────────────┘     │
│  ┌───────────┐ ┌───────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ GameEngine│ │ PokerAI   │ │BehaviorAnalyzer│ │ LessonEngine │   │
│  │  (原有)   │ │(改造+解释)│ │   (全新)      │ │   (全新)      │   │
│  └─────┬─────┘ └────┬──────┘ └──────┬───────┘ └──────┬───────┘   │
│        └─────────────┴───────────────┴────────────────┘           │
│                    │ Repository 抽象层 (新增)                      │
│     bias_repo / decision_repo / lesson_repo / profile_repo       │
└────────────────────────────┬──────────────────────────────────────┘
                             │
┌────────────────────────────┴──────────────────────────────────────┐
│                    数据层 (PostgreSQL + Redis)                     │
│  新增表: bias_reports / decision_logs / lesson_progress           │
│  Redis缓存: 当前对局实时分析数据（<5分钟过期）                      │
└───────────────────────────────────────────────────────────────────┘
```

### 2.2 分层设计原则（严格遵守）
1. **路由层（app.py / routers/*）**：只做入参校验 → 调用 service → 返回响应
2. **服务层（services/*、ai/*）**：纯业务逻辑，**不依赖 HTTP/FastAPI**，可独立单元测试
3. **Repository层（repositories/*）**：唯一能写数据库的地方，service 通过接口调用
4. **Schema层（models/schemas.py）**：按领域拆分文件，不再堆在一个文件里

---

## 3. 阶段一：MVP（1周，3人日）— AI决策可解释化

> **目标**：让玩家每一步决策都能看到"凯利公式怎么算的"、"AI为什么这么打"
> **验收标准**：玩家对局后停留时长 > 8 分钟

---

### 3.1 功能清单
| # | 功能 | 优先级 |
|---|------|--------|
| 3.1.1 | AI决策附带完整解释（凯利步骤+金融类比+延伸阅读） | P0 |
| 3.1.2 | 玩家每次决策后，显示"凯利建议 vs 你的实际下注"对比 | P0 |
| 3.1.3 | Dashboard 改造：展示凯利计算的完整公式展开过程 | P0 |
| 3.1.4 | 新增"教学模式"开关：开启后每次决策前弹出提示 | P1 |

---

### 3.2 后端改动

#### 📄 新增文件：`backend/schemas/ai_explain.py`
```python
"""
AI决策解释相关的数据模型
MVP阶段：新增 DecisionExplanation / FormulaStep / FinanceAnalogy
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class FormulaStep(BaseModel):
    """公式推导的单一步骤"""
    step_no: int = Field(..., description="步骤编号，从1开始")
    formula: str = Field(..., description="公式表达式，e.g. 'p = 72%'")
    explanation: str = Field(..., description="人类可读解释")
    value: Optional[float] = Field(None, description="计算出的数值结果")

class FinanceAnalogy(BaseModel):
    """金融类比教学"""
    concept: str = Field(..., description="对应的金融概念，e.g. '凯利仓位管理'")
    story: str = Field(..., description="类比小故事/真实投资案例")
    read_more: Optional[str] = Field(None, description="延伸阅读书籍章节")

class DecisionExplanation(BaseModel):
    """AI决策完整解释"""
    # 基础决策信息
    decision_action: str = Field(..., description="fold/check/call/raise/allin")
    decision_amount: int = Field(0, description="下注金额")
    decision_reason: str = Field(..., description="一句话决策理由")

    # 核心数据
    hand_strength: float = Field(..., ge=0, le=1, description="手牌胜率 0~1")
    kelly_ratio: float = Field(..., ge=0, le=1, description="凯利建议仓位比例")
    pot_odds: float = Field(..., description="底池赔率")
    expected_value: float = Field(..., description="期望值(EV)")

    # 教学内容
    formula_steps: List[FormulaStep] = Field(..., description="公式推导步骤列表")
    finance_analogy: FinanceAnalogy = Field(..., description="金融类比")
    warning: Optional[str] = Field(None, description="风险警告")
    teaching_tip: Optional[str] = Field(None, description="教学提示")
```

#### 📄 修改文件：`backend/ai/ai_engine.py`
```python
"""
在 PokerAI 类中新增 3 个方法：
1. decide_with_explanation() — 带解释的决策入口（替代原 decide_action）
2. _build_formula_steps() — 生成公式推导步骤
3. _build_finance_analogy() — 生成金融类比
"""

class PokerAI:
    # ... 原有代码保持不变 ...

    def decide_with_explanation(self, game_state: dict) -> dict:
        """【MVP 新增】返回决策 + 完整教学解释"""
        # Step 1: 用原逻辑计算决策
        decision = self.decide_action(game_state)

        # Step 2: 提取计算中间数据
        hole_cards = game_state["hole_cards"]
        board_cards = game_state["board_cards"]
        pot = game_state["pot"]
        current_bet = game_state["current_bet"]
        my_chips = game_state["my_chips"]
        stage = game_state["stage"]

        # 计算中间量
        all_cards = hole_cards + board_cards
        evaluation = HandEvaluator.evaluate(all_cards) if len(all_cards) >= 5 \
            else {"strength": 0.2 + (len(hole_cards) > 0) * 0.1}
        hand_strength = evaluation["strength"]

        pot_odds = current_bet / (pot + current_bet) if (pot + current_bet) > 0 else 0
        odds = pot / current_bet if current_bet > 0 else float("inf")
        expected_value = (hand_strength * (pot + current_bet)) \
                         - (1 - hand_strength) * current_bet
        kelly_ratio = self._calculate_kelly(pot, current_bet)

        # Step 3: 生成教学内容
        formula_steps = self._build_formula_steps(
            hand_strength, pot, current_bet, odds, kelly_ratio, expected_value
        )
        finance_analogy = self._build_finance_analogy(
            decision["action"], hand_strength, kelly_ratio
        )
        decision_reason = self._build_decision_reason(
            decision, hand_strength, kelly_ratio, expected_value
        )
        warning = self._build_warning(decision, kelly_ratio, current_bet, my_chips)

        return {
            "action": decision["action"],
            "amount": decision.get("amount", 0),
            "explanation": DecisionExplanation(
                decision_action=decision["action"],
                decision_amount=decision.get("amount", 0),
                decision_reason=decision_reason,
                hand_strength=hand_strength,
                kelly_ratio=kelly_ratio,
                pot_odds=pot_odds,
                expected_value=expected_value,
                formula_steps=formula_steps,
                finance_analogy=finance_analogy,
                warning=warning,
                teaching_tip=self._build_teaching_tip(stage, hand_strength)
            ).dict()
        }

    def _build_formula_steps(self, p, pot, bet, odds, kelly, ev) -> List[FormulaStep]:
        """生成凯利公式 + EV 的逐步推导"""
        steps = [
            FormulaStep(
                step_no=1,
                formula=f"胜率 p ≈ {p:.2%}",
                explanation="结合手牌质量 + 公共牌 + 听牌概率估算",
                value=p
            ),
            FormulaStep(
                step_no=2,
                formula=f"赔率 b = 底池¥{pot} / 跟注¥{bet} = {odds:.1f}",
                explanation="冒1块钱的风险，能赢回来多少钱",
                value=odds
            ),
            FormulaStep(
                step_no=3,
                formula=f"凯利 f* = (b·p - q) / b = ({odds:.1f}×{p:.2%} - {1-p:.2%}) / {odds:.1f}",
                explanation="凯利标准公式：最优资金投入比例",
                value=kelly
            ),
            FormulaStep(
                step_no=4,
                formula=f"凯利建议仓位 = {kelly:.2%}",
                explanation="若有¥10000总筹码，这次最多投入 ¥{int(kelly*10000)}",
                value=kelly
            ),
            FormulaStep(
                step_no=5,
                formula=f"EV = p·win - q·lose = {ev:.1f}",
                explanation="长期重复这个决策，每次平均赚多少钱",
                value=ev
            ),
        ]
        return steps

    def _build_finance_analogy(self, action, p, kelly):
        """【核心教学内容】把扑克决策映射到真实投资案例"""
        if action == "raise" and p > 0.6:
            return FinanceAnalogy(
                concept="确定性机会下的重仓出击",
                story="这就像2016年巴菲特买入苹果："
                      "商业模式清晰（强牌）、价格便宜（底池赔率高）、"
                      "凯利建议仓位 25%+。"
                      "巴菲特最终投入了伯克希尔 40% 的仓位在苹果上，5年赚 1600 亿美元。",
                read_more="《巴菲特致股东的信》— 2016 年关于 '集中投资' 的章节"
            )
        elif action == "fold" and p < 0.3:
            return FinanceAnalogy(
                concept="止损纪律 = 免费的看涨期权",
                story="这就像 2022 年木头姐的 ARKK 基金："
                      "当基本面已经恶化（牌力弱）、继续持有只会亏更多时，"
                      "止损不是认输，而是'保留资金等下一个好机会'。"
                      "专业投资者的止损比例通常设定在 10~20% 之间。",
                read_more="《黑天鹅》第13章：'极端斯坦的杠铃策略'"
            )
        elif action == "call":
            return FinanceAnalogy(
                concept="持有观察 = 时间价值",
                story="这就像'持有可转债'：下有债底（跟注成本有限）、"
                      "上有转股期权（公共牌发出来牌力大增）。"
                      "当赔率有利但确定性还不够时，'先跟注看一下'是最优策略。",
                read_more="《期权、期货及其他衍生品》第 10 章：期权交易策略"
            )
        else:
            return FinanceAnalogy(
                concept="概率思维 vs 结果思维",
                story="投资评估的是'做决策时的质量'，而不是'单次结果的盈亏'。"
                      "拿 AA 输给 27 杂色是运气不好，但决策本身是对的。"
                      "重复 1000 次，拿 AA 的人一定赚钱。",
                read_more="《对赌：信息不足时如何做出高明决策》安妮·杜克"
            )

    # ... 辅助方法 _build_decision_reason / _build_warning 省略
    # （按同样模式写即可）
```

#### 📄 修改文件：`backend/app.py`
```python
"""
改动2处：
1. process_ai_turn() 广播 AI 决策时，附带 explanation 字段
2. 新增 POST /api/ai/explain 接口，供玩家主动请求"如果是AI会怎么打"
"""

# === 改动1: process_ai_turn 中广播 explanation ===
async def process_ai_turn(self, game_id: str):
    # ... 原有代码 ...
    ai = self.ai_decision_maker.get_ai(ai_player.ai_difficulty)

    # 把 get_state() 结果转成 ai_state（原有逻辑）...
    # ai_state = { ... }

    # ↓↓↓ 替换原来的 ai.decide_action() ↓↓↓
    decision_with_exp = ai.decide_with_explanation(ai_state)
    decision = {
        "action": decision_with_exp["action"],
        "amount": decision_with_exp["amount"]
    }

    # ... 执行 action ...

    if result["success"]:
        await self.broadcast(game_id, {
            "type": "ai_action",
            "data": {
                "player": ai_player.name,
                "action": decision["action"],
                "amount": decision["amount"],
                "message": result["message"],
                # ↓↓↓ MVP新增：附带解释 ↓↓↓
                "explanation": decision_with_exp["explanation"]
            }
        })
    # ... 其余不变 ...

# === 改动2: 新增路由 /api/ai/explain ===
class AIExplainRequest(BaseModel):
    game_id: str
    player_id: str
    # 当前玩家视角的游戏状态（也可以不传，后端从game_manager查）
    hand_cards: List[dict]
    board_cards: List[dict]
    pot: int
    current_bet: int
    my_chips: int
    stage: str
    ai_difficulty: str = "hard"  # 用哪个难度的AI来做"导师建议"

@app.post("/api/ai/explain")
async def get_ai_explanation(req: AIExplainRequest):
    """【MVP 新增】获取AI导师的决策建议 + 教学解释"""
    ai_maker = game_manager.ai_decision_maker
    ai = ai_maker.get_ai(req.ai_difficulty)

    game_state = {
        "hole_cards": req.hand_cards,
        "board_cards": req.board_cards,
        "pot": req.pot,
        "current_bet": req.current_bet,
        "my_chips": req.my_chips,
        "stage": req.stage,
        "position": "middle"
    }

    result = ai.decide_with_explanation(game_state)
    return {"success": True, "data": result}
```

---

### 3.3 前端改动

#### 📄 修改文件：`frontend/src/components/Dashboard/Dashboard.jsx`
> 目标：把原来"随机数填充"的凯利仪表盘，替换为**真实公式推导 + 可点击展开步骤**

```jsx
// Dashboard.jsx 重写思路
// Step 1: 从 props.gameState 里的 ai_action.explanation 或
//         主动调 /api/ai/explain 获取解释数据
// Step 2: 真实渲染凯利指数、胜率、EV、底池赔率
// Step 3: 新增"展开公式推导"按钮，点击展开步骤列表
// Step 4: 新增"金融类比"小卡片

import React, { useState, useEffect } from 'react';
import { Card, Progress, Tag, Collapse, Steps, Alert, Divider, Typography } from 'antd';
import {
  RiseOutlined, FallOutlined, WarningOutlined,
  BulbOutlined, FundOutlined, CalculatorOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Panel } = Collapse;

const Dashboard = ({ gameState, playerId }) => {
  const [explanation, setExplanation] = useState(null);
  const [teachingMode, setTeachingMode] = useState(true); // 教学模式开关

  // MVP: 每次状态变更时，如果轮到玩家行动，主动拉取AI建议
  useEffect(() => {
    if (!gameState || !playerId) return;

    // 判断是否是玩家的回合
    const currentPlayer = gameState.players?.[gameState.current_player];
    if (currentPlayer && currentPlayer.id === playerId && !currentPlayer.is_ai) {
      fetchAIExplanation();
    }

    // 如果收到 AI action 带 explanation，也展示出来
    if (gameState.latest_ai_explanation) {
      setExplanation(gameState.latest_ai_explanation);
    }
  }, [gameState?.id, gameState?.current_player, playerId]);

  const fetchAIExplanation = async () => {
    try {
      const me = gameState.players.find(p => p.id === playerId);
      const resp = await fetch('/api/ai/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          game_id: gameState.id,
          player_id: playerId,
          hand_cards: me?.hole_cards || [],
          board_cards: gameState.board || [],
          pot: gameState.pot,
          current_bet: Math.max(...gameState.players.map(p => p.bet), 0),
          my_chips: me?.chips || 0,
          stage: gameState.stage
        })
      });
      const data = await resp.json();
      if (data.success) {
        setExplanation(data.data.explanation);
      }
    } catch (e) {
      console.error('拉取AI解释失败', e);
    }
  };

  if (!explanation) {
    return <Card className="dashboard-container"><div className="dashboard-empty">
      <FundOutlined style={{fontSize: 40, opacity: .4}} />
      <p>AI导师正在分析...</p>
    </div></Card>;
  }

  const { hand_strength, kelly_ratio, pot_odds, expected_value,
          formula_steps, finance_analogy, warning, teaching_tip } = explanation;

  const kellyColor = kelly_ratio > 0.2 ? 'green' : kelly_ratio > 0.08 ? 'gold' : 'red';

  return (
    <div className="dashboard-container">
      {/* 顶部：教学模式开关 */}
      <Card size="small" style={{marginBottom: 12}}>
        <Text>🎓 教学模式</Text>
        <Switch
          checked={teachingMode}
          onChange={setTeachingMode}
          style={{marginLeft: 12}}
        />
        <Text type="secondary" style={{marginLeft: 12, fontSize: 12}}>
          开启后每步决策都显示详细推导
        </Text>
      </Card>

      {/* 核心指标卡：凯利仪表盘 */}
      <Card className="dashboard-card" title="📐 凯利仪表盘（真实计算）">
        <div className="kelly-display">
          <div className="kelly-value">
            <span className="kelly-number">{(kelly_ratio * 100).toFixed(1)}%</span>
            <Tag color={kellyColor}>
              {kelly_ratio > 0.2 ? <RiseOutlined/> : <FallOutlined/>}
              {kelly_ratio > 0.2 ? '重仓机会' : kelly_ratio > 0.08 ? '轻仓参与' : '建议观望'}
            </Tag>
          </div>
          <Progress
            percent={kelly_ratio * 100}
            strokeColor={{'0%': '#22c55e', '50%': '#fbbf24', '100%': '#ef4444'}}
            showInfo={false} size="small"
          />
          <div className="kelly-label">
            凯利建议最优仓位
            <Text type="secondary">（长期最大化收益的数学最优解）</Text>
          </div>
        </div>

        <Divider style={{margin: '16px 0'}}/>

        <div className="metrics-grid">
          <div className="metric-item">
            <span className="metric-label">🎴 估算胜率</span>
            <span className="metric-value win">{(hand_strength * 100).toFixed(0)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">🎯 底池赔率</span>
            <span className="metric-value">1 : {pot_odds > 0 ? (1/pot_odds).toFixed(1) : '∞'}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">💰 单次EV</span>
            <span className={`metric-value ${expected_value >= 0 ? 'good' : 'bad'}`}>
              ¥{expected_value.toFixed(0)}
            </span>
          </div>
        </div>
      </Card>

      {/* 公式推导步骤（可折叠展开） */}
      {teachingMode && (
        <Card
          className="dashboard-card"
          title={
            <span>
              <CalculatorOutlined /> 公式推导步骤
              <Tag color="blue" style={{marginLeft: 8}}>点击展开</Tag>
            </span>
          }
        >
          <Collapse ghost>
            <Panel header={`凯利公式 + EV 推导 · 共 ${formula_steps.length} 步`} key="1">
              <Steps
                direction="vertical"
                size="small"
                current={formula_steps.length}
                items={formula_steps.map(step => ({
                  title: <Text strong>{step.formula}</Text>,
                  description: (
                    <div>
                      <Text type="secondary">{step.explanation}</Text>
                      {step.value !== undefined && (
                        <Tag color="purple" style={{marginTop: 4}}>
                          结果 = {typeof step.value === 'number'
                            ? (step.value > 1 ? step.value.toFixed(2) : (step.value*100).toFixed(1) + '%')
                            : step.value}
                        </Tag>
                      )}
                    </div>
                  )
                }))}
              />
            </Panel>
          </Collapse>
        </Card>
      )}

      {/* 金融类比卡 — MVP最有特色的部分 */}
      <Card
        className="dashboard-card finance-card"
        title={<span><BulbOutlined style={{color: '#f59e0b'}}/> 投资思维类比</span>}
      >
        <Tag color="gold" style={{marginBottom: 8}}>
          金融概念：{finance_analogy.concept}
        </Tag>
        <Paragraph style={{margin: '8px 0'}}>
          {finance_analogy.story}
        </Paragraph>
        {finance_analogy.read_more && (
          <Alert
            type="info" showIcon
            message="📚 延伸阅读"
            description={finance_analogy.read_more}
            style={{marginTop: 8, fontSize: 12}}
          />
        )}
      </Card>

      {/* 风险警告 */}
      {warning && (
        <Alert
          type="warning" showIcon
          message="⚠️ 风险提示"
          description={warning}
          style={{marginBottom: 12}}
        />
      )}
    </div>
  );
};

export default Dashboard;
```

#### 📄 修改文件：`frontend/src/store/gameStore.js`
```js
// 在 WebSocket onmessage 里新增 2 个 case:
// 1. 把 ai_action 带的 explanation 存到 gameState.latest_ai_explanation
// 2. 新增 player_decision_compared 消息（后端在玩家决策后返回"凯利建议 vs 实际"对比）

// 在 state 里新增字段:
latestAIExplanation: null,
playerDecisionFeedback: null,

// onmessage 中:
case 'ai_action':
  set(state => ({
    gameState: {
      ...state.gameState,
      latest_ai_explanation: data.explanation || null
    }
  }));
  break;

case 'player_decision_feedback':
  // MVP新增：玩家行动后收到对比反馈
  set({ playerDecisionFeedback: data });
  break;
```

#### 📄 修改文件：`backend/app.py` 玩家行动处补充反馈
```python
# 在 POST /api/game/{id}/action 和 WS action 处理完成后补充：
# ... result = game.process_action(...) 之后 ...

# === MVP 新增：给玩家返回凯利对比反馈 ===
if result["success"]:
    player = game.get_player_by_id(action.player_id)
    if player and not player.is_ai:
        # 重新算一遍凯利建议（这里可以从AI复用逻辑）
        kelly_ref = _compute_player_kelly_reference(player, game)

        actual_ratio = action.amount / player.chips if player.chips > 0 else 0
        feedback = {
            "kelly_suggested_ratio": kelly_ref["kelly_ratio"],
            "kelly_suggested_action": kelly_ref["suggested_action"],
            "actual_action": action.action_type,
            "actual_ratio": actual_ratio,
            "deviation": abs(actual_ratio - kelly_ref["kelly_ratio"]),
            "score": _score_decision(kelly_ref, action),  # 0~100分
            "comment": _generate_comment(kelly_ref, action)
        }

        await game_manager.broadcast(game_id, {
            "type": "player_decision_feedback",
            "data": feedback
        })
```

---

### 3.3 MVP 验收 Checklist
- [ ] 玩家点击"跟注/加注/弃牌"后，Dashboard 弹出决策得分（0~100）
- [ ] AI行动后，Dashboard 能看到 5 步公式推导 + 金融类比故事
- [ ] 点击"公式推导步骤"的折叠面板，能看到每一步的输入、公式、结果
- [ ] 关闭"教学模式"开关后，只显示核心指标（凯利% / 胜率 / EV），不显示推导

---

## 4. 阶段二：V1（2周，5人日）— 行为偏误检测系统

> **目标**：打完 10 局后，系统能告诉你"你有哪些典型的投资行为偏误，它们让你亏了多少钱"
> **验收标准**：70% 玩家在看完行为画像后，表示"原来我投资就是这么亏的"

---

### 4.1 功能清单
| # | 功能 | 优先级 |
|---|------|--------|
| 4.1.1 | 记录玩家**每一步**决策（10局×20步 = 200条样本起步） | P0 |
| 4.1.2 | 检测 5 大核心行为偏误：损失厌恶 / 赌徒谬误 / 过度自信 / 处置效应 / 锚定效应 | P0 |
| 4.1.3 | 生成"投资行为画像"页面，每条偏误附证据+金融影响+修正练习 | P0 |
| 4.1.4 | Stats 页面改造：除了胜率，还要展示凯利一致性、偏误严重程度雷达图 | P1 |

---

### 4.2 后端改动

#### 📄 新增文件：`backend/services/behavior_analyzer.py`
```python
"""
【V1 核心新增】行为金融学偏误检测引擎
输入：玩家的历史决策流（DecisionLog 列表）
输出：BiasReport 列表 + 行为画像（BehaviorProfile）
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict
from enum import Enum
import math

class BiasType(str, Enum):
    LOSS_AVERSION = "损失厌恶 (Loss Aversion)"
    GAMBLERS_FALLACY = "赌徒谬误 (Gambler's Fallacy)"
    OVERCONFIDENCE = "过度自信 (Overconfidence)"
    DISPOSITION_EFFECT = "处置效应 (Disposition Effect)"
    ANCHORING = "锚定效应 (Anchoring Effect)"

class Severity(str, Enum):
    NONE = "无"
    MILD = "轻度"
    MODERATE = "中度"
    SEVERE = "严重"

@dataclass
class DecisionLog:
    """单步决策日志（数据库要存的结构）"""
    hand_id: str
    decision_id: str
    player_id: str
    stage: str                    # preflop/flop/turn/river
    hand_strength: float          # 决策时的牌力
    kelly_suggested_ratio: float  # 凯利建议仓位比例
    kelly_suggested_action: str   # fold/check/call/raise
    actual_action: str            # 玩家实际操作
    actual_bet_ratio: float       # 玩家实际下注占筹码比例
    expected_value: float         # 决策EV
    chips_before: int             # 决策前玩家筹码
    chips_after: int              # 本局结束后玩家总筹码
    hand_result: str              # win/loss/tie
    is_losing_state: bool         # 做决策时玩家是否处于浮亏状态
    consecutive_losses_before: int # 之前连输了几局
    timestamp: float

@dataclass
class BiasReport:
    """单一偏误的检测报告"""
    bias_type: BiasType
    severity: Severity
    evidence_count: int           # 多少次案例支持这个偏误
    evidence_examples: List[Dict] = field(default_factory=list)  # 最典型的3个例子
    financial_impact: str         # 对投资的影响描述
    estimated_annual_loss: float  # 估算年化收益损失%
    fix_exercise: str             # 修正练习建议
    reading: str                  # 延伸阅读

@dataclass
class BehaviorProfile:
    """玩家完整的行为画像"""
    player_id: str
    total_decisions: int
    total_hands: int
    kelly_consistency: float      # 0~1，决策与凯利建议的一致性
    win_rate: float
    bias_reports: List[BiasReport]
    strengths: List[str]
    overall_score: float          # 0~100
    personalized_training_plan: List[str]  # 个性化训练路径


class BehaviorAnalyzer:
    """偏误检测引擎"""

    MIN_SAMPLES = 20  # 至少20个决策样本才开始分析（否则容易误判）

    def __init__(self):
        self.repo = None  # 后续接 repository，MVP可以先用内存列表

    def record_decision(self, log: DecisionLog):
        """记录单步决策（在玩家每次行动后被调用）"""
        if self.repo:
            self.repo.save_decision_log(log)
        else:
            if not hasattr(self, '_memory_logs'):
                self._memory_logs = defaultdict(list)
            self._memory_logs[log.player_id].append(log)

    def analyze(self, player_id: str) -> Optional[BehaviorProfile]:
        """生成行为画像"""
        logs = self._get_logs(player_id)
        if len(logs) < self.MIN_SAMPLES:
            return None  # 样本不足

        # Step 1: 算基本统计量
        total_decisions = len(logs)
        total_hands = len(set(l.hand_id for l in logs))
        win_rate = sum(1 for l in logs if l.hand_result == "win") / total_hands
        kelly_consistency = self._calc_kelly_consistency(logs)

        # Step 2: 逐个检测偏误
        bias_reports: List[BiasReport] = []
        bias_reports.append(self._detect_loss_aversion(logs))
        bias_reports.append(self._detect_gamblers_fallacy(logs))
        bias_reports.append(self._detect_overconfidence(logs))
        bias_reports.append(self._detect_disposition_effect(logs))
        bias_reports.append(self._detect_anchoring(logs))
        # 过滤掉没有检测到的
        bias_reports = [b for b in bias_reports if b.severity != Severity.NONE]
        # 按严重程度排序
        bias_reports.sort(key=lambda b: {
            Severity.SEVERE: 0, Severity.MODERATE: 1, Severity.MILD: 2
        }[b.severity])

        # Step 3: 总结优势 + 综合评分
        strengths = self._identify_strengths(logs, kelly_consistency)
        overall_score = self._calc_overall_score(kelly_consistency, win_rate, bias_reports)

        # Step 4: 个性化训练路径
        plan = self._build_training_plan(bias_reports, kelly_consistency)

        return BehaviorProfile(
            player_id=player_id,
            total_decisions=total_decisions,
            total_hands=total_hands,
            kelly_consistency=kelly_consistency,
            win_rate=win_rate,
            bias_reports=bias_reports,
            strengths=strengths,
            overall_score=overall_score,
            personalized_training_plan=plan
        )

    # ========== 5 大偏误检测算法 ==========

    def _detect_loss_aversion(self, logs: List[DecisionLog]) -> BiasReport:
        """
        检测损失厌恶：
        定义：处于浮亏局面时，本该弃牌的局，玩家却硬跟注（为了"翻本"不愿认亏）
        证据：
          a) is_losing_state=True 时，fold 比例显著低于非亏损状态（低于50%算严重）
          b) 凯利建议 fold 但玩家 call/raise 的比例在亏损状态下特别高
        """
        losing_logs = [l for l in logs if l.is_losing_state]
        normal_logs = [l for l in logs if not l.is_losing_state]

        if len(losing_logs) < 5:
            return BiasReport(BiasType.LOSS_AVERSION, Severity.NONE, 0, [], "", 0, "", "")

        losing_fold_rate = sum(1 for l in losing_logs if l.actual_action == "fold") / len(losing_logs)
        normal_fold_rate = sum(1 for l in normal_logs if l.actual_action == "fold") \
                           / max(len(normal_logs), 1)

        # 凯利建议弃牌，但玩家选择跟注/加注的案例（亏损状态下）
        bad_examples = [
            l for l in losing_logs
            if l.kelly_suggested_action == "fold" and l.actual_action in ("call", "raise")
        ]

        # 严重程度判断
        if losing_fold_rate < 0.25 and len(bad_examples) >= 3:
            severity = Severity.SEVERE
            annual_loss = 6.0
        elif losing_fold_rate < 0.4 and len(bad_examples) >= 2:
            severity = Severity.MODERATE
            annual_loss = 3.5
        elif losing_fold_rate < 0.55:
            severity = Severity.MILD
            annual_loss = 1.5
        else:
            severity = Severity.NONE
            annual_loss = 0

        return BiasReport(
            bias_type=BiasType.LOSS_AVERSION,
            severity=severity,
            evidence_count=len(bad_examples),
            evidence_examples=[
                {
                    "hand_id": l.hand_id,
                    "stage": l.stage,
                    "kelly_action": "建议弃牌",
                    "your_action": f"你选择了{l.actual_action}",
                    "chips_lost": l.chips_before - l.chips_after
                }
                for l in bad_examples[:3]
            ],
            financial_impact=(
                f"亏损局面下你的弃牌率仅 {losing_fold_rate:.0%}，"
                f"比正常局面低 {normal_fold_rate - losing_fold_rate:.0%}。"
                f"这就是'被套死扛'：不愿承认小亏，结果变成大亏。"
                f"真实投资中，这个偏误是散户亏损的第一大原因。"
            ),
            estimated_annual_loss=annual_loss,
            fix_exercise=(
                "🚨 强制止损练习：接下来 20 局，只要浮亏超过总筹码的 15% 且凯利建议弃牌，"
                "必须立刻弃牌。完成 15 次正确操作后，这个偏误将显著改善。"
            ),
            reading="《思考，快与慢》第 26 章 更人性化的前景理论 / "
                    "《股票大作手回忆录》第 7 章 止损是保命符"
        )

    def _detect_gamblers_fallacy(self, logs: List[DecisionLog]) -> BiasReport:
        """
        检测赌徒谬误：
        定义：连输 N 局后，下注比例突然显著放大（认为"该我赢了"，但历史事件独立）
        证据：
          consecutive_losses_before >= 3 时，actual_bet_ratio / 近3局平均下注比 >= 2.0
        """
        examples = []
        for i, l in enumerate(logs):
            if l.consecutive_losses_before >= 3 and i >= 3:
                avg_recent = sum(logs[i-3:i][j].actual_bet_ratio for j in range(3)) / 3
                if avg_recent > 0:
                    ratio = l.actual_bet_ratio / avg_recent
                    if ratio >= 1.8:
                        examples.append((l, ratio))

        if len(examples) < 2:
            return BiasReport(BiasType.GAMBLERS_FALLACY, Severity.NONE, 0, [], "", 0, "", "")

        severity = Severity.SEVERE if len(examples) >= 4 else \
                   Severity.MODERATE if len(examples) >= 3 else Severity.MILD
        annual_loss = {Severity.SEVERE: 4.5, Severity.MODERATE: 2.5, Severity.MILD: 1.0}[severity]

        return BiasReport(
            bias_type=BiasType.GAMBLERS_FALLACY,
            severity=severity,
            evidence_count=len(examples),
            evidence_examples=[
                {
                    "hand_id": ex[0].hand_id,
                    "consecutive_losses": ex[0].consecutive_losses_before,
                    "bet_inflate_ratio": f"{ex[1]:.1f}x",
                    "result": ex[0].hand_result
                }
                for ex, _ in examples[:3]
            ],
            financial_impact=(
                f"检测到 {len(examples)} 次'连输后突然加大下注'的行为。"
                f"每局下注放大 {sum(e[1] for e in examples)/len(examples):.1f} 倍。"
                f"对应投资中的'越跌越补仓，最后满仓套牢'。"
            ),
            estimated_annual_loss=annual_loss,
            fix_exercise=(
                "📏 下注比例铁律练习：设定'单局下注不得超过总筹码的 5%'，"
                "连续 10 局遵守后，可提高到 10%。无论连输多少局，都不能突破上限。"
            ),
            reading="《清醒思考的艺术》第 29 章 赌徒谬误 / "
                    "《漫步华尔街》第 6 章 技术分析与随机漫步"
        )

    def _detect_overconfidence(self, logs: List[DecisionLog]) -> BiasReport:
        """
        检测过度自信：
        定义：牌力中等（hand_strength < 0.6），但下注比例超过凯利建议的 2 倍
        """
        examples = [
            l for l in logs
            if l.hand_strength < 0.6
            and l.kelly_suggested_ratio > 0
            and l.actual_bet_ratio / max(l.kelly_suggested_ratio, 0.001) >= 2.0
            and l.actual_action in ("raise", "allin")
        ]

        ratio = len(examples) / max(len(logs), 1)
        if ratio < 0.05:
            return BiasReport(BiasType.OVERCONFIDENCE, Severity.NONE, 0, [], "", 0, "", "")

        severity = Severity.SEVERE if ratio > 0.15 else \
                   Severity.MODERATE if ratio > 0.10 else Severity.MILD
        annual_loss = {Severity.SEVERE: 5.0, Severity.MODERATE: 3.0, Severity.MILD: 1.2}[severity]

        return BiasReport(
            bias_type=BiasType.OVERCONFIDENCE,
            severity=severity,
            evidence_count=len(examples),
            evidence_examples=[...],  # 同上
            financial_impact="...",
            estimated_annual_loss=annual_loss,
            fix_exercise="🎯 半凯利练习：接下来 30 局，所有下注严格使用'凯利建议 × 0.5'。"
                         "体会'活得久'比'赚得多'更重要。",
            reading="《穷查理宝典》多元思维模型 / 《黑天鹅》如何应对不可预知的未来"
        )

    # --- _detect_disposition_effect（处置效应：赢的拿不住，亏的死扛）
    # --- _detect_anchoring（锚定效应：被之前的下注金额锚定）
    # 按同样模式写，这里省略详细实现

    # ========== 辅助方法 ==========

    def _calc_kelly_consistency(self, logs: List[DecisionLog]) -> float:
        """凯利一致性 = 1 - 平均(实际比例-建议比例)偏差，归一化到 0~1"""
        if not logs:
            return 0.0
        deviations = [abs(l.actual_bet_ratio - l.kelly_suggested_ratio) for l in logs]
        avg_dev = sum(deviations) / len(deviations)
        return max(0.0, 1.0 - avg_dev * 4)  # 偏差 0.25 以上一致性归 0

    def _calc_overall_score(self, kelly, win_rate, biases) -> float:
        """综合评分 = 凯利一致性×60 + 胜率×20 - 偏误扣分"""
        base = kelly * 60 + win_rate * 100 * 0.2
        penalty = sum(
            {"SEVERE": 8, "MODERATE": 4, "MILD": 1}[b.severity.value]
            for b in biases
        )
        return round(max(0.0, min(100.0, base - penalty)), 1)

    def _build_training_plan(self, biases, kelly) -> List[str]:
        """根据检测到的偏误生成个性化训练路径"""
        plan = ["🎓 完成基础关卡 1-3（期望值/凯利公式/底池赔率）"]
        if any(b.bias_type == BiasType.LOSS_AVERSION for b in biases):
            plan.append("🚨 强制止损训练营（20局）")
        if any(b.bias_type == BiasType.GAMBLERS_FALLACY for b in biases):
            plan.append("📏 仓位上限铁律练习（10局）")
        if kelly < 0.5:
            plan.append("🎯 半凯利一致性训练（30局，达到一致性>70%通过）")
        plan.append("📈 完成进阶关卡 4-7（对手建模/行为偏误/资产配置类比）")
        return plan
```

#### 📄 新增文件：`backend/schemas/behavior.py`
```python
"""行为分析相关的 Pydantic Schema"""
from pydantic import BaseModel, Field
from typing import List, Optional

class BiasReportOut(BaseModel):
    bias_type: str
    severity: str
    evidence_count: int
    evidence_examples: List[dict]
    financial_impact: str
    estimated_annual_loss: float
    fix_exercise: str
    reading: str

class BehaviorProfileOut(BaseModel):
    player_id: str
    total_decisions: int
    total_hands: int
    kelly_consistency: float
    win_rate: float
    overall_score: float
    bias_reports: List[BiasReportOut]
    strengths: List[str]
    personalized_training_plan: List[str]
    radar_data: dict  # 前端雷达图用：{凯利一致性, 风险控制, 纪律性, 概率思维, EV思维}
```

#### 📄 新增文件：`backend/repositories/decision_repo.py` + 修改 `database.py`
```python
"""
新增数据库表 decision_logs（在 database._create_tables 里追加）：
"""
await conn.execute("""
    CREATE TABLE IF NOT EXISTS decision_logs (
        id SERIAL PRIMARY KEY,
        hand_id VARCHAR(36) NOT NULL,
        decision_id VARCHAR(36) NOT NULL UNIQUE,
        player_id VARCHAR(36) NOT NULL,
        stage VARCHAR(20) NOT NULL,
        hand_strength REAL NOT NULL,
        kelly_suggested_ratio REAL NOT NULL,
        kelly_suggested_action VARCHAR(10) NOT NULL,
        actual_action VARCHAR(10) NOT NULL,
        actual_bet_ratio REAL NOT NULL,
        expected_value REAL NOT NULL,
        chips_before INTEGER NOT NULL,
        chips_after INTEGER NOT NULL,
        hand_result VARCHAR(10) NOT NULL,
        is_losing_state BOOLEAN NOT NULL,
        consecutive_losses_before INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_decision_logs_player ON decision_logs(player_id);
    CREATE INDEX IF NOT EXISTS idx_decision_logs_hand ON decision_logs(hand_id);
""")
```

#### 📄 新增路由：`backend/app.py`
```python
@app.get("/api/behavior/profile/{player_id}")
async def get_behavior_profile(player_id: str):
    """【V1 新增】获取玩家的行为金融学画像"""
    analyzer = game_manager.behavior_analyzer  # 在 GameManager 初始化时创建
    profile = analyzer.analyze(player_id)

    if not profile:
        return {
            "success": True,
            "data": None,
            "message": f"样本不足，至少需要 {BehaviorAnalyzer.MIN_SAMPLES} 个决策样本。"
                       f"当前已有 {len(analyzer._memory_logs.get(player_id, []))} 个"
        }

    # 组装雷达图数据
    radar = {
        "凯利一致性": round(profile.kelly_consistency * 100, 1),
        "风险控制": round(_calc_risk_control_score(profile.bias_reports), 1),
        "纪律性": round(_calc_discipline_score(profile), 1),
        "概率思维": round(profile.win_rate * 200, 1),  # 50%胜率=100分
        "EV思维": round(_calc_ev_score(profile), 1)
    }

    # 转 Pydantic 输出
    return {
        "success": True,
        "data": BehaviorProfileOut(
            player_id=player_id,
            total_decisions=profile.total_decisions,
            total_hands=profile.total_hands,
            kelly_consistency=profile.kelly_consistency,
            win_rate=profile.win_rate,
            overall_score=profile.overall_score,
            bias_reports=[BiasReportOut(**b.__dict__) for b in profile.bias_reports],
            strengths=profile.strengths,
            personalized_training_plan=profile.personalized_training_plan,
            radar_data=radar
        ).dict()
    }
```

---

### 4.3 前端改动

#### 📄 新增文件：`frontend/src/pages/BehaviorProfile.jsx`
```jsx
/**
 * 【V1 新增】投资行为画像页面
 * 核心内容：
 *   1) 综合评分卡 + 雷达图
 *   2) 行为偏误列表（严重→轻微排序），每条附证据、影响、练习
 *   3) 个性化训练路径时间线
 */
import React, { useEffect, useState } from 'react';
import {
  Card, Progress, Tag, Timeline, Alert, Statistic, Row, Col, Empty, Spin,
  Typography, List, Badge, Divider, Button
} from 'antd';
import {
  TrophyOutlined, WarningOutlined, BulbOutlined, ThunderboltOutlined,
  SolutionOutlined, LineChartOutlined, ArrowRightOutlined
} from '@ant-design/icons';
import {
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer
} from 'recharts';

const { Title, Text, Paragraph } = Typography;

const BehaviorProfile = ({ playerId }) => {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    if (!playerId) return;
    fetchProfile();
  }, [playerId]);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const resp = await fetch(`/api/behavior/profile/${playerId}`);
      const data = await resp.json();
      setProfile(data.data || null);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={{textAlign: 'center', padding: 40}}><Spin size="large"/></div>;
  if (!profile) return (
    <div style={{padding: 40}}>
      <Card>
        <Empty
          description={<div>
            <Title level={4}>📊 还不够数据生成画像</Title>
            <Paragraph>
              行为金融学分析需要至少 <Tag color="blue">20 个决策样本</Tag>
              （约打 10 局牌）。当前样本不足，请先去玩几局再来查看！
            </Paragraph>
            <Button type="primary" size="large">
              <ArrowRightOutlined/> 去玩牌积累数据
            </Button>
          </div>}
        />
      </Card>
    </div>
  );

  const radarSource = Object.entries(profile.radar_data).map(([k, v]) => ({
    subject: k, score: v, fullMark: 100
  }));

  const scoreColor = profile.overall_score >= 80 ? '#22c55e'
                    : profile.overall_score >= 60 ? '#f59e0b' : '#ef4444';

  const severityColor = {
    '严重': 'red', '中度': 'orange', '轻度': 'gold', '无': 'green'
  };

  return (
    <div className="behavior-profile-page" style={{padding: 20, maxWidth: 1400, margin: '0 auto'}}>
      <Title level={2} style={{marginBottom: 24}}>
        <SolutionOutlined style={{color: scoreColor}}/>
        我的投资行为画像
        <Tag color={scoreColor} style={{fontSize: 16, marginLeft: 16, padding: '4px 12px'}}>
          综合得分 {profile.overall_score} / 100
        </Tag>
      </Title>

      {/* 第一行：综合卡 + 雷达图 */}
      <Row gutter={24} style={{marginBottom: 24}}>
        <Col xs={24} md={10}>
          <Card className="score-main-card">
            <Row gutter={16}>
              <Col span={10} style={{textAlign: 'center'}}>
                <Progress
                  type="dashboard"
                  percent={profile.overall_score}
                  strokeColor={scoreColor}
                  format={v => <span style={{fontSize: 32, color: scoreColor}}>{v}</span>}
                  width={180}
                />
                <Text type="secondary">投资决策综合评分</Text>
              </Col>
              <Col span={14}>
                <Row gutter={[0, 16]}>
                  <Col span={12}>
                    <Statistic title="决策样本数" value={profile.total_decisions}
                               prefix={<ThunderboltOutlined/>}/>
                  </Col>
                  <Col span={12}>
                    <Statistic title="总局数" value={profile.total_hands}/>
                  </Col>
                  <Col span={12}>
                    <Statistic title="凯利一致性"
                               value={Math.round(profile.kelly_consistency * 100)}
                               suffix="%" valueStyle={{color: '#1677ff'}}/>
                  </Col>
                  <Col span={12}>
                    <Statistic title="胜率"
                               value={Math.round(profile.win_rate * 100)}
                               suffix="%" valueStyle={{color: '#52c41a'}}/>
                  </Col>
                </Row>
              </Col>
            </Row>

            <Divider style={{margin: '20px 0'}}/>

            <Title level={5} style={{marginTop: 0}}>
              <TrophyOutlined style={{color: '#f59e0b'}}/> 做得好的地方
            </Title>
            <List
              size="small"
              dataSource={profile.strengths}
              renderItem={item => (
                <List.Item style={{padding: '6px 0'}}>
                  <Badge status="success" text={<Text>{item}</Text>}/>
                </List.Item>
              )}
            />
          </Card>
        </Col>

        <Col xs={24} md={14}>
          <Card title="📈 五维能力雷达图" style={{height: '100%'}}>
            <ResponsiveContainer width="100%" height={320}>
              <RadarChart data={radarSource}>
                <PolarGrid stroke="#e5e7eb"/>
                <PolarAngleAxis dataKey="subject" tick={{fontSize: 13}}/>
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{fontSize: 11}}/>
                <Radar name="当前能力" dataKey="score"
                       stroke="#6366f1" fill="#6366f1" fillOpacity={0.4}
                       strokeWidth={2}/>
              </RadarChart>
            </ResponsiveContainer>
            <div style={{marginTop: 8, textAlign: 'center'}}>
              <Tag color="purple">满分 100</Tag>
              <Text type="secondary">：80+ 专业级 · 60+ 熟练 · 40+ 入门 · &lt;40 新手</Text>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 第二行：年化收益损失估算 */}
      <Row gutter={24} style={{marginBottom: 24}}>
        <Col span={24}>
          <Alert
            showIcon type="warning"
            message={
              <span>
                💰 行为偏误估算年化收益损失：
                <b style={{color: '#ef4444', fontSize: 20, marginLeft: 8}}>
                  -{profile.bias_reports.reduce((s, b) => s + b.estimated_annual_loss, 0).toFixed(1)}%
                </b>
              </span>
            }
            description={
              <span>
                这意味着：如果你的年化投资收益本应达到 10%，由于这些行为偏误，
                实际只能拿到 {Math.max(0, 10 - profile.bias_reports.reduce((s, b) => s + b.estimated_annual_loss, 0)).toFixed(1)}%。
                按 10 万本金复利计算，10 年后相差约 ¥
                {(100000 * (Math.pow(1.1, 10) - Math.pow(
                  Math.max(0.01, 1 + (10 - profile.bias_reports.reduce((s, b) => s + b.estimated_annual_loss, 0)) / 100),
                  10))).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
                } 元。
              </span>
            }
          />
        </Col>
      </Row>

      {/* 第三行：偏误列表 */}
      <Title level={3} style={{marginTop: 8}}>
        <WarningOutlined style={{color: '#ef4444'}}/> 检测到的行为偏误
        <Tag color="red" style={{marginLeft: 12}}>{profile.bias_reports.length} 项</Tag>
      </Title>

      <Row gutter={[16, 16]} style={{marginBottom: 24}}>
        {profile.bias_reports.map((bias, idx) => (
          <Col xs={24} lg={12} key={idx}>
            <Card
              className={`bias-card bias-${bias.severity}`}
              title={
                <span>
                  <Tag color={severityColor[bias.severity]} style={{fontSize: 14}}>
                    {bias.severity}
                  </Tag>
                  <Text strong style={{fontSize: 16, marginLeft: 8}}>
                    {bias.bias_type}
                  </Text>
                </span>
              }
              extra={<Tag>证据 {bias.evidence_count} 条</Tag>}
              hoverable
            >
              <Paragraph type="secondary" style={{marginTop: 0}}>
                {bias.financial_impact}
              </Paragraph>

              <Alert
                type="error" showIcon
                message="💰 年化收益损失估算"
                description={`此偏误约导致你的年化收益降低 ${bias.estimated_annual_loss}%`}
                style={{marginBottom: 12}}
              />

              <Title level={5} style={{margin: '12px 0 8px'}}>📋 典型证据</Title>
              <List
                size="small" bordered
                dataSource={bias.evidence_examples}
                renderItem={(ex, i) => (
                  <List.Item>
                    <Text code>#{i+1}</Text>
                    <Text style={{marginLeft: 8}}>
                      {Object.entries(ex).map(([k, v]) => `${k}=${v}`).join(' · ')}
                    </Text>
                  </List.Item>
                )}
              />

              <Divider style={{margin: '16px 0'}}/>

              <Title level={5} style={{margin: '0 0 8px'}}>
                <BulbOutlined style={{color: '#16a34a'}}/> 修正练习
              </Title>
              <Paragraph style={{marginBottom: 8}}>
                {bias.fix_exercise}
              </Paragraph>

              <Text type="secondary">📚 {bias.reading}</Text>
            </Card>
          </Col>
        ))}
      </Row>

      {/* 第四行：个性化训练路径 */}
      <Card title={<span><LineChartOutlined/> 个性化训练路径</span>}>
        <Timeline
          mode="left"
          items={profile.personalized_training_plan.map((step, i) => ({
            color: i === 0 ? '#1677ff' : 'gray',
            dot: i === 0 ? <SolutionOutlined/> : undefined,
            children: <Text strong={i === 0}>{step}</Text>
          }))}
        />
      </Card>
    </div>
  );
};

export default BehaviorProfile;
```

#### 📄 修改文件：`frontend/src/App.jsx` 增加路由
```jsx
// 在路由部分新增：
import BehaviorProfile from './pages/BehaviorProfile';

<Routes>
  {/* ... 原有路由 ... */}
  <Route path="/behavior" element={
    <BehaviorProfile playerId={user?.id || localStorage.getItem('demo_player_id')}/>
  }/>
</Routes>

// 在 Header 菜单里新增一项：
<Menu.Item key="behavior" icon={<SolutionOutlined />}>
  <Link to="/behavior">行为画像</Link>
</Menu.Item>
```

---

### 4.4 V1 验收 Checklist
- [ ] 玩家打满 20 个决策（约 10 局）后，点击"行为画像"能看到完整报告
- [ ] 行为报告中，至少有 2 个偏误检测出具体证据样例
- [ ] 五维雷达图渲染正常，数值 0~100
- [ ] 年化收益损失估算金额显示正确
- [ ] 个性化训练路径第一项被高亮（蓝色）
- [ ] 样本不足 20 时，显示"去玩牌积累数据"的引导页

---

## 5. 阶段三：V2（1个月，10人日）— 关卡教程 + 自适应AI

> **目标**：从"随便玩"变成"系统性训练"，完成率 40%
> 核心：**15 个关卡的教程系统 + AI 导师根据玩家水平自适应难度**

---

### 5.1 关卡系统设计（共 15 关，三大模块）

| 模块 | 关卡 | 名称 | 教学目标（扑克 → 金融） | 通关条件 |
|------|------|------|------------------------|----------|
| **基础** | 1 | 期望值入门 | EV = p·win - q·lose，彩票为什么是负EV | 连续 5 局只做正EV决策 |
| | 2 | 凯利公式仓位 | f* = (bp-q)/b 的直觉理解 | 下注比例在凯利建议 ±10% 内连续 10 局 |
| | 3 | 底池赔率 = 风险收益比 | 赔率 > 所需胜率的倒数才值得参与 | 正确识别 8 次赔率是否划算 |
| | 4 | 止损纪律练习 | 承认小亏 = 买入下一个好机会的看涨期权 | 凯利建议弃牌时 90% 以上执行弃牌 |
| **进阶** | 5 | 半凯利原则 | 现实世界永远"算不准"，5~7折是安全边际 | 连续 15 局下注≤凯利×0.7 |
| | 6 | 对手行为建模 | 从对手下注推断他的牌力范围 = 从市场价格推断基本面 | 正确识别对手加注模式 5/7 次 |
| | 7 | 赌徒谬误免疫 | 历史独立事件不会互相"补偿" | 连输 3 局后下注比例≤前 3 局均值 ×1.2 |
| | 8 | 处置效应纠正 | 截断亏损，让利润奔跑（赢的拿得住，亏的及时走）| 盈利局持有比例>60%，亏损局弃牌比例>70% |
| | 9 | 波动容忍度训练 | 短期 Bad Beat 是噪声，长期看 EV | 连续 3 次 Bad Beat 后仍遵守凯利纪律 |
| **高级** | 10 | 资产配置类比 | 9人桌各位置 = 不同风险等级的资产类别 | 位置-下注策略匹配正确≥80% |
| | 11 | 再平衡策略 | 筹码波动后的仓位再调整 | 3 次强制再平衡操作全部正确 |
| | 12 | 情绪（Tilt）管理 | 连续亏损后的心理暂停 = 市场剧烈波动后的空仓观望 | Tilt 检测触发后正确暂停 |
| | 13 | 锦标赛泡沫期 | 幸存者偏差 vs 风险厌恶 | 正确处理 ICM 压力下的决策 |
| | 14 | 混合纳什策略 | 不可剥削的均衡策略基础 | 通过"AI考官"的不可剥削性测试 |
| | 15 | 综合实战考核 | 与"职业难度AI"打 50 局，综合评分≥75 | 综合评分≥75 + 至少盈利 |

---

### 5.2 后端改动

#### 📄 新增文件：`backend/services/lesson_engine.py`
```python
"""
【V2 核心】关卡系统引擎
职责：
  1. 管理 15 个关卡的配置、通关条件、规则校验
  2. 跟踪玩家进度（已通过哪些关、当前卡在哪一关、哪一关尝试了几次）
  3. 玩家每次决策后，判断是否满足通关条件，触发"关卡通过"事件
"""
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional
from enum import Enum

class DifficultyBand(str, Enum):
    FOUNDATION = "基础"
    INTERMEDIATE = "进阶"
    ADVANCED = "高级"

@dataclass
class LessonCondition:
    """单条通关条件"""
    condition_id: str
    description: str          # 人类可读描述（前端展示）
    metric: str               # 指标名，例如 kelly_accuracy_in_tolerance
    threshold: float          # 阈值
    operator: str = ">="      # ">=" / "<=" / "==" / ">"
    min_samples: int = 1      # 最少样本数（比如"连续10局"就需要10个样本）

@dataclass
class Lesson:
    """单个关卡配置"""
    lesson_id: int            # 1 ~ 15
    title: str
    module: DifficultyBand
    description: str          # 关卡目标长文本
    poker_concept: str        # 扑克知识点
    finance_concept: str      # 对应金融知识点
    story_intro: str          # 开场小故事（渲染代入感）
    ai_difficulty: str        # 本局AI的难度（前几关放水，后几关变难）
    special_ai_mode: Optional[str] = None  # 针对关卡设置的AI特殊模式
    conditions: List[LessonCondition] = field(default_factory=list)
    unlock_next_on_pass: bool = True

@dataclass
class PlayerProgress:
    """玩家关卡进度"""
    player_id: str
    current_lesson: int = 1
    passed_lessons: List[int] = field(default_factory=list)
    attempt_count: Dict[int, int] = field(default_factory=dict)  # 每关尝试次数
    per_lesson_stats: Dict[int, Dict] = field(default_factory=dict)  # 每关积累的统计数据
    best_scores: Dict[int, float] = field(default_factory=dict)  # 每关历史最佳分数


class LessonEngine:
    """关卡引擎"""

    def __init__(self):
        self.lessons = self._build_lesson_configs()
        # 内存版，后续接 repository
        self._progress: Dict[str, PlayerProgress] = {}

    # ============ 配置加载 ============

    def _build_lesson_configs(self) -> Dict[int, Lesson]:
        """构建 15 个关卡的完整配置（这里演示前 5 关，其余按模式补全）"""
        return {
            # ===== 基础模块 =====
            1: Lesson(
                lesson_id=1,
                title="期望值（EV）入门",
                module=DifficultyBand.FOUNDATION,
                description="理解'单次结果'和'决策质量'不是一回事——"
                           "只要期望为正，就算输了也是好决策。",
                poker_concept="Expected Value = p·win - q·lose",
                finance_concept="任何投资先算数学期望，负EV的彩票/赌博坚决不碰",
                story_intro="想象你是一家量化基金的新分析师，老板让你评估一个策略："
                           "60% 概率赚 1 万，40% 概率亏 1 万。你会建议老板做吗？"
                           "打完这一关你就知道答案了。",
                ai_difficulty="easy",
                conditions=[
                    LessonCondition(
                        condition_id="positive_ev_decisions_ratio",
                        description="连续 5 次决策，期望为正的选项选择比例 ≥ 80%",
                        metric="positive_ev_decision_ratio",
                        threshold=0.8,
                        min_samples=5
                    ),
                    LessonCondition(
                        condition_id="no_negative_ev_big_raise",
                        description="绝不在期望明显为负（EV < -¥20）时下重注",
                        metric="max_negative_ev_raise_amount",
                        threshold=20,
                        operator="<="
                    )
                ]
            ),
            2: Lesson(
                lesson_id=2,
                title="凯利公式：数学最优仓位",
                module=DifficultyBand.FOUNDATION,
                description="凯利公式告诉你：面对一个正EV的机会，应该投入总资金的百分之多少。"
                           "投入太少赚得慢，投入太多有破产风险。",
                poker_concept="f* = (bp - q) / b",
                finance_concept="巴菲特20%单票上限、桥水风险平价，本质都是凯利家族策略",
                story_intro="1956 年，贝尔实验室的约翰·凯利发表了《信息率的新解读》，"
                           "推导出了'长期增长率最大化'的资金投入公式。"
                           "索普用它在赌场 21 点和股市上都赚了几十亿美元。"
                           "现在轮到你用它了。",
                ai_difficulty="easy",
                conditions=[
                    LessonCondition(
                        condition_id="kelly_tolerance_10pct_10hands",
                        description="连续 10 局，你的下注比例与凯利建议偏差不超过 ±10%",
                        metric="kelly_accuracy_within_10pct",
                        threshold=1.0,  # 100% 达到
                        min_samples=10
                    )
                ]
            ),
            3: Lesson(...,),  # 底池赔率关卡
            4: Lesson(...,),  # 止损纪律关卡
            5: Lesson(...,),  # 半凯利原则关卡
            # ... 剩余 10 关按同样模式配置 ...
            15: Lesson(
                lesson_id=15,
                title="🏆 综合实战考核",
                module=DifficultyBand.ADVANCED,
                description="和职业难度AI打 50 局，综合评分 ≥ 75 且盈利，即可毕业。",
                poker_concept="综合运用前 14 关学到的全部技能",
                finance_concept="真实投资环境：不确定性 + 对手博弈 + 情绪干扰",
                story_intro="毕业典礼。如果你能通过这一关，说明你的决策质量已经超过了"
                           "市场上 80% 的散户投资者。",
                ai_difficulty="hard",
                conditions=[
                    LessonCondition("overall_score_75", "综合行为评分≥75", "overall_score", 75),
                    LessonCondition("positive_chips", "最终总筹码>初始值", "final_chips", 1000, ">"),
                    LessonCondition("min_50_hands", "至少打完 50 局", "total_hands", 50)
                ]
            )
        }

    # ============ 进度管理 ============

    def start_lesson(self, player_id: str, lesson_id: int) -> Dict:
        """玩家点击某一关"开始挑战""""
        lesson = self.lessons.get(lesson_id)
        if not lesson:
            raise ValueError(f"关卡 {lesson_id} 不存在")

        # 检查前置关卡是否通过
        if lesson_id > 1 and (lesson_id - 1) not in \
           self.get_progress(player_id).passed_lessons:
            return {
                "success": False,
                "message": f"请先通过第 {lesson_id-1} 关",
                "code": "PREV_LESSON_NOT_PASSED"
            }

        # 初始化这一关的统计容器
        progress = self.get_progress(player_id)
        progress.attempt_count[lesson_id] = progress.attempt_count.get(lesson_id, 0) + 1
        progress.per_lesson_stats.setdefault(lesson_id, {
            "decisions": [],
            "hands": [],
            "metrics": {},
            "started_at": ...
        })
        progress.current_lesson = lesson_id

        return {
            "success": True,
            "lesson": lesson,
            "attempt_no": progress.attempt_count[lesson_id],
            # 返回：前端要创建对局时的参数（AI难度、特殊规则等）
            game_config: {
                "ai_difficulty": lesson.ai_difficulty,
                "special_ai_mode": lesson.special_ai_mode
            }
        }

    def record_lesson_decision(self, player_id: str, decision_log):
        """玩家在关卡中做了一次决策 → 累积统计 + 判断是否过关"""
        progress = self.get_progress(player_id)
        lesson_id = progress.current_lesson
        lesson = self.lessons[lesson_id]
        stats = progress.per_lesson_stats[lesson_id]

        # 1) 存入决策列表
        stats["decisions"].append(decision_log)
        # 2) 实时计算各个 condition 的指标
        stats["metrics"] = self._compute_lesson_metrics(lesson, stats)
        # 3) 判断是否全部满足
        passed = self._check_pass_conditions(lesson, stats)
        if passed:
            return self._on_lesson_pass(player_id, lesson, stats)

        return {"in_progress": True, "current_metrics": stats["metrics"]}

    def _compute_lesson_metrics(self, lesson, stats) -> Dict:
        """计算本关定义的各个指标"""
        decisions = stats["decisions"]
        metrics = {}

        # 例：第1关指标 positive_ev_decision_ratio
        if any(c.condition_id == "positive_ev_decision_ratio" for c in lesson.conditions):
            ev_positive_decisions = [d for d in decisions if d.expected_value > 0]
            # 这些正EV决策中，玩家选择了call/raise（参与了正EV机会）的比例
            participated = sum(
                1 for d in ev_positive_decisions if d.actual_action in ("call", "raise", "check")
            )
            metrics["positive_ev_decision_ratio"] = \
                participated / len(ev_positive_decisions) if ev_positive_decisions else 0
            metrics["max_negative_ev_raise_amount"] = max(
                [d.actual_bet_ratio * d.chips_before
                 for d in decisions if d.expected_value < -20 and d.actual_action == "raise"],
                default=0
            )

        # 例：第2关指标 kelly_accuracy_within_10pct
        if any(c.condition_id == "kelly_tolerance_10pct_10hands" for c in lesson.conditions):
            accurate = sum(
                1 for d in decisions
                if abs(d.actual_bet_ratio - d.kelly_suggested_ratio) <= 0.10
                and d.kelly_suggested_ratio > 0.01  # 排除建议几乎不下注的情形
            )
            total_valid = sum(1 for d in decisions if d.kelly_suggested_ratio > 0.01)
            # 指标：最近 10 个决策中，凯利一致性 100%？
            recent_10 = decisions[-10:]
            if len(recent_10) >= 10:
                metrics["kelly_accuracy_within_10pct"] = 1.0 if all(
                    abs(d.actual_bet_ratio - d.kelly_suggested_ratio) <= 0.10
                    for d in recent_10 if d.kelly_suggested_ratio > 0.01
                ) else 0.0
            else:
                metrics["kelly_accuracy_within_10pct"] = None  # 样本不足

        return metrics

    def _check_pass_conditions(self, lesson, stats) -> bool:
        """检查所有条件是否同时满足"""
        metrics = stats["metrics"]
        for cond in lesson.conditions:
            value = metrics.get(cond.metric)
            if value is None:
                return False  # 该指标还没算出来（样本不够）
            if cond.operator == ">=" and not (value >= cond.threshold):
                return False
            if cond.operator == "<=" and not (value <= cond.threshold):
                return False
        return True

    def _on_lesson_pass(self, player_id, lesson, stats) -> Dict:
        """关卡通过的善后处理"""
        progress = self.get_progress(player_id)
        if lesson.lesson_id not in progress.passed_lessons:
            progress.passed_lessons.append(lesson.lesson_id)
        # 算一个"本关得分"（0~100），存 best_scores
        score = self._score_lesson_performance(lesson, stats)
        progress.best_scores[lesson.lesson_id] = max(
            progress.best_scores.get(lesson.lesson_id, 0), score
        )
        return {
            "passed": True,
            "lesson_id": lesson.lesson_id,
            "score": score,
            "unlocked_next_lesson_id": lesson.lesson_id + 1
                                    if lesson.unlock_next_on_pass and lesson.lesson_id < 15
                                    else None,
            "certificate_url": f"/certificate/{lesson.lesson_id}" if lesson.lesson_id == 15 else None
        }
```

#### 📄 新增路由 & Pydantic Schema
```python
# backend/schemas/lesson.py
class StartLessonRequest(BaseModel):
    player_id: str
    lesson_id: int

class LessonOut(BaseModel):
    lesson_id: int
    title: str
    module: str
    description: str
    poker_concept: str
    finance_concept: str
    story_intro: str
    conditions: List[dict]
    ai_difficulty: str

# backend/app.py 新增路由
@app.get("/api/lessons")
async def list_lessons(player_id: str):
    """列出所有关卡 + 玩家的完成状态、每关最佳分数"""
    engine = game_manager.lesson_engine
    progress = engine.get_progress(player_id)
    lessons = []
    for lid, l in sorted(engine.lessons.items()):
        lessons.append({
            **LessonOut(
                lesson_id=l.lesson_id, title=l.title, module=l.module,
                description=l.description, poker_concept=l.poker_concept,
                finance_concept=l.finance_concept, story_intro=l.story_intro,
                conditions=[c.__dict__ for c in l.conditions],
                ai_difficulty=l.ai_difficulty
            ).dict(),
            "passed": lid in progress.passed_lessons,
            "attempts": progress.attempt_count.get(lid, 0),
            "best_score": progress.best_scores.get(lid, 0),
            "locked": lid > 1 and (lid - 1) not in progress.passed_lessons
        })
    return {"success": True, "data": lessons}

@app.post("/api/lessons/start")
async def start_lesson(req: StartLessonRequest):
    result = game_manager.lesson_engine.start_lesson(req.player_id, req.lesson_id)
    return {"success": result.get("success", True), "data": result}
```

---

### 5.3 自适应AI升级（V2 部分）
```python
"""backend/ai/ai_engine.py 新增 AdaptivePokerAI（继承 PokerAI）"""
class AdaptivePokerAI(PokerAI):
    def __init__(self, base_difficulty="medium"):
        super().__init__(base_difficulty)
        self.mode = "tutorial"  # tutorial / practice / challenge
        self.target_biases = []  # 针对玩家的哪些偏误进行针对性训练

    def adapt_to_behavior_profile(self, profile: BehaviorProfile):
        """根据玩家的行为画像调整AI策略"""
        kelly = profile.kelly_consistency
        # 新手：放水（降低 aggression，降低 bluff）
        if kelly < 0.5:
            self.mode = "tutorial"
            self.aggression = 0.1
            self.bluff_frequency = 0.02
        # 熟练：标准
        elif kelly < 0.75:
            self.mode = "practice"
            self.aggression = 0.3
            self.bluff_frequency = 0.12
        # 高手：真的上强度
        else:
            self.mode = "challenge"
            self.aggression = 0.6
            self.bluff_frequency = 0.25

        # 针对性训练：如果有损失厌恶，AI就频繁诈唬逼他做弃牌决策
        bias_types = {b.bias_type for b in profile.bias_reports}
        if BiasType.LOSS_AVERSION in bias_types:
            self.strategy_override = "LOSS_AVERSION_TRAINING"
            self.aggression = min(self.aggression + 0.15, 0.9)
        if BiasType.OVERCONFIDENCE in bias_types:
            self.strategy_override = "OVERCONFIDENCE_TRAP"
            self.aggression -= 0.1  # 前期示弱，强牌慢打引诱
```

---

### 5.4 前端：关卡系统页面

#### 📄 新增文件：`frontend/src/pages/Lessons.jsx`
```jsx
/**
 * 关卡地图页（15关线性进度 + 模块分组）
 * 每个关卡卡片展示：锁状态/通过徽章/最佳分数/尝试次数/开始按钮
 */
import React, { useState, useEffect } from 'react';
import {
  Card, Row, Col, Tag, Button, Progress, Badge, Statistic, Empty,
  Modal, Divider, Typography, Timeline, Steps, message
} from 'antd';
import {
  LockOutlined, CheckCircleOutlined, PlayCircleOutlined, TrophyOutlined,
  StarOutlined, BookOutlined, LineChartOutlined
} from '@ant-design/icons';
const { Title, Paragraph, Text } = Typography;

const Lessons = ({ playerId }) => {
  const [lessons, setLessons] = useState([]);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [starting, setStarting] = useState(false);

  useEffect(() => { fetchLessons(); }, [playerId]);

  const fetchLessons = async () => {
    const r = await fetch(`/api/lessons?player_id=${playerId}`);
    const d = await r.json();
    setLessons(d.data || []);
  };

  const moduleGroups = {
    '基础': lessons.filter(l => l.module === '基础'),
    '进阶': lessons.filter(l => l.module === '进阶'),
    '高级': lessons.filter(l => l.module === '高级'),
  };
  const passed = lessons.filter(l => l.passed).length;
  const overallProgress = lessons.length ? (passed / lessons.length * 100) : 0;

  const handleStart = async () => {
    setStarting(true);
    try {
      const r = await fetch('/api/lessons/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({player_id: playerId, lesson_id: selectedLesson.lesson_id})
      });
      const d = await r.json();
      if (d.success && d.data.success) {
        message.success(`开始挑战第 ${selectedLesson.lesson_id} 关！`);
        setModalOpen(false);
        // 跳转到游戏大厅，并携带参数进入"关卡模式"
        navigate(`/lobby?lesson_id=${selectedLesson.lesson_id}&mode=lesson`);
      } else {
        message.error(d.data?.message || '启动失败');
      }
    } finally {
      setStarting(false);
    }
  };

  const renderLessonCard = (lesson) => {
    const isPassed = lesson.passed;
    const isLocked = lesson.locked;
    const badgeColor = isPassed ? 'green' : isLocked ? 'default' : 'blue';
    const titleIcon = isPassed ? <CheckCircleOutlined style={{color: '#52c41a'}}/>
                    : isLocked ? <LockOutlined/> : <BookOutlined style={{color: '#1677ff'}}/>;
    return (
      <Col xs={24} sm={12} lg={8} xl={6} key={lesson.lesson_id}>
        <Card
          hoverable={!isLocked}
          className={`lesson-card lesson-${isPassed ? 'passed' : isLocked ? 'locked' : 'active'}`}
          onClick={() => !isLocked && (setSelectedLesson(lesson), setModalOpen(true))}
        >
          <Badge.Ribbon
            text={isPassed ? '已通关' : isLocked ? '未解锁' : '进行中'}
            color={badgeColor}
          >
            <div>
              <Title level={5} style={{margin: 0}}>
                {titleIcon}
                <span style={{marginLeft: 8}}>
                  第{lesson.lesson_id}关 · {lesson.title}
                </span>
              </Title>
              <Tag color="geekblue" style={{margin: '8px 0'}}>{lesson.module}</Tag>

              <Paragraph ellipsis={{rows: 2}} type="secondary" style={{fontSize: 13, margin: '8px 0'}}>
                {lesson.description}
              </Paragraph>

              <Row gutter={8}>
                <Col span={12}>
                  <Text type="secondary" style={{fontSize: 12}}>最佳分数</Text>
                  <div style={{fontSize: 20, fontWeight: 700, color: isPassed ? '#16a34a' : '#94a3b8'}}>
                    {lesson.best_score || '--'}
                  </div>
                </Col>
                <Col span={12}>
                  <Text type="secondary" style={{fontSize: 12}}>尝试次数</Text>
                  <div style={{fontSize: 20, fontWeight: 700}}>
                    {lesson.attempts || 0}
                  </div>
                </Col>
              </Row>

              <Button
                type={isPassed ? 'default' : 'primary'}
                block
                disabled={isLocked}
                icon={isPassed ? <StarOutlined/> : <PlayCircleOutlined/>}
                style={{marginTop: 12}}
                onClick={(e) => {
                  e.stopPropagation();
                  if (!isLocked) { setSelectedLesson(lesson); setModalOpen(true); }
                }}
              >
                {isPassed ? '重新挑战' : isLocked ? '先通关上一关' : '开始挑战'}
              </Button>
            </div>
          </Badge.Ribbon>
        </Card>
      </Col>
    );
  };

  return (
    <div style={{padding: 24, maxWidth: 1500, margin: '0 auto'}}>
      {/* 顶部总进度条 */}
      <Card style={{marginBottom: 24}}>
        <Row gutter={24} align="middle">
          <Col md={6}>
            <Statistic title="学习进度" value={passed} suffix={`/ ${lessons.length} 关`}
                       prefix={<TrophyOutlined/>}/>
          </Col>
          <Col md={12}>
            <Progress percent={overallProgress} strokeColor="#6366f1" trailColor="#e0e7ff" size="large"/>
          </Col>
          <Col md={6} style={{textAlign: 'right'}}>
            <Button type="primary" size="large">
              <LineChartOutlined/> 查看我的课程报告
            </Button>
          </Col>
        </Row>
      </Card>

      {/* 按模块分组的关卡列表 */}
      {Object.entries(moduleGroups).map(([moduleName, list]) => (
        <div key={moduleName} style={{marginBottom: 32}}>
          <Title level={3} style={{margin: '16px 0'}}>
            {moduleName === '基础' ? '📗 ' : moduleName === '进阶' ? '📘 ' : '📕 '}
            {moduleName}模块
            <Tag color="purple" style={{marginLeft: 12}}>{list.length} 关</Tag>
          </Title>
          <Row gutter={[16, 16]}>{list.map(renderLessonCard)}</Row>
          <Divider/>
        </div>
      ))}

      {/* 关卡详情弹窗 */}
      <Modal
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        title={
          selectedLesson && `第 ${selectedLesson.lesson_id} 关 · ${selectedLesson.title}`
        }
        footer={[
          <Button key="cancel" onClick={() => setModalOpen(false)}>稍后再说</Button>,
          <Button key="start" type="primary" size="large"
                  icon={<PlayCircleOutlined/>}
                  loading={starting} onClick={handleStart}>
            开始挑战
          </Button>
        ]}
        width={720}
      >
        {selectedLesson && (
          <div>
            <Alert
              type="info" showIcon
              message={
                <span>
                  🎴 扑克概念：<b>{selectedLesson.poker_concept}</b>
                  <Divider type="vertical"/>
                  💼 金融迁移：<b>{selectedLesson.finance_concept}</b>
                </span>
              }
              style={{marginBottom: 16}}
            />

            <Title level={5}>🎯 关卡目标</Title>
            <Paragraph>{selectedLesson.description}</Paragraph>

            <Title level={5}>📖 开场故事</Title>
            <Paragraph style={{background: '#fafafa', padding: 12, borderRadius: 8}}>
              {selectedLesson.story_intro}
            </Paragraph>

            <Title level={5}>✅ 通关条件（全部满足）</Title>
            <Steps
              direction="vertical" size="small"
              current={-1}
              items={selectedLesson.conditions.map(c => ({
                title: <Text strong>{c.description}</Text>,
                description: (
                  <Tag color="blue">
                    指标 {c.metric} {c.operator} {typeof c.threshold === 'number'
                      && c.threshold < 1 ? (c.threshold*100).toFixed(0)+'%' : c.threshold}
                    {c.min_samples > 1 && ` · 至少 ${c.min_samples} 样本`}
                  </Tag>
                )
              }))}
            />
          </div>
        )}
      </Modal>
    </div>
  );
};
export default Lessons;
```

---

## 6. 阶段四：V3（长期，2~3个月）— CFR纳什AI + LLM导师

> 本阶段属于"专业级增强"，只在 V2 跑通数据后再做。这里只给方向和关键架构。

### 6.1 CFR（反事实后悔最小化）AI 实现路径
```
1) 用 Python 实现简化版 Vanilla CFR（针对 Heads-up 单挑德州，状态空间约 10^8，可接受）
2) 离线自博弈训练 1,000,000 局 → 得到各信息集的平均策略
3) 存储格式：JSON 或 SQLite，key = "信息集（手牌+公共牌+下注历史的抽象）"
4) 运行时查表：玩家面临决策时，从预计算策略中按概率采样
5) 效果：AI 达到"不可剥削"级别，即无论对手怎么打，AI 的EV≥0
```

### 6.2 LLM 导师接入
```
1) 在 DecisionExplanation 增加 open_question 字段
2) 前端在"金融类比"卡底部加"问AI导师更多..."输入框
3) 新增 POST /api/ai/chat，将"当前对局上下文+玩家问题"拼装成 prompt
4) 调用 DeepSeek / 通义千问 / GPT，返回自然语言解释
5) 核心 Prompt 设计：
   """
   你是一位行为金融学导师+职业扑克教练。
   当前对局情况：{game_state_json}
   凯利分析结果：{formula_steps_json}
   学生问：{user_question}
   请用【投资案例 + 扑克实战 + 可操作建议】三段式回答，
   并引用 1 本经典书籍的具体章节。
   避免空洞鸡汤，要具体、可执行、数字说话。
   """
```

---

## 7. 测试策略

### 7.1 单元测试（必须，覆盖率 > 80%）
| 模块 | 测试文件 | 覆盖点 |
|------|----------|--------|
| 手牌评估 | `tests/test_hand_evaluator.py` | 10种牌型 × 边界情况（皇家同花顺、A-2-3-4-5 小顺子） |
| 凯利计算 | `tests/test_kelly_formula.py` | 胜率/赔率边界、0值、负数、半凯利 |
| 偏误检测 | `tests/test_behavior_analyzer.py` | 构造人工样本，验证 5 种偏误在特定输入下必然检出 |
| 关卡条件 | `tests/test_lesson_engine.py` | 人工喂 decision_log 列表，验证"通过/不通过"判断正确性 |

### 7.2 集成测试
- `tests/integration/test_full_game.py`：模拟"玩家创建对局 → 打 3 个阶段 → AI行动 → 结算"完整链路
- `tests/integration/test_behavior_flow.py`：模拟 20 局决策 → 调用 `/behavior/profile` → 检查返回结构

### 7.3 前端自动化（Playwright）
- 验证首页 → 登录 → 开始第 1 关 → 做 5 个决策 → 弹出"决策得分"
- 验证样本不足 20 时"行为画像页"显示引导

---

## 8. 部署与运维

### 8.1 升级后的 docker-compose.yml 关键改动
```yaml
services:
  # 新增 Celery worker（V3 做离线 CFR 训练、LLM 异步调用）
  celery_worker:
    build: {context: ./backend, target: production}
    command: celery -A tasks worker --loglevel=info
    depends_on: [redis, postgres]

  # PostgreSQL 数据卷定期备份（pg_dump）
  # Grafana + Prometheus 做监控：API 响应时间、决策数量、活跃玩家
```

### 8.2 数据库迁移
- 引入 Alembic，首次迁移创建：`decision_logs` / `behavior_reports` / `lesson_progress` 三张表
- 每次 schema 变更，执行 `alembic revision --autogenerate` + 代码评审后再 `upgrade head`

---

## 9. 风险评估与应对

| 风险 | 概率 | 影响 | 应对策略 |
|------|------|------|----------|
| **"就是个打牌游戏"，用户没get到金融价值** | 高 | 高 | 强制新手引导"第1关必须先看'为什么用扑克学投资'视频+答题"；首页直接放"年化损失估算器" |
| **行为偏误检测样本冷启动** | 中 | 中 | 新增"快速测评"模式：10 道情景选择题，5 分钟出初始画像（无需打满 10 局） |
| **AI 难度曲线调不好** | 中 | 高 | 前 5 关做 A/B 测试（2组不同AI参数），看哪组通关率在 50~70% 之间（最佳难度） |
| **合规风险（被误认为赌博）** | 低 | 极高 | 全站点禁用任何"充值/兑换/真金白银"字眼；筹码永久不可提现；每局重置筹码；FAQ 明示"纯教学用途" |
| **PostgreSQL 压力过大** | 低 | 中 | 决策日志写入量大 → 走 Redis 队列 + 异步批量落库；`decision_logs` 按月分区 |

---

## 10. 文件改动总清单

| 阶段 | 操作 | 路径 | 说明 |
|------|------|------|------|
| **MVP** | 新增 | `backend/schemas/ai_explain.py` | 决策解释 Schema |
| MVP | 修改 | `backend/ai/ai_engine.py` | `decide_with_explanation()` + 金融类比生成 |
| MVP | 修改 | `backend/app.py` | `/api/ai/explain` 路由 + 广播 explanation 字段 |
| MVP | 修改 | `frontend/src/components/Dashboard/Dashboard.jsx` | 真实凯利计算 + 公式步骤 + 金融类比卡 |
| MVP | 修改 | `frontend/src/store/gameStore.js` | explanation 状态 + player_decision_feedback |
| **V1** | 新增 | `backend/services/behavior_analyzer.py` | 5 种偏误检测引擎 |
| V1 | 新增 | `backend/schemas/behavior.py` | 行为画像输出 Schema |
| V1 | 新增 | `backend/repositories/decision_repo.py` | 决策日志持久化 |
| V1 | 修改 | `backend/models/database.py` | `decision_logs` 表 DDL |
| V1 | 修改 | `backend/app.py` | `/api/behavior/profile/*` 路由 |
| V1 | 新增 | `frontend/src/pages/BehaviorProfile.jsx` | 行为画像页（评分卡+雷达+偏误+训练路径） |
| V1 | 修改 | `frontend/src/App.jsx` | 新增路由 + 导航菜单 |
| **V2** | 新增 | `backend/services/lesson_engine.py` | 15 关配置 + 条件校验 |
| V2 | 新增 | `backend/schemas/lesson.py` | 关卡相关 Schema |
| V2 | 修改 | `backend/ai/ai_engine.py` | `AdaptivePokerAI` 根据画像调整 |
| V2 | 修改 | `backend/app.py` | `/api/lessons/*` 路由 |
| V2 | 新增 | `frontend/src/pages/Lessons.jsx` | 关卡地图页 |
| V2 | 新增 | `frontend/src/components/Lesson/LessonHUD.jsx` | 对局中显示"本关进度条" |
| **V3** | 新增 | `backend/ai/cfr_engine.py` | CFR 纳什均衡 AI |
| V3 | 新增 | `backend/services/llm_tutor.py` | LLM 导师 prompt 拼装 + 异步调用 |
| V3 | 修改 | `backend/app.py` | `/api/ai/chat` 流式 WebSocket 路由 |

---

> **文档版本**：v1.0 (2026-08-06)
> **下次评审节点**：MVP 完成后（约 1 周），重新评估 V1/V2 的需求优先级
