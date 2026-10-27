#!/usr/bin/env python3
"""Re-anchor validate_cycle2594.py to the DRIFT-#41 root baseline (23,0,2,18,3) @ 446B.

Second pass of the c2577/c2580/c2581/c2583/c2590/c2591 two-pass precedent: the match-path
rebadge was executed FIRST and FAILED on baseline_match with exactly ONE failure (all other
assertions passing) — that run is THE DRIFT-#41 DECLARATION EVIDENCE. This pass re-anchors
the same file to the new root baseline and restructures the chain (root cite + DRIFT-#40
closure).
Re-anchor P-HIST invariant — NOT the 3-REF case (the closed DRIFT-#40 root c2591 is three
cycles back; the immediate predecessor is c2593): the post-re-anchor "2593" count must be
exactly 2 (rebadged-from + chain re-attach) and the "2591" count exactly 2 (closure root
cite + chain history).
"""
import re
import sys

F = "/home/z/my-project/scripts/validate_cycle2594.py"
text = open(F).read()

def rep(old, new, expect=1):
    c = text.count(old)
    assert c == expect, f"patch pre-count != {expect}: {c} for {old[:60]!r}"
    return text.replace(old, new)

# 1) header line: declaration language
text = rep(
    "DRIFT-#40 verification-4 CARRY (root declared 2026-10-27 ~02:28 +08): rebadged from "
    "validate_cycle2593.py (the match-path rebadge was executed FIRST and FAILED on "
    "baseline_match — that run is the DRIFT-#40 declaration evidence — then re-anchored "
    "to the new root baseline)",
    "DRIFT-#41 ROOT DECLARED (2026-10-27 ~03:02 +08): rebadged from validate_cycle2593.py "
    "(the match-path rebadge was executed FIRST and FAILED on baseline_match — that run is "
    "the DRIFT-#41 declaration evidence — then re-anchored to the new root baseline)")

# 2) root line
text = rep(
    "(24,0,3,18,3) @ 446B DRIFT-#40 root; c2594 = DRIFT-#40 verification 4",
    "(23,0,2,18,3) @ 446B DRIFT-#41 root; c2594 = DRIFT-#41 verification 1")

# 3) chain-head: DRIFT-#41 root cite + DRIFT-#40 closure (root c2591 cite) + chain re-attach
text = rep(
    "(c2594 = DRIFT-#40 verification 4; c2593 = DRIFT-#40 verification 3; "
    "c2592 = DRIFT-#40 verification 2; c2591 = DRIFT-#40 verification 1, ROOT — "
    "the movement: total 25->24 (-1),",
    "(c2594 = DRIFT-#41 verification 1, ROOT — the movement: total 24->23 (-1), "
    "honest_free 3->2 (-1) HONEST INVENTORY CONTRACTION (a single honest-free departure "
    "accounts for BOTH deltas — the FOURTH of the post-DRIFT-#35 era: the 6-task c2577 "
    "emergence has contracted 6->5->4->3->2; honest_paid=0 = NO GOLD), "
    "unknown 3 + scam 18 unchanged, SIZE 446B streak intact (wire-size verification "
    "RESUMED — 446B on genuine captured bytes); DRIFT-#40 CLOSED at 3-fold "
    "(root c2591, verifications 1-3, 3-of-59 = 5.1% of the DRIFT-#30 record span; "
    "chain context-carried post-LOSS-#5: DRIFT-#39 closed 1-fold c2590, #38 8-fold "
    "c2583, #37 2-fold c2581, #36 1-fold c2580, #35 3-fold c2577, #34 14-fold c2563, "
    "#33 7-fold c2556, #32 3-fold c2553, #31 39-fold c2514, #30 record 59-fold c2454); "
    "c2593 = DRIFT-#40 verification 3; c2592 = DRIFT-#40 verification 2; "
    "c2591 = DRIFT-#40 verification 1, ROOT — the movement: total 25->24 (-1),")

# 4) assertions docstring block
text = rep(
    "Assertions encode the DRIFT-#40 baseline (24,0,3,18,3) @ 446B:",
    "Assertions encode the DRIFT-#41 baseline (23,0,2,18,3) @ 446B:")
text = rep(
    "  - BA composition: total=24 honest_paid=0 honest_free=3 scam=18 unknown=3",
    "  - BA composition: total=23 honest_paid=0 honest_free=2 scam=18 unknown=3")
text = rep(
    "  (unknown=3 = the DRIFT-#40 movement — a single unknown-category DEPARTURE;\n"
    "  honest_free 3 HOLDS — the DRIFT-#39 departure did NOT extend; aggregate-only visibility —",
    "  (honest_free=2 = the DRIFT-#41 movement — a single honest-free DEPARTURE,\n"
    "  the FOURTH of the post-DRIFT-#35 era (6->5->4->3->2); aggregate-only visibility —")
text = rep(
    "  the 3 honest free tasks are NOT taken per the PAID-only policy)",
    "  the 2 honest free tasks are NOT taken per the PAID-only policy)")

# 5) BASELINE_COMP constant
text = rep(
    'BASELINE_COMP = {"total": 24, "honest_paid": 0, "honest_free": 3, "scam": 18, "unknown": 3}',
    'BASELINE_COMP = {"total": 23, "honest_paid": 0, "honest_free": 2, "scam": 18, "unknown": 3}')

open(F, "w").write(text)

# P-HIST invariants — NOT the 3-REF case: "2593" == 2, "2591" == 2
sites_93 = [m.start() for m in re.finditer("2593", text)]
sites_91 = [m.start() for m in re.finditer("2591", text)]
print(f"P-HIST 2593 refs post-re-anchor = {len(sites_93)}")
for s in sites_93:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
print(f"P-HIST 2591 refs post-re-anchor = {len(sites_91)}")
for s in sites_91:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites_93) != 2 or len(sites_91) != 2:
    print("RE-ANCHOR P-HIST FAILED: expected 2593==2 and 2591==2")
    sys.exit(1)
print("RE-ANCHOR P-HIST CLEAN (2593: rebadged-from + chain re-attach; 2591: closure root cite + chain history)")
print(f"reanchored_ok={F}")
