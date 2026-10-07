import { NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const BUNDLE_PATH = "/home/z/my-project/upload/APSA-2026-COMPLETE-AUTONOMOUS-MONEY-HUNTER.zip";
const BUNDLE_FILENAME = "APSA-2026-COMPLETE-AUTONOMOUS-MONEY-HUNTER.zip";

/** GET /api/download/bundle.zip — serve the original uploaded protocol archive. */
export async function GET() {
  try {
    const data = await fs.readFile(BUNDLE_PATH);
    return new NextResponse(data as unknown as BodyInit, {
      status: 200,
      headers: {
        "Content-Type": "application/zip",
        "Content-Disposition": `attachment; filename="${BUNDLE_FILENAME}"`,
        "Content-Length": String(data.byteLength),
        "Cache-Control": "public, max-age=300",
      },
    });
  } catch {
    return NextResponse.json(
      { error: "Bundle archive not found on server.", path: BUNDLE_PATH },
      { status: 404 },
    );
  }
}

// Helper kept for potential future generated-bundle flows.
export async function HEAD() {
  try {
    const stat = await fs.stat(BUNDLE_PATH);
    return new NextResponse(null, {
      status: 200,
      headers: {
        "Content-Length": String(stat.size),
        "Content-Type": "application/zip",
      },
    });
  } catch {
    return new NextResponse(null, { status: 404 });
  }
}

// Avoid unused var lint warning for path import in some setups.
void path;
