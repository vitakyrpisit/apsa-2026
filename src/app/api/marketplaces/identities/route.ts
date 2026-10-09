import { NextResponse } from "next/server";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { existsSync } from "node:fs";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * GET /api/marketplaces/identities
 *
 * Returns the complete map of our agent's identities across all known
 * AI agent marketplaces, with live profile data where we have credentials.
 *
 * Each marketplace entry includes:
 *  - platform: name
 *  - status: registered | auth_only | dead | spa_only | not_an_agent_market | not_attempted
 *  - agent_id: identifier on the platform
 *  - profile_url: public profile link (where it exists)
 *  - api_base: API root used for live queries
 *  - credential_path: where the credentials live (NEVER exposed via this endpoint)
 *  - registered_at, capabilities, wallet (where applicable)
 *  - live: a fresh fetch when the platform has a public GET endpoint for our profile
 *
 * This is the single source of truth for the dashboard "Marketplaces" tab.
 */

const PROJECT = "/home/z/my-project";

interface CredentialFile {
  [key: string]: unknown;
}

async function readJson(path: string): Promise<CredentialFile | null> {
  try {
    if (!existsSync(path)) return null;
    const txt = await readFile(path, "utf8");
    return JSON.parse(txt) as CredentialFile;
  } catch {
    return null;
  }
}

// Public, unsigned profile fetches (no secrets on the wire)
async function fetchJson(url: string, timeoutMs = 8000): Promise<unknown | null> {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    const r = await fetch(url, {
      headers: {
        "User-Agent": "APSA-2026/1.0 (+https://apsa-2026.vercel.app)",
        Accept: "application/json",
      },
      signal: ctrl.signal,
      cache: "no-store",
    });
    clearTimeout(t);
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  }
}

interface MarketplaceIdentity {
  platform: string;
  slug: string;
  status:
    | "registered"
    | "auth_only"
    | "dead"
    | "spa_only"
    | "not_an_agent_market"
    | "not_attempted";
  agent_id: string | null;
  agent_id_field?: string; // which credential field holds the ID
  profile_url: string | null;
  api_base: string;
  credential_path: string | null;
  registered_at: string | null;
  capabilities: string[] | null;
  payout_wallet: string | null;
  payout_wallet_verified: boolean | null;
  reputation_score: number | null;
  reputation_label: string | null;
  live: {
    fetched_at: string;
    profile_reachable: boolean;
    fields_seen: string[];
    raw_excerpt?: unknown;
  } | null;
  notes: string | null;
}

export async function GET() {
  const startedAt = Date.now();
  const identities: MarketplaceIdentity[] = [];

  // ── 1. BasedAgents (signed profile fetch lives at /api/basedagents/status) ──
  // v5 re-registered 2026-10-09 after sandbox wipe destroyed v2/v4 keypairs.
  const baCreds = await readJson(
    join(PROJECT, ".basedagents/keys/apsa-2026-bugfixer-v5-keypair.json"),
  );
  identities.push({
    platform: "BasedAgents",
    slug: "basedagents",
    status: baCreds ? "registered" : "not_attempted",
    agent_id: "ag_EuuNoKptr2m6kBsmF1ZWZZFCPhaWnzkQ1iWj4N4dPiJh",
    agent_id_field: "agent_id",
    profile_url:
      "https://basedagents.ai/agents/ag_EuuNoKptr2m6kBsmF1ZWZZFCPhaWnzkQ1iWj4N4dPiJh",
    api_base: "https://api.basedagents.ai",
    credential_path: ".basedagents/keys/apsa-2026-bugfixer-v5-keypair.json",
    registered_at: "2026-10-09T06:06:00.000Z",
    capabilities: ["research", "code", "security", "testing", "documentation"],
    payout_wallet: "0xfA82DD7B785706975642e367A017073fC399f0Df",
    payout_wallet_verified: true,
    reputation_score: 0,
    reputation_label: "new (0/5)",
    live: null, // live fetch is on /api/basedagents/status
    notes:
      "v5 identity (receive-only Base wallet 0xfA82...f0Df, EIP-191 verified). Predecessors v2/v4 orphaned by sandbox wipe — keypairs unrecoverable. Keypair backed up to 3 locations. Unified scanner at /api/marketplaces/scan.",
  });

  // ── 2. Agent Souk ──
  const asCreds = await readJson(join(PROJECT, ".agentsouk/credentials.json"));
  const asAgentId = (asCreds?.agent_id as string) || null;
  identities.push({
    platform: "Agent Souk",
    slug: "agentsouk",
    status: asAgentId ? "registered" : "not_attempted",
    agent_id: asAgentId,
    agent_id_field: "agent_id",
    profile_url: asAgentId ? `https://agentsouk.dev/agents/${asAgentId}` : null,
    api_base: "https://api.agentsouk.dev",
    credential_path: ".agentsouk/credentials.json",
    registered_at: (asCreds?.created_at as string) || "2026-10-08T01:54:06Z",
    capabilities: ["research", "code", "security", "testing", "documentation"],
    payout_wallet: null, // wallet binding requires separate POST /v1/agents/me/wallet-address with EIP-191 sig
    payout_wallet_verified: null,
    reputation_score: 0,
    reputation_label: "trust_tier 0",
    live: null,
    notes:
      "did:key identity, Ed25519. Wallet-to-wallet USDC on Base (no custody). NPM CLI: agentsouk. MCP server + skill.md + openapi.json.",
  });

  // ── 3. AgentPact ──
  const apCreds = await readJson(join(PROJECT, ".agentpact/credentials.json"));
  const apAgentId = (apCreds?.agentId as string) || null;
  // Live profile fetch — AgentPact GET /api/agents/{id} doesn't require auth for public fields
  const apLiveRaw = apAgentId
    ? await fetchJson(`https://api.agentpact.xyz/api/agents/${apAgentId}`)
    : null;
  const apLive = apLiveRaw as Record<string, unknown> | null;
  identities.push({
    platform: "AgentPact",
    slug: "agentpact",
    status: apAgentId ? "registered" : "not_attempted",
    agent_id: apAgentId,
    agent_id_field: "agentId",
    profile_url: apAgentId ? `https://agentpact.xyz/agents/${apAgentId}` : null,
    api_base: "https://api.agentpact.xyz",
    credential_path: ".agentpact/credentials.json",
    registered_at: "2026-10-08T01:57:38.436Z",
    capabilities: null, // not in public profile response
    payout_wallet: (apLive?.owner_wallet_address as string) || null,
    payout_wallet_verified: null,
    reputation_score:
      (apLive?.reputation_score as string | number | undefined) !== undefined
        ? Number(apLive?.reputation_score)
        : 0,
    reputation_label: (apLive?.trustTier as { label?: string } | undefined)?.label || "new",
    live: {
      fetched_at: new Date().toISOString(),
      profile_reachable: !!apLive,
      fields_seen: apLive ? Object.keys(apLive) : [],
    },
    notes:
      "UUID agentId + apiKey. Has /api/offers, /api/needs, /api/deals, /api/payments, /api/disputes. POST /api/auth/register → apiKey.",
  });

  // ── 4. Toku.agency ──
  const tokuCreds = await readJson(join(PROJECT, ".toku/credentials.json"));
  const tokuAgentId = (tokuCreds?.agent_id as string) || null;
  identities.push({
    platform: "Toku.agency",
    slug: "toku",
    status: tokuAgentId ? "registered" : "not_attempted",
    agent_id: tokuAgentId,
    agent_id_field: "agent_id",
    profile_url: (tokuCreds?.profileUrl as string) || null,
    api_base: "https://toku.agency",
    credential_path: ".toku/credentials.json",
    registered_at: (tokuCreds?.registered_at as string) || "2026-10-08T02:00:00Z",
    capabilities: null,
    payout_wallet: null,
    payout_wallet_verified: null,
    reputation_score: 0,
    reputation_label: "new",
    live: null,
    notes:
      "self-service registration POST /api/agents/register (no ownerEmail needed). Has /api/agents/webhooks, /api/agents/claim, /api/agents/bidding. setupScore: 1/5 (more setup needed).",
  });

  // ── 5. Mercatai ──
  const merCreds = await readJson(join(PROJECT, ".mercatai/credentials.json"));
  const merAgentId = (merCreds?.id as string) || null;
  identities.push({
    platform: "Mercatai",
    slug: "mercatai",
    status: merAgentId ? "registered" : "not_attempted",
    agent_id: (merCreds?.agent_id as string) || merAgentId,
    agent_id_field: "agent_id",
    profile_url: merAgentId ? `https://mercatai.eu/agents/${merCreds?.agent_id}` : null,
    api_base: "https://mercatai.eu",
    credential_path: ".mercatai/credentials.json",
    registered_at: (merCreds?.registered_at as string) || "2026-10-08T02:04:00Z",
    capabilities: ["research", "code_review", "data_analysis"],
    payout_wallet: null, // Stripe Connect — operator must complete KYC onboarding
    payout_wallet_verified: null,
    reputation_score: 0,
    reputation_label: "new",
    live: null,
    notes:
      "EU B2B marketplace, 0% fee on first 10 tasks. Stripe Connect onboarding required for payouts (Standard account, EU countries). Post /api/v1/agents → id + api_key. Bid at /api/v1/bids, deliver at /api/v1/tasks/{id}/deliver.",
  });

  // ── 6. BountyBook (auth-only; agent identity = wallet address) ──
  identities.push({
    platform: "BountyBook",
    slug: "bountybook",
    status: "auth_only",
    agent_id: "0x869734666c78B90Aa9fE0D202E568b870f25e575", // agent identity IS the wallet
    agent_id_field: "wallet_address",
    profile_url:
      "https://api.bountybook.ai/agents?address=0x869734666c78B90Aa9fE0D202E568b870f25e575",
    api_base: "https://api.bountybook.ai",
    credential_path: ".basedagents/wallets/apsa-2026-agent-wallet.json",
    registered_at: "2026-10-08T01:55:00Z",
    capabilities: null,
    payout_wallet: "0x869734666c78B90Aa9fE0D202E568b870f25e575",
    payout_wallet_verified: true,
    reputation_score: null,
    reputation_label: "newcomer",
    live: null,
    notes:
      "Auth flow: GET /auth/nonce?address=0x... → sign nonce with wallet (EIP-191 personal_sign) → POST /auth/verify → bearer token. No separate registration — agent identity IS the wallet address. 1801 agents on the board.",
  });

  // ── 7. APSA-2026 service on Agent402 router (via APSA-2026 service metadata) ──
  identities.push({
    platform: "Agent402 router",
    slug: "agent402",
    status: "registered",
    agent_id: "apsa-2026-sentinelshield",
    agent_id_field: "service_id",
    profile_url: "https://apsa-2026.vercel.app/api/agent402/router",
    api_base: "https://apsa-2026.vercel.app",
    credential_path: null,
    registered_at: "2026-10-07T15:27:04Z",
    capabilities: ["security", "market", "trading", "business"],
    payout_wallet: "0x829f877daAb94D766BB2b8511ad486C40f2C2BDA",
    payout_wallet_verified: true,
    reputation_score: 0,
    reputation_label: "trial_tier_active",
    live: null,
    notes:
      "APSA-2026 service exposes router-eligibility metadata via /api/agent402/router. routerDispatchEligible=true, unprovenTier=true, toolCount=5. Trial tier pricing $0.05 USDC (was $9.50).",
  });

  // ── Tried and failed ──
  const failed: MarketplaceIdentity[] = [
    {
      platform: "ClawGig.ai",
      slug: "clawgig",
      status: "dead",
      agent_id: null,
      profile_url: "https://clawgig.ai",
      api_base: "https://clawgig.ai",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes:
        "Vercel deployment disabled (x-vercel-error: DEPLOYMENT_DISABLED). Site dead as of 2026-10-08.",
    },
    {
      platform: "Daydreams TaskMarket",
      slug: "daydreams",
      status: "dead",
      agent_id: null,
      profile_url: "https://docs-market.daydreams.systems",
      api_base: "https://docs-market.daydreams.systems",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes: "Returns 404 'Application not found' — service not deployed.",
    },
    {
      platform: "Atrest.ai",
      slug: "atrest",
      status: "spa_only",
      agent_id: null,
      profile_url: "https://atrest.ai",
      api_base: "https://atrest.ai",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes:
        "Next.js SPA. Has /onboarding route but no public API endpoint for self-registration. Requires web UI.",
    },
    {
      platform: "Moltverr",
      slug: "moltverr",
      status: "spa_only",
      agent_id: null,
      profile_url: "https://moltverr.com",
      api_base: "https://moltverr.com",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes:
        "Next.js SPA. Has /gigs, /agents, /dashboard routes but no public API endpoint for self-registration.",
    },
    {
      platform: "AgentHire.ai",
      slug: "agenthire",
      status: "spa_only",
      agent_id: null,
      profile_url: "https://agenthire.ai",
      api_base: "https://agenthire.ai",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes: "Next.js SPA, no public registration API.",
    },
    {
      platform: "AgentWorld",
      slug: "agentworld",
      status: "spa_only",
      agent_id: null,
      profile_url: "https://agentworld.com",
      api_base: "https://agentworld.com",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes: "Next.js SPA, no public registration API.",
    },
    {
      platform: "OpenWork.io",
      slug: "openwork",
      status: "spa_only",
      agent_id: null,
      profile_url: "https://openwork.io",
      api_base: "https://openwork.io",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes: "Next.js SPA, no public registration API.",
    },
    {
      platform: "BotWork.com",
      slug: "botwork",
      status: "dead",
      agent_id: null,
      profile_url: "https://botwork.com",
      api_base: "https://botwork.com",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes: "Returns NOT_FOUND 404. Site is dead.",
    },
    {
      platform: "WorkProtocol.ai",
      slug: "workprotocol",
      status: "dead",
      agent_id: null,
      profile_url: "https://workprotocol.ai",
      api_base: "https://workprotocol.ai",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes: "Empty response on probe. Site unreachable or no API.",
    },
    {
      platform: "Algora.io",
      slug: "algora",
      status: "not_an_agent_market",
      agent_id: null,
      profile_url: "https://algora.io/bounties",
      api_base: "https://algora.io",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes:
        "Human-focused GitHub issue bounty platform (Elixir/Phoenix app). Not an AI agent marketplace. Would need browser-based human auth.",
    },
    {
      platform: "Near.ai",
      slug: "nearai",
      status: "not_attempted",
      agent_id: null,
      profile_url: "https://near.ai",
      api_base: "https://near.ai",
      credential_path: null,
      registered_at: null,
      capabilities: null,
      payout_wallet: null,
      payout_wallet_verified: null,
      reputation_score: null,
      reputation_label: null,
      live: null,
      notes:
        "Has /v1/model/list and /cloud/signin. Complex auth — requires cloud.near.ai sign-in (OAuth-style), not direct API registration. Mostly a model marketplace, not an agent task marketplace.",
    },
  ];

  const all = [...identities, ...failed];

  return NextResponse.json(
    {
      ok: true,
      agent_name: "APSA-2026 SentinelShield",
      summary: {
        total_platforms: all.length,
        registered: all.filter((i) => i.status === "registered").length,
        auth_only: all.filter((i) => i.status === "auth_only").length,
        dead: all.filter((i) => i.status === "dead").length,
        spa_only: all.filter((i) => i.status === "spa_only").length,
        not_an_agent_market: all.filter((i) => i.status === "not_an_agent_market").length,
        not_attempted: all.filter((i) => i.status === "not_attempted").length,
        payout_wallets_used: Array.from(
          new Set(
            all
              .map((i) => i.payout_wallet)
              .filter((w): w is string => !!w),
          ),
        ),
      },
      identities: all,
      fetched_at: new Date().toISOString(),
      fetch_duration_ms: Date.now() - startedAt,
    },
    {
      headers: {
        "Cache-Control": "no-store",
        "X-Platforms-Registered": String(
          all.filter((i) => i.status === "registered").length,
        ),
      },
    },
  );
}
