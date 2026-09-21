import { createContext, useContext, useEffect, useState } from "react";

import { getCurrentUser, loginUser, logoutUser } from "../auth/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [accessToken, setAccessToken] = useState(
    localStorage.getItem("access_token")
  );
  const [role, setRole] = useState(localStorage.getItem("role") || null);
  const [loading, setLoading] = useState(true);

  const isAuthenticated = Boolean(accessToken);

  const login = async (email, password) => {
    const data = await loginUser({
      email,
      password,
    });

    const token = data.access_token;
    const refreshToken = data.refresh_token;

    localStorage.setItem("access_token", token);

    if (refreshToken) {
      localStorage.setItem("refresh_token", refreshToken);
    }

    setAccessToken(token);

    let user = data.user;

    if (!user) {
      user = await getCurrentUser();
    }

    setCurrentUser(user);

    const userRole = user?.role || "user";
    setRole(userRole);
    localStorage.setItem("role", userRole);

    return data;
  };

  const logout = async () => {
    try {
      if (accessToken) {
        await logoutUser();
      }
    } catch (error) {
      console.error("Logout API failed:", error);
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("role");

      setCurrentUser(null);
      setAccessToken(null);
      setRole(null);
    }
  };

  const loadCurrentUser = async () => {
    try {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setLoading(false);
        return;
      }

      const user = await getCurrentUser();

      setCurrentUser(user);

      const userRole = user?.role || "user";
      setRole(userRole);
      localStorage.setItem("role", userRole);
    } catch (error) {
      console.error("Failed to load current user:", error);

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("role");

      setCurrentUser(null);
      setAccessToken(null);
      setRole(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCurrentUser();
  }, []);

  const value = {
    currentUser,
    accessToken,
    role,
    loading,
    isAuthenticated,
    login,
    logout,
    setCurrentUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}