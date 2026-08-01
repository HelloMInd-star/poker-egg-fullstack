# ♠️ Poker Egg Fullstack

> 德州扑克AI陪练平台 · React + Python 全栈应用

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://python.org/)

## ✨ 功能特性

- 🃏 完整德州扑克对局
- 🤖 AI智能陪练（3个难度级别）
- 📊 凯利公式实时计算
- 🎯 表理映射面板
- 👤 用户系统（JWT认证）
- 📈 战绩统计分析
- 🔄 WebSocket实时通信
- 🎨 暗紫极简风格

## 🛠️ 技术栈

### 前端
- **React 18** + **Vite**
- **Ant Design** UI组件
- **Zustand** 状态管理
- **Socket.io-client** 实时通信
- **Framer Motion** 动画

### 后端
- **FastAPI** (Python)
- **WebSocket** 实时通信
- **SQLAlchemy** ORM
- **PostgreSQL** 数据库
- **Redis** 缓存

### AI引擎
- **scikit-learn** 机器学习
- **NumPy** 数值计算
- **Pandas** 数据分析

## 🚀 快速开始

### 方式一：Docker（推荐）

```bash
# 克隆项目
git clone https://github.com/HelloMind-star/poker-egg-fullstack.git
cd poker-egg-fullstack

# 一键启动
docker-compose up -d

# 访问
# 前端: http://localhost:3000
# 后端: http://localhost:5000
