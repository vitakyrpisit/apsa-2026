// Generate receive-only EVM wallet for BasedAgents agent v6.
// The private key is NEVER printed to stdout — written directly to protected file (mode 600).
// This wallet only RECEIVES USDC payouts. Operator never funds it; agent never spends from it.
// Re-registered 2026-10-09 after sandbox wipe destroyed v5 keypair (ag_EuuNoKptr2m6kBsmF1ZWZZFCPhaWnzkQ1iWj4N4dPiJh).
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'fs';

const KEYFILE = '/home/z/my-project/.basedagents/keys/apsa-2026-bugfixer-v6-evm-wallet.json';

let privateKey, account;

if (existsSync(KEYFILE)) {
  // Idempotent: reuse existing wallet if present
  const existing = JSON.parse(readFileSync(KEYFILE, 'utf8'));
  account = privateKeyToAccount(existing.private_key);
  console.log('REUSED existing v6 wallet (idempotent):', account.address);
  process.exit(0);
}

privateKey = generatePrivateKey();
account = privateKeyToAccount(privateKey);

const record = {
  purpose: 'receive-only payout wallet for BasedAgents agent v6 (ag_H4iqUgXaxg86ZSaaUej2fLVLxGnmaon58wxs2pJskqjG)',
  address: account.address,
  network: 'eip155:8453 (Base)',
  private_key: privateKey,
  created_at: new Date().toISOString(),
  policy: 'NEVER fund from operator money. NEVER spend. Receive-only. Never print private_key.',
};

mkdirSync('/home/z/my-project/.basedagents/keys', { recursive: true });
writeFileSync(KEYFILE, JSON.stringify(record, null, 2), { mode: 0o600 });

// Print ONLY the address (public info)
console.log('GENERATED new v6 wallet:', account.address);
