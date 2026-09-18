import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { api } from "../api/client";
import type { UserMe } from "../types";

type AuthContextValue = {
  user: UserMe | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<UserMe>;
  register: (payload: Record<string, string>) => Promise<UserMe>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserMe | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .get<UserMe>("/auth/me")
      .then(setUser)
      .catch(() => localStorage.removeItem("token"))
      .finally(() => setLoading(false));
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      loading,
      login: async (email, password) => {
        const res = await api.post<{ access_token: string; role: string }>("/auth/login", { email, password });
        localStorage.setItem("token", res.access_token);
        const me = await api.get<UserMe>("/auth/me");
        setUser(me);
        return me;
      },
      register: async (payload) => {
        const res = await api.post<{ access_token: string }>("/auth/register", payload);
        localStorage.setItem("token", res.access_token);
        const me = await api.get<UserMe>("/auth/me");
        setUser(me);
        return me;
      },
      logout: () => {
        localStorage.removeItem("token");
        setUser(null);
        void api.post("/auth/logout");
      },
    }),
    [user, loading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth mora biti unutar AuthProvider");
  return ctx;
}
