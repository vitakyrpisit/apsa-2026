import { NextResponse } from "next/server";
import {
  EVM_PAYOUT_ADDRESS,
  SENTINEL_PRICE_USDC,
  PROTOCOL_VERSION,
  BASE_MAINNET_CHAIN_ID,
} from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** GET /api/health — free uptime/readiness probe, no payment required. */
export async function GET() {
  return NextResponse.json(
    {
      status: "ok",
      protocol: PROTOCOL_VERSION,
      paymentProtocol: "x402-v2",
      network: `Base Mainnet (eip155:${BASE_MAINNET_CHAIN_ID})`,
      services: [
        { id: "sentinel-shield", price: `${SENTINEL_PRICE_USDC.toFixed(2)} USDC`, endpoint: "POST /api/x402/sentinelshield" },
        { id: "market-analysis", price: "0.05 USDC", endpoint: "POST /api/market-analysis?symbol={SYMBOL}" },
        { id: "market-signal", price: "0.01 USDC", endpoint: "POST /api/market-signal?symbol={SYMBOL}" },
      ],
      payTo: EVM_PAYOUT_ADDRESS,
      payToMode: "receive-only",
      operatorKeysExposed: 0,
      manifest: "/.well-known/x402-manifest.json",
      agentStatus: "/api/market-intel",
      timestamp: new Date().toISOString(),
    },
    { headers: { "Cache-Control": "no-store" } },
  );
}
