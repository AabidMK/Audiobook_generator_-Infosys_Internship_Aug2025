// src/api.js
import axios from "axios";

<<<<<<< HEAD
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";
=======
const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
>>>>>>> 7508fd7f3204606fd8e9396d1b9d8870ceb8a5a4

const api = axios.create({
  baseURL: API_BASE,
  timeout: 20 * 60 * 1000, // long timeout (audio generation can be long)
});

export default api;
export { API_BASE };