import { NextResponse } from "next/server";
import { generateV2PaymentRequirements } from "@/lib/apsa/x402-core";
import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  SENTINEL_PRICE_USDC,
  BASE_MAINNET_CHAIN_ID,
  PROTOCOL_VERSION,
} from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * GET /.well-known/x402-manifest.json
 * Machine-readable discovery document for autonomous buyer agents.
 */
export async function GET() {
  const reqs = generateV2PaymentRequirements("/api/x402/sentinelshield");
  const manifest = {
    x402Version: "2.0",
    protocol: PROTOCOL_VERSION,
    serviceId: "sentinel-shield",
    name: "SentinelShield Autonomous Risk & Threat Matrix",
    network: "base-mainnet",
    token: "USDC",
    tokenAddress: BASE_USDC_MAINNET_ADDRESS,
    chainId: BASE_MAINNET_CHAIN_ID,
    priceAtomic: SENTINEL_PRICE_ATOMIC,
    priceUSDC: SENTINEL_PRICE_USDC,
    pricingTier: "trial",
    routerDispatchEligible: true,
    unprovenTier: true,
    maxRouterCeilingUSDC: 0.05,
    payoutAddress: EVM_PAYOUT_ADDRESS,
    payoutAddressMode: "receive-only",
    services: [
      { id: "sentinel-shield", priceUSDC: 0.05, endpoint: "POST /api/x402/sentinelshield", type: "security" },
      { id: "market-analysis", priceUSDC: 0.05, endpoint: "POST /api/market-analysis?symbol={SYMBOL}", type: "market" },
      { id: "market-signal", priceUSDC: 0.001, endpoint: "POST /api/market-signal?symbol={SYMBOL}", type: "trading" },
      { id: "site-audit", priceUSDC: 0.25, endpoint: "POST /api/site-audit?url={URL}", type: "security" },
      { id: "company-intel", priceUSDC: 0.50, endpoint: "POST /api/company-intel?name={COMPANY}", type: "business" },
    ],
    discovery: {
      protocols: ["x402", "mcp", "openapi-v3", "agent402-router"],
      tags: [
        "security",
        "smart-contract-audit",
        "risk-triage",
        "sarif",
        "autonomous-defense",
        "trial-tier",
        "router-eligible",
      ],
      endpoints: {
        analyze: "/api/x402/sentinelshield",
        health: "/api/health",
        manifest: "/.well-known/x402-manifest.json",
        agent402Router: "/api/agent402/router",
        catalog: "/api/x402",
      },
      router: {
        dispatchEligible: true,
        unprovenTier: true,
        toolCount: 5,
        settlementRequired: true,
        ceilingUSDC: 0.05,
      },
    },
    paymentRequirements: reqs,
    legal: {
      operatorIntervention: "minimal",
      kycRequired: false,
      antiWashTrading: true,
    },
    generatedAt: new Date().toISOString(),
  };

  return NextResponse.json(manifest, {
    headers: {
      "Cache-Control": "public, max-age=60",
      "Content-Type": "application/json",
    },
  });
}
