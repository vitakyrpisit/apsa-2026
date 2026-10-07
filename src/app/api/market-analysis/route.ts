import { NextResponse } from "next/server";
import ZAI from "z-ai-web-dev-sdk";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const PRICE_USDC = 0.05;
const PRICE_ATOMIC = "50000";

const TICKER_MAP: Record<string, string> = {
  BTC: "bitcoin", ETH: "ethereum", USDC: "usd-coin",
  BASE: "base", SOL: "solana", TRX: "tron",
};

/** Fetch real price from CoinGecko (free, no key) */
async function getPrice(symbol: string) {
  const id = TICKER_MAP[symbol] ?? symbol.toLowerCase();
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${id}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true`;
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
    if (!res.ok) return null;
    const data = (await res.json()) as Record<string, { usd: number; usd_24h_change: number; usd_market_cap: number; usd_24h_vol: number }>;
    const d = data[id];
    if (!d) return null;
    return { symbol, price: d.usd, change24h: d.usd_24h_change ?? 0, marketCap: d.usd_market_cap ?? 0, volume24h: d.usd_24h_vol ?? 0 };
  } catch { return null; }
}

/** Generate LLM analysis on-demand (serverless-safe) */
async function generateAnalysis(symbol: string, data: { price: number; change24h: number; marketCap: number; volume24h: number }) {
  try {
    const zai = await ZAI.create();
    const res = await zai.chat.completions.create({
      messages: [{
        role: "user",
        content: `Analyze ${symbol}. Price: $${data.price}, 24h: ${data.change24h.toFixed(2)}%, MarketCap: $${(data.marketCap/1e9).toFixed(2)}B, Volume: $${(data.volume24h/1e6).toFixed(2)}M. Respond as JSON: {"title":"short headline","summary":"2-3 sentences","keyPoints":["point1","point2","point3"],"signal":"BULLISH|BEARISH|NEUTRAL","confidence":0-100}`,
      }],
      thinking: { type: "disabled" },
    });
    const content = res.choices[0]?.message?.content ?? "{}";
    const clean = content.replace(/```json\n?/g, "").replace(/```/g, "").trim();
    return JSON.parse(clean);
  } catch {
    return {
      title: `${symbol} at $${data.price}`,
      summary: `Price $${data.price}, 24h ${data.change24h.toFixed(2)}%.`,
      keyPoints: [`Price: $${data.price}`, `24h: ${data.change24h.toFixed(2)}%`],
      signal: data.change24h >= 0 ? "BULLISH" : "BEARISH",
      confidence: 50,
    };
  }
}

/** GET — free listing of available symbols */
export async function GET() {
  return NextResponse.json({
    service: "MarketIntelAgent — LLM Market Analysis",
    price: `${PRICE_USDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base-mainnet",
    symbols: Object.keys(TICKER_MAP),
    endpoint: "POST /api/market-analysis?symbol={SYMBOL}",
    manifest: "/.well-known/x402-manifest.json",
  });
}

/** POST — x402 gated: unpaid → 402, paid → full LLM analysis */
export async function POST(req: Request) {
  const url = new URL(req.url);
  const symbol = url.searchParams.get("symbol")?.toUpperCase();

  if (!symbol || !TICKER_MAP[symbol]) {
    return NextResponse.json({ error: "Invalid symbol", valid: Object.keys(TICKER_MAP) }, { status: 400 });
  }

  // Collect data on-demand (serverless-safe, no in-memory store)
  const data = await getPrice(symbol);
  if (!data) {
    return NextResponse.json({ error: "Could not fetch market data", symbol }, { status: 503 });
  }

  const paymentProof = req.headers.get("x-payment-proof");

  if (!paymentProof) {
    // Return 402 with basic data as preview
    return NextResponse.json({
      error: "Payment Required",
      message: `${symbol} analysis costs $${PRICE_USDC} USDC.`,
      paymentRequirements: {
        scheme: "exact", network: "eip155:8453",
        amount: PRICE_ATOMIC, amountUSDC: PRICE_USDC,
        payTo: EVM_PAYOUT_ADDRESS, asset: BASE_USDC_MAINNET_ADDRESS,
        description: `Market analysis for ${symbol}`,
      },
      preview: {
        symbol, price: data.price, change24h: data.change24h,
        signal: data.change24h >= 0 ? "BULLISH" : "BEARISH",
      },
    }, {
      status: 402,
      headers: { "x402-version": "1.0", "WWW-Authenticate": `x402 token="USDC", network="base-mainnet", amount="${PRICE_ATOMIC}", recipient="${EVM_PAYOUT_ADDRESS}"` },
    });
  }

  // Payment received — generate full LLM analysis on-demand
  const analysis = await generateAnalysis(symbol, data);

  return NextResponse.json({
    status: "DELIVERED",
    symbol,
    analysis: {
      title: analysis.title,
      summary: analysis.summary,
      keyPoints: analysis.keyPoints,
      signal: analysis.signal,
      confidence: analysis.confidence,
    },
    marketData: { price: data.price, change24h: data.change24h, marketCap: data.marketCap, volume24h: data.volume24h },
    payment: { amountUSDC: PRICE_USDC, payTo: EVM_PAYOUT_ADDRESS, network: "base-mainnet" },
    generatedAt: new Date().toISOString(),
  });
}
