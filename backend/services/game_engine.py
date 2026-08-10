"""
德州扑克游戏引擎
处理：发牌、行动、结算、状态管理
修复版：加注逻辑、轮次推进、牌力评估、1v1盲注顺序
"""
import random
from typing import List, Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from itertools import combinations


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
    bet: int = 0            # 当前轮下注总额
    total_bet: int = 0      # 本局累计下注
    folded: bool = False
    all_in: bool = False
    has_acted: bool = False
    is_ai: bool = False
    ai_difficulty: str = "medium"
    # 盲注位标记
    is_sb: bool = False
    is_bb: bool = False
    # dealer/button标记（1v1中SB是BTN）
    is_dealer: bool = False
    
    def reset_hand(self):
        """重置手牌状态"""
        self.hole_cards = []
        self.bet = 0
        self.total_bet = 0
        self.folded = False
        self.all_in = False
        self.has_acted = False
        self.is_sb = False
        self.is_bb = False
        self.is_dealer = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "chips": self.chips,
            "bet": self.bet,
            "total_bet": self.total_bet,
            "folded": self.folded,
            "all_in": self.all_in,
            "has_acted": self.has_acted,
            "is_ai": self.is_ai,
            "is_sb": self.is_sb,
            "is_bb": self.is_bb,
            "is_dealer": self.is_dealer,
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
    """手牌评估器 - 修复版"""
    
    RANK_NAMES = {
        0: "Unknown",
        1: "High Card",
        2: "One Pair",
        3: "Two Pair",
        4: "Three of a Kind",
        5: "Straight",
        6: "Flush",
        7: "Full House",
        8: "Four of a Kind",
        9: "Straight Flush"
    }
    
    @staticmethod
    def _rank_value(rank_str: str) -> int:
        return Card._rank_to_value(rank_str)
    
    @classmethod
    def _best_five(cls, cards: List[Card]) -> Tuple[int, List[int]]:
        """
        从N张牌(5-7)中选出最佳5张牌型。
        返回: (hand_rank, tie_breakers)  tie_breakers 是按重要性降序的牌值列表，用于比较kicker
        """
        best_rank = -1
        best_tie = []
        
        for five in combinations(cards, 5):
            rank, tie = cls._evaluate_five(five)
            # 比较：rank高的好；rank相同时逐位比较tiebreaker
            if rank > best_rank or (rank == best_rank and tie > best_tie):
                best_rank = rank
                best_tie = tie
        
        return best_rank, best_tie
    
    @classmethod
    def _evaluate_five(cls, five: Tuple[Card, ...]) -> Tuple[int, List[int]]:
        """评估恰好5张牌"""
        ranks = sorted([c.rank_value for c in five], reverse=True)
        suits = [c.suit for c in five]
        
        # 统计各点数出现次数
        rank_counts: Dict[int, int] = {}
        for r in ranks:
            rank_counts[r] = rank_counts.get(r, 0) + 1
        # 按 (次数降序, 点数降序) 排序
        count_groups = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))
        counts_sorted = [c for _, c in count_groups]
        values_sorted = [v for v, _ in count_groups]
        
        is_flush = len(set(suits)) == 1
        
        # 检测顺子
        unique_ranks = sorted(set(ranks), reverse=True)
        is_straight = False
        straight_high = 0
        if len(unique_ranks) == 5:
            if unique_ranks[0] - unique_ranks[4] == 4:
                is_straight = True
                straight_high = unique_ranks[0]
            # A-2-3-4-5 特殊顺子（用A当1）
            elif unique_ranks == [14, 5, 4, 3, 2]:
                is_straight = True
                straight_high = 5
        
        # 同花顺/皇家同花顺
        if is_flush and is_straight:
            return (9, [straight_high])
        # 四条
        if counts_sorted[0] == 4:
            # four value + kicker
            return (8, values_sorted)
        # 葫芦（三条+对子）
        if counts_sorted[0] == 3 and counts_sorted[1] == 2:
            return (7, values_sorted)
        # 同花
        if is_flush:
            return (6, ranks)
        # 顺子
        if is_straight:
            return (5, [straight_high])
        # 三条
        if counts_sorted[0] == 3:
            return (4, values_sorted)
        # 两对
        if counts_sorted[0] == 2 and counts_sorted[1] == 2:
            return (3, values_sorted)
        # 一对
        if counts_sorted[0] == 2:
            return (2, values_sorted)
        # 高牌
        return (1, ranks)
    
    @classmethod
    def evaluate(cls, cards: List[Card]) -> Dict:
        """
        评估手牌强度
        返回: {
            "strength": float 0-1,
            "hand_name": str,
            "rank": int,
            "tie_breakers": List[int],
            "high_card": int
        }
        """
        if len(cards) < 5:
            # 不足5张时：粗略估计（对子强度 + 高牌）
            ranks = [c.rank_value for c in cards]
            rank_counts: Dict[int, int] = {}
            for r in ranks:
                rank_counts[r] = rank_counts.get(r, 0) + 1
            pairs = sum(1 for c in rank_counts.values() if c >= 2)
            high = max(ranks) if ranks else 2
            if pairs >= 1:
                pair_val = max(v for v, c in rank_counts.items() if c >= 2)
                strength = 0.2 + (pair_val - 2) / 12 * 0.2
                name = "Pair (draw)"
                r = 2
            else:
                strength = 0.05 + (high - 2) / 12 * 0.15
                name = "High Card"
                r = 1
            return {
                "strength": strength,
                "hand_name": name,
                "rank": r,
                "tie_breakers": sorted(ranks, reverse=True),
                "high_card": high
            }
        
        rank, tie = cls._best_five(cards)
        # 粗略强度映射
        base_strength = {
            9: 1.0, 8: 0.95, 7: 0.9, 6: 0.85,
            5: 0.8, 4: 0.7, 3: 0.6, 2: 0.4, 1: 0.2
        }.get(rank, 0.1)
        # 加上tiebreaker带来的微调
        if tie:
            kicker_bonus = (tie[0] - 2) / 12 * 0.05
            strength = min(base_strength + kicker_bonus, 1.0)
        else:
            strength = base_strength
        
        return {
            "strength": strength,
            "hand_name": cls.RANK_NAMES.get(rank, "Unknown"),
            "rank": rank,
            "tie_breakers": tie,
            "high_card": tie[0] if tie else max((c.rank_value for c in cards), default=0)
        }
    
    @classmethod
    def compare_hands(cls, hand1: Dict, hand2: Dict) -> int:
        """比较两手牌，返回 1: hand1赢, -1: hand2赢, 0: 平局"""
        if hand1["rank"] != hand2["rank"]:
            return 1 if hand1["rank"] > hand2["rank"] else -1
        
        # 同级别：按 tie_breakers 逐位比较
        t1 = hand1.get("tie_breakers", [hand1.get("high_card", 0)])
        t2 = hand2.get("tie_breakers", [hand2.get("high_card", 0)])
        
        for a, b in zip(t1, t2):
            if a != b:
                return 1 if a > b else -1
        return 0


class GameEngine:
    """游戏引擎主类 - 修复版"""
    
    MIN_RAISE = 20  # 最小加注增量（等于大盲）
    
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
        self.current_bet = 0       # 当前轮最大下注
        self.min_raise = self.big_blind  # 当前最小加注增量
        self.hand_over = False
        self.winner: Optional[Player] = None
        self.winners: List[Player] = field(default_factory=list) if False else []  # 分池可能多赢家
        self.created_at = datetime.now()
        self.history: List[Dict] = []
        self.dealer_index = 0  # 庄位索引（1v1中SB=BTN）
        self.last_raiser_index: Optional[int] = None  # 最后加注者索引
    
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
        # 清理上局状态
        for player in self.players:
            player.reset_hand()
        
        self.deck.reset()
        self.board = []
        self.pot = 0
        self.stage = Stage.PREFLOP
        self.hand_over = False
        self.winner = None
        self.winners = []
        self.current_bet = 0
        self.min_raise = self.big_blind
        self.last_raiser_index = None
        
        # 过滤有筹码的玩家
        active_players = [p for p in self.players if p.chips > 0]
        if len(active_players) < 2:
            self._add_history("筹码不足，无法开始", "system")
            self.hand_over = True
            return
        
        # 盲注旋转（第一局 dealer=0 即 player1=SB=BTN, player2=BB；下一局轮换）
        # 1v1规则: BTN/SB先行动preflop，BB最后；翻牌后BB先行动，BTN最后
        n = len(active_players)
        sb_idx = self.dealer_index % n
        bb_idx = (self.dealer_index + 1) % n
        
        for i, p in enumerate(active_players):
            if i == sb_idx:
                p.is_sb = True
                p.is_dealer = True
            if i == bb_idx:
                p.is_bb = True
        
        # 发手牌
        for player in active_players:
            player.hole_cards = self.deck.draw(2)
        
        # 下盲注
        sb_player = active_players[sb_idx]
        bb_player = active_players[bb_idx]
        
        sb_amount = min(self.small_blind, sb_player.chips)
        sb_player.chips -= sb_amount
        sb_player.bet = sb_amount
        sb_player.total_bet = sb_amount
        self.pot += sb_amount
        
        bb_amount = min(self.big_blind, bb_player.chips)
        bb_player.chips -= bb_amount
        bb_player.bet = bb_amount
        bb_player.total_bet = bb_amount
        self.pot += bb_amount
        
        self.current_bet = bb_amount
        
        self._add_history(f"小盲 {sb_player.name}: {sb_amount}, 大盲 {bb_player.name}: {bb_amount}", "system")
        
        # MVP fix: preflop行动顺序——1v1中SB/BTN先行动（sb_idx），BB最后；
        # 多人(>=3)preflop从BB下家（UTG）开始行动
        n = len(active_players)
        if n == 2:
            # heads-up: SB/BTN先行动
            self.current_player_index = sb_idx
        else:
            # 多人: UTG = BB下一位
            self.current_player_index = (bb_idx + 1) % n
        self.last_raiser_index = bb_idx  # BB是最后加注者（大盲相当于强制加注）
        
        # BB如果已经all-in了，需要标记has_acted相关逻辑交给_check_round处理
        for p in self.players:
            p.has_acted = False
        # 盲注不自动算acted（SB/BB都还需要行动）
        
        self._add_history("新的一局开始", "system")
        # 旋转dealer到下一位（为下一手准备）
        self.dealer_index = (self.dealer_index + 1) % n
    
    def process_action(self, player_id: str, action_type: str, amount: int = 0) -> Dict:
        """处理玩家行动"""
        if self.hand_over:
            return {"success": False, "message": "本局已结束"}
        
        player = self._get_player(player_id)
        if not player:
            return {"success": False, "message": "玩家不存在"}
        
        # 验证是否轮到该玩家
        if self.players[self.current_player_index].id != player_id:
            return {"success": False, "message": "不是你的回合"}
        
        if player.folded or player.all_in:
            return {"success": False, "message": "玩家已弃牌或All-in"}
        
        result = {"success": True, "message": "", "action": action_type, "amount": 0}
        
        call_amount = self._get_call_amount(player)
        
        if action_type == "fold":
            player.folded = True
            player.has_acted = True
            result["message"] = f"{player.name} 弃牌"
            
        elif action_type == "check":
            if call_amount > 0:
                return {"success": False, "message": "无法过牌，需要跟注或加注"}
            player.has_acted = True
            result["message"] = f"{player.name} 过牌"
            
        elif action_type == "call":
            pay = min(call_amount, player.chips)
            player.chips -= pay
            player.bet += pay
            player.total_bet += pay
            self.pot += pay
            if player.chips == 0:
                player.all_in = True
            player.has_acted = True
            result["message"] = f"{player.name} 跟注 {pay}"
            result["amount"] = pay
            
        elif action_type == "raise":
            # MVP fix: 正确加注逻辑——先补足call_amount，剩余筹码才是可加注部分
            # amount 表示 raise 增量（超出 call 的部分）
            if amount < self.min_raise:
                amount = self.min_raise
            
            call_amount = self._get_call_amount(player)
            # 玩家最多能支付：先call，再加raise；若筹码不足，则all-in
            total_pay = call_amount + amount
            if total_pay > player.chips:
                # 筹码不足以"call + 完整min-raise"：
                # - 如果连call都不够 → 全部押入（相当于all-in跟注）
                # - 如果能call但加不足min-raise → 短all-in（不重开加注轮次）
                total_pay = player.chips
            
            player.chips -= total_pay
            player.bet += total_pay
            player.total_bet += total_pay
            self.pot += total_pay
            
            if player.chips == 0:
                player.all_in = True
            
            new_bet = player.bet
            raise_delta = new_bet - self.current_bet
            if raise_delta >= self.min_raise:
                # 合法加注
                self.min_raise = max(self.big_blind, raise_delta)
                self.current_bet = new_bet
                self.last_raiser_index = self.players.index(player)
                # 其他未弃牌未all-in玩家需要再次行动
                for p in self.players:
                    if not p.folded and not p.all_in and p.id != player.id:
                        p.has_acted = False
            elif raise_delta > 0:
                # 短 all-in：raise_delta < min_raise，只更新current_bet不重开加注
                self.current_bet = max(self.current_bet, new_bet)
            
            player.has_acted = True
            if player.all_in:
                result["message"] = f"{player.name} ALL IN {total_pay}（短加注）"
            else:
                result["message"] = f"{player.name} 加注到 {player.bet}（总付 {total_pay}）"
            result["amount"] = total_pay
            
        elif action_type == "allin":
            all_amount = player.chips
            player.chips = 0
            player.bet += all_amount
            player.total_bet += all_amount
            self.pot += all_amount
            player.all_in = True
            
            new_bet = player.bet
            raise_delta = new_bet - self.current_bet
            if raise_delta >= self.min_raise:
                # 合法加注
                self.min_raise = max(self.big_blind, raise_delta)
                self.current_bet = new_bet
                self.last_raiser_index = self.players.index(player)
                # 其他玩家需要重新行动
                for p in self.players:
                    if not p.folded and not p.all_in and p.id != player.id:
                        p.has_acted = False
            elif raise_delta > 0:
                # 小于min-raise的all-in（短all-in），此时call量上升但不重开加注回合
                self.current_bet = max(self.current_bet, new_bet)
            
            player.has_acted = True
            result["message"] = f"{player.name} ALL IN {all_amount}"
            result["amount"] = all_amount
            
        else:
            return {"success": False, "message": f"未知行动: {action_type}"}
        
        self._add_history(result["message"], "action")
        
        # 检查是否只剩一个活跃玩家（其他人都fold了）
        active_not_allin = [p for p in self.players if not p.folded and not p.all_in]
        active_not_folded = [p for p in self.players if not p.folded]
        if len(active_not_folded) == 1:
            self._award_pot(active_not_folded[0])
            return result
        
        # 推进到下一个需要行动的玩家
        self._advance_player()
        
        # 检查轮次是否结束
        self._check_round_complete()
        
        return result
    
    def _get_call_amount(self, player: Player) -> int:
        """计算跟注金额（需要补到current_bet）"""
        return max(0, self.current_bet - player.bet)
    
    def _advance_player(self):
        """推进到下一位需要行动的玩家"""
        n = len(self.players)
        next_idx = (self.current_player_index + 1) % n
        # 找下一个未fold未all-in的玩家
        for _ in range(n):
            p = self.players[next_idx]
            if not p.folded and not p.all_in:
                self.current_player_index = next_idx
                return
            next_idx = (next_idx + 1) % n
        # 没有可行动玩家（全部all-in或fold），保持当前位置
        self.current_player_index = next_idx
    
    def _active_players(self) -> List[Player]:
        """返回未弃牌且未all-in的玩家（还能行动的）"""
        return [p for p in self.players if not p.folded and not p.all_in]
    
    def _relevant_players(self) -> List[Player]:
        """返回未弃牌的玩家（包括all-in）"""
        return [p for p in self.players if not p.folded]
    
    def _check_round_complete(self):
        """检查当前轮是否结束"""
        if self.hand_over:
            return
        
        # MVP fix: 正确判断轮次结束——避免单人未行动时误触发摊牌
        # 能继续下注的玩家（未弃牌、未all-in）
        active = self._active_players()
        # 未弃牌的玩家（包括all-in）
        alive = self._relevant_players()
        
        if len(alive) == 1:
            # 其他玩家都弃牌
            self._award_pot(alive[0])
            return
        
        if len(active) == 0:
            # 所有未弃牌玩家都 all-in，直接发完公牌摊牌
            self._run_out_board()
            self._showdown()
            return
        
        # 所有可行动玩家都已行动，且下注额相等 → 进入下一阶段
        all_acted = all(p.has_acted for p in active)
        all_bets_equal = all(p.bet == self.current_bet for p in active)
        
        if all_acted and all_bets_equal:
            self._advance_stage()
    
    def _run_out_board(self):
        """把剩余公牌发完（当有人all-in时直接发完）"""
        cards_needed = {
            Stage.PREFLOP: 5,
            Stage.FLOP: 2,
            Stage.TURN: 1,
            Stage.RIVER: 0,
            Stage.SHOWDOWN: 0
        }[self.stage]
        if cards_needed > 0:
            self.board.extend(self.deck.draw(cards_needed))
            self._add_history(f"剩余公牌发完: {self._board_str()}", "system")
            self.stage = Stage.RIVER
    
    def _advance_stage(self):
        """进入下一阶段"""
        # 重置每轮下注
        for p in self.players:
            p.bet = 0
            p.has_acted = False
        self.current_bet = 0
        self.min_raise = self.big_blind
        self.last_raiser_index = None
        
        if self.stage == Stage.PREFLOP:
            self.board = self.deck.draw(3)
            self.stage = Stage.FLOP
            self._add_history(f"翻牌: {self._board_str()}", "system")
        elif self.stage == Stage.FLOP:
            self.board.extend(self.deck.draw(1))
            self.stage = Stage.TURN
            self._add_history(f"转牌: {self._board_str()}", "system")
        elif self.stage == Stage.TURN:
            self.board.extend(self.deck.draw(1))
            self.stage = Stage.RIVER
            self._add_history(f"河牌: {self._board_str()}", "system")
        elif self.stage == Stage.RIVER:
            self.stage = Stage.SHOWDOWN
            self._showdown()
            return
        
        # 决定新轮次谁先行动：翻牌后从BB（最靠近BB左边的活跃玩家/小盲/BTN之后）开始
        # 简化为：从SB/BTN之后的第一个未弃牌玩家开始（1v1中preflop之后是BB先行动，BB是idx=1在1v1里）
        # 标准规则：flop/turn/river 从SB位置开始（1v1中BTN=SB，故BTN先行动；但实际1v1 flop后是BB先check，哦等等）
        # 更正 1v1 翻牌后顺序：BB先行动（out of position），BTN最后
        # 找到第一个非fold非all-in玩家，从最靠近BB左边开始
        # 简单起见：从SB开始（1v1即player[0]）；preflop之后1v1 flop顺序：BB先行动
        # 统一规则：从dealer/SB之后位置即BB开始行动 flop之后（1v1正确）
        # 实际上标准heads-up：post-flop BB先行动
        # 找BB位或其之后第一个活跃玩家
        bb_idx = 0
        for i, p in enumerate(self.players):
            if p.is_bb:
                bb_idx = i
                break
        
        # 从BB位开始找活跃玩家
        n = len(self.players)
        for offset in range(n):
            idx = (bb_idx + offset) % n
            p = self.players[idx]
            if not p.folded and not p.all_in:
                self.current_player_index = idx
                break
        
        # 活跃玩家只剩1人？
        active = self._active_players()
        if len(active) == 1:
            # 全all-in，发完牌比大小
            self._run_out_board()
            self._showdown()
    
    def _showdown(self):
        """摊牌"""
        self.stage = Stage.SHOWDOWN
        contenders = [p for p in self.players if not p.folded]
        
        if len(contenders) == 1:
            self._award_pot(contenders[0])
            return
        
        # 评估所有玩家最佳手牌
        best_rank = -1
        best_tie = []
        winners = []
        for player in contenders:
            all_cards = player.hole_cards + self.board
            if len(all_cards) < 5:
                continue
            evaluation = HandEvaluator.evaluate(all_cards)
            player._last_eval = evaluation
            r, t = evaluation["rank"], evaluation["tie_breakers"]
            if r > best_rank or (r == best_rank and t > best_tie):
                best_rank = r
                best_tie = t
                winners = [player]
            elif r == best_rank and t == best_tie:
                winners.append(player)
        
        if not winners:
            winners = contenders[:1]
        
        # 分池（简化：均分底池；不处理边池，边池是P2优化）
        share = self.pot // len(winners)
        remainder = self.pot % len(winners)
        for i, w in enumerate(winners):
            w.chips += share + (1 if i < remainder else 0)
        
        self.winner = winners[0]
        self.winners = winners
        self.hand_over = True
        winner_names = ", ".join(w.name for w in winners)
        hand_name = getattr(winners[0], '_last_eval', {}).get('hand_name', '?')
        self._add_history(f"{winner_names} 赢了 {self.pot} 筹码! ({hand_name})", "winner")
        self.pot = 0
    
    def _award_pot(self, winner: Player):
        """分配底池（无对手）"""
        winner.chips += self.pot
        self.winner = winner
        self.winners = [winner]
        self.hand_over = True
        self.stage = Stage.SHOWDOWN
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
            "winners": [w.to_dict() for w in self.winners] if self.winners else None,
            "current_player": self.current_player_index,
            "current_bet": self.current_bet,
            "min_raise": self.min_raise,
            "last_raise": self.current_bet,
            "big_blind": self.big_blind,
            "small_blind": self.small_blind,
            "history": self.history[-10:]
        }
    
    def get_ai_player(self) -> Optional[Player]:
        """获取当前应该行动的AI玩家（非当前玩家的下一位AI）"""
        # 如果当前玩家是AI，返回当前玩家
        current = self.players[self.current_player_index]
        if current.is_ai and not current.folded and not current.all_in:
            return current
        # 否则找下一个AI（兼容逻辑）
        for p in self.players:
            if p.is_ai and not p.folded and not p.all_in:
                return p
        return None
    
    def get_ai_opponent(self, player_id: str) -> Optional[Player]:
        """获取指定玩家的AI对手（用于1v1）"""
        for p in self.players:
            if p.is_ai and p.id != player_id and not p.folded:
                return p
        return None
    
    def is_ai_turn(self) -> bool:
        """是否轮到AI"""
        if self.hand_over:
            return False
        if self.current_player_index >= len(self.players):
            return False
        current_player = self.players[self.current_player_index]
        return current_player.is_ai and not current_player.folded and not current_player.all_in
