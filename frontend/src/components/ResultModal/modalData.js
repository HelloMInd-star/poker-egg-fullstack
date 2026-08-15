// 对局结果弹窗文案与人物形象映射
// 文案为逐字定稿，禁止改动
export const MODAL_DATA = {
  win: {
    tag: '胜利',
    title: '计算成立，局面向你倾斜',
    body: '你这一次的风险预判与凯利系数匹配，在不确定的信息里找到了最优解。这一局的胜利，来源于你对边界的判断，而非单纯运气。',
    image: 'characters/modal_win.jpg',
    button: '收下这一局',
  },
  push: {
    tag: '平局',
    title: '势均力敌，局面持平',
    body: '双方期望值趋于平衡，没有最优解。记住这一局，很多现实选择本就不存在绝对赢家。',
    image: 'characters/modal_push.jpg',
    button: '记住了',
  },
  fold: {
    tag: '弃牌',
    title: '选择弃牌，守住你的安全边际',
    body: '当期望值为负时，放弃是决策者最重要的能力。凯利模型教会我们：不必参与每一场对局。',
    image: 'characters/modal_fold.jpg',
    button: '守住边界',
  },
  raise: {
    tag: '加注',
    title: '你选择加码，接受更大的不确定性',
    body: '你主动抬高风险权重，押注自己对局面的推演。高收益永远伴随更高的波动，请记录本次决策倾向。',
    image: 'characters/modal_raise.jpg',
    button: '记下这次倾向',
  },
  trial: {
    tag: '整局试炼结束',
    title: '本局试炼结束',
    slogan: '每一次选择，都在勾勒你的决策者心智。',
    image: 'characters/dealer.jpg',
    button: '回到牌桌',
  },
};
