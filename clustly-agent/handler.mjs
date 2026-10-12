// APSA Security & Code Review Agent — Clustly handler
// Receives {criteria, inputs} from a funded order, returns a structured audit report.
// Supports: Solidity, TypeScript/JavaScript, Python, and generic code review.
// Fetches code from GitHub URLs (raw.githubusercontent.com) or analyzes inline code.

const SOLIDITY_PATTERNS = [
  { id: 'SOL-REENTRANCY', severity: 'HIGH', pattern: /\.call\s*\{[^}]*\}/gs, msg: 'Potential reentrancy: external .call{...} without reentrancy guard. Ensure checks-effects-interactions pattern and use ReentrancyGuard.' },
  { id: 'SOL-EXTERNAL-CALL-UNCHECKED', severity: 'MEDIUM', pattern: /\.call\([^)]*\)\s*(?:;|\n)/g, msg: 'External .call() without return value check. Validate success: (bool success,) = target.call{...}(...); require(success).' },
  { id: 'SOL-TX-ORIGIN', severity: 'HIGH', pattern: /\btx\.origin\b/g, msg: 'tx.origin used for authorization — vulnerable to phishing attacks. Use msg.sender instead.' },
  { id: 'SOL-LOW-LEVEL-CALL', severity: 'MEDIUM', pattern: /\bdelegatecall\b/g, msg: 'delegatecall used — ensure target is trusted; delegatecall executes in caller context.' },
  { id: 'SOL-INLINE-ASSEMBLY', severity: 'LOW', pattern: /\bassembly\s*\{/g, msg: 'Inline assembly used — verify memory/stack safety; assembly bypasses Solidity safety checks.' },
  { id: 'SOL-BLOCK-TIMESTAMP', severity: 'LOW', pattern: /\bblock\.timestamp\b/g, msg: 'block.timestamp used for logic — miners can manipulate within ~15s tolerance. Avoid for strict conditions.' },
  { id: 'SOL-SELFDESTRUCT', severity: 'HIGH', pattern: /\bselfdestruct\s*\(/g, msg: 'selfdestruct — can remove contract code; deprecated in newer Solidity, restrict access.' },
  { id: 'SOL-PRIVATE-VIS', severity: 'INFO', pattern: /\bprivate\s+(mapping|address|uint|int|bytes|string)\b/g, msg: 'Private state variable — note: "private" only hides from other contracts, not off-chain.' },
  { id: 'SOL-UNCHECKED-MATH', severity: 'MEDIUM', pattern: /unchecked\s*\{/g, msg: 'unchecked arithmetic block — confirm no overflow/underflow is possible in this scope.' },
];

const TS_PATTERNS = [
  { id: 'TS-EVAL', severity: 'HIGH', pattern: /\beval\s*\(/g, msg: 'eval() used — arbitrary code execution risk. Avoid; use JSON.parse or a safe parser.' },
  { id: 'TS-CHILD-PROCESS', severity: 'HIGH', pattern: /\bexec\s*\(|\bexecSync\s*\(|\bspawn\s*\(/g, msg: 'child_process exec/spawn — command injection if input is user-controlled. Validate/sanitize input.' },
  { id: 'TS-INNERHTML', severity: 'MEDIUM', pattern: /\.innerHTML\s*=/g, msg: 'innerHTML assignment — XSS risk. Use textContent or sanitize via DOMPurify.' },
  { id: 'TS-DANGEROUS-REGEX', severity: 'LOW', pattern: /(\(\.\*\)\+|(\+\+))/g, msg: 'Potentially catastrophic backtracking regex (ReDoS). Simplify or use safe-replace.' },
  { id: 'TS-HARDCODED-SECRET', severity: 'HIGH', pattern: /(api[_-]?key|secret|password|token|private[_-]?key)\s*[=:]\s*['"][A-Za-z0-9]{16,}['"]/gi, msg: 'Hardcoded credential detected — move to env var / secrets manager.' },
  { id: 'TS-PROTOTYPE', severity: 'MEDIUM', pattern: /__proto__|constructor\[/g, msg: 'Prototype pollution vector — validate object keys before assignment.' },
  { id: 'TS-HTTP-NO-HTTPS', severity: 'LOW', pattern: /http:\/\/(?!localhost|127\.0\.0\.1)/g, msg: 'HTTP (not HTTPS) URL — data in transit is unencrypted.' },
];

const GENERAL_PATTERNS = [
  { id: 'GEN-TODO', severity: 'INFO', pattern: /\bTODO\b|\bFIXME\b|\bHACK\b|\bXXX\b/g, msg: 'Unresolved TODO/FIXME marker — review before production.' },
  { id: 'GEN-DEBUG', severity: 'LOW', pattern: /\bconsole\.(log|debug|error)\s*\(|\bprint\s*\(|\bdebugger\b/g, msg: 'Debug statement left in code — remove before production.' },
  { id: 'GEN-PRIV-KEY-LONG', severity: 'HIGH', pattern: /\b(0x)?[0-9a-fA-F]{64}\b/g, msg: '64-hex string — possible private key. Remove from source immediately.' },
];

function detectLanguage(criteria, code) {
  const c = (criteria + ' ' + code).toLowerCase();
  if (c.includes('solidity') || /\bcontract\s+\w+/i.test(code) || /\bsolidity\s*\^/i.test(code)) return 'solidity';
  if (c.includes('typescript') || c.includes('javascript') || /\bexport\s+(default|function|const)/i.test(code)) return 'typescript';
  if (c.includes('python') || /\bdef\s+\w+\s*\(/i.test(code) || /\bimport\s+\w+/i.test(code)) return 'python';
  return 'generic';
}

async function fetchGitHubRaw(url) {
  // Convert github.com/blob URLs to raw.githubusercontent.com
  let raw = url.replace('github.com/', 'raw.githubusercontent.com/').replace('/blob/', '/');
  if (!raw.startsWith('http')) raw = 'https://' + raw;
  try {
    const r = await fetch(raw, { headers: { 'User-Agent': 'APSA-Security-Agent' } });
    if (!r.ok) return null;
    return await r.text();
  } catch { return null; }
}

function extractGitHubUrls(text) {
  const urls = [];
  const re = /https?:\/\/(?:www\.)?github\.com\/[^\s"'<>]+\/blob\/[^\s"'<>]+/g;
  let m;
  while ((m = re.exec(text)) !== null) urls.push(m[0]);
  // raw URLs
  const re2 = /https?:\/\/raw\.githubusercontent\.com\/[^\s"'<>]+/g;
  while ((m = re2.exec(text)) !== null) urls.push(m[0]);
  return urls;
}

function runPatterns(code, patterns) {
  const findings = [];
  for (const p of patterns) {
    p.pattern.lastIndex = 0;
    let m;
    let count = 0;
    while ((m = p.pattern.exec(code)) !== null && count < 5) {
      const line = code.slice(0, m.index).split('\n').length;
      findings.push({ id: p.id, severity: p.severity, line, msg: p.msg, snippet: code.slice(m.index, m.index + 60).replace(/\n/g, ' ').trim() });
      count++;
    }
  }
  return findings;
}

function severityScore(findings) {
  const w = { HIGH: 10, MEDIUM: 5, LOW: 2, INFO: 0 };
  return findings.reduce((s, f) => s + (w[f.severity] || 0), 0);
}

export default async function handler({ id, input }) {
  const { criteria, inputs } = input;
  const startedAt = new Date().toISOString();

  // 1. Parse criteria for code or GitHub URL
  let code = '';
  const urls = extractGitHubUrls(criteria);
  if (inputs?.code) code += inputs.code + '\n';
  if (inputs?.url) urls.push(inputs.url);
  // If GitHub URLs found, fetch raw content
  for (const u of urls.slice(0, 3)) {
    const fetched = await fetchGitHubRaw(u);
    if (fetched) code += `\n// === ${u} ===\n${fetched}\n`;
  }
  // If no explicit code/URL, treat criteria text as inline code if it looks like code
  if (!code && (criteria.includes('function') || criteria.includes('contract') || criteria.includes('def ') || criteria.includes('{'))) {
    code = criteria;
  }

  if (!code.trim()) {
    return `# APSA Security Audit — Job ${id}\n\n**Started:** ${startedAt}\n\n## ⚠️ No code provided\n\nThe criteria did not contain a GitHub URL, inline code, or an \`inputs.code\` field.\n\n**To use this agent:**\n- Paste a GitHub blob URL (e.g. \`https://github.com/org/repo/blob/main/file.sol\`)\n- OR provide inline code in the criteria\n- OR use the \`code\` input field\n\nNo analysis performed. No charge expected.`;
  }

  // 2. Detect language + select patterns
  const lang = detectLanguage(criteria, code);
  let patterns = GENERAL_PATTERNS;
  if (lang === 'solidity') patterns = [...SOLIDITY_PATTERNS, ...GENERAL_PATTERNS];
  else if (lang === 'typescript') patterns = [...TS_PATTERNS, ...GENERAL_PATTERNS];

  // 3. Run analysis
  const findings = runPatterns(code, patterns);
  const score = severityScore(findings);
  const grade = score === 0 ? 'A' : score <= 5 ? 'B' : score <= 15 ? 'C' : score <= 30 ? 'D' : 'F';

  // 4. Build report
  const langLabel = { solidity: 'Solidity', typescript: 'TypeScript/JavaScript', python: 'Python', generic: 'Generic' }[lang] || 'Generic';
  const lines = code.split('\n').length;
  const sevCounts = { HIGH: 0, MEDIUM: 0, LOW: 0, INFO: 0 };
  findings.forEach(f => sevCounts[f.severity]++);

  let report = `# APSA Security & Code Review — Job ${id}\n\n`;
  report += `**Started:** ${startedAt}\n`;
  report += `**Completed:** ${new Date().toISOString()}\n`;
  report += `**Language:** ${langLabel}\n`;
  report += `**Lines analyzed:** ${lines}\n`;
  report += `**Sources:** ${urls.length ? urls.join(', ') : 'inline code'}\n\n`;
  report += `## Summary\n\n`;
  report += `| Severity | Count |\n|---|---|\n`;
  report += `| 🔴 HIGH | ${sevCounts.HIGH} |\n| 🟡 MEDIUM | ${sevCounts.MEDIUM} |\n| 🔵 LOW | ${sevCounts.LOW} |\n| ℹ️ INFO | ${sevCounts.INFO} |\n\n`;
  report += `**Risk grade: ${grade}** (score: ${score})\n`;
  report += grade === 'A' ? `_No significant issues detected. Minor findings may exist — review details below._\n\n` : `\n`;

  if (findings.length === 0) {
    report += `## ✅ No issues detected\n\nAutomated pattern analysis found no common vulnerability signatures.\n\n`;
    report += `**Note:** Automated scanning is a first-pass filter, not a complete audit. For production contracts handling user funds, commission a manual review.\n`;
  } else {
    report += `## Findings\n\n`;
    for (const f of findings) {
      const icon = { HIGH: '🔴', MEDIUM: '🟡', LOW: '🔵', INFO: 'ℹ️' }[f.severity];
      report += `### ${icon} [${f.severity}] ${f.id} — line ${f.line}\n\n`;
      report += `${f.msg}\n\n`;
      report += `\`\`\`\n${f.snippet}\n\`\`\`\n\n`;
    }
  }

  report += `\n---\n_APSA-2026 BugFixer — autonomous security & code review agent. This report is automated; verify critical findings manually before acting._\n`;
  return report;
}
