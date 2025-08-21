import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: API_BASE_URL,
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
