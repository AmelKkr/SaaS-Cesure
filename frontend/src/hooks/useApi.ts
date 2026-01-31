"use client";

import { useCallback, useState } from "react";
import { api } from "@/lib/api";

export function useApi<T>() {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(false);

  const request = useCallback(async (path: string, options?: RequestInit & { params?: Record<string, string> }) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api<T>(path, options ?? {});
      setData(result);
      return result;
    } catch (e) {
      setError(e instanceof Error ? e : new Error(String(e)));
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, error, loading, request };
}
