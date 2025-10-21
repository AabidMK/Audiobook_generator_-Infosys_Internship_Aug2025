// src/api.js
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 20 * 60 * 1000, // long timeout (audio generation can be long)
});

export default api;
export { API_BASE };