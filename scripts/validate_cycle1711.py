#!/usr/bin/env python3
"""Validator for cycle 1711.

DRIFT-#14 REBASE POINT (new era root; prior post-rollback-#7 validator
chain validate_cycle1700..1710.py encoded the (25,4,1,17,3) @ 40360B
baseline and is retired by this drift event).

Drift event #14: detected at c1711 (scanned_at 2026-10-20T04:27:14.486Z,
scan_duration_ms=5237 slow band, raw 32376B). Task
task_tCnB8RqX3b3iOrNjXBHVW (WURK onboarding pilot 5/5, 0.10 USDC, the
prior best_paid_task) DISAPPEARED from the market: total_tasks 25->24,
honest_paid 4->3. Disappearance cause is NOT determinable from payload
(API returns only open tasks; claimed-vs-delisted indistinguishable).
The 3 surviving WURK slots (4/5, 3/5, 2/5) are all bounty=100000 raw
units (0.10 USDC), escrow=funded, status=open, claimed_by=None.
All other market facets unchanged: honest_free=1, scam=17, unknown=3,
taskbounty api_key=False paid_missions=0, clawlancer absent,
auto_claim_pending=False, next_scan=300.

Old-baseline probe evidence (validate_cycle1710.py logic against c1711
payload, scratch run): ASSERTION_FAILURES: 5 —
  size_matches_baseline_band (32376B vs band (40360, 40361)),
  baseline_match ((24,3,1,17,3) vs (25,4,1,17,3)),
  all_honest_paid_len (3 vs 4),
  expected_paid_ids (tCnB8RqX missing),
  best_paid_task (8zjlRRCh != tCnB8RqX).
All per-task assertions for surviving slots passed.

recursive_diff c1710 vs c1711 (correct arg order <new> <old>):
MARKET_CHANGED (stripped canonical 41116 -> 32975). Drift-#14 era
stripped-canonical constant: 32975 bytes.

Assertions encode the drift-#14 baseline (24,3,1,17,3) @ 32376B:
  - response size 32376 bytes (band 32376-32377)
  - BA composition: total=24 honest_paid=3 honest_free=1 scam=17 unknown=3
  - 3 honest paid tasks, best_paid_task=task_8zjlRRChZW7kWIb0Oy6Ai
  - all escrow status=funded, status=open, unclaimed
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1711
RAW = "/home/z/my-project/scripts/scan_cycle1711_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1711.json"
BASELINE_SIZE_BAND = (32376, 32377)
BASELINE_COMP = {"total": 24, "honest_paid": 3, "honest_free": 1, "scam": 17, "unknown": 3}
BEST_PAID = "task_8zjlRRChZW7kWIb0Oy6Ai"
EXPECTED_PAID_IDS = [
    "task_8zjlRRChZW7kWIb0Oy6Ai",
    "task_qKxsDuYZks86pyzXcpgpU",
    "task_5yzaOsv8NK1uNPtq59d2v",
]

failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"ok: {name}" + (f" ({detail})" if detail else ""))
    else:
        failures.append(f"{name} ({detail})")
        print(f"FAIL: {name} ({detail})")


with open(RAW, "rb") as f:
    raw_bytes = f.read()
print(f"clean_body_bytes={len(raw_bytes)}")
check("size_matches_baseline_band", len(raw_bytes) in BASELINE_SIZE_BAND,
      f"{len(raw_bytes)}B vs band {BASELINE_SIZE_BAND}")

d = json.loads(raw_bytes)
ba = d.get("basedagents", {})
hp = ba.get("all_honest_paid", []) or []
tb = d.get("taskbounty", {})

comp = {
    "total": ba.get("total_tasks"),
    "honest_paid": ba.get("honest_paid"),
    "honest_free": ba.get("honest_free"),
    "scam": ba.get("scam_pattern"),
    "unknown": ba.get("unknown"),
}
print(f"scanned_at={d.get('scanned_at')}")
print(f"scan_duration_ms={d.get('scan_duration_ms')}")
print(f"BA composition: total={comp['total']} honest_paid={comp['honest_paid']} "
      f"honest_free={comp['honest_free']} scam={comp['scam']} unknown={comp['unknown']}")
check("baseline_match", comp == BASELINE_COMP, str(comp))
check("all_honest_paid_len", len(hp) == BASELINE_COMP["honest_paid"], f"len={len(hp)}")

for t in hp:
    tid = t.get("task_id")
    esc = (t.get("escrow") or {}).get("status")
    print(f"  paid_task={tid} bounty={t.get('bounty', {}).get('amount_atomic')} "
          f"{t.get('bounty', {}).get('token')} escrow={esc} status={t.get('status')} "
          f"claimed_by={t.get('claimed_by')}")
    check(f"escrow_funded:{tid}", esc == "funded", str(esc))
    check(f"status_open:{tid}", t.get("status") == "open", str(t.get("status")))
    check(f"unclaimed:{tid}", t.get("claimed_by") is None, str(t.get("claimed_by")))

ids = [t.get("task_id") for t in hp]
check("expected_paid_ids", sorted(ids) == sorted(EXPECTED_PAID_IDS), str(ids))

bpt = ba.get("best_paid_task") or {}
check("best_paid_task", bpt.get("task_id") == BEST_PAID, str(bpt.get("task_id")))

print(f"taskbounty: api_key={tb.get('api_key_configured')} bounties={tb.get('total_bounties')} "
      f"paid_missions={tb.get('paid_missions')}")
check("taskbounty_no_key", tb.get("api_key_configured") is False)
check("taskbounty_paid_zero", (tb.get("paid_missions") or 0) == 0)
check("clawlancer_absent", "clawlancer" not in json.dumps(d).lower())
check("auto_claim_pending_false", d.get("auto_claim_pending") is False)
check("next_scan_300", d.get("next_scan_in_seconds") == 300, str(d.get("next_scan_in_seconds")))

if failures:
    print(f"ASSERTION_FAILURES: {len(failures)}")
    for f_ in failures:
        print(f"  - {f_}")
    sys.exit(1)

with open(PRETTY, "w") as f:
    f.write(json.dumps(d, indent=2, sort_keys=False) + "\n")
print(f"archive_written={PRETTY}")
print("ALL_ASSERTIONS_PASSED")
print(f"baseline_match_c{CYCLE}=true")
