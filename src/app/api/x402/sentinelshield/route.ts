import { NextResponse } from "next/server";
import {
  processPayment,
  buildPaymentRequirements,
  extractPaymentPayload,
  type PaymentRequirements,
} from "@/lib/apsa/payai-facilitator";
import { analyzeContractRisk } from "@/lib/apsa/sentinel-shield";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS, SENTINEL_PRICE_ATOMIC } from "@/lib/apsa/wallet-registry";
import { handleX402Payment, build402Response, build200Response, type X402ServiceConfig, X402Error } from "@/lib/apsa/x402-handler";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const SERVICE: X402ServiceConfig = {
  serviceId: "sentinel-shield",
  serviceName: "SentinelShield",
  description: "Smart contract security preflight — check if a contract is safe before your agent interacts with it",
  resource: "/api/x402/sentinelshield",
  priceUSDC: 9.5,
  amountAtomic: SENTINEL_PRICE_ATOMIC,
  tags: ["security", "audit", "smart-contract", "risk", "preflight", "sarif", "base", "arbitrum", "polygon", "avalanche", "evm"],
  mimeType: "application/json",
};

export async function POST(req: Request) {
  let body: unknown = null;
  try { body = await req.json(); } catch { body = null; }

  const input = (body as { chain?: string; contractAddress?: string }) || {};
  const targetContract = input.contractAddress || BASE_USDC_MAINNET_ADDRESS;
  const preview = { service: SERVICE.serviceName, targetContract };

  try {
    const settlement = await handleX402Payment(req, body, SERVICE, preview);
    if (!settlement) return build402Response(SERVICE, preview);

    const outcome = await analyzeContractRisk({
      chain: "base",
      contractAddress: targetContract,
    });

    return build200Response(SERVICE, outcome, settlement);
  } catch (e) {
    if (e instanceof X402Error) return NextResponse.json(e.body, { status: e.statusCode });
    throw e;
  }
}

export async function GET() {
  return NextResponse.json({
    service: SERVICE.serviceName,
    version: "2.0.0",
    resource: SERVICE.resource,
    method: "POST",
    price: `$${SERVICE.priceUSDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base",
    facilitator: "https://facilitator.payai.network",
    manifest: "/.well-known/x402-manifest.json",
    openapi: "/openapi.json",
    catalog: "/api/x402",
    health: "/api/health",
  });
}
