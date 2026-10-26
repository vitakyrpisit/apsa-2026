#!/usr/bin/env python3
"""Re-anchor validate_cycle2590.py to the DRIFT-#39 root baseline (25,0,3,18,4) @ 446B.

Second pass of the c2577/c2580/c2581/c2583 two-pass precedent: the match-path rebadge was
executed FIRST and FAILED on baseline_match with exactly ONE failure (all other assertions
passing) — that run is THE DRIFT-#39 DECLARATION EVIDENCE. This pass re-anchors the same
file to the new root baseline and restructures the chain (root cite + DRIFT-#38 closure).
Re-anchor P-HIST invariant (c2583 precedent — the closed DRIFT-#38 root c2583 is seven-plus
cycles back): STANDARD 2 refs — the post-re-anchor "2589" count must remain exactly 2
(rebadged-from + chain re-attach). The closure-root cite is c2583 (a 2583 ref, not 2589).
"""
import re
import sys

F = "/home/z/my-project/scripts/validate_cycle2590.py"
text = open(F).read()

def rep(old, new, expect=1):
    c = text.count(old)
    assert c == expect, f"patch pre-count != {expect}: {c} for {old[:60]!r}"
    return text.replace(old, new)

# 1) header line: declaration language
text = rep(
    "DRIFT-#38 verification-8 CARRY (root declared 2026-10-27 ~01:06 +08): rebadged from "
    "validate_cycle2589.py (the match-path rebadge was executed FIRST and FAILED on "
    "baseline_match — that run is the DRIFT-#38 declaration evidence — then re-anchored "
    "to the new root baseline)",
    "DRIFT-#39 ROOT DECLARED (2026-10-27 ~02:22 +08): rebadged from validate_cycle2589.py "
    "(the match-path rebadge was executed FIRST and FAILED on baseline_match — that run is "
    "the DRIFT-#39 declaration evidence — then re-anchored to the new root baseline)")

# 2) root line
text = rep(
    "(26,0,4,18,4) @ 446B DRIFT-#38 root; c2590 = DRIFT-#38 verification 1",
    "(25,0,3,18,4) @ 446B DRIFT-#39 root; c2590 = DRIFT-#39 verification 1")

# 3) chain-head: DRIFT-#39 root cite + DRIFT-#38 closure + chain re-attach
text = rep(
    "(c2590 = DRIFT-#38 verification 8; c2589 = DRIFT-#38 verification 7; c2588",
    "(c2590 = DRIFT-#39 verification 1, ROOT — the movement: total 26->25 (-1), "
    "honest_free 4->3 (-1) HONEST INVENTORY CONTRACTION (a single honest-free DEPARTURE — "
    "the third of the post-DRIFT-#35 era: the 6-task c2577 emergence has contracted "
    "6->5->4->3; honest_paid=0 = NO GOLD), scam 18 + unknown 4 unchanged, SIZE 446B streak "
    "intact; DRIFT-#38 CLOSED at 8-fold (root c2583, verifications 1-8, 8-of-59 = 13.6% of "
    "the DRIFT-#30 record span; chain context-carried post-LOSS-#5: DRIFT-#37 closed at "
    "2-fold, DRIFT-#36 at 1-fold, DRIFT-#35 at 3-fold, DRIFT-#34 at 14-fold, DRIFT-#33 at "
    "7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); "
    "c2589 = DRIFT-#38 verification 7; c2588")

# 4) assertions docstring block
text = rep(
    "Assertions encode the DRIFT-#38 baseline (26,0,4,18,4) @ 446B:",
    "Assertions encode the DRIFT-#39 baseline (25,0,3,18,4) @ 446B:")
text = rep(
    "  - BA composition: total=26 honest_paid=0 honest_free=4 scam=18 unknown=4",
    "  - BA composition: total=25 honest_paid=0 honest_free=3 scam=18 unknown=4")
text = rep(
    "  (honest_free=4 = the DRIFT-#38 movement — a single honest-free DEPARTURE,\n"
    "  the second of the post-DRIFT-#35 era (6->5->4); aggregate-only visibility —",
    "  (honest_free=3 = the DRIFT-#39 movement — a single honest-free DEPARTURE,\n"
    "  the third of the post-DRIFT-#35 era (6->5->4->3); aggregate-only visibility —")
text = rep(
    "  the 4 honest free tasks are NOT taken per the PAID-only policy)",
    "  the 3 honest free tasks are NOT taken per the PAID-only policy)")

# 5) BASELINE_COMP constant
text = rep(
    'BASELINE_COMP = {"total": 26, "honest_paid": 0, "honest_free": 4, "scam": 18, "unknown": 4}',
    'BASELINE_COMP = {"total": 25, "honest_paid": 0, "honest_free": 3, "scam": 18, "unknown": 4}')

open(F, "w").write(text)

# P-HIST invariant: "2589" refs must remain exactly 2 (rebadged-from + chain re-attach)
sites = [m.start() for m in re.finditer("2589", text)]
print(f"P-HIST 2589 refs post-re-anchor = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("RE-ANCHOR P-HIST FAILED: expected exactly 2")
    sys.exit(1)
print("RE-ANCHOR P-HIST CLEAN (STANDARD 2 refs, c2583 precedent)")
print(f"reanchored_ok={F}")
