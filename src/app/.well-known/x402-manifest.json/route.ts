import { NextResponse } from "next/server";
import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  SENTINEL_PRICE_USDC,
  SENTINEL_PRICE_ATOMIC,
  SENTINEL_PREVIOUS_PRICE_USDC,
  BASE_MAINNET_CHAIN_ID,
  PROTOCOL_VERSION,
} from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  const manifest = {
    x402Version: "2.0",
    protocol: PROTOCOL_VERSION,
    routerDispatchEligible: true,
    unprovenTier: true,
    toolCount: 5,
    settlementReady: true,
    pricingTier: "trial",
    maxRouterCeilingUSDC: 0.05,
    pricingMigration: {
      sentinelShieldPreviousUSDC: SENTINEL_PREVIOUS_PRICE_USDC,
      sentinelShieldCurrentUSDC: SENTINEL_PRICE_USDC,
      reason: "Lowered to clear router ceiling for unproven providers and trigger unprovenTier=true.",
    },
    services: [
      {
        serviceId: "sentinel-shield",
        name: "SentinelShield — Smart Contract Risk Triage",
        priceUSDC: SENTINEL_PRICE_USDC, // 0.05 trial tier (was 9.5)
        priceAtomic: SENTINEL_PRICE_ATOMIC, // "50000"
        pricingTier: "trial",
        routerDispatchEligible: true,
        unprovenTier: true,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        network: "base-mainnet", token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        endpoints: { paid: "POST /api/x402/sentinelshield", free: "GET /api/sentinelshield/preview?address={ADDRESS}" },
        tags: ["security", "audit", "sarif", "trial-tier", "router-eligible"],
      },
      {
        serviceId: "market-analysis",
        name: "MarketIntelAgent — LLM Market Analysis",
        priceUSDC: 0.05, priceAtomic: "50000",
        routerDispatchEligible: true,
        unprovenTier: true,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        network: "base-mainnet", token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        endpoints: { paid: "POST /api/market-analysis?symbol={SYMBOL}", free: "GET /api/market-analysis" },
        tags: ["market", "analysis", "trading", "llm", "trial-tier"],
        symbols: ["BTC", "ETH", "USDC", "BASE", "SOL", "TRX"],
      },
      {
        serviceId: "market-signal",
        name: "MarketIntelAgent — Trading Signals",
        priceUSDC: 0.001, priceAtomic: "1000",
        routerDispatchEligible: true,
        unprovenTier: true,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        network: "base-mainnet", token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        endpoints: { paid: "POST /api/market-signal?symbol={SYMBOL}", free: "GET /api/market-signal" },
        tags: ["trading", "signal"],
        symbols: ["BTC", "ETH", "USDC", "BASE", "SOL", "TRX"],
      },
      {
        serviceId: "site-audit",
        name: "Site Audit — Security, Performance, SEO",
        priceUSDC: 0.25, priceAtomic: "250000",
        routerDispatchEligible: true,
        unprovenTier: true,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        network: "base-mainnet", token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        endpoints: { paid: "POST /api/site-audit?url={URL}", free: "GET /api/site-audit" },
        tags: ["security", "audit", "seo", "performance"],
      },
      {
        serviceId: "company-intel",
        name: "Company Intelligence — B2B Research",
        priceUSDC: 0.50, priceAtomic: "500000",
        routerDispatchEligible: true,
        unprovenTier: true,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        network: "base-mainnet", token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        endpoints: { paid: "POST /api/company-intel?name={COMPANY}", free: "GET /api/company-intel" },
        tags: ["business", "intelligence", "research", "b2b"],
      },
    ],
    payoutAddress: EVM_PAYOUT_ADDRESS,
    payoutAddressMode: "receive-only",
    chainId: BASE_MAINNET_CHAIN_ID,
    discovery: {
      manifest: "/.well-known/x402-manifest.json",
      catalog: "/api/x402",
      health: "/api/health",
      agent402Router: "/api/agent402/router",
      freePriceFeed: "/api/price?symbol={SYMBOL}",
    },
    freeEndpoints: [
      { method: "GET", resource: "/api/sentinelshield/preview?address={ADDRESS}", description: "Free smart contract risk preview (loss leader → paid full report)" },
      { endpoint: "GET /api/price?symbol={SYMBOL}", description: "Free crypto price feed (no payment)" },
      { endpoint: "GET /api/agent402/router", description: "Agent402 router discovery endpoint" },
      { endpoint: "GET /api/x402", description: "x402 service catalog" },
      { endpoint: "GET /api/health", description: "Health check + router dispatch metadata" },
    ],
    generatedAt: new Date().toISOString(),
  };

  return NextResponse.json(manifest, {
    headers: {
      "Cache-Control": "public, max-age=60",
      "Content-Type": "application/json",
      "X-Router-Dispatch-Eligible": "true",
      "X-Unproven-Tier": "true",
      "X-Tool-Count": "5",
    },
  });
}
