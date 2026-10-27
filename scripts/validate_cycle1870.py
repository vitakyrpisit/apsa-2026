#!/usr/bin/env python3
"""Validator for cycle 1870.

DRIFT-#23 ERA ROOT (new chain root; DRIFT-#21 baseline retired; DRIFT-#22
baseline never materialized as an era).

OUTAGE-GAP context (standing history): 11h35m trigger outage between
c1858 scan (2026-10-21T04:27:38Z) and c1859 scan (2026-10-21T16:03:45Z);
no rollback (forensics at c1859 trigger), gap classified OUTAGE-GAP.

Drift event #22: detected at c1867 (scanned_at 2026-10-21T16:42:53.695Z,
wall 10.49s, raw 447B). Old validator failed baseline_match only: 1
failure / 12 passes, exit 1, archive refused — signature matched
#19/#20/#21. Field-level: honest_free 2 -> 1, total 24 -> 23 (FOURTH
honest_free erosion event). c1867 pretty is a manual-drift-override
rewrite; raw is fact source. DRIFT-#22 era root was planned for c1868
with baseline (23,0,1,19,3) but the market moved AGAIN before any
era-root validation -> DRIFT-#22 era lifespan = 0 validated cycles
(baseline (23,0,1,19,3) retired unvalidated).

Drift event #23: detected at c1868 (era root cycle;
scanned_at 2026-10-21T16:47:59.961Z, wall 2.09s fast band,
scan_duration_ms=2081, raw 446B). Composition (22,0,1,18,3) vs planned
#22 baseline (23,0,1,19,3): scam_pattern 19 -> 18 (SECOND-EVER
scam-class decrease; first was #21), total 23 -> 22; honest_free HELD
at 1 (no further erosion at c1868). Confirmation run: the planned
#22-root validator (baseline 23,0,1,19,3) built and executed against
this raw -> 1 FAIL (baseline_match) / 12 PASS, exit 1, archive refused,
then re-baselined to (22,0,1,18,3) as this root. NOT an API fault:
HTTP 200, valid JSON, arithmetic self-consistent (0+1+18+3=22).
honest_paid stayed 0.

Drift numbering caveat: #23 is next ordinal in the SESSION-TRACEABLE
sequence (#19 c1832, #20 c1858, #21 c1859, #22 c1867). The 109
rollback-lost cycles (c1713..c1821) plus the outage gap may conceal
further unrecorded drift events; true global ordinal may be higher.

Erosion watch (operator item k): honest_free path 5 -> 4 (#19, c1832)
-> 3 (#20, c1858) -> 2 (#21, c1859) -> 1 (#22, c1867), HELD at 1 in
#23 (c1868). Free pool ONE task from exhaustion — if a future drift
touches honest_free (1 -> 0), flag as FREE-POOL EXHAUSTION signal
(potential precursor to paid-task appearance OR market decay;
indistinguishable a priori). Note: two of the last three drifts
(#21, #23) touched the scam class — market decay may be broadening.

Prior eras: DRIFT-#19 era streaks 25/25 (record); DRIFT-#21 era
streaks terminated at c1867 at 7/7 (c1859..c1866, 8 cycles incl.
root). Latency note: c1867 spike 10.49s was one-cycle (c1868 2.09s
fast band, self-recovery like c1841 precedent); watch stays closed.

Assertions encode the DRIFT-#23 baseline (22,0,1,18,3) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=22 honest_paid=0 honest_free=1 scam=18 unknown=3
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 1870
RAW = "/home/z/my-project/scripts/scan_cycle1870_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1870.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 22, "honest_paid": 0, "honest_free": 1, "scam": 18, "unknown": 3}
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
