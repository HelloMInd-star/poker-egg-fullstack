![Game‑OS Y.Mine Midnight Tavern](./github-poker-background.jpg)
# Game‑OS · Y.Mine
> Midnight Tavern｜智能体记忆闭环 · 博弈推演世界观

<div align="center">

# ♠️♥️ Poker Face Arena ♦️♣️

### 扑克人格竞技场 · Game-OS V2.5 决策AI中台 · 首个公开可玩 Demo

> **Read your opponent. Read yourself.**
>
> *你的弃牌率，比你更懂你。*

[![MIT License](https://img.shields.io/badge/License-MIT-fbbf24.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![React 18](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![GitHub Pages](https://pages.github.com/)
[![Railway](https://img.shields.io/badge/Railway-Backend-0B0D0E?style=for-the-badge&logo=railway)](https://railway.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

<br/>

> ⚠️ **Entertainment Only / 本项目仅用于 AI 行为模拟演示，不涉及真实货币博弈。**
>
> 所有对局均为虚拟筹码，所有行为数据仅用于人格建模研究。

[🎮 在线体验](https://hellomind-star.github.io/poker-egg-fullstack/) · [📖 API 文档](https://poker-egg-fullstack-production.up.railway.app/docs) · [🧠 三层 AI 架构](#-三层-ai-架构) · [🃏 16 型人格对手](#-四大气质组速览) · [🔌 后端 API](https://poker-egg-fullstack-production.up.railway.app/api/health)

</div>

---

## 🔮 这是什么

**Poker Face Arena（扑克人格竞技场）** 不是一个普通的在线扑克游戏——它是一座**博弈人格训练场**。

在牌桌上，你面对的不是冷冰冰的随机数 AI，而是 **16 种 MBTI 人格** 驱动的虚拟对手：紫人（NF）会用 62%~66% 的诈唬频率诱你上钩，黄人（NT）以 87%~89% 的抗噪能力冷静读牌，蓝人（SJ）用 72%~83% 的弃牌率构筑铜墙铁壁，绿人（SP）则以 66%~81% 的激进度对你穷追猛打。

每一次 all-in、每一次弃牌、每一次被诈唬，都是一次人格照镜子。**它不是在教你打牌，而是在教你看清自己。**

### 为什么不一样

| 普通扑克 AI | Poker Face Arena |
|---|---|
| 单一难度滑块，调整"聪明度" | **三层 AI 架构**：数学层 + 人格层 + 表演层解耦 |
| 行为随机/规则树，风格可预测 | **12 维行为向量**驱动 16 型差异化打法，毫秒级配置切换，不依赖 LLM |
| 盲注/赔率靠玩家心算 | **Kelly Criterion 实时最优投注比例**，三基准风控（0.48 保本 / 0.50 稳态 / 0.68 熔断）|
| 筹码归零无提醒 | **Game-OS 风控层**实时介入，EV 触线即熔断 |
| 单机 Demo，不可玩 | **WebSocket 实时对战**、Vercel + Railway 零成本部署，开箱即玩 |

### 在 Game-OS 体系中的位置

Poker Face Arena 是 **Game-OS V2.5 决策AI中台** 的第一个公开可玩 Demo——它验证了中台的核心假设：

> **"人格建模 + 决策数学"可以跨域迁移。**
>
> 金融风控里的 Kelly 投注与噪声抵抗，在扑克桌上是 EV 计算与读牌；
> 商业谈判里的人格画像与情绪管理，在牌桌上是 tilt 控制与 bluff 频率。
>
> 同一套人格内核，下一个战场可以是加密交易、电商定价、电竞 BP，或你定义的任何博弈场景。

---

## ✨ 核心特性

<div align="center">

| 🃏 **MBTI 16 型人格对手** | 📊 **Kelly 实时风控** | 🔄 **WebSocket 实时对局** |
|---|---|---|
| 12 维行为向量 × 16 型人格，毫秒级配置驱动，零 LLM 延迟 | 实时 EV 计算 + Kelly 最优投注比例，三基准阈值熔断 | 发牌/下注/摊牌全流程 WS 通信，毫秒级牌桌同步 |

| 📈 **战绩与人格画像** | 🧠 **三层 AI 架构解耦** | ⚡ **零成本一键部署** |
|---|---|---|
| 胜率/弃牌率/bluff 捕获率多维统计，牌桌上暴露你的决策人格 | 数学层/人格层/表演层完全解耦，可独立替换升级 | Dockerfile 就绪，Railway + Vercel 双平台零成本部署 |

</div>

---

## 🧠 三层 AI 架构

```
┌─────────────────────────────────────────────────────────────┐
│                     🎭  表演层 (Performer)                    │
│   可选 LLM 驱动的人格化台词 / 嘲讽 / 情绪反应 / 桌面戏剧       │
│   ─ 关闭即退化为纯行为人格，毫秒级响应                         │
├─────────────────────────────────────────────────────────────┤
│                     🎴  人格层 (Persona)                      │
│   PersonaPokerMapper · 12 维 MBTI 行为模型                    │
│   ─ bluffFreq / tiltResist / noiseResist / aggrFactor       │
│   ─ foldFreq / callFreq / raiseFreq / positionBias ...      │
│   ─ 16 型人格配置驱动，无需 LLM，毫秒级切换                    │
├─────────────────────────────────────────────────────────────┤
│                     📐  数学层 (Mathematics)                  │
│   Kelly Criterion · 蒙特卡洛确定性 EV · 手牌强度评估          │
│   ─ 实时最优投注比例 f* = (bp - q) / b                       │
│   ─ 蒙特卡洛枚举对手范围，确定性 EV 计算（非采样估计）          │
│   ─ Game-OS 风控三阈值：0.48 保本 / 0.50 稳态 / 0.68 熔断      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    🃏  Poker Game Engine
               (preflop → flop → turn → river → showdown)
```

| 层级 | 职责 | 核心模块 | 延迟 |
|---|---|---|---|
| 📐 数学层 | EV 计算、Kelly 投注、手牌强度 | `ai_engine.py` + NumPy | < 5ms |
| 🎴 人格层 | 12 维行为向量、MBTI 映射、决策偏差 | `personalities.py` (PersonaPokerMapper) | < 1ms（配置查表） |
| 🎭 表演层 | 台词人格、情绪表演、桌面戏剧 | 可选 LLM 接入（规划中） | 200ms~2s（异步） |

---

## 🃏 四大气质组速览

<div align="center">

### 🔮 NF · 紫人组 — 理想主义者（The Dreamers）

> INFP · INFJ · ENFP · ENFJ

**bluff 62%~66% · tilt 抗性低 · 情绪驱动**

读心者与叙事家。他们把牌局当故事讲，bluff 频率全场最高——不是因为算得准，而是因为**他们真的相信自己能赢**。跟他们打，要警惕那些"故事讲得太圆"的加注；但一旦故事讲崩，他们 tilt 得比谁都快。

---

### 🧪 NT · 黄人组 — 理性主义者（The Analysts）

> INTP · INTJ · ENTP · ENTJ

**noiseResist 87%~89% · 决策逻辑优先 · 情绪绝缘**

冷酷的概率机器。87%+ 的抗噪能力意味着你的表情、你的下注节奏、你特意演出来的"破绽"——他们全都过滤掉了，只看牌和赔率。跟他们打，bluff 基本无效；但他们也会因为过度计算而错过"不合理但赢"的机会。

---

### 🛡️ SJ · 蓝人组 — 护卫者（The Guardians）

> ISTJ · ISFJ · ESTJ · ESFJ

**fold 72%~83% · 极紧 · 风险厌恶**

铜墙铁壁。十把牌里他们能弃七到八把，但一旦他们加注，你最好相信他们真有牌。想从蓝人身上赢筹码，靠 bluff 几乎不可能——你得有耐心，等他们自己犯"按规矩打但规矩错了"的错。

---

### ⚡ SP · 绿人组 — 艺术创造者（The Explorers）

> ISTP · ISFP · ESTP · ESFP

**aggr 66%~81% · 松凶 · 即兴进攻**

牌桌上的野兽。高激进度 + 松入池，他们用加注频率压垮你，用不可预测性折磨你。跟他们打最刺激也最危险——他们可能用 7-2 offsuit 把你 all-in，然后真的赢了。Kelly 风控在绿人桌前是你的保命符。

</div>

---

## 🛠️ 技术栈

### 前端
| 技术 | 用途 |
|---|---|
| **React 18** | UI 框架 |
| **Vite** | 构建工具（HMR 毫秒级） |
| **Zustand** | 轻量状态管理 |
| **Framer Motion** | 动效引擎（发牌/筹码/翻牌动画） |
| **Ant Design 5** | UI 组件库 |
| **Recharts** | 数据可视化（战绩图表） |
| **原生 WebSocket** | 实时通信 |

### 后端
| 技术 | 用途 |
|---|---|
| **FastAPI** | 异步 Web 框架 |
| **Uvicorn** | ASGI 服务器（单 worker 保内存状态） |
| **WebSocket** | 实时牌桌通信 |
| **NumPy** | AI 数学层（EV/蒙特卡洛） |
| **PyJWT + python-jose** | JWT 认证 |
| **passlib + bcrypt** | 密码哈希 |
| **asyncpg** | PostgreSQL 异步驱动（无 DB 时自动降级内存模式） |

### 部署
| 平台 | 用途 | 成本 |
|---|---|---|
| **Vercel** | 前端托管 | 免费额度 |
| **Railway** | 后端 + PostgreSQL | 免费额度（Starter Plan） |
| **Docker** | 容器化部署 | 自建服务器 |

---

## 🚀 本地启动

前置依赖：Node.js ≥ 18、Python ≥ 3.11

```bash
# 克隆仓库
git clone https://github.com/HelloMInd-star/poker-egg-fullstack.git
cd poker-egg-fullstack

# ─── 后端 ───────────────────────────────
cd backend
cp .env.example .env              # 修改 DATABASE_URL / SECRET_KEY
pip install -r requirements.txt
uvicorn app:app --reload --port 5000
# 后端启动后：http://localhost:5000 · API 文档 http://localhost:5000/docs

# ─── 前端（新终端）─────────────────────
cd ../frontend
cp .env.example .env              # 修改 VITE_API_URL / VITE_WS_URL
npm install
npm run dev
# 前端启动后：http://localhost:5173
```

> 💡 **无数据库也能玩**：未配置 `DATABASE_URL` 时后端自动降级为**内存模式**，任意用户名密码均可登录（如 `test` / `123456`），重启后数据清空。
> ⚠️ **单 worker 限制**：游戏状态存于进程内存，生产必须 `--workers 1`，多进程会导致房间状态不一致。多副本部署需引入 Redis（规划中）。

---

## 🌐 部署

### 前端 · Vercel（推荐）

1. Fork 本仓库 → Vercel **New Project** → Import
2. **Root Directory** 设为 `frontend`，Framework 自动识别为 Vite
3. 环境变量：
   - `VITE_API_URL` = 后端 Railway 地址（`https://xxx.up.railway.app`）
   - `VITE_WS_URL`  = 后端 WS 地址（`wss://xxx.up.railway.app`）
4. 仓库已包含 `frontend/vercel.json`，SPA 路由 rewrite 自动生效
5. Deploy → 获得 `*.vercel.app` 域名

### 后端 · Railway（推荐）

1. Railway **New Project** → **Deploy from GitHub repo** → 选本仓库
2. **Root Directory 留空**（仓库根目录，使用根 `Dockerfile`）
3. 添加 PostgreSQL 服务：**+ New** → **Database** → **Add PostgreSQL**，`DATABASE_URL` 自动注入
4. 手动设置环境变量：

| 变量 | 值 | 说明 |
|---|---|---|
| `SECRET_KEY` | 随机字符串 | 生产务必修改 |
| `JWT_ALGORITHM` | `HS256` | JWT 算法 |
| `JWT_EXPIRE_MINUTES` | `10080` | Token 有效期（7天） |
| `ENVIRONMENT` | `production` | 环境标识 |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app` | 逗号分隔的允许源列表 |
| `PORT` | — | Railway 自动注入，无需手动设置 |

5. 部署后在 **Settings → Networking** 生成公共域名，填回前端环境变量
6. 健康检查：`/api/health`（Dockerfile 已配置，超时 10s）

---

## 📡 API 端点

启动后端后访问 `/docs` 查看 Swagger UI，或 `/redoc` 查看 ReDoc。

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/` | 服务信息 |
| `GET` | `/api/health` | 健康检查 |
| `POST` | `/api/auth/register` | 用户注册 |
| `POST` | `/api/auth/login` | 用户登录（form/json 均支持） |
| `GET` | `/api/auth/me` | 当前用户信息 |
| `POST` | `/api/game/create` | 创建牌局 |
| `POST` | `/api/game/{id}/join` | 加入牌局 |
| `POST` | `/api/game/{id}/start` | 开始对局（发牌） |
| `POST` | `/api/game/{id}/action` | 玩家行动（fold / call / raise） |
| `POST` | `/api/game/{id}/ai/add` | 添加 AI 对手 |
| `GET` | `/api/game/{id}` | 获取牌局状态 |
| `GET` | `/api/stats/{playerId}` | 玩家战绩统计 |
| `WS` | `/ws/{game_id}` | WebSocket 实时通信通道 |

---

## 🗺️ 路线图 Roadmap

### ✅ 已完成
- [x] 完整德州扑克流程：preflop → flop → turn → river → showdown
- [x] WebSocket 实时多人牌桌
- [x] Kelly Criterion 实时最优投注比例
- [x] Game-OS 三基准风控阈值（0.48 / 0.50 / 0.68）
- [x] PersonaPokerMapper · 12 维 MBTI 行为模型（16 型人格配置数据就绪）
- [x] JWT 用户系统 + 战绩统计
- [x] Docker 容器化 + Railway/Vercel 零成本部署配置
- [x] ymine 深色科技感 UI（深紫 `#a78bfa` + 霓虹青 `#22d3ee` + 琥珀金 `#fbbf24`）

### 🎯 MVP 进行中
- [ ] 16 型 MBTI 人格对手引擎接入（数据已就绪，`ai_engine.py` 对接中）
- [ ] AI 对手选择界面（选 MBTI 类型上桌）
- [ ] 人格画像面板（对局后生成你的决策人格报告）

### 🔮 规划中
- [ ] 🎭 LLM 表演层（人格化台词 / 嘲讽 / 情绪反应，异步不阻塞决策）
- [ ] Redis 外置状态存储（多 worker / 多副本水平扩展）
- [ ] 人格对战匹配（基于你的决策画像匹配"最克制你"的对手）
- [ ] 锦标赛模式（MTT / SNG）
- [ ] 移动端响应式适配
- [ ] Game-OS 中台化：人格内核跨域输出（金融/电商/电竞场景）
- [ ] 强化学习层（人格 + RL 自适应进化）

---

## 📁 项目结构

```
poker-egg-fullstack/
├── frontend/                     # React 18 + Vite 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── PokerTable/       # 牌桌组件（发牌/下注/摊牌）
│   │   │   ├── Dashboard/        # 仪表盘（EV/Kelly/风控面板）
│   │   │   ├── GameLobby/        # 游戏大厅（创建/加入房间）
│   │   │   ├── Profile/          # 个人资料
│   │   │   └── Stats/            # 战绩统计
│   │   ├── store/gameStore.js    # Zustand 全局状态
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json               # Vercel SPA 配置
│   └── Dockerfile
│
├── backend/                      # FastAPI 后端
│   ├── services/game_engine.py   # 扑克游戏引擎（发牌/比牌/回合管理）
│   ├── ai/
│   │   ├── ai_engine.py          # AI 决策引擎（数学层 + 决策逻辑）
│   │   └── personalities.py      # PersonaPokerMapper · 16 型 MBTI 配置
│   ├── models/
│   │   ├── database.py           # 数据库连接（PG / 内存降级）
│   │   └── schemas.py            # Pydantic 数据模型
│   ├── auth/auth.py              # JWT 认证
│   ├── app.py                    # FastAPI 入口（路由 + WebSocket）
│   ├── requirements.txt
│   └── Dockerfile
│
├── nginx/nginx.conf              # Nginx 反代配置
├── .github/workflows/deploy.yml  # GitHub Actions CI
├── docker-compose.yml
├── Dockerfile                    # 根目录 Dockerfile（Railway 部署用）
├── .env.example
├── LICENSE
└── README.md
```

---

## 🤝 贡献

欢迎 PR、Issue 与人格配置调优建议。

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: add your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 开启 Pull Request

如果你对人格配置参数（bluffFreq/aggrFactor 等）有基于实战的调优建议，尤其欢迎——**16 型人格的行为向量需要大量对局数据校准**。

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源。

---

## 👨‍💻 作者

**Hello.Mind-star（Y.MINE）** · Game-OS V2.5 架构师

- GitHub: [@HelloMInd-star](https://github.com/HelloMInd-star)
- 项目地址: [https://github.com/HelloMInd-star/poker-egg-fullstack](https://github.com/HelloMInd-star/poker-egg-fullstack)

---

<div align="center">

**♠️♥️♦️♣️**

*"The cards don't lie. But the people holding them do."*

*牌不会说谎。但握牌的人会。*

⚠️ **Entertainment Only / 本项目仅用于 AI 行为模拟演示，不涉及真实货币博弈。**

如果你在牌桌上看到了自己——那就是这个项目存在的意义。 ⭐

</div>
