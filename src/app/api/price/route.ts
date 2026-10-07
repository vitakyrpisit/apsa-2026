import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 10;

const TICKERS: Record<string, string> = {
  BTC: "bitcoin", ETH: "ethereum", USDC: "usd-coin",
  SOL: "solana", TRX: "tron",
};

/** GET /api/price?symbol=BTC — FREE real-time crypto price (no payment required) */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const symbol = url.searchParams.get("symbol")?.toUpperCase();
  const id = symbol ? TICKERS[symbol] : null;

  if (!id) {
    return NextResponse.json({
      service: "Free Crypto Price Feed",
      price: "FREE — no payment required",
      symbols: Object.keys(TICKERS),
      paidServices: {
        marketAnalysis: "POST /api/market-analysis?symbol={SYMBOL} ($0.05 USDC)",
        marketSignal: "POST /api/market-signal?symbol={SYMBOL} ($0.001 USDC)",
      },
      manifest: "/.well-known/x402-manifest.json",
    });
  }

  try {
    const res = await fetch(
      `https://api.coingecko.com/api/v3/simple/price?ids=${id}&vs_currencies=usd&include_24hr_change=true`,
      { signal: AbortSignal.timeout(5000) },
    );
    const data = (await res.json()) as Record<string, { usd: number; usd_24h_change: number }>;
    const d = data[id];
    return NextResponse.json({
      symbol,
      price: d.usd,
      change24h: d.usd_24h_change,
      source: "CoinGecko",
      timestamp: new Date().toISOString(),
      paidAnalysis: `POST /api/market-analysis?symbol=${symbol} ($0.05 USDC for LLM analysis)`,
    });
  } catch {
    return NextResponse.json({ error: "Price feed temporarily unavailable", symbol }, { status: 503 });
  }
}
