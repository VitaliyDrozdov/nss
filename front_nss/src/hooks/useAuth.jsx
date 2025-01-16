import { createContext, useContext, useState } from "react";
import api from "../utils/api";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();

  const [token, setToken] = useState(() => localStorage.getItem("token"));

  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = async () => {
    if (localStorage.getItem("token")) {
      const response = await api.post("/auth/logout");
      if (response.status === 200) {
        localStorage.removeItem("token");
        setToken(null);
        navigate("/signin");
      }
    } else {
      console.log("Токен отсутствует в localStorage");
      navigate("/signin");
    }
  };

  const isLoggedIn = Boolean(token);

  return (
    <AuthContext.Provider value={{ token, isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Хук для удобного доступа к AuthContext
export const useAuthContext = () => useContext(AuthContext);

export const useAuth = () => {
  return useAuthContext();
};