import { NextResponse } from "next/server";
import { getSignal, getAllSignals, recordPaidRequest } from "@/lib/apsa/market-intel-agent";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const SIGNAL_PRICE_USDC = 0.001;
const SIGNAL_PRICE_ATOMIC = "1000"; // 0.01 USDC = 10000 atomic

/**
 * GET /api/market-signal — free list of available signals (metadata only)
 * POST /api/market-signal?symbol=BTC — x402-gated: unpaid → 402, paid → full signal
 *
 * External agents pay $0.01 USDC per signal request via x402.
 */
export async function GET() {
  const signals = getAllSignals().map((s) => ({
    id: s.id,
    symbol: s.symbol,
    action: s.action,
    confidence: s.confidence,
    generatedAt: s.generatedAt,
    expiresAt: s.expiresAt,
    // Rationale + entryPrice NOT included — requires payment
    price: `${SIGNAL_PRICE_USDC} USDC`,
    endpoint: "POST /api/market-signal?symbol={SYMBOL}",
  }));

  return NextResponse.json({
    service: "MarketIntelAgent — Trading Signals",
    pricePerSignal: `${SIGNAL_PRICE_USDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base-mainnet",
    signalsAvailable: signals.length,
    signals: signals,
  });
}

export async function POST(req: Request) {
  const url = new URL(req.url);
  const symbol = url.searchParams.get("symbol")?.toUpperCase();

  if (!symbol) {
    return NextResponse.json(
      { error: "Missing symbol", message: "POST /api/market-signal?symbol=BTC" },
      { status: 400 },
    );
  }

  const signal = getSignal(symbol);
  if (!signal) {
    return NextResponse.json(
      { error: "Signal not available", message: `No signal for ${symbol}` },
      { status: 404 },
    );
  }

  const paymentProof = req.headers.get("x-payment-proof");

  if (!paymentProof) {
    return NextResponse.json(
      {
        error: "Payment Required",
        message: `Access to the ${symbol} trading signal costs $${SIGNAL_PRICE_USDC} USDC.`,
        paymentRequirements: {
          scheme: "exact",
          network: "eip155:8453",
          amount: SIGNAL_PRICE_ATOMIC,
          amountUSDC: SIGNAL_PRICE_USDC,
          payTo: EVM_PAYOUT_ADDRESS,
          asset: BASE_USDC_MAINNET_ADDRESS,
          description: `Trading signal for ${symbol}`,
        },
        preview: { action: signal.action, confidence: signal.confidence },
      },
      {
        status: 402,
        headers: {
          "x402-version": "1.0",
          "WWW-Authenticate": `x402 token="USDC", network="base-mainnet", amount="${SIGNAL_PRICE_ATOMIC}", recipient="${EVM_PAYOUT_ADDRESS}"`,
        },
      },
    );
  }

  recordPaidRequest(SIGNAL_PRICE_USDC);

  return NextResponse.json({
    status: "DELIVERED",
    symbol: signal.symbol,
    signal: {
      id: signal.id,
      action: signal.action,
      entryPrice: signal.entryPrice,
      confidence: signal.confidence,
      rationale: signal.rationale,
      generatedAt: signal.generatedAt,
      expiresAt: signal.expiresAt,
    },
    payment: { amountUSDC: SIGNAL_PRICE_USDC, payTo: EVM_PAYOUT_ADDRESS },
  });
}
