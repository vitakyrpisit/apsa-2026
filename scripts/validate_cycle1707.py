#!/usr/bin/env python3
"""Validator for cycle 1707.

POST-ROLLBACK-#7 REBASE POINT (new era root; prior era root
validate_cycle1695.py chain and entire drift-#13 validator set
validate_cycle1675..1694.py were ERASED by midnight rollback event #7).

Rollback event #7 (7th occurrence of item (g)): detected 2026-10-20
11:32 +08 on trigger delivery. Session outage ~11:07 -> ~11:31 (~24 min,
triggers c1695..c1699 undelivered; c1695 and c1700 arrived batched).
Filesystem rolled back to ~Oct 13 04:29 snapshot (SAME snapshot as
rollback #6):
  - worklog.md restored to Oct 13 state (578927B, mtime Oct 13 04:29;
    ALL post-rollback-#6 era entries c1675..c1694 gone)
  - scripts/: all validate_cycle16*.py + scan_cycle16*.json archives
    ERASED (only cycle-210-era clawlancer files survive)
  - tool-results/: era artifacts erased
  - .basedagents/ tree ENTIRELY GONE (keypair item (a) absent again,
    along with dir)
Drift-#13 era record preserved ONLY in conversation context:
  1694 cumulative executions, 0 claims, 0 violations, 0 spend, 0 revenue;
  validator clean streak 46 (final); drift-#13 era MARKET_UNCHANGED
  streak 45 (final at c1694); baseline was (25,4,1,17,3) @ 40360B /
  normalized 41087; 4 WURK slots funded/open/unclaimed; one slow-band
  scan (7078ms at c1685, one-off).

Post-rollback re-baseline at c1700 (scanned_at 2026-10-20T03:38:47Z):
  - composition IDENTICAL to drift-#13 baseline: (25,4,1,17,3)
  - same 4 WURK task IDs, bounty=100000 raw (0.10 USDC), escrow=funded,
    status=open, claimed_by=None -> MARKET_CARRIED_ACROSS_ROLLBACK
  - raw size 40360B (in band), taskbounty api_key=False paid_missions=0,
    clawlancer absent, auto_claim_pending=False, next_scan=300

Assertions encode the post-rollback-#7 baseline (25,4,1,17,3) @ 40360B:
  - response size 40360 bytes (band 40360-40361; size fluctuates only
    via scan_duration_ms digit count)
  - BA composition: total=25 honest_paid=4 honest_free=1 scam=17 unknown=3
  - 4 honest paid tasks, best_paid_task=task_tCnB8RqX3b3iOrNjXBHVW
  - all escrow status=funded, status=open, unclaimed
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1707
RAW = "/home/z/my-project/scripts/scan_cycle1707_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1707.json"
BASELINE_SIZE_BAND = (40360, 40361)
BASELINE_COMP = {"total": 25, "honest_paid": 4, "honest_free": 1, "scam": 17, "unknown": 3}
BEST_PAID = "task_tCnB8RqX3b3iOrNjXBHVW"
EXPECTED_PAID_IDS = [
    "task_tCnB8RqX3b3iOrNjXBHVW",
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
