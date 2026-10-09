// Upwork OAuth 2.1 + MCP integration
// Verified endpoints from https://mcp.upwork.com/.well-known/oauth-authorization-server:
//   authorization_endpoint: https://www.upwork.com/ab/account-security/oauth2/authorize
//   token_endpoint:          https://www.upwork.com/api/v3/oauth2/token
//   revocation_endpoint:     https://www.upwork.com/api/v3/oauth2/token/revoke
//   code_challenge_methods_supported: ["S256"]  (PKCE required)
//   grant_types_supported: ["authorization_code","refresh_token","client_credentials"]
//
// Operator must register an API app at https://www.upwork.com/developer (Create New App)
// and set redirect_uri = https://apsa-2026.vercel.app/api/upwork/oauth/callback
// Then set in .env.local:
//   UPWORK_CLIENT_ID=<from dev portal>
//   UPWORK_CLIENT_SECRET=<from dev portal>
//   UPWORK_REDIRECT_URI=https://apsa-2026.vercel.app/api/upwork/oauth/callback
//
// Tokens stored to /home/z/my-project/.upwork/tokens.json (mode 0600, .gitignored)
// Tokens include: access_token, refresh_token, expires_at, scope, obtained_at

import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { createHash, randomBytes } from "node:crypto";

export const UPWORK = {
  ISSUER: "https://mcp.upwork.com",
  AUTHORIZE: "https://www.upwork.com/ab/account-security/oauth2/authorize",
  TOKEN: "https://www.upwork.com/api/v3/oauth2/token",
  REVOKE: "https://www.upwork.com/api/v3/oauth2/token/revoke",
  MCP: "https://mcp.upwork.com/mcp",
  RESOURCE_METADATA: "https://mcp.upwork.com/.well-known/oauth-protected-resource/mcp",
  TOKENS_FILE: "/home/z/my-project/.upwork/tokens.json",
  PKCE_FILE: "/home/z/my-project/.upwork/pending-pkce.json",
};

export const UPWORK_CLIENT_ID = process.env.UPWORK_CLIENT_ID || "";
export const UPWORK_CLIENT_SECRET = process.env.UPWORK_CLIENT_SECRET || "";
export const UPWORK_REDIRECT_URI =
  process.env.UPWORK_REDIRECT_URI ||
  "https://apsa-2026.vercel.app/api/upwork/oauth/callback";

// ─────────────────────────────────────────────────────────────────────────────
// PKCE (RFC 7636) — required by Upwork (code_challenge_methods_supported=["S256"])
// ─────────────────────────────────────────────────────────────────────────────

export function makePkcePair(): { verifier: string; challenge: string } {
  const verifier = randomBytes(32).toString("base64url");
  const challenge = createHash("sha256").update(verifier).digest("base64url");
  return { verifier, challenge };
}

export async function savePendingPkce(
  state: string,
  verifier: string,
  next: string,
): Promise<void> {
  await mkdir(join(UPWORK.PKCE_FILE, ".."), { recursive: true });
  const rec = {
    state,
    verifier,
    next, // where the user wanted to land after auth
    created_at: new Date().toISOString(),
  };
  await writeFile(UPWORK.PKCE_FILE, JSON.stringify(rec, null, 2), { mode: 0o600 });
}

export async function loadAndClearPendingPkce(
  state: string,
): Promise<{ verifier: string; next: string } | null> {
  if (!existsSync(UPWORK.PKCE_FILE)) return null;
  try {
    const rec = JSON.parse(await readFile(UPWORK.PKCE_FILE, "utf8"));
    if (rec.state !== state) return null;
    // Verify freshness (≤10 min)
    const ageMs = Date.now() - new Date(rec.created_at).getTime();
    if (ageMs > 10 * 60_000) return null;
    return { verifier: rec.verifier, next: rec.next || "/?tab=marketplaces" };
  } catch {
    return null;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Token storage (receive-only use; never exposed to client)
// ─────────────────────────────────────────────────────────────────────────────

export interface UpworkTokens {
  access_token: string;
  refresh_token: string | null;
  token_type: string;
  expires_at: string; // ISO
  scope: string;
  obtained_at: string;
}

export async function saveTokens(t: UpworkTokens): Promise<void> {
  await mkdir(join(UPWORK.TOKENS_FILE, ".."), { recursive: true });
  await writeFile(UPWORK.TOKENS_FILE, JSON.stringify(t, null, 2), { mode: 0o600 });
}

export async function loadTokens(): Promise<UpworkTokens | null> {
  if (!existsSync(UPWORK.TOKENS_FILE)) return null;
  try {
    return JSON.parse(await readFile(UPWORK.TOKENS_FILE, "utf8"));
  } catch {
    return null;
  }
}

export async function refreshTokens(t: UpworkTokens): Promise<UpworkTokens | null> {
  if (!t.refresh_token) return null;
  const body = new URLSearchParams({
    grant_type: "refresh_token",
    refresh_token: t.refresh_token,
    client_id: UPWORK_CLIENT_ID,
    client_secret: UPWORK_CLIENT_SECRET,
  });
  const r = await fetch(UPWORK.TOKEN, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
    cache: "no-store",
  });
  if (!r.ok) return null;
  const j = (await r.json()) as Record<string, string | number>;
  const next: UpworkTokens = {
    access_token: String(j.access_token),
    refresh_token: (j.refresh_token as string) || t.refresh_token,
    token_type: (j.token_type as string) || "Bearer",
    expires_at: new Date(
      Date.now() + Number(j.expires_in ?? 3600) * 1000,
    ).toISOString(),
    scope: (j.scope as string) || t.scope,
    obtained_at: new Date().toISOString(),
  };
  await saveTokens(next);
  return next;
}

export async function getValidAccessToken(): Promise<string | null> {
  const t = await loadTokens();
  if (!t) return null;
  // Refresh if <60s left
  const expiresAt = new Date(t.expires_at).getTime();
  if (expiresAt - Date.now() < 60_000 && t.refresh_token) {
    const refreshed = await refreshTokens(t);
    return refreshed?.access_token || null;
  }
  return t.access_token;
}

// ─────────────────────────────────────────────────────────────────────────────
// MCP JSON-RPC call (Streamable HTTP transport)
// ─────────────────────────────────────────────────────────────────────────────

export async function callUpworkMcp(
  toolName: string,
  args: Record<string, unknown> = {},
): Promise<unknown> {
  const token = await getValidAccessToken();
  if (!token) {
    return { error: "no_upwork_token", message: "Run /api/upwork/oauth/authorize first" };
  }
  const r = await fetch(UPWORK.MCP, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      "mcp-protocol-version": "2025-06-18",
      "User-Agent": "APSA-2026/1.0 (+https://apsa-2026.vercel.app)",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: toolName, arguments: args },
    }),
    cache: "no-store",
  });
  if (r.status === 401) {
    return { error: "unauthorized", message: "Token expired or revoked — refresh needed" };
  }
  if (!r.ok) {
    return { error: `http_${r.status}`, message: `MCP call ${toolName} failed` };
  }
  const data = (await r.json()) as { result?: { content?: Array<{ text?: string }> } };
  const text = data?.result?.content?.[0]?.text || "";
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}
