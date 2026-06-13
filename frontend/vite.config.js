import { defineConfig } from 'vite'

export default defineConfig({
  root: '.',
  base: './',
  build: {
    outDir: '../static',
    emptyOutDir: false,
    rollupOptions: {
      input: './index.html',
    },
  },
  server: {
    port: 3000,
    open: false,
    allowedHosts: true,
  },
})
