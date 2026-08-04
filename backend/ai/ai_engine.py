"""
AI陪练引擎
支持3个难度级别：easy, medium, hard
"""
import random
import numpy as np
from typing import Dict, List, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.game_engine import Card, HandEvaluator


class PokerAI:
    """扑克AI"""
    
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.hand_strength = 0.0
        self.aggression = 0.3
        self.bluff_frequency = 0.1
        self._init_difficulty_params()
    
    def _init_difficulty_params(self):
        """根据难度初始化参数"""
        if self.difficulty == "easy":
            self.aggression = 0.1
            self.bluff_frequency = 0.05
            self.thinking_time = 0.5
        elif self.difficulty == "medium":
            self.aggression = 0.3
            self.bluff_frequency = 0.15
            self.thinking_time = 1.0
        else:  # hard
            self.aggression = 0.5
            self.bluff_frequency = 0.25
            self.thinking_time = 1.5
    
    def decide_action(self, game_state: Dict) -> Dict:
        """
        做出决策
        返回: {"action": str, "amount": int}
        """
        hole_cards = game_state.get("hole_cards", [])
        board_cards = game_state.get("board_cards", [])
        pot = game_state.get("pot", 0)
        my_chips = game_state.get("my_chips", 1000)
        current_bet = game_state.get("current_bet", 0)
        position = game_state.get("position", "middle")
        stage = game_state.get("stage", "preflop")
        
        # 评估手牌
        all_cards = hole_cards + board_cards
        evaluation = HandEvaluator.evaluate(all_cards) if len(all_cards) >= 5 else {
            "strength": 0.2 + (len(hole_cards) > 0) * 0.1
        }
        self.hand_strength = evaluation["strength"]
        
        # 根据难度决策
        if self.difficulty == "easy":
            return self._easy_decision(pot, current_bet, my_chips)
        elif self.difficulty == "medium":
            return self._medium_decision(pot, current_bet, my_chips, stage)
        else:
            return self._hard_decision(pot, current_bet, my_chips, stage)
    
    def _easy_decision(self, pot: int, current_bet: int, my_chips: int) -> Dict:
        """简单AI：主要看手牌强度"""
        rand = random.random()
        
        # 手牌强 -> 加注
        if self.hand_strength > 0.7 and rand > 0.3:
            raise_amount = min(int(pot * 0.3) + 20, my_chips)
            return {"action": "raise", "amount": max(20, raise_amount)}
        
        # 手牌中等 -> 跟注
        elif self.hand_strength > 0.4 and rand > 0.5:
            return {"action": "call"}
        
        # 手牌弱 -> 弃牌或诈唬
        else:
            if rand < self.bluff_frequency and my_chips > 100:
                return {"action": "raise", "amount": min(20, my_chips)}
            return {"action": "fold"}
    
    def _medium_decision(self, pot: int, current_bet: int, my_chips: int, stage: str) -> Dict:
        """中级AI：考虑赔率和期望值"""
        # 计算底池赔率
        pot_odds = current_bet / (pot + current_bet) if pot + current_bet > 0 else 0
        
        # 计算期望值
        expected_value = (self.hand_strength * (pot + current_bet)) - (1 - self.hand_strength) * current_bet
        
        # 阶段调整
        stage_multiplier = {
            "preflop": 0.8,
            "flop": 1.0,
            "turn": 1.2,
            "river": 1.4
        }.get(stage, 1.0)
        
        adjusted_strength = self.hand_strength * stage_multiplier
        
        # 决策
        if adjusted_strength > 0.6 and expected_value > 20:
            raise_amount = min(
                int(pot * (0.3 + adjusted_strength * 0.3)),
                my_chips
            )
            return {"action": "raise", "amount": max(20, raise_amount)}
        
        elif pot_odds < adjusted_strength and adjusted_strength > 0.3:
            return {"action": "call"}
        
        elif adjusted_strength < 0.25:
            if random.random() < self.bluff_frequency * 0.5:
                return {"action": "raise", "amount": min(20, my_chips)}
            return {"action": "fold"}
        
        else:
            return {"action": "check" if current_bet == 0 else "call"}
    
    def _hard_decision(self, pot: int, current_bet: int, my_chips: int, stage: str) -> Dict:
        """高级AI：使用凯利公式 + 策略混合"""
        # 计算凯利指数
        kelly = self._calculate_kelly(pot, current_bet)
        
        # 计算诈唬概率
        bluff_prob = self._calculate_bluff_probability(stage)
        
        # 对手建模（简化）
        opponent_aggression = 0.3
        
        # 综合决策
        if self.hand_strength > 0.7 and kelly > 0.15:
            # 强牌 + 高凯利 -> 加注
            raise_amount = min(
                int(pot * (0.2 + kelly * 0.5)),
                my_chips
            )
            return {"action": "raise", "amount": max(20, raise_amount)}
        
        elif self.hand_strength > 0.4 and kelly > 0:
            # 中等牌 + 正凯利 -> 跟注
            return {"action": "call"}
        
        elif self.hand_strength < 0.3 and bluff_prob > 0.2:
            # 弱牌但诈唬概率高 -> 诈唬
            if random.random() < 0.3:
                return {"action": "raise", "amount": min(int(pot * 0.5), my_chips)}
            return {"action": "fold"}
        
        elif opponent_aggression > 0.6 and self.hand_strength > 0.35:
            # 对手激进，中等牌也跟注
            return {"action": "call"}
        
        else:
            return {"action": "check" if current_bet == 0 else "fold"}
    
    def _calculate_kelly(self, pot: int, current_bet: int) -> float:
        """计算凯利指数"""
        if current_bet == 0:
            return 0.1
        
        win_rate = min(self.hand_strength + 0.1, 0.95)
        odds = pot / current_bet
        
        kelly = (win_rate * odds - (1 - win_rate)) / odds
        return max(0, min(kelly, 0.5))
    
    def _calculate_bluff_probability(self, stage: str) -> float:
        """计算诈唬概率"""
        base_bluff = self.bluff_frequency
        
        # 后期阶段诈唬概率降低
        stage_factor = {
            "preflop": 1.0,
            "flop": 0.8,
            "turn": 0.6,
            "river": 0.4
        }.get(stage, 0.5)
        
        # 手牌越弱，诈唬概率越高
        weakness_factor = 1 - self.hand_strength
        
        return min(base_bluff * stage_factor * (1 + weakness_factor), 0.5)
    
    def get_hand_description(self) -> str:
        """获取手牌描述"""
        strength = self.hand_strength
        if strength > 0.8:
            return "非常强"
        elif strength > 0.6:
            return "强"
        elif strength > 0.4:
            return "中等"
        elif strength > 0.2:
            return "弱"
        else:
            return "非常弱"


class AIDecisionMaker:
    """AI决策者 - 管理多个AI实例"""
    
    def __init__(self):
        self.ai_instances = {}
    
    def get_ai(self, difficulty: str = "medium") -> PokerAI:
        """获取或创建AI实例"""
        key = difficulty
        if key not in self.ai_instances:
            self.ai_instances[key] = PokerAI(difficulty)
        return self.ai_instances[key]
    
    def train_from_history(self, histories: List[Dict]):
        """从历史数据训练（未来扩展）"""
        # 这里可以实现强化学习训练
        pass
