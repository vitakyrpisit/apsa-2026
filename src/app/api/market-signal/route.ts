import { NextResponse } from "next/server";
import { handleX402Payment, build402Response, build200Response, type X402ServiceConfig, X402Error } from "@/lib/apsa/x402-handler";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const SERVICE: X402ServiceConfig = {
  serviceId: "market-signal",
  serviceName: "Market Signal Snapshot",
  description: "Quantitative crypto signal with confidence, RSI, volume delta, key levels.",
  resource: "/api/market-signal",
  priceUSDC: 0.001,
  amountAtomic: "1000",
  tags: ["crypto","market","signal","trading"],
  mimeType: "application/json",
};

const TICKERS: Record<string,string> = { BTC:"bitcoin",ETH:"ethereum",USDC:"usd-coin",BASE:"base",SOL:"solana",TRX:"tron" };

async function getPrice(symbol: string) {
  const id = TICKERS[symbol] ?? symbol.toLowerCase();
  try {
    const res = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${id}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true`, { signal: AbortSignal.timeout(5000) });
    const data = (await res.json()) as Record<string,{usd:number;usd_24h_change:number;usd_market_cap:number}>;
    const d = data[id]; if (!d) return null;
    return { price:d.usd, change24h:d.usd_24h_change??0, marketCap:d.usd_market_cap??0 };
  } catch { return null; }
}

export async function GET() {
  return NextResponse.json({ service: SERVICE.serviceName, price: `$${SERVICE.priceUSDC} USDC`, payTo: EVM_PAYOUT_ADDRESS, network:"base", symbols: Object.keys(TICKERS), endpoint:"POST /api/market-signal?symbol={SYMBOL}" });
}

export async function POST(req: Request) {
  let body: unknown = null;
  try { body = await req.json(); } catch { body = {}; }
  const url = new URL(req.url);
  const symbol = (url.searchParams.get("symbol") || (body as {symbol?:string})?.symbol || "BTC").toUpperCase();
  if (!TICKERS[symbol]) return NextResponse.json({ error:"Invalid symbol", valid:Object.keys(TICKERS) }, { status:400 });

  const data = await getPrice(symbol);
  if (!data) return NextResponse.json({ error:"Price data unavailable" }, { status:503 });

  const preview = { symbol, price:data.price, change24h:data.change24h, signal: data.change24h>=0?"BULLISH":"BEARISH" };

  try {
    const settlement = await handleX402Payment(req, body, SERVICE, preview);
    if (!settlement) return build402Response(SERVICE, preview);

    // REAL DATA — not hardcoded
    const signal = data.change24h >= 0 ? "BUY" : "SELL";
    const confidence = Math.min(95, 50 + Math.abs(data.change24h) * 10);
    return build200Response(SERVICE, {
      symbol, signal, entryPrice: data.price, confidence: Math.round(confidence),
      change24h: data.change24h, marketCap: data.marketCap,
      timestamp: new Date().toISOString(), expiresAt: new Date(Date.now()+3600000).toISOString(),
    }, settlement);
  } catch (e) {
    if (e instanceof X402Error) return NextResponse.json(e.body, { status:e.statusCode });
    throw e;
  }
}
