import { NextResponse } from "next/server";
import { loadCreds } from "@/lib/apsa/upwork-oauth";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Upwork MCP connection status.
 * NEVER returns the access token — only presence/expiry metadata.
 */
export async function GET() {
  const creds = await loadCreds();
  if (!creds) {
    return NextResponse.json(
      {
        connected: false,
        mcp_endpoint: "https://mcp.upwork.com/mcp",
        next_step: "GET /api/oauth/upwork/authorize → open authorization_url in browser",
      },
      { headers: { "Cache-Control": "no-store" } },
    );
  }
  const expiresAt = creds.expires_at ? new Date(creds.expires_at) : null;
  const expired = expiresAt ? expiresAt.getTime() < Date.now() : false;
  return NextResponse.json(
    {
      connected: true,
      expired,
      scope: creds.scope,
      obtained_at: creds.obtained_at,
      expires_at: creds.expires_at,
      has_refresh_token: !!creds.refresh_token,
      token_prefix: `${creds.access_token.slice(0, 6)}…`,
      mcp_endpoint: creds.mcp_endpoint,
    },
    { headers: { "Cache-Control": "no-store" } },
  );
}
