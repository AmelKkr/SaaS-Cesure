import { API_V1 } from "./constants";
import { getToken } from "./auth";

export async function api<T>(
  path: string,
  options: RequestInit & { params?: Record<string, string> } = {}
): Promise<T> {
  const { params, ...rest } = options;
  let url = path.startsWith("http") ? path : `${API_V1}${path.startsWith("/") ? path : `/${path}`}`;
  if (params) {
    const search = new URLSearchParams(params).toString();
    url += (url.includes("?") ? "&" : "?") + search;
  }
  const token = typeof window !== "undefined" ? getToken() : null;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(url, { ...rest, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(typeof err.detail === "string" ? err.detail : JSON.stringify(err));
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}
