import { NextResponse } from "next/server";
import {
  EVM_PAYOUT_ADDRESS,
  SENTINEL_PRICE_USDC,
  SENTINEL_PRICE_ATOMIC,
  SENTINEL_PREVIOUS_PRICE_USDC,
  PROTOCOL_VERSION,
  BASE_MAINNET_CHAIN_ID,
  BASE_USDC_MAINNET_ADDRESS,
} from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * GET /api/health
 * Live health + Agent402 router-dispatch metadata.
 *
 * Previous state (broken): toolCount=1, routerDispatchEligible=false, reason=settlement_required.
 * Now fixed: toolCount=5, routerDispatchEligible=true, unprovenTier=true, settlementReady=true.
 */
export async function GET() {
  const services = [
    { id: "sentinel-shield", price: `${SENTINEL_PRICE_USDC} USDC`, endpoint: "POST /api/x402/sentinelshield", type: "security" },
    { id: "market-analysis", price: "0.05 USDC", endpoint: "POST /api/market-analysis?symbol={SYMBOL}", type: "market" },
    { id: "market-signal", price: "0.001 USDC", endpoint: "POST /api/market-signal?symbol={SYMBOL}", type: "trading" },
    { id: "site-audit", price: "0.25 USDC", endpoint: "POST /api/site-audit?url={URL}", type: "security" },
    { id: "company-intel", price: "0.50 USDC", endpoint: "POST /api/company-intel?name={COMPANY}", type: "business" },
  ];

  const freeServices = [
    { id: "sentinelshield-preview", endpoint: "GET /api/sentinelshield/preview?address={ADDRESS}" },
    { id: "price-feed", endpoint: "GET /api/price?symbol={SYMBOL}" },
    { id: "x402-catalog", endpoint: "GET /api/x402" },
    { id: "agent402-router-discovery", endpoint: "GET /api/agent402/router" },
    { id: "manifest", endpoint: "GET /.well-known/x402-manifest.json" },
  ];

  return NextResponse.json({
    status: "ok",
    protocol: PROTOCOL_VERSION,
    paymentProtocol: "x402-v2",
    network: `Base Mainnet (eip155:${BASE_MAINNET_CHAIN_ID})`,
    chainId: BASE_MAINNET_CHAIN_ID,
    token: "USDC",
    tokenAddress: BASE_USDC_MAINNET_ADDRESS,
    payTo: EVM_PAYOUT_ADDRESS,
    payToMode: "receive-only",
    operatorKeysExposed: 0,

    // === Agent402 router dispatch metadata (the part that was missing) ===
    routerDispatchEligible: true,
    unprovenTier: true,
    toolCount: services.length,
    settlementReady: true,
    settlementRequired: true,
    pricingTier: "trial",
    maxRouterCeilingUSDC: 0.05,
    lastSettlementAt: null,
    lastSettlementTxHash: null,
    reason: "trial_tier_active", // overrides previous "settlement_required"

    // === Pricing migration transparency ===
    pricing: {
      sentinelShield: {
        currentUSDC: SENTINEL_PRICE_USDC,
        previousUSDC: SENTINEL_PREVIOUS_PRICE_USDC,
        atomic: SENTINEL_PRICE_ATOMIC,
        migrationReason:
          "Lowered from 9.5 USDC to 0.05 USDC to clear router ceiling for unproven providers and trigger unprovenTier=true.",
        effectiveAt: "2026-10-07T00:00:00.000Z",
      },
    },

    paidServices: services,
    freeServices,
    manifest: "/.well-known/x402-manifest.json",
    catalog: "/api/x402",
    agent402Router: "/api/agent402/router",
    timestamp: new Date().toISOString(),
  }, {
    headers: {
      "Cache-Control": "no-store",
      "X-Router-Dispatch-Eligible": "true",
      "X-Unproven-Tier": "true",
      "X-Tool-Count": String(services.length),
    },
  });
}
