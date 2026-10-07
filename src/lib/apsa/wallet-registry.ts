/**
 * APSA-2026 Operator Payout Rail Registry.
 * Four immutable, strictly RECEIVE-ONLY destination addresses across EVM, Solana, Tron, Bitcoin.
 * The agent NEVER requests seed phrases, private keys, or passwords.
 */

export type RailId = "evm" | "solana" | "tron" | "bitcoin";

export interface PayoutRail {
  id: RailId;
  label: string;
  ecosystem: string;
  network: string;
  address: string;
  supportedAssets: string;
  accentClass: string; // tailwind text/border accent token
  borderClass: string;
  shortPrefix: string;
  memo?: string;
}

export const EVM_PAYOUT_ADDRESS = "0x829f877daAb94D766BB2b8511ad486C40f2C2BDA";
export const SOLANA_PAYOUT_ADDRESS = "EyTxSdVtku7QtbwgntLvUwyxMvraJyAxoPoZ8ALdG6qL";
export const TRON_PAYOUT_ADDRESS = "TVVhpdHEg1ZgvPjJNSe2P28bhUDE4m85ZX";
export const BITCOIN_PAYOUT_ADDRESS = "bc1qaedy7cmquxjlmkezlxlytkrecv0ufku970tk9c";

export const OFFICIAL_PAYOUT_ADDRESS = EVM_PAYOUT_ADDRESS;

export const BASE_USDC_MAINNET_ADDRESS =
  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
export const BASE_USDC_SEPOLIA_ADDRESS =
  "0x036CbD53842c5426634e7929541eC2318f3dCF7e";
export const BASE_X402_FACILITATOR_MAINNET =
  "0x4020000000000000000000000000000000000402";

export const SENTINEL_PRICE_USDC = 9.5;
export const SENTINEL_PRICE_ATOMIC = "9500000";
export const BASE_MAINNET_CHAIN_ID = 8453;
export const BASE_SEPOLIA_CHAIN_ID = 84532;

export const ARBITRUM_DEPOSIT_MEMO = "578354";

export const PAYOUT_RAILS: PayoutRail[] = [
  {
    id: "evm",
    label: "EVM (Base / Eth / Arb)",
    ecosystem: "Base (8453) / Ethereum (1) / Arbitrum (42161)",
    network: "EVM",
    address: EVM_PAYOUT_ADDRESS,
    supportedAssets: "USDC, ETH, ARB",
    accentClass: "text-emerald-300",
    borderClass: "border-emerald-500/30",
    shortPrefix: "0x829f",
    memo: ARBITRUM_DEPOSIT_MEMO,
  },
  {
    id: "solana",
    label: "Solana Mainnet (SPL)",
    ecosystem: "Solana Mainnet",
    network: "SOL",
    address: SOLANA_PAYOUT_ADDRESS,
    supportedAssets: "SOL, USDC (SPL)",
    accentClass: "text-violet-300",
    borderClass: "border-violet-500/30",
    shortPrefix: "EyTx",
  },
  {
    id: "tron",
    label: "Tron Mainnet (TRC-20)",
    ecosystem: "Tron Mainnet",
    network: "TRX",
    address: TRON_PAYOUT_ADDRESS,
    supportedAssets: "TRX, USDT (TRC-20)",
    accentClass: "text-rose-300",
    borderClass: "border-rose-500/30",
    shortPrefix: "TVVh",
  },
  {
    id: "bitcoin",
    label: "Bitcoin Native (SegWit)",
    ecosystem: "Bitcoin Native SegWit",
    network: "BTC",
    address: BITCOIN_PAYOUT_ADDRESS,
    supportedAssets: "Native BTC",
    accentClass: "text-amber-300",
    borderClass: "border-amber-500/30",
    shortPrefix: "bc1q",
  },
];

export const OPERATOR_EMAIL = "valykirpisit@gmail.com";

export const PROTOCOL_VERSION = "APSA-2026.4";

export function shortAddr(addr: string, head = 6, tail = 4): string {
  if (!addr) return "";
  if (addr.length <= head + tail) return addr;
  return `${addr.slice(0, head)}…${addr.slice(-tail)}`;
}
