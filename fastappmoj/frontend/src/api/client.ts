import type { SearchParams } from "../types";

const API = "/api";

function authHeader(): HeadersInit {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = "Greška na serveru";
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === "string" ? detail : "Zahtev nije uspeo");
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  get: <T>(path: string) => fetch(`${API}${path}`, { headers: { ...authHeader() } }).then(handle<T>),
  post: <T>(path: string, body?: unknown) =>
    fetch(`${API}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: body ? JSON.stringify(body) : undefined,
    }).then(handle<T>),
  patch: <T>(path: string, body: unknown) =>
    fetch(`${API}${path}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify(body),
    }).then(handle<T>),
  delete: (path: string) =>
    fetch(`${API}${path}`, { method: "DELETE", headers: { ...authHeader() } }).then(handle<void>),
  upload: <T>(path: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return fetch(`${API}${path}`, { method: "POST", headers: { ...authHeader() }, body: form }).then(handle<T>);
  },
};

export function carsQuery(params: SearchParams) {
  const q = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value) q.set(key, value);
  });
  const suffix = q.toString();
  return `/cars${suffix ? `?${suffix}` : ""}`;
}
