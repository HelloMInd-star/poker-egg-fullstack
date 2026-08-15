"""
MBTI 人格决策引擎
==================
把 personalities.py 的 8 维行为参数真正接入 AI 决策（此前为死数据）。

决策管道：
1. 客观基准层：牌力评估 + 蒙特卡洛胜率 + 底池赔率
2. 人格滤镜层：foldRate / aggressionLevel / bluffFrequency / allinRate /
   potControl / tiltResistance / noiseResistance 逐维调制决策倾向
3. 可解释输出：每次决策附带人格化理由（reason），前端可展示

设计哲学：同一手牌，不同人格必须打出可感知差异。
ISTJ 边缘牌全弃几乎不诈唬；ESTP 高频施压常诈唬敢全下。
"""
import random
from typing import Dict, List, Optional

from .personalities import MBTI_PERSONALITIES
from .analysis import evaluate_hand_strength, monte_carlo_win_rate


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(x, hi))


class PersonalityAI:
    """MBTI 人格 AI：客观牌力 × 人格滤镜 → 决策 + 人格化理由"""

    def __init__(self, mbti: str):
        self.mbti = (mbti or "").upper()
        self.p = MBTI_PERSONALITIES.get(self.mbti)
        if not self.p:
            raise ValueError(f"未知人格类型: {mbti}")
        self._initial_chips: Optional[int] = None

    # ---------- 人格滤镜 ----------

    def _tilt_factor(self, my_chips: int, starting_chips: int = 1000) -> float:
        """连输/亏损后的情绪漂移系数。tiltResistance 越低，亏损时越容易失控（变松、注额变大）。"""
        if self._initial_chips is None:
            self._initial_chips = max(my_chips, starting_chips)
        base = max(self._initial_chips, starting_chips)
        if base <= 0:
            return 0.0
        loss_ratio = _clamp((base - my_chips) / base, 0.0, 1.0)
        return loss_ratio * (1.0 - self.p["tiltResistance"])

    def _facing_pressure_fold_boost(self, call_amount: int, pot: int) -> float:
        """面对大额跟注压力时，低抗噪人格弃牌阈值上调（被吓退）。"""
        if pot <= 0 or call_amount <= 0:
            return 0.0
        pressure = _clamp(call_amount / max(pot, 1), 0.0, 1.0)  # 相对底池的跟注压力
        return pressure * (1.0 - self.p["noiseResistance"]) * 0.25

    # ---------- 主决策 ----------

    def decide_action(self, game_state: Dict) -> Dict:
        hole = game_state.get("hole_cards", [])
        board = game_state.get("board_cards", [])
        pot = game_state.get("pot", 0)
        my_chips = game_state.get("my_chips", 1000)
        call_amount = max(game_state.get("call_amount", 0), 0)
        stage = game_state.get("stage", "preflop")

        if call_amount > my_chips:
            call_amount = my_chips

        # ===== 1. 客观基准层 =====
        strength = evaluate_hand_strength(hole, board)
        # 蒙特卡洛真胜率（AI 内部判断用，比静态强度更接近真实胜率）
        win_rate = monte_carlo_win_rate(hole, board, simulations=300)
        pot_total = pot + call_amount
        pot_odds = call_amount / pot_total if pot_total > 0 else 0.0

        # ===== 2. 人格滤镜层 =====
        p = self.p
        tilt = self._tilt_factor(my_chips)
        # tilt 让人变松、变凶（失控）
        eff_aggression = _clamp(p["aggressionLevel"] + tilt * 0.35)
        eff_bluff = _clamp(p["bluffFrequency"] + tilt * 0.25)
        # 弃牌阈值：foldRate 基准 + 大注压力加成（低抗噪被吓退）- tilt 上头不肯走
        fold_threshold = _clamp(
            p["foldRate"] + self._facing_pressure_fold_boost(call_amount, pot) - tilt * 0.30
        )
        # 注额尺度：攻击性定大小，控池强的人格压低注额
        sizing = 0.30 + eff_aggression * 0.50          # 0.30 ~ 0.80 pot
        sizing *= (1.0 - p["potControl"] * 0.45)        # 高控池压注额
        sizing = _clamp(sizing, 0.20, 0.85)

        # ===== 3. 决策树（人格化阈值） =====
        can_check = call_amount == 0
        strong_line = 0.78 - eff_aggression * 0.10      # 凶者对"强牌"门槛更低
        mid_line = 0.42 - (1 - fold_threshold) * 0.12   # 松者中线更低，愿玩更多边缘牌

        action = "fold"
        amount = 0
        reason = ""

        if win_rate >= strong_line:
            # —— 强牌：加注/全下 ——
            if random.random() < p["allinRate"] * 3.5 and my_chips > pot_total:
                action, amount = "allin", 0
                reason = self._reason("allin_strong", win_rate)
            elif random.random() < 0.35 + eff_aggression * 0.55:
                action = "raise"
                amount = self._raise_size(pot, call_amount, my_chips, sizing)
                reason = self._reason("raise_strong", win_rate)
            else:
                action = "call" if not can_check else "check"
                reason = self._reason("slowplay", win_rate)

        elif win_rate >= mid_line:
            # —— 中牌：数学+性格博弈 ——
            ev_positive = win_rate > pot_odds  # 胜率覆盖赔率才值得继续
            if not ev_positive and random.random() < fold_threshold:
                action = "fold" if not can_check else "check"
                reason = self._reason("fold_math", win_rate, pot_odds)
            elif random.random() < eff_aggression * 0.45 and my_chips > call_amount + 40:
                action = "raise"
                amount = self._raise_size(pot, call_amount, my_chips, sizing * 0.8)
                reason = self._reason("raise_mid", win_rate)
            else:
                action = "call" if not can_check else "check"
                reason = self._reason("call_mid", win_rate, pot_odds)

        else:
            # —— 弱牌：诈唬或放弃 ——
            stage_bluff_decay = {"preflop": 1.0, "flop": 0.85, "turn": 0.65, "river": 0.45}.get(stage, 0.6)
            bluff_chance = eff_bluff * stage_bluff_decay
            if random.random() < bluff_chance and my_chips > call_amount + 40 and not can_check:
                if random.random() < p["allinRate"] * 2:
                    action, amount = "allin", 0
                    reason = self._reason("allin_bluff", win_rate)
                else:
                    action = "raise"
                    amount = self._raise_size(pot, call_amount, my_chips, sizing)
                    reason = self._reason("bluff", win_rate)
            elif can_check:
                action = "check"
                reason = self._reason("check_weak", win_rate)
            else:
                action = "fold"
                reason = self._reason("fold_weak", win_rate, pot_odds)

        return {
            "action": action,
            "amount": int(amount),
            "reason": reason,
            "debug": {
                "mbti": self.mbti,
                "win_rate": round(win_rate, 3),
                "pot_odds": round(pot_odds, 3),
                "tilt": round(tilt, 3),
            },
        }

    # ---------- 注额计算 ----------

    def _raise_size(self, pot: int, call_amount: int, my_chips: int, sizing: float) -> int:
        bet = call_amount + max(20, int(pot * sizing))
        return int(min(bet, my_chips))

    # ---------- 人格化理由 ----------

    def _reason(self, kind: str, win_rate: float, pot_odds: float = 0.0) -> str:
        wr = f"{win_rate*100:.0f}%"
        po = f"{pot_odds*100:.0f}%"
        group = self.p["group"]
        # 按气质组定语气，让 16 人格的"可解释性"有群体辨识度
        if kind == "allin_strong":
            return {"SP": f"机会来了，全下！来啊！", "NT": f"胜率 {wr}，全下是最大化EV",
                    "NF": f"直觉告诉我就是现在，全下", "SJ": f"牌面足够扎实，全下收池"}[group]
        if kind == "allin_bluff":
            return {"SP": f"赌一把！全下诈唬，敢跟吗？", "NT": f"计算过弃牌率，全下施压",
                    "NF": f"心跳加速……全下！", "SJ": f"非常规动作：全下施压"}[group]
        if kind == "raise_strong":
            return {"SP": f"胜率 {wr}，加注收下这个池", "NT": f"胜率 {wr}，加注是 +EV 的",
                    "NF": f"感觉牌在我这边，加注", "SJ": f"胜率 {wr}，按纪律加注"}[group]
        if kind == "slowplay":
            return {"SP": f"好牌不急着亮，先蹲一手", "NT": f"胜率 {wr}，慢打诱捕",
                    "NF": f"静观其变……", "SJ": f"稳健跟注，控池观察"}[group]
        if kind == "raise_mid":
            return {"SP": f"边缘牌也要施压，加注！", "NT": f"半诈唬，加注试探你的牌力",
                    "NF": f"试试水，加注", "SJ": f"适度加注，控制节奏"}[group]
        if kind == "call_mid":
            return {"SP": f"跟注看看下一张", "NT": f"胜率 {wr} 覆盖赔率 {po}，跟注合理",
                    "NF": f"再信一次感觉，跟", "SJ": f"赔率 {po} 尚可，谨慎跟注"}[group]
        if kind == "fold_math":
            return {"SP": f"赔率不对，这手不玩了", "NT": f"胜率 {wr} 低于赔率 {po}，弃牌是数学",
                    "NF": f"心里没底，弃了", "SJ": f"胜率 {wr} 不达标，按纪律弃牌"}[group]
        if kind == "bluff":
            return {"SP": f"什么都没有？那就诈唬！加注", "NT": f"你的下注模式有破绽，加注诈唬",
                    "NF": f"虚张声势一下～加注", "SJ": f"罕见地激进一次，加注"}[group]
        if kind == "check_weak":
            return {"SP": f"先过牌，等你露破绽", "NT": f"无投入必要，过牌",
                    "NF": f"过牌看看风向", "SJ": f"过牌，不冒无谓风险"}[group]
        # fold_weak
        return {"SP": f"牌太烂，撤了撤了", "NT": f"胜率 {wr}，弃牌止损",
                "NF": f"这局不属于我，弃牌", "SJ": f"牌力不足，弃牌"}[group]


class PersonalityAIManager:
    """按人格缓存 AI 实例（每局一个实例，保留 tilt 记忆）"""

    def __init__(self):
        self._instances: Dict[str, PersonalityAI] = {}

    def get(self, game_id: str, mbti: str) -> PersonalityAI:
        key = f"{game_id}:{mbti.upper()}"
        if key not in self._instances:
            self._instances[key] = PersonalityAI(mbti)
        return self._instances[key]

    def reset(self, game_id: str):
        """牌局结束后清空该局的 tilt 记忆"""
        for k in [k for k in self._instances if k.startswith(f"{game_id}:")]:
            del self._instances[k]


personality_ai_manager = PersonalityAIManager()
