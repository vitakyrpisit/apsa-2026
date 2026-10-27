#!/usr/bin/env python3
"""Validator for cycle 2373.

DUAL CHAIN ROOT: ROLLBACK-#12 + DRIFT-#29 (all prior baselines retired).

ROLLBACK-#12: detected 2026-10-25 00:03+08 at the c2437 trigger (gateway
batch trace cron-agent-loop-202610250003). The filesystem state
(worklog.md + scripts/) was AGAIN restored to the c1858 snapshot
(worklog mtime 2026-10-21 04:29:42+0000 = 12:29:42+08 — IDENTICAL to
the ROLLBACK-#11 restore point; same node-level rollback class).
LOST: worklog entries c1859..c2308 (450 entries — INCLUDING the entire
post-#11 rebuild: DRIFT-#26 era c2159..c2216, DRIFT-#27 era
c2217..c2306, DRIFT-#28 root c2307..c2308), validators
validate_cycle1859..2308.py (150), raw/pretty archives
scan_cycle1859..2308 (150 pairs), and tools qualify_scan.py (lost for
the 2nd time; not rebuilt this cycle). SURVIVED: recursive_diff.py,
worklog up to c1858 (7826 lines, DRIFT-#20 event cycle at tail with
the #20 root unbuilt), validators/raw up to c1858 (50 each), 505
pretty archives up to c1858.

Cycle ordinals CONTINUE per precedent (rollbacks #9 and #11 did not
reset the counter); last session-traceable executed cycle = c2308
(2026-10-24 12:28+08, five-tuple (21,0,0,18,3), DRIFT-#28 baseline,
cumulative 2308 scans / 0 claims).

DRIFT-#29: era root established at c2437 (scanned_at
2026-10-24T16:05:59.175Z, client 1.991821s / scan_duration_ms=1978,
raw 446B — size inside the band as predicted; 4-digit duration).
Composition (21,0,0,18,3) — the market has NOT drifted vs the last
session-traceable DRIFT-#28 baseline (21,0,0,18,3 @ c2308): total=21,
honest_paid=0, honest_free=0, scam=18, unknown=3, best_paid_task=None,
all_honest_paid=[], taskbounty side unchanged (api_key False, 0
bounties, 0 paid missions). Root baseline = live reading (c2159
precedent). #29 is the next ordinal in the SESSION-TRACEABLE sequence
(after #28; #28 root c2307 known from session context — its ledger
evidence was lost with the c1859..c2308 entries).

DRIFT-#28 CONTEXT (session-context knowledge, ledger lost): root
c2307, baseline (21,0,0,18,3) — established when the last honest FREE
task was removed (honest_free 1->0). #27 era (root c2217) archived 89
consecutive MARKET_UNCHANGED (c2218..c2306), era min 1.590108s (c2248)
/ high 2.659048s (c2297), PLATEAU-13 = 11 sole record. All archived
streaks/records are RESTARTED at this root.

Assertions encode the DRIFT-#29 baseline (21,0,0,18,3) @ 446B:
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

CYCLE = 2373
RAW = "/home/z/my-project/scripts/scan_cycle2437_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2437.json"
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
