#!/usr/bin/env python3
"""Validator for cycle 1822.

ROLLBACK-#9 ERA ROOT (new chain root; prior chains lost to node rollback).

Rollback event #9: detected at c1822 trigger (2026-10-21 09:22:22 +08:00)
when worklog.md shrank 9184 -> 7074 lines and its mtime read
2026-10-20T04:32:44Z (= the c1712 close instant). Node filesystem state
reverted ~21h. Last surviving worklog entry: c1712 (drift-#14 era,
post-rollback-#7 chain root c1700).

LOST to rollback #9 (no off-node backup existed; item (h) had stood at
CRITICAL HIGHEST):
  - worklog entries c1713..c1821 (109 cycles)
  - archives scan_cycle{1713..1821}_raw.json + .json
  - validator chain validate_cycle{1713..1821}.py
  - drift-#17 and drift-#18 era artifacts (era root validate_cycle1818.py)

SURVIVED: worklog.md through c1712; 13 raw archives (c1700..c1712, the
post-#7 chain); validate_cycle{1700..1712}.py; scan_cycle1712.json.

Market NOT rolled back (external API): fresh c1822 payload measured
(28, 0, 5, 20, 3) @ 446B, matching the drift-#18 baseline held through
c1821 per session context (era root c1818; streak 4 at loss time).
This validator re-roots the chain on that measured baseline.

Assertions encode the drift-#18/rollback-#9 baseline (28,0,5,20,3) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=28 honest_paid=0 honest_free=5 scam=20 unknown=3
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 1822
RAW = "/home/z/my-project/scripts/scan_cycle1822_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1822.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 28, "honest_paid": 0, "honest_free": 5, "scam": 20, "unknown": 3}
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
