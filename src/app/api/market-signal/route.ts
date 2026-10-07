import { NextResponse } from "next/server";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const PRICE_USDC = 0.001;
const PRICE_ATOMIC = "1000";

const TICKER_MAP: Record<string, string> = {
  BTC: "bitcoin", ETH: "ethereum", USDC: "usd-coin",
  BASE: "base", SOL: "solana", TRX: "tron",
};

async function getPrice(symbol: string) {
  const id = TICKER_MAP[symbol] ?? symbol.toLowerCase();
  try {
    const res = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${id}&vs_currencies=usd&include_24hr_change=true`, { signal: AbortSignal.timeout(5000) });
    const data = (await res.json()) as Record<string, { usd: number; usd_24h_change: number }>;
    const d = data[id];
    if (!d) return null;
    return { price: d.usd, change24h: d.usd_24h_change ?? 0 };
  } catch { return null; }
}

export async function GET() {
  return NextResponse.json({
    service: "Market Signal Snapshot",
    price: `${PRICE_USDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base-mainnet",
    symbols: Object.keys(TICKER_MAP),
    endpoint: "POST /api/market-signal?symbol={SYMBOL}",
  });
}

export async function POST(req: Request) {
  const url = new URL(req.url);
  const symbol = url.searchParams.get("symbol")?.toUpperCase();

  if (!symbol || !TICKER_MAP[symbol]) {
    return NextResponse.json({ error: "Invalid symbol", valid: Object.keys(TICKER_MAP) }, { status: 400 });
  }

  const data = await getPrice(symbol);
  if (!data) {
    return NextResponse.json({ error: "Price data unavailable", symbol }, { status: 503 });
  }

  const paymentProof = req.headers.get("x-payment-proof");
  if (!paymentProof) {
    const signal = data.change24h >= 0 ? "BULLISH" : "BEARISH";
    return NextResponse.json({
      error: "Payment Required",
      message: `${symbol} signal costs $${PRICE_USDC} USDC.`,
      paymentRequirements: {
        scheme: "exact", network: "eip155:8453",
        amount: PRICE_ATOMIC, amountUSDC: PRICE_USDC,
        payTo: EVM_PAYOUT_ADDRESS, asset: BASE_USDC_MAINNET_ADDRESS,
        description: `Market signal: ${symbol}`,
      },
      preview: { symbol, signal, price: data.price, change24h: data.change24h },
    }, {
      status: 402,
      headers: { "x402-version": "1.0", "WWW-Authenticate": `x402 token="USDC", network="base-mainnet", amount="${PRICE_ATOMIC}", recipient="${EVM_PAYOUT_ADDRESS}"` },
    });
  }

  // Payment received — generate full signal
  const signal = data.change24h >= 0 ? "BUY" : "SELL";
  const confidence = Math.min(95, 50 + Math.abs(data.change24h) * 10);

  return NextResponse.json({
    status: "DELIVERED",
    symbol,
    signal: {
      action: signal,
      entryPrice: data.price,
      confidence: Math.round(confidence),
      change24h: data.change24h,
      timestamp: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 3600000).toISOString(),
    },
    payment: { amountUSDC: PRICE_USDC, payTo: EVM_PAYOUT_ADDRESS, network: "base-mainnet" },
  });
}
