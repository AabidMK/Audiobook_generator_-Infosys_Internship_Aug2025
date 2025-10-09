// src/api.js
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 20 * 60 * 1000, // long timeout (audio generation can be long)
});

export default api;
export { API_BASE };