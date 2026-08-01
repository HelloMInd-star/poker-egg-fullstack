"""
德州扑克游戏引擎
处理：发牌、行动、结算、状态管理
"""
import random
from typing import List, Dict, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class Stage(Enum):
    """游戏阶段"""
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"


class ActionType(Enum):
    """行动类型"""
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"
    ALL_IN = "allin"


@dataclass
class Card:
    """扑克牌"""
    rank: str
    suit: str
    color: str = "black"
    
    def __post_init__(self):
        self.color = "red" if self.suit in ['♥', '♦'] else "black"
        self.rank_value = self._rank_to_value(self.rank)
    
    @staticmethod
    def _rank_to_value(rank: str) -> int:
        values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return values.get(rank, 0)
    
    def to_dict(self) -> Dict:
        return {
            "rank": self.rank,
            "suit": self.suit,
            "color": self.color,
            "rank_value": self.rank_value
        }


@dataclass
class Player:
    """玩家"""
    id: str
    name: str
    chips: int = 1000
    hole_cards: List[Card] = field(default_factory=list)
    bet: int = 0
    folded: bool = False
    all_in: bool = False
    has_acted: bool = False
    is_ai: bool = False
    ai_difficulty: str = "medium"
    
    def reset_hand(self):
        """重置手牌状态"""
        self.hole_cards = []
        self.bet = 0
        self.folded = False
        self.all_in = False
        self.has_acted = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "chips": self.chips,
            "bet": self.bet,
            "folded": self.folded,
            "all_in": self.all_in,
            "has_acted": self.has_acted,
            "is_ai": self.is_ai,
            "hole_cards": [c.to_dict() for c in self.hole_cards],
            "ai_difficulty": self.ai_difficulty
        }


class Deck:
    """牌堆"""
    SUITS = ['♠', '♥', '♦', '♣']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        """重置牌堆"""
        self.cards = [
            Card(rank, suit)
            for suit in self.SUITS
            for rank in self.RANKS
        ]
        self.shuffle()
    
    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)
    
    def draw(self, count: int = 1) -> List[Card]:
        """抽牌"""
        drawn = []
        for _ in range(count):
            if self.cards:
                drawn.append(self.cards.pop())
        return drawn


class HandEvaluator:
    """手牌评估器"""
    
    @staticmethod
    def evaluate(cards: List[Card]) -> Dict:
        """
        评估手牌强度
        返回: {
            "strength": float 0-1,
            "hand_name": str,
            "rank": int 排名
        }
        """
        if len(cards) < 5:
            return {"strength": 0.0, "hand_name": "Unknown", "rank": 0}
        
        # 按牌值排序
        sorted_cards = sorted(cards, key=lambda c: c.rank_value, reverse=True)
        ranks = [c.rank_value for c in sorted_cards]
        suits = [c.suit for c in sorted_cards]
        
        # 检查同花
        is_flush = any(suits.count(s) >= 5 for s in set(suits))
        
        # 检查顺子
        unique_ranks = sorted(set(ranks), reverse=True)
        is_straight = False
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                is_straight = True
                break
        # 特殊：A-2-3-4-5
        if set([14, 2, 3, 4, 5]).issubset(set(unique_ranks)):
            is_straight = True
        
        # 检查对子
        rank_counts = {}
        for r in ranks:
            rank_counts[r] = rank_counts.get(r, 0) + 1
        
        pairs = [r for r, c in rank_counts.items() if c == 2]
        trips = [r for r, c in rank_counts.items() if c == 3]
        quads = [r for r, c in rank_counts.items() if c == 4]
        
        # 判断牌型
        strength = 0.0
        hand_name = "High Card"
        hand_rank = 0
        
        if is_flush and is_straight:
            # 同花顺
            strength = 1.0
            hand_name = "Straight Flush"
            hand_rank = 9
        elif quads:
            strength = 0.95
            hand_name = "Four of a Kind"
            hand_rank = 8
        elif trips and pairs:
            strength = 0.9
            hand_name = "Full House"
            hand_rank = 7
        elif is_flush:
            strength = 0.85
            hand_name = "Flush"
            hand_rank = 6
        elif is_straight:
            strength = 0.8
            hand_name = "Straight"
            hand_rank = 5
        elif trips:
            strength = 0.7
            hand_name = "Three of a Kind"
            hand_rank = 4
        elif len(pairs) == 2:
            strength = 0.6
            hand_name = "Two Pair"
            hand_rank = 3
        elif pairs:
            strength = 0.4
            hand_name = "One Pair"
            hand_rank = 2
        else:
            # 高牌
            high_card = max(ranks)
            strength = 0.1 + (high_card - 2) / 12 * 0.3
            hand_name = "High Card"
            hand_rank = 1
        
        return {
            "strength": strength,
            "hand_name": hand_name,
            "rank": hand_rank,
            "high_card": max(ranks) if ranks else 0
        }
    
    @staticmethod
    def compare_hands(hand1: Dict, hand2: Dict) -> int:
        """比较两手牌，返回 1: hand1赢, -1: hand2赢, 0: 平局"""
        if hand1["rank"] != hand2["rank"]:
            return 1 if hand1["rank"] > hand2["rank"] else -1
        
        # 同级别比较高牌
        if hand1["high_card"] != hand2["high_card"]:
            return 1 if hand1["high_card"] > hand2["high_card"] else -1
        
        return 0


class GameEngine:
    """游戏引擎主类"""
    
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        self.players: List[Player] = []
        self.deck = Deck()
        self.board: List[Card] = []
        self.pot = 0
        self.stage = Stage.PREFLOP
        self.current_player_index = 0
        self.big_blind = 20
        self.small_blind = 10
        self.last_raise = 0
        self.hand_over = False
        self.winner = None
        self.created_at = datetime.now()
        self.history: List[Dict] = []
    
    def add_player(self, name: str, is_ai: bool = False, ai_difficulty: str = "medium") -> Player:
        """添加玩家"""
        player = Player(
            id=str(uuid.uuid4())[:8],
            name=name,
            chips=1000,
            is_ai=is_ai,
            ai_difficulty=ai_difficulty
        )
        self.players.append(player)
        return player
    
    def start_new_hand(self):
        """开始新的一局"""
        # 重置所有玩家状态
        for player in self.players:
            player.reset_hand()
        
        # 重置牌桌
        self.deck.reset()
        self.board = []
        self.pot = 0
        self.stage = Stage.PREFLOP
        self.hand_over = False
        self.winner = None
        self.last_raise = 0
        
        # 发牌
        for player in self.players:
            if not player.folded and player.chips > 0:
                player.hole_cards = self.deck.draw(2)
        
        # 设置盲注
        self._post_blinds()
        
        # 重置行动状态
        for player in self.players:
            player.has_acted = False
        
        self.current_player_index = 0
        self._add_history("新的一局开始", "system")
    
    def _post_blinds(self):
        """设置盲注"""
        active_players = [p for p in self.players if p.chips > 0]
        if len(active_players) < 2:
            return
        
        # 小盲
        sb_player = active_players[0]
        sb_amount = min(self.small_blind, sb_player.chips)
        sb_player.chips -= sb_amount
        sb_player.bet = sb_amount
        self.pot += sb_amount
        
        # 大盲
        bb_player = active_players[1] if len(active_players) > 1 else active_players[0]
        bb_amount = min(self.big_blind, bb_player.chips)
        bb_player.chips -= bb_amount
        bb_player.bet = bb_amount
        self.pot += bb_amount
        
        self._add_history(f"小盲 {sb_player.name}: {sb_amount}, 大盲 {bb_player.name}: {bb_amount}", "system")
    
    def process_action(self, player_id: str, action_type: str, amount: int = 0) -> Dict:
        """处理玩家行动"""
        if self.hand_over:
            return {"success": False, "message": "本局已结束"}
        
        player = self._get_player(player_id)
        if not player:
            return {"success": False, "message": "玩家不存在"}
        
        if player.folded or player.all_in:
            return {"success": False, "message": "玩家已弃牌或All-in"}
        
        # 根据行动类型处理
        result = {"success": True, "message": "", "action": action_type}
        
        if action_type == "fold":
            player.folded = True
            result["message"] = f"{player.name} 弃牌"
        
        elif action_type == "check":
            result["message"] = f"{player.name} 过牌"
        
        elif action_type == "call":
            call_amount = self._get_call_amount(player)
            call_amount = min(call_amount, player.chips)
            player.chips -= call_amount
            player.bet += call_amount
            self.pot += call_amount
            result["message"] = f"{player.name} 跟注 {call_amount}"
            result["amount"] = call_amount
        
        elif action_type == "raise":
            raise_amount = min(amount, player.chips)
            if raise_amount < self.big_blind:
                raise_amount = self.big_blind
            player.chips -= raise_amount
            player.bet += raise_amount
            self.pot += raise_amount
            self.last_raise = raise_amount
            result["message"] = f"{player.name} 加注 {raise_amount}"
            result["amount"] = raise_amount
        
        elif action_type == "allin":
            all_amount = player.chips
            player.chips = 0
            player.bet += all_amount
            self.pot += all_amount
            player.all_in = True
            result["message"] = f"{player.name} ALL IN {all_amount}"
            result["amount"] = all_amount
        
        player.has_acted = True
        self._add_history(result["message"], "action")
        
        # 检查是否所有玩家都行动完毕
        self._check_round_complete()
        
        return result
    
    def _get_call_amount(self, player: Player) -> int:
        """计算跟注金额"""
        max_bet = max([p.bet for p in self.players if not p.folded])
        return max_bet - player.bet
    
    def _check_round_complete(self):
        """检查当前轮是否结束"""
        active_players = [p for p in self.players if not p.folded and not p.all_in]
        players_acted = [p for p in active_players if p.has_acted]
        
        # 如果只剩一个玩家或所有玩家都行动了
        if len(active_players) <= 1 or len(players_acted) == len(active_players):
            self._advance_stage()
    
    def _advance_stage(self):
        """进入下一阶段"""
        if self.stage == Stage.PREFLOP:
            # 发翻牌
            self.board = self.deck.draw(3)
            self.stage = Stage.FLOP
            self._add_history(f"翻牌: {self._board_str()}", "system")
        
        elif self.stage == Stage.FLOP:
            # 发转牌
            self.board.extend(self.deck.draw(1))
            self.stage = Stage.TURN
            self._add_history(f"转牌: {self._board_str()}", "system")
        
        elif self.stage == Stage.TURN:
            # 发河牌
            self.board.extend(self.deck.draw(1))
            self.stage = Stage.RIVER
            self._add_history(f"河牌: {self._board_str()}", "system")
        
        elif self.stage == Stage.RIVER:
            # 摊牌
            self.stage = Stage.SHOWDOWN
            self._showdown()
            return
        
        # 重置玩家行动状态
        for player in self.players:
            if not player.folded and not player.all_in:
                player.has_acted = False
        
        # 检查是否只剩一个玩家
        active_players = [p for p in self.players if not p.folded and not p.all_in]
        if len(active_players) == 1:
            self._award_pot(active_players[0])
    
    def _showdown(self):
        """摊牌"""
        active_players = [p for p in self.players if not p.folded]
        
        if len(active_players) == 1:
            self._award_pot(active_players[0])
            return
        
        # 评估所有玩家手牌
        hand_evaluations = []
        for player in active_players:
            all_cards = player.hole_cards + self.board
            evaluation = HandEvaluator.evaluate(all_cards)
            hand_evaluations.append({
                "player": player,
                "evaluation": evaluation
            })
        
        # 找赢家
        winner = max(hand_evaluations, key=lambda x: x["evaluation"]["strength"])
        self._award_pot(winner["player"])
        self._add_history(
            f"{winner['player'].name} 赢了 {self.pot} 筹码! ({winner['evaluation']['hand_name']})",
            "winner"
        )
    
    def _award_pot(self, winner: Player):
        """分配底池"""
        winner.chips += self.pot
        self.winner = winner
        self.hand_over = True
        self._add_history(f"{winner.name} 赢得 {self.pot} 筹码!", "winner")
        self.pot = 0
    
    def _board_str(self) -> str:
        """牌面字符串"""
        return " ".join([f"{c.rank}{c.suit}" for c in self.board])
    
    def _add_history(self, message: str, type: str):
        """添加历史记录"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "type": type
        })
        # 限制历史记录数量
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def _get_player(self, player_id: str) -> Optional[Player]:
        """获取玩家"""
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def get_state(self) -> Dict:
        """获取游戏状态"""
        return {
            "id": self.id,
            "players": [p.to_dict() for p in self.players],
            "board": [c.to_dict() for c in self.board],
            "pot": self.pot,
            "stage": self.stage.value,
            "hand_over": self.hand_over,
            "winner": self.winner.to_dict() if self.winner else None,
            "current_player": self.current_player_index,
            "last_raise": self.last_raise,
            "big_blind": self.big_blind,
            "small_blind": self.small_blind,
            "history": self.history[-10:]  # 最近10条
        }
    
    def get_ai_player(self) -> Optional[Player]:
        """获取AI玩家"""
        for player in self.players:
            if player.is_ai and not player.folded and not player.all_in:
                return player
        return None
    
    def is_ai_turn(self) -> bool:
        """是否轮到AI"""
        if self.hand_over:
            return False
        current_player = self.players[self.current_player_index]
        return current_player.is_ai and not current_player.folded
