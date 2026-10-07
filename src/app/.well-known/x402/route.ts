import { NextResponse } from "next/server";
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** GET /.well-known/x402 — x402scan-compatible discovery endpoint */
export async function GET() {
  return NextResponse.json({
    protocol: "x402",
    version: "2.0",
    manifest: "/.well-known/x402-manifest.json",
    catalog: "/api/x402",
    openapi: "/openapi.json",
    health: "/api/health",
    root: "/?format=json",
  }, { headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=60" } });
}
