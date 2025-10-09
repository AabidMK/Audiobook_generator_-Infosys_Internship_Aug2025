import axios from "axios";

const API = axios.create({
<<<<<<< HEAD
  baseURL: "http://localhost:8080", // Backend server port
=======
  baseURL: "http://127.0.0.1:8000", // FastAPI default port
>>>>>>> 7508fd7f3204606fd8e9396d1b9d8870ceb8a5a4
});

export default API;