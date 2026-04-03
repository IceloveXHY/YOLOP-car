import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      
    },
  },
  server: {
    proxy: {
      // 配置代理规则
      '/drowsy_driving': {
        target: 'http://localhost:8000', // 后端服务器地址
        changeOrigin: true, // 允许跨域
        rewrite: (path) => path.replace(/^\/drowsy_driving/, ''), // 重写路径
      },
      // '/illegal_parking': {
      //   target: 'http://localhost:8000', // 后端服务器地址
      //   changeOrigin: true, // 允许跨域
      //   rewrite: (path) => path.replace(/^\/illegal_parking/, ''), // 重写路径
      // },
      '/api/upload': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/upload/, '/api/upload') // 或者不写rewrite，看实际情况
      },
      '/ws/process': {
        target: 'ws://localhost:8000',
        ws: true, // 启用WebSocket代理
        changeOrigin: true
      },
      '/lane_markings': {
        target: 'http://localhost:8000', // 后端服务器地址
        changeOrigin: true, // 允许跨域
        rewrite: (path) => path.replace(/^\/lane_markings/, ''), // 重写路径
      },
      '/throws': {
        target: 'http://localhost:8000', // 后端服务器地址
        changeOrigin: true, // 允许跨域
        rewrite: (path) => path.replace(/^\/throws/, ''), // 重写路径
      },
    },
  },
})
