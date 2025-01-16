// src/utils/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/api", // Укажите базовый URL
  headers: {
    "Content-Type": "application/json", // Общие заголовки для всех запросов
  },
});

// Добавьте обработку токенов, если требуется авторизация
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // Получаем токен из localStorage
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`; // Добавляем токен в заголовки
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
