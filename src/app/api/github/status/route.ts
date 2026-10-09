import { NextResponse } from "next/server";
import { status as ghStatus } from "@/lib/apsa/github-client";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

/**
 * GET /api/github/status
 * Returns GitHub PAT connection status WITHOUT leaking the token.
 * Mirrors /api/upwork/status pattern.
 */
export async function GET() {
  const s = await ghStatus();
  return NextResponse.json({
    ok: s.connected,
    connected: s.connected,
    reason: s.reason,
    login: s.login,
    account_id: s.account_id,
    public_repos: s.public_repos,
    has_write: s.has_write,
    has_pr_read: s.has_pr_read,
    token_kind: s.token_kind,
    verified_at: s.verified_at,
  });
}
