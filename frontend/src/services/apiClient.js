import axios from 'axios';

// In dev, Vite proxies /api to the FastAPI backend (see vite.config.js).
// In prod, set VITE_API_URL to the deployed backend's origin.
const baseURL = import.meta.env.VITE_API_URL || '/api';

const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
