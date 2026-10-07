import { NextRequest, NextResponse } from "next/server";
import { verifyTransactionHash } from "@/lib/apsa/base-rpc";
import { EVM_PAYOUT_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  let body: { txHash?: string; network?: string } = {};
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      { error: "Invalid JSON body" },
      { status: 400 },
    );
  }

  const txHash = (body.txHash || "").trim();
  if (!txHash.startsWith("0x") || txHash.length !== 66) {
    return NextResponse.json(
      {
        status: "invalid",
        message:
          "Please provide a full 66-character transaction hash starting with 0x.",
      },
      { status: 400 },
    );
  }

  const network =
    body.network === "base-sepolia" ? "base-sepolia" : "base-mainnet";

  const result = await verifyTransactionHash(
    txHash,
    network as "base-mainnet" | "base-sepolia",
    EVM_PAYOUT_ADDRESS,
  );
  return NextResponse.json(result, {
    headers: { "Cache-Control": "no-store" },
  });
}
