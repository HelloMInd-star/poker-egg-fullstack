// 午夜酒馆・决策者试炼 —— 文案与数据（文案为产品定稿原文，勿改字）

export const INTRO_LINES = [
  '夜色落下，你推开午夜酒馆厚重的木门。',
  '吧台之内，四位调酒师安静伫立。',
  '今夜没有棋局，没有筹码，没有标准答案。',
  '试炼藏在五件最真实的抉择里：事业、独处、微醺、人群、爱意。',
  '你不需要填写问卷。你的每一次选择，都会记录你的决策者心智。',
  '试炼结束之时，四位调酒师会呈上各自的专属特调，由你来选择今夜归属于你的那一杯。',
];

export const QUESTIONS = [
  {
    key: 'career',
    tag: '事业',
    title: '情景 1｜事业・重大项目',
    scene: '你接手一个回报巨大的长期项目，但需要持续高强度投入，同时伴随着不小失败的风险。',
    options: [
      { label: 'A', text: '先搭建完整风险预案，拉长周期稳步推进，给自己留好退路。', type: 'INTJ' },
      { label: 'B', text: '先搜集全部资料，推演所有可能性，完善整套方案之后再启动，不急着开工。', type: 'INTP' },
      { label: 'C', text: '看准机会便全力投入，集中全部资源，快速拿下目标。', type: 'ENTJ' },
      { label: 'D', text: '拒绝被单一计划束缚，边执行边迭代，不断尝试全新思路。', type: 'ENTP' },
    ],
  },
  {
    key: 'solitude',
    tag: '独处',
    title: '情景 2｜独处・完整空闲日',
    scene: '漫长忙碌过后，你拥有完全属于自己的一整天，没有任何安排。',
    options: [
      { label: 'A', text: '安静复盘过往，规划接下来一段时期的长期路线。', type: 'INTJ' },
      { label: 'B', text: '一头扎进感兴趣的理论与知识，任由思绪自由发散探索。', type: 'INTP' },
      { label: 'C', text: '设立新目标，利用这段时间自我提升，推进搁置已久的事项。', type: 'ENTJ' },
      { label: 'D', text: '即兴出门游荡，去体验从未尝试过的新鲜事物。', type: 'ENTP' },
    ],
  },
  {
    key: 'tipsy',
    tag: '微醺',
    title: '情景 3｜微醺・深夜吧台',
    scene: '深夜，你独自坐在吧台，面前空着一只酒杯。',
    options: [
      { label: 'A', text: '小酌一杯，安静复盘今日得失，思索未来的布局。', type: 'INTJ' },
      { label: 'B', text: '慢慢饮酒，任由无数想法在脑海之中碰撞推演。', type: 'INTP' },
      { label: 'C', text: '短暂放松之后迅速整理思绪，列好明日清晰的行动清单。', type: 'ENTJ' },
      { label: 'D', text: '主动与调酒师交谈，交换观点，碰撞新奇的想法。', type: 'ENTP' },
    ],
  },
  {
    key: 'social',
    tag: '人群',
    title: '情景 4｜社交・智者聚会',
    scene: '一场汇聚众多行业强者、思想者的聚会向你发出邀约。',
    options: [
      { label: 'A', text: '带着明确目的选择性赴约，高效交流，适时离场。', type: 'INTJ' },
      { label: 'B', text: '以观察者的心态前往，乐于交换观点，不必刻意融入圈子。', type: 'INTP' },
      { label: 'C', text: '把握机遇拓展人脉，寻找合作与未来的机会。', type: 'ENTJ' },
      { label: 'D', text: '期待思想的交锋，乐于抛出不一样的观点，享受辩论。', type: 'ENTP' },
    ],
  },
  {
    key: 'love',
    tag: '爱意',
    title: '情景 5｜爱意・不确定的缘分',
    scene: '你遇见一个极具吸引力的人，但两个人的性格、未来规划都充满未知。',
    options: [
      { label: 'A', text: '冷静衡量双方长期适配度，谨慎投入，慢慢观察。', type: 'INTJ' },
      { label: 'B', text: '拆解彼此三观与思维差异，不断推演这段关系所有可能性。', type: 'INTP' },
      { label: 'C', text: '认定之后便主动奔赴，认真规划两个人的前路。', type: 'ENTJ' },
      { label: 'D', text: '顺其自然享受思想同频的时刻，不急着定义、不束缚彼此。', type: 'ENTP' },
    ],
  },
];

export const FINAL_LINES = [
  '五次试炼已经结束。',
  '根据你一路的抉择，酒馆已经窥见了你心智的偏向。',
  '但最终的答案不必由系统单方面判定。',
  '四位调酒师向前一步，各自推来一杯独属于自己心智的特调。',
  '你不必完全成为某一类人，只是今夜，请认领一杯最契合你内心的酒。',
];

export const DRINKS = [
  {
    type: 'INTJ',
    name: '尼格罗尼',
    nameEn: 'Negroni',
    image: 'negroni.jpg',
    desc: '苦甜平衡，配方恒久。克制权衡，谋定而后动。',
    kellyMode: '半凯利，预留安全边际',
    kellyCoefficient: 0.5,
  },
  {
    type: 'INTP',
    name: '马天尼',
    nameEn: 'Martini',
    image: 'martini.jpg',
    desc: '拥有无穷的调配变体，永远存在另一种解法。',
    kellyMode: '多情景推演，分析优先',
    kellyCoefficient: 0.3,
  },
  {
    type: 'ENTJ',
    name: '古典',
    nameEn: 'Old-Fashioned',
    image: 'oldfashioned.jpg',
    desc: '纯粹厚重，删繁就简，目标坚定一往无前。',
    kellyMode: '高确信度启用 Full-Kelly',
    kellyCoefficient: 1.0,
  },
  {
    type: 'ENTP',
    name: '血腥玛丽',
    nameEn: 'Bloody Mary',
    image: 'bloodymary.jpg',
    desc: '没有固定配方，可以自由添加香料，改写一切规则。',
    kellyMode: '以凯利为基准，主动扰动局面',
    kellyCoefficient: 0.75,
  },
];

// 决策者特质报告
export const TRAIT_REPORTS = {
  INTJ: [
    '你是长线布局者：克制权衡，谋定而后动。出手之前，你习惯先在沙盘上推演完整的风险预案——宁可慢一步，也不给失控留机会。',
    '在博弈中，你的优势是纪律与耐心：不为一时波动所动，只在赔率站在你这边时下注。',
    '半凯利模式为你的决策预留安全边际：用一半的波动，换长期的复利曲线。',
  ],
  INTP: [
    '你是思想实验者：多情景推演，分析优先。落子之前，你习惯在脑内跑完所有可能的分支，永远相信存在另一种更优的解法。',
    '在博弈中，你的优势是深度与客观：不被情绪带节奏，对胜率的估计比多数人更接近真实。',
    '修正后的仓位更保守，为你留足推演与等待的时间——看得足够清楚，再出手。',
  ],
  ENTJ: [
    '你是目标坚定的进攻者：删繁就简，一往无前。看准的机会，你会集中全部资源快速拿下，不接受半吊子的投入。',
    '在博弈中，你的优势是决断与执行：别人犹豫的窗口期，就是你的利润来源。',
    '当确信度足够高时，Full-Kelly 让你的优势最大化兑现——数学站在你这边时，你从不退缩。',
  ],
  ENTP: [
    '你是规则的改写者：以凯利为基准，主动扰动局面。你不接受被单一计划束缚，习惯边执行边迭代，在变化中制造优势。',
    '在博弈中，你的优势是灵活与创造：你打出的每一手，都在破坏对手的心理模型。',
    '修正系数给你凯利基准之上的弹性空间：用可控的扰动，制造对手的不适应。',
  ],
};

export const TAVERN_STORAGE_KEY = 'midnight_tavern_profile';
