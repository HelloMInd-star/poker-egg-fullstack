"""
Poker Egg 后端主程序
FastAPI + WebSocket 实时通信
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any
import json
import asyncio
import uuid
from datetime import datetime, timedelta
import logging

# 导入自定义模块
from services.game_engine import GameEngine, Player, Card
from ai.ai_engine import PokerAI, AIDecisionMaker
from models.database import Database
from models.schemas import (
    UserCreate, UserLogin, Token, GameCreate, GameJoin,
    PlayerAction, GameState, PlayerStats
)
from auth.auth import AuthHandler

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# FastAPI 应用初始化
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("🚀 Poker Egg 服务器启动中...")
    await Database.connect()
    logger.info("✅ 数据库连接成功")
    yield
    # 关闭时
    await Database.disconnect()
    logger.info("🛑 Poker Egg 服务器已关闭")

app = FastAPI(
    title="Poker Egg API",
    description="德州扑克AI陪练平台 - 全栈应用",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================
# CORS 配置
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://hellomind-star.github.io",
        "*"  # 生产环境请限制具体域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 依赖注入
# ============================================

auth_handler = AuthHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# ============================================
# 全局状态管理
# ============================================

class GameManager:
    """游戏管理器 - 管理所有游戏会话"""
    
    def __init__(self):
        self.games: Dict[str, GameEngine] = {}
        self.connections: Dict[str, WebSocket] = {}
        self.players: Dict[str, Dict] = {}  # player_id -> {game_id, name}
        self.ai_decision_maker = AIDecisionMaker()
    
    def create_game(self, player_name: str, ai_difficulty: str = "medium") -> Dict:
        """创建新游戏"""
        game = GameEngine()
        
        # 添加玩家
        player = game.add_player(player_name, is_ai=False)
        
        # 添加AI玩家
        ai_player = game.add_player("AI Bot", is_ai=True, ai_difficulty=ai_difficulty)
        
        self.games[game.id] = game
        
        return {
            "game_id": game.id,
            "player_id": player.id,
            "ai_player_id": ai_player.id,
            "game_state": game.get_state()
        }
    
    def join_game(self, game_id: str, player_name: str) -> Optional[Dict]:
        """加入游戏"""
        game = self.games.get(game_id)
        if not game:
            return None
        
        # 检查是否已满（最多6人）
        if len([p for p in game.players if not p.is_ai]) >= 5:
            return {"error": "游戏已满"}
        
        player = game.add_player(player_name, is_ai=False)
        
        return {
            "game_id": game.id,
            "player_id": player.id,
            "game_state": game.get_state()
        }
    
    def add_ai_player(self, game_id: str, difficulty: str = "medium") -> Optional[Dict]:
        """添加AI玩家"""
        game = self.games.get(game_id)
        if not game:
            return None
        
        ai_player = game.add_player(f"AI Bot {len([p for p in game.players if p.is_ai]) + 1}", 
                                   is_ai=True, ai_difficulty=difficulty)
        
        return {
            "player_id": ai_player.id,
            "game_state": game.get_state()
        }
    
    def get_game(self, game_id: str) -> Optional[GameEngine]:
        """获取游戏"""
        return self.games.get(game_id)
    
    def remove_game(self, game_id: str):
        """移除游戏"""
        if game_id in self.games:
            del self.games[game_id]
        if game_id in self.connections:
            del self.connections[game_id]
    
    def register_connection(self, game_id: str, websocket: WebSocket):
        """注册WebSocket连接"""
        self.connections[game_id] = websocket
    
    def unregister_connection(self, game_id: str):
        """注销WebSocket连接"""
        if game_id in self.connections:
            del self.connections[game_id]
    
    async def broadcast(self, game_id: str, message: Dict):
        """广播消息给游戏中的所有玩家"""
        websocket = self.connections.get(game_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"广播失败: {e}")
    
    async def process_ai_turn(self, game_id: str):
        """处理AI回合"""
        game = self.games.get(game_id)
        if not game:
            return
        
        ai_player = game.get_ai_player()
        if not ai_player:
            return
        
        # 等待一下模拟思考
        await asyncio.sleep(ai_player.ai_difficulty == "hard" and 1.5 or 1.0)
        
        # 获取AI决策
        ai = self.ai_decision_maker.get_ai(ai_player.ai_difficulty)
        
        # 构建游戏状态
        game_state = game.get_state()
        ai_state = {
            "hole_cards": [c.to_dict() for c in ai_player.hole_cards],
            "board_cards": [c.to_dict() for c in game.board],
            "pot": game.pot,
            "my_chips": ai_player.chips,
            "current_bet": max([p.bet for p in game.players if not p.folded] or [0]),
            "position": "late",
            "stage": game.stage.value
        }
        
        # AI决策
        decision = ai.decide_action(ai_state)
        
        # 执行AI行动
        result = game.process_action(ai_player.id, decision["action"], decision.get("amount", 0))
        
        if result["success"]:
            # 广播更新
            await self.broadcast(game_id, {
                "type": "ai_action",
                "data": {
                    "player": ai_player.name,
                    "action": decision["action"],
                    "amount": decision.get("amount", 0),
                    "message": result["message"]
                }
            })
            
            # 广播游戏状态
            await self.broadcast(game_id, {
                "type": "game_state",
                "data": game.get_state()
            })
            
            # 检查游戏是否结束
            if game.hand_over:
                await self.broadcast(game_id, {
                    "type": "hand_over",
                    "data": {
                        "winner": game.winner.to_dict() if game.winner else None,
                        "pot": game.pot
                    }
                })
                
                # 自动开始下一局（延迟2秒）
                await asyncio.sleep(2)
                game.start_new_hand()
                await self.broadcast(game_id, {
                    "type": "game_state",
                    "data": game.get_state()
                })
                await self.broadcast(game_id, {
                    "type": "system_message",
                    "data": {"message": "🔄 新的一局开始"}
                })

game_manager = GameManager()

# ============================================
# API 路由
# ============================================

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "Poker Egg API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
        "websocket": "ws://localhost:5000/ws/{game_id}"
    }

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "games": len(game_manager.games),
        "connections": len(game_manager.connections)
    }

# ============================================
# 游戏 API
# ============================================

@app.post("/api/game/create")
async def create_game(request: GameCreate):
    """创建新游戏"""
    try:
        result = game_manager.create_game(
            player_name=request.player_name or "Player",
            ai_difficulty=request.ai_difficulty or "medium"
        )
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"创建游戏失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game/{game_id}/join")
async def join_game(game_id: str, request: GameJoin):
    """加入游戏"""
    result = game_manager.join_game(game_id, request.player_name or "Player")
    if not result:
        raise HTTPException(status_code=404, detail="游戏不存在")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "success": True,
        "data": result
    }

@app.get("/api/game/{game_id}")
async def get_game_state(game_id: str):
    """获取游戏状态"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    return {
        "success": True,
        "data": game.get_state()
    }

@app.post("/api/game/{game_id}/ai/add")
async def add_ai_player(game_id: str, difficulty: str = "medium"):
    """添加AI玩家"""
    result = game_manager.add_ai_player(game_id, difficulty)
    if not result:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    # 广播更新
    await game_manager.broadcast(game_id, {
        "type": "player_joined",
        "data": {"message": "AI玩家加入了游戏"}
    })
    
    return {
        "success": True,
        "data": result
    }

@app.post("/api/game/{game_id}/action")
async def player_action(game_id: str, action: PlayerAction):
    """玩家行动"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    # 检查是否轮到该玩家
    current_player = game.players[game.current_player_index]
    if current_player.id != action.player_id:
        raise HTTPException(status_code=400, detail="不是你的回合")
    
    # 处理行动
    result = game.process_action(
        action.player_id,
        action.action_type,
        action.amount or 0
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    # 广播更新
    await game_manager.broadcast(game_id, {
        "type": "action_result",
        "data": result
    })
    
    await game_manager.broadcast(game_id, {
        "type": "game_state",
        "data": game.get_state()
    })
    
    # 检查是否需要AI行动
    if not game.hand_over and game.is_ai_turn():
        asyncio.create_task(game_manager.process_ai_turn(game_id))
    
    return {
        "success": True,
        "data": result
    }

@app.post("/api/game/{game_id}/start")
async def start_game(game_id: str):
    """开始游戏"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    game.start_new_hand()
    
    await game_manager.broadcast(game_id, {
        "type": "game_state",
        "data": game.get_state()
    })
    
    await game_manager.broadcast(game_id, {
        "type": "system_message",
        "data": {"message": "🃏 游戏开始！"}
    })
    
    # 检查是否轮到AI
    if not game.hand_over and game.is_ai_turn():
        asyncio.create_task(game_manager.process_ai_turn(game_id))
    
    return {
        "success": True,
        "data": game.get_state()
    }

# ============================================
# WebSocket 连接
# ============================================

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """
    WebSocket 连接端点
    用于实时游戏通信
    """
    await websocket.accept()
    logger.info(f"WebSocket 连接建立: {game_id}")
    
    game_manager.register_connection(game_id, websocket)
    
    # 发送当前游戏状态
    game = game_manager.get_game(game_id)
    if game:
        await websocket.send_json({
            "type": "game_state",
            "data": game.get_state()
        })
        await websocket.send_json({
            "type": "system_message",
            "data": {"message": "👋 欢迎来到 Poker Egg!"}
        })
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "ping":
                await websocket.send_json({"type": "pong"})
            
            elif message_type == "action":
                # 玩家行动
                action_data = message.get("data", {})
                player_id = action_data.get("player_id")
                action_type = action_data.get("action")
                amount = action_data.get("amount", 0)
                
                if not game:
                    await websocket.send_json({
                        "type": "error",
                        "data": {"message": "游戏不存在"}
                    })
                    continue
                
                # 检查是否轮到该玩家
                if game.players[game.current_player_index].id != player_id:
                    await websocket.send_json({
                        "type": "error",
                        "data": {"message": "不是你的回合"}
                    })
                    continue
                
                # 执行行动
                result = game.process_action(player_id, action_type, amount)
                
                if result["success"]:
                    # 广播更新
                    await game_manager.broadcast(game_id, {
                        "type": "action_result",
                        "data": result
                    })
                    
                    await game_manager.broadcast(game_id, {
                        "type": "game_state",
                        "data": game.get_state()
                    })
                    
                    # 检查是否需要AI行动
                    if not game.hand_over and game.is_ai_turn():
                        asyncio.create_task(game_manager.process_ai_turn(game_id))
                else:
                    await websocket.send_json({
                        "type": "error",
                        "data": {"message": result["message"]}
                    })
            
            elif message_type == "chat":
                # 聊天消息
                chat_data = message.get("data", {})
                await game_manager.broadcast(game_id, {
                    "type": "chat",
                    "data": {
                        "player": chat_data.get("player_name", "Unknown"),
                        "message": chat_data.get("message", ""),
                        "timestamp": datetime.now().isoformat()
                    }
                })
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket 断开: {game_id}")
        game_manager.unregister_connection(game_id)
    
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
        game_manager.unregister_connection(game_id)

# ============================================
# 用户认证 API（后续扩展）
# ============================================

@app.post("/api/auth/register")
async def register(user_data: UserCreate):
    """用户注册"""
    # 检查用户是否存在
    existing_user = await Database.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 创建用户
    user = await Database.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    
    # 生成token
    token = auth_handler.create_access_token(user["id"])
    
    return {
        "success": True,
        "data": {
            "user": user,
            "token": token
        }
    }

@app.post("/api/auth/login")
async def login(request: Request):
    """用户登录（同时支持表单和 JSON 格式）"""
    # 尝试从表单读取
    username = None
    password = None
    
    try:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
    except Exception:
        pass
    
    # 如果表单没有，尝试从 JSON 读取
    if not username or not password:
        try:
            body = await request.json()
            username = body.get("username") or username
            password = body.get("password") or password
        except Exception:
            pass
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名和密码不能为空",
        )
    
    user = await Database.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_handler.create_access_token(user["id"])
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/api/auth/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户信息"""
    payload = auth_handler.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的token")
    
    user = await Database.get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return user

# ============================================
# 统计数据 API
# ============================================

@app.get("/api/stats/{player_id}")
async def get_player_stats(player_id: str):
    """获取玩家统计数据"""
    stats = await Database.get_player_stats(player_id)
    if not stats:
        return {
            "success": True,
            "data": {
                "total_hands": 0,
                "hands_won": 0,
                "win_rate": 0,
                "total_chips_won": 0,
                "best_hand": "High Card",
                "aggression": 0.0,
                "vpip": 0.0,
                "pfr": 0.0
            }
        }
    return {
        "success": True,
        "data": stats
    }

@app.get("/api/stats/{player_id}/history")
async def get_player_history(player_id: str, limit: int = 50):
    """获取玩家历史记录"""
    history = await Database.get_player_history(player_id, limit)
    return {
        "success": True,
        "data": history
    }

# ============================================
# 错误处理
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "服务器内部错误"
        }
    )

# ============================================
# 启动入口
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )
