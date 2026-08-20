![Game-OS Y.Mine · Midnight Tavern](./github-poker-background.jpg)

<div align="center">

# 🌃 MIDNIGHT TAVERN · 午夜酒馆

### 人格化娱乐宇宙 — V1 房间「Poker Egg 人格牌桌」营业中 · MBTI × Kelly × 三层 AI 架构

**Game-OS V2.5 决策AI中台 · 首个公开版本 V1**

> **Read your opponent. Read yourself.**
>
> *你的弃牌率，比你更懂你。*

**[简体中文](./README.md)** · [English](./README_EN.md)

[![Version](https://img.shields.io/badge/Version-V1.0.0-a78bfa?style=for-the-badge)](https://github.com/HelloMInd-star/poker-egg-fullstack/releases)
[![MIT License](https://img.shields.io/badge/License-MIT-fbbf24.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![React 18](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Live-22d3ee?style=for-the-badge&logo=github&logoColor=white)](https://hellomind-star.github.io/poker-egg-fullstack/)
[![Railway](https://img.shields.io/badge/Railway-Backend-0B0D0E?style=for-the-badge&logo=railway)](https://railway.app/)
[![MBTI](https://img.shields.io/badge/MBTI-16_Personas-ef4444?style=for-the-badge)](./README_EN.md)

> ⚠️ **Entertainment Only / 本项目仅用于 AI 行为模拟演示，不涉及真实货币博弈。**
>
> 所有对局均为虚拟筹码，所有行为数据仅用于人格建模研究。

[🎮 在线体验](https://hellomind-star.github.io/poker-egg-fullstack/) · [📖 API 文档](https://poker-egg-fullstack-production.up.railway.app/docs) · [🧠 三层 AI 架构](#-三层-ai-架构) · [🃏 四大气质组](#-四大气质组速览) · [🗺️ 路线图](#️-路线图-roadmap)

</div>

---

## 🔮 这是什么

**MIDNIGHT TAVERN 午夜酒馆** 不是一个游戏 Demo——它是一座正在生长的**人格化娱乐宇宙**。

酒馆里每个房间都住着同一套引擎：**人格建模 + 决策数学**。扑克、调酒、音乐，只是同一颗人格内核披上不同场景的外衣。

推开酒馆大门，黑胶唱片在转，霓虹在杯壁上反光。第一个房间「**Poker Egg 人格牌桌**」已经开业——你坐下的这张牌桌，对面不是冷冰冰的随机数 AI，而是 **16 种 MBTI 人格**驱动的虚拟对手：紫人（NF）用 62%~66% 的诈唬频率诱你上钩，黄人（NT）以 87%~89% 的抗噪能力冷静读牌，蓝人（SJ）用 72%~83% 的弃牌率构筑铜墙铁壁，绿人（SP）以 66%~81% 的激进度穷追猛打。

每一次 all-in、每一次弃牌、每一次被诈唬，都是一次人格照镜子。**它不是在教你打牌，而是在教你看清自己。**

### 🚪 酒馆里的房间

| 房间 | 状态 | 一句话 |
|---|---|---|
| ♠️ **Poker Egg 人格牌桌** | ✅ V1 营业中 | 16 型 MBTI 对手的人格博弈训练场 |
| 🍸 **MBTI 调酒吧台** | 🧪 Beta 内测（四型先行版，站内「午夜酒馆」页） | 答题选酒，人格决定你的杯中物 |
| 🎵 **黑胶点唱机** | 📋 规划中 | 人格主题曲，每种人格都有自己的 BGM |

> 三个房间，同一套引擎——**人格建模 + 决策数学**在娱乐场景里的跨域同构。

### 为什么不一样

| 普通扑克 AI | Poker Egg 人格牌桌 |
|---|---|
| 单一难度滑块，调整"聪明度" | **三层 AI 架构**：数学层 + 人格层 + 表演层解耦 |
| 行为随机/规则树，风格可预测 | **8 维人格参数 + 12 维行为向量**驱动 16 型差异化打法，毫秒级配置切换，不依赖 LLM |
| AI 行动没有理由 | **人格化决策理由**：每个 AI 每次行动都给出符合其人格的"内心戏" |
| 盲注/赔率靠玩家心算 | **Kelly Criterion 实时最优投注比例** + 蒙特卡洛真胜率逐街重算 |
| 筹码归零无提醒 | **Game-OS 风控层**实时介入，三基准阈值（0.48 保本 / 0.50 稳态 / 0.68 熔断）|
| 界面千篇一律 | **午夜酒馆沉浸式场景**：贴纸涂鸦美术、人物座位头像、酒馆夜景氛围层 |

### 在 Game-OS 体系中的位置

午夜酒馆是 **Game-OS V2.5 决策AI中台**的场景展示层，「Poker Egg 人格牌桌」是它开放的第一个房间——它验证了中台的核心假设：

> **"人格建模 + 决策数学"可以跨域迁移。**
>
> 金融风控里的 Kelly 投注与噪声抵抗，在扑克桌上是 EV 计算与读牌；
> 商业谈判里的人格画像与情绪管理，在牌桌上是 tilt 控制与 bluff 频率。
>
> 同一套人格内核，下一个战场可以是加密交易、电商定价、电竞 BP，或你定义的任何博弈场景。

---

## ✨ V1 核心特性

<div align="center">

| 🃏 **MBTI 16 型人格对手** | 📊 **Kelly 实时风控面板** | 🔄 **WebSocket 实时对局** |
|---|---|---|
| 8 维人格参数 × 12 维行为向量，毫秒级配置驱动，零 LLM 延迟 | 蒙特卡洛真胜率逐街重算 + 牌型识别 + Kelly 最优比例 + 三基准熔断提示 | 发牌/下注/摊牌全流程 WS 通信，毫秒级牌桌同步 |

| 🎭 **人格化决策理由** | 🍸 **午夜酒馆场景** | 🧠 **三层 AI 架构解耦** |
|---|---|---|
| AI 每次行动附带人格化理由与 tilt 记忆——输给谁，都输得明白 | 酒馆夜景氛围层 + 贴纸涂鸦牌桌 + 人物座位头像 + 试炼总结 | 数学层/人格层/表演层完全解耦，可独立替换升级 |

| 📈 **战绩与人格画像** | 🗂️ **抽屉式数据区** | ⚡ **零成本一键部署** |
|---|---|---|
| 胜率/弃牌率/bluff 捕获率多维统计，牌桌上暴露你的决策人格 | 六维面板/牌局信息收纳进侧边抽屉，主视觉只留牌局本身 | Dockerfile 就绪，GitHub Pages + Railway 零成本运行 |

| 🕶️ **viewer_id 观众遮罩** | 📱 **移动端 768px 适配** | 🌐 **后端云端在线** |
|---|---|---|
| 观众视角按 viewer_id 脱敏对手底牌，摊牌才揭示 | 768px 断点响应式布局 + PWA 全量能力，可安装到主屏 | Railway 生产后端已上线，API 文档 `/docs` 即开即用 |

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
│   PersonaPokerMapper · 8 维人格参数 × 12 维行为模型           │
│   ─ bluffFreq / tiltResist / noiseResist / aggrFactor       │
│   ─ foldFreq / callFreq / raiseFreq / positionBias ...      │
│   ─ 人格化决策理由 + tilt 情绪记忆（连续被诈唬会"上头"）        │
├─────────────────────────────────────────────────────────────┤
│                     📐  数学层 (Mathematics)                  │
│   Kelly Criterion · 蒙特卡洛真胜率 · 手牌强度评估              │
│   ─ 实时最优投注比例 f* = (bp - q) / b                       │
│   ─ 逐街重算胜率（翻牌/转牌/河牌），非静态查表                 │
│   ─ Game-OS 风控三阈值：0.48 保本 / 0.50 稳态 / 0.68 熔断      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    🃏  Poker Game Engine
               (preflop → flop → turn → river → showdown)
```

| 层级 | 职责 | 核心模块 | 延迟 |
|---|---|---|---|
| 📐 数学层 | EV 计算、Kelly 投注、手牌强度 | `ai/ai_engine.py` + NumPy | < 5ms |
| 🎴 人格层 | 人格参数、决策理由、tilt 记忆 | `ai/personality_engine.py` + `ai/personalities.py` | < 1ms（配置查表） |
| 🎭 表演层 | 台词人格、情绪表演、桌面戏剧 | 可选 LLM 接入（规划中） | 200ms~2s（异步） |

---

## 🃏 四大气质组速览

<div align="center">

### 🔮 NF · 紫人组 — 诗意弈者（The Dreamers）

> INFP · INFJ · ENFP · ENFJ

**bluff 62%~66% · tilt 抗性低 · 情绪驱动**

读心者与叙事家。他们把牌局当故事讲，bluff 频率全场最高——不是因为算得准，而是因为**他们真的相信自己能赢**。跟他们打，要警惕那些"故事讲得太圆"的加注；但一旦故事讲崩，他们 tilt 得比谁都快。

---

### 🧪 NT · 黄人组 — 算度大师（The Analysts）

> INTP · INTJ · ENTP · ENTJ

**noiseResist 87%~89% · 决策逻辑优先 · 情绪绝缘**

冷酷的概率机器。87%+ 的抗噪能力意味着你的表情、你的下注节奏、你特意演出来的"破绽"——他们全都过滤掉了，只看牌和赔率。跟他们打，bluff 基本无效；但他们也会因为过度计算而错过"不合理但赢"的机会。

---

### 🛡️ SJ · 蓝人组 — 阵地守将（The Guardians）

> ISTJ · ISFJ · ESTJ · ESFJ

**fold 72%~83% · 极紧 · 风险厌恶**

铜墙铁壁。十把牌里他们能弃七到八把，但一旦他们加注，你最好相信他们真有牌。想从蓝人身上赢筹码，靠 bluff 几乎不可能——你得有耐心，等他们自己犯"按规矩打但规矩错了"的错。

---

### ⚡ SP · 绿人组 — 战术猎手（The Explorers）

> ISTP · ISFP · ESTP · ESFP

**aggr 66%~81% · 松凶 · 即兴进攻**

牌桌上的野兽。高激进度 + 松入池，他们用加注频率压垮你，用不可预测性折磨你。跟他们打最刺激也最危险——他们可能用 7-2 offsuit 把你 all-in，然后真的赢了。Kelly 风控在绿人桌前是你的保命符。

</div>

---

## 🛠️ 技术栈

### 前端
| 技术 | 用途 |
|---|---|
| **React 18 + Vite** | UI 框架与构建（HMR 毫秒级） |
| **Zustand** | 轻量全局状态（牌局数据流实时刷新） |
| **Framer Motion** | 动效引擎（发牌/筹码/翻牌动画） |
| **Ant Design 5** | UI 组件库 |
| **Recharts** | 战绩数据可视化 |
| **原生 WebSocket** | 实时通信 |
| **PWA** | manifest + Service Worker，可安装到主屏 |

### 后端
| 技术 | 用途 |
|---|---|
| **FastAPI + Uvicorn** | 异步 Web 框架（单 worker 保内存状态） |
| **WebSocket** | 实时牌桌通信 |
| **NumPy** | 数学层（EV / 蒙特卡洛胜率） |
| **PyJWT + python-jose** | JWT 认证 |
| **passlib + bcrypt** | 密码哈希 |
| **asyncpg** | PostgreSQL 异步驱动（无 DB 自动降级内存模式） |

### 部署
| 平台 | 用途 | 成本 |
|---|---|---|
| **GitHub Pages + Actions** | 前端托管与 CI（push main 自动构建发布） | 免费 |
| **Railway** | 后端容器 + PostgreSQL | 免费额度 |
| **Docker** | 自建服务器容器化 | — |

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
>
> ⚠️ **单 worker 限制**：游戏状态存于进程内存，生产必须 `--workers 1`，多进程会导致房间状态不一致。多副本部署需引入 Redis（规划中）。

---

## 🌐 部署

### 前端 · GitHub Pages（本仓库现状）

1. 仓库已内置 `.github/workflows/deploy.yml`：**push 到 main 即自动构建并发布**到 GitHub Pages
2. Pages 源选择 **GitHub Actions**，无需手动配置
3. 前端通过 `import.meta.env.BASE_URL` 自动适配子路径 `/poker-egg-fullstack/`
4. 全程约 3~5 分钟，发布后访问 `https://<username>.github.io/poker-egg-fullstack/`

### 后端 · Railway（本仓库现状）

1. Railway **New Project** → **Deploy from GitHub repo** → 选本仓库
2. **Root Directory 留空**（使用根目录 `Dockerfile`）
3. 添加 PostgreSQL 服务：**+ New** → **Database** → **Add PostgreSQL**，`DATABASE_URL` 自动注入
4. 手动设置环境变量：

| 变量 | 值 | 说明 |
|---|---|---|
| `SECRET_KEY` | 随机字符串 | 生产务必修改 |
| `JWT_ALGORITHM` | `HS256` | JWT 算法 |
| `JWT_EXPIRE_MINUTES` | `10080` | Token 有效期（7 天） |
| `ENVIRONMENT` | `production` | 环境标识 |
| `CORS_ORIGINS` | 前端域名 | 逗号分隔的允许源列表 |
| `PORT` | — | Railway 自动注入，无需手动设置 |

5. 部署后在 **Settings → Networking** 生成公共域名，填回前端环境变量
6. 健康检查：`/api/health`（Dockerfile 已配置，超时 10s）

**当前生产实例**：<https://poker-egg-fullstack-production.up.railway.app>（Swagger 文档 `/docs`）

> ⚠️ **踩坑记录**：Railway 服务的 **startCommand 若硬编码 `--port 5000`，会覆盖 Dockerfile CMD**，导致端口与健康检查不匹配、部署反复失败；最终通过将 API 调整至 **8080** 端口解决。自定义 startCommand 时务必与 Railway 注入的 `PORT` 行为对齐。

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
| `POST` | `/api/game/{id}/action` | 玩家行动（fold / call / raise / all-in） |
| `POST` | `/api/game/{id}/ai/add` | 添加 AI 对手 |
| `GET` | `/api/game/{id}` | 获取牌局状态 |
| `GET` | `/api/stats/{playerId}` | 玩家战绩统计 |
| `WS` | `/ws/{game_id}` | WebSocket 实时通信通道 |

---

## 📁 项目结构

```
poker-egg-fullstack/
├── frontend/                        # React 18 + Vite 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── PokerTable/          # 牌桌（座位椭圆布局/贴纸涂鸦/行动按钮）
│   │   │   ├── MidnightTavern/      # 午夜酒馆主页与氛围层
│   │   │   ├── AnalysisPanel/       # Kelly 面板（蒙特卡洛真胜率逐街重算）
│   │   │   ├── SideDrawer/          # 侧边抽屉（六维面板/牌局信息）
│   │   │   ├── ResultModal/         # 试炼总结与结果弹窗
│   │   │   ├── Dashboard/           # 仪表盘（EV/Kelly/风控）
│   │   │   ├── GameLobby/           # 游戏大厅（创建/加入房间）
│   │   │   ├── Profile/             # 个人资料
│   │   │   └── Stats/               # 战绩统计
│   │   ├── store/gameStore.js       # Zustand 全局状态
│   │   ├── App.jsx / main.jsx
│   ├── public/
│   │   ├── characters/              # 人物素材（荷官/座位头像/结果弹窗立绘）
│   │   ├── stickers/                # 贴纸素材（牌背/筹码堆）
│   │   ├── bg/                      # 酒馆夜景背景
│   │   └── manifest.json / sw.js    # PWA
│   ├── package.json / vite.config.js
│
├── backend/                         # FastAPI 后端
│   ├── app.py                       # 入口（路由 + WebSocket）
│   ├── services/game_engine.py      # 扑克引擎（发牌/比牌/回合管理）
│   ├── ai/
│   │   ├── ai_engine.py             # 数学层（EV/Kelly/蒙特卡洛）
│   │   ├── personality_engine.py    # 人格引擎（决策理由 + tilt 记忆）
│   │   ├── personalities.py         # PersonaPokerMapper · 16 型配置
│   │   └── analysis.py              # 行为分析
│   ├── models/                      # 数据库连接（PG/内存降级）+ Pydantic 模型
│   ├── auth/auth.py                 # JWT 认证
│   └── requirements.txt
│
├── .github/workflows/deploy.yml     # GitHub Actions 前端 CI
├── Dockerfile                       # 根 Dockerfile（Railway 部署用）
├── railway.toml / docker-compose.yml / nginx/
├── github-poker-background.jpg      # README 封面 · Midnight Tavern 主视觉
├── LICENSE
└── README.md / README_EN.md
```

---

## 🗺️ 路线图 Roadmap

### ✅ V1.0「Poker Egg 人格牌桌」（2026-08，当前版本）
- [x] 完整德州扑克流程：preflop → flop → turn → river → showdown
- [x] WebSocket 实时牌桌 + 座位椭圆自适应布局
- [x] **16 型人格对手引擎**：8 维人格参数 + 人格化决策理由 + tilt 情绪记忆（NT 算度大师 / NF 诗意弈者 / SJ 阵地守将 / SP 战术猎手 四大气质组全量实装）
- [x] **Kelly 实时风控面板**：蒙特卡洛真胜率逐街重算 + 牌型识别 + AnalysisPanel 前端 + 三基准熔断（0.48 / 0.50 / 0.68）
- [x] **午夜酒馆沉浸式场景**：酒馆夜景氛围层 + 贴纸涂鸦牌桌 + 人物座位头像 + 牌背/筹码贴纸
- [x] 试炼总结（对局复盘弹窗）+ 抽屉式数据区（六维/牌局信息）
- [x] **观众视角脱敏**：viewer_id 遮罩对手底牌（HTTP 轮询脱敏，摊牌揭示，WS 广播不变）
- [x] **移动端适配**：768px 断点响应式布局 + PWA 全量能力
- [x] JWT 用户系统 + 战绩统计 + PWA
- [x] GitHub Pages + Railway 零成本部署链路（生产后端已上线）

### 🎯 V1.1（进行中）
- [ ] 16 型人格调酒卡视觉集（与 Y.Mine 调酒线联动）
- [ ] AI 对手选择界面（点选 MBTI 类型上桌）
- [ ] 对局后决策人格报告（基于你的行动序列生成）
- [ ] 🍸 MBTI 调酒吧台 16 型完整版（现站内 Beta 为四型先行版）
- [ ] 🎵 黑胶点唱机（人格主题曲，联动 Y.Mine 音乐线）

### 🔮 V2（规划中）
- [ ] 🎭 LLM 表演层（人格化台词/嘲讽/情绪反应，异步不阻塞决策）
- [ ] Redis 外置状态存储（多副本水平扩展）
- [ ] 人格对战匹配（基于决策画像匹配"最克制你"的对手）
- [ ] 锦标赛模式（MTT / SNG）
- [ ] Game-OS 中台化：人格内核跨域输出（金融/电商/电竞）
- [ ] 强化学习层（人格 + RL 自适应进化）

---

## 🤝 贡献

欢迎 PR、Issue 与人格配置调优建议。

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: add your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 开启 Pull Request

如果你对人格配置参数（bluffFreq / aggrFactor 等）有基于实战的调优建议，尤其欢迎——**16 型人格的行为向量需要大量对局数据校准**。

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
