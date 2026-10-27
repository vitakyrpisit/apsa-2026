#!/usr/bin/env python3
"""Validator for cycle 1769.

DRIFT-#16 REBASE POINT (new era root; prior drift-#15 validator chain
validate_cycle1713..1714.py encoded the (28,2,5,18,3) @ 24392B baseline
and is retired by this drift event).

Drift event #16: detected at c1715 (scanned_at 2026-10-20T16:12:32.519Z
= 2026-10-21 00:12:32 +08, scan_duration_ms=2073 fast band, raw 16408B,
-7984B vs drift-#15 band — same -7984B step as drifts #14/#15, i.e.
one paid-task payload removal each time). Changes vs drift-#15 baseline
(28,2,5,18,3):
  - task_5yzaOsv8NK1uNPtq59d2v (WURK onboarding pilot 2/5, 0.10 USDC)
    DISAPPEARED (cause not determinable: API returns only open tasks;
    claimed-vs-delisted indistinguishable)
  - honest_paid 2->1; sole surviving slot: task_qKxsDuYZks86pyzXcpgpU
    (pilot 3/5, also the unchanged best_paid_task) — bounty=100000 raw
    (0.10 USDC), escrow=funded, open, unclaimed
  - honest_free=5, scam=18, unknown=3 all unchanged; total 28->27
  - all other facets unchanged: taskbounty api_key=False
    paid_missions=0, clawlancer absent, auto_claim_pending=False,
    next_scan=300

WURK pilot attrition pattern (visible inventory): 4 slots at drift-#14
(c1711, 5/5 gone) -> 3 slots at drift-#15 (c1713, 4/5 gone) -> 1 slot
at drift-#16 (c1715, 2/5 gone). One slot remains (3/5).

Old-baseline probe evidence (validate_cycle1714.py logic against c1715
payload, scratch run, artifacts cleaned): ASSERTION_FAILURES: 4 —
  size_matches_baseline_band (16408B vs band (24392, 24393)),
  baseline_match ((27,1,5,18,3) vs (28,2,5,18,3)),
  all_honest_paid_len (1 vs 2),
  expected_paid_ids (5yzaOsv8 missing).
best_paid_task assertion did NOT fail (sole survivor is the prior
best_paid). All per-task assertions for the surviving slot passed.

recursive_diff c1714 vs c1715 (correct arg order <new> <old>):
MARKET_CHANGED (stripped canonical 24834 -> 16693). Drift-#16 era
stripped-canonical constant: 16693 bytes.

Assertions encode the drift-#16 baseline (27,1,5,18,3) @ 16408B:
  - response size 16408 bytes (band 16408-16409)
  - BA composition: total=27 honest_paid=1 honest_free=5 scam=18 unknown=3
  - 1 honest paid task, best_paid_task=task_qKxsDuYZks86pyzXcpgpU
  - escrow status=funded, status=open, unclaimed
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1769
RAW = "/home/z/my-project/scripts/scan_cycle1769_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1769.json"
BASELINE_SIZE_BAND = (16408, 16409)
BASELINE_COMP = {"total": 27, "honest_paid": 1, "honest_free": 5, "scam": 18, "unknown": 3}
BEST_PAID = "task_qKxsDuYZks86pyzXcpgpU"
EXPECTED_PAID_IDS = [
    "task_qKxsDuYZks86pyzXcpgpU",
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
