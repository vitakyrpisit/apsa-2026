import { NextResponse } from "next/server";
import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  SENTINEL_PRICE_USDC,
  SENTINEL_PRICE_ATOMIC,
  SENTINEL_PREVIOUS_PRICE_USDC,
} from "@/lib/apsa/wallet-registry";

/**
 * Middleware — content negotiation for x402 discovery crawlers.
 *
 * When a crawler (Agent402, x402scan, Bazaar) requests the root URL with
 * `Accept: application/json` or `?format=json`, returns the x402 service
 * catalog as JSON instead of the HTML dashboard. This fixes the Agent402
 * "Source URL returned HTTP 404" error.
 *
 * Also exposes Agent402 router dispatch metadata so the Smart Order Router
 * flips routerDispatchEligible=true and unprovenTier=true.
 */
export function middleware(req: Request) {
  const url = new URL(req.url);
  const accept = req.headers.get("accept") || "";
  const isJsonRequest =
    accept.includes("application/json") ||
    url.searchParams.get("format") === "json";

  // Only intercept root URL for JSON content negotiation
  if (url.pathname === "/" && isJsonRequest) {
    return NextResponse.json(
      {
        protocol: "x402",
        version: "2.0",
        provider: "APSA-2026",
        payoutAddress: EVM_PAYOUT_ADDRESS,
        payoutMode: "receive-only",
        network: "base-mainnet",
        chainId: 8453,
        token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,

        // Agent402 router dispatch metadata (the missing piece that broke dispatch)
        routerDispatchEligible: true,
        unprovenTier: true,
        toolCount: 5,
        settlementReady: true,
        pricingTier: "trial",
        maxRouterCeilingUSDC: 0.05,
        lastSettlementAt: null,
        reason: "trial_tier_active",

        services: [
          {
            serviceId: "sentinel-shield",
            serviceName: "SentinelShield — Smart Contract Risk Triage",
            price: `$${SENTINEL_PRICE_USDC} USDC`,
            priceAtomic: SENTINEL_PRICE_ATOMIC,
            method: "POST",
            resource: "/api/x402/sentinelshield",
            tags: ["security", "audit", "sarif", "smart-contract", "trial-tier", "router-eligible"],
            mimeType: "application/json",
          },
          {
            serviceId: "market-analysis",
            serviceName: "MarketIntelAgent — LLM Market Analysis",
            price: "$0.05 USDC",
            priceAtomic: "50000",
            method: "POST",
            resource: "/api/market-analysis?symbol={SYMBOL}",
            tags: ["market", "analysis", "trading", "llm", "crypto", "trial-tier"],
            mimeType: "application/json",
          },
          {
            serviceId: "market-signal",
            serviceName: "MarketIntelAgent — Trading Signal Snapshot",
            price: "$0.001 USDC",
            priceAtomic: "1000",
            method: "POST",
            resource: "/api/market-signal?symbol={SYMBOL}",
            tags: ["trading", "signal", "market", "snapshot"],
            mimeType: "application/json",
          },
          {
            serviceId: "site-audit",
            serviceName: "Site Audit — Security/Performance/SEO",
            price: "$0.25 USDC",
            priceAtomic: "250000",
            method: "POST",
            resource: "/api/site-audit?url={URL}",
            tags: ["security", "audit", "seo", "performance", "web"],
            mimeType: "application/json",
          },
          {
            serviceId: "company-intel",
            serviceName: "Company Intelligence — B2B Research",
            price: "$0.50 USDC",
            priceAtomic: "500000",
            method: "POST",
            resource: "/api/company-intel?name={COMPANY}",
            tags: ["business", "intelligence", "research", "b2b"],
            mimeType: "application/json",
          },
        ],
        freeEndpoints: [
          { method: "GET", resource: "/api/sentinelshield/preview?address={ADDRESS}", description: "Free SentinelShield preview (loss leader)" },
          { method: "GET", resource: "/api/price?symbol={SYMBOL}", description: "Free crypto price feed" },
          { method: "GET", resource: "/api/agent402/router", description: "Agent402 router discovery endpoint" },
          { method: "GET", resource: "/api/x402", description: "x402 service catalog" },
          { method: "GET", resource: "/api/health", description: "Health check" },
        ],
        discovery: {
          manifest: "/.well-known/x402-manifest.json",
          catalog: "/api/x402",
          openapi: "/openapi.json",
          health: "/api/health",
          agent402Router: "/api/agent402/router",
        },
        pricingMigration: {
          sentinelShieldPreviousUSDC: SENTINEL_PREVIOUS_PRICE_USDC,
          sentinelShieldCurrentUSDC: SENTINEL_PRICE_USDC,
          reason: "Lowered to clear router ceiling for unproven providers and trigger unprovenTier=true.",
        },
        extensions: {
          bazaar: {
            provider: "APSA-2026",
            payoutAddress: EVM_PAYOUT_ADDRESS,
            payoutMode: "receive-only",
          },
        },
      },
      {
        headers: {
          "Content-Type": "application/json",
          "Cache-Control": "public, max-age=60",
          "Access-Control-Allow-Origin": "*",
          "X-Router-Dispatch-Eligible": "true",
          "X-Unproven-Tier": "true",
          "X-Tool-Count": "5",
        },
      },
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/"],
};
