#!/usr/bin/env python3
"""Validator for cycle 2133.

DRIFT-#25 ERA OPENING CYCLE (composition change vs DRIFT-#24).

DRIFT-#24 era (baseline (21,0,0,18,3)) ran from c1876 through c2092
(217-cycle span incl. rollback-#10 recovery re-root at c2009; era
closing streaks: MARKET_UNCHANGED 216, validator clean 216). At
c2093 the live market composition changed, verified by field-level
raw diff (exactly two payload fields moved, plus routine timestamps):
  - basedagents.total_tasks 21 -> 22
  - basedagents.unknown 3 -> 4
  - honest_paid=0, honest_free=0, scam=18 ALL UNCHANGED
    (no (k) precursor; best_paid_task=None, PAID_FOUND=False;
    zero-claim posture holds trivially)
Internal consistency holds: 22 = 0+0+18+4; best_paid_task None is
consistent with honest_paid=0. The +1 unknown task is a genuinely
unclassified addition (not honest, not scam-pattern). Era renamed
DRIFT-#25 per drift-numbering convention; this validator re-roots
the validation chain on the new baseline, verified against the LIVE
market at scan time (five-tuple matched before this validator was
built). Assertions encode (22,0,0,18,4) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=22 honest_paid=0 honest_free=0 scam=18 unknown=4
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 2133
RAW = "/home/z/my-project/scripts/scan_cycle2133_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2133.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 22, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 4}
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
