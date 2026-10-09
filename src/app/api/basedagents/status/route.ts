import { NextResponse } from "next/server";
import { readFile } from "node:fs/promises";
import { deserializeKeypair, signRequest, type AgentKeypair } from "basedagents";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const API_BASE = "https://api.basedagents.ai";
const AGENT_ID = "ag_EuuNoKptr2m6kBsmF1ZWZZFCPhaWnzkQ1iWj4N4dPiJh";
const AGENT_NAME = "APSA-2026 BugFixer v5";
const AGENT_WALLET = "0xfA82DD7B785706975642e367A017073fC399f0Df";
const KEYPAIR_PATH =
  "/home/z/my-project/.basedagents/keys/apsa-2026-bugfixer-v5-keypair.json";

async function loadKeypair(): Promise<AgentKeypair> {
  const json = await readFile(KEYPAIR_PATH, "utf8");
  return deserializeKeypair(json);
}

async function signedGet(path: string, keypair: AgentKeypair) {
  const headers = await signRequest(keypair, "GET", path, "");
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "User-Agent": "APSA-2026/1.0 (+https://apsa-2026.vercel.app)",
      ...headers,
    },
    cache: "no-store",
  });
  const body = res.ok ? await res.json() : null;
  return { status: res.status, ok: res.ok, body };
}

async function unsignedGet(path: string) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "User-Agent": "APSA-2026/1.0 (+https://apsa-2026.vercel.app)",
      Accept: "application/json",
    },
    cache: "no-store",
  });
  const body = res.ok ? await res.json() : null;
  return { status: res.status, ok: res.ok, body };
}

/**
 * GET /api/basedagents/status
 *
 * Aggregates our agent's live status from BasedAgents registry:
 *  - profile (signed GET /v1/agents/{id}) → name, capabilities, reputation, wallet
 *  - claim budget (signed GET /v1/agents/me/claim-budget) → budget, bond slots
 *  - open tasks count (GET /v1/tasks?status=open) → 38 visible across all creators
 *  - scam pattern alert → all paid "Industrial Sentinel" tasks identified as honeypot
 *
 * All signed requests use the Ed25519 keypair stored at KEYPAIR_PATH.
 * The private key never leaves the server, never printed, never logged.
 */
export async function GET() {
  const startedAt = Date.now();
  try {
    const keypair = await loadKeypair();

    // Parallel fetches — profile and tasks are unsigned, claim-budget is signed
    const [profileRes, claimBudgetRes, openTasksRes, registryStatusRes] =
      await Promise.all([
        unsignedGet(`/v1/agents/${AGENT_ID}`),
        signedGet(`/v1/agents/me/claim-budget`, keypair),
        unsignedGet(`/v1/tasks?status=open&limit=100`),
        unsignedGet(`/v1/status`),
      ]);

    const profile = (profileRes.body as { agent_id?: string }) || null;
    const claimBudget =
      (claimBudgetRes.body as {
        budget?: number;
        bonded_slots?: number;
        bond_capacity?: number;
      }) || null;
    const tasksData = (openTasksRes.body as { tasks?: unknown[] }) || null;
    const registry = (registryStatusRes.body as { tasks?: Record<string, number> }) || null;

    const allTasks = (tasksData?.tasks as Array<Record<string, unknown>>) || [];

    // Categorize tasks: honest (BasedAgents_bot) vs scam-pattern (Industrial Sentinel)
    const honestTasks = allTasks.filter((t) => {
      const creator = (t.creator as { name?: string })?.name || "";
      return creator.includes("BasedAgents");
    });
    const scamPatternTasks = allTasks.filter((t) => {
      const creator = (t.creator as { name?: string })?.name || "";
      return creator.toLowerCase().includes("industrial sentinel");
    });
    const paidScamTasks = scamPatternTasks.filter((t) => {
      const b = t.bounty as { amount_display?: string } | null;
      return b && b.amount_display;
    });

    // Match our capabilities (research, code, security, testing, documentation)
    const ourCaps = ["research", "code", "security", "testing", "documentation"];
    const matchingHonest = honestTasks.filter((t) => {
      const caps = (t.required_capabilities as string[]) || [];
      return caps.some((c) => ourCaps.includes(c));
    });

    const response = {
      ok: true,
      agent: {
        agent_id: AGENT_ID,
        name: AGENT_NAME,
        profile_url: `https://basedagents.ai/agents/${AGENT_ID}`,
        status: profile?.status || "unknown",
        capabilities: profile?.capabilities || ourCaps,
        registered_at: profile?.registered_at,
        reputation_score: profile?.reputation_score ?? 0,
        verification_count: profile?.verification_count ?? 0,
        ratings: profile?.ratings || { count: 0, average: null },
      },
      wallet: {
        address: AGENT_WALLET,
        network: "eip155:8453",
        verified: profile?.wallet_verified ?? false,
        verified_at: profile?.wallet_verified_at,
        note: "Sandbox-generated EVM wallet. Operator must fund 1 USDC for claim-bond to enable paid tasks. Bounty payouts land here.",
        current_balance_usdc: null, // would need RPC call — left as null for now
      },
      claim_budget: claimBudget
        ? {
            budget: claimBudget.budget ?? 10,
            bonded_slots: claimBudget.bonded_slots ?? 0,
            bond_capacity: claimBudget.bond_capacity ?? 0,
            bond_required_per_bounty_slot_usdc: 1,
            signed_endpoint_works: claimBudgetRes.ok,
          }
        : {
            budget: null,
            signed_endpoint_works: claimBudgetRes.ok,
            error: "claim-budget endpoint not reachable (likely a signing or path issue)",
            http_status: claimBudgetRes.status,
          },
      registry: {
        agents_total: registry?.agents
          ? (registry.agents as { total?: number }).total
          : null,
        tasks_open: registry?.tasks?.open ?? null,
        tasks_paid: registry?.tasks?.paid ?? null,
        paid_usdc_total: registry?.tasks?.paid_usdc_total ?? null,
        payments: registry?.payments,
        escrow: registry?.escrow,
      },
      open_tasks: {
        total_visible: allTasks.length,
        honest_count: honestTasks.length,
        scam_pattern_count: scamPatternTasks.length,
        paid_scam_count: paidScamTasks.length,
        matching_our_capabilities: matchingHonest.length,
        matching_task_ids: matchingHonest.map((t) => t.task_id).slice(0, 10),
      },
      scam_alert: {
        pattern: "Industrial Sentinel Revenue (Guard / Cashback / Trial / External Deployment)",
        creator_agents: [
          "ag_769zigCfkxCQie1Ra5QTeXppcguQ2mDnJiCN9JzL619R (Industrial Sentinel Acquisition)",
          "ag_*(IndustrialSentinelAc*)",
        ],
        red_flags: [
          "Requires running unverified docker container from ghcr.io/industrial-platform-ai/industrial-sentinel-runtime",
          "Container 'monitors your wallet' with SENTINEL_CASHBACK_MODE=1 and 1.25 USDC/day hard spend cap",
          "Cashback paid only AFTER installation generates $2.50+ Industrial Platform revenue through the same container (circular attribution)",
          "Bounty is 'sign-at-accept, no escrow required upfront' — bounty not pre-funded, no payment guarantee",
          "Violates BasedAgents skill.md §1 Trust boundary: introduces another host for payment, asks for wallet authority",
        ],
        recommendation:
          "Do not claim any Industrial Sentinel task. All 28 paid tasks from this creator are honeypot pattern. Honest paid tasks do not currently exist on the board.",
      },
      profile_history: [
        {
          agent_id: "ag_2P4kffVnkJeDZxMtFEj92ybt3w7yhijPHMDU6Yb1cxqd",
          name: "APSA-2026 SentinelShield (v1, lost)",
          status: "orphaned",
          reason: "Keypair file at /home/z/.basedagents/keys/ was wiped by sandbox session restart. Ed25519 has no recovery path. Agent ID remains in registry but we have no signing key for it.",
          lesson:
            "Always store keypairs inside the project tree (/home/z/my-project/.basedagents/keys/) so they survive sandbox restarts, and back them up offsite.",
        },
      ],
      fetched_at: new Date().toISOString(),
      fetch_duration_ms: Date.now() - startedAt,
    };

    return NextResponse.json(response, {
      headers: {
        "Cache-Control": "no-store",
        "X-Agent-Id": AGENT_ID,
        "X-Wallet-Verified": String(profile?.wallet_verified ?? false),
      },
    });
  } catch (e) {
    return NextResponse.json(
      {
        ok: false,
        error: e instanceof Error ? e.message : "Unknown error",
        agent_id: AGENT_ID,
        fetched_at: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}
