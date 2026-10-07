import type { TabHelp } from "@/components/apsa/help-drawer";

/**
 * Per-tab help content for the HelpDrawer. Each entry explains what the tab
 * is for and lists the 3-4 key things the operator should look at there.
 * Aimed at reducing the "information density" accessibility concern flagged
 * by VLM in round 1.
 */
export const TAB_HELPS: TabHelp[] = [
  {
    id: "mission",
    title: "🎯 Real Revenue Mission",
    summary:
      "The live nerve center. A 12-test automated verification suite exercises the entire x402 protocol enforcement logic — 402 challenge, signature verification, nonce replay protection, and the critical 'signature ≠ settlement' rule. Tests 5 and 11 hit the real Base Mainnet RPC.",
    bullets: [
      "The 12-test table — all 12 must show green PASS. Test 10 is the most important: it proves a valid cryptographic signature alone does NOT count as revenue without an on-chain USDC transfer.",
      "The 4 payout-rail cards (EVM/Solana/Tron/Bitcoin) — these are the operator's immutable receive-only addresses. Never share private keys.",
      "The On-Chain Transaction Verifier — paste any 66-char tx hash to confirm it settled USDC to the payout wallet.",
    ],
  },
  {
    id: "verdict",
    title: "1. Verdict & Report",
    summary:
      "The formal scientific verdict on whether the autonomous agent claim is proven. Strictly separates CLAIMED from VERIFIED from OUR_REVENUE. All hypothetical figures are tagged [MODELLED ASSUMPTION].",
    bullets: [
      "The 6-fold verdict grid — The Claim, Technically Verified, On-Chain Verified (market), Our Own Test, Our Own Received, Our Own Net Profit. Only the last two count as real revenue.",
      "The live USDC balance pulled from the payout wallet — if this stays $0.00, no real external buyer has paid yet.",
      "The 'What Operator Must Do' section — the 4 strictly non-automatable human tasks (create receive-only wallet, register free-tier API keys, fiat off-ramp + tax, no fraud).",
    ],
  },
  {
    id: "forensics",
    title: "2. Wash Volume & Forensics",
    summary:
      "Forensic deconstruction of on-chain settlement volume. Separates synthetic self-funded wash (E0–E2) from genuine independent external demand (E3–E5). Only E3–E5 is admitted into economic calculations.",
    bullets: [
      "The donut chart — shows the ecosystem-wide wash vs external split (71.4% wash). The center label shows total audited USDC volume.",
      "The E0–E5 buyer tier cards — E0/E1/E2 are disqualified (self-funded, sybil, obscure). E3/E4/E5 are admitted (independent, CEX-funded, institutional).",
      "The interactive Loop Analyzer — paste any buyer address (or click a preset) to trace its funding provenance and classify it.",
    ],
  },
  {
    id: "candidates",
    title: "3. Top 10 Candidates",
    summary:
      "The 10 highest-leverage outcome services the agent could sell, with a full 17-parameter breakdown each. Follows the 'SELL OUTCOME, NOT RAW INPUT' doctrine — no $0.0001 commodity APIs.",
    bullets: [
      "The left list — click any candidate to inspect it. The score badge (/45) ranks by evidence + external demand + autonomy + zero-capital + net margin.",
      "The right inspector — shows machine input/output, buyer behavior, granular cost breakdown (DATA/LLM/COMPUTE/RPC/HOSTING/FACILITATOR), and zero-capital feasibility.",
      "The 'Outcome vs Raw Input' comparison strip — decision-ready reports ($6.50–$12) outperform raw feeds ($0.001) by 5,000×.",
    ],
  },
  {
    id: "novel",
    title: "4. Novel Service Ideas",
    summary:
      "5 new autonomous service architectures constructed from verified on-chain demand signals. Each delivers a high-leverage structured outcome priced $4.50–$18.00 with >98% net margins. The Top 2 are selected for production.",
    bullets: [
      "The Top 2 highlight section — selected for optimal risk-adjusted profitability (demand + ticket + margin + repeatability + zero-capital + autonomy + low legal risk).",
      "The 14-attribute dossier — machine input, structured output, data sources, automation degree, marginal cost, who pays, why agents pay, discovery channel, competitors, legal risk, A4/A5 feasibility.",
      "The 5-idea quick selector at the bottom — click any to inspect its full dossier.",
    ],
  },
  {
    id: "testnet",
    title: "5. Testnet & Mainnet Cycle",
    summary:
      "Interactive x402 protocol workbench. Trigger a full 7-step payment handshake: client request → 402 challenge → EIP-712 signature → facilitator verify → outcome production → settlement → 200 OK delivery.",
    bullets: [
      "The 3 control fields — service (SentinelShield $9.50 or VeriVendor $7.00), target input (contract address), buyer wallet. Values are saved to your browser.",
      "The Trigger button — runs the full handshake and produces a 7-step console log + delivered SARIF outcome + per-order unit economics.",
      "The Repeat Demand tracker — counts simulated payments and unique buyer wallets toward the 5-payment / 3-independent-wallet goal. Testnet revenue is always $0.",
    ],
  },
  {
    id: "economics",
    title: "6. Unit Economics",
    summary:
      "Financial forensics and projections. Three empirical scenarios (Conservative/Base/Strong) plus a live simulator with sliders. All projections are tagged [MODELLED ASSUMPTION] vs [ON-CHAIN FACT].",
    bullets: [
      "The 3 scenario cards — click any to load its preset into the sliders. Net/month ranges from ~$550 (conservative) to ~$5,600 (strong).",
      "The Revenue Projection Chart — bars show net/month for each scenario + a LIVE bar computed from the sliders; the line shows net/day.",
      "The Revenue Timeline Chart — forward-looking cumulative net profit over 30/90/365 days, with an adjustable daily discovery ramp rate.",
    ],
  },
  {
    id: "autonomy",
    title: "7. A4/A5 Autonomy",
    summary:
      "Audits the 10-step autonomous operational cycle and the zero-marketing machine discovery channels. A4 = fully autonomous execution; A5 = fully autonomous economics (not yet proven).",
    bullets: [
      "The 10-step cycle — every step must show 'AUTONOMOUS' with 'Human: 0'. Steps span discovery → 402 challenge → signature → outcome → settlement → ledger → repeat.",
      "The 4 discovery channels — x402scan, Agent402/Bazaar marketplaces, MCP catalogs, BaseScan verified-contract webhooks. No human marketing required.",
      "The x402-manifest.json preview — the machine-readable discovery document served at /.well-known/x402-manifest.json that buyer agents fetch autonomously.",
    ],
  },
  {
    id: "scanner",
    title: "8. Live Base RPC Scanner",
    summary:
      "Direct JSON-RPC queries to Base Mainnet (or Sepolia) for the receive-only payout wallet. Shows real ETH/USDC balances, latest block, and any inbound USDC transfers in the scanned range.",
    bullets: [
      "The USDC balance card — this is the ONLY number that counts as real revenue. If it reads $0.00, no external buyer has paid.",
      "The ETH balance card — the receive-only wallet does not need ETH gas; facilitators sponsor gas under ERC-3009.",
      "The inbound transfers table — lists any USDC Transfer events to the payout address with tx hash, payer, amount, block, and a link to BaseScan.",
    ],
  },
];
