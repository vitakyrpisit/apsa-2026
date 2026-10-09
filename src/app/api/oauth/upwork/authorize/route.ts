import { NextResponse } from "next/server";
import { randomBytes } from "node:crypto";
import {
  pkcePair,
  saveStateFile,
  buildAuthorizeUrl,
  UPWORK_SCOPE,
} from "@/lib/apsa/upwork-oauth";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Step 1 of the Upwork MCP OAuth flow.
 * GET /api/oauth/upwork/authorize
 * → creates PKCE pair + state, persists them, returns { authorization_url }.
 * Operator opens authorization_url in their browser, logs in to Upwork, approves.
 * Upwork redirects to /api/oauth/upwork/callback?code=...&state=...
 *
 * Optional query param: ?redirect_uri=... override (must be listed in the
 * client metadata document). Default: <this origin>/api/oauth/upwork/callback
 */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const base = process.env.PUBLIC_BASE_URL || `${url.protocol}//${url.host}`;
  const redirectUri =
    url.searchParams.get("redirect_uri") || `${base}/api/oauth/upwork/callback`;

  const { verifier, challenge } = pkcePair();
  const state = randomBytes(24).toString("base64url");

  // Public client_id = the metadata document URL served by this deployment.
  // Prefer the PUBLIC (Vercel) URL when configured, so Upwork can fetch it.
  const publicBase = process.env.PUBLIC_BASE_URL || base;
  const clientId = `${publicBase}/api/oauth/upwork/client-metadata`;

  await saveStateFile({
    created_at: new Date().toISOString(),
    state,
    verifier,
    redirect_uri: redirectUri,
    client_id: clientId,
    used: false,
  });

  const authorization_url = buildAuthorizeUrl({
    clientId,
    redirectUri,
    challenge,
    state,
  });

  return NextResponse.json({
    ok: true,
    authorization_url,
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: UPWORK_SCOPE,
    instructions: [
      "1. Open authorization_url in a normal browser (operator action).",
      "2. Log in to Upwork and approve the APSA-2026 client.",
      "3. Upwork redirects to our callback — the token exchange happens automatically.",
      "4. Check GET /api/oauth/upwork/status — it must show connected: true.",
    ],
  });
}
