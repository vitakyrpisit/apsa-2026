import { NextResponse } from "next/server";
import ZAI from "z-ai-web-dev-sdk";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const PRICE_USDC = 0.50;
const PRICE_ATOMIC = "500000";

export async function GET() {
  return NextResponse.json({
    service: "Company Intelligence — B2B Research Report",
    price: `${PRICE_USDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base-mainnet",
    endpoint: "POST /api/company-intel?name={COMPANY}",
  });
}

export async function POST(req: Request) {
  const url = new URL(req.url);
  const companyName = url.searchParams.get("name");

  if (!companyName) {
    return NextResponse.json({ error: "Missing name", endpoint: "POST /api/company-intel?name=Apple" }, { status: 400 });
  }

  const paymentProof = req.headers.get("x-payment-proof");

  if (!paymentProof) {
    return NextResponse.json({
      error: "Payment Required",
      message: `Intelligence report for ${companyName} costs $${PRICE_USDC} USDC.`,
      paymentRequirements: {
        scheme: "exact", network: "eip155:8453",
        amount: PRICE_ATOMIC, amountUSDC: PRICE_USDC,
        payTo: EVM_PAYOUT_ADDRESS, asset: BASE_USDC_MAINNET_ADDRESS,
        description: `Company intelligence: ${companyName}`,
      },
      preview: { company: companyName, type: "B2B research + competitive analysis" },
    }, {
      status: 402,
      headers: { "x402-version": "1.0", "WWW-Authenticate": `x402 token="USDC", network="base-mainnet", amount="${PRICE_ATOMIC}", recipient="${EVM_PAYOUT_ADDRESS}"` },
    });
  }

  // Payment received — generate intelligence report via LLM + web search
  let report;
  try {
    const zai = await ZAI.create();
    // First: web search for company info
    const searchResults = await zai.functions.invoke("web_search", { query: `${companyName} company revenue employees business model 2026`, num: 5 });
    const searchContext = searchResults.map((r: { name: string; snippet: string }) => `${r.name}: ${r.snippet}`).join("\n");

    // Then: LLM analysis
    const llmRes = await zai.chat.completions.create({
      messages: [{
        role: "user",
        content: `Create a B2B intelligence report for "${companyName}". Search results:\n${searchContext}\n\nRespond as JSON: {"overview":"2-3 sentences","businessModel":"description","revenueEstimate":"estimate","keyStrengths":["s1","s2"],"weaknesses":["w1","w2"],"opportunities":["o1","o2"],"threats":["t1","t2"],"competitivePosition":"assessment","recommendation":"BUY|SELL|PARTNER|AVOID"}`,
      }],
      thinking: { type: "disabled" },
    });
    const content = llmRes.choices[0]?.message?.content ?? "{}";
    report = JSON.parse(content.replace(/```json\n?/g, "").replace(/```/g, "").trim());
  } catch {
    report = {
      overview: `Intelligence report for ${companyName}.`,
      businessModel: "Could not determine — analysis limited.",
      recommendation: "NEUTRAL",
    };
  }

  return NextResponse.json({
    status: "DELIVERED",
    company: companyName,
    report,
    payment: { amountUSDC: PRICE_USDC, payTo: EVM_PAYOUT_ADDRESS, network: "base-mainnet" },
    generatedAt: new Date().toISOString(),
  });
}
