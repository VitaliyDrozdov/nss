import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    const storedToken = localStorage.getItem("token");
    return storedToken !== null;
  });

  const login = () => {
    // TODO: add login logic
    localStorage.setItem("token", "MY_LOVELY_TOKEN");
    setIsLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => useContext(AuthContext);

export const useAuth = () => {
  return useAuthContext();
};