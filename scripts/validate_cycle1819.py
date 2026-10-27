#!/usr/bin/env python3
"""Validator for cycle 1819.

DRIFT-#18 REBASE POINT (new era root; prior drift-#17 validator chain
validate_cycle1798..1817.py encoded the (29,1,5,20,3) @ 16408B baseline
and is retired by this drift event).

Drift event #18: detected at c1817 (scanned_at 2026-10-21T00:42:46.176Z
= 2026-10-21 08:42:46 +08, scan_duration_ms=1564 fast band, HTTP 200,
raw 446B vs drift-#17 band (16408,16409) — massive structural change).
Changes vs drift-#17 baseline (29,1,5,20,3):
  - honest_paid 1->0 (SLOT VANISHED): sole WURK pilot slot
    task_qKxsDuYZks86pyzXcpgpU (steady 101 cycles unchanged, c1715..
    c1816, bounty 0.10 USDC escrow=funded open unclaimed) disappeared
    from the market — all_honest_paid now [], best_paid_task=null
  - total_tasks 29->28 (-1, exactly the vanished paid slot)
  - honest_free 5, scam 20, unknown 3 all unchanged
  - raw payload 16408B -> 446B (-97.3%): the paid-task detail object
    (full task fields incl. escrow/status/claimed_by/bounty) is gone
    from the response; remaining payload is aggregate counters only
  - taskbounty unchanged: api_key=False paid_missions=0; clawlancer
    absent; auto_claim_pending=False; next_scan=300

recursive_diff c1816 vs c1817 (correct arg order <new> <old>):
MARKET_CHANGED (stripped canonical 16693 -> 419, -97.5% — structural
signature of a removed task detail object, not counter substitution).

drift-#17 era MARKET_UNCHANGED streak: ENDED at 18 (c1797..c1816).
drift-#18 era streak restarts at 0 from c1817.

Operator impact: item (o) WURK pilot decision is now MOOT in its prior
form — the slot it referenced no longer exists. Scan branch falls to
step 4 (no paid task found). EV of remaining market: no paid task =>
no EV to compute; zero-claim posture trivially holds.

Assertions encode the drift-#18 baseline (28,0,5,20,3) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=28 honest_paid=0 honest_free=5 scam=20 unknown=3
  - 0 honest paid tasks, all_honest_paid=[], best_paid_task=null
  - (escrow/status/unclaimed assertions self-skip when paid list empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1819
RAW = "/home/z/my-project/scripts/scan_cycle1819_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1819.json"
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
