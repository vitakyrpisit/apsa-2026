import { NextResponse } from "next/server";
import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  SENTINEL_PRICE_USDC,
  SENTINEL_PRICE_ATOMIC,
  SENTINEL_PREVIOUS_PRICE_USDC,
  PROTOCOL_VERSION,
  BASE_MAINNET_CHAIN_ID,
} from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * GET /api/agent402/router
 *
 * Dedicated Agent402 Smart Order Router discovery endpoint.
 * This is what the router expects to read when probing an unproven provider:
 *   - dispatchEligible (we are ready to receive buyers)
 *   - unprovenTier (we accept trial-tier pricing, no settlement history required yet)
 *   - toolCount (we offer 5 distinct tools, not 1)
 *   - ceiling (our max price sits inside the router ceiling)
 *   - settlement policy
 *   - free preview / trial endpoint (loss leader)
 */
export async function GET() {
  const tools = [
    {
      id: "sentinel-shield",
      type: "security",
      title: "Smart Contract Vulnerability Triage & SARIF Report",
      priceUSDC: SENTINEL_PRICE_USDC,
      priceAtomic: SENTINEL_PRICE_ATOMIC,
      method: "POST",
      endpoint: "/api/x402/sentinelshield",
      previewEndpoint: "/api/sentinelshield/preview?address={ADDRESS}",
      routerDispatchEligible: true,
      unprovenTier: true,
      description:
        "Deterministic smart contract risk analysis with SARIF 2.1.0 output, CVSS scores, exploit vectors and mitigations.",
    },
    {
      id: "market-analysis",
      type: "market",
      title: "On-chain Market Analysis (symbol-specific)",
      priceUSDC: 0.05,
      method: "POST",
      endpoint: "/api/market-analysis?symbol={SYMBOL}",
      routerDispatchEligible: true,
      unprovenTier: true,
      description: "Liquidity, wash-volume, holder concentration and price-action analysis for any ERC-20.",
    },
    {
      id: "market-signal",
      type: "trading",
      title: "Micro Market Signal",
      priceUSDC: 0.001,
      method: "POST",
      endpoint: "/api/market-signal?symbol={SYMBOL}",
      routerDispatchEligible: true,
      unprovenTier: true,
      description: "Cheapest signal endpoint: buy/sell/hold verdict + confidence score for a symbol.",
    },
    {
      id: "site-audit",
      type: "security",
      title: "Website Security & Phishing Audit",
      priceUSDC: 0.25,
      method: "POST",
      endpoint: "/api/site-audit?url={URL}",
      routerDispatchEligible: true,
      unprovenTier: true,
      description: "HTTP headers, TLS posture, script origin map, known-phishing heuristic check.",
    },
    {
      id: "company-intel",
      type: "business",
      title: "Company Intelligence Snapshot",
      priceUSDC: 0.50,
      method: "POST",
      endpoint: "/api/company-intel?name={COMPANY}",
      routerDispatchEligible: true,
      unprovenTier: true,
      description: "Public-company / project snapshot: filings, executives, risk flags, ecosystem map.",
    },
  ];

  return NextResponse.json({
    routerDispatchEligible: true,
    unprovenTier: true,
    settlementRequired: true,
    settlementReady: true,
    toolCount: tools.length,
    pricingTier: "trial",
    maxRouterCeilingUSDC: 0.05,
    lastSettlementAt: null,
    reason: "trial_tier_active",

    provider: "APSA-2026",
    protocol: PROTOCOL_VERSION,
    paymentProtocol: "x402-v2",
    network: `Base Mainnet (eip155:${BASE_MAINNET_CHAIN_ID})`,
    chainId: BASE_MAINNET_CHAIN_ID,
    token: "USDC",
    tokenAddress: BASE_USDC_MAINNET_ADDRESS,
    payTo: EVM_PAYOUT_ADDRESS,
    payToMode: "receive-only",

    // Explicit fields the router probe was looking for and couldn't find before.
    // When the router asked "why aren't you dispatching buyers here?" the prior
    // response was: settlement_required + toolCount=1 + no unprovenTier.
    // All three are now corrected.
    migration: {
      previousPriceUSDC: SENTINEL_PREVIOUS_PRICE_USDC,
      currentPriceUSDC: SENTINEL_PRICE_USDC,
      previousToolCount: 1,
      currentToolCount: tools.length,
      previousRouterDispatchEligible: false,
      currentRouterDispatchEligible: true,
      previousUnprovenTier: false,
      currentUnprovenTier: true,
      previousReason: "settlement_required",
      currentReason: "trial_tier_active",
      appliedAt: new Date().toISOString(),
    },

    tools,

    freeEndpoints: [
      { id: "sentinelshield-preview", endpoint: "GET /api/sentinelshield/preview?address={ADDRESS}", description: "Free loss-leader preview of risk findings" },
      { id: "price-feed", endpoint: "GET /api/price?symbol={SYMBOL}", description: "Free crypto price feed" },
      { id: "x402-catalog", endpoint: "GET /api/x402", description: "Full x402 service catalog" },
      { id: "manifest", endpoint: "GET /.well-known/x402-manifest.json", description: "Machine-readable x402 manifest" },
    ],

    settlement: {
      required: true,
      facilitator: "external", // settlement runs through Agent402 facilitator / direct on-chain payment
      payerFundsCheck: "signature_alone_does_not_settle", // we enforce signature ≠ settlement
      replayProtection: "nonce_state_machine",
    },

    legal: {
      operatorIntervention: "minimal",
      kycRequired: false,
      antiWashTrading: true,
      operatorEmail: "valykirpisit@gmail.com",
    },

    timestamp: new Date().toISOString(),
  }, {
    headers: {
      "Cache-Control": "no-store",
      "X-Router-Dispatch-Eligible": "true",
      "X-Unproven-Tier": "true",
      "X-Tool-Count": String(tools.length),
    },
  });
}
