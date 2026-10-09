// GET /api/upwork/status
// Reports OAuth state + tries a minimal MCP call to confirm tokens work.

import { NextResponse } from "next/server";
import { loadTokens, callUpworkMcp } from "@/lib/apsa/upwork-oauth";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  const tokens = await loadTokens();
  if (!tokens) {
    return NextResponse.json({
      ok: false,
      connected: false,
      reason: "no_tokens",
      next_step: "GET /api/upwork/oauth/authorize — open the returned URL in browser",
    });
  }

  const expiresAt = new Date(tokens.expires_at).getTime();
  const ttlSec = Math.max(0, Math.floor((expiresAt - Date.now()) / 1000));
  const isExpired = ttlSec === 0 && !tokens.refresh_token;
  const isExpiringSoon = ttlSec < 60 && !!tokens.refresh_token;

  return NextResponse.json({
    ok: true,
    connected: !isExpired,
    obtained_at: tokens.obtained_at,
    expires_at: tokens.expires_at,
    ttl_seconds: ttlSec,
    has_refresh: !!tokens.refresh_token,
    expiring_soon: isExpiringSoon,
    scope: tokens.scope,
    next_step: isExpired
      ? "re-authorize at GET /api/upwork/oauth/authorize"
      : isExpiringSoon
        ? "will auto-refresh on next call"
        : "ready to call MCP tools",
  });
}
