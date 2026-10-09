import { NextResponse } from "next/server";
import {
  loadStateFile,
  saveStateFile,
  saveCreds,
  exchangeCodeForTokens,
  UPWORK_MCP_URL,
} from "@/lib/apsa/upwork-oauth";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Step 2 of the Upwork MCP OAuth flow (redirect_uri target).
 * Upwork redirects here with ?code=...&state=...
 * We validate state against the stored pending flow, exchange the code for
 * tokens (public client — no secret), persist credentials (3 locations),
 * and show a human-friendly confirmation page.
 *
 * GET /api/oauth/upwork/callback?code=...&state=...
 */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const error = url.searchParams.get("error");

  if (error) {
    return new NextResponse(
      `<html><body style="font-family:sans-serif;background:#0a0f1e;color:#f87171;padding:40px"><h1>Upwork OAuth denied</h1><p>${error}</p><p>${url.searchParams.get("error_description") || ""}</p><a style="color:#38bdf8" href="/api/oauth/upwork/authorize">Start over</a></body></html>`,
      { headers: { "Content-Type": "text/html" } },
    );
  }
  if (!code || !state) {
    return new NextResponse(
      `<html><body style="font-family:sans-serif;background:#0a0f1e;color:#fbbf24;padding:40px"><h1>Missing code/state</h1><p>Open /api/oauth/upwork/authorize first, then approve in Upwork.</p></body></html>`,
      { headers: { "Content-Type": "text/html" } },
    );
  }

  const pending = await loadStateFile<{
    state: string;
    verifier: string;
    redirect_uri: string;
    client_id: string;
    used: boolean;
  }>();

  if (!pending) {
    return new NextResponse(
      `<html><body style="font-family:sans-serif;background:#0a0f1e;color:#fbbf24;padding:40px"><h1>No pending OAuth flow</h1><p>Open /api/oauth/upwork/authorize first.</p></body></html>`,
      { headers: { "Content-Type": "text/html" } },
    );
  }
  if (pending.state !== state) {
    return new NextResponse(
      `<html><body style="font-family:sans-serif;background:#0a0f1e;color:#f87171;padding:40px"><h1>State mismatch (CSRF guard)</h1><p>Start a fresh flow: /api/oauth/upwork/authorize</p></body></html>`,
      { headers: { "Content-Type": "text/html" } },
    );
  }
  if (pending.used) {
    return new NextResponse(
      `<html><body style="font-family:sans-serif;background:#0a0f1e;color:#fbbf24;padding:40px"><h1>Code already used</h1><p>Start a fresh flow: /api/oauth/upwork/authorize</p></body></html>`,
      { headers: { "Content-Type": "text/html" } },
    );
  }

  const { status, ok, json } = await exchangeCodeForTokens({
    code,
    clientId: pending.client_id,
    redirectUri: pending.redirect_uri,
    verifier: pending.verifier,
  });

  await saveStateFile({ ...pending, used: true });

  if (!ok || !json.access_token) {
    return new NextResponse(
      `<html><body style="font-family:sans-serif;background:#0a0f1e;color:#f87171;padding:40px"><h1>Token exchange failed (HTTP ${status})</h1><pre style="white-space:pre-wrap">${JSON.stringify(json, null, 2).slice(0, 2000)}</pre><p>Start over: <a style="color:#38bdf8" href="/api/oauth/upwork/authorize">/api/oauth/upwork/authorize</a></p></body></html>`,
      { headers: { "Content-Type": "text/html" } },
    );
  }

  await saveCreds({
    platform: "Upwork MCP",
    mcp_endpoint: UPWORK_MCP_URL,
    access_token: json.access_token,
    refresh_token: json.refresh_token,
    token_type: json.token_type,
    expires_at: json.expires_in
      ? new Date(Date.now() + Number(json.expires_in) * 1000).toISOString()
      : undefined,
    scope: json.scope,
    obtained_at: new Date().toISOString(),
  });

  return new NextResponse(
    `<html><body style="font-family:sans-serif;background:#0a0f1e;color:#34d399;padding:40px"><h1>✓ Upwork MCP CONNECTED</h1><p>Access token stored (3 locations, mode 600). Scope: ${json.scope || "mcp"}.</p><p>The agent can now call <code>https://mcp.upwork.com/mcp</code>. Check status: <a style="color:#38bdf8" href="/api/oauth/upwork/status">/api/oauth/upwork/status</a></p><p style="color:#94a3b8">You can close this tab. The scanner will pick Upwork up automatically.</p></body></html>`,
    { headers: { "Content-Type": "text/html" } },
  );
}
