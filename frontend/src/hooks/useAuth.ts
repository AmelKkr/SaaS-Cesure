"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { User, AuthResponse } from "@/types/auth";
import { api } from "@/lib/api";
import { setTokens, clearTokens, getToken, getRefreshToken } from "@/lib/auth";
import { API_V1 } from "@/lib/constants";

export function useAuth() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const loadUser = useCallback(async () => {
    const token = getToken();
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const u = await api<User>("/users/me");
      setUser(u);
    } catch {
      setUser(null);
      clearTokens();
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = useCallback(
    async (email: string, password: string) => {
      const data = await api<AuthResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setTokens(data.access_token, data.refresh_token);
      setUser(data.user);
      router.push("/dashboard");
    },
    [router]
  );

  const signup = useCallback(
    async (email: string, password: string, full_name?: string) => {
      const data = await api<AuthResponse>("/auth/signup", {
        method: "POST",
        body: JSON.stringify({ email, password, full_name: full_name || null }),
      });
      setTokens(data.access_token, data.refresh_token);
      setUser(data.user);
      router.push("/dashboard");
    },
    [router]
  );

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
    router.push("/");
  }, [router]);

  const resetPasswordRequest = useCallback(async (email: string) => {
    await api("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  }, []);

  const resetPassword = useCallback(async (token: string, new_password: string) => {
    await api("/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ token, new_password }),
    });
  }, []);

  return {
    user,
    loading,
    login,
    signup,
    logout,
    resetPasswordRequest,
    resetPassword,
    refreshUser: loadUser,
  };
}
