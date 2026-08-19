"""
Poker Face Arena 后端主程序 · 扑克人格竞技场
Game-OS V2.5 决策AI中台 · 首个公开可玩 Demo
FastAPI + WebSocket 实时通信 + MBTI人格AI + Kelly风控
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any
import json
import asyncio
import os
from datetime import datetime
import logging

from services.game_engine import GameEngine, Player, Card
from ai.ai_engine import PokerAI, AIDecisionMaker
from ai.personalities import MBTI_PERSONALITIES
from ai.personality_engine import personality_ai_manager
from ai.analysis import kelly_analysis
import random
from models.database import Database
from models.schemas import (
    UserCreate, GameCreate, GameJoin,
    PlayerAction
)
from auth.auth import AuthHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("♠️ Poker Face Arena 服务器启动中...")
    await Database.connect()
    # MVP fix: 真正通过 _pool 是否为 None 判断数据库连接状态，区分成功/降级
    if Database._pool is not None:
        logger.info("✅ 数据库连接成功 (PostgreSQL)")
    else:
        logger.info("⚠️ 数据库未连接，以内存模式运行（无持久化）")
    yield
    await Database.disconnect()
    logger.info("🛑 Poker Face Arena 服务器已关闭")


app = FastAPI(
    title="Poker Face Arena API",
    description="扑克人格竞技场 · Game-OS V2.5 决策AI中台 · MBTI人格对手 × Kelly风控 × 三层AI架构",
    version="1.1.0",
    lifespan=lifespan
)

# ============================================
# CORS 配置 - 从环境变量读取，默认允许本地开发 + Vercel预览
# ============================================
def _parse_cors_origins() -> List[str]:
    raw = os.getenv("CORS_ORIGINS", "")
    defaults = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://hellomind-star.github.io",
    ]
    if raw.strip():
        extra = [o.strip() for o in raw.split(",") if o.strip()]
        defaults.extend(extra)
    return list(dict.fromkeys(defaults))


# MVP fix: CORS 使用明确白名单 + allow_credentials=True，并从 CORS_ORIGINS 环境变量读取额外域名
cors_origins = _parse_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 依赖注入
# ============================================

auth_handler = AuthHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)

# ============================================
# 全局状态管理
# ============================================

class GameManager:
    """游戏管理器 - 管理所有游戏会话"""
    
    def __init__(self):
        self.games: Dict[str, GameEngine] = {}
        # 修复：每个room允许多个WebSocket连接
        self.connections: Dict[str, List[WebSocket]] = {}
        self.ai_decision_maker = AIDecisionMaker()
        self._ai_tasks: Dict[str, asyncio.Task] = {}
    
    def create_game(self, player_name: str, ai_difficulty: str = "medium", ai_personality: str = None, auto_next_hand: bool = True) -> Dict:
        """创建新游戏（1v1: 玩家 + AI），支持MBTI人格AI"""
        game = GameEngine()
        game.auto_next_hand = auto_next_hand
        player = game.add_player(player_name, is_ai=False)
        persona = MBTI_PERSONALITIES.get(ai_personality) if ai_personality else None
        if persona:
            ai_name = f"{ai_personality} · {persona['archetype']}"
            agg = persona.get("aggressionLevel", 0.5)
            ai_difficulty = "hard" if agg >= 0.6 else ("medium" if agg >= 0.35 else "easy")
        else:
            ai_name = "AI Bot"
            ai_personality = ""
        ai_player = game.add_player(ai_name, is_ai=True, ai_difficulty=ai_difficulty, ai_personality=ai_personality)
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
        ai_count = len([p for p in game.players if p.is_ai])
        ai_player = game.add_player(f"AI Bot {ai_count + 1}", is_ai=True, ai_difficulty=difficulty)
        return {
            "player_id": ai_player.id,
            "game_state": game.get_state()
        }
    
    def get_game(self, game_id: str) -> Optional[GameEngine]:
        return self.games.get(game_id)
    
    def remove_game(self, game_id: str):
        if game_id in self.games:
            del self.games[game_id]
        if game_id in self.connections:
            del self.connections[game_id]
    
    def register_connection(self, game_id: str, websocket: WebSocket):
        """注册WebSocket连接（一个房间多个连接）"""
        if game_id not in self.connections:
            self.connections[game_id] = []
        # 避免重复
        if websocket not in self.connections[game_id]:
            self.connections[game_id].append(websocket)
    
    def unregister_connection(self, game_id: str, websocket: WebSocket):
        if game_id in self.connections:
            try:
                self.connections[game_id].remove(websocket)
            except ValueError:
                pass
            if not self.connections[game_id]:
                del self.connections[game_id]
    
    async def broadcast(self, game_id: str, message: Dict):
        """广播消息给房间内所有WebSocket"""
        sockets = list(self.connections.get(game_id, []))
        dead = []
        for ws in sockets:
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.warning(f"广播失败，移除失效连接: {e}")
                dead.append(ws)
        for ws in dead:
            self.unregister_connection(game_id, ws)
    
    async def process_ai_turn(self, game_id: str):
        """处理AI回合 - 循环检查并执行所有待行动AI"""
        game = self.games.get(game_id)
        if not game:
            return
        
        # 最多循环N次，避免死循环
        for _ in range(20):
            if game.hand_over:
                break
            if not game.is_ai_turn():
                break
            
            ai_player = game.get_ai_player()
            if not ai_player:
                break
            
            # 思考延迟：优先按MBTI人格thinkingMs，回退难度映射
            persona = MBTI_PERSONALITIES.get(getattr(ai_player, "ai_personality", "") or "")
            if persona and persona.get("thinkingMs"):
                lo, hi = persona["thinkingMs"]
                think_time = random.uniform(lo, hi) / 1000.0
            else:
                think_time = {"easy": 0.5, "medium": 1.0, "hard": 1.5}.get(ai_player.ai_difficulty, 1.0)
            await asyncio.sleep(think_time)
            
            # 再检查一次，可能中途结束
            if game.hand_over or ai_player.folded or ai_player.all_in:
                break
            
            # 当前最大下注
            active_bets = [p.bet for p in game.players if not p.folded]
            current_bet_for_ai = max(active_bets) if active_bets else 0
            call_amount = current_bet_for_ai - ai_player.bet

            game_state_ai = {
                "hole_cards": [c.to_dict() for c in ai_player.hole_cards],
                "board_cards": [c.to_dict() for c in game.board],
                "pot": game.pot,
                "my_chips": ai_player.chips,
                "current_bet": current_bet_for_ai,
                "call_amount": call_amount,
                "position": "late",
                "stage": game.stage.value
            }

            try:
                mbti_name = getattr(ai_player, "ai_personality", "") or ""
                if mbti_name:
                    # MBTI 人格引擎：客观牌力 × 人格滤镜，决策附带人格化理由
                    pai = personality_ai_manager.get(game_id, mbti_name)
                    decision = pai.decide_action(game_state_ai)
                else:
                    ai = self.ai_decision_maker.get_ai(ai_player.ai_difficulty)
                    decision = ai.decide_action(game_state_ai)
            except Exception as e:
                logger.error(f"AI决策错误: {e}")
                # 出错就check/fold
                decision = {"action": "check" if call_amount == 0 else "fold"}
            
            action = decision.get("action", "fold")
            amount = int(decision.get("amount", 0))
            
            # AI的raise amount语义：ai_engine返回的是"加注总额"或"加注增量"，
            # 这里ai_engine的raise_amount是pot*系数作为"下注金额"，为了兼容，
            # 若amount < call_amount 则视为call；若amount > call_amount，raise增量 = amount - call_amount
            # game_engine.process_action中raise的amount是增量，所以转换一下
            if action == "raise":
                total_bet_target = max(amount, current_bet_for_ai + game.min_raise)
                raise_increment = total_bet_target - current_bet_for_ai
                if raise_increment < game.min_raise:
                    raise_increment = game.min_raise
                # 如果AI筹码不足以raise，则改为call或all-in
                needed = call_amount + raise_increment
                if needed >= ai_player.chips:
                    action = "allin"
                    amount = 0
                else:
                    amount = raise_increment
            elif action == "call":
                if call_amount == 0:
                    action = "check"
                amount = 0
            
            result = game.process_action(ai_player.id, action, amount)
            
            if result["success"]:
                await self.broadcast(game_id, {
                    "type": "ai_action",
                    "data": {
                        "player": ai_player.name,
                        "player_id": ai_player.id,
                        "action": action,
                        "amount": result.get("amount", 0),
                        "message": result["message"],
                        "reason": decision.get("reason", "")
                    }
                })
                await self.broadcast(game_id, {
                    "type": "game_state",
                    "data": game.get_state()
                })
            else:
                logger.warning(f"AI行动失败: {result.get('message')}")
                # 失败则强制check/fold以推进游戏
                fallback = "check" if game._get_call_amount(ai_player) == 0 else "fold"
                game.process_action(ai_player.id, fallback, 0)
                await self.broadcast(game_id, {"type": "game_state", "data": game.get_state()})
            
            if game.hand_over:
                await self._handle_hand_over(game_id, game)
                break
        
        # 若牌局未结束但已轮到人类玩家，简单结束任务
    
    async def _handle_hand_over(self, game_id: str, game: GameEngine):
        """处理牌局结束"""
        winners_data = None
        if game.winners:
            winners_data = [w.to_dict() for w in game.winners]
        elif game.winner:
            winners_data = [game.winner.to_dict()]
        await self.broadcast(game_id, {
            "type": "hand_over",
            "data": {
                "winner": game.winner.to_dict() if game.winner else None,
                "winners": winners_data,
                "pot": sum(w.get("total_bet", 0) for w in [p.to_dict() for p in game.players]) - 0
                if False else game.winner.chips if game.winner else 0
            }
        })
        # 1v1：自动开始下一手（延迟3秒）——仅 WS 模式默认开启；HTTP 轮询客户端由玩家显式调 /start
        if getattr(game, "auto_next_hand", True):
            await asyncio.sleep(3)
            if game_id in self.games:
                still_has_chips = [p for p in game.players if p.chips > 0]
                if len(still_has_chips) >= 2:
                    game.start_new_hand()
                    await self.broadcast(game_id, {"type": "game_state", "data": game.get_state()})
                    await self.broadcast(game_id, {"type": "system_message", "data": {"message": "🔄 新的一局开始"}})
                    # 新的一手可能还是AI先手（1v1 preflop SB=BTN=human先？SB是player0=human先？）
                    if not game.hand_over and game.is_ai_turn():
                        asyncio.create_task(self.process_ai_turn(game_id))


game_manager = GameManager()

# ============================================
# 基础路由
# ============================================

@app.get("/")
async def root():
    return {
        "name": "Poker Face Arena API",
        "version": "1.1.0",
        "status": "running",
        "tagline": "Read your opponent. Read yourself.",
        "documentation": "/docs",
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "games": len(game_manager.games),
        "connections": sum(len(v) for v in game_manager.connections.values()),
        "db_connected": Database.is_connected()
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
            ai_difficulty=request.ai_difficulty or "medium",
            ai_personality=request.ai_personality,
            auto_next_hand=request.auto_next_hand if request.auto_next_hand is not None else True
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"创建游戏失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/game/{game_id}/join")
async def join_game(game_id: str, request: GameJoin):
    result = game_manager.join_game(game_id, request.player_name or "Player")
    if not result:
        raise HTTPException(status_code=404, detail="游戏不存在")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"success": True, "data": result}


@app.get("/api/game/{game_id}")
async def get_game_state(game_id: str, player_id: Optional[str] = Query(None)):
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    return {"success": True, "data": game.get_state(viewer_id=player_id)}


@app.get("/api/game/{game_id}/analysis")
async def get_hand_analysis(game_id: str, player_id: str = Query(...)):
    """
    Kelly 实时决策面板：真胜率（蒙特卡洛逐街重算）+ 牌型识别 + 底池赔率 + Kelly 注额。
    仅返回请求玩家本人手牌的分析（不向他人泄露底牌信息）。
    """
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    player = next((p for p in game.players if p.id == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="玩家不存在")
    if player.is_ai:
        raise HTTPException(status_code=400, detail="仅支持人类玩家查询")

    try:
        call_amount = game._get_call_amount(player)
        data = kelly_analysis(
            hole_dicts=[c.to_dict() for c in player.hole_cards],
            board_dicts=[c.to_dict() for c in game.board],
            pot=game.pot,
            call_amount=max(call_amount, 0),
            my_chips=player.chips,
        )
        data["stage"] = game.stage.value
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"分析失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"分析失败: {e}")


@app.post("/api/game/{game_id}/ai/add")
async def add_ai_player(game_id: str, difficulty: str = Query("medium")):
    result = game_manager.add_ai_player(game_id, difficulty)
    if not result:
        raise HTTPException(status_code=404, detail="游戏不存在")
    await game_manager.broadcast(game_id, {
        "type": "player_joined",
        "data": {"message": "AI玩家加入了游戏", "player_id": result["player_id"]}
    })
    return {"success": True, "data": result}


@app.post("/api/game/{game_id}/action")
async def player_action(game_id: str, action: PlayerAction):
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    if game.current_player_index >= len(game.players):
        raise HTTPException(status_code=400, detail="无当前玩家")
    current_player = game.players[game.current_player_index]
    if current_player.id != action.player_id:
        raise HTTPException(status_code=400, detail=f"不是你的回合（当前是{current_player.name}）")
    
    result = game.process_action(action.player_id, action.action_type, action.amount or 0)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    await game_manager.broadcast(game_id, {"type": "action_result", "data": result})
    await game_manager.broadcast(game_id, {"type": "game_state", "data": game.get_state()})
    
    if game.hand_over:
        await game_manager._handle_hand_over(game_id, game)
    elif game.is_ai_turn():
        asyncio.create_task(game_manager.process_ai_turn(game_id))
    
    return {"success": True, "data": result}


@app.post("/api/game/{game_id}/start")
async def start_game(game_id: str):
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    game.start_new_hand()
    
    await game_manager.broadcast(game_id, {"type": "game_state", "data": game.get_state()})
    await game_manager.broadcast(game_id, {"type": "system_message", "data": {"message": "🃏 游戏开始！"}})
    
    if not game.hand_over and game.is_ai_turn():
        asyncio.create_task(game_manager.process_ai_turn(game_id))
    
    return {"success": True, "data": game.get_state()}


# ============================================
# WebSocket 连接
# ============================================

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    await websocket.accept()
    logger.info(f"WebSocket 连接建立: {game_id}")
    
    game_manager.register_connection(game_id, websocket)
    
    game = game_manager.get_game(game_id)
    if game:
        await websocket.send_json({"type": "game_state", "data": game.get_state()})
        await websocket.send_json({"type": "system_message", "data": {"message": "♠️ 欢迎来到 Poker Face Arena · 扑克人格竞技场"}})
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "data": {"message": "消息格式错误"}})
                continue
            
            message_type = message.get("type")
            
            if message_type == "ping":
                await websocket.send_json({"type": "pong"})
            
            elif message_type == "action":
                action_data = message.get("data", {})
                player_id = action_data.get("player_id")
                action_type = action_data.get("action")
                amount = int(action_data.get("amount", 0) or 0)
                
                game = game_manager.get_game(game_id)
                if not game:
                    await websocket.send_json({"type": "error", "data": {"message": "游戏不存在"}})
                    continue
                
                if game.current_player_index >= len(game.players):
                    await websocket.send_json({"type": "error", "data": {"message": "无当前玩家"}})
                    continue
                
                if game.players[game.current_player_index].id != player_id:
                    await websocket.send_json({"type": "error", "data": {"message": "不是你的回合"}})
                    continue
                
                result = game.process_action(player_id, action_type, amount)
                
                if result["success"]:
                    await game_manager.broadcast(game_id, {"type": "action_result", "data": result})
                    await game_manager.broadcast(game_id, {"type": "game_state", "data": game.get_state()})
                    
                    if game.hand_over:
                        await game_manager._handle_hand_over(game_id, game)
                    elif game.is_ai_turn():
                        asyncio.create_task(game_manager.process_ai_turn(game_id))
                else:
                    await websocket.send_json({"type": "error", "data": {"message": result["message"]}})
            
            elif message_type == "chat":
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
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
    finally:
        game_manager.unregister_connection(game_id, websocket)


# ============================================
# 用户认证 API
# ============================================

@app.post("/api/auth/register")
async def register(user_data: UserCreate):
    existing_user = await Database.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    existing_username = await Database.get_user_by_username(user_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="用户名已被使用")
    
    user = await Database.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    
    token = auth_handler.create_access_token(user["id"])
    
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user": user,
        "data": {"user": user, "token": token}
    }


@app.post("/api/auth/login")
async def login(request: Request):
    """用户登录（支持表单和 JSON）"""
    username = None
    password = None
    
    try:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
    except Exception:
        pass
    
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
    if not token:
        raise HTTPException(status_code=401, detail="未提供token")
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
    return {"success": True, "data": stats}


@app.get("/api/stats/{player_id}/history")
async def get_player_history(player_id: str, limit: int = 50):
    history = await Database.get_player_history(player_id, limit)
    return {"success": True, "data": history}


# ============================================
# 错误处理
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "服务器内部错误"}
    )


# ============================================
# 启动入口（支持 $PORT 环境变量，适配 Railway/Render 等）
# ============================================

if __name__ == "__main__":
    import uvicorn
    # 默认端口 8080（对齐 Railway 代理转发端口），读取 PORT 环境变量（适配 Vercel/Railway/Render）
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1,
        log_level="info"
    )
