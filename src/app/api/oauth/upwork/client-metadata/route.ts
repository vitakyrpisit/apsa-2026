import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * RFC 7592-style OAuth 2.0 Client Metadata Document for Upwork MCP.
 * Upwork's authorization server supports client_id_metadata_document (see
 * https://mcp.upwork.com/.well-known/oauth-authorization-server).
 * This document IS our client_id: we pass this URL as `client_id` in the
 * authorization request. Upwork fetches it and reads redirect_uris etc.
 */
export async function GET(req: Request) {
  const url = new URL(req.url);
  // Base URL of THIS deployment (works both on localhost and Vercel)
  const base = process.env.PUBLIC_BASE_URL || `${url.protocol}//${url.host}`;
  const localhostRedirect = "http://localhost:3000/api/oauth/upwork/callback";
  const primaryRedirect = `${base}/api/oauth/upwork/callback`;
  const redirect_uris = [...new Set([primaryRedirect, localhostRedirect])];

  const doc = {
    client_id: `${base}/api/oauth/upwork/client-metadata`,
    client_name: "APSA-2026 SentinelShield BugFixer",
    client_uri: base,
    contacts: ["apsa-2026@proton.me"],
    tos_uri: `${base}/`,
    policy_uri: `${base}/`,
    redirect_uris,
    grant_types: ["authorization_code", "refresh_token"],
    response_types: ["code"],
    token_endpoint_auth_method: "none",
    scope: "mcp",
    software_id: "apsa-2026-bugfixer",
    software_version: "1.0.0",
  };

  return NextResponse.json(doc, {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
