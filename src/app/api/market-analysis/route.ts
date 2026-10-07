import { NextResponse } from "next/server";
import { handleX402Payment, build402Response, build200Response, type X402ServiceConfig, X402Error } from "@/lib/apsa/x402-handler";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const SERVICE: X402ServiceConfig = {
  serviceId: "market-analysis", serviceName: "Market Analysis", description: "LLM market analysis",
  resource: "/api/market-analysis", priceUSDC: 0.05, amountAtomic: "50000",
  tags: ["market","analysis","crypto","llm"], mimeType: "application/json",
};

const TICKERS: Record<string,string> = { BTC:"bitcoin",ETH:"ethereum",USDC:"usd-coin",BASE:"base",SOL:"solana",TRX:"tron" };

async function getPrice(symbol: string) {
  const id = TICKERS[symbol] ?? symbol.toLowerCase();
  try {
    const res = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${id}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true`, { signal: AbortSignal.timeout(5000) });
    const data = (await res.json()) as Record<string,{usd:number;usd_24h_change:number;usd_market_cap:number;usd_24h_vol:number}>;
    const d = data[id]; if (!d) return null;
    return { price:d.usd, change24h:d.usd_24h_change??0, marketCap:d.usd_market_cap??0, volume24h:d.usd_24h_vol??0 };
  } catch { return null; }
}

export async function GET() { return NextResponse.json({ service:SERVICE.serviceName, price:`$${SERVICE.priceUSDC}`, symbols:Object.keys(TICKERS), endpoint:"POST /api/market-analysis?symbol={SYMBOL}" }); }

export async function POST(req: Request) {
  let body: unknown = null; try { body = await req.json(); } catch { body = {}; }
  const url = new URL(req.url);
  const symbol = (url.searchParams.get("symbol") || (body as {symbol?:string})?.symbol || "BTC").toUpperCase();
  if (!TICKERS[symbol]) return NextResponse.json({ error:"Invalid symbol", valid:Object.keys(TICKERS) }, { status:400 });

  const data = await getPrice(symbol);
  if (!data) return NextResponse.json({ error:"Price data unavailable" }, { status:503 });

  const preview = { symbol, price:data.price, change24h:data.change24h, signal: data.change24h>=0?"BULLISH":"BEARISH" };
  try {
    const settlement = await handleX402Payment(req, body, SERVICE, preview);
    if (!settlement) return build402Response(SERVICE, preview);

    // REAL DATA — LLM analysis
    let analysis;
    try {
      const ZAI = (await import("z-ai-web-dev-sdk")).default;
      const zai = await ZAI.create();
      const res = await zai.chat.completions.create({
        messages: [{ role:"user", content:`Analyze ${symbol}. Price:$${data.price}, 24h:${data.change24h.toFixed(2)}%, MCap:$${(data.marketCap/1e9).toFixed(2)}B, Vol:$${(data.volume24h/1e6).toFixed(2)}M. JSON: {"title":"headline","summary":"2-3 sentences","keyPoints":["p1","p2","p3"],"signal":"BULLISH|BEARISH|NEUTRAL","confidence":0-100}` }],
        thinking: { type:"disabled" },
      });
      const content = res.choices[0]?.message?.content || "{}";
      analysis = JSON.parse(content.replace(/```json\n?/g,"").replace(/```/g,"").trim());
    } catch { analysis = { title:`${symbol} at $${data.price}`, summary:`Price $${data.price}, 24h ${data.change24h.toFixed(2)}%.`, keyPoints:[`Price: $${data.price}`,`24h: ${data.change24h.toFixed(2)}%`], signal: data.change24h>=0?"BULLISH":"BEARISH", confidence:50 }; }

    return build200Response(SERVICE, { ...analysis, marketData: data }, settlement);
  } catch (e) { if (e instanceof X402Error) return NextResponse.json(e.body, { status:e.statusCode }); throw e; }
}
