#!/usr/bin/env python3
"""Re-anchor validate_cycle2591.py to the DRIFT-#40 root baseline (24,0,3,18,3) @ 446B.

Second pass of the c2577/c2580/c2581/c2583/c2590 two-pass precedent: the match-path rebadge
was executed FIRST and FAILED on baseline_match with exactly ONE failure (all other
assertions passing) — that run is THE DRIFT-#40 DECLARATION EVIDENCE. This pass re-anchors
the same file to the new root baseline and restructures the chain (root cite + DRIFT-#39
closure).
Re-anchor P-HIST invariant — the 3-REF case (c2581 precedent: the closed DRIFT-#39 root
c2590 IS the immediate predecessor): the post-re-anchor "2590" count must be exactly 3
(rebadged-from + closure root cite + chain re-attach).
"""
import re
import sys

F = "/home/z/my-project/scripts/validate_cycle2591.py"
text = open(F).read()

def rep(old, new, expect=1):
    c = text.count(old)
    assert c == expect, f"patch pre-count != {expect}: {c} for {old[:60]!r}"
    return text.replace(old, new)

# 1) header line: declaration language
text = rep(
    "DRIFT-#39 verification-2 CARRY (root declared 2026-10-27 ~02:22 +08): rebadged from "
    "validate_cycle2590.py (the match-path rebadge was executed FIRST and FAILED on "
    "baseline_match — that run is the DRIFT-#39 declaration evidence — then re-anchored "
    "to the new root baseline)",
    "DRIFT-#40 ROOT DECLARED (2026-10-27 ~02:28 +08): rebadged from validate_cycle2590.py "
    "(the match-path rebadge was executed FIRST and FAILED on baseline_match — that run is "
    "the DRIFT-#40 declaration evidence — then re-anchored to the new root baseline)")

# 2) root line
text = rep(
    "(25,0,3,18,4) @ 446B DRIFT-#39 root; c2591 = DRIFT-#39 verification 1",
    "(24,0,3,18,3) @ 446B DRIFT-#40 root; c2591 = DRIFT-#40 verification 1")

# 3) chain-head: DRIFT-#40 root cite + DRIFT-#39 closure (root c2590 cite) + chain re-attach
text = rep(
    "(c2591 = DRIFT-#39 verification 2; c2590 = DRIFT-#39 verification 1, ROOT — the movement: total 26->25 (-1),",
    "(c2591 = DRIFT-#40 verification 1, ROOT — the movement: total 25->24 (-1), "
    "unknown 4->3 (-1) UNKNOWN DEPARTURE (a single unknown-category departure accounts for "
    "BOTH deltas — the first inventory movement of the DRIFT-#39 span; honest_free 3 HOLDS "
    "— the DRIFT-#39 honest-free DEPARTURE did NOT extend; honest_paid=0 = NO GOLD), "
    "scam 18 + honest_free 3 unchanged, SIZE 446B streak intact; DRIFT-#39 CLOSED at 1-fold "
    "(root c2590, verification 1 only — 1-of-59 = 1.7% of the DRIFT-#30 record span, "
    "TIED-SHORTEST with DRIFT-#36; chain context-carried post-LOSS-#5: DRIFT-#38 closed at "
    "8-fold, DRIFT-#37 at 2-fold, DRIFT-#36 at 1-fold, DRIFT-#35 at 3-fold, DRIFT-#34 at "
    "14-fold, DRIFT-#33 at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 "
    "record 59-fold); c2590 = DRIFT-#39 verification 1, ROOT — the movement: total 26->25 (-1),")

# 4) assertions docstring block
text = rep(
    "Assertions encode the DRIFT-#39 baseline (25,0,3,18,4) @ 446B:",
    "Assertions encode the DRIFT-#40 baseline (24,0,3,18,3) @ 446B:")
text = rep(
    "  - BA composition: total=25 honest_paid=0 honest_free=3 scam=18 unknown=4",
    "  - BA composition: total=24 honest_paid=0 honest_free=3 scam=18 unknown=3")
text = rep(
    "  (honest_free=3 = the DRIFT-#39 movement — a single honest-free DEPARTURE,\n"
    "  the third of the post-DRIFT-#35 era (6->5->4->3); aggregate-only visibility —",
    "  (unknown=3 = the DRIFT-#40 movement — a single unknown-category DEPARTURE;\n"
    "  honest_free 3 HOLDS — the DRIFT-#39 departure did NOT extend; aggregate-only visibility —")

# 5) BASELINE_COMP constant
text = rep(
    'BASELINE_COMP = {"total": 25, "honest_paid": 0, "honest_free": 3, "scam": 18, "unknown": 4}',
    'BASELINE_COMP = {"total": 24, "honest_paid": 0, "honest_free": 3, "scam": 18, "unknown": 3}')

open(F, "w").write(text)

# P-HIST invariant — 3-REF case (c2581 precedent): "2590" refs must be exactly 3
sites = [m.start() for m in re.finditer("2590", text)]
print(f"P-HIST 2590 refs post-re-anchor = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 3:
    print("RE-ANCHOR P-HIST FAILED: expected exactly 3 (c2581 precedent)")
    sys.exit(1)
print("RE-ANCHOR P-HIST CLEAN (3 refs: rebadged-from + closure root cite + chain re-attach)")
print(f"reanchored_ok={F}")
