import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  // 关键：发布到 GitHub Pages 子路径时需要设置 base
  base: '/poker-egg-fullstack/',
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://localhost:5000',
        ws: true
      }
    }
  },
  build: {
    outDir: 'dist'
  }
});
