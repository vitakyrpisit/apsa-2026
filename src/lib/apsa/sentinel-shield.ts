/**
 * SentinelShield Contract Risk Triage Core Engine (v2.1).
 * Deterministic EVM-bytecode triage: walks real opcodes.
 * No viem dependency — uses fetch for RPC, regex for address validation.
 */

import type { SentinelShieldInput, SentinelShieldOutput, Finding } from './types';
import { createHash } from 'node:crypto';

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

const MAX_BYTECODE_BYTES = 49152;

function isAddress(addr: string): boolean {
  return /^0x[0-9a-fA-F]{40}$/.test(addr);
}

export function validateSentinelInput(input: SentinelShieldInput): void {
  if (!input || typeof input !== 'object') throw new SentinelInputError('Request body must be a JSON object.', 400);
  if (input.chain && input.chain !== 'base') throw new SentinelInputError('Only chain "base" is supported.', 400);
  const addr = input.contractAddress?.trim();
  const code = input.bytecode?.trim();
  if (!addr && !code) throw new SentinelInputError('Provide "contractAddress" (Base) or "bytecode" (hex).', 400);
  if (addr && !isAddress(addr.toLowerCase())) throw new SentinelInputError('"contractAddress" is not a valid EVM address.', 400);
  if (code) {
    const hex = code.replace(/^0x/i, '');
    if (hex.length === 0 || hex.length % 2 !== 0 || !/^[0-9a-fA-F]+$/.test(hex)) throw new SentinelInputError('"bytecode" must be even-length hex.', 400);
    if (hex.length / 2 > MAX_BYTECODE_BYTES) throw new SentinelInputError(`"bytecode" exceeds ${MAX_BYTECODE_BYTES} bytes.`, 400);
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

export function scanBytecode(hexInput: string): OpcodeScan {
  const clean = hexInput.replace(/^0x/i, '').toLowerCase();
  const total = clean.length / 2;
  if (total === 0) return { codeBytes: 0, codeBytesAnalysed: 0, hasDelegatecall: false, hasCallcode: false, hasSelfdestruct: false, hasCreate: false, hasCreate2: false, hasOrigin: false, hasTimestamp: false, callCount: 0, eip1967Slot: false, minimalProxy: false, metadataTrailerBytes: 0 };

  const bytes = Buffer.from(clean, 'hex');
  const scan: OpcodeScan = { codeBytes: total, codeBytesAnalysed: 0, hasDelegatecall: false, hasCallcode: false, hasSelfdestruct: false, hasCreate: false, hasCreate2: false, hasOrigin: false, hasTimestamp: false, callCount: 0, eip1967Slot: false, minimalProxy: false, metadataTrailerBytes: 0 };

  // Check EIP-1167 minimal proxy
  if (total >= 45) {
    const head = clean.substring(0, 20);
    if (head === '363d3d373d3d3d363d73' && bytes.subarray(30, 45).toString('hex') === '5af43d82803e903d91602b57fd5bf3') {
      scan.minimalProxy = true;
    }
  }

  // Check EIP-1967 slot references
  if (clean.includes(EIP1967_IMPL_SLOT) || clean.includes(EIP1967_ADMIN_SLOT)) {
    scan.eip1967Slot = true;
  }

  // Walk opcodes, skipping PUSH data
  let i = 0;
  while (i < bytes.length) {
    const op = bytes[i];
    scan.codeBytesAnalysed++;
    switch (op) {
      case 0x00: case 0x01: case 0x02: case 0x03: case 0x04: case 0x05: case 0x06: case 0x07:
      case 0x08: case 0x09: case 0x0a: case 0x0b: case 0x0c: case 0x0d: case 0x0e: case 0x0f:
      case 0x10: case 0x11: case 0x12: case 0x13: case 0x14: case 0x15: case 0x16: case 0x17:
      case 0x18: case 0x19: case 0x1a: case 0x1b: case 0x1c: case 0x1d: case 0x1e: case 0x1f:
      case 0x20: case 0x21: case 0x22: case 0x23: case 0x24: case 0x25: case 0x26: case 0x27:
      case 0x28: case 0x29: case 0x2a: case 0x2b: case 0x2c: case 0x2d: case 0x2e: case 0x2f:
      case 0x30: case 0x31: case 0x32: case 0x33: case 0x34: case 0x35: case 0x36: case 0x37:
      case 0x38: case 0x39: case 0x3a: case 0x3b: case 0x3c: case 0x3d: case 0x3e: case 0x3f:
      case 0x40: case 0x41: case 0x42: case 0x43: case 0x44: case 0x45: case 0x46: case 0x47:
      case 0x50: case 0x51: case 0x52: case 0x53: case 0x54: case 0x55: case 0x56: case 0x57:
      case 0x58: case 0x59: case 0x5a: case 0x5b: case 0x5c: case 0x5d: case 0x5e: case 0x5f:
      case 0xa0: case 0xa1: case 0xa2: case 0xa3: case 0xa4: case 0xa5:
      case 0xf0: case 0xf1: case 0xf2: case 0xf3: case 0xf4: case 0xf5:
      case 0xfa: case 0xfd: case 0xfe:
        break;
      case 0x60: case 0x61: case 0x62: case 0x63: case 0x64: case 0x65: case 0x66: case 0x67:
      case 0x68: case 0x69: case 0x6a: case 0x6b: case 0x6c: case 0x6d: case 0x6e: case 0x6f:
      case 0x70: case 0x71: case 0x72: case 0x73: case 0x74: case 0x75: case 0x76: case 0x77:
      case 0x78: case 0x79: case 0x7a: case 0x7b: case 0x7c: case 0x7d: case 0x7e: case 0x7f:
        { const n = op - 0x5f; i += n; break; }
      case 0xf1: scan.callCount++; break;
      case 0xf2: scan.callCount++; break;
      case 0xf4: scan.hasDelegatecall = true; scan.callCount++; break;
      case 0xf5: scan.hasCreate2 = true; break;
      case 0xf0: scan.hasCreate = true; break;
      case 0xff: scan.hasSelfdestruct = true; break;
      case 0x32: scan.hasOrigin = true; break;
      case 0x42: scan.hasTimestamp = true; break;
      default: break;
    }
    i++;
  }

  return scan;
}

const RULES = [
  { id: 'SEC-001', name: 'DelegatecallPresence', shortDescription: { text: 'DELEGATECALL / CALLCODE opcode present in executable code' } },
  { id: 'SEC-002', name: 'SelfdestructPresence', shortDescription: { text: 'SELFDESTRUCT opcode present in executable code' } },
  { id: 'SEC-003', name: 'TxOriginUsage', shortDescription: { text: 'ORIGIN opcode present (tx.origin may be used for authorization)' } },
  { id: 'SEC-004', name: 'ProxyPattern', shortDescription: { text: 'EIP-1967 slot constant or EIP-1167 minimal proxy detected' } },
  { id: 'SEC-005', name: 'ContractCreation', shortDescription: { text: 'CREATE / CREATE2 opcode present' } },
];

export async function analyzeContractRisk(input: SentinelShieldInput): Promise<SentinelShieldOutput> {
  const targetAddress = input.contractAddress?.toLowerCase().trim();
  let bytecode = input.bytecode || '';
  let isContractDeployed = false;

  if (targetAddress && isAddress(targetAddress)) {
    try {
      const res = await fetch('https://mainnet.base.org', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'eth_getCode', params: [targetAddress, 'latest'] }),
        signal: AbortSignal.timeout(8000),
      });
      const data = await res.json();
      const code = data?.result;
      if (code && code !== '0x') { bytecode = code; isContractDeployed = true; }
    } catch { /* offline fallback */ }
  }

  const findings: Finding[] = [];
  const s = scanBytecode(bytecode);

  if (s.hasDelegatecall) {
    findings.push({ id: 'FINDING-101', ruleId: 'SEC-001', level: 'warning', title: s.eip1967Slot ? 'DELEGATECALL used by a proxy pattern' : 'DELEGATECALL / CALLCODE present', description: 'An executable DELEGATECALL/CALLCODE opcode exists.', exploitVector: 'Storage collision or proxy implementation hijacking.', mitigation: 'Implement ERC-1967 storage slot isolation.', cvssScore: 6.8 });
  }
  if (s.hasSelfdestruct) {
    findings.push({ id: 'FINDING-102', ruleId: 'SEC-002', level: 'error', title: 'SELFDESTRUCT opcode present', description: 'Since EIP-6780 SELFDESTRUCT only removes code if called in the creating transaction.', exploitVector: 'Broken teardown logic.', mitigation: 'Refactor teardown routines.', cvssScore: 7.2 });
  }
  if (s.hasOrigin) {
    findings.push({ id: 'FINDING-103', ruleId: 'SEC-003', level: 'warning', title: 'ORIGIN opcode present', description: 'tx.origin may be used for authorization.', exploitVector: 'Phishing attack through intermediary contracts.', mitigation: 'Use msg.sender instead.', cvssScore: 5.0 });
  }
  if (s.eip1967Slot || s.minimalProxy) {
    findings.push({ id: 'FINDING-104', ruleId: 'SEC-004', level: 'note', title: s.minimalProxy ? 'EIP-1167 minimal proxy' : 'EIP-1967 proxy slot referenced', description: 'Proxy pattern detected.', exploitVector: 'Implementation address manipulation.', mitigation: 'Verify implementation is trusted.', cvssScore: 3.0 });
  }
  if (s.hasCreate || s.hasCreate2) {
    findings.push({ id: 'FINDING-105', ruleId: 'SEC-005', level: 'note', title: s.hasCreate2 ? 'CREATE2 present' : 'CREATE present', description: 'Contract creation opcode detected.', exploitVector: 'Address prediction or factory pattern.', mitigation: 'Verify creation logic is access-controlled.', cvssScore: 3.0 });
  }

  let riskLevel: SentinelShieldOutput['riskLevel'] = 'LOW';
  let overallScore = 88;
  let exploitability: SentinelShieldOutput['exploitability'] = 'LOW';
  if (findings.some(f => f.level === 'error')) { riskLevel = 'HIGH'; overallScore = 48; exploitability = 'HIGH'; }
  else if (findings.length > 0) { riskLevel = 'MEDIUM'; overallScore = 72; exploitability = 'MEDIUM'; }
  else { riskLevel = 'LOW'; overallScore = 94; exploitability = 'NONE'; }

  const summary = `SentinelShield audited ${targetAddress || 'bytecode'}. Bytecode analysed (${s.codeBytes} bytes, ${s.codeBytesAnalysed} opcodes). ${findings.length} findings. Risk: ${riskLevel} (${overallScore}/100).`;

  return {
    service: 'SentinelShield Contract Risk Triage',
    version: '2.1.0',
    target: { chain: input.chain || 'base', contractAddress: targetAddress, verifiedOnScan: isContractDeployed },
    riskLevel, overallScore, summary, exploitability, findings,
    metrics: { reentrancyProtected: null, flashLoanDrainVulnerable: null, unauthorizedUpgradeVector: s.hasDelegatecall, uncheckedArithmetic: null },
    sarif: { $schema: 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json', version: '2.1.0', runs: [{ tool: { driver: { name: 'SentinelShield Static Analyzer', version: '2.1.0', rules: RULES } }, results: findings.map(f => ({ ruleId: f.ruleId, level: f.level, message: { text: `${f.title}: ${f.description}` } })) }] },
    generatedAt: new Date().toISOString(),
    sha256Checksum: 'sha256:' + sha256(summary + JSON.stringify(findings)),
  };
}
