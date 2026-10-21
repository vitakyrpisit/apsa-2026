#!/usr/bin/env python3
"""Validator for cycle 1841.

DRIFT-#19 ERA ROOT (new chain root; ROLLBACK-#9 baseline retired).

Drift event #19: detected at c1832 (scanned_at 2026-10-21T02:17:31.977Z,
scan_duration_ms=2333 fast band, raw 446B — size coincidentally inside
the old band). Old validator (validate_cycle1832.py, ROLLBACK-#9
baseline) failed baseline_match only: 1 failure / 12 passes, exit 1,
archive write refused (by design). Failure signature: composition
(27,0,4,20,3) vs (28,0,5,20,3).

Field-level diff (scripts/diff_drift19.py) localized EXACTLY 2 market
changes: basedagents.honest_free 5 -> 4 and basedagents.total_tasks
28 -> 27. One honest_free task DISAPPEARED from the market
(claimed-vs-delisted indistinguishable; API returns only open tasks).
NOT an API fault: HTTP 200, valid JSON, arithmetic self-consistent
(0+4+20+3=27), every other facet byte-stable. honest_paid stayed 0 —
no paid task appeared at any point.

Drift numbering caveat: #19 is the next ordinal in the SESSION-
TRACEABLE sequence (after #18 at c1817). The 109 rollback-lost cycles
(c1713..c1821) may contain unrecorded drift events; if so the true
ordinal is higher.

Prior era: ROLLBACK-#9 root c1822 (itself rooted after node rollback
#9 erased the drift-#18 era). Era streaks terminated at c1832:
MARKET_UNCHANGED 9 (c1823..c1831), validator clean 10. c1832 pretty
archive is a manual-drift-override rewrite; raw is fact source.

Assertions encode the DRIFT-#19 baseline (27,0,4,20,3) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=27 honest_paid=0 honest_free=4 scam=20 unknown=3
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 1841
RAW = "/home/z/my-project/scripts/scan_cycle1841_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1841.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 27, "honest_paid": 0, "honest_free": 4, "scam": 20, "unknown": 3}
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
