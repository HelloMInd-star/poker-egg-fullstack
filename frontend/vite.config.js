import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  // base路径可通过环境变量配置，默认根路径（Docker部署），GitHub Pages设置为 /poker-egg-fullstack/
  base: process.env.VITE_BASE_PATH || '/',
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        // Docker环境使用 http://backend:5000，本地开发使用 http://localhost:5000
        target: process.env.VITE_PROXY_TARGET || 'http://localhost:5000',
        changeOrigin: true
      },
      '/ws': {
        target: process.env.VITE_WS_PROXY_TARGET || 'ws://localhost:5000',
        ws: true
      }
    }
  },
  build: {
    outDir: 'dist'
  }
});
