import { NextResponse } from "next/server";
import {
  processPayment,
  buildPaymentRequirements,
  extractPaymentPayload,
} from "@/lib/apsa/payai-facilitator";
import { analyzeContractRisk, validateSentinelInput, SentinelInputError } from "@/lib/apsa/sentinel-shield";
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

  const input = (body as { chain?: string; contractAddress?: string; bytecode?: string }) || {};

  // STEP 1: Validate input BEFORE any payment — buyer not charged for invalid input
  try {
    validateSentinelInput(input);
  } catch (e) {
    if (e instanceof SentinelInputError) {
      return NextResponse.json({ error: e.message, charged: false }, { status: e.status });
    }
    return NextResponse.json({ error: "Invalid input", charged: false }, { status: 422 });
  }

  const targetContract = input.contractAddress || BASE_USDC_MAINNET_ADDRESS;
  const preview = { service: SERVICE.serviceName, targetContract };

  try {
    // STEP 2: Do the analysis FIRST — if it fails, payment is never settled
    let outcome;
    try {
      outcome = await analyzeContractRisk(input);
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Analysis failed";
      return NextResponse.json({ error: msg, charged: false }, { status: 502 });
    }

    // STEP 3: Now handle payment — verify → settle → on-chain check
    const settlement = await handleX402Payment(req, body, SERVICE, preview);
    if (!settlement) return build402Response(SERVICE, preview);

    // STEP 4: Payment settled — deliver the already-computed result
    return build200Response(SERVICE, outcome, settlement);
  } catch (e) {
    if (e instanceof X402Error) return NextResponse.json(e.body, { status: e.statusCode });
    throw e;
  }
}

export async function GET() {
  return NextResponse.json({
    service: SERVICE.serviceName,
    version: "2.1.0",
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
