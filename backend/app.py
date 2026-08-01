from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, List, Optional
import json
import asyncio
from datetime import datetime
import uuid

app = FastAPI(
    title="Poker Egg API",
    description="德州扑克AI陪练平台",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 游戏管理
games = {}
connections = {}

@app.get("/")
async def root():
    return {
        "message": "♠️ Poker Egg API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/game/create")
async def create_game(player_name: str = "Player"):
    """创建游戏"""
    game_id = str(uuid.uuid4())[:8]
    games[game_id] = {
        "id": game_id,
        "players": [],
        "board": [],
        "pot": 0,
        "stage": "preflop",
        "created_at": datetime.now().isoformat()
    }
    return {"game_id": game_id, "message": "游戏创建成功"}

@app.get("/api/game/{game_id}")
async def get_game(game_id: str):
    """获取游戏状态"""
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    return game

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket连接"""
    await websocket.accept()
    connections[game_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 处理消息
            if message["type"] == "action":
                # 处理游戏动作
                await websocket.send_json({
                    "type": "game_update",
                    "data": {"status": "action_processed"}
                })
            elif message["type"] == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        del connections[game_id]
    except Exception as e:
        print(f"WebSocket错误: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
