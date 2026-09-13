import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite configuration for the Complaint Management System frontend.
// A dev-server proxy forwards /api calls to the FastAPI backend so the
// browser never needs to know the backend's real host/port.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
