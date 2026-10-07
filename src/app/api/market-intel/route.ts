import { NextResponse } from "next/server";
import {
  getAgentStats,
  getAllMarketData,
  getAllAnalyses,
  getAllSignals,
  runMarketIntelCycle,
  startMarketIntelAgent,
} from "@/lib/apsa/market-intel-agent";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Start the autonomous agent on first request to this route.
let agentStarted = false;
if (!agentStarted) {
  agentStarted = true;
  startMarketIntelAgent(300000); // 5-minute cycle
}

/**
 * GET /api/market-intel — agent status + all collected data
 * POST /api/market-intel — trigger a manual collection+analysis cycle
 */
export async function GET() {
  return NextResponse.json({
    stats: getAgentStats(),
    marketData: getAllMarketData(),
    analyses: getAllAnalyses(),
    signals: getAllSignals(),
    endpoints: {
      analysis: {
        free: "GET /api/market-analysis",
        paid: "POST /api/market-analysis?symbol=BTC",
        price: "$0.05 USDC",
      },
      signal: {
        free: "GET /api/market-signal",
        paid: "POST /api/market-signal?symbol=BTC",
        price: "$0.01 USDC",
      },
    },
  });
}

export async function POST() {
  // Trigger a manual collection + analysis cycle
  try {
    await runMarketIntelCycle();
    return NextResponse.json({
      triggered: true,
      stats: getAgentStats(),
    });
  } catch {
    return NextResponse.json(
      { triggered: false, error: "Cycle already running or failed" },
      { status: 409 },
    );
  }
}
