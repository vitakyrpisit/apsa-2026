import { NextResponse } from "next/server";
import {
  processPayment,
  buildPaymentRequirements,
  extractPaymentPayload,
  type PaymentRequirements,
} from "@/lib/apsa/payai-facilitator";
import { analyzeContractRisk } from "@/lib/apsa/sentinel-shield";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS, SENTINEL_PRICE_ATOMIC } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const PRICE_USDC = 9.5;

export async function POST(req: Request) {
  let body: unknown = null;
  try { body = await req.json(); } catch { body = null; }

  const paymentPayload = extractPaymentPayload(req, body);
  const reqs = buildPaymentRequirements(SENTINEL_PRICE_ATOMIC, "/api/x402/sentinelshield", "SentinelShield Smart Contract Vulnerability Triage & SARIF Report");

  if (!paymentPayload) {
    // Return 402 with payment requirements
    return NextResponse.json({
      error: "Payment Required",
      message: "Access to SentinelShield requires x402 payment authorization.",
      paymentRequirements: reqs,
    }, {
      status: 402,
      headers: {
        "Content-Type": "application/json",
        "x402-version": "1.0",
        "WWW-Authenticate": `x402 token="USDC", network="base", amount="${SENTINEL_PRICE_ATOMIC}", recipient="${EVM_PAYOUT_ADDRESS}"`,
      },
    });
  }

  // Process payment: verify → settle → on-chain check
  const result = await processPayment(paymentPayload, reqs);

  if (!result.verified) {
    return NextResponse.json({
      error: "Payment Verification Failed",
      reason: result.error,
      settledOnChain: false,
    }, { status: 402 });
  }

  if (!result.settled || !result.txHash) {
    return NextResponse.json({
      error: "Settlement Incomplete",
      reason: result.error,
      verified: true,
      settledOnChain: false,
    }, { status: 402 });
  }

  // Payment settled on-chain — deliver the service
  const input = (body as { chain?: string; contractAddress?: string }) || {};
  const outcome = await analyzeContractRisk({
    chain: "base",
    contractAddress: input.contractAddress || BASE_USDC_MAINNET_ADDRESS,
  });

  return NextResponse.json({
    success: true,
    service: "SentinelShield Contract Risk Triage",
    payment: {
      status: "SETTLED",
      txHash: result.txHash,
      payer: result.payer,
      payTo: EVM_PAYOUT_ADDRESS,
      amountUSDC: PRICE_USDC,
      verifiedOnChain: true,
    },
    outcome,
  });
}

export async function GET() {
  return NextResponse.json({
    service: "SentinelShield Contract Risk Triage",
    version: "2.0.0",
    resource: "/api/x402/sentinelshield",
    method: "POST",
    price: `${PRICE_USDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base",
    facilitator: "https://facilitator.payai.network",
    manifest: "/.well-known/x402-manifest.json",
    health: "/api/health",
  });
}
