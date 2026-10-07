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
 * Now includes BOTH services:
 * - SentinelShield (smart contract audit, $9.50)
 * - MarketIntelAgent (market analysis $0.05, trading signals $0.01)
 */
export async function GET() {
  const reqs = generateV2PaymentRequirements("/api/x402/sentinelshield");
  const manifest = {
    x402Version: "2.0",
    protocol: PROTOCOL_VERSION,
    services: [
      {
        serviceId: "sentinel-shield",
        name: "SentinelShield — Smart Contract Risk Triage",
        description: "SARIF vulnerability matrix + exploit remediation for Base smart contracts",
        network: "base-mainnet",
        token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        chainId: BASE_MAINNET_CHAIN_ID,
        priceAtomic: "9500000",
        priceUSDC: SENTINEL_PRICE_USDC,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        payoutAddressMode: "receive-only",
        tags: ["security", "smart-contract-audit", "risk-triage", "sarif"],
        endpoints: {
          paid: "POST /api/x402/sentinelshield",
          free: "GET /api/x402/sentinelshield",
        },
      },
      {
        serviceId: "market-analysis",
        name: "MarketIntelAgent — LLM Market Analysis",
        description: "AI-generated market analysis for BTC, ETH, SOL, TRX, USDC, BASE with directional signal + confidence",
        network: "base-mainnet",
        token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        chainId: BASE_MAINNET_CHAIN_ID,
        priceAtomic: "50000",
        priceUSDC: 0.05,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        payoutAddressMode: "receive-only",
        tags: ["market-data", "analysis", "trading", "crypto", "llm"],
        endpoints: {
          paid: "POST /api/market-analysis?symbol={SYMBOL}",
          free: "GET /api/market-analysis",
        },
        symbols: ["BTC", "ETH", "USDC", "BASE", "SOL", "TRX"],
      },
      {
        serviceId: "market-signal",
        name: "MarketIntelAgent — Trading Signals",
        description: "BUY/SELL/HOLD trading signals with entryPrice, confidence, rationale, 1h expiry",
        network: "base-mainnet",
        token: "USDC",
        tokenAddress: BASE_USDC_MAINNET_ADDRESS,
        chainId: BASE_MAINNET_CHAIN_ID,
        priceAtomic: "10000",
        priceUSDC: 0.01,
        payoutAddress: EVM_PAYOUT_ADDRESS,
        payoutAddressMode: "receive-only",
        tags: ["trading", "signal", "crypto", "market"],
        endpoints: {
          paid: "POST /api/market-signal?symbol={SYMBOL}",
          free: "GET /api/market-signal",
        },
        symbols: ["BTC", "ETH", "USDC", "BASE", "SOL", "TRX"],
      },
    ],
    discovery: {
      protocols: ["x402", "mcp", "openapi-v3"],
      manifest: "/.well-known/x402-manifest.json",
      health: "/api/health",
      agentStatus: "/api/market-intel",
    },
    payoutAddress: EVM_PAYOUT_ADDRESS,
    payoutAddressMode: "receive-only",
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
