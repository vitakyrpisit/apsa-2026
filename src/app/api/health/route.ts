import { NextResponse } from "next/server";
import { EVM_PAYOUT_ADDRESS, SENTINEL_PRICE_USDC, PROTOCOL_VERSION, BASE_MAINNET_CHAIN_ID } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json({
    status: "ok",
    protocol: PROTOCOL_VERSION,
    paymentProtocol: "x402-v2",
    network: `Base Mainnet (eip155:${BASE_MAINNET_CHAIN_ID})`,
    paidServices: [
      { id: "sentinel-shield", price: `${SENTINEL_PRICE_USDC} USDC`, endpoint: "POST /api/x402/sentinelshield" },
      { id: "market-analysis", price: "0.05 USDC", endpoint: "POST /api/market-analysis?symbol={SYMBOL}" },
      { id: "market-signal", price: "0.001 USDC", endpoint: "POST /api/market-signal?symbol={SYMBOL}" },
      { id: "site-audit", price: "0.25 USDC", endpoint: "POST /api/site-audit?url={URL}" },
      { id: "company-intel", price: "0.50 USDC", endpoint: "POST /api/company-intel?name={COMPANY}" },
    ],
    freeServices: [
      { id: "price-feed", endpoint: "GET /api/price?symbol={SYMBOL}" },
      { id: "x402-catalog", endpoint: "GET /api/x402" },
      { id: "manifest", endpoint: "GET /.well-known/x402-manifest.json" },
    ],
    payTo: EVM_PAYOUT_ADDRESS,
    payToMode: "receive-only",
    operatorKeysExposed: 0,
    manifest: "/.well-known/x402-manifest.json",
    catalog: "/api/x402",
    timestamp: new Date().toISOString(),
  }, { headers: { "Cache-Control": "no-store" } });
}
