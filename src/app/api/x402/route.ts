import { NextResponse } from "next/server";
import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  SENTINEL_PRICE_USDC,
  SENTINEL_PREVIOUS_PRICE_USDC,
  PROTOCOL_VERSION,
  BASE_MAINNET_CHAIN_ID,
} from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** GET /api/x402 — x402 service catalog for crawlers, buyers, and Agent402 router discovery */
export async function GET() {
  const services = [
    { id: "sentinel-shield", price: "$0.05", priceUSDC: 0.05, endpoint: "POST /api/x402/sentinelshield", type: "security" },
    { id: "market-analysis", price: "$0.05", priceUSDC: 0.05, endpoint: "POST /api/market-analysis?symbol={SYMBOL}", type: "market" },
    { id: "market-signal", price: "$0.001", priceUSDC: 0.001, endpoint: "POST /api/market-signal?symbol={SYMBOL}", type: "trading" },
    { id: "site-audit", price: "$0.25", priceUSDC: 0.25, endpoint: "POST /api/site-audit?url={URL}", type: "security" },
    { id: "company-intel", price: "$0.50", priceUSDC: 0.50, endpoint: "POST /api/company-intel?name={COMPANY}", type: "business" },
  ];

  return NextResponse.json({
    protocol: "x402",
    version: "2.0",
    provider: "APSA-2026",
    protocolVersion: PROTOCOL_VERSION,
    payoutAddress: EVM_PAYOUT_ADDRESS,
    payoutMode: "receive-only",
    network: "base-mainnet",
    chainId: BASE_MAINNET_CHAIN_ID,
    token: "USDC",
    tokenAddress: BASE_USDC_MAINNET_ADDRESS,

    // Router dispatch metadata
    routerDispatchEligible: true,
    unprovenTier: true,
    toolCount: services.length,
    settlementReady: true,
    pricingTier: "trial",
    maxRouterCeilingUSDC: 0.05,

    services,
    freeEndpoints: [
      { endpoint: "GET /api/sentinelshield/preview?address={ADDRESS}", description: "Free smart contract risk preview" },
      { endpoint: "GET /api/price?symbol={SYMBOL}", description: "Free crypto price feed" },
      { endpoint: "GET /api/x402", description: "This service catalog" },
      { endpoint: "GET /api/agent402/router", description: "Agent402 router discovery endpoint" },
      { endpoint: "GET /api/health", description: "Health check + router dispatch metadata" },
    ],

    manifest: "/.well-known/x402-manifest.json",
    discovery: {
      protocols: ["x402", "http-402", "openapi", "agent402-router"],
      manifest: "/.well-known/x402-manifest.json",
      catalog: "/api/x402",
      health: "/api/health",
      agent402Router: "/api/agent402/router",
    },

    pricingMigration: {
      sentinelShieldPreviousUSDC: SENTINEL_PREVIOUS_PRICE_USDC,
      sentinelShieldCurrentUSDC: SENTINEL_PRICE_USDC,
      reason: "Lowered to clear router ceiling for unproven providers and trigger unprovenTier=true.",
    },
  });
}
