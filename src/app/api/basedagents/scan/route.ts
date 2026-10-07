import { NextResponse } from "next/server";
import { readFile } from "node:fs/promises";
import { deserializeKeypair, signRequest, type AgentKeypair } from "basedagents";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const API_BASE = "https://api.basedagents.ai";
const AGENT_ID = "ag_8ChyUm8F8de6uEMxUUMeDcnphJJT3ChJH7yuXEcgzXbP";
const KEYPAIR_PATH =
  "/home/z/my-project/.basedagents/keys/apsa-2026-sentinelshield-v2-keypair.json";

async function loadKeypair(): Promise<AgentKeypair> {
  const json = await readFile(KEYPAIR_PATH, "utf8");
  return deserializeKeypair(json);
}

async function unsignedGet(path: string) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "User-Agent": "APSA-2026/1.0 (+https://apsa-2026.vercel.app)",
      Accept: "application/json",
    },
    cache: "no-store",
  });
  return { status: res.status, ok: res.ok, body: res.ok ? await res.json() : null };
}

interface TaskSummary {
  task_id: string;
  title: string;
  creator: { kind?: string; id?: string; name?: string } | string | null;
  category: string;
  bounty: { amount_display?: string; token?: string; network?: string } | null;
  escrow: { status?: string } | null;
  required_capabilities: string[];
  expires_at: string | null;
  claimable: boolean;
  max_active_claims_per_agent: number | null;
}

interface ClassifiedTask extends TaskSummary {
  classification: "honest" | "scam_pattern" | "unknown";
  reasons: string[];
  matches_our_capabilities: boolean;
  our_caps_overlap: string[];
  estimated_effort: "quick" | "multi-day" | "unknown";
}

const OUR_CAPS = ["research", "code", "security", "testing", "documentation"];

/**
 * Classify a task as honest, scam_pattern, or unknown based on:
 *  - creator (BasedAgents_bot = honest, Industrial Sentinel* = scam_pattern)
 *  - description keywords (docker container + wallet monitoring = scam)
 *  - bounty funding model (sign-at-accept no escrow = red flag)
 */
function classifyTask(t: TaskSummary, description: string): ClassifiedTask {
  const creatorRaw = t.creator;
  const creator =
    typeof creatorRaw === "string"
      ? creatorRaw
      : (creatorRaw?.name || creatorRaw?.id || "");
  const reasons: string[] = [];
  let classification: "honest" | "scam_pattern" | "unknown" = "unknown";

  // Creator-based
  if (creator.includes("BasedAgents")) {
    classification = "honest";
    reasons.push("creator is BasedAgents project automation");
  } else if (
    creator.toLowerCase().includes("industrial sentinel") ||
    creator.toLowerCase().includes("industrialsentinelac")
  ) {
    classification = "scam_pattern";
    reasons.push("creator name matches Industrial Sentinel pattern");
  } else {
    reasons.push(`unknown creator: ${creator}`);
  }

  // Content-based red flags
  const descLower = description.toLowerCase();
  const redFlagKeywords = [
    { kw: "ghcr.io/industrial-platform", reason: "references unverified industrial-platform-ai container" },
    { kw: "sentinel_cashback_mode", reason: "requires SENTINEL_CASHBACK_MODE env" },
    { kw: "sentinel_revenue_guard_mode", reason: "requires SENTINEL_REVENUE_GUARD_MODE env" },
    { kw: "no escrow required upfront", reason: "bounty not pre-funded (no payment guarantee)" },
    { kw: "sign-at-accept", reason: "bounty is sign-at-accept (not escrowed)" },
    { kw: "bounded payer configuration", reason: "asks to delegate wallet payment authority" },
    { kw: "1.25 usdc/day hard cap", reason: "container has wallet spend cap (potentially drains wallet)" },
  ];
  for (const { kw, reason } of redFlagKeywords) {
    if (descLower.includes(kw)) {
      reasons.push(`red flag: ${reason}`);
      if (classification !== "honest") classification = "scam_pattern";
    }
  }

  // Bounty funding model
  const escrowStatus = t.escrow?.status;
  const hasBounty = !!t.bounty?.amount_display;
  if (hasBounty && escrowStatus !== "funded") {
    if (classification !== "honest") {
      reasons.push(`bounty $${t.bounty?.amount_display} but escrow=${escrowStatus || "null"} (not pre-funded)`);
      if (classification === "unknown") classification = "scam_pattern";
    }
  }
  if (hasBounty && escrowStatus === "funded") {
    reasons.push(`bounty $${t.bounty?.amount_display} with escrow=funded (honest)`);
    if (classification === "unknown") classification = "honest";
  }

  // Capabilities overlap
  const overlap = (t.required_capabilities || []).filter((c) =>
    OUR_CAPS.includes(c),
  );

  // Effort estimation
  let effort: "quick" | "multi-day" | "unknown" = "unknown";
  if (description.toLowerCase().includes("hard task")) {
    effort = "multi-day";
  } else if (description.toLowerCase().includes("time-box")) {
    effort = "quick";
  } else if (description.toLowerCase().includes("15 minutes")) {
    effort = "quick";
  } else if (t.category === "content" || t.category === "automation") {
    effort = "multi-day";
  }

  return {
    ...t,
    classification,
    reasons,
    matches_our_capabilities: overlap.length > 0,
    our_caps_overlap: overlap,
    estimated_effort: effort,
  };
}

/**
 * GET /api/basedagents/scan
 *
 * Polls the BasedAgents board for all open tasks, classifies each by
 * honest/scam/unknown, identifies honest paid tasks (the gold we want),
 * and identifies quick wins matching our capabilities.
 *
 * Used by the dashboard "Honest Task Monitor" to surface actionable work
 * the moment it appears. Polling every 5-15 minutes is reasonable.
 */
export async function GET() {
  const startedAt = Date.now();
  try {
    const tasksRes = await unsignedGet(`/v1/tasks?status=open&limit=100`);
    if (!tasksRes.ok) {
      return NextResponse.json(
        {
          ok: false,
          error: `tasks endpoint failed: HTTP ${tasksRes.status}`,
        },
        { status: 502 },
      );
    }

    const rawTasks = (tasksRes.body as { tasks?: TaskSummary[] })?.tasks || [];

    // Fetch each task's full description in parallel (max 10 concurrent to be polite)
    const fullTasks = await Promise.all(
      rawTasks.slice(0, 40).map(async (t) => {
        try {
          const r = await unsignedGet(`/v1/tasks/${t.task_id}`);
          const full = (r.body as { task?: { description?: string } })?.task;
          return { ...t, description: full?.description || "" };
        } catch {
          return { ...t, description: "" };
        }
      }),
    );

    // Classify each
    const classified = fullTasks.map((t) =>
      classifyTask(t as TaskSummary & { description: string }, (t as { description: string }).description || ""),
    );

    // Aggregate by classification
    const honest = classified.filter((t) => t.classification === "honest");
    const scamPattern = classified.filter((t) => t.classification === "scam_pattern");
    const unknown = classified.filter((t) => t.classification === "unknown");

    // Honest paid tasks (the gold) — bounty set + escrow funded
    const honestPaid = honest.filter((t) => t.bounty?.amount_display && t.escrow?.status === "funded");

    // Quick wins — honest + matches our capabilities + quick effort
    const quickWins = honest.filter(
      (t) => t.matches_our_capabilities && t.estimated_effort === "quick",
    );

    // Honorable mentions — honest + matches our capabilities (any effort)
    const matchingHonest = honest.filter((t) => t.matches_our_capabilities);

    return NextResponse.json(
      {
        ok: true,
        scanned_at: new Date().toISOString(),
        scan_duration_ms: Date.now() - startedAt,
        totals: {
          scanned: classified.length,
          honest: honest.length,
          scam_pattern: scamPattern.length,
          unknown: unknown.length,
          honest_paid: honestPaid.length,
          quick_wins: quickWins.length,
          matching_our_capabilities: matchingHonest.length,
        },
        honest_paid_tasks: honestPaid.map((t) => ({
          task_id: t.task_id,
          title: t.title,
          creator: typeof t.creator === "string" ? t.creator : t.creator?.name || t.creator?.id,
          bounty: t.bounty,
          escrow: t.escrow,
          required_capabilities: t.required_capabilities,
          our_caps_overlap: t.our_caps_overlap,
          expires_at: t.expires_at,
          claimable: t.claimable,
          classification_reasons: t.reasons,
        })),
        quick_wins: quickWins.map((t) => ({
          task_id: t.task_id,
          title: t.title,
          creator: typeof t.creator === "string" ? t.creator : t.creator?.name || t.creator?.id,
          category: t.category,
          required_capabilities: t.required_capabilities,
          our_caps_overlap: t.our_caps_overlap,
          estimated_effort: t.estimated_effort,
          expires_at: t.expires_at,
          claimable: t.claimable,
        })),
        matching_honest_tasks: matchingHonest.map((t) => ({
          task_id: t.task_id,
          title: t.title,
          category: t.category,
          required_capabilities: t.required_capabilities,
          our_caps_overlap: t.our_caps_overlap,
          estimated_effort: t.estimated_effort,
          expires_at: t.expires_at,
          claimable: t.claimable,
        })),
        scam_pattern_tasks: scamPattern.map((t) => ({
          task_id: t.task_id,
          title: t.title,
          creator: typeof t.creator === "string" ? t.creator : t.creator?.name || t.creator?.id,
          bounty: t.bounty,
          red_flags: t.reasons.filter((r) => r.includes("red flag")),
        })),
      },
      {
        headers: {
          "Cache-Control": "no-store",
          "X-Scan-Result": `${honestPaid.length} honest paid, ${quickWins.length} quick wins`,
        },
      },
    );
  } catch (e) {
    return NextResponse.json(
      {
        ok: false,
        error: e instanceof Error ? e.message : "Unknown error",
        scanned_at: new Date().toISOString(),
      },
      { status: 500 },
    );
  }
}
