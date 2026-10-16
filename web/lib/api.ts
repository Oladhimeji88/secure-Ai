const base = process.env.API_URL_INTERNAL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function req(path: string, init?: RequestInit) {
  const res = await fetch(`${base}${path}`, { ...init, cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  return res.json();
}

export const api = {
  overview: () => req("/overview"),
  alerts: (query = "") => req(`/alerts${query}`),
  alert: (id: string) => req(`/alerts/${id}`),
  triage: (id: string, token?: string) =>
    req(`/alerts/${id}/triage`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    }),
  assets: () => req("/assets"),
  asset: (id: string) => req(`/assets/${id}`),
  remediation: () => req("/remediation-plan"),
  gatewayLogs: () => req("/agent-gateway/logs"),
  gatewayPolicy: () => req("/agent-gateway/policy"),
  users: () => req("/settings/users"),
  thresholds: () => req("/settings/thresholds"),
};
