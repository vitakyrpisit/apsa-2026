import { NextResponse } from "next/server";
import { runAllTests } from "@/lib/apsa/test-suite";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST() {
  const { passed, results } = await runAllTests();
  return NextResponse.json(
    { passed, count: results.length, results },
    {
      headers: { "Cache-Control": "no-store" },
    },
  );
}

export async function GET() {
  const { passed, results } = await runAllTests();
  return NextResponse.json(
    { passed, count: results.length, results },
    {
      headers: { "Cache-Control": "no-store" },
    },
  );
}
