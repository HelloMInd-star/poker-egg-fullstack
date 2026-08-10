"""
AI陪练引擎
支持3个难度级别：easy, medium, hard
修复版：正确处理dict格式的卡牌
"""
import random
from typing import Dict, List, Optional
import os
import sys
# 允许从backend根目录运行时导入services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.game_engine import HandEvaluator, Card


def _dict_to_card(d: Dict) -> Card:
    """把dict格式的卡牌转成Card对象"""
    return Card(rank=d.get("rank", "2"), suit=d.get("suit", "♠"))


class PokerAI:
    """扑克AI"""
    
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.hand_strength = 0.0
        self.aggression = 0.3
        self.bluff_frequency = 0.1
        self._init_difficulty_params()
    
    def _init_difficulty_params(self):
        if self.difficulty == "easy":
            self.aggression = 0.1
            self.bluff_frequency = 0.05
            self.thinking_time = 0.5
        elif self.difficulty == "medium":
            self.aggression = 0.3
            self.bluff_frequency = 0.15
            self.thinking_time = 1.0
        else:
            self.aggression = 0.5
            self.bluff_frequency = 0.25
            self.thinking_time = 1.5
    
    def decide_action(self, game_state: Dict) -> Dict:
        hole_dicts = game_state.get("hole_cards", [])
        board_dicts = game_state.get("board_cards", [])
        pot = game_state.get("pot", 0)
        my_chips = game_state.get("my_chips", 1000)
        current_bet = game_state.get("current_bet", 0)
        call_amount = game_state.get("call_amount", current_bet)
        stage = game_state.get("stage", "preflop")
        
        # 转为Card对象进行评估
        hole_cards = [_dict_to_card(c) for c in hole_dicts]
        board_cards = [_dict_to_card(c) for c in board_dicts]
        all_cards = hole_cards + board_cards
        
        if len(all_cards) >= 5:
            evaluation = HandEvaluator.evaluate(all_cards)
            self.hand_strength = evaluation["strength"]
        else:
            # 不足5张：基于起手牌粗略估计
            self.hand_strength = self._preflop_strength(hole_cards)
        
        if self.difficulty == "easy":
            return self._easy_decision(pot, call_amount, current_bet, my_chips)
        elif self.difficulty == "medium":
            return self._medium_decision(pot, call_amount, current_bet, my_chips, stage)
        else:
            return self._hard_decision(pot, call_amount, current_bet, my_chips, stage)
    
    def _preflop_strength(self, hole_cards: List[Card]) -> float:
        """翻牌前手牌强度粗略估计（基于对子/高牌/同花连张）"""
        if len(hole_cards) < 2:
            return 0.2
        c1, c2 = hole_cards[0], hole_cards[1]
        v1, v2 = c1.rank_value, c2.rank_value
        high, low = max(v1, v2), min(v1, v2)
        suited = c1.suit == c2.suit
        pair = v1 == v2
        gap = high - low
        
        if pair:
            # 对子：22=0.5, AA=0.85
            return 0.5 + (high - 2) / 12 * 0.35
        # 高牌估计
        base = (high - 2) / 12 * 0.3 + (low - 2) / 12 * 0.15
        if gap == 1:
            base += 0.08  # 连张
        elif gap == 0:
            pass
        elif gap <= 3:
            base += 0.04
        if suited:
            base += 0.08
        # AX 加成
        if high == 14:
            base += 0.05
        return min(max(base, 0.2), 0.8)
    
    def _easy_decision(self, pot, call_amount, current_bet, my_chips):
        rand = random.random()
        if call_amount > my_chips:
            call_amount = my_chips
        
        if self.hand_strength > 0.7 and rand > 0.3:
            raise_total = min(call_amount + max(20, int(pot * 0.5)), my_chips)
            return {"action": "raise", "amount": raise_total}
        elif self.hand_strength > 0.4 and rand > 0.4:
            return {"action": "call" if call_amount > 0 else "check"}
        else:
            if rand < self.bluff_frequency and my_chips > call_amount + 40:
                return {"action": "raise", "amount": min(call_amount + 20, my_chips)}
            return {"action": "fold" if call_amount > 0 else "check"}
    
    def _medium_decision(self, pot, call_amount, current_bet, my_chips, stage):
        pot_total = pot + call_amount
        pot_odds = call_amount / pot_total if pot_total > 0 else 0
        expected_value = (self.hand_strength * (pot + call_amount)) - (1 - self.hand_strength) * call_amount
        
        stage_multiplier = {"preflop": 0.8, "flop": 1.0, "turn": 1.2, "river": 1.4}.get(stage, 1.0)
        adjusted_strength = self.hand_strength * stage_multiplier
        
        if adjusted_strength > 0.6 and expected_value > 20 and my_chips > call_amount:
            raise_total = min(call_amount + max(20, int(pot * (0.3 + adjusted_strength * 0.3))), my_chips)
            return {"action": "raise", "amount": raise_total}
        elif pot_odds < adjusted_strength and adjusted_strength > 0.3 and call_amount <= my_chips:
            return {"action": "call" if call_amount > 0 else "check"}
        elif adjusted_strength < 0.25:
            if random.random() < self.bluff_frequency * 0.5 and my_chips > call_amount + 40:
                return {"action": "raise", "amount": min(call_amount + 20, my_chips)}
            return {"action": "fold" if call_amount > 0 else "check"}
        else:
            return {"action": "call" if call_amount > 0 else "check"}
    
    def _hard_decision(self, pot, call_amount, current_bet, my_chips, stage):
        kelly = self._calculate_kelly(pot, call_amount)
        bluff_prob = self._calculate_bluff_probability(stage)
        opponent_aggression = 0.3
        
        if self.hand_strength > 0.7 and kelly > 0.15 and my_chips > call_amount:
            raise_total = min(call_amount + max(20, int(pot * (0.2 + kelly * 0.5))), my_chips)
            return {"action": "raise", "amount": raise_total}
        elif self.hand_strength > 0.4 and kelly >= 0 and call_amount <= my_chips:
            return {"action": "call" if call_amount > 0 else "check"}
        elif self.hand_strength < 0.3 and bluff_prob > 0.2 and my_chips > call_amount + 40:
            if random.random() < 0.3:
                return {"action": "raise", "amount": min(call_amount + int(pot * 0.5), my_chips)}
            return {"action": "fold" if call_amount > 0 else "check"}
        elif opponent_aggression > 0.6 and self.hand_strength > 0.35 and call_amount <= my_chips:
            return {"action": "call" if call_amount > 0 else "check"}
        else:
            return {"action": "call" if call_amount > 0 and call_amount <= my_chips else ("check" if call_amount == 0 else "fold")}
    
    def _calculate_kelly(self, pot, call_amount):
        if call_amount == 0:
            return 0.1
        win_rate = min(self.hand_strength + 0.1, 0.95)
        odds = pot / call_amount if call_amount > 0 else 1
        kelly = (win_rate * odds - (1 - win_rate)) / odds
        return max(0, min(kelly, 0.5))
    
    def _calculate_bluff_probability(self, stage):
        base_bluff = self.bluff_frequency
        stage_factor = {"preflop": 1.0, "flop": 0.8, "turn": 0.6, "river": 0.4}.get(stage, 0.5)
        weakness_factor = 1 - self.hand_strength
        return min(base_bluff * stage_factor * (1 + weakness_factor), 0.5)
    
    def get_hand_description(self) -> str:
        s = self.hand_strength
        if s > 0.8: return "非常强"
        if s > 0.6: return "强"
        if s > 0.4: return "中等"
        if s > 0.2: return "弱"
        return "非常弱"


class AIDecisionMaker:
    """AI决策者 - 管理多个AI实例"""
    
    def __init__(self):
        self.ai_instances = {}
    
    def get_ai(self, difficulty: str = "medium") -> PokerAI:
        key = difficulty
        if key not in self.ai_instances:
            self.ai_instances[key] = PokerAI(difficulty)
        return self.ai_instances[key]
    
    def train_from_history(self, histories: List[Dict]):
        pass
