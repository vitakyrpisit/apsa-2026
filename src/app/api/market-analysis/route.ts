import { NextResponse } from "next/server";
import { getAnalysis, getAllAnalyses, recordPaidRequest } from "@/lib/apsa/market-intel-agent";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ANALYSIS_PRICE_USDC = 0.05;
const ANALYSIS_PRICE_ATOMIC = "50000"; // 0.05 USDC = 50000 atomic (6 decimals)

/**
 * GET /api/market-analysis — free list of available analyses (metadata only)
 * POST /api/market-analysis?symbol=BTC — x402-gated: unpaid → 402, paid → full analysis
 *
 * External agents pay $0.05 USDC per analysis request via x402.
 */
export async function GET() {
  const analyses = getAllAnalyses().map((a) => ({
    id: a.id,
    symbol: a.symbol,
    title: a.title,
    signal: a.signal,
    confidence: a.confidence,
    generatedAt: a.generatedAt,
    sha256: a.sha256,
    // Summary is NOT included in the free listing — only the metadata.
    // The full analysis (summary + keyPoints + priceTarget) requires payment.
    price: `${ANALYSIS_PRICE_USDC} USDC`,
    endpoint: "POST /api/market-analysis?symbol={SYMBOL}",
  }));

  return NextResponse.json({
    service: "MarketIntelAgent — Crypto Market Analysis",
    pricePerAnalysis: `${ANALYSIS_PRICE_USDC} USDC`,
    payTo: EVM_PAYOUT_ADDRESS,
    network: "base-mainnet",
    analysesAvailable: analyses.length,
    analyses: analyses,
    manifest: "/.well-known/x402-manifest.json",
  });
}

export async function POST(req: Request) {
  const url = new URL(req.url);
  const symbol = url.searchParams.get("symbol")?.toUpperCase();

  if (!symbol) {
    return NextResponse.json(
      {
        error: "Missing symbol parameter",
        message: "POST /api/market-analysis?symbol=BTC",
      },
      { status: 400 },
    );
  }

  const analysis = getAnalysis(symbol);
  if (!analysis) {
    return NextResponse.json(
      {
        error: "Analysis not available",
        message: `No analysis available for ${symbol}. Try GET /api/market-analysis for available symbols.`,
      },
      { status: 404 },
    );
  }

  // Check for payment. In production, this would verify the x402 payment
  // signature via the CDP Facilitator. For now, we accept a custom
  // X-Payment-Proof header or return a 402 challenge.
  const paymentProof = req.headers.get("x-payment-proof");

  if (!paymentProof) {
    // Return 402 Payment Required with x402 requirements
    const paymentRequirements = {
      scheme: "exact",
      network: "eip155:8453",
      amount: ANALYSIS_PRICE_ATOMIC,
      amountUSDC: ANALYSIS_PRICE_USDC,
      payTo: EVM_PAYOUT_ADDRESS,
      asset: BASE_USDC_MAINNET_ADDRESS,
      description: `Market analysis for ${symbol}: ${analysis.title}`,
      resource: "/api/market-analysis",
    };

    return NextResponse.json(
      {
        error: "Payment Required",
        message: `Access to the full ${symbol} analysis costs $${ANALYSIS_PRICE_USDC} USDC.`,
        paymentRequirements,
        preview: {
          title: analysis.title,
          signal: analysis.signal,
          confidence: analysis.confidence,
          generatedAt: analysis.generatedAt,
        },
      },
      {
        status: 402,
        headers: {
          "Content-Type": "application/json",
          "x402-version": "1.0",
          "WWW-Authenticate": `x402 token="USDC", network="base-mainnet", amount="${ANALYSIS_PRICE_ATOMIC}", recipient="${EVM_PAYOUT_ADDRESS}"`,
        },
      },
    );
  }

  // Payment received — deliver the full analysis
  recordPaidRequest(ANALYSIS_PRICE_USDC);

  return NextResponse.json({
    status: "DELIVERED",
    symbol: analysis.symbol,
    analysis: {
      id: analysis.id,
      title: analysis.title,
      summary: analysis.summary,
      keyPoints: analysis.keyPoints,
      signal: analysis.signal,
      confidence: analysis.confidence,
      priceTarget: analysis.priceTarget,
      generatedAt: analysis.generatedAt,
      llmModel: analysis.llmModel,
      sha256: analysis.sha256,
    },
    payment: {
      amountUSDC: ANALYSIS_PRICE_USDC,
      payTo: EVM_PAYOUT_ADDRESS,
      network: "base-mainnet",
    },
  });
}
