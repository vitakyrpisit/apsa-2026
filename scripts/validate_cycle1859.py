#!/usr/bin/env python3
"""Validator for cycle 1859.

DRIFT-#21 ERA ROOT (new chain root; DRIFT-#19 baseline retired; DRIFT-#20
baseline never materialized as an era).

OUTAGE-GAP context: 11h35m trigger outage between c1858 scan
(2026-10-21T04:27:38Z) and c1859 scan (2026-10-21T16:03:45Z).
Rollback forensics at c1859 trigger (2026-10-22T00:02:37 +08): NO rollback
— worklog 7826 lines (grown), mtime intact at c1858 closure moment
(04:29:42Z), c1858-era artifacts all present, tail entry intact.
Gap classified OUTAGE-GAP (scanner job suspended; no filesystem damage;
no data loss). Gap drift detected on first post-outage scan.

Drift event #20: detected at c1858 (scanned_at 2026-10-21T04:27:38.138Z,
wall 2.56s fast band, raw 446B). Old validator failed baseline_match
only: 1 failure / 12 passes, exit 1, archive refused — signature exactly
matched DRIFT-#19 (c1832). Field-level: honest_free 4 -> 3, total 27 ->
26 (single honest_free task disappearance). c1858 pretty is a
manual-drift-override rewrite; raw is fact source. DRIFT-#20 era root
was planned for c1859 but the market moved again during the outage gap
BEFORE any era-root validation -> DRIFT-#20 era lifespan = 0 validated
cycles (baseline (26,0,3,20,3) retired unvalidated).

Drift event #21: detected at c1859 (this cycle, first post-outage scan;
scanned_at 2026-10-21T16:03:45.533Z, wall 8.23s medium band,
scan_duration_ms=8220, raw 446B). Composition (24,0,2,19,3) vs c1858
(26,0,3,20,3): honest_free 3 -> 2, scam_pattern 20 -> 19 (FIRST-EVER
scam-class decrease in session memory — all prior drifts touched
honest_free only), total 26 -> 24. Two tasks disappeared during the
gap (one free, one scam; claimed-vs-delisted indistinguishable). NOT an
API fault: HTTP 200, valid JSON, arithmetic self-consistent
(0+2+19+3=24). honest_paid stayed 0 — no paid task appeared at any
point, including across the 11.5h outage.

Drift numbering caveat: #21 is next ordinal in the SESSION-TRACEABLE
sequence (#19 c1832, #20 c1858). The 109 rollback-lost cycles
(c1713..c1821) plus the outage gap (c1858..c1859) may conceal further
unrecorded drift events; true global ordinal may be higher.

Erosion watch (operator item k): honest_free path 5 -> 4 (#19, c1832)
-> 3 (#20, c1858) -> 2 (#21, c1859). Third erosion event; free-pool
draining — if trend continues to 0, flag as free-pool exhaustion signal
(potential precursor to paid-task appearance OR market decay;
indistinguishable a priori).

Prior era: DRIFT-#19 root c1833. Era streaks terminated at c1858:
MARKET_UNCHANGED 25 (era all-time record; record segment c1833..c1852
reached 20, extended to 25 through c1857), validator clean 25.

Assertions encode the DRIFT-#21 baseline (24,0,2,19,3) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=24 honest_paid=0 honest_free=2 scam=19 unknown=3
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 1859
RAW = "/home/z/my-project/scripts/scan_cycle1859_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1859.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 24, "honest_paid": 0, "honest_free": 2, "scam": 19, "unknown": 3}
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
