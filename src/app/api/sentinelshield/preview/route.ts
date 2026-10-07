import { NextResponse } from "next/server";
import { analyzeContractRisk, validateSentinelInput, SentinelInputError } from "@/lib/apsa/sentinel-shield";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 20;

/**
 * GET /api/sentinelshield/preview?address=0x... — FREE preview
 * Returns: risk count, severity, top finding titles
 * Does NOT return: full SARIF, detailed mitigations, exploit vectors
 * 
 * Purpose: "loss leader" funnel — agent sees risk → pays for full report
 */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const address = url.searchParams.get("address");
  const bytecode = url.searchParams.get("bytecode");

  if (!address && !bytecode) {
    return NextResponse.json({
      service: "SentinelShield Preview (FREE)",
      description: "Free smart contract risk preview. Returns risk count + severity.",
      usage: "GET /api/sentinelshield/preview?address=0x... or ?bytecode=0x...",
      fullReportPrice: "$9.50 USDC on Base",
      fullReportEndpoint: "POST /api/x402/sentinelshield",
      manifest: "/.well-known/x402-manifest.json",
    });
  }

  const input = { chain: "base", contractAddress: address || undefined, bytecode: bytecode || undefined };

  try {
    validateSentinelInput(input);
  } catch (e) {
    if (e instanceof SentinelInputError) {
      return NextResponse.json({ error: e.message }, { status: e.status });
    }
    return NextResponse.json({ error: "Invalid input" }, { status: 422 });
  }

  try {
    const full = await analyzeContractRisk(input);

    // Return ONLY preview data — no full findings, no SARIF, no mitigations
    return NextResponse.json({
      service: "SentinelShield Preview (FREE)",
      target: address || "bytecode",
      riskLevel: full.riskLevel,
      overallScore: full.overallScore,
      exploitability: full.exploitability,
      findingCount: full.findings.length,
      findingsPreview: full.findings.map(f => ({
        level: f.level,
        title: f.title,
      })),
      metrics: {
        delegatecall: full.metrics.unauthorizedUpgradeVector,
        selfdestruct: full.findings.some(f => f.title.includes("SELFDESTRUCT")),
        proxy: full.findings.some(f => f.title.includes("proxy") || f.title.includes("EIP-1967") || f.title.includes("EIP-1167")),
      },
      fullReport: {
        price: "$9.50 USDC",
        endpoint: "POST /api/x402/sentinelshield",
        includes: ["SARIF 2.1.0", "exploit vectors", "mitigations", "CVSS scores"],
        paymentNetwork: "Base Mainnet (eip155:8453)",
        payTo: "0x829f877daAb94D766BB2b8511ad486C40f2C2BDA",
      },
      message: full.findings.length > 0
        ? `${full.findings.length} finding(s) detected. Pay $9.50 USDC for full SARIF report.`
        : "No critical findings in bytecode analysis. Full report still recommended for source-level review.",
    });
  } catch (e) {
    return NextResponse.json({
      error: e instanceof Error ? e.message : "Analysis failed",
      fullReportPrice: "$9.50 USDC",
    }, { status: 502 });
  }
}
