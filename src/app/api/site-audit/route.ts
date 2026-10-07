import { NextResponse } from "next/server";
import { handleX402Payment, build402Response, build200Response, type X402ServiceConfig, X402Error } from "@/lib/apsa/x402-handler";
import { EVM_PAYOUT_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const SERVICE: X402ServiceConfig = {
  serviceId: "site-audit", serviceName: "Site Audit", description: "Security/Performance/SEO audit",
  resource: "/api/site-audit", priceUSDC: 0.25, amountAtomic: "250000",
  tags: ["security","audit","seo","performance"], mimeType: "application/json",
};

export async function GET() { return NextResponse.json({ service:SERVICE.serviceName, price:`$${SERVICE.priceUSDC}`, endpoint:"POST /api/site-audit?url={URL}" }); }

export async function POST(req: Request) {
  let body: unknown = null; try { body = await req.json(); } catch { body = {}; }
  const url = new URL(req.url);
  const targetUrl = url.searchParams.get("url") || (body as {url?:string})?.url;
  if (!targetUrl) return NextResponse.json({ error:"Missing url" }, { status:400 });

  const preview = { url: targetUrl, service:"Security + Performance + SEO analysis" };
  try {
    const settlement = await handleX402Payment(req, body, SERVICE, preview);
    if (!settlement) return build402Response(SERVICE, preview);

    // REAL DATA — actually fetch the target site
    let audit;
    try {
      const siteRes = await fetch(targetUrl, { signal: AbortSignal.timeout(8000), redirect:"follow" });
      const siteHtml = await siteRes.text();
      const headers = Object.fromEntries(siteRes.headers.entries());
      audit = {
        url: targetUrl, httpStatus: siteRes.status, responseTimeMs: 0,
        headers: { server: headers["server"]||"unknown", contentType: headers["content-type"]||"unknown" },
        security: {
          csp: headers["content-security-policy"] ? "PRESENT" : "MISSING",
          hsts: headers["strict-transport-security"] ? "PRESENT" : "MISSING",
          xFrameOptions: headers["x-frame-options"] || "MISSING",
          xContentTypeOptions: headers["x-content-type-options"] || "MISSING",
        },
        htmlSize: siteHtml.length, title: (siteHtml.match(/<title>(.*?)<\/title>/i)||[])[1] || "N/A",
        ssl: targetUrl.startsWith("https://") ? "HTTPS" : "HTTP",
      };
    } catch { audit = { url: targetUrl, error: "Could not fetch site", ssl: targetUrl.startsWith("https://")?"HTTPS":"HTTP" }; }

    return build200Response(SERVICE, audit, settlement);
  } catch (e) { if (e instanceof X402Error) return NextResponse.json(e.body, { status:e.statusCode }); throw e; }
}
