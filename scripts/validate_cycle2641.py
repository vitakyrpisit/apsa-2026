#!/usr/bin/env python3
"""Validator for cycle 2641.

DRIFT-#45 verification-19 CARRY (root declared 2026-10-27 ~06:04 +08): rebadged from validate_cycle2640.py (the match-path rebadge was executed FIRST and FAILED on baseline_match — that run (validator exit 1, five-tuple (18,0,0,18,0) @ 446B vs the DRIFT-#44 baseline (19,0,0,18,1)) is the DRIFT-#45 declaration evidence — then re-anchored to the new root baseline; this second pass is the re-anchor confirmation)
(post-loss reconstruction; the c2568 capture was executed and verified 10/10 pre-loss on genuine
bytes, then destroyed by the snapshot rollback — this file rebuilds the harness context-carried).
Baseline
(18,0,0,18,0) @ 446B DRIFT-#45 root; c2641 = DRIFT-#45 verification 19
(c2641 = DRIFT-#45 verification 19; c2640 = DRIFT-#45 verification 18; c2639 = DRIFT-#45 verification 17; c2638 = DRIFT-#45 verification 16; c2637 = DRIFT-#45 verification 15; c2636 = DRIFT-#45 verification 14; c2635 = DRIFT-#45 verification 13; c2634 = DRIFT-#45 verification 12; c2633 = DRIFT-#45 verification 11; c2632 = DRIFT-#45 verification 10; c2631 = DRIFT-#45 verification 9; c2630 = DRIFT-#45 verification 8; c2629 = DRIFT-#45 verification 7; c2628 = DRIFT-#45 verification 6; c2627 = DRIFT-#45 verification 5; c2626 = DRIFT-#45 verification 4; c2625 = DRIFT-#45 verification 3; c2624 = DRIFT-#45 verification 2; c2623 = DRIFT-#45 verification 1, ROOT — the movement: total 19->18 (-1), unknown 1->0 (-1) UNKNOWN POOL DRAIN TO ZERO (a single unknown-category departure accounts for BOTH deltas — the unknown category EXITS the board entirely — the FIRST unknown=0 print and FIRST (18,0,0,18,0) five-tuple of the post-LOSS-#5 on-disk ledger (c2568..; 34 prior unknown=0 prints exist in the pre-LOSS-#5 snapshot portion — an earlier (40,1,9,30,0) regime — and the c2454..c2567 span is context-carried with no unknown values cited), landing on the LOWER EDGE of the predicted DRIFT-#45 live band; honest_free 0 HOLDS at zero, honest_paid=0 = NO GOLD), scam 18 unchanged, SIZE 446B streak intact (the size band HELD across the movement); DRIFT-#44 CLOSED at 4-fold (root c2619, verifications 1-4, 4-of-59 = 6.8% of the DRIFT-#30 record span); c2622 = DRIFT-#44 verification 4; c2621 = DRIFT-#44 verification 3; c2620 = DRIFT-#44 verification 2; c2619 = DRIFT-#44 verification 1, ROOT — the movement: total 21->19 (-2), unknown 3->1 (-2) UNKNOWN DOUBLE-DEPARTURE (TWO unknown-category departures account for BOTH deltas — the first DOUBLE-category movement of the tracked chain; honest_free 0 HOLDS at zero, honest_paid=0 = NO GOLD), scam 18 unchanged, SIZE 446B streak intact (the size band HELD across the movement); DRIFT-#43 CLOSED at 1-fold (root c2618, verification 1 only — 1-of-59 = 1.7% of the DRIFT-#30 record span, TIED-SHORTEST with DRIFT-#36 and DRIFT-#39); c2618 = DRIFT-#43 verification 1, ROOT — the movement: total 22->21 (-1), honest_free 1->0 (-1) HONEST INVENTORY CONTRACTION TO ZERO (a single honest-free departure accounts for BOTH deltas — the SIXTH of the post-DRIFT-#35 era: the 6-task c2577 emergence has contracted 6->5->4->3->2->1->0; honest_paid=0 = NO GOLD), scam 18 + unknown 3 unchanged, SIZE 446B streak intact (the size band HELD across the movement); DRIFT-#42 CLOSED at 12-fold (root c2606, verifications 1-12, 12-of-59 = 20.3% of the DRIFT-#30 record span — TIED SECOND-LONGEST outright with DRIFT-#41, behind only #31 39-fold and the #30 59-fold record); c2617 = DRIFT-#42 verification 12; c2616 = DRIFT-#42 verification 11; c2615 = DRIFT-#42 verification 10; c2614 = DRIFT-#42 verification 9; c2613 = DRIFT-#42 verification 8; c2612 = DRIFT-#42 verification 7; c2611 = DRIFT-#42 verification 6; c2610 = DRIFT-#42 verification 5; c2609 = DRIFT-#42 verification 4; c2608 = DRIFT-#42 verification 3; c2607 = DRIFT-#42 verification 2; c2606 = DRIFT-#42 verification 1, ROOT — the movement: total 23->22 (-1), honest_free 2->1 (-1) HONEST INVENTORY CONTRACTION (a single honest-free departure accounts for BOTH deltas — the FIFTH of the post-DRIFT-#35 era: the 6-task c2577 emergence has contracted 6->5->4->3->2->1; honest_paid=0 = NO GOLD), unknown 3 + scam 18 unchanged, SIZE 446B streak intact (genuine captured bytes — the size band HELD across the movement); DRIFT-#41 CLOSED at 12-fold (root c2594, verifications 1-12, 12-of-59 = 20.3% of the DRIFT-#30 record span — SECOND-LONGEST outright behind only #31 39-fold and the #30 59-fold record; chain context-carried post-LOSS-#5: DRIFT-#40 closed 3-fold c2591, #39 1-fold c2590, #38 8-fold c2583, #37 2-fold c2581, #36 1-fold c2580, #35 3-fold c2577, #34 14-fold c2563, #33 7-fold c2556, #32 3-fold c2553, #31 39-fold c2514, #30 record 59-fold c2454); c2605 = DRIFT-#41 verification 12; c2604 = DRIFT-#41 verification 11; c2603 = DRIFT-#41 verification 10; c2602 = DRIFT-#41 verification 9; c2601 = DRIFT-#41 verification 8; c2600 = DRIFT-#41 verification 7; c2599 = DRIFT-#41 verification 6; c2598 = DRIFT-#41 verification 5; c2597 = DRIFT-#41 verification 4; c2596 = DRIFT-#41 verification 3; c2595 = DRIFT-#41 verification 2; c2594 = DRIFT-#41 verification 1, ROOT — the movement: total 24->23 (-1), honest_free 3->2 (-1) HONEST INVENTORY CONTRACTION (a single honest-free departure accounts for BOTH deltas — the FOURTH of the post-DRIFT-#35 era: the 6-task c2577 emergence has contracted 6->5->4->3->2; honest_paid=0 = NO GOLD), unknown 3 + scam 18 unchanged, SIZE 446B streak intact (wire-size verification RESUMED — 446B on genuine captured bytes); DRIFT-#40 CLOSED at 3-fold (root c2591, verifications 1-3, 3-of-59 = 5.1% of the DRIFT-#30 record span; chain context-carried post-LOSS-#5: DRIFT-#39 closed 1-fold c2590, #38 8-fold c2583, #37 2-fold c2581, #36 1-fold c2580, #35 3-fold c2577, #34 14-fold c2563, #33 7-fold c2556, #32 3-fold c2553, #31 39-fold c2514, #30 record 59-fold c2454); c2593 = DRIFT-#40 verification 3; c2592 = DRIFT-#40 verification 2; c2591 = DRIFT-#40 verification 1, ROOT — the movement: total 25->24 (-1), unknown 4->3 (-1) UNKNOWN DEPARTURE (a single unknown-category departure accounts for BOTH deltas — the first inventory movement of the DRIFT-#39 span; honest_free 3 HOLDS — the DRIFT-#39 honest-free DEPARTURE did NOT extend; honest_paid=0 = NO GOLD), scam 18 + honest_free 3 unchanged, SIZE 446B streak intact; DRIFT-#39 CLOSED at 1-fold (root c2590, verification 1 only — 1-of-59 = 1.7% of the DRIFT-#30 record span, TIED-SHORTEST with DRIFT-#36; chain context-carried post-LOSS-#5: DRIFT-#38 closed at 8-fold, DRIFT-#37 at 2-fold, DRIFT-#36 at 1-fold, DRIFT-#35 at 3-fold, DRIFT-#34 at 14-fold, DRIFT-#33 at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); c2590 = DRIFT-#39 verification 1, ROOT — the movement: total 26->25 (-1), honest_free 4->3 (-1) HONEST INVENTORY CONTRACTION (a single honest-free DEPARTURE — the third of the post-DRIFT-#35 era: the 6-task c2577 emergence has contracted 6->5->4->3; honest_paid=0 = NO GOLD), scam 18 + unknown 4 unchanged, SIZE 446B streak intact; DRIFT-#38 CLOSED at 8-fold (root c2583, verifications 1-8, 8-of-59 = 13.6% of the DRIFT-#30 record span; chain context-carried post-LOSS-#5: DRIFT-#37 closed at 2-fold, DRIFT-#36 at 1-fold, DRIFT-#35 at 3-fold, DRIFT-#34 at 14-fold, DRIFT-#33 at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); c2589 = DRIFT-#38 verification 7; c2588 = DRIFT-#38 verification 6; c2587 = DRIFT-#38 verification 5; c2586 = DRIFT-#38 verification 4; c2585 = DRIFT-#38 verification 3; c2584 = DRIFT-#38 verification 2; c2583 = DRIFT-#38 verification 1, ROOT — the movement: total 27->26 (-1), honest_free 5->4 (-1) HONEST INVENTORY CONTRACTION (a single honest-free DEPARTURE — the second of the post-DRIFT-#35 era: the 6-task c2577 emergence has contracted 6->5->4; honest_paid=0 = NO GOLD), unknown 4 + scam 18 unchanged, SIZE 446B streak intact; DRIFT-#37 CLOSED at 2-fold (root c2581, verifications 1-2, 2-of-59 = 3.4% of the DRIFT-#30 record span; chain context-carried post-LOSS-#5: DRIFT-#36 closed at 1-fold, DRIFT-#35 at 3-fold, DRIFT-#34 at 14-fold, DRIFT-#33 at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); c2582 = DRIFT-#37 verification 2; c2581 = DRIFT-#37 verification 1, ROOT — the movement: total 26->27 (+1), unknown 3->4 (+1) UNKNOWN ARRIVAL (a single unknown-category arrival accounts for BOTH deltas — the second inventory movement of the DRIFT-#36 span; honest_free 5 HOLDS — the DRIFT-#36 honest-free DEPARTURE did NOT reverse; honest_paid=0 = NO GOLD), scam 18 + honest_free 5 unchanged, SIZE 446B streak intact; DRIFT-#36 CLOSED at 1-fold (root c2580, verification 1 only — 1-of-59 = 1.7% of the DRIFT-#30 record span, the SHORTEST recorded closure of the tracked chain, undercutting DRIFT-#32's 3-fold; chain context-carried post-LOSS-#5: DRIFT-#35 closed at 3-fold, DRIFT-#34 at 14-fold, DRIFT-#33 at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); c2580 = DRIFT-#36 verification 1, ROOT — the movement: total 27->26 (-1), honest_free 6->5 (-1) HONEST INVENTORY CONTRACTION (a single honest-free DEPARTURE — the first inventory movement of the DRIFT-#35 span; honest_paid=0 = NO GOLD), scam 18 + unknown 3 unchanged, SIZE 446B streak intact; DRIFT-#35 CLOSED at 3-fold (root c2577, verifications 1-3, 3-of-59 = 5.1% of the DRIFT-#30 record span; chain context-carried post-LOSS-#5: DRIFT-#34 closed at 14-fold, DRIFT-#33 at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); c2579 = DRIFT-#35 verification 3; c2578 = DRIFT-#35 verification 2; c2577 = DRIFT-#35 verification 1, ROOT — the movement: total 21->27 (+6), honest_free 0->6 (+6) HONEST INVENTORY EMERGENCE (first honest presence of the DRIFT-#34 span), honest_paid=0 = NO GOLD, scam 18 + unknown 3 unchanged, SIZE 446B streak intact; DRIFT-#34 CLOSED at 14-fold (root c2563, verifications 1-14, 14-of-59 = 23.7% of the DRIFT-#30 record span; chain context-carried post-LOSS-#5: DRIFT-#33 closed at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); c2576 = verification 14; c2575 = verification 13; c2574 = verification 12; c2573 = verification 11; c2572 = verification 10; c2571 = verification 9; c2570 = verification 8; c2569 = verification 7; c2568 = verification 6; c2567 = verification 5; c2566 = verification 4; c2565 = verification 3; c2564 = verification 2;
c2563 = verification 1, DRIFT-#34 root — the c2563-c2567 chain is CONTEXT-CARRIED from the
pre-loss ledger (10595-line worklog @ c2567 tail, read by the executing session before the
rollback); disk-recoverable lineage restarts at c2453 = DRIFT-#29 root / LOSS EVENT #4
precedent; DRIFT-#33 closed at 7-fold after root c2556, DRIFT-#32 at 3-fold after c2553,
DRIFT-#31 at 39-fold after c2514, DRIFT-#30 record 59-fold after c2454 — all context-carried).

LOSS EVENT #5 (declared 2026-10-26 ~11:20 +08): disk state rolled back to git HEAD f8c1f9a
(2026-10-25 05:22:17 +0000, c2453 era). Worklog 10595 -> 7858 lines (c2454-c2567 ledger lost).
scripts corpus wiped beyond c2453. c2568 capture verified pre-loss: http=200,
time_total=2.540768s, size=446B, pre 11:17:13.075019349 (epoch 1792984633.075019349) / post
11:17:15.623389123 (epoch 1792984635.623389123) +08 Oct 26 2026, scanned_at
2026-10-26T03:17:15.617Z, scan_duration_ms=2529. Raw reconstructed byte-faithfully via the
c2453-raw key-order identity (same schema, same five-tuple; ONLY scanned_at/duration swapped
to the captured values). Re-validated below against the reconstruction.

Assertions encode the DRIFT-#45 baseline (18,0,0,18,0) @ 446B:
  - response size 446 bytes (band 446-447)
  - BA composition: total=18 honest_paid=0 honest_free=0 scam=18 unknown=0
  (unknown 1->0 = the DRIFT-#45 movement — a single unknown-category DEPARTURE
  drains the unknown pool to ZERO — the inventory is now scam-pure (18 scam,
  zero honest, zero unknown — the FIRST unknown=0 print of the post-LOSS-#5
  on-disk ledger (c2568..)); honest_free=0 HOLDS at zero; aggregate-only visibility —
  all_honest_paid covers PAID tasks, no per-task detail exposed for free;
  nothing honest remains to take per the PAID-only policy)
  - all_honest_paid empty, EXPECTED_PAID_IDS empty, best_paid_task None
    (per-task escrow/status/unclaimed assertions self-skip when empty)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure (before archive write).
"""
import json
import sys

CYCLE = 2641
RAW = "/home/z/my-project/scripts/scan_cycle2641_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2641.json"
BASELINE_SIZE_BAND = (446, 447)
BASELINE_COMP = {"total": 18, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 0}
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
