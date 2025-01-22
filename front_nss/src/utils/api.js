import axios from "axios";

import { useNavigate } from 'react-router-dom';

const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});



api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Добавьте обработку ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error("Ошибка авторизации: Токен истёк или недействителен.");
      const navigate = useNavigate();

      // Удаляем токен из локального хранилища
      localStorage.removeItem("token");

      // Перенаправляем пользователя на страницу авторизации
      navigate("/signin");
      window.location.reload(); // Перезагрузка страницы для корректного редиректа
    }

    return Promise.reject(error); // Пропускаем ошибку дальше
  }
);

export default api;

