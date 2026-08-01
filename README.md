# ♠️ Poker Egg Fullstack

德州扑克AI陪练平台 · React + Python 全栈应用

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/Railway-Deployed-0B0D0E?logo=railway)](https://railway.app/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployed-brightgreen?logo=github)](https://hellomind-star.github.io/poker-egg-fullstack/)


## 在线体验

- 前端地址: https://hellomind-star.github.io/poker-egg-fullstack/
- 后端 API: https://poker-egg-fullstack.up.railway.app
- API 文档: https://poker-egg-fullstack.up.railway.app/docs


## 功能特性

- 完整德州扑克对局 - 发牌、翻牌、转牌、河牌、摊牌全流程
- AI智能陪练 - 3个难度级别（简单/中等/困难）
- 凯利公式实时计算 - 动态计算最优投注比例
- 表理映射面板 - 博弈状态可视化分析
- 用户系统 - JWT 认证，个人资料管理
- 战绩统计分析 - 胜率、趋势、历史记录
- WebSocket实时通信 - 流畅的多人对战体验
- Docker一键部署 - 开箱即用


## 游戏机制

### 核心玩法
1. 注册/登录账号
2. 创建游戏房间或加入现有房间
3. AI自动加入（可选择难度）
4. 进行德州扑克对局
5. 实时查看凯利指数和牌桌数据

### 游戏操作
- 弃牌: 放弃本局，损失已下注筹码
- 跟注: 跟随当前最高下注
- 加注: 提高下注额
- All-in: 押上所有筹码

### AI难度说明
- 简单: 随机决策，主要看手牌，适合新手入门
- 中等: 考虑赔率和期望值，适合有一定基础
- 困难: 使用凯利公式+策略混合，适合进阶玩家


## 技术栈

### 前端
- React 18 - UI 框架
- Vite - 构建工具
- Ant Design - UI 组件库
- Zustand - 状态管理
- Socket.io-client - 实时通信
- Framer Motion - 动画效果
- Recharts - 数据图表

### 后端
- FastAPI - Web 框架
- WebSocket - 实时通信
- SQLAlchemy - ORM
- PostgreSQL - 数据库
- Redis - 缓存
- scikit-learn - AI/ML 引擎
- JWT - 用户认证


## 项目结构
poker-egg-fullstack/
├── frontend/ # React 前端
│ ├── src/
│ │ ├── components/ # UI 组件
│ │ ├── store/ # 状态管理
│ │ ├── services/ # API 服务
│ │ ├── App.jsx
│ │ └── main.jsx
│ ├── public/
│ │ └── easter-egg.html # 经典彩蛋
│ ├── package.json
│ └── vite.config.js
│
├── backend/ # Python 后端
│ ├── services/
│ │ └── game_engine.py # 游戏引擎
│ ├── ai/
│ │ └── ai_engine.py # AI 引擎
│ ├── models/ # 数据模型
│ ├── auth/ # 用户认证
│ ├── app.py # 主程序
│ └── requirements.txt
│
├── docker-compose.yml # Docker 部署
├── railway.json # Railway 配置
└── README.md

---

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

### 方式二：本地开发
```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 5000

# 前端（新终端）
cd frontend
npm install
npm run dev

# 访问 http://localhost:5173

