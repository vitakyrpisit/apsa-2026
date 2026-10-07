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
    priceAtomic: "9500000",
    priceUSDC: SENTINEL_PRICE_USDC,
    payoutAddress: EVM_PAYOUT_ADDRESS,
    payoutAddressMode: "receive-only",
    discovery: {
      protocols: ["x402", "mcp", "openapi-v3"],
      tags: [
        "security",
        "smart-contract-audit",
        "risk-triage",
        "sarif",
        "autonomous-defense",
      ],
      endpoints: {
        analyze: "/api/x402/sentinelshield",
        health: "/api/health",
        manifest: "/.well-known/x402-manifest.json",
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
