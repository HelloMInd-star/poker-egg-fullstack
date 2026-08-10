"""
数据库连接和操作
使用 PostgreSQL + asyncpg；密码使用 passlib[bcrypt] 哈希
"""
import asyncpg
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

# 密码哈希 - 优先使用bcrypt；如不可用降级到passlib或明文
_bcrypt_lib = None
_passlib_ctx = None

try:
    import bcrypt as _bcrypt_lib
except ImportError:
    _bcrypt_lib = None

if _bcrypt_lib is None:
    try:
        from passlib.context import CryptContext
        _passlib_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    except Exception:
        _passlib_ctx = None


def hash_password(password: str) -> str:
    """哈希密码"""
    if isinstance(password, str):
        pw_bytes = password.encode("utf-8")[:72]  # bcrypt 限制72字节
    else:
        pw_bytes = password[:72]
    if _bcrypt_lib is not None:
        salt = _bcrypt_lib.gensalt()
        return _bcrypt_lib.hashpw(pw_bytes, salt).decode("utf-8")
    if _passlib_ctx is not None:
        return _passlib_ctx.hash(password)
    return f"plain:{password}"


def verify_password(password: str, password_hash: str) -> bool:
    """验证密码"""
    if not password_hash:
        return False
    if password_hash.startswith("plain:"):
        return password == password_hash[len("plain:"):]
    if isinstance(password, str):
        pw_bytes = password.encode("utf-8")[:72]
    else:
        pw_bytes = password[:72]
    if _bcrypt_lib is not None:
        try:
            return _bcrypt_lib.checkpw(pw_bytes, password_hash.encode("utf-8"))
        except Exception:
            return False
    if _passlib_ctx is not None:
        try:
            return _passlib_ctx.verify(password, password_hash)
        except Exception:
            return False
    return password == password_hash


class Database:
    """数据库管理类"""
    
    _pool: asyncpg.Pool = None
    _memory_users: Dict[str, Dict] = {}  # 内存模式的用户存储
    _db_connected: bool = False
    
    @classmethod
    async def connect(cls):
        """连接数据库"""
        if cls._pool:
            return
        
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/poker_egg")
        
        try:
            cls._pool = await asyncpg.create_pool(
                database_url,
                min_size=2,
                max_size=10
            )
            await cls._create_tables()
            cls._db_connected = True
            print("✅ 数据库连接成功")
        except Exception as e:
            print(f"⚠️ 数据库连接失败，使用内存模式: {e}")
            cls._pool = None
            cls._db_connected = False
    
    @classmethod
    def is_connected(cls) -> bool:
        return cls._db_connected
    
    @classmethod
    async def disconnect(cls):
        """断开数据库连接"""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
    
    @classmethod
    async def _create_tables(cls):
        """创建数据表"""
        if not cls._pool:
            return
        
        async with cls._pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    chips INTEGER DEFAULT 1000,
                    total_hands INTEGER DEFAULT 0,
                    hands_won INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                    id SERIAL PRIMARY KEY,
                    game_id VARCHAR(36) NOT NULL,
                    player_id VARCHAR(36) NOT NULL,
                    hand_data JSONB NOT NULL,
                    result VARCHAR(20),
                    chips_change INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_training_data (
                    id SERIAL PRIMARY KEY,
                    game_id VARCHAR(36) NOT NULL,
                    state_data JSONB NOT NULL,
                    action_taken VARCHAR(20),
                    result VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_game_history_player ON game_history(player_id);
                CREATE INDEX IF NOT EXISTS idx_game_history_game ON game_history(game_id);
                CREATE INDEX IF NOT EXISTS idx_ai_training_game ON ai_training_data(game_id);
            """)
    
    @classmethod
    async def get_user_by_email(cls, email: str) -> Optional[Dict]:
        """根据邮箱获取用户"""
        if not cls._pool:
            for u in cls._memory_users.values():
                if u.get("email") == email:
                    return dict(u)
            return None
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1",
                email
            )
            return dict(row) if row else None
    
    @classmethod
    async def get_user_by_username(cls, username: str) -> Optional[Dict]:
        """根据用户名获取用户"""
        if not cls._pool:
            for u in cls._memory_users.values():
                if u.get("username") == username:
                    return dict(u)
            return None
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE username = $1",
                username
            )
            return dict(row) if row else None
    
    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Optional[Dict]:
        """根据ID获取用户"""
        if not cls._pool:
            u = cls._memory_users.get(user_id)
            return dict(u) if u else None
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1",
                user_id
            )
            return dict(row) if row else None
    
    @classmethod
    async def create_user(cls, username: str, email: str, password: str) -> Dict:
        """创建用户（密码在调用前或此处哈希）"""
        pw_hash = hash_password(password)
        user_id = str(uuid.uuid4())[:8]
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": pw_hash,
            "chips": 1000,
            "total_hands": 0,
            "hands_won": 0
        }
        
        if not cls._pool:
            cls._memory_users[user_id] = user
            return {k: v for k, v in user.items() if k != "password_hash"}
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO users (id, username, email, password_hash, chips)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, username, email, chips, total_hands, hands_won, created_at
                """,
                user_id, username, email, pw_hash, 1000
            )
            return dict(row) if row else None
    
    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Optional[Dict]:
        """验证用户名密码"""
        if not cls._pool:
            # 内存模式：如果用户存在则校验；否则自动创建（方便开发）
            user = None
            for u in cls._memory_users.values():
                if u.get("username") == username:
                    user = u
                    break
            if user:
                if verify_password(password, user.get("password_hash", "")):
                    return {k: v for k, v in user.items() if k != "password_hash"}
                return None
            # 开发模式：首次登录自动注册
            new_user = {
                "id": str(uuid.uuid4())[:8],
                "username": username,
                "email": f"{username}@demo.local",
                "password_hash": hash_password(password),
                "chips": 1000,
                "total_hands": 0,
                "hands_won": 0
            }
            cls._memory_users[new_user["id"]] = new_user
            return {k: v for k, v in new_user.items() if k != "password_hash"}
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE username = $1",
                username
            )
            if not row:
                return None
            user = dict(row)
            if verify_password(password, user.get("password_hash", "")):
                return {k: v for k, v in user.items() if k != "password_hash"}
            return None
    
    @classmethod
    async def save_game_history(cls, game_id: str, player_id: str, hand_data: Dict, result: str, chips_change: int):
        """保存游戏历史"""
        if not cls._pool:
            return
        
        async with cls._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO game_history (game_id, player_id, hand_data, result, chips_change)
                VALUES ($1, $2, $3, $4, $5)
                """,
                game_id, player_id, json.dumps(hand_data), result, chips_change
            )
    
    @classmethod
    async def get_player_stats(cls, player_id: str) -> Optional[Dict]:
        """获取玩家统计数据"""
        if not cls._pool:
            return None
        
        async with cls._pool.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT chips, total_hands, hands_won FROM users WHERE id = $1",
                player_id
            )
            if not user:
                return None
            history = await conn.fetch(
                """
                SELECT 
                    COUNT(*) as total_hands,
                    SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
                    SUM(chips_change) as total_chips_won
                FROM game_history
                WHERE player_id = $1
                """,
                player_id
            )
            total = history[0] if history else None
            return {
                "chips": user["chips"],
                "total_hands": user["total_hands"],
                "hands_won": user["hands_won"],
                "win_rate": user["hands_won"] / user["total_hands"] if user["total_hands"] > 0 else 0,
                "total_chips_won": total["total_chips_won"] if total else 0
            }
    
    @classmethod
    async def get_player_history(cls, player_id: str, limit: int = 50) -> List[Dict]:
        """获取玩家历史记录"""
        if not cls._pool:
            return []
        
        async with cls._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT game_id, hand_data, result, chips_change, created_at
                FROM game_history
                WHERE player_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                player_id, limit
            )
            return [dict(row) for row in rows]
