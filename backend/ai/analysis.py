"""
实时牌局分析引擎
================
为 Kelly 决策面板提供数据：真胜率（蒙特卡洛）+ 底池赔率 + Kelly 注额 + 牌型识别。

与竞品的本质差异：胜率不是翻牌前查表死数字，
而是基于当前手牌+公共牌的蒙特卡洛实时模拟，每张公共牌落地重新计算。
"""
import random
from typing import Dict, List

from services.game_engine import HandEvaluator, Card


RANKS = "23456789TJQKA"
SUITS = ["♠", "♥", "♦", "♣"]


def _dict_to_card(d: Dict) -> Card:
    return Card(rank=d.get("rank", "2"), suit=d.get("suit", "♠"))


def _full_deck() -> List[Card]:
    return [Card(rank=r, suit=s) for r in RANKS for s in SUITS]


def evaluate_hand_strength(hole_dicts: List[Dict], board_dicts: List[Dict]) -> float:
    """牌力 0-1：≥5 张用 HandEvaluator，翻牌前用起手牌估算（与 ai_engine 同口径）。"""
    hole = [_dict_to_card(c) for c in hole_dicts]
    board = [_dict_to_card(c) for c in board_dicts]
    all_cards = hole + board
    if len(all_cards) >= 5:
        return HandEvaluator.evaluate(all_cards)["strength"]
    return _preflop_strength(hole)


def _preflop_strength(hole: List[Card]) -> float:
    """翻牌前手牌强度估算（对子/高牌/同花连张），与 ai_engine._preflop_strength 同逻辑。"""
    if len(hole) < 2:
        return 0.2
    c1, c2 = hole[0], hole[1]
    v1, v2 = c1.rank_value, c2.rank_value
    high, low = max(v1, v2), min(v1, v2)
    suited = c1.suit == c2.suit
    if v1 == v2:
        return 0.5 + (high - 2) / 12 * 0.35
    gap = high - low
    base = (high - 2) / 12 * 0.3 + (low - 2) / 12 * 0.15
    if gap == 1:
        base += 0.08
    elif gap <= 3:
        base += 0.04
    if suited:
        base += 0.08
    if high == 14:
        base += 0.05
    return min(max(base, 0.2), 0.8)


def monte_carlo_win_rate(hole_dicts: List[Dict], board_dicts: List[Dict],
                         simulations: int = 400, num_opponents: int = 1) -> float:
    """
    蒙特卡洛真胜率：已知自己底牌+公共牌，随机补全对手底牌与剩余公共牌，
    模拟 N 次摊牌统计胜率。随每张公共牌落地实时变化。
    """
    hole = [_dict_to_card(c) for c in hole_dicts]
    board = [_dict_to_card(c) for c in board_dicts]
    if len(hole) < 2:
        return 0.0

    known = {(c.rank, c.suit) for c in hole + board}
    deck = [c for c in _full_deck() if (c.rank, c.suit) not in known]
    need_board = 5 - len(board)

    wins = 0.0
    sims = max(simulations, 50)
    for _ in range(sims):
        random.shuffle(deck)
        idx = 0
        # 随机发对手底牌
        opp_hole = deck[idx:idx + 2 * num_opponents]
        idx += 2 * num_opponents
        # 补全公共牌
        runout = board + deck[idx:idx + need_board]

        my_eval = HandEvaluator.evaluate(hole + runout)
        my_rank = my_eval.get("rank", 0)
        my_tb = my_eval.get("tie_breakers", [])

        beaten = False
        tied = False
        for o in range(num_opponents):
            oh = opp_hole[o * 2:o * 2 + 2]
            opp_eval = HandEvaluator.evaluate(oh + runout)
            opp_rank = opp_eval.get("rank", 0)
            opp_tb = opp_eval.get("tie_breakers", [])
            if opp_rank > my_rank or (opp_rank == my_rank and opp_tb > my_tb):
                beaten = True
                break
            if opp_rank == my_rank and opp_tb == my_tb:
                tied = True
        if not beaten:
            wins += 0.5 if tied else 1.0

    return wins / sims


def current_hand_name(hole_dicts: List[Dict], board_dicts: List[Dict]) -> str:
    """当前牌型名。≥5 张用评估器；翻牌前给起手牌描述（对子/同花/高牌）。"""
    hole = [_dict_to_card(c) for c in hole_dicts]
    board = [_dict_to_card(c) for c in board_dicts]
    all_cards = hole + board
    if len(all_cards) >= 5:
        return HandEvaluator.evaluate(all_cards).get("hand_name", "未知")
    if len(hole) == 2:
        v1, v2 = hole[0].rank_value, hole[1].rank_value
        suited = hole[0].suit == hole[1].suit
        if v1 == v2:
            return f"口袋对子 {hole[0].rank}{hole[0].rank}"
        label = "同花" if suited else "杂色"
        hi = hole[0].rank if v1 >= v2 else hole[1].rank
        lo = hole[1].rank if v1 >= v2 else hole[0].rank
        return f"{label} {hi}{lo}"
    return "等待发牌"


def kelly_analysis(hole_dicts: List[Dict], board_dicts: List[Dict],
                   pot: int, call_amount: int, my_chips: int) -> Dict:
    """
    Kelly 决策面板完整数据。
    f* = (b·p − q) / b，其中 p=胜率，q=1−p，b=净赔率（pot/call）。
    """
    win_rate = monte_carlo_win_rate(hole_dicts, board_dicts, simulations=400)
    hand_name = current_hand_name(hole_dicts, board_dicts)
    strength = evaluate_hand_strength(hole_dicts, board_dicts)

    pot_total = pot + call_amount
    pot_odds = call_amount / pot_total if pot_total > 0 else 0.0

    # Kelly：b = 赢时净赚/投入 = pot / call
    if call_amount > 0:
        b = pot / call_amount
        p, q = win_rate, 1 - win_rate
        kelly_f = (b * p - q) / b if b > 0 else 0.0
    else:
        # 无需跟注时：胜率即底气，给出进攻性建议比例
        kelly_f = max(0.0, (win_rate - 0.5)) * 1.2
    kelly_f = max(0.0, min(kelly_f, 0.5))  # 封顶 50% 筹码，防极端
    kelly_amount = int(my_chips * kelly_f)

    # 综合建议
    if call_amount > 0:
        if win_rate >= pot_odds + 0.10:
            suggestion = "raise"
            suggestion_text = f"胜率 {win_rate*100:.0f}% 明显覆盖赔率 {pot_odds*100:.0f}%，价值加注"
        elif win_rate >= pot_odds:
            suggestion = "call"
            suggestion_text = f"胜率 {win_rate*100:.0f}% 勉强覆盖赔率 {pot_odds*100:.0f}%，跟注合理"
        else:
            suggestion = "fold"
            suggestion_text = f"胜率 {win_rate*100:.0f}% 低于赔率 {pot_odds*100:.0f}%，长期跟注是 -EV"
    else:
        if win_rate >= 0.65:
            suggestion = "raise"
            suggestion_text = f"胜率 {win_rate*100:.0f}%，主动造池收价值"
        elif win_rate >= 0.45:
            suggestion = "check"
            suggestion_text = f"胜率 {win_rate*100:.0f}%，过牌控池观察"
        else:
            suggestion = "check"
            suggestion_text = f"胜率 {win_rate*100:.0f}%，免费看牌即可"

    return {
        "hand_name": hand_name,
        "strength": round(strength, 3),
        "win_rate": round(win_rate, 3),
        "pot_odds": round(pot_odds, 3),
        "kelly_fraction": round(kelly_f, 3),
        "kelly_amount": kelly_amount,
        "suggestion": suggestion,
        "suggestion_text": suggestion_text,
        "pot": pot,
        "call_amount": call_amount,
    }
