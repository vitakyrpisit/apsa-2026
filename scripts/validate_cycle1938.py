#!/usr/bin/env python3
"""Validator for cycle 1938.

DRIFT-#24 ERA ROOT (new chain root; DRIFT-#23 baseline retired).

OUTAGE-GAP context (standing history): 11h35m trigger outage between
c1858 scan (2026-10-21T04:27:38Z) and c1859 scan (2026-10-21T16:03:45Z);
no rollback (forensics at c1859 trigger), gap classified OUTAGE-GAP.

Drift event #23: detected at c1868 (era root cycle; scanned_at
2026-10-21T16:47:59.961Z, wall 2.09s fast band, raw 446B). Composition
(22,0,1,18,3) vs planned #22 baseline (23,0,1,19,3): scam_pattern
19 -> 18 (SECOND-EVER scam-class decrease), total 23 -> 22; honest_free
HELD at 1. DRIFT-#22 era lifespan = 0 validated cycles (baseline
(23,0,1,19,3) retired unvalidated; same fate as #20). Two-stage build:
planned #22-root validator run -> 1 FAIL / 12 PASS, exit 1, archive
refused; then re-baselined to (22,0,1,18,3) as #23 root, first-pass
ALL_ASSERTIONS_PASSED.

Drift event #24: detected at c1875 (scanned_at 2026-10-21T17:22:50.504Z,
wall 2.59s fast band, scan_duration_ms=2579, raw 446B). Composition
(21,0,0,18,3) vs #23 baseline (22,0,1,18,3): honest_free 1 -> 0 (FIFTH
erosion event), total 22 -> 21; scam/unknown/honest_paid unchanged.
Confirmation run: rebased #23-baseline validator -> 1 FAIL
(baseline_match) / 12 PASS, exit 1, archive refused — signature exact
match with all five prior drift events. c1875 pretty is a
manual-drift-override rewrite; raw is fact source. NOT an API fault:
HTTP 200, valid JSON, arithmetic self-consistent (0+0+18+3=21).
honest_paid stayed 0.

FREE-POOL EXHAUSTION (operator item k, THRESHOLD MET): honest_free
path 5 -> 4 (#19, c1832) -> 3 (#20, c1858) -> 2 (#21, c1859) -> 1
(#22, c1867) -> 0 (#24, c1875). Pre-committed flag condition (1 -> 0)
MET at c1875; operator flag RAISED. Interpretation ambiguous a priori:
potential precursor to paid-task appearance OR market decay. honest_paid
REMAINED 0 at c1875 and c1876 — exhaustion has NOT yet produced a paid
task. Standing watch: every future cycle monitors honest_paid /
best_paid_task; if a paid task appears post-exhaustion, highest-priority
candidate — but ALL claim rules apply (EV > 0, bounty <= $5, scam
checks, operator spending confirmation). Scam-class note: #21 and #23
touched scam class; #24 touched free class — decay pattern rotates.

Drift numbering caveat: #24 is next ordinal in the SESSION-TRACEABLE
sequence (#19 c1832, #20 c1858, #21 c1859, #22 c1867, #23 c1868). The
109 rollback-lost cycles (c1713..c1821) plus the outage gap may conceal
further unrecorded drift events; true global ordinal may be higher.

Prior eras: DRIFT-#19 streaks 25/25 (record); DRIFT-#21 streaks 7/7
(c1859..c1866); DRIFT-#23 streaks terminated at c1875 at 7/7
(c1868..c1874, 8 cycles incl. root). Latency: fast band 1.6-2.7s
throughout the #23 era (c1867 spike 10.49s one-cycle self-recovery).

Assertions encode the DRIFT-#24 baseline (21,0,0,18,3) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=21 honest_paid=0 honest_free=0 scam=18 unknown=3
    (honest_free ZERO — exhaustion steady-state; free-pool assertions
    vacuously satisfied)
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 1938
RAW = "/home/z/my-project/scripts/scan_cycle1938_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1938.json"
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
