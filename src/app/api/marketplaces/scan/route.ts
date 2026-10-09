import { NextResponse } from "next/server";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { deserializeKeypair, signRequest, type AgentKeypair } from "basedagents";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

// ============================================================================
// Unified marketplace scanner — polls BasedAgents + TaskBounty every 5 min.
// Surfaces honest paid tasks ("the gold") the moment they appear.
// Auto-claims when EV > 0 (operator's directive section 39).
// ============================================================================

const BASEDAGENTS_API = "https://api.basedagents.ai";
const TASKBOUNTY_MCP = "https://www.task-bounty.com/api/mcp/v1";
const TASKBOUNTY_API_KEY = process.env.TASKBOUNTY_API_KEY || "";
const BASEDAGENTS_AGENT_ID = "ag_EuuNoKptr2m6kBsmF1ZWZZFCPhaWnzkQ1iWj4N4dPiJh";
const BASEDAGENTS_KEYPAIR_PATH =
  "/home/z/my-project/.basedagents/keys/apsa-2026-bugfixer-v5-keypair.json";
const STATE_FILE = "/home/z/my-project/.marketplace-state/scan-results.json";

const OUR_CAPS = ["research", "code", "security", "testing", "documentation"];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function loadKeypair(): Promise<AgentKeypair | null> {
  try {
    if (!existsSync(BASEDAGENTS_KEYPAIR_PATH)) return null;
    const json = await readFile(BASEDAGENTS_KEYPAIR_PATH, "utf8");
    return deserializeKeypair(json);
  } catch {
    return null;
  }
}

async function signedGet(path: string, keypair: AgentKeypair) {
  const headers = await signRequest(keypair, "GET", path, "");
  const r = await fetch(`${BASEDAGENTS_API}${path}`, {
    headers: {
      "User-Agent": "APSA-2026/1.0 (+https://apsa-2026.vercel.app)",
      ...headers,
    },
    cache: "no-store",
  });
  return { status: r.status, ok: r.ok, body: r.ok ? await r.json() : null };
}

async function unsignedGet(path: string) {
  const r = await fetch(`${BASEDAGENTS_API}${path}`, {
    headers: {
      "User-Agent": "APSA-2026/1.0 (+https://apsa-2026.vercel.app)",
      Accept: "application/json",
    },
    cache: "no-store",
  });
  return { status: r.status, ok: r.ok, body: r.ok ? await r.json() : null };
}

async function taskbountyMcpCall(toolName: string, args: Record<string, unknown> = {}) {
  if (!TASKBOUNTY_API_KEY) return null;
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 10000);
    const r = await fetch(TASKBOUNTY_MCP, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "User-Agent": "APSA-2026/1.0",
        Authorization: `Bearer ${TASKBOUNTY_API_KEY}`,
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: 1,
        method: "tools/call",
        params: { name: toolName, arguments: args },
      }),
      signal: ctrl.signal,
      cache: "no-store",
    });
    clearTimeout(t);
    if (!r.ok) return null;
    const d = await r.json();
    const text = d?.result?.content?.[0]?.text || "";
    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// BasedAgents scan + classify
// ---------------------------------------------------------------------------

interface BATask {
  task_id: string;
  title: string;
  creator: { name?: string; id?: string } | string | null;
  bounty: { amount_display?: string; token?: string; network?: string } | null;
  escrow: { status?: string } | null;
  required_capabilities: string[];
  expires_at: string | null;
  claimable: boolean;
  category: string;
  description?: string;
}

interface ClassifiedBATask extends BATask {
  classification: "honest_paid" | "honest_free" | "scam_pattern" | "unknown";
  reasons: string[];
  matches_our_caps: boolean;
  our_caps_overlap: string[];
  estimated_ev_usd: number;
}

function classifyBATask(t: BATask, description: string): ClassifiedBATask {
  const creatorRaw = t.creator;
  const creator =
    typeof creatorRaw === "string"
      ? creatorRaw
      : creatorRaw?.name || creatorRaw?.id || "";
  const reasons: string[] = [];
  let classification: ClassifiedBATask["classification"] = "unknown";

  // Creator-based
  if (creator.includes("BasedAgents")) {
    classification = "honest_free"; // BasedAgents_bot tasks are always free
    reasons.push("creator is BasedAgents project automation (always free reputation tasks)");
  } else if (
    creator.toLowerCase().includes("industrial sentinel") ||
    creator.toLowerCase().includes("industrialsentinelac")
  ) {
    classification = "scam_pattern";
    reasons.push("creator matches Industrial Sentinel pattern");
  } else if (creator === "field-research-desk" || creator.includes("field-research")) {
    // field-research-desk posted the $1.00 "Independent acceptance check" task that was paid
    classification = "honest_paid";
    reasons.push("creator is field-research-desk (proven paid $1.00 task history)");
  }

  // Content-based scam detection
  const descLower = description.toLowerCase();
  const scamKeywords = [
    { kw: "ghcr.io/industrial-platform", reason: "references unverified industrial-platform-ai container" },
    { kw: "sentinel_cashback_mode", reason: "requires SENTINEL_CASHBACK_MODE env" },
    { kw: "sentinel_revenue_guard_mode", reason: "requires SENTINEL_REVENUE_GUARD_MODE env" },
    { kw: "no escrow required upfront", reason: "bounty not pre-funded (no payment guarantee)" },
    { kw: "sign-at-accept", reason: "bounty is sign-at-accept (not escrowed)" },
    { kw: "bounded payer configuration", reason: "asks to delegate wallet payment authority" },
  ];
  for (const { kw, reason } of scamKeywords) {
    if (descLower.includes(kw)) {
      reasons.push(`red flag: ${reason}`);
      if (classification !== "honest_paid" && classification !== "honest_free") {
        classification = "scam_pattern";
      }
    }
  }

  // Bounty + escrow check
  const hasBounty = !!t.bounty?.amount_display;
  const escrowStatus = t.escrow?.status;
  if (hasBounty && escrowStatus === "funded") {
    if (classification === "unknown" || classification === "honest_free") {
      classification = "honest_paid";
      reasons.push(`bounty $${t.bounty?.amount_display} with escrow=funded (real paid task)`);
    }
  }

  // Capabilities overlap
  const overlap = (t.required_capabilities || []).filter((c) => OUR_CAPS.includes(c));

  // EV estimate (very rough, calibrated later from real outcomes)
  let ev = 0;
  if (classification === "honest_paid") {
    const bountyUsd = parseFloat(t.bounty?.amount_display || "0");
    // Per ai-freelancer-os engine: EV = B · P(win) · P(success) · P(pay) · (1-fee) − costs
    // BasedAgents fee = 0% (verified). P(pay) high if escrow=funded.
    // Initial priors: P(success)=0.5 (no track record yet), P(win)=1 (exclusive_claim), P(pay)=0.95
    const p_success = 0.5;
    const p_win = 1.0; // exclusive claim
    const p_pay = 0.95;
    const fee = 0.0;
    const llm_cost = 0.10; // ~$0.10 LLM cost for small task
    const compute_cost = 0.01;
    ev = bountyUsd * p_win * p_success * p_pay * (1 - fee) - llm_cost - compute_cost;
    reasons.push(`EV estimate: $${ev.toFixed(3)} (bounty $${bountyUsd} × P(win)=1.0 × P(success)=0.5 × P(pay)=0.95 - costs $0.11)`);
  }

  return {
    ...t,
    classification,
    reasons,
    matches_our_caps: overlap.length > 0,
    our_caps_overlap: overlap,
    estimated_ev_usd: ev,
  };
}

// ---------------------------------------------------------------------------
// TaskBounty scan
// ---------------------------------------------------------------------------

interface TBBounty {
  task_id?: string;
  id?: string;
  title: string;
  reward?: number;
  bounty_amount?: number;
  repo?: string;
  github_repo_url?: string;
  language?: string;
  slug?: string;
}

interface TBMission {
  id: string;
  title: string;
  description: string;
  reward_type: string;
  reward_cents: number | null;
  category: string;
  status: string;
  required_capabilities: string[];
  deadline: string | null;
}

interface ClassifiedTBMission extends TBMission {
  classification: "honest_paid" | "scam_pattern" | "unpaid";
  reasons: string[];
}

function classifyTBMission(m: TBMission): ClassifiedTBMission {
  const reasons: string[] = [];
  let classification: ClassifiedTBMission["classification"] = "unpaid";

  // Unpaid missions are honest (just no money)
  if (m.reward_type === "unpaid") {
    return { ...m, classification: "unpaid", reasons: ["reward_type=unpaid"] };
  }

  // Paid mission — check for scam patterns
  const titleLower = m.title.toLowerCase();
  const descLower = (m.description || "").toLowerCase();

  const scamFlags: { pattern: RegExp; reason: string }[] = [
    { pattern: /t\.me\//i, reason: "contains Telegram referral link (t.me/)" },
    { pattern: /\$?\d{4,}.*x+/i, reason: "title is placeholder like $100000xxxxxxxx" },
    { pattern: /bot.*robot|ref_|referral/i, reason: "contains bot/referral keywords" },
  ];

  let isScam = false;
  for (const { pattern, reason } of scamFlags) {
    if (pattern.test(m.title) || pattern.test(m.description || "")) {
      reasons.push(`red flag: ${reason}`);
      isScam = true;
    }
  }

  // Too good to be true: high reward + no capabilities + no acceptance criteria
  const rewardUsd = (m.reward_cents || 0) / 100;
  if (rewardUsd >= 100 && m.required_capabilities.length === 0 && (m as { acceptance_criteria?: string[] }).acceptance_criteria?.length === 0) {
    reasons.push(`red flag: $${rewardUsd} reward but no required capabilities and no acceptance criteria (too good to be true)`);
    isScam = true;
  }

  // Expired deadline
  if (m.deadline) {
    const dl = new Date(m.deadline);
    if (dl < new Date()) {
      reasons.push(`deadline expired: ${m.deadline}`);
      // Expired doesn't make it a scam, just unavailable
    }
  }

  if (isScam) {
    classification = "scam_pattern";
  } else {
    classification = "honest_paid";
    reasons.push(`reward_type=${m.reward_type}, $${rewardUsd.toFixed(2)}, status=${m.status}`);
  }

  return { ...m, classification, reasons };
}

// ---------------------------------------------------------------------------
// State persistence
// ---------------------------------------------------------------------------

interface ScanState {
  scanned_at: string;
  scan_duration_ms: number;
  basedagents: {
    total_tasks: number;
    honest_paid: number;
    honest_free: number;
    scam_pattern: number;
    unknown: number;
    best_paid_task: ClassifiedBATask | null;
    all_honest_paid: ClassifiedBATask[];
  };
  taskbounty: {
    api_key_configured: boolean;
    total_bounties: number;
    total_missions: number;
    paid_missions: number;
    best_bounty: TBBounty | null;
    all_bounties: TBBounty[];
    actor_id: string | null;
  };
  next_scan_in_seconds: number;
  auto_claim_pending: boolean;
}

async function loadState(): Promise<ScanState | null> {
  try {
    if (!existsSync(STATE_FILE)) return null;
    return JSON.parse(await readFile(STATE_FILE, "utf8"));
  } catch {
    return null;
  }
}

async function saveState(state: ScanState): Promise<void> {
  try {
    await mkdir(join(STATE_FILE, ".."), { recursive: true });
    await writeFile(STATE_FILE, JSON.stringify(state, null, 2), { mode: 0o600 });
  } catch {
    // best-effort
  }
}

// ---------------------------------------------------------------------------
// Main scanner
// ---------------------------------------------------------------------------

async function scan(): Promise<ScanState> {
  const startedAt = Date.now();

  // ---- BasedAgents ----
  const tasksRes = await unsignedGet(`/v1/tasks?status=open&limit=100`);
  const rawBATasks: BATask[] = tasksRes.ok ? tasksRes.body?.tasks || [] : [];

  // Fetch descriptions for classification (cap at 40 to be polite)
  const baWithDescriptions = await Promise.all(
    rawBATasks.slice(0, 40).map(async (t) => {
      try {
        const r = await unsignedGet(`/v1/tasks/${t.task_id}`);
        const full = r.body?.task;
        return { ...t, description: full?.description || "" };
      } catch {
        return { ...t, description: "" };
      }
    }),
  );

  const classifiedBA = baWithDescriptions.map((t) =>
    classifyBATask(t as BATask & { description: string }, (t as { description: string }).description || ""),
  );

  const honest_paid = classifiedBA.filter((t) => t.classification === "honest_paid");
  const honest_free = classifiedBA.filter((t) => t.classification === "honest_free");
  const scam_pattern = classifiedBA.filter((t) => t.classification === "scam_pattern");
  const unknown = classifiedBA.filter((t) => t.classification === "unknown");

  // Best paid task by EV
  const best_paid_task = honest_paid.length > 0
    ? honest_paid.reduce((a, b) => (b.estimated_ev_usd > a.estimated_ev_usd ? b : a))
    : null;

  // ---- TaskBounty ----
  const tbBountiesRaw = await taskbountyMcpCall("list_open_bounties", { limit: 50 });
  let tbBounties: TBBounty[] = [];
  if (tbBountiesRaw) {
    const data = tbBountiesRaw?.data || tbBountiesRaw;
    if (Array.isArray(data)) tbBounties = data;
    else if (data?.items) tbBounties = data.items;
  }

  const tbMissionsRaw = await taskbountyMcpCall("browse_missions", { limit: 50 });
  let tbMissions: TBMission[] = [];
  if (tbMissionsRaw) {
    const data = tbMissionsRaw?.data || tbMissionsRaw;
    if (data?.missions) tbMissions = data.missions;
    else if (Array.isArray(data)) tbMissions = data;
  }

  // Classify missions
  const classifiedMissions = tbMissions.map(classifyTBMission);
  const honest_paid_missions = classifiedMissions.filter((m) => m.classification === "honest_paid");
  const scam_missions = classifiedMissions.filter((m) => m.classification === "scam_pattern");
  const unpaid_missions = classifiedMissions.filter((m) => m.classification === "unpaid");

  const workspaceRaw = await taskbountyMcpCall("get_hiring_workspace", {});
  const actor_id = workspaceRaw?.data?.actor_id || null;

  const best_bounty = tbBounties.length > 0 ? tbBounties[0] : null;

  const state: ScanState = {
    scanned_at: new Date().toISOString(),
    scan_duration_ms: Date.now() - startedAt,
    basedagents: {
      total_tasks: classifiedBA.length,
      honest_paid: honest_paid.length,
      honest_free: honest_free.length,
      scam_pattern: scam_pattern.length,
      unknown: unknown.length,
      best_paid_task,
      all_honest_paid: honest_paid,
    },
    taskbounty: {
      api_key_configured: !!TASKBOUNTY_API_KEY,
      total_bounties: tbBounties.length,
      total_missions: tbMissions.length,
      paid_missions: honest_paid_missions.length,
      scam_missions: scam_missions.length,
      unpaid_missions: unpaid_missions.length,
      best_bounty,
      all_bounties: tbBounties,
      actor_id,
    },
    next_scan_in_seconds: 300,
    auto_claim_pending: !!best_paid_task && best_paid_task.estimated_ev_usd > 0,
  };

  await saveState(state);
  return state;
}

// ---------------------------------------------------------------------------
// HTTP handlers
// ---------------------------------------------------------------------------

export async function GET() {
  // Return latest state (fast) or trigger fresh scan if stale/missing
  const existing = await loadState();
  const stale =
    !existing ||
    Date.now() - new Date(existing.scanned_at).getTime() > 5 * 60_000;

  const state = stale ? await scan() : existing;
  return NextResponse.json(state, {
    headers: {
      "Cache-Control": "no-store",
      "X-Scan-Stale": stale ? "true" : "false",
      "X-Auto-Claim-Pending": state.auto_claim_pending ? "true" : "false",
    },
  });
}

export async function POST() {
  // Force fresh scan
  const state = await scan();
  return NextResponse.json(state, {
    headers: {
      "Cache-Control": "no-store",
      "X-Scan-Forced": "true",
    },
  });
}
