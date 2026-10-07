import { NextRequest, NextResponse } from "next/server";
import { fetchLiveOnChainStatus } from "@/lib/apsa/base-rpc";
import { EVM_PAYOUT_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const networkParam = req.nextUrl.searchParams.get("network");
  const addressParam = req.nextUrl.searchParams.get("address");
  const network =
    networkParam === "base-sepolia" ? "base-sepolia" : "base-mainnet";
  const address = addressParam || EVM_PAYOUT_ADDRESS;

  const status = await fetchLiveOnChainStatus(
    address,
    network as "base-mainnet" | "base-sepolia",
  );
  return NextResponse.json(status, {
    headers: {
      "Cache-Control": "no-store, max-age=0",
      "X-APSA-Network": network,
    },
  });
}
