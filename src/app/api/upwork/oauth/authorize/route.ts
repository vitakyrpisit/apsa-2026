// GET /api/upwork/oauth/authorize
// Generates a PKCE pair + state, persists it, returns the Upwork Authorize URL
// for the operator (or any human) to click. After Upwork redirects back to
// /api/upwork/oauth/callback, the tokens are stored server-side.
//
// Query: ?next=/dashboard  (optional landing page after success)

import { NextResponse } from "next/server";
import { randomBytes } from "node:crypto";
import {
  UPWORK,
  UPWORK_CLIENT_ID,
  UPWORK_REDIRECT_URI,
  makePkcePair,
  savePendingPkce,
} from "@/lib/apsa/upwork-oauth";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(req: Request) {
  if (!UPWORK_CLIENT_ID) {
    return NextResponse.json(
      {
        ok: false,
        error: "missing_env",
        message:
          "Set UPWORK_CLIENT_ID + UPWORK_CLIENT_SECRET + UPWORK_REDIRECT_URI in .env.local. Register an app at https://www.upwork.com/developer and use https://apsa-2026.vercel.app/api/upwork/oauth/callback as the redirect URI.",
      },
      { status: 503 },
    );
  }

  const url = new URL(req.url);
  const next = url.searchParams.get("next") || "/?tab=marketplaces";
  const state = randomBytes(16).toString("hex");
  const { verifier, challenge } = makePkcePair();

  await savePendingPkce(state, verifier, next);

  const authUrl = new URL(UPWORK.AUTHORIZE);
  authUrl.searchParams.set("response_type", "code");
  authUrl.searchParams.set("client_id", UPWORK_CLIENT_ID);
  authUrl.searchParams.set("redirect_uri", UPWORK_REDIRECT_URI);
  authUrl.searchParams.set("code_challenge", challenge);
  authUrl.searchParams.set("code_challenge_method", "S256");
  authUrl.searchParams.set("state", state);

  return NextResponse.json({
    ok: true,
    authorize_url: authUrl.toString(),
    state,
    redirect_uri: UPWORK_REDIRECT_URI,
    instructions:
      "Open authorize_url in a browser, log in to Upwork, click Authorize. You will be redirected back to redirect_uri and tokens will be stored server-side. After success, call GET /api/upwork/status to verify.",
  });
}
