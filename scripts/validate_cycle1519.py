#!/usr/bin/env python3
"""Validator for cycle 1506.

DRIFT-#9 REBASE POINT (chain root for the new era; prior era root
validate_cycle1414.py, last prior-era source validate_cycle1505.py).

Drift #9 observed at c1519 (trigger 2026-10-19 07:41:30 +08:00, scanned_at
2026-10-18T23:46:22.294Z): FIRST honest paid tasks in 1506 cycles.
  - WURK onboarding pilot 1/5..5/5 (5 tasks, one creator
    ag_Cz3eFFDssop1mixwEu2yKrArLh4iYD3zf3aSVB657VRc), 0.10 USDC each on Base
    (eip155:8453), all escrow=funded with individual deposit_tx_hash, all
    unclaimed, created 2026-10-18T23:38:23..40Z.
  - Delta vs drift-#8 baseline: total 23->28, honest_paid 0->5;
    honest_free/scam/unknown unchanged (4/16/3).
  - Drift-#8 era lasted 92 obs (c1414..c1505). Paid-zero streak ended at 242
    consecutive cycles (c1264..c1505).
  - Response size 446B -> 48344B (task detail payloads now present).

CAUTION: honest_paid is claim-sensitive (5 slots, max 1 claim per agent,
tasks expire 2026-11-17). Expect possible micro-drifts; adjust per evidence.

Assertions encode the drift-#9 baseline (28,5,4,16,3) @ 48344B:
  - response size 48344 bytes
  - BA composition: total=28 honest_paid=5 honest_free=4 scam=16 unknown=3
  - 5 honest paid tasks, best_paid_task=task_tCnB8RqX3b3iOrNjXBHVW
  - all escrow status=funded
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1519
RAW = "/home/z/my-project/scripts/scan_cycle1519_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1519.json"
BASELINE_SIZE = 48344
BASELINE_COMP = {"total": 28, "honest_paid": 5, "honest_free": 4, "scam": 16, "unknown": 3}
BEST_PAID = "task_tCnB8RqX3b3iOrNjXBHVW"

def fail(msg):
    print(f"ASSERT_FAIL: {msg}")
    sys.exit(1)

raw = open(RAW, "rb").read()
clean = raw.strip()
print(f"clean_body_bytes={len(clean)}")

if len(clean) != BASELINE_SIZE:
    fail(f"size {len(clean)} != baseline {BASELINE_SIZE}")
print(f"size_matches_baseline=true ({len(clean)}B vs {BASELINE_SIZE}B)")

try:
    d = json.loads(clean)
except Exception as e:
    fail(f"json invalid: {e}")
print("json_valid=true")
print(f"scanned_at={d.get('scanned_at')}")
print(f"scan_duration_ms={d.get('scan_duration_ms')}")

ba = d.get("basedagents", {})
# Actual key names verified from raw response at c1519:
# total_tasks / honest_paid / honest_free / scam_pattern / unknown / best_paid_task / all_honest_paid
comp = {
    "total": int(ba.get("total_tasks", 0) or 0),
    "honest_paid": int(ba.get("honest_paid", 0) or 0),
    "honest_free": int(ba.get("honest_free", 0) or 0),
    "scam": int(ba.get("scam_pattern", 0) or 0),
    "unknown": int(ba.get("unknown", 0) or 0),
}

print(f"BA composition: total={comp['total']} honest_paid={comp['honest_paid']} honest_free={comp['honest_free']} scam={comp['scam']} unknown={comp['unknown']}")

if comp != BASELINE_COMP:
    fail(f"composition {comp} != drift-#9 baseline {BASELINE_COMP}")
print(f"baseline_match_c{CYCLE}=true")

honest_paid = ba.get("all_honest_paid") or []
honest_paid_len = len(honest_paid) if isinstance(honest_paid, (list, dict)) else int(honest_paid or 0)
print(f"all_honest_paid_len={honest_paid_len}")
if honest_paid_len != 5:
    fail(f"honest_paid_len {honest_paid_len} != 5")

for t in honest_paid:
    tid = t.get("task_id")
    esc = (t.get("escrow") or {}).get("status")
    print(f"  paid_task={tid} bounty={t.get('bounty_amount')} {t.get('bounty_token')} escrow={esc} status={t.get('status')} claimed_by={t.get('claimed_by_agent_id')}")
    if esc != "funded":
        fail(f"task {tid} escrow status {esc} != funded")
    if t.get("status") != "open":
        fail(f"task {tid} status {t.get('status')} != open")
    if t.get("claimed_by_agent_id") is not None:
        fail(f"task {tid} already claimed: {t.get('claimed_by_agent_id')}")

bpt = ba.get("best_paid_task") if "best_paid_task" in ba else d.get("best_paid_task")
bpt_id = (bpt or {}).get("task_id") if isinstance(bpt, dict) else bpt
print(f"best_paid_task={bpt_id}")
if bpt_id != BEST_PAID:
    fail(f"best_paid_task {bpt_id} != {BEST_PAID}")

tb = d.get("taskbounty", {})
print(f"taskbounty: api_key={bool(tb.get('api_key'))} bounties={len(tb.get('bounties', []) or [])} paid_missions={len(tb.get('paid_missions', []) or [])}")
if tb.get("api_key"):
    fail("taskbounty api_key present (unexpected)")
if len(tb.get("paid_missions", []) or []) != 0:
    fail("taskbounty paid_missions > 0")

cl = d.get("clawlancer", {})
clawlancer_present = bool(cl) or (d.get("clawlancer_present") is True)
print(f"clawlancer_present={clawlancer_present}")
if clawlancer_present:
    fail("clawlancer present (unexpected)")

acp = d.get("auto_claim_pending", False)
print(f"auto_claim_pending={acp}")
if acp:
    fail("auto_claim_pending=true (unexpected)")

print(f"next_scan_in_seconds={d.get('next_scan_in_seconds')}")

with open(PRETTY, "w") as f:
    json.dump(d, f, indent=2, sort_keys=True)
print(f"archive_written={PRETTY}")
print("ALL_ASSERTIONS_PASSED")
