#!/usr/bin/env python3
"""Validator for cycle 2060.

DRIFT-#24 ERA ROOT RE-ESTABLISHMENT (ROLLBACK-#10 RECOVERY CYCLE).

Rollback event #10: discovered at the 2026-10-23 00:03:03 +08 trigger
(~11h31m after c2008, 2026-10-22 12:27). The node environment was
restored to an on-disk state as of c1858 (2026-10-21 ~12:32 +08
snapshot). Losses verified by direct inspection:
  - worklog.md truncated at the c1858 entry (49 Task ID lines,
    7826 lines total); entries c1859..c2008 (150 cycles) ERASED
  - scripts archive chain truncated: validate_cycle1859..2008.py,
    scan_cycle1859..2008*.json, recursive_diff-era artifacts ABSENT
  - qualify_scan.py ABSENT (rebuilt this cycle as RECOVERY BUILD)
  - no on-node backups found (project root scan: no backup*/ *.bak)
Session-verifiable record survives in agent conversation trace:
  - lost-era drifts: DRIFT-#23 @ c1868 (scam 19->18), DRIFT-#24
    @ c1875 (honest_free 1->0, free-pool exhaustion, (k) flag)
  - DRIFT-#24 era baseline (21,0,0,18,3) held from c1876 through
    c2008; era MARKET_UNCHANGED streak 132, validator clean 132
  - record latency run x25 (era high 7.446s @ c1991); run broken
    @ c2006 (1.928s); WATCH episode 2 open at count 2 (c2007
    2.648s + c2008 2.544s)
  - cumulative at c2008 close: 2009 scans, 0 claims, 0 violations,
    0 spend, 0 revenue
Rollback numbering: #10 is next in the SESSION-TRACEABLE sequence
(after #9, which lost c1713..c1821); standing caveat applies.

This cycle re-roots the validation chain on the DRIFT-#24 baseline,
verified against the LIVE market at scan time (five-tuple matched
before this validator was built). Assertions encode (21,0,0,18,3)
@ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=21 honest_paid=0 honest_free=0 scam=18 unknown=3
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 2060
RAW = "/home/z/my-project/scripts/scan_cycle2060_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2060.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 3}
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
