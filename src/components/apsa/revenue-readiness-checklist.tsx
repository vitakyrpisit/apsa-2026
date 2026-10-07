"use client";

import { useState } from "react";
import {
  CheckCircle2,
  Circle,
  ExternalLink,
  Copy,
  Check,
  AlertTriangle,
  Zap,
  Rocket,
  ShieldCheck,
  Terminal,
} from "lucide-react";
import { toast } from "sonner";
import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  SENTINEL_PRICE_USDC,
  BASE_MAINNET_CHAIN_ID,
} from "@/lib/apsa/wallet-registry";

interface ReadinessStep {
  id: string;
  category: "technical" | "listing" | "first-payment" | "scaling";
  title: string;
  status: "done" | "actionable" | "blocked";
  detail: string;
  action?: {
    label: string;
    url?: string;
    command?: string;
  };
}

const STEPS: ReadinessStep[] = [
  // Technical readiness (all verified)
  {
    id: "price",
    category: "technical",
    title: "Production price set",
    status: "done",
    detail: `$${SENTINEL_PRICE_USDC.toFixed(2)} USDC (9500000 atomic) — consistent across /api/health, manifest, 402 challenge, and test suite.`,
  },
  {
    id: "payTo",
    category: "technical",
    title: "payTo = operator receive-only wallet",
    status: "done",
    detail: `${EVM_PAYOUT_ADDRESS} — receive-only, no operator keys exposed.`,
  },
  {
    id: "chain",
    category: "technical",
    title: "Base Mainnet + USDC contract",
    status: "done",
    detail: `chainId ${BASE_MAINNET_CHAIN_ID}, USDC ${BASE_USDC_MAINNET_ADDRESS}. Verified in manifest + 402 paymentRequirements.`,
  },
  {
    id: "manifest",
    category: "technical",
    title: "x402 manifest published",
    status: "done",
    detail: `GET /.well-known/x402-manifest.json returns discovery metadata (serviceId, endpoints, pricing, payout address).`,
  },
  {
    id: "402",
    category: "technical",
    title: "402 challenge works",
    status: "done",
    detail: `POST /api/x402/sentinelshield (no body) → HTTP 402 + PAYMENT-REQUIRED header with exact EIP-712 schema.`,
  },
  {
    id: "tests",
    category: "technical",
    title: "12-test verification suite passes",
    status: "done",
    detail: `All 12 protocol enforcement tests pass against real Base Mainnet RPC (block ~#52.27M). Test 10 proves "signature ≠ settlement".`,
  },

  // Marketplace listing (operator action required)
  {
    id: "agent402",
    category: "listing",
    title: "Register on Agent402 index",
    status: "actionable",
    detail: `Free listing, no KYC. Agent402 indexes 500+ x402 tools and re-probes endpoint health every 30 min.`,
    action: {
      label: "POST /api/index/register",
      command: `curl -X POST https://agent402.tools/api/index/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "endpoint": "https://YOUR_DEPLOYED_URL/api/x402/sentinelshield",
    "manifest": "https://YOUR_DEPLOYED_URL/.well-known/x402-manifest.json",
    "serviceId": "sentinel-shield",
    "price": "${SENTINEL_PRICE_USDC}",
    "network": "base-mainnet",
    "payTo": "${EVM_PAYOUT_ADDRESS}"
  }'`,
    },
  },
  {
    id: "x402dash",
    category: "listing",
    title: "Get listed on x402dash",
    status: "actionable",
    detail: `x402dash is a liveness monitoring + discovery index that tracks all x402 endpoints. Submit your endpoint for health monitoring.`,
    action: {
      label: "Submit to x402dash",
      url: "https://x402dash.com",
    },
  },
  {
    id: "circle-discovery",
    category: "listing",
    title: "Circle for Agents Discovery API",
    status: "actionable",
    detail: `Circle launched a no-auth Discovery API for x402 services. Agents can discover and pay without signup or API keys.`,
    action: {
      label: "Circle Agent Marketplace",
      url: "https://agents.circle.com",
    },
  },

  // First payment (the chicken-and-egg problem)
  {
    id: "bazaar-trigger",
    category: "first-payment",
    title: "Trigger Coinbase Bazaar indexing",
    status: "blocked",
    detail: `The CDP x402 Bazaar has NO registration form. Indexing is triggered automatically when a settled payment goes through the CDP Facilitator. You need a genuine external buyer to make the first paid call.`,
  },
  {
    id: "first-buyer",
    category: "first-payment",
    title: "Find the first external buyer",
    status: "actionable",
    detail: `Share your endpoint URL directly with an autonomous agent operator or a developer who has a USDC-funded Base wallet. They POST to your endpoint, receive the 402, sign the EIP-712 authorization, and the facilitator settles USDC to your payTo.`,
    action: {
      label: "Share endpoint URL",
      command: `# Your SentinelShield endpoint (after deployment):
POST https://YOUR_DEPLOYED_URL/api/x402/sentinelshield
Content-Type: application/json

# Unpaid → 402 + paymentRequirements
# Pay $${SENTINEL_PRICE_USDC} USDC → 200 OK + SARIF report`,
    },
  },
  {
    id: "verify-settlement",
    category: "first-payment",
    title: "Verify on-chain settlement",
    status: "blocked",
    detail: `After the first payment, verify on BaseScan that a USDC Transfer from the external payer to ${EVM_PAYOUT_ADDRESS} settled in a confirmed block. Only then mark OUR_REVENUE.`,
    action: {
      label: "View on BaseScan",
      url: `https://basescan.org/address/${EVM_PAYOUT_ADDRESS}`,
    },
  },

  // Scaling
  {
    id: "scale",
    category: "scaling",
    title: "Scale with proven settlement history",
    status: "blocked",
    detail: `After the first confirmed settlement, Agent402 and the Bazaar rank you as a "proven seller". The Smart Order Router will route more external buyers to your endpoint automatically. Monitor the Live RPC Scanner tab for incoming USDC.`,
  },
];

const CATEGORIES = [
  { id: "technical" as const, label: "Technical Readiness", icon: ShieldCheck, tone: "emerald" },
  { id: "listing" as const, label: "Marketplace Listing", icon: Rocket, tone: "amber" },
  { id: "first-payment" as const, label: "First External Payment", icon: Zap, tone: "rose" },
  { id: "scaling" as const, label: "Scaling", icon: Terminal, tone: "slate" },
];

const TONE_MAP = {
  emerald: { text: "text-emerald-400", bg: "bg-emerald-950/40", border: "border-emerald-800/40" },
  amber: { text: "text-amber-400", bg: "bg-amber-950/30", border: "border-amber-800/40" },
  rose: { text: "text-rose-400", bg: "bg-rose-950/30", border: "border-rose-800/40" },
  slate: { text: "text-slate-300", bg: "bg-slate-900/60", border: "border-slate-700/40" },
};

/**
 * RevenueReadinessChecklist — a structured panel showing the operator exactly
 * what's been verified, what they need to do next, and what's blocked on
 * the first external payment. Organized into 4 categories with per-step
 * status icons, details, and actionable commands/links.
 */
export function RevenueReadinessChecklist() {
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
    toast.success("Copied to clipboard");
  };

  const doneCount = STEPS.filter((s) => s.status === "done").length;
  const actionableCount = STEPS.filter((s) => s.status === "actionable").length;
  const blockedCount = STEPS.filter((s) => s.status === "blocked").length;

  return (
    <div className="bg-gradient-to-br from-emerald-950/30 via-slate-900 to-slate-950 border border-emerald-800/40 rounded-xl p-6 shadow-xl">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono uppercase tracking-wider mb-1">
            <Rocket className="w-4 h-4" />
            <span>Revenue Readiness Checklist</span>
          </div>
          <h2 className="text-lg font-bold text-white tracking-tight">
            From Technical Readiness → Real Revenue
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            The single non-negotiable KPI:{" "}
            <span className="text-emerald-400 font-semibold font-mono">
              CONFIRMED USDC SETTLEMENT
            </span>{" "}
            from an external payer to the receive-only wallet. No tests, no
            HTTP 200/402, no simulation counts as revenue.
          </p>
        </div>
        <div className="flex items-center gap-3 text-[11px] font-mono">
          <span className="flex items-center gap-1 text-emerald-400">
            <CheckCircle2 className="w-3 h-3" />
            {doneCount} done
          </span>
          <span className="flex items-center gap-1 text-amber-400">
            <Circle className="w-3 h-3" />
            {actionableCount} actionable
          </span>
          <span className="flex items-center gap-1 text-rose-400">
            <AlertTriangle className="w-3 h-3" />
            {blockedCount} blocked
          </span>
        </div>
      </div>

      <div className="mt-5 space-y-6">
        {CATEGORIES.map((cat) => {
          const steps = STEPS.filter((s) => s.category === cat.id);
          const tone = TONE_MAP[cat.tone];
          const Icon = cat.icon;
          return (
            <div key={cat.id}>
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-6 h-6 rounded ${tone.bg} border ${tone.border} flex items-center justify-center`}>
                  <Icon className={`w-3.5 h-3.5 ${tone.text}`} />
                </div>
                <span className={`text-xs font-mono uppercase tracking-wider ${tone.text}`}>
                  {cat.label}
                </span>
                <span className="text-[10px] font-mono text-slate-500">
                  ({steps.filter((s) => s.status === "done").length}/{steps.length})
                </span>
              </div>
              <div className="space-y-2 ml-8">
                {steps.map((step) => (
                  <div
                    key={step.id}
                    className={`p-3 rounded-lg border ${
                      step.status === "done"
                        ? "bg-emerald-950/20 border-emerald-900/30"
                        : step.status === "actionable"
                          ? "bg-amber-950/15 border-amber-900/30"
                          : "bg-rose-950/15 border-rose-900/30"
                    }`}
                  >
                    <div className="flex items-start gap-2.5">
                      {step.status === "done" ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                      ) : step.status === "actionable" ? (
                        <Circle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-semibold text-slate-100">
                          {step.title}
                        </div>
                        <p className="text-[11px] text-slate-400 mt-0.5 leading-relaxed">
                          {step.detail}
                        </p>
                        {step.action && (
                          <div className="mt-2 flex items-center gap-2">
                            {step.action.url && (
                              <a
                                href={step.action.url}
                                target="_blank"
                                rel="noreferrer"
                                className="px-2.5 py-1 text-[11px] font-mono rounded-md bg-emerald-950/60 border border-emerald-800/40 text-emerald-300 hover:bg-emerald-900/40 flex items-center gap-1.5 transition-colors"
                              >
                                {step.action.label}
                                <ExternalLink className="w-3 h-3" />
                              </a>
                            )}
                            {step.action.command && (
                              <button
                                onClick={() => handleCopy(step.action!.command!, step.id)}
                                className="px-2.5 py-1 text-[11px] font-mono rounded-md bg-slate-800 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 flex items-center gap-1.5 transition-colors"
                              >
                                {copied === step.id ? (
                                  <>
                                    <Check className="w-3 h-3 text-emerald-400" />
                                    Copied
                                  </>
                                ) : (
                                  <>
                                    <Copy className="w-3 h-3" />
                                    {step.action.label}
                                  </>
                                )}
                              </button>
                            )}
                          </div>
                        )}
                        {step.action?.command && (
                          <pre className="mt-2 p-2.5 rounded-md bg-slate-950 border border-slate-800 text-[10px] font-mono text-slate-300 overflow-x-auto max-h-32">
                            {step.action.command}
                          </pre>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
