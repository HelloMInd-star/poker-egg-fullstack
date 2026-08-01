# ♠️ Poker Egg Fullstack

> 德州扑克AI陪练平台 · React + Python 全栈应用

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/Railway-Deployed-0B0D0E?logo=railway)](https://railway.app/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployed-brightgreen?logo=github)](https://hellomind-star.github.io/poker-egg-fullstack/)

---

## 🎯 在线体验

- 🎮 **前端地址**：[https://hellomind-star.github.io/poker-egg-fullstack/](https://hellomind-star.github.io/poker-egg-fullstack/)
- 🚀 **后端 API**：[https://poker-egg-fullstack.up.railway.app](https://poker-egg-fullstack.up.railway.app)
- 📖 **API 文档**：[https://poker-egg-fullstack.up.railway.app/docs](https://poker-egg-fullstack.up.railway.app/docs)

---

## ✨ 功能特性

- 🃏 **完整德州扑克对局** - 发牌、翻牌、转牌、河牌、摊牌全流程
- 🤖 **AI智能陪练** - 3个难度级别（简单/中等/困难）
- 📊 **凯利公式实时计算** - 动态计算最优投注比例
- 🎯 **表理映射面板** - 博弈状态可视化分析
- 👤 **用户系统** - JWT 认证，个人资料管理
- 📈 **战绩统计分析** - 胜率、趋势、历史记录
- 🔄 **WebSocket实时通信** - 流畅的多人对战体验
- 🐳 **Docker一键部署** - 开箱即用

---

## 🎮 游戏机制

### 核心玩法
1. 注册/登录账号
2. 创建游戏房间或加入现有房间
3. AI自动加入（可选择难度）
4. 进行德州扑克对局
5. 实时查看凯利指数和牌桌数据

### 游戏操作
| 操作 | 说明 |
|------|------|
| 弃牌 | 放弃本局，损失已下注筹码 |
| 跟注 | 跟随当前最高下注 |
| 加注 | 提高下注额 |
| All-in | 押上所有筹码 |

### AI难度说明
| 难度 | 说明 | 适合人群 |
|------|------|----------|
| 😊 简单 | 随机决策，主要看手牌 | 新手入门 |
| 🤔 中等 | 考虑赔率和期望值 | 有一定基础 |
| 😈 困难 | 使用凯利公式+策略混合 | 进阶玩家 |

---

## 🛠️ 技术栈

### 前端
| 技术 | 说明 |
|------|------|
| **React 18** | UI 框架 |
| **Vite** | 构建工具 |
| **Ant Design** | UI 组件库 |
| **Zustand** | 状态管理 |
| **Socket.io-client** | 实时通信 |
| **Framer Motion** | 动画效果 |
| **Recharts** | 数据图表 |

### 后端
| 技术 | 说明 |
|------|------|
| **FastAPI** | Web 框架 |
| **WebSocket** | 实时通信 |
| **SQLAlchemy** | ORM |
| **PostgreSQL** | 数据库 |
| **Redis** | 缓存 |
| **scikit-learn** | AI/ML 引擎 |
| **JWT** | 用户认证 |

---

## 📁 项目结构

poker\-egg\-fullstack/

├── frontend/                 \# React 前端

│   ├── src/

│   │   ├── components/      \# UI 组件

│   │   ├── store/           \# 状态管理

│   │   ├── services/        \# API 服务

│   │   ├── App\.jsx

│   │   └── main\.jsx

│   ├── public/

│   │   └── easter\-egg\.html  \# 经典彩蛋

│   ├── package\.json

│   └── vite\.config\.js

│

├── backend/                  \# Python 后端

│   ├── services/

│   │   └── game\_engine\.py   \# 游戏引擎

│   ├── ai/

│   │   └── ai\_engine\.py     \# AI 引擎

│   ├── models/              \# 数据模型

│   ├── auth/                \# 用户认证

│   ├── app\.py               \# 主程序

│   └── requirements\.txt

│

├── docker\-compose\.yml       \# Docker 部署

├── railway\.json             \# Railway 配置

└── README\.md

```Plain

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 克隆项目
git clone https://github.com/HelloMind-star/poker-egg-fullstack.git
cd poker-egg-fullstack

# 一键启动
docker-compose up -d

# 访问
# 前端: http://localhost:3000
# 后端: http://localhost:5000
# API 文档: http://localhost:5000/docs
```
### 方式二：本地开发

```Bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 5000

# 前端（新终端）
cd frontend
npm install
npm run dev

# 访问 http://localhost:5173
```
---

## 🌐 部署指南

### 前端部署到 GitHub Pages

1. 构建前端：

   ```Bash
   cd frontend
   npm run build
   ```
2. 将 `dist/` 目录部署到 GitHub Pages
3. 访问 `https://hellomind-star.github.io/poker-egg-fullstack/`

### 后端部署到 Railway

1. 在 Railway 创建新项目
2. 连接 GitHub 仓库
3. 设置 Root Directory 为 `backend`
4. 添加环境变量
5. 自动部署完成

---

## 📊 API 文档

启动后端后访问：

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

### 主要 API


| 方法 | 路径                  | 说明           |
| ---- | --------------------- | -------------- |
| GET  | `/api/health`         | 健康检查       |
| POST | `/api/game/create`    | 创建游戏       |
| POST | `/api/game/{id}/join` | 加入游戏       |
| GET  | `/api/game/{id}`      | 获取游戏状态   |
| POST | `/api/auth/register`  | 用户注册       |
| POST | `/api/auth/login`     | 用户登录       |
| WS   | `/ws/{game_id}`       | WebSocket 连接 |

---

## 📝 环境变量

### 后端环境变量

```Plain
# 数据库
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://redis:6379

# JWT
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```
### 前端环境变量

```Plain
VITE_API_URL=https://your-backend-domain.com
VITE_WS_URL=wss://your-backend-domain.com
```
---

## 🎯 路线图

* [ ]  基础牌桌交互
* [ ]  AI 陪练（3个难度）
* [ ]  凯利公式集成
* [ ]  用户认证
* [ ]  战绩统计
* [ ]  多人对战模式
* [ ]  强化学习 AI
* [ ]  锦标赛模式
* [ ]  移动端 APP

---

## 🤝 贡献指南

欢迎贡献代码！

1. Fork 本仓库
2. 创建特性分支 \(`git checkout -b feature/AmazingFeature`\)
3. 提交更改 \(`git commit -m 'Add some AmazingFeature'`\)
4. 推送到分支 \(`git push origin feature/AmazingFeature`\)
5. 开启 Pull Request

---

## 📄 开源协议

本项目采用 MIT 协议 \- 详见 \[LICENSE\]\(LICENSE\) 文件

---

## 👨‍💻 作者

**HelloMind\-star** \(Mine\)

- GitHub: [@HelloMind\-star](https://github.com/HelloMind-star)

---

## ⭐ 支持项目

如果这个项目对你有帮助，请给个 Star ⭐ 支持一下！
