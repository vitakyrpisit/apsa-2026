// GET /api/upwork/oauth/callback?code=...&state=...
// OAuth 2.1 callback. Upwork redirects here after the operator authorizes.
// Exchanges code+verifier for tokens, stores them, redirects to ?next= page.

import { NextResponse } from "next/server";
import {
  UPWORK,
  UPWORK_CLIENT_ID,
  UPWORK_CLIENT_SECRET,
  UPWORK_REDIRECT_URI,
  loadAndClearPendingPkce,
  saveTokens,
  type UpworkTokens,
} from "@/lib/apsa/upwork-oauth";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(req: Request) {
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const error = url.searchParams.get("error");
  const errorDesc = url.searchParams.get("error_description");

  if (error) {
    return NextResponse.json(
      { ok: false, error, message: errorDesc || "Upwork returned an error" },
      { status: 400 },
    );
  }
  if (!code || !state) {
    return NextResponse.json(
      { ok: false, error: "missing_params", message: "code and state are required" },
      { status: 400 },
    );
  }

  const pending = await loadAndClearPendingPkce(state);
  if (!pending) {
    return NextResponse.json(
      {
        ok: false,
        error: "invalid_state",
        message:
          "PKCE verifier not found for this state. Restart the flow at GET /api/upwork/oauth/authorize.",
      },
      { status: 400 },
    );
  }

  // Exchange code + verifier for tokens
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    code,
    redirect_uri: UPWORK_REDIRECT_URI,
    client_id: UPWORK_CLIENT_ID,
    client_secret: UPWORK_CLIENT_SECRET,
    code_verifier: pending.verifier,
  });

  const tokenRes = await fetch(UPWORK.TOKEN, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
    cache: "no-store",
  });

  if (!tokenRes.ok) {
    const errText = await tokenRes.text();
    return NextResponse.json(
      {
        ok: false,
        error: "token_exchange_failed",
        status: tokenRes.status,
        message: errText.slice(0, 500),
      },
      { status: 502 },
    );
  }

  const tk = (await tokenRes.json()) as Record<string, string | number>;
  const tokens: UpworkTokens = {
    access_token: String(tk.access_token),
    refresh_token: (tk.refresh_token as string) || null,
    token_type: (tk.token_type as string) || "Bearer",
    expires_at: new Date(
      Date.now() + Number(tk.expires_in ?? 3600) * 1000,
    ).toISOString(),
    scope: (tk.scope as string) || "",
    obtained_at: new Date().toISOString(),
  };
  await saveTokens(tokens);

  // Redirect to the next page (browser-visible success)
  return NextResponse.redirect(new URL(pending.next, url.origin));
}
