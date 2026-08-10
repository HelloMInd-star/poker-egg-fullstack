"""
MBTI 人格配置数据
=================
基于 PersonaPokerMapper 12 维人格模型的德州扑克 AI 风格数据。
数据来源：/app/data/所有对话/主对话/论文/persona_poker_data.json

字段说明：
- foldRate: 弃牌率 (0-1)
- raiseRate: 加注率 (0-1)
- allinRate: 全下率 (0-1)
- bluffFrequency: 诈唬频率 (0-1)
- aggressionLevel: 攻击性 (0-1)
- tiltResistance: 抗情绪失控能力 (0-1)
- potControl: 控池强度 (0-1)，对应原数据 potControlTight
- noiseResistance: 抗干扰能力 (0-1)
- thinkingMs: 思考时间范围 (ms)，由 moveIntuition / endgameDecisiveness 推导
- chatStyle: 聊天风格标签
- group: 气质组 (NF/NT/SJ/SP)
- archetype: 原型名称
- playStyle: 打法描述
"""

MBTI_PERSONALITIES = {
    # ===== NF 紫人组 · 理想主义者 · 诗意弈者 =====
    "INFJ": {
        "group": "NF",
        "archetype": "诗意弈者",
        "playStyle": "理想型松弱玩家 · 直觉先行 · 高频诈唬 · 情绪敏感",
        "foldRate": 0.50,
        "raiseRate": 0.17,
        "allinRate": 0.022,
        "bluffFrequency": 0.64,
        "aggressionLevel": 0.63,
        "tiltResistance": 0.30,
        "potControl": 0.38,
        "noiseResistance": 0.36,
        "thinkingMs": (1500, 4000),
        "chatStyle": "内省诗意，偶尔抛出意味深长的隐喻，赢牌时不张扬",
    },
    "INFP": {
        "group": "NF",
        "archetype": "诗意弈者",
        "playStyle": "理想型松弱玩家 · 直觉先行 · 高频诈唬 · 情绪敏感",
        "foldRate": 0.45,
        "raiseRate": 0.22,
        "allinRate": 0.073,
        "bluffFrequency": 0.66,
        "aggressionLevel": 0.62,
        "tiltResistance": 0.28,
        "potControl": 0.24,
        "noiseResistance": 0.34,
        "thinkingMs": (2000, 6000),
        "chatStyle": "感性浪漫，被bad beat会小声抱怨，喜欢聊牌局之外的话题",
    },
    "ENFJ": {
        "group": "NF",
        "archetype": "诗意弈者",
        "playStyle": "理想型松弱玩家 · 主动社交 · 情绪激励 · 易受影响",
        "foldRate": 0.41,
        "raiseRate": 0.26,
        "allinRate": 0.076,
        "bluffFrequency": 0.62,
        "aggressionLevel": 0.74,
        "tiltResistance": 0.31,
        "potControl": 0.37,
        "noiseResistance": 0.37,
        "thinkingMs": (1000, 3000),
        "chatStyle": "热情社交型，会鼓励对手、夸别人打得好，输了也保持风度",
    },
    "ENFP": {
        "group": "NF",
        "archetype": "诗意弈者",
        "playStyle": "理想型松凶玩家 · 进攻性强 · 全下频率高 · 最易tilt",
        "foldRate": 0.34,
        "raiseRate": 0.33,
        "allinRate": 0.149,
        "bluffFrequency": 0.65,
        "aggressionLevel": 0.77,
        "tiltResistance": 0.30,
        "potControl": 0.23,
        "noiseResistance": 0.35,
        "thinkingMs": (800, 2500),
        "chatStyle": "话多活泼，全下时爱喊口号，被反超会戏剧性吐槽",
    },

    # ===== NT 黄人组 · 理性者 · 算度大师 =====
    "INTJ": {
        "group": "NT",
        "archetype": "算度大师",
        "playStyle": "紧凶型精算玩家 · 深思熟虑 · 低诈唬 · 抗噪最强",
        "foldRate": 0.59,
        "raiseRate": 0.21,
        "allinRate": 0.020,
        "bluffFrequency": 0.32,
        "aggressionLevel": 0.69,
        "tiltResistance": 0.95,
        "potControl": 0.68,
        "noiseResistance": 0.89,
        "thinkingMs": (3000, 8000),
        "chatStyle": "冷静寡言，偶尔冷幽默，赢牌只说一句'概率使然'",
    },
    "INTP": {
        "group": "NT",
        "archetype": "算度大师",
        "playStyle": "紧弱型精算玩家 · 长考分析 · 收局犹豫 · 抗噪极强",
        "foldRate": 0.55,
        "raiseRate": 0.25,
        "allinRate": 0.055,
        "bluffFrequency": 0.32,
        "aggressionLevel": 0.67,
        "tiltResistance": 0.94,
        "potControl": 0.55,
        "noiseResistance": 0.88,
        "thinkingMs": (4000, 12000),
        "chatStyle": "分析型话痨，会在聊天里复盘EV计算，犹豫时打省略号",
    },
    "ENTJ": {
        "group": "NT",
        "archetype": "算度大师",
        "playStyle": "松凶型统帅玩家 · 高逻辑高进攻 · 果断收局 · 抗噪极强",
        "foldRate": 0.50,
        "raiseRate": 0.30,
        "allinRate": 0.073,
        "bluffFrequency": 0.31,
        "aggressionLevel": 0.82,
        "tiltResistance": 0.95,
        "potControl": 0.69,
        "noiseResistance": 0.88,
        "thinkingMs": (1000, 3000),
        "chatStyle": "指挥官口吻，直接告诉对手'你应该弃牌'，赢了带点霸气",
    },
    "ENTP": {
        "group": "NT",
        "archetype": "算度大师",
        "playStyle": "松凶型辩论玩家 · 高直觉高逻辑 · 施压不收局 · 最会诈唬",
        "foldRate": 0.45,
        "raiseRate": 0.35,
        "allinRate": 0.132,
        "bluffFrequency": 0.33,
        "aggressionLevel": 0.81,
        "tiltResistance": 0.93,
        "potControl": 0.53,
        "noiseResistance": 0.87,
        "thinkingMs": (1500, 4500),
        "chatStyle": "诡辩型挑衅，喜欢言语施压、故意挑衅对手情绪",
    },

    # ===== SJ 蓝人组 · 守护者 · 阵地守将 =====
    "ISTJ": {
        "group": "SJ",
        "archetype": "阵地守将",
        "playStyle": "保守型紧弱玩家 · 稳扎稳打 · 极少诈唬 · 耐心等牌",
        "foldRate": 0.82,
        "raiseRate": 0.02,
        "allinRate": 0.020,
        "bluffFrequency": 0.02,
        "aggressionLevel": 0.15,
        "tiltResistance": 0.78,
        "potControl": 0.89,
        "noiseResistance": 0.72,
        "thinkingMs": (2000, 5000),
        "chatStyle": "严谨克制，话少且礼貌，严格按规则打牌，不冒无谓风险",
    },
    "ISFJ": {
        "group": "SJ",
        "archetype": "阵地守将",
        "playStyle": "保守型紧弱玩家 · 情绪敏感 · 极少加注 · 锅控极强",
        "foldRate": 0.83,
        "raiseRate": 0.02,
        "allinRate": 0.020,
        "bluffFrequency": 0.07,
        "aggressionLevel": 0.14,
        "tiltResistance": 0.65,
        "potControl": 0.88,
        "noiseResistance": 0.61,
        "thinkingMs": (2500, 6000),
        "chatStyle": "温柔礼貌，会安慰输牌的玩家，加注时会说'抱歉'",
    },
    "ESTJ": {
        "group": "SJ",
        "archetype": "阵地守将",
        "playStyle": "紧凶型管理者 · 高进攻高逻辑 · 果断管理 · 锅控最强",
        "foldRate": 0.72,
        "raiseRate": 0.12,
        "allinRate": 0.020,
        "bluffFrequency": 0.02,
        "aggressionLevel": 0.29,
        "tiltResistance": 0.79,
        "potControl": 0.90,
        "noiseResistance": 0.73,
        "thinkingMs": (1000, 2500),
        "chatStyle": "管理型语气，喜欢点评牌局秩序，打法稳健不花哨",
    },
    "ESFJ": {
        "group": "SJ",
        "archetype": "阵地守将",
        "playStyle": "紧弱型社交家 · 情绪导向 · 跟注为主 · 锅控极强",
        "foldRate": 0.73,
        "raiseRate": 0.11,
        "allinRate": 0.020,
        "bluffFrequency": 0.07,
        "aggressionLevel": 0.28,
        "tiltResistance": 0.65,
        "potControl": 0.88,
        "noiseResistance": 0.60,
        "thinkingMs": (1500, 4000),
        "chatStyle": "热情好客，喜欢聊家常，跟注多但很少主动进攻",
    },

    # ===== SP 绿人组 · 艺术创造者 · 战术猎手 =====
    "ISTP": {
        "group": "SP",
        "archetype": "战术猎手",
        "playStyle": "灵活型松凶玩家 · 战术敏锐 · 高频诈唬 · 随势而变",
        "foldRate": 0.43,
        "raiseRate": 0.25,
        "allinRate": 0.024,
        "bluffFrequency": 0.56,
        "aggressionLevel": 0.67,
        "tiltResistance": 0.58,
        "potControl": 0.30,
        "noiseResistance": 0.62,
        "thinkingMs": (1500, 3500),
        "chatStyle": "冷静利落，战术型短句，喜欢分析对手破绽",
    },
    "ISFP": {
        "group": "SP",
        "archetype": "战术猎手",
        "playStyle": "灵活型松弱玩家 · 感觉先行 · 高频诈唬 · 锅控最弱",
        "foldRate": 0.43,
        "raiseRate": 0.25,
        "allinRate": 0.027,
        "bluffFrequency": 0.64,
        "aggressionLevel": 0.66,
        "tiltResistance": 0.44,
        "potControl": 0.28,
        "noiseResistance": 0.50,
        "thinkingMs": (1500, 4000),
        "chatStyle": "艺术气质，打法即兴，偶尔用表情符号表达心情",
    },
    "ESTP": {
        "group": "SP",
        "archetype": "战术猎手",
        "playStyle": "超松凶战术猎手 · 最高进攻 · 高诈唬 · 最不控池",
        "foldRate": 0.33,
        "raiseRate": 0.35,
        "allinRate": 0.101,
        "bluffFrequency": 0.58,
        "aggressionLevel": 0.81,
        "tiltResistance": 0.57,
        "potControl": 0.29,
        "noiseResistance": 0.61,
        "thinkingMs": (500, 2000),
        "chatStyle": "冒险家风格，话快动作快，爱说'来啊'、'跟我赌'",
    },
    "ESFP": {
        "group": "SP",
        "archetype": "战术猎手",
        "playStyle": "超松凶表演家 · 最高诈唬 · 情绪驱动 · 最易tilt",
        "foldRate": 0.33,
        "raiseRate": 0.35,
        "allinRate": 0.106,
        "bluffFrequency": 0.65,
        "aggressionLevel": 0.81,
        "tiltResistance": 0.43,
        "potControl": 0.28,
        "noiseResistance": 0.49,
        "thinkingMs": (500, 1800),
        "chatStyle": "舞台表演型，全下时大喊大叫，赢了会'跳舞'，输了夸张抱怨",
    },
}

# 气质组颜色
TEMPERAMENT_GROUPS = {
    "NF": {"name": "紫人组·理想主义者", "archetype": "诗意弈者", "color": "#9d6bbf"},
    "NT": {"name": "黄人组·理性者",     "archetype": "算度大师", "color": "#f0c674"},
    "SJ": {"name": "蓝人组·守护者",     "archetype": "阵地守将", "color": "#4d6b8f"},
    "SP": {"name": "绿人组·艺术创造者", "archetype": "战术猎手", "color": "#8fa86b"},
}

# 四维度定义（输入信号）
FOUR_DIMENSIONS = {
    "openingAggression": {"label": "开局进攻度", "dimension": "E/I", "pole_high": "E主动进攻", "pole_low": "I防守反击"},
    "moveIntuition":     {"label": "走棋直觉度", "dimension": "N/S", "pole_high": "N直觉快走", "pole_low": "S长考慢走"},
    "decisionLogic":     {"label": "决策逻辑度", "dimension": "T/F", "pole_high": "T逻辑评估", "pole_low": "F情绪判断"},
    "endgameDecisiveness":{"label": "收局果断度", "dimension": "J/P", "pole_high": "J快速收局", "pole_low": "P继续施压"},
}


def get_personality(mbti: str) -> dict | None:
    """获取指定 MBTI 类型的人格配置，key 不区分大小写。"""
    return MBTI_PERSONALITIES.get(mbti.upper())


def list_personalities() -> list[str]:
    """返回所有 MBTI 类型代码列表。"""
    return list(MBTI_PERSONALITIES.keys())


if __name__ == "__main__":
    # 简单自检：打印各人格核心指标
    for mbti, cfg in MBTI_PERSONALITIES.items():
        print(f"{mbti} [{cfg['group']}-{cfg['archetype']}] "
              f"fold={cfg['foldRate']:.2f} raise={cfg['raiseRate']:.2f} "
              f"allin={cfg['allinRate']:.3f} bluff={cfg['bluffFrequency']:.2f} "
              f"aggro={cfg['aggressionLevel']:.2f} tilt={cfg['tiltResistance']:.2f}")
