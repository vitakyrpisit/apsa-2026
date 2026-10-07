import { NextResponse } from "next/server";
import { handleX402Payment, build402Response, build200Response, type X402ServiceConfig, X402Error } from "@/lib/apsa/x402-handler";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const SERVICE: X402ServiceConfig = {
  serviceId: "company-intel", serviceName: "Company Intelligence", description: "B2B research report",
  resource: "/api/company-intel", priceUSDC: 0.50, amountAtomic: "500000",
  tags: ["business","intelligence","research","b2b"], mimeType: "application/json",
};

export async function GET() { return NextResponse.json({ service:SERVICE.serviceName, price:`$${SERVICE.priceUSDC}`, endpoint:"POST /api/company-intel?name={COMPANY}" }); }

export async function POST(req: Request) {
  let body: unknown = null; try { body = await req.json(); } catch { body = {}; }
  const url = new URL(req.url);
  const companyName = url.searchParams.get("name") || (body as {name?:string})?.name;
  if (!companyName) return NextResponse.json({ error:"Missing name" }, { status:400 });

  const preview = { company: companyName, type:"B2B research + competitive analysis" };
  try {
    const settlement = await handleX402Payment(req, body, SERVICE, preview);
    if (!settlement) return build402Response(SERVICE, preview);

    // REAL DATA — web search + LLM analysis
    let report;
    try {
      const ZAI = (await import("z-ai-web-dev-sdk")).default;
      const zai = await ZAI.create();
      const searchResults = await zai.functions.invoke("web_search", { query: `${companyName} company revenue employees business model 2026`, num: 5 });
      const searchContext = searchResults.map((r:{name:string;snippet:string}) => `${r.name}: ${r.snippet}`).join("\n");
      const llmRes = await zai.chat.completions.create({
        messages: [{ role:"user", content:`Create B2B intelligence report for "${companyName}". Search results:\n${searchContext}\n\nRespond as JSON: {"overview":"2-3 sentences","businessModel":"description","keyStrengths":["s1","s2"],"weaknesses":["w1","w2"],"recommendation":"BUY|SELL|PARTNER|AVOID"}` }],
        thinking: { type:"disabled" },
      });
      const content = llmRes.choices[0]?.message?.content || "{}";
      report = JSON.parse(content.replace(/```json\n?/g,"").replace(/```/g,"").trim());
    } catch { report = { overview:`Intelligence report for ${companyName}.`, businessModel:"Could not determine.", recommendation:"NEUTRAL" }; }

    return build200Response(SERVICE, report, settlement);
  } catch (e) { if (e instanceof X402Error) return NextResponse.json(e.body, { status:e.statusCode }); throw e; }
}
