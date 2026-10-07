/**
 * SentinelShield Contract Risk Triage Core Engine (v2.1).
 * Deterministic EVM-bytecode triage: walks real opcodes (skipping PUSH data and the
 * Solidity metadata trailer) instead of searching the hex text for substrings.
 * This is automated triage of BYTECODE ONLY. It is not a security audit and it cannot
 * evaluate reentrancy, oracle manipulation, arithmetic or access-control logic.
 */

import { SentinelShieldInput, SentinelShieldOutput, Finding } from '../types/x402';
import { createHash } from 'node:crypto';
import { createPublicClient, http, isAddress } from 'viem';
import { base } from 'viem/chains';

const client = createPublicClient({
  chain: base,
  transport: http(process.env.BASE_RPC_URL || 'https://mainnet.base.org')
});

/** Error that should be shown to the caller as a 4xx and must NOT result in a charge. */
export class SentinelInputError extends Error {
  status: number;
  constructor(message: string, status = 422) {
    super(message);
    this.name = 'SentinelInputError';
    this.status = status;
  }
}

function sha256(text: string): string {
  return createHash('sha256').update(text, 'utf8').digest('hex');
}

const MAX_BYTECODE_BYTES = 49152; // 2x the EIP-170 limit; refuse absurd inputs

/** Cheap shape check used BEFORE any money is taken. Throws SentinelInputError. */
export function validateSentinelInput(input: SentinelShieldInput): void {
  if (!input || typeof input !== 'object') throw new SentinelInputError('Request body must be a JSON object.', 400);
  if (input.chain && input.chain !== 'base') {
    throw new SentinelInputError('Only chain "base" is supported.', 400);
  }
  const addr = input.contractAddress?.trim();
  const code = input.bytecode?.trim();
  if (!addr && !code) {
    throw new SentinelInputError('Provide "contractAddress" (Base) or "bytecode" (hex).', 400);
  }
  if (addr && !isAddress(addr.toLowerCase())) {
    throw new SentinelInputError('"contractAddress" is not a valid EVM address.', 400);
  }
  if (code) {
    const hex = code.replace(/^0x/i, '');
    if (hex.length === 0 || hex.length % 2 !== 0 || !/^[0-9a-fA-F]+$/.test(hex)) {
      throw new SentinelInputError('"bytecode" must be even-length hex.', 400);
    }
    if (hex.length / 2 > MAX_BYTECODE_BYTES) {
      throw new SentinelInputError(`"bytecode" exceeds ${MAX_BYTECODE_BYTES} bytes.`, 400);
    }
  }
}

export interface OpcodeScan {
  codeBytes: number;
  codeBytesAnalysed: number;
  hasDelegatecall: boolean;
  hasCallcode: boolean;
  hasSelfdestruct: boolean;
  hasCreate: boolean;
  hasCreate2: boolean;
  hasOrigin: boolean;
  hasTimestamp: boolean;
  callCount: number;
  eip1967Slot: boolean;
  minimalProxy: boolean;
  metadataTrailerBytes: number;
}

const EIP1967_IMPL_SLOT = '360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc';
const EIP1967_ADMIN_SLOT = 'b53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103';

/** Pure function: scan runtime bytecode (hex, with or without 0x). Exported for tests. */
export function scanBytecode(hexInput: string): OpcodeScan {
  const hex = hexInput.replace(/^0x/i, '');
  const bytes = Buffer.from(hex, 'hex');
  const total = bytes.length;

  // Solidity appends CBOR metadata followed by its 2-byte big-endian length.
  let end = total;
  let trailer = 0;
  if (total > 2) {
    const metaLen = (bytes[total - 2] << 8) | bytes[total - 1];
    const start = total - 2 - metaLen;
    if (metaLen > 0 && start > 0 && bytes[start] >= 0xa1 && bytes[start] <= 0xa6) {
      end = start;
      trailer = total - start;
    }
  }

  const scan: OpcodeScan = {
    codeBytes: total,
    codeBytesAnalysed: end,
    hasDelegatecall: false,
    hasCallcode: false,
    hasSelfdestruct: false,
    hasCreate: false,
    hasCreate2: false,
    hasOrigin: false,
    hasTimestamp: false,
    callCount: 0,
    eip1967Slot: false,
    minimalProxy: false,
    metadataTrailerBytes: trailer
  };

  // EIP-1167 minimal proxy: 363d3d373d3d3d363d73 <20 bytes> 5af43d82803e903d91602b57fd5bf3
  const head = bytes.subarray(0, 10).toString('hex');
  if (total >= 45 && head === '363d3d373d3d3d363d73' && bytes.subarray(30, 45).toString('hex') === '5af43d82803e903d91602b57fd5bf3') {
    scan.minimalProxy = true;
  }

  let i = 0;
  while (i < end) {
    const op = bytes[i];
    if (op >= 0x60 && op <= 0x7f) {
      const n = op - 0x5f; // PUSH1..PUSH32
      if (op === 0x7f) {
        const imm = bytes.subarray(i + 1, i + 33).toString('hex');
        if (imm === EIP1967_IMPL_SLOT || imm === EIP1967_ADMIN_SLOT) scan.eip1967Slot = true;
      }
      i += 1 + n;
      continue;
    }
    switch (op) {
      case 0xf4: scan.hasDelegatecall = true; scan.callCount++; break;
      case 0xf2: scan.hasCallcode = true; scan.callCount++; break;
      case 0xf1: case 0xfa: scan.callCount++; break;
      case 0xff: scan.hasSelfdestruct = true; break;
      case 0xf0: scan.hasCreate = true; break;
      case 0xf5: scan.hasCreate2 = true; break;
      case 0x32: scan.hasOrigin = true; break;
      case 0x42: scan.hasTimestamp = true; break;
      default: break;
    }
    i += 1;
  }
  return scan;
}

const RULES = [
  { id: 'SEC-001', name: 'DelegatecallPresence', shortDescription: { text: 'DELEGATECALL / CALLCODE opcode present in executable code' } },
  { id: 'SEC-002', name: 'SelfdestructPresence', shortDescription: { text: 'SELFDESTRUCT opcode present in executable code' } },
  { id: 'SEC-003', name: 'TxOriginUsage', shortDescription: { text: 'ORIGIN opcode present (tx.origin may be used for authorization)' } },
  { id: 'SEC-004', name: 'ProxyPattern', shortDescription: { text: 'EIP-1967 slot constant or EIP-1167 minimal proxy detected' } },
  { id: 'SEC-005', name: 'ContractCreation', shortDescription: { text: 'CREATE / CREATE2 opcode present' } }
];

export async function analyzeContractRisk(input: SentinelShieldInput): Promise<SentinelShieldOutput> {
  validateSentinelInput(input);

  const targetAddress = input.contractAddress?.toLowerCase().trim();
  let bytecode = (input.bytecode || '').trim();
  let isContractDeployed = false;

  if (targetAddress) {
    let code: string | undefined;
    try {
      code = await client.getCode({ address: targetAddress as `0x${string}` });
    } catch {
      throw new SentinelInputError('Base RPC read failed; you were not charged. Try again.', 503);
    }
    if (!code || code === '0x') {
      throw new SentinelInputError('No contract code at that address on Base (EOA or undeployed).', 422);
    }
    bytecode = code;
    isContractDeployed = true;
  }

  const s = scanBytecode(bytecode);
  const findings: Finding[] = [];

  if (s.hasDelegatecall || s.hasCallcode) {
    const proxy = s.eip1967Slot || s.minimalProxy;
    findings.push({
      id: 'FINDING-101',
      ruleId: 'SEC-001',
      level: proxy ? 'note' : 'warning',
      title: proxy ? 'DELEGATECALL used by a proxy pattern' : 'DELEGATECALL / CALLCODE present',
      description: proxy
        ? 'A proxy pattern was detected. Who controls the implementation (admin / upgrade rights) cannot be determined from bytecode alone.'
        : 'An executable DELEGATECALL/CALLCODE opcode exists. Whether its target can be influenced by an attacker requires source or storage review.',
      exploitVector: 'If the delegate target or calldata is attacker-influenced, foreign code runs with this contract\'s storage and balance.',
      mitigation: 'Verify the target is fixed or access-controlled; review upgrade authority.',
      cvssScore: proxy ? 3.0 : 5.0
    });
  }
  if (s.hasSelfdestruct) {
    findings.push({
      id: 'FINDING-102',
      ruleId: 'SEC-002',
      level: 'warning',
      title: 'SELFDESTRUCT opcode present',
      description: 'Since EIP-6780 (Dencun) SELFDESTRUCT only removes code if called in the creating transaction; it still forwards the balance. Presence alone is not proof of an exploitable path.',
      exploitVector: 'Forced ETH transfer or teardown logic that surprises integrators.',
      mitigation: 'Confirm the opcode is unreachable or properly access-controlled.',
      cvssScore: 4.0
    });
  }
  if (s.hasOrigin) {
    findings.push({
      id: 'FINDING-103',
      ruleId: 'SEC-003',
      level: 'warning',
      title: 'ORIGIN opcode present',
      description: 'tx.origin may be used for authorization or may be benign (e.g. gas-refund logic). Bytecode cannot show which.',
      exploitVector: 'If used for auth, a malicious intermediate contract can phish the owner.',
      mitigation: 'Use msg.sender for authorization.',
      cvssScore: 4.3
    });
  }
  if (s.eip1967Slot || s.minimalProxy) {
    findings.push({
      id: 'FINDING-104',
      ruleId: 'SEC-004',
      level: 'note',
      title: s.minimalProxy ? 'EIP-1167 minimal proxy' : 'EIP-1967 proxy slot referenced',
      description: s.minimalProxy
        ? 'Clone proxy: logic lives at another address. Analyse the implementation contract instead; this result describes only the clone stub.'
        : 'The code references the EIP-1967 implementation/admin slot, which indicates an upgradeable proxy or an implementation.',
      exploitVector: 'Upgrade authority compromise changes contract behaviour.',
      mitigation: 'Review who can upgrade and any timelock.',
      cvssScore: 0.0
    });
  }
  if (s.hasCreate || s.hasCreate2) {
    findings.push({
      id: 'FINDING-105',
      ruleId: 'SEC-005',
      level: 'note',
      title: s.hasCreate2 ? 'CREATE2 present' : 'CREATE present',
      description: 'The contract can deploy other contracts. CREATE2 enables deterministic, possibly re-deployable addresses.',
      exploitVector: 'Address-reuse tricks after metamorphic patterns (limited post-Dencun).',
      mitigation: 'Check what is deployed and by whom.',
      cvssScore: 0.0
    });
  }

  const warnings = findings.filter((f) => f.level === 'warning').length;
  let riskLevel: SentinelShieldOutput['riskLevel'] = 'LOW';
  let overallScore = 85;
  let exploitability: SentinelShieldOutput['exploitability'] = 'NONE';
  if (warnings >= 2) { riskLevel = 'MEDIUM'; overallScore = 60; exploitability = 'MEDIUM'; }
  else if (warnings === 1) { riskLevel = 'MEDIUM'; overallScore = 70; exploitability = 'LOW'; }
  else if (findings.length > 0) { riskLevel = 'LOW'; overallScore = 80; exploitability = 'LOW'; }

  const summary =
    `SentinelShield bytecode triage for ${targetAddress || 'supplied bytecode'}: ${s.codeBytes} bytes ` +
    `(${s.codeBytesAnalysed} executable bytes scanned, ${s.metadataTrailerBytes} metadata bytes skipped). ` +
    `${findings.length} signal(s), risk ${riskLevel} (${overallScore}/100 triage index). ` +
    `LIMITATIONS: bytecode-only; reentrancy, oracle/flash-loan exposure, arithmetic and access-control logic were NOT evaluated. ` +
    `A LOW result is not a statement that the contract is safe. This is not a security audit.`;

  const output: SentinelShieldOutput = {
    service: 'SentinelShield Contract Risk Triage',
    version: '2.1.0',
    target: {
      chain: 'base',
      contractAddress: targetAddress,
      verifiedOnScan: isContractDeployed
    },
    riskLevel,
    overallScore,
    summary,
    exploitability,
    findings,
    metrics: {
      reentrancyProtected: null,
      flashLoanDrainVulnerable: null,
      unauthorizedUpgradeVector: s.hasDelegatecall || s.hasCallcode || s.eip1967Slot || s.minimalProxy,
      uncheckedArithmetic: null
    },
    sarif: {
      $schema: 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json',
      version: '2.1.0',
      runs: [
        {
          tool: { driver: { name: 'SentinelShield Bytecode Triage', version: '2.1.0', rules: RULES } },
          results: findings.map((f) => ({ ruleId: f.ruleId, level: f.level, message: { text: `${f.title}: ${f.description}` } }))
        }
      ]
    },
    generatedAt: new Date().toISOString(),
    sha256Checksum: 'sha256:' + sha256(summary + JSON.stringify(findings))
  };

  return output;
}
