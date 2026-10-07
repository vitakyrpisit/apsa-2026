/**
 * PayAI x402 Facilitator integration — verify + settle + on-chain verification.
 *
 * Flow:
 * 1. Buyer signs EIP-712 TransferWithAuthorization
 * 2. Buyer sends payment payload to seller (PAYMENT-SIGNATURE header)
 * 3. Seller calls PayAI /verify → checks signature validity
 * 4. Seller calls PayAI /settle → facilitator executes on-chain USDC transfer
 * 5. Seller verifies tx via Base RPC (eth_getTransactionReceipt)
 * 6. Only then seller delivers the service
 *
 * No API key needed for /verify (free tier).
 * No private key needed (facilitator sponsors gas).
 */

import { verifyTypedData, isAddressEqual } from "viem";
import { base } from "viem/chains";
import { createPublicClient, http } from "viem";
import {
  EVM_PAYOUT_ADDRESS,
  BASE_USDC_MAINNET_ADDRESS,
  BASE_MAINNET_CHAIN_ID,
} from "./wallet-registry";

const PAYAI_BASE_URL = "https://facilitator.payai.network";
const BASE_RPC = "https://mainnet.base.org";

// EIP-712 domain for USDC TransferWithAuthorization on Base
const EIP712_DOMAIN = {
  name: "USD Coin",
  version: "2",
  chainId: BASE_MAINNET_CHAIN_ID,
  verifyingContract: BASE_USDC_MAINNET_ADDRESS as `0x${string}`,
};

const EIP712_TYPES = {
  TransferWithAuthorization: [
    { name: "from", type: "address" },
    { name: "to", type: "address" },
    { name: "value", type: "uint256" },
    { name: "validAfter", type: "uint256" },
    { name: "validBefore", type: "uint256" },
    { name: "nonce", type: "bytes32" },
  ],
};

export interface PaymentPayload {
  x402Version: number;
  scheme: string;
  network: string;
  payload: {
    authorization: {
      from: string;
      to: string;
      value: string;
      validAfter: number;
      validBefore: number;
      nonce: string;
    };
    signature: string;
  };
}

export interface PaymentRequirements {
  scheme: string;
  network: string;
  maxAmountRequired: string;
  asset: string;
  payTo: string;
  resource: string;
  description: string;
  maxTimeoutSeconds: number;
}

export interface SettlementResult {
  verified: boolean;
  settled: boolean;
  txHash?: string;
  error?: string;
  payer?: string;
  amountUSDC?: number;
}

const baseClient = createPublicClient({
  chain: base,
  transport: http(BASE_RPC),
});

/**
 * Verify a payment payload via PayAI facilitator (no API key needed).
 */
export async function verifyPayment(
  payload: PaymentPayload,
  requirements: PaymentRequirements,
): Promise<{ isValid: boolean; error?: string }> {
  try {
    const res = await fetch(`${PAYAI_BASE_URL}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paymentPayload: payload, paymentRequirements: requirements }),
      signal: AbortSignal.timeout(10000),
    });
    const data = (await res.json()) as { isValid: boolean; invalidReason?: string; invalidMessage?: string };
    return { isValid: data.isValid, error: data.invalidMessage || data.invalidReason };
  } catch (err) {
    return { isValid: false, error: err instanceof Error ? err.message : "verify failed" };
  }
}

/**
 * Settle a verified payment via PayAI facilitator (triggers on-chain USDC transfer).
 */
export async function settlePayment(
  payload: PaymentPayload,
  requirements: PaymentRequirements,
): Promise<{ success: boolean; txHash?: string; error?: string }> {
  try {
    const res = await fetch(`${PAYAI_BASE_URL}/settle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paymentPayload: payload, paymentRequirements: requirements }),
      signal: AbortSignal.timeout(15000),
    });
    const data = (await res.json()) as {
      success: boolean;
      transaction?: string;
      errorReason?: string;
      errorMessage?: string;
    };
    return {
      success: data.success,
      txHash: data.transaction,
      error: data.errorMessage || data.errorReason,
    };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : "settle failed" };
  }
}

/**
 * Verify on-chain that a USDC Transfer event occurred in the transaction.
 * Checks: Transfer.from == payer, Transfer.to == operator, amount >= expected.
 */
const TRANSFER_EVENT_TOPIC =
  "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef";

export async function verifyOnChainSettlement(
  txHash: string,
  expectedPayer: string,
  expectedPayTo: string,
  expectedAmount: bigint,
): Promise<{ verified: boolean; blockNumber?: bigint; error?: string }> {
  try {
    const receipt = await baseClient.getTransactionReceipt({
      hash: txHash as `0x${string}`,
    });

    if (receipt.status !== "success") {
      return { verified: false, error: "Transaction reverted on-chain" };
    }

    // Check for USDC Transfer event
    for (const log of receipt.logs) {
      if (log.topics[0]?.toLowerCase() === TRANSFER_EVENT_TOPIC &&
          log.address.toLowerCase() === BASE_USDC_MAINNET_ADDRESS.toLowerCase()) {
        const from = "0x" + (log.topics[1] || "").slice(26);
        const to = "0x" + (log.topics[2] || "").slice(26);
        const amount = BigInt(log.data);

        if (
          from.toLowerCase() === expectedPayer.toLowerCase() &&
          to.toLowerCase() === expectedPayTo.toLowerCase() &&
          amount >= expectedAmount
        ) {
          return { verified: true, blockNumber: receipt.blockNumber };
        }
      }
    }

    return { verified: false, error: "No matching USDC Transfer event found" };
  } catch (err) {
    return { verified: false, error: err instanceof Error ? err.message : "RPC error" };
  }
}

/**
 * Full payment flow: verify → settle → on-chain check.
 * Returns SettlementResult with all details.
 */
export async function processPayment(
  paymentPayload: PaymentPayload,
  paymentRequirements: PaymentRequirements,
): Promise<SettlementResult> {
  const auth = paymentPayload.payload.authorization;
  const expectedAmount = BigInt(auth.value);

  // Step 1: Verify via PayAI facilitator
  const verifyResult = await verifyPayment(paymentPayload, paymentRequirements);
  if (!verifyResult.isValid) {
    return {
      verified: false,
      settled: false,
      error: `Payment verification failed: ${verifyResult.error}`,
    };
  }

  // Step 2: Settle via PayAI facilitator (triggers on-chain USDC transfer)
  const settleResult = await settlePayment(paymentPayload, paymentRequirements);
  if (!settleResult.success || !settleResult.txHash) {
    return {
      verified: true,
      settled: false,
      error: `Settlement failed: ${settleResult.error}`,
    };
  }

  // Step 3: Verify on-chain settlement via Base RPC
  const onChainResult = await verifyOnChainSettlement(
    settleResult.txHash,
    auth.from,
    EVM_PAYOUT_ADDRESS,
    expectedAmount,
  );

  if (!onChainResult.verified) {
    return {
      verified: true,
      settled: true,
      txHash: settleResult.txHash,
      error: `On-chain verification failed: ${onChainResult.error}`,
    };
  }

  return {
    verified: true,
    settled: true,
    txHash: settleResult.txHash,
    payer: auth.from,
    amountUSDC: Number(expectedAmount) / 1e6,
  };
}

/**
 * Build PayAI-compatible payment requirements for a 402 response.
 */
export function buildPaymentRequirements(
  amountAtomic: string,
  resource: string,
  description: string,
): PaymentRequirements {
  return {
    scheme: "exact",
    network: "base",
    maxAmountRequired: amountAtomic,
    asset: BASE_USDC_MAINNET_ADDRESS,
    payTo: EVM_PAYOUT_ADDRESS,
    resource,
    description,
    maxTimeoutSeconds: 3600,
  };
}

/**
 * Extract payment payload from the PAYMENT-SIGNATURE header (base64-encoded JSON)
 * or from the request body.
 */
export function extractPaymentPayload(req: Request, body: unknown): PaymentPayload | null {
  // Try PAYMENT-SIGNATURE header first (base64-encoded)
  const sigHeader = req.headers.get("payment-signature") || req.headers.get("PAYMENT-SIGNATURE");
  if (sigHeader) {
    try {
      const decoded = Buffer.from(sigHeader.trim(), "base64").toString("utf8");
      return JSON.parse(decoded) as PaymentPayload;
    } catch {
      try {
        return JSON.parse(sigHeader) as PaymentPayload;
      } catch {
        return null;
      }
    }
  }

  // Try request body
  if (body && typeof body === "object") {
    const b = body as Record<string, unknown>;
    if (b.paymentPayload) return b.paymentPayload as PaymentPayload;
    if (b.payload && b.x402Version) return b as unknown as PaymentPayload;
    const auth = (b as { paymentAuthorization?: Record<string, unknown> }).paymentAuthorization ||
      (b.from && b.signature ? b : null);
    if (auth) {
      const a = auth as { from: string; to: string; value: string; validAfter: number; validBefore: number; nonce: string };
      const sig = (b as { signature?: string }).signature;
      return {
        x402Version: 1,
        scheme: "exact",
        network: "base",
        payload: {
          authorization: {
            from: a.from,
            to: a.to || EVM_PAYOUT_ADDRESS,
            value: a.value,
            validAfter: a.validAfter,
            validBefore: a.validBefore,
            nonce: a.nonce,
          },
          signature: sig || "",
        },
      };
    }
  }

  return null;
}
