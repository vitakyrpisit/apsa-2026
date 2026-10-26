#!/usr/bin/env python3
"""Re-anchor validate_cycle2606.py to the DRIFT-#42 root baseline (22,0,1,18,3) @ 446B.

Second pass of the c2577/c2580/c2581/c2583/c2590/c2591/c2594 two-pass precedent: the
match-path rebadge was executed FIRST and FAILED on baseline_match with exactly ONE
failure (all other assertions passing) — that run is THE DRIFT-#42 DECLARATION EVIDENCE.
This pass re-anchors the same file to the new root baseline and restructures the chain
(root cite + DRIFT-#41 closure at 12-fold).
Re-anchor P-HIST invariant — NOT the 3-REF case (the closed DRIFT-#41 root c2594 is
twelve cycles back; the immediate predecessor is c2605): the post-re-anchor "2605" count
must be exactly 2 (rebadged-from + chain re-attach) and the "2594" count exactly 2
(closure root cite + chain history).
"""
import re
import sys

F = "/home/z/my-project/scripts/validate_cycle2606.py"
text = open(F).read()

def rep(old, new, expect=1):
    c = text.count(old)
    assert c == expect, f"patch pre-count != {expect}: {c} for {old[:60]!r}"
    return text.replace(old, new)

# 1) header line: declaration language
text = rep(
    "DRIFT-#41 verification-13 CARRY (root declared 2026-10-27 ~03:02 +08): rebadged from "
    "validate_cycle2605.py (the match-path rebadge was executed FIRST and FAILED on "
    "baseline_match — that run is the DRIFT-#41 declaration evidence — then re-anchored "
    "to the new root baseline)",
    "DRIFT-#42 ROOT DECLARED (2026-10-27 ~04:07 +08): rebadged from validate_cycle2605.py "
    "(the match-path rebadge was executed FIRST and FAILED on baseline_match — that run is "
    "the DRIFT-#42 declaration evidence — then re-anchored to the new root baseline)")

# 2) root line
text = rep(
    "(23,0,2,18,3) @ 446B DRIFT-#41 root; c2606 = DRIFT-#41 verification 13",
    "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2606 = DRIFT-#42 verification 1")

# 3) chain-head: DRIFT-#42 root cite + DRIFT-#41 closure (root c2594 cite) + chain re-attach
text = rep(
    "(c2606 = DRIFT-#41 verification 13; c2605 = DRIFT-#41 verification 12; "
    "c2604 = DRIFT-#41 verification 11; c2603 = DRIFT-#41 verification 10; "
    "c2602 = DRIFT-#41 verification 9; c2601 = DRIFT-#41 verification 8; "
    "c2600 = DRIFT-#41 verification 7; c2599 = DRIFT-#41 verification 6; "
    "c2598 = DRIFT-#41 verification 5; c2597 = DRIFT-#41 verification 4; "
    "c2596 = DRIFT-#41 verification 3; c2595 = DRIFT-#41 verification 2; "
    "c2594 = DRIFT-#41 verification 1, ROOT — the movement: total 24->23 (-1),",
    "(c2606 = DRIFT-#42 verification 1, ROOT — the movement: total 23->22 (-1), "
    "honest_free 2->1 (-1) HONEST INVENTORY CONTRACTION (a single honest-free departure "
    "accounts for BOTH deltas — the FIFTH of the post-DRIFT-#35 era: the 6-task c2577 "
    "emergence has contracted 6->5->4->3->2->1; honest_paid=0 = NO GOLD), "
    "unknown 3 + scam 18 unchanged, SIZE 446B streak intact (genuine captured bytes — "
    "the size band HELD across the movement); DRIFT-#41 CLOSED at 12-fold "
    "(root c2594, verifications 1-12, 12-of-59 = 20.3% of the DRIFT-#30 record span — "
    "SECOND-LONGEST outright behind only #31 39-fold and the #30 59-fold record; "
    "chain context-carried post-LOSS-#5: DRIFT-#40 closed 3-fold c2591, #39 1-fold "
    "c2590, #38 8-fold c2583, #37 2-fold c2581, #36 1-fold c2580, #35 3-fold c2577, "
    "#34 14-fold c2563, #33 7-fold c2556, #32 3-fold c2553, #31 39-fold c2514, "
    "#30 record 59-fold c2454); "
    "c2605 = DRIFT-#41 verification 12; c2604 = DRIFT-#41 verification 11; "
    "c2603 = DRIFT-#41 verification 10; c2602 = DRIFT-#41 verification 9; "
    "c2601 = DRIFT-#41 verification 8; c2600 = DRIFT-#41 verification 7; "
    "c2599 = DRIFT-#41 verification 6; c2598 = DRIFT-#41 verification 5; "
    "c2597 = DRIFT-#41 verification 4; c2596 = DRIFT-#41 verification 3; "
    "c2595 = DRIFT-#41 verification 2; "
    "c2594 = DRIFT-#41 verification 1, ROOT — the movement: total 24->23 (-1),")

# 4) assertions docstring block
text = rep(
    "Assertions encode the DRIFT-#41 baseline (23,0,2,18,3) @ 446B:",
    "Assertions encode the DRIFT-#42 baseline (22,0,1,18,3) @ 446B:")
text = rep(
    "  - BA composition: total=23 honest_paid=0 honest_free=2 scam=18 unknown=3",
    "  - BA composition: total=22 honest_paid=0 honest_free=1 scam=18 unknown=3")
text = rep(
    "  (honest_free=2 = the DRIFT-#41 movement — a single honest-free DEPARTURE,\n"
    "  the FOURTH of the post-DRIFT-#35 era (6->5->4->3->2); aggregate-only visibility —",
    "  (honest_free=1 = the DRIFT-#42 movement — a single honest-free DEPARTURE,\n"
    "  the FIFTH of the post-DRIFT-#35 era (6->5->4->3->2->1); aggregate-only visibility —")
text = rep(
    "  the 2 honest free tasks are NOT taken per the PAID-only policy)",
    "  the 1 honest free task is NOT taken per the PAID-only policy)")

# 5) BASELINE_COMP constant
text = rep(
    'BASELINE_COMP = {"total": 23, "honest_paid": 0, "honest_free": 2, "scam": 18, "unknown": 3}',
    'BASELINE_COMP = {"total": 22, "honest_paid": 0, "honest_free": 1, "scam": 18, "unknown": 3}')

open(F, "w").write(text)

# P-HIST invariants — NOT the 3-REF case: "2605" == 2, "2594" == 2
sites_05 = [m.start() for m in re.finditer("2605", text)]
sites_94 = [m.start() for m in re.finditer("2594", text)]
print(f"P-HIST 2605 refs post-re-anchor = {len(sites_05)}")
for s in sites_05:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
print(f"P-HIST 2594 refs post-re-anchor = {len(sites_94)}")
for s in sites_94:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites_05) != 2 or len(sites_94) != 2:
    print("RE-ANCHOR P-HIST FAILED: expected 2605==2 and 2594==2")
    sys.exit(1)
print("RE-ANCHOR P-HIST CLEAN (2605: rebadged-from + chain re-attach; 2594: closure root cite + chain history)")
print(f"reanchored_ok={F}")
