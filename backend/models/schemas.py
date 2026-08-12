"""
Pydantic 数据模型
用于请求/响应验证
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserCreate(BaseModel):
    """用户注册"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """用户登录"""
    username: str
    password: str


class Token(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"
    user: Optional[Dict] = None


class GameCreate(BaseModel):
    """创建游戏"""
    player_name: Optional[str] = "Player"
    ai_difficulty: Optional[str] = "medium"
    ai_personality: Optional[str] = None  # MBTI人格类型(如INTJ)，优先于ai_difficulty


class GameJoin(BaseModel):
    """加入游戏"""
    player_name: Optional[str] = "Player"


class PlayerAction(BaseModel):
    """玩家行动"""
    player_id: str
    action_type: str = Field(..., pattern="^(fold|check|call|raise|allin)$")
    amount: Optional[int] = 0


class GameState(BaseModel):
    """游戏状态"""
    id: str
    players: List[Dict]
    board: List[Dict]
    pot: int
    stage: str
    hand_over: bool
    winner: Optional[Dict]
    current_player: int
    history: List[Dict]


class PlayerStats(BaseModel):
    """玩家统计"""
    player_id: str
    total_hands: int
    hands_won: int
    win_rate: float
    total_chips_won: int
    best_hand: str
    aggression: float


class WebSocketMessage(BaseModel):
    """WebSocket消息"""
    type: str
    data: Optional[Dict] = None
