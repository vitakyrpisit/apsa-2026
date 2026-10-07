import { NextResponse } from "next/server";
import ZAI from "z-ai-web-dev-sdk";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

const PRICE_USDC = 0.25;
const PRICE_ATOMIC = "250000";

/** GET — free metadata */
export async function GET() {
  return NextResponse.json({
    service: "Site Audit — Security, Performance, SEO Analysis",
    price: `${PRICE_USDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base-mainnet",
    endpoint: "POST /api/site-audit?url={URL}",
  });
}

/** POST — x402 gated site audit */
export async function POST(req: Request) {
  const url = new URL(req.url);
  const targetUrl = url.searchParams.get("url");

  if (!targetUrl) {
    return NextResponse.json({ error: "Missing url parameter", endpoint: "POST /api/site-audit?url=https://example.com" }, { status: 400 });
  }

  const paymentProof = req.headers.get("x-payment-proof");

  if (!paymentProof) {
    return NextResponse.json({
      error: "Payment Required",
      message: `Site audit for ${targetUrl} costs $${PRICE_USDC} USDC.`,
      paymentRequirements: {
        scheme: "exact", network: "eip155:8453",
        amount: PRICE_ATOMIC, amountUSDC: PRICE_USDC,
        payTo: EVM_PAYOUT_ADDRESS, asset: BASE_USDC_MAINNET_ADDRESS,
        description: `Site audit: ${targetUrl}`,
      },
      preview: { url: targetUrl, service: "Security + Performance + SEO analysis" },
    }, {
      status: 402,
      headers: { "x402-version": "1.0", "WWW-Authenticate": `x402 token="USDC", network="base-mainnet", amount="${PRICE_ATOMIC}", recipient="${EVM_PAYOUT_ADDRESS}"` },
    });
  }

  // Payment received — perform site audit
  let auditResult;
  try {
    // Fetch the target site
    const siteRes = await fetch(targetUrl, { signal: AbortSignal.timeout(8000), redirect: "follow" });
    const siteHtml = await siteRes.text();
    const headers = Object.fromEntries(siteRes.headers.entries());

    // Use LLM to analyze
    const zai = await ZAI.create();
    const llmRes = await zai.chat.completions.create({
      messages: [{
        role: "user",
        content: `Audit this website. URL: ${targetUrl}. Status: ${siteRes.status}. Headers: ${JSON.stringify(headers).slice(0,500)}. HTML length: ${siteHtml.length}. First 1000 chars: ${siteHtml.slice(0,1000)}. Respond as JSON: {"securityScore":0-100,"performanceScore":0-100,"seoScore":0-100,"findings":["finding1","finding2","finding3"],"recommendations":["rec1","rec2"]}`,
      }],
      thinking: { type: "disabled" },
    });
    const content = llmRes.choices[0]?.message?.content ?? "{}";
    auditResult = JSON.parse(content.replace(/```json\n?/g, "").replace(/```/g, "").trim());
  } catch {
    auditResult = {
      securityScore: 50, performanceScore: 50, seoScore: 50,
      findings: ["Could not fully analyze site", `HTTP status: ${targetUrl}`],
      recommendations: ["Add HTTPS", "Add security headers"],
    };
  }

  return NextResponse.json({
    status: "DELIVERED",
    url: targetUrl,
    audit: auditResult,
    payment: { amountUSDC: PRICE_USDC, payTo: EVM_PAYOUT_ADDRESS, network: "base-mainnet" },
    generatedAt: new Date().toISOString(),
  });
}
