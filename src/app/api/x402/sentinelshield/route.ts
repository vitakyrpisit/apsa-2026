import { NextResponse } from "next/server";
import { handlePaidSentinelRequest, generateV2PaymentRequirements } from "@/lib/apsa/x402-core";
import { BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * POST /api/x402/sentinelshield
 * Faithful x402 v2 endpoint:
 *  - No payment payload → 402 + PAYMENT-REQUIRED header
 *  - Malformed / wrong recipient / wrong amount / expired → 400
 *  - Otherwise runs the full verification pipeline and returns the
 *    SentinelShield outcome when fully settled.
 */
export async function POST(req: Request) {
  let body: unknown = null;
  try {
    body = await req.json();
  } catch {
    body = null;
  }

  const paymentSignature = req.headers.get("payment-signature");
  if (paymentSignature && !body) {
    try {
      body = JSON.parse(
        Buffer.from(paymentSignature, "base64").toString("utf8"),
      );
    } catch {
      // keep body null → triggers 402
    }
  }

  const result = await handlePaidSentinelRequest(
    {
      chain: "base",
      contractAddress: BASE_USDC_MAINNET_ADDRESS,
    },
    body,
  );

  return NextResponse.json(result.body, {
    status: result.statusCode,
    headers: {
      "Cache-Control": "no-store",
      ...result.headers,
    },
  });
}

export async function GET() {
  const reqs = generateV2PaymentRequirements("/sentinelshield");
  return NextResponse.json(
    {
      service: "SentinelShield Contract Risk Triage",
      version: "2.0.0",
      resource: "/api/x402/sentinelshield",
      method: "POST",
      accepts: [reqs],
      discovery: "/.well-known/x402-manifest.json",
      health: "/api/health",
    },
    { headers: { "Cache-Control": "no-store" } },
  );
}
