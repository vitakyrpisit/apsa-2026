import { NextResponse } from "next/server";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** GET /api/x402 — x402 service catalog for crawlers and discovery */
export async function GET() {
  return NextResponse.json({
    protocol: "x402",
    version: "2.0",
    provider: "APSA-2026",
    payoutAddress: EVM_PAYOUT_ADDRESS,
    payoutMode: "receive-only",
    network: "base-mainnet",
    chainId: 8453,
    token: "USDC",
    tokenAddress: BASE_USDC_MAINNET_ADDRESS,
    services: [
      { id: "sentinel-shield", price: "$9.50", endpoint: "POST /api/x402/sentinelshield", type: "security" },
      { id: "market-analysis", price: "$0.05", endpoint: "POST /api/market-analysis?symbol={SYMBOL}", type: "market" },
      { id: "market-signal", price: "$0.001", endpoint: "POST /api/market-signal?symbol={SYMBOL}", type: "trading" },
      { id: "site-audit", price: "$0.25", endpoint: "POST /api/site-audit?url={URL}", type: "security" },
      { id: "company-intel", price: "$0.50", endpoint: "POST /api/company-intel?name={COMPANY}", type: "business" },
    ],
    freeEndpoints: [
      { endpoint: "GET /api/price?symbol={SYMBOL}", description: "Free crypto price feed" },
      { endpoint: "GET /api/x402", description: "This service catalog" },
      { endpoint: "GET /api/health", description: "Health check" },
    ],
    manifest: "/.well-known/x402-manifest.json",
    discovery: {
      protocols: ["x402", "http-402", "openapi"],
      manifest: "/.well-known/x402-manifest.json",
      catalog: "/api/x402",
      health: "/api/health",
    },
  });
}
