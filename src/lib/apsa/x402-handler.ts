/**
 * Shared x402 payment handler for all paid services.
 * Mirrors the v2 patched `handleGenericX402Service` flow:
 *   402 → payload → PayAI /verify → PayAI /settle → txHash → Base receipt → 200
 *
 * NO mock headers. NO settlement_pending = success. NO result without on-chain proof.
 */

import { NextResponse } from "next/server";
import {
  processPayment,
  buildPaymentRequirements,
  extractPaymentPayload,
  type PaymentPayload,
  type PaymentRequirements,
} from "./payai-facilitator";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "./wallet-registry";

export interface X402ServiceConfig {
  serviceId: string;
  serviceName: string;
  description: string;
  resource: string;
  priceUSDC: number;
  amountAtomic: string;
  tags: string[];
  mimeType: string;
}

/**
 * Build a PayAI-compatible 402 response (v1 format: maxAmountRequired, network=base).
 */
export function build402Response(service: X402ServiceConfig, preview: Record<string, unknown>) {
  const reqs: PaymentRequirements = buildPaymentRequirements(
    service.amountAtomic,
    service.resource,
    service.description,
  );

  return NextResponse.json(
    {
      error: "Payment Required",
      status: "UNPAID",
      message: `Payment of $${service.priceUSDC} USDC required on Base Mainnet to invoke ${service.serviceName}.`,
      requirements: {
        ...reqs,
        amount: service.amountAtomic,
        amountUSD: service.priceUSDC,
        chainId: 8453,
        x402Version: 2,
        scheme: "exact",
        network: "eip155:8453",
        asset: BASE_USDC_MAINNET_ADDRESS,
        payTo: EVM_PAYOUT_ADDRESS,
        resource: service.resource,
        description: service.description,
        maxTimeoutSeconds: 3600,
        extensions: {
          bazaar: {
            serviceName: service.serviceName,
            tags: service.tags,
            mimeType: service.mimeType,
          },
        },
      },
      preview,
    },
    {
      status: 402,
      headers: {
        "Content-Type": "application/json",
        "x402-version": "2.0",
        "PAYMENT-REQUIRED": Buffer.from(JSON.stringify(reqs)).toString("base64"),
        "payment-required": Buffer.from(JSON.stringify(reqs)).toString("base64"),
        "WWW-Authenticate": `x402 token="USDC", network="base", amount="${service.amountAtomic}", recipient="${EVM_PAYOUT_ADDRESS}"`,
      },
    },
  );
}

/**
 * Full x402 payment handler for Next.js API routes.
 *
 * Flow:
 * 1. No payment → 402
 * 2. Payment payload → PayAI /verify → /settle → txHash → Base receipt → 200
 * 3. Pre-confirmed txHash → Base receipt → 200
 *
 * @returns null if payment is required (402 already sent),
 *          or the settlement result if payment is confirmed.
 */
export async function handleX402Payment(
  req: Request,
  body: unknown,
  service: X402ServiceConfig,
  preview: Record<string, unknown>,
): Promise<{ settled: true; txHash: string; payer?: string; amountUSDC?: number } | null> {
  const payload = extractPaymentPayload(req, body);
  const clientTxHash =
    (body as { txHash?: string })?.txHash ||
    req.headers.get("x-402-tx-hash") ||
    req.headers.get("x-tx-hash");

  // No payment → 402
  if (!payload && !clientTxHash) {
    return null; // Caller should return build402Response()
  }

  // Pre-confirmed tx hash → verify on-chain directly
  if (clientTxHash && !payload) {
    const payer = (body as { payer?: string })?.payer || "";
    const { verifyOnChainSettlement } = await import("./payai-facilitator");
    const result = await verifyOnChainSettlement(
      clientTxHash,
      payer,
      EVM_PAYOUT_ADDRESS,
      BigInt(service.amountAtomic),
    );
    if (!result.verified) {
      throw new X402Error(402, {
        error: "Payment Required",
        status: "INSUFFICIENT_OR_UNVERIFIED_SETTLEMENT",
        detail: result.error || "On-chain transaction did not settle required amount to operator wallet.",
      });
    }
    return { settled: true, txHash: clientTxHash };
  }

  // Payment payload → PayAI verify → settle → on-chain check
  if (payload) {
    const reqs: PaymentRequirements = buildPaymentRequirements(
      service.amountAtomic,
      service.resource,
      service.description,
    );

    const result = await processPayment(payload, reqs);

    if (!result.verified) {
      throw new X402Error(402, {
        error: "Payment Required",
        status: "PAYMENT_NOT_VERIFIED",
        detail: result.error || "x402 facilitator rejected payment authorization.",
        ourRevenueCounted: false,
      });
    }

    if (!result.settled || !result.txHash) {
      throw new X402Error(402, {
        error: "Payment Required",
        status: "FACILITATOR_SETTLEMENT_FAILED",
        detail: result.error || "Facilitator did not return a settlement transaction hash.",
        ourRevenueCounted: false,
      });
    }

    return {
      settled: true,
      txHash: result.txHash,
      payer: result.payer,
      amountUSDC: result.amountUSDC,
    };
  }

  // Malformed
  throw new X402Error(400, {
    error: "Malformed Payment Payload",
    status: "UNPAID",
    detail: "Provide an official x402 PAYMENT-SIGNATURE or an already-confirmed tx hash.",
  });
}

export class X402Error extends Error {
  constructor(
    public statusCode: number,
    public body: Record<string, unknown>,
  ) {
    super(body.error as string);
  }
}

/**
 * Build a successful 200 response with settlement proof.
 */
export function build200Response(
  service: X402ServiceConfig,
  data: unknown,
  settlement: { txHash: string; payer?: string; amountUSDC?: number },
) {
  return NextResponse.json(
    {
      success: true,
      service: service.serviceName,
      feeChargedUSD: service.priceUSDC,
      settlementTxHash: settlement.txHash,
      data,
      payment: {
        status: "SETTLED",
        txHash: settlement.txHash,
        payer: settlement.payer,
        payTo: EVM_PAYOUT_ADDRESS,
        amountUSDC: settlement.amountUSDC ?? service.priceUSDC,
        verifiedOnChain: true,
      },
    },
    {
      status: 200,
      headers: {
        "X-Payment-Status": "SETTLED",
        "X-Settlement-Tx-Hash": settlement.txHash,
        "X-Operator-Receipt-Wallet": EVM_PAYOUT_ADDRESS,
      },
    },
  );
}
