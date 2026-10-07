import { NextResponse } from "next/server";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

/**
 * Middleware — content negotiation for x402 discovery crawlers.
 *
 * When a crawler (Agent402, x402scan, Bazaar) requests the root URL with
 * `Accept: application/json` or `?format=json`, returns the x402 service
 * catalog as JSON instead of the HTML dashboard. This fixes the Agent402
 * "Source URL returned HTTP 404" error.
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
        services: [
          {
            serviceId: "sentinel-shield",
            serviceName: "SentinelShield — Smart Contract Risk Triage",
            price: "$9.50 USDC",
            priceAtomic: "9500000",
            method: "POST",
            resource: "/api/x402/sentinelshield",
            tags: ["security", "audit", "sarif", "smart-contract"],
            mimeType: "application/json",
          },
          {
            serviceId: "market-analysis",
            serviceName: "MarketIntelAgent — LLM Market Analysis",
            price: "$0.05 USDC",
            priceAtomic: "50000",
            method: "POST",
            resource: "/api/market-analysis?symbol={SYMBOL}",
            tags: ["market", "analysis", "trading", "llm", "crypto"],
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
          { method: "GET", resource: "/api/price?symbol={SYMBOL}", description: "Free crypto price feed" },
          { method: "GET", resource: "/api/x402", description: "x402 service catalog" },
          { method: "GET", resource: "/api/health", description: "Health check" },
        ],
        discovery: {
          manifest: "/.well-known/x402-manifest.json",
          catalog: "/api/x402",
          openapi: "/openapi.json",
          health: "/api/health",
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
        },
      },
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/"],
};
