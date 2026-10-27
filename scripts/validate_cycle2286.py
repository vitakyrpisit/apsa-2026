#!/usr/bin/env python3
"""Validator for cycle 2286.

DUAL CHAIN ROOT: ROLLBACK-#11 + DRIFT-#27 (DRIFT-#26 baseline retired).

ROLLBACK-#11: detected 2026-10-24 00:03+08 at the c2159 trigger. The
filesystem state (worklog.md + scripts/) was restored to c1858
(mtime 2026-10-21 12:29:42+08). LOST: worklog entries c1859..c2158
(300 entries), validators validate_cycle1859..2158.py, raw/pretty
archives scan_cycle1859..2158, and tools qualify_scan.py (rebuilt
this cycle). SURVIVED: recursive_diff.py, archives up to c1858.
Cycle ordinals CONTINUE per precedent (rollback #9 did not reset the
counter); last session-traceable executed cycle = c2158 (2026-10-23
12:28+08, five-tuple (22,0,0,18,4), cumulative 2159 scans).

DRIFT-#27: detected at c2217 (scanned_at 2026-10-23T20:53:43.546Z,
client 2.116903s / scan_duration_ms=2109, raw 446B — size inside the
band as predicted; 4-digit duration). Composition (22,0,1,18,3) vs
DRIFT-#26 baseline (23,0,2,18,3). Field-level changes: total_tasks
23->22, honest_free 2->1 (one honest FREE task removed from the
marketplace). honest_paid STAYED 0 (best_paid_task=None,
all_honest_paid=[] — no paid task appeared or disappeared);
scam_pattern 18 and unknown 3 unchanged; taskbounty side unchanged.
Change detected LIVE in-session (no rollback gap) — exact cycle is
c2217 itself. #27 is the next ordinal in the SESSION-TRACEABLE
sequence (after #26).

Prior era: DRIFT-#26 root c2159. Era closed at c2216: MARKET_UNCHANGED
streak 57 (c2160..c2216), validator clean 58 (last: c2216), era
episodes 3 (EP1 14, EP2 1, EP3 2; EP4 never opened), era min 1.682s
(c2192) / high 13.827s (c2174) / longest sub-2.0 run 7 (PLATEAU-3,
c2208..c2214). Arm census at era close: 7 candidates, 1 open / 6
cancel. Era records ARCHIVED with DRIFT-#26; DRIFT-#27 latency
records start fresh at this root (first reading: c2217 2.117s).
Ledger-verifiable streaks RESTART at this root.

Assertions encode the DRIFT-#27 baseline (22,0,1,18,3) @ 446B:
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

CYCLE = 2286
RAW = "/home/z/my-project/scripts/scan_cycle2286_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2286.json"
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
