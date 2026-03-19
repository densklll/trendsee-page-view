import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  // localhost часто резолвится в ::1, а uvicorn на 127.0.0.1 — прокси «молча» падает
  const apiProxy = env.API_PROXY_TARGET || 'http://127.0.0.1:8000'

  return {
    base: process.env.GITHUB_ACTIONS ? '/trendsee-page-view/' : '/',
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      host: '0.0.0.0',
      port: 5173,
      watch: {
        usePolling: true,
      },
      proxy: {
        '/api': {
          target: apiProxy,
          changeOrigin: true,
        },
      },
    },
  }
})
