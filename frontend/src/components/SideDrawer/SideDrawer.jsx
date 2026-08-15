import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './SideDrawer.css';

/**
 * 侧边抽屉 · 辅助信息收纳层
 * 右缘贴纸风悬浮钮，点击滑出、遮罩/✕关闭。
 * 内容组件随 gameState props 实时刷新，数据流不断。
 */
const SideDrawer = ({ items }) => {
  const [openKey, setOpenKey] = useState(null);
  const active = items.find(i => i.key === openKey);

  return (
    <>
      <div className="side-rail">
        {items.map(i => (
          <button
            key={i.key}
            className={`side-rail-btn ${openKey === i.key ? 'active' : ''}`}
            onClick={() => setOpenKey(openKey === i.key ? null : i.key)}
            title={i.title}
          >
            <span className="rail-icon">{i.icon}</span>
            <span className="rail-label">{i.label}</span>
          </button>
        ))}
      </div>

      <AnimatePresence>
        {active && (
          <>
            <motion.div
              key="mask"
              className="side-drawer-mask"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setOpenKey(null)}
            />
            <motion.aside
              key="drawer"
              className="side-drawer"
              initial={{ x: '110%' }}
              animate={{ x: 0 }}
              exit={{ x: '110%' }}
              transition={{ type: 'tween', duration: 0.28, ease: 'easeOut' }}
            >
              <div className="side-drawer-head">
                <span className="side-drawer-title">{active.icon} {active.title}</span>
                <button className="side-drawer-close" onClick={() => setOpenKey(null)}>✕</button>
              </div>
              <div className="side-drawer-body">
                {active.content}
              </div>
              <span className="drawer-doodle dd-1">✦</span>
              <span className="drawer-doodle dd-2">⚡</span>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
};

export default SideDrawer;
