import { createHash, randomBytes } from "node:crypto";
import { readFile, writeFile, mkdir, chmod } from "node:fs/promises";
import { existsSync } from "node:fs";

/**
 * Shared helpers for the Upwork MCP OAuth 2.1 flow.
 * - PKCE S256 pair generation
 * - State store (single pending flow, mode 600)
 * - Authorization URL builder (per https://mcp.upwork.com/.well-known/oauth-authorization-server)
 * - Code → token exchange (public client, auth method "none")
 * - Credential persistence (3 locations, mode 600 — lesson #1: sandbox wipes)
 */

export const UPWORK_AUTH_URL =
  "https://www.upwork.com/ab/account-security/oauth2/authorize";
export const UPWORK_TOKEN_URL = "https://www.upwork.com/api/v3/oauth2/token";
export const UPWORK_MCP_URL = "https://mcp.upwork.com/mcp";
export const UPWORK_SCOPE = "mcp";

export const STATE_FILE =
  "/home/z/my-project/.upwork/oauth-state.json";
export const CREDS_FILE =
  "/home/z/my-project/.upwork/credentials.json";
export const CREDS_BACKUP_1 = "/home/z/.upwork/credentials.json";
export const CREDS_BACKUP_2 =
  "/home/z/.local/share/apsa-credentials/upwork/credentials.json";

export interface UpworkCreds {
  platform: "Upwork MCP";
  mcp_endpoint: string;
  access_token: string;
  refresh_token?: string;
  token_type?: string;
  expires_at?: string;
  scope?: string;
  obtained_at: string;
}

export function pkcePair() {
  const verifier = randomBytes(48).toString("base64url");
  const challenge = createHash("sha256").update(verifier).digest("base64url");
  return { verifier, challenge };
}

export async function saveStateFile(state: unknown) {
  await mkdir("/home/z/my-project/.upwork", { recursive: true });
  await writeFile(STATE_FILE, JSON.stringify(state, null, 2), { mode: 0o600 });
  await chmod(STATE_FILE, 0o600).catch(() => {});
}

export async function loadStateFile<T>(): Promise<T | null> {
  try {
    if (!existsSync(STATE_FILE)) return null;
    return JSON.parse(await readFile(STATE_FILE, "utf8")) as T;
  } catch {
    return null;
  }
}

export async function saveCreds(creds: UpworkCreds) {
  const paths = [CREDS_FILE, CREDS_BACKUP_1, CREDS_BACKUP_2];
  for (const p of paths) {
    const dir = p.split("/").slice(0, -1).join("/");
    await mkdir(dir, { recursive: true });
    await writeFile(p, JSON.stringify(creds, null, 2), { mode: 0o600 });
    await chmod(p, 0o600).catch(() => {});
  }
}

export async function loadCreds(): Promise<UpworkCreds | null> {
  for (const p of [CREDS_FILE, CREDS_BACKUP_1, CREDS_BACKUP_2]) {
    try {
      if (existsSync(p)) return JSON.parse(await readFile(p, "utf8"));
    } catch {
      /* try next */
    }
  }
  return null;
}

export function buildAuthorizeUrl(params: {
  clientId: string;
  redirectUri: string;
  challenge: string;
  state: string;
}) {
  const u = new URL(UPWORK_AUTH_URL);
  u.searchParams.set("response_type", "code");
  u.searchParams.set("client_id", params.clientId);
  u.searchParams.set("redirect_uri", params.redirectUri);
  u.searchParams.set("scope", UPWORK_SCOPE);
  u.searchParams.set("state", params.state);
  u.searchParams.set("code_challenge", params.challenge);
  u.searchParams.set("code_challenge_method", "S256");
  return u.toString();
}

export async function exchangeCodeForTokens(params: {
  code: string;
  clientId: string;
  redirectUri: string;
  verifier: string;
}) {
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    code: params.code,
    client_id: params.clientId,
    redirect_uri: params.redirectUri,
    code_verifier: params.verifier,
  });
  const r = await fetch(UPWORK_TOKEN_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    },
    body,
  });
  const json = await r.json().catch(() => ({}));
  return { status: r.status, ok: r.ok, json };
}
