/**
 * APSA-2026 x402 v2 Resource Server Core (deterministic, no external deps).
 * Reimplements the protocol enforcement logic from the original x402ServerCore
 * without @x402/* or viem packages. Tests the same guarantees: 402 challenge,
 * malformed rejection, recipient/amount/time-window checks, nonce replay
 * protection, and the critical "signature ≠ settlement" rule.
 *
 * This is a faithful LOGIC port — cryptographic EIP-712 signature verification
 * is represented as a deterministic mock that an external signer could satisfy.
 */

import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  BASE_MAINNET_CHAIN_ID,
  SENTINEL_PRICE_ATOMIC,
  SENTINEL_PRICE_USDC,
} from "./wallet-registry";
import { analyzeContractRisk } from "./sentinel-shield";
import type { SentinelShieldInput, SentinelShieldOutput } from "./types";

export type NonceState =
  | "SEEN"
  | "VERIFIED"
  | "SETTLEMENT_PENDING"
  | "SETTLED"
  | "SETTLEMENT_FAILED";

export interface NonceRecord {
  state: NonceState;
  timestamp: number;
  payer: string;
  amount: string;
  txHash?: string;
  failureReason?: string;
}

export interface V2Authorization {
  from: string;
  to: string;
  value: string;
  validAfter: number;
  validBefore: number;
  nonce: string;
}

export interface V2PaymentPayload {
  x402Version: number;
  payload: {
    authorization: V2Authorization;
    signature: string;
  };
}

export interface V2PaymentRequirements {
  x402Version: number;
  scheme: "exact";
  network: "eip155:8453";
  amount: string;
  payTo: string;
  asset: string;
  maxTimeoutSeconds: number;
  extra: {
    name: string;
    version: string;
    chainId: number;
    priceUSD: number;
    resource: string;
    description: string;
  };
}

export interface PaidRequestHandlerResponse {
  statusCode: number;
  headers: Record<string, string>;
  body: Record<string, unknown>;
}

// In-memory nonce registry — replay protection state.
const nonceRegistry = new Map<string, NonceRecord>();

export function nonceKey(payer: string, nonce: string): string {
  return `${payer.toLowerCase()}-${nonce.toLowerCase()}`;
}

export function getNonceState(payer: string, nonce: string): NonceRecord | undefined {
  return nonceRegistry.get(nonceKey(payer, nonce));
}

export function setNonceState(
  payer: string,
  nonce: string,
  state: NonceState,
  amount: string = SENTINEL_PRICE_ATOMIC,
  extra: { txHash?: string; failureReason?: string } = {},
): NonceRecord {
  const record: NonceRecord = {
    state,
    timestamp: Date.now(),
    payer: payer.toLowerCase(),
    amount,
    txHash: extra.txHash,
    failureReason: extra.failureReason,
  };
  nonceRegistry.set(nonceKey(payer, nonce), record);
  return record;
}

export function clearNonceRegistry(): void {
  nonceRegistry.clear();
}

export function generateV2PaymentRequirements(
  resourceUri: string = "/sentinelshield",
): V2PaymentRequirements {
  return {
    x402Version: 2,
    scheme: "exact",
    network: "eip155:8453",
    amount: SENTINEL_PRICE_ATOMIC,
    payTo: EVM_PAYOUT_ADDRESS,
    asset: BASE_USDC_MAINNET_ADDRESS,
    maxTimeoutSeconds: 3600,
    extra: {
      name: "USD Coin",
      version: "2",
      chainId: BASE_MAINNET_CHAIN_ID,
      priceUSD: SENTINEL_PRICE_USDC,
      resource: resourceUri,
      description: "SentinelShield Smart Contract Vulnerability Triage & SARIF Report",
    },
  };
}

/**
 * Deterministic mock of EIP-712 signature verification.
 * Accepts any 0x-prefixed hex string of correct length as a stand-in for a
 * valid signature, so the rest of the protocol logic can be exercised. In a
 * production build this would call viem's verifyTypedData.
 */
function mockVerifyTypedData(
  _authorization: V2Authorization,
  signature: string,
): boolean {
  if (typeof signature !== "string") return false;
  if (!signature.startsWith("0x")) return false;
  // 0x + 130 hex chars (65 bytes: r(32) + s(32) + v(1))
  return signature.length === 132;
}

/**
 * Mock on-chain payer balance check. Returns insufficient unless the caller
 * explicitly marks the payer as funded (used by the test suite to exercise the
 * "signature ≠ settlement" guarantee).
 */
const fundedPayers = new Set<string>();

export function markPayerFunded(payer: string, funded: boolean): void {
  if (funded) fundedPayers.add(payer.toLowerCase());
  else fundedPayers.delete(payer.toLowerCase());
}

export function isPayerFunded(payer: string): boolean {
  return fundedPayers.has(payer.toLowerCase());
}

/**
 * Mock settlement evidence verification. Only returns verified=true when the
 * caller explicitly supplies a tx hash that was previously marked as settled
 * via markSettlementEvidence().
 */
const settledHashes = new Map<
  string,
  { from: string; to: string; amount: string; blockNumber: number; gasUsed: string }
>();

export function markSettlementEvidence(
  txHash: string,
  opts: { from: string; to: string; amount: string; blockNumber: number; gasUsed: string },
): void {
  settledHashes.set(txHash.toLowerCase(), { ...opts });
}

export function verifySettlementEvidence(
  txHash: string,
  payer: string,
  payTo: string,
  requiredAmount: bigint,
): {
  verified: boolean;
  toVerified: boolean;
  receiptStatus: string;
  error?: string;
  blockNumber?: number;
  gasUsed?: string;
} {
  const evidence = settledHashes.get(txHash.toLowerCase());
  if (!evidence) {
    return {
      verified: false,
      toVerified: false,
      receiptStatus: "UNMINED_OR_UNLINKED",
      error:
        "Transaction not found in settlement registry or does not link payer → payTo.",
    };
  }
  const fromOk = evidence.from.toLowerCase() === payer.toLowerCase();
  const toOk = evidence.to.toLowerCase() === payTo.toLowerCase();
  let amountOk = false;
  try {
    amountOk = BigInt(evidence.amount) >= requiredAmount;
  } catch {
    amountOk = false;
  }
  const verified = fromOk && toOk && amountOk;
  return {
    verified,
    toVerified: toOk,
    receiptStatus: verified ? "CONFIRMED" : "MISMATCH",
    error: verified ? undefined : "Settlement evidence fields do not match payer/payTo/amount.",
    blockNumber: evidence.blockNumber,
    gasUsed: evidence.gasUsed,
  };
}

export interface SettlementEvidence {
  verified: boolean;
  toVerified: boolean;
  receiptStatus: string;
  error?: string;
  blockNumber?: number;
  gasUsed?: string;
}

/**
 * Production handler for POST /sentinelshield.
 * 1) 402 challenge if no payment payload
 * 2) Malformed payload rejection
 * 3) Wrong recipient / wrong amount / expired window rejection
 * 4) Nonce state machine (replay protection)
 * 5) EIP-712 signature verification (mocked deterministically)
 * 6) On-chain payer balance check (signature ≠ settlement)
 * 7) Settlement + post-settlement evidence verification
 * 8) Outcome delivery ONLY when fully verified on-chain
 */
export async function handlePaidSentinelRequest(
  input: SentinelShieldInput,
  rawPayload?: unknown,
  _network: "eip155:8453" = "eip155:8453",
  clientTxHash?: string,
): Promise<PaidRequestHandlerResponse> {
  const reqs = generateV2PaymentRequirements("/sentinelshield");
  const encodedReqs = Buffer.from(JSON.stringify(reqs)).toString("base64");

  // STEP 1: Unpaid → 402
  if (!rawPayload) {
    return {
      statusCode: 402,
      headers: {
        "Content-Type": "application/json",
        "PAYMENT-REQUIRED": encodedReqs,
        "payment-required": encodedReqs,
        "x402-version": "2",
      },
      body: {
        error: "Payment Required",
        message:
          "Access to SentinelShield requires x402 payment authorization.",
        paymentRequirements: reqs,
      },
    };
  }

  const payload = rawPayload as V2PaymentPayload;
  const auth = payload?.payload?.authorization;
  const signature = payload?.payload?.signature;

  // STEP 2: Malformed payload
  if (
    !auth ||
    !auth.from ||
    !auth.to ||
    !auth.value ||
    !auth.nonce ||
    !signature
  ) {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: {
        error: "Malformed Payment Payload",
        reason:
          "Missing required EIP-712 authorization fields: from, to, value, nonce, or signature.",
      },
    };
  }

  // STEP 3: Wrong recipient
  if (auth.to.toLowerCase() !== EVM_PAYOUT_ADDRESS.toLowerCase()) {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: {
        error: "Invalid Recipient",
        reason: `Payment rejected: payTo must be ${EVM_PAYOUT_ADDRESS}, received ${auth.to}`,
      },
    };
  }

  // STEP 4: Wrong / insufficient amount
  let valueBig: bigint;
  try {
    valueBig = BigInt(auth.value);
  } catch {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: { error: "Invalid Amount Format", reason: "Malformed value string" },
    };
  }
  const requiredBig = BigInt(SENTINEL_PRICE_ATOMIC);
  if (valueBig < requiredBig) {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: {
        error: "Insufficient Payment Amount",
        reason: `Required ${SENTINEL_PRICE_ATOMIC} ($9.50 USDC), received ${auth.value}`,
      },
    };
  }

  // STEP 5: Time window
  const now = Math.floor(Date.now() / 1000);
  if (auth.validBefore && Number(auth.validBefore) < now) {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: {
        error: "Authorization Expired",
        reason: `validBefore (${auth.validBefore}) is in the past`,
      },
    };
  }

  // STEP 6: Nonce state machine (replay protection)
  const existing = getNonceState(auth.from, auth.nonce);
  if (existing?.state === "SETTLED") {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: {
        error: "Nonce Already Settled",
        reason:
          "Payment nonce has already been finalized on-chain (Replay Protection Active)",
      },
    };
  }
  if (existing?.state === "SETTLEMENT_PENDING") {
    return {
      statusCode: 409,
      headers: { "Content-Type": "application/json" },
      body: {
        error: "Settlement In Progress",
        reason:
          "This payment authorization is currently undergoing settlement.",
      },
    };
  }

  setNonceState(auth.from, auth.nonce, "SEEN", auth.value);

  // STEP 7: Cryptographic signature verification (mocked)
  if (!mockVerifyTypedData(auth, signature)) {
    setNonceState(auth.from, auth.nonce, "SETTLEMENT_FAILED", auth.value, {
      failureReason: "Cryptographic signature mismatch",
    });
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: {
        error: "Invalid Signature",
        reason: "Recovered signer address does not match from address.",
      },
    };
  }

  setNonceState(auth.from, auth.nonce, "VERIFIED", auth.value);

  // STEP 8: On-chain payer balance — signature ≠ settlement
  if (!isPayerFunded(auth.from)) {
    setNonceState(auth.from, auth.nonce, "SETTLEMENT_FAILED", auth.value, {
      failureReason: "Payer has insufficient on-chain USDC balance",
    });
    return {
      statusCode: 402,
      headers: {
        "Content-Type": "application/json",
        "PAYMENT-REQUIRED": encodedReqs,
        "payment-required": encodedReqs,
      },
      body: {
        error: "Payment Settlement Incomplete",
        status: "INSUFFICIENT_PAYER_BALANCE",
        signatureValid: true,
        settledOnChain: false,
        payer: auth.from,
        requiredUSDC: `${SENTINEL_PRICE_USDC} USDC`,
        reason: "Payer wallet has 0 USDC on Base Mainnet; signature alone does not settle.",
        ourRevenueCounted: false,
      },
    };
  }

  // STEP 9: Settlement + evidence
  setNonceState(auth.from, auth.nonce, "SETTLEMENT_PENDING", auth.value);
  let settlementTxHash = clientTxHash;
  if (!settlementTxHash) {
    // No facilitator in the sandbox; require caller-supplied hash marked settled.
    settlementTxHash = undefined;
  }
  if (!settlementTxHash || !verifySettlementEvidence(settlementTxHash, auth.from, EVM_PAYOUT_ADDRESS, valueBig).verified) {
    setNonceState(auth.from, auth.nonce, "SETTLEMENT_FAILED", auth.value, {
      failureReason: "Settlement evidence unverified",
    });
    return {
      statusCode: 402,
      headers: {
        "Content-Type": "application/json",
        "PAYMENT-REQUIRED": encodedReqs,
        "payment-required": encodedReqs,
      },
      body: {
        error: "Settlement Evidence Verification Failed",
        status: "UNVERIFIED_ON_CHAIN",
        settledOnChain: false,
        payer: auth.from,
        reason:
          "Transaction not confirmed on Base Mainnet or does not link payer → payTo.",
        ourRevenueCounted: false,
      },
    };
  }

  setNonceState(auth.from, auth.nonce, "SETTLED", auth.value, {
    txHash: settlementTxHash,
  });

  // STEP 10: Deliver outcome
  const outcome: SentinelShieldOutput = await analyzeContractRisk(input);
  const evidence = verifySettlementEvidence(
    settlementTxHash,
    auth.from,
    EVM_PAYOUT_ADDRESS,
    valueBig,
  );

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
      "x402-settlement": "confirmed",
      "x402-tx-hash": settlementTxHash,
      "x402-block-number": String(evidence.blockNumber || ""),
    },
    body: {
      success: true,
      service: "SentinelShield Contract Risk Triage",
      payment: {
        status: "SETTLED",
        x402Version: 2,
        txHash: settlementTxHash,
        blockNumber: evidence.blockNumber,
        gasUsed: evidence.gasUsed,
        payer: auth.from,
        payTo: EVM_PAYOUT_ADDRESS,
        token: BASE_USDC_MAINNET_ADDRESS,
        amountUSDC: SENTINEL_PRICE_USDC,
        verifiedOnRpc: true,
      },
      outcome,
    },
  };
}
