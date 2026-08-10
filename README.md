# ♠️ Poker Egg Fullstack

> 德州扑克AI陪练平台 · React + Python 全栈应用

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?logo=vercel)](https://vercel.com/)
[![Railway](https://img.shields.io/badge/Railway-Backend-0B0D0E?logo=railway)](https://railway.app/)

---

## 🚧 当前状态：MVP v1.0

项目已完成核心 MVP，可进行完整德州扑克对局（发牌/翻牌/转牌/河牌/摊牌）、AI 陪练（3 档难度）、WebSocket 实时对战、JWT 用户系统与战绩统计。
部分能力尚未接入：MBTI 人格化 AI（`backend/ai/personalities.py` 数据已准备，待引擎接入）、Redis 缓存、强化学习 AI。

---

## 🎯 在线体验

- 🎮 **前端地址**：Vercel 部署（或 GitHub Pages: https://hellomind-star.github.io/poker-egg-fullstack/）
- 🚀 **后端 API**：Railway 部署
- 📖 **API 文档**：后端部署地址 `/docs`

---

## ✨ 功能特性

- 🃏 **完整德州扑克对局** - 发牌、翻牌、转牌、河牌、摊牌全流程
- 🤖 **AI 智能陪练** - 3 个难度级别（简单/中等/困难），未来接入 16 型 MBTI 人格
- 📊 **凯利公式实时计算** - 动态计算最优投注比例
- 🎯 **博弈状态可视化** - 表理映射面板分析
- 👤 **用户系统** - JWT 认证，个人资料管理
- 📈 **战绩统计分析** - 胜率、趋势、历史记录
- 🔄 **WebSocket 实时通信** - 流畅的多人对战体验
- 🐳 **Docker 一键部署** - 开箱即用

---

## 🛠️ 技术栈

### 前端
| 技术 | 说明 |
|------|------|
| **React 18** | UI 框架 |
| **Vite** | 构建工具 |
| **Ant Design 5** | UI 组件库（全局消息提示） |
| **Zustand** | 状态管理 |
| **WebSocket（原生）** | 实时通信 |
| **Framer Motion** | 动画效果 |
| **Recharts** | 数据图表 |
| **Day.js** | 日期处理 |

### 后端
| 技术 | 说明 |
|------|------|
| **FastAPI** | Web 框架 |
| **Uvicorn** | ASGI 服务器 |
| **asyncpg** | PostgreSQL 异步驱动 |
| **SQLAlchemy** | ORM（预留，当前手写 SQL） |
| **PostgreSQL** | 数据库（未配置时降级为内存模式） |
| **PyJWT + python-jose** | JWT 用户认证 |
| **passlib + bcrypt** | 密码哈希 |
| **NumPy** | AI 计算基础 |
| **WebSockets** | 实时通信 |

---

## 项目结构

```
poker-egg-fullstack/
├── frontend/                 # React 前端（Vite）
│   ├── public/
│   │   └── easter-egg.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── PokerTable/   # 牌桌组件
│   │   │   │   ├── PokerTable.jsx
│   │   │   │   └── PokerTable.css
│   │   │   ├── Dashboard/    # 仪表盘
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   └── Dashboard.css
│   │   │   ├── GameLobby/    # 游戏大厅
│   │   │   │   ├── GameLobby.jsx
│   │   │   │   └── GameLobby.css
│   │   │   ├── Profile/      # 个人资料
│   │   │   │   ├── Profile.jsx
│   │   │   │   └── Profile.css
│   │   │   └── Stats/        # 战绩统计
│   │   │       ├── Stats.jsx
│   │   │       └── Stats.css
│   │   ├── store/
│   │   │   └── gameStore.js  # Zustand 全局状态（含 fetch/ws 调用）
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json           # Vercel 部署配置
│   ├── nginx.conf
│   ├── Dockerfile
│   ├── .env.example
│   ├── .env
│   ├── .env.production
│   └── index.html
│
├── backend/                  # FastAPI 后端
│   ├── services/
│   │   └── game_engine.py    # 游戏引擎（含发牌/比牌/AI 决策）
│   ├── ai/
│   │   ├── ai_engine.py      # AI 决策引擎（规则+随机）
│   │   └── personalities.py  # 16 型 MBTI 人格配置数据（待接入）
│   ├── models/
│   │   ├── database.py       # 数据库连接与 SQL
│   │   └── schemas.py        # Pydantic 数据模型
│   ├── auth/
│   │   └── auth.py           # JWT 认证
│   ├── app.py                # FastAPI 入口
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── .dockerignore
│
├── nginx/
│   └── nginx.conf
│
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions CI
│
├── docker-compose.yml
├── railway.json              # Railway 后端部署配置
├── Procfile
├── .gitignore
├── .env.example
├── LICENSE
└── README.md
```

---

## 🚀 快速开始

### 方式一：本地开发

```bash
# 1. 后端
cd backend
cp .env.example .env          # 修改 DATABASE_URL / SECRET_KEY
pip install -r requirements.txt
uvicorn app:app --reload --port 5000

# 2. 前端（新终端）
cd frontend
cp .env.example .env          # 修改 VITE_API_URL / VITE_WS_URL
npm install
npm run dev

# 前端访问 http://localhost:5173
# 后端 API  http://localhost:5000
# API 文档  http://localhost:5000/docs
```

> 💡 **提示**：如果没有配置 PostgreSQL（未设置 `DATABASE_URL`），后端会自动降级为**内存模式**。
> 内存模式下任意用户名和密码均可登录（例如 `testuser` / `123456`），但重启后数据会丢失。
> **生产环境必须配置 PostgreSQL**，且必须使用单 worker 启动（游戏状态存内存，不能多进程）。

### 方式二：Docker Compose

```bash
git clone https://github.com/HelloMind-star/poker-egg-fullstack.git
cd poker-egg-fullstack
docker-compose up -d

# 前端: http://localhost:3000
# 后端: http://localhost:5000
```

---

## 🌐 部署指南

### 前端：Vercel（推荐）

1. 将仓库推送到 GitHub。
2. 在 Vercel 点击 **New Project** → Import 仓库。
3. **Framework Preset** 选 `Vite`；**Root Directory** 设为 `frontend`。
4. 环境变量：
   - `VITE_API_URL` = 后端 Railway 地址（如 `https://your-app.up.railway.app`）
   - `VITE_WS_URL`  = 后端 WebSocket 地址（如 `wss://your-app.up.railway.app`）
5. 仓库内已包含 `frontend/vercel.json`，SPA rewrites 自动生效（所有路由回退到 `index.html`）。
6. 点击 Deploy，完成后 Vercel 会自动分配 `*.vercel.app` 域名。

> GitHub Pages 也支持，但需要在 `vite.config.js` 设置正确的 `base` 路径，且不支持 SPA 路由 rewrites（需 404.html 兜底）。

### 后端：Railway（推荐）

1. 在 Railway 创建 **New Project** → **Deploy from GitHub repo**。
2. 选择本仓库，**Root Directory 留空**（仓库根目录，使用 `railway.json`）。
3. 仓库根目录已包含 `railway.json`，会自动使用 `backend/Dockerfile` 构建。
4. 添加 PostgreSQL 服务：在项目内 **+ New** → **Database** → **Add PostgreSQL**，Railway 会自动注入 `DATABASE_URL` / `PGHOST` / `PGPORT` 等环境变量。
5. 其余环境变量手动设置：
   - `SECRET_KEY` = 随机字符串（生产务必修改）
   - `JWT_ALGORITHM` = `HS256`
   - `JWT_EXPIRE_MINUTES` = `10080`
   - `ENVIRONMENT` = `production`
   - `PORT` = Railway 自动注入，无需手动设置
6. 部署完成后在 **Settings → Networking** 生成公共域名，填入前端 `VITE_API_URL` / `VITE_WS_URL`。
7. 健康检查路径：`/api/health`（已在 `railway.json` 中配置，超时 10s）。

> ⚠️ **注意**：游戏状态保存在进程内存中，**必须以单 worker 模式运行**（`--workers 1`），Dockerfile 与 railway.json 已固定此配置，请勿修改为多 worker，否则多进程会导致房间状态不一致。持久化多副本部署需引入 Redis / 外部状态存储（规划中）。

---

## 📊 API 文档

启动后端后访问：

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

### 主要 API

| 方法 | 路径                        | 说明                         |
| ---- | --------------------------- | ---------------------------- |
| GET  | `/api/health`               | 健康检查                     |
| POST | `/api/game/create`          | 创建游戏                     |
| POST | `/api/game/{id}/join`       | 加入游戏                     |
| POST | `/api/game/{id}/start`      | 开始游戏（发牌）             |
| POST | `/api/game/{id}/action`     | 玩家行动（弃牌/跟注/加注）   |
| POST | `/api/game/{id}/ai/add`     | 添加 AI 玩家                 |
| GET  | `/api/game/{id}`            | 获取游戏状态                 |
| GET  | `/api/auth/me`              | 获取当前用户信息             |
| POST | `/api/auth/register`        | 用户注册                     |
| POST | `/api/auth/login`           | 用户登录                     |
| GET  | `/api/stats/{playerId}`     | 获取玩家统计                 |
| WS   | `/ws/{game_id}`             | WebSocket 实时通信           |

> 💡 `/api/auth/login` 同时支持 `application/x-www-form-urlencoded` 和 `application/json` 两种请求格式。

---

## 📝 环境变量

### 后端 (`backend/.env`)

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/poker_egg
SECRET_KEY=change-me-to-random-hex-string
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
ENVIRONMENT=development
PORT=5000
```

### 前端 (`frontend/.env`)

```env
VITE_API_URL=http://localhost:5000
VITE_WS_URL=ws://localhost:5000
```

生产环境请把 URL 改为部署后的 https/wss 域名。

---

## 🎯 路线图

- [x] 基础牌桌交互（发牌/下注/比牌全流程）
- [x] AI 陪练（3 个难度：简单/中等/困难）
- [x] 凯利公式集成
- [x] 用户认证（JWT）
- [x] 战绩统计
- [x] WebSocket 多人房间
- [x] Vercel + Railway 部署配置
- [ ] 16 型 MBTI 人格化 AI（数据已就绪，待接入 `ai_engine.py`）
- [ ] Redis 外置状态存储（支撑多 worker/多副本）
- [ ] 强化学习 AI
- [ ] 锦标赛模式
- [ ] 移动端适配

---

## 🤝 贡献指南

欢迎贡献代码！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源协议

本项目采用 MIT 协议 - 详见 [LICENSE](LICENSE) 文件。

---

## 👨‍💻 作者

**HelloMind-star** (Mine)

- GitHub: [@HelloMind-star](https://github.com/HelloMind-star)

---

## ⭐ 支持项目

如果这个项目对你有帮助，请给个 Star ⭐ 支持一下！
