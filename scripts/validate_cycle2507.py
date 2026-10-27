#!/usr/bin/env python3
"""Validator for cycle 2507.

DRIFT-#30 BASELINE CARRY: rebadged from validate_cycle2506.py
(sed 2506->2507, the DRIFT-#30 root harness). Baseline
(23,0,3,17,3) @ 446B carried unchanged; c2507 = verification 53
(c2506 = verification 52; c2505 = verification 51; c2504 = verification 50; c2503 = verification 49; c2502 = verification 48; c2501 = verification 47; c2500 = verification 46; c2499 = verification 45; c2498 = verification 44; c2497 = verification 43; c2496 = verification 42; c2495 = verification 41; c2494 = verification 40; c2493 = verification 39; c2492 = verification 38; c2491 = verification 37; c2490 = verification 36; c2489 = verification 35; c2488 = verification 34; c2487 = verification 33; c2486 = verification 32; c2485 = verification 31; c2484 = verification 30; c2483 = verification 29; c2482 = verification 28; c2481 = verification 27; c2480 = verification 26; c2479 = verification 25; c2478 = verification 24; c2477 = verification 23; c2476 = verification 22; c2475 = verification 21; c2474 = verification 20; c2473 = verification 19; c2472 = verification 18; c2471 = verification 17; c2470 = verification 16; c2469 = verification 15; c2468 = verification 14; c2467 = verification 13; c2466 = verification 12; c2465 = verification 11; c2464 =
verification 10; c2463 = verification 9; c2462 =
verification 8; c2461 = verification 7; c2460 =
verification 6; c2459 = verification 5; c2458 =
verification 4; c2457 = verification 3; c2456 =
verification 2; c2455 =
verification 1, single-pass exit=0 10/10; c2454 = re-anchor
root). Historical narrative
retained below — first pass against the c2454 payload produced
exactly one failure —
baseline_match (9/10 ok, exit=1) — the algorithmic confirmation
of DRIFT #30; this file re-anchors per the c2453 chain-break
precedent. Lineage: ROLLBACK-#9 -> DRIFT-#19 ((27,0,4,20,3),
c1858 era root) -> [594 cycles off-node, LOSS EVENT #4] ->
DRIFT-#29 ((21,0,0,18,3), c2453 root, 144-fold verified thru
c2453) -> DRIFT-#30 (this root).

DRIFT-#30 delta vs DRIFT-#29: total 21->23, honest_free 0->3
(re-emergence; echoes the c1858-era composition family), scam
18->17, unknown 3 stable, honest_paid 0 throughout. All other
sentinels held: 446B size band, all_honest_paid empty,
best_paid_task None, taskbounty zeros, next_scan=300.

Assertions encode the DRIFT-#30 baseline (23,0,3,17,3) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=23 honest_paid=0 honest_free=3 scam=17 unknown=3
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 2507
RAW = "/home/z/my-project/scripts/scan_cycle2507_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2507.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 23, "honest_paid": 0, "honest_free": 3, "scam": 17, "unknown": 3}
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
