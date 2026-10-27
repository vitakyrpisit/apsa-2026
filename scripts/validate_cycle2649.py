#!/usr/bin/env python3
"""Validator for cycle 2649.

DRIFT-#45 verification-27 CARRY (post-LOSS-#6 rebadge lineage, third sed-carry): rebuilt from the
verification-26 carry validate_cycle2648.py (post-LOSS-#6 sed-carry class, honest
context-carried provenance; the c2577..c2645 harnesses are LOST).
Baseline
(18,0,0,18,0) @ 446B DRIFT-#45 root; c2649 = verification 27
(c2648 = verification 26; c2647 = verification 25; c2646 = verification 24; c2645 = verification 23; c2644 = verification 22; c2643 = verification 21; ... c2624 = verification 2;
c2623 = verification 1, DRIFT-#45 root declared 2026-10-27 ~06:04 +08 — the c2623-c2645 chain is
CONTEXT-CARRIED from the pre-loss ledger (9791-line worklog @ c2645 tail, attested by the executing
session's conversation summary before the rollback); disk-recoverable lineage restarts at
c2576 = DRIFT-#34 verification-14 harness / LOSS EVENT #5 reconstruction precedent;
DRIFT-#44 closed 4-fold after root c2619, DRIFT-#43 and earlier closed pre-root — all context-carried).

LOSS EVENT #6 (declared 2026-10-27 ~09:00 +08 by the c2646 executing session): disk state rolled back
to the c2576 exit state — git HEAD 0159607 (foreign scratch commit, 2026-10-26 04:44:42 +0000) atop
828f53b (post-c2576, 2026-10-26 04:44:26 +0000). Worklog 9791 -> 8095 lines (c2577-c2645 ledger
lost). scripts corpus wiped beyond c2576. The lost-span scans (c2577-c2645) were executed and
verified honest_paid=0 pre-loss (context-carried); commit objects 7df8989 / 2aacad8 absent from the
object database. Cross-loss continuity: the fresh c2646 capture returned (18,0,0,18,0) @ 446B —
composition-identical to the context-carried c2645 state; the loss destroyed LEDGER STATE ONLY.

Assertions encode the DRIFT-#45 baseline (18,0,0,18,0) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=18 honest_paid=0 honest_free=0 scam=18 unknown=0
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 2649
RAW = "/home/z/my-project/scripts/scan_cycle2649_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2649.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 18, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 0}
BEST_PAID = None
EXPECTED_PAID_IDS = []

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
