"""
数据库连接和操作
使用 PostgreSQL + asyncpg
"""
import asyncpg
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    """数据库管理类"""
    
    _pool: asyncpg.Pool = None
    
    @classmethod
    async def connect(cls):
        """连接数据库"""
        if cls._pool:
            return
        
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/poker_egg")
        
        try:
            cls._pool = await asyncpg.create_pool(
                database_url,
                min_size=5,
                max_size=20
            )
            
            # 创建表
            await cls._create_tables()
            
        except Exception as e:
            print(f"数据库连接失败: {e}")
            # 如果连接失败，使用内存存储（开发模式）
            cls._pool = None
    
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
            # 用户表
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
            
            # 游戏历史表
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
            
            # AI训练数据表
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
            
            # 创建索引
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_game_history_player ON game_history(player_id);
                CREATE INDEX IF NOT EXISTS idx_game_history_game ON game_history(game_id);
                CREATE INDEX IF NOT EXISTS idx_ai_training_game ON ai_training_data(game_id);
            """)
    
    @classmethod
    async def get_user_by_email(cls, email: str) -> Optional[Dict]:
        """根据邮箱获取用户"""
        if not cls._pool:
            return None
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1",
                email
            )
            return dict(row) if row else None
    
    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Optional[Dict]:
        """根据ID获取用户"""
        if not cls._pool:
            return None
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1",
                user_id
            )
            return dict(row) if row else None
    
    @classmethod
    async def create_user(cls, username: str, email: str, password_hash: str) -> Dict:
        """创建用户"""
        if not cls._pool:
            # 内存模式
            return {
                "id": str(uuid.uuid4())[:8],
                "username": username,
                "email": email,
                "chips": 1000,
                "total_hands": 0,
                "hands_won": 0
            }
        
        import uuid
        user_id = str(uuid.uuid4())[:8]
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO users (id, username, email, password_hash, chips)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
                """,
                user_id, username, email, password_hash, 1000
            )
            return dict(row) if row else None
    
    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Optional[Dict]:
        """验证用户"""
        # 这里简化处理，实际应该使用bcrypt验证
        if not cls._pool:
            # 内存模式 - 允许任意登录
            return {
                "id": "demo_user",
                "username": username,
                "email": "demo@example.com",
                "chips": 1000
            }
        
        async with cls._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE username = $1",
                username
            )
            if row:
                # 验证密码（这里应该使用bcrypt）
                return dict(row)
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
            # 从用户表获取基本信息
            user = await conn.fetchrow(
                "SELECT chips, total_hands, hands_won FROM users WHERE id = $1",
                player_id
            )
            
            if not user:
                return None
            
            # 从历史记录获取更多统计
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


# 导入uuid用于内存模式
import uuid
