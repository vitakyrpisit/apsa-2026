#!/usr/bin/env python3
"""Reanchor validate_cycle2618.py to the DRIFT-#43 ROOT (second pass of the two-pass protocol).

DRIFT-#43 DECLARATION EVIDENCE (first pass, booked): the match-path rebadge run of
validate_cycle2618.py FAILED on baseline_match (validator exit 1) — captured five-tuple
(21,0,0,18,3) @ 446B vs the DRIFT-#42 baseline (22,0,1,18,3): total 22->21 (-1),
honest_free 1->0 (-1) HONEST INVENTORY CONTRACTION TO ZERO (the SIXTH of the post-
DRIFT-#35 era: 6->5->4->3->2->1->0); scam 18 + unknown 3 unchanged; recursive diff
confirmed exactly 2 field-level moves (basedagents.honest_free 1->0,
basedagents.total_tasks 22->21); honest_paid=0 — NO GOLD. DRIFT-#42 CLOSES at 12-fold
(root c2606, verifications 1-12, 12-of-59 = 20.3% — TIED SECOND-LONGEST outright with
DRIFT-#41, behind only #31 39-fold and the #30 59-fold record).

THIS script performs the re-anchor: baseline -> (21,0,0,18,3), DRIFT-#43 root narrative,
chain insert with the movement cite, constants updated, py_compile gate. The validator
run that follows is the RE-ANCHOR CONFIRMATION (expected PASS 10/10 on the new root).
"""
import sys

DST = "/home/z/my-project/scripts/validate_cycle2618.py"
text = open(DST).read()

def rep(old, new, label):
    c = text.count(old)
    assert c == 1, f"{label} pre-patch count != 1: {c}"
    return text.replace(old, new)

# 1) P1 header -> DRIFT-#43 ROOT declaration
text = rep(
    "DRIFT-#42 verification-13 CARRY (root declared 2026-10-27 ~04:07 +08): "
    "rebadged from validate_cycle2617.py (the match-path rebadge was executed FIRST "
    "and FAILED on baseline_match — that run is the DRIFT-#42 declaration evidence — "
    "then re-anchored to the new root baseline)",
    "DRIFT-#43 ROOT DECLARATION (declared 2026-10-27 ~05:18 +08): "
    "rebadged from validate_cycle2617.py (the match-path rebadge was executed FIRST "
    "and FAILED on baseline_match — that run (validator exit 1, five-tuple "
    "(21,0,0,18,3) @ 446B vs the DRIFT-#42 baseline (22,0,1,18,3)) is the DRIFT-#43 "
    "declaration evidence — then re-anchored to the new root baseline; this second "
    "pass is the re-anchor confirmation)",
    "P1",
)

# 2) baseline line (line-8 instance)
text = rep(
    "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2618 = DRIFT-#42 verification 13",
    "(21,0,0,18,3) @ 446B DRIFT-#43 root; c2618 = DRIFT-#43 verification 1, ROOT",
    "baseline-line",
)

# 3) chain head -> DRIFT-#43 root insert with movement cite + DRIFT-#42 closure
text = rep(
    "(c2618 = DRIFT-#42 verification 13; c2617 = DRIFT-#42 verification 12; ",
    "(c2618 = DRIFT-#43 verification 1, ROOT — the movement: total 22->21 (-1), "
    "honest_free 1->0 (-1) HONEST INVENTORY CONTRACTION TO ZERO (a single honest-free "
    "departure accounts for BOTH deltas — the SIXTH of the post-DRIFT-#35 era: the "
    "6-task c2577 emergence has contracted 6->5->4->3->2->1->0; honest_paid=0 = NO "
    "GOLD), scam 18 + unknown 3 unchanged, SIZE 446B streak intact (the size band "
    "HELD across the movement); DRIFT-#42 CLOSED at 12-fold (root c2606, verifications "
    "1-12, 12-of-59 = 20.3% of the DRIFT-#30 record span — TIED SECOND-LONGEST outright "
    "with DRIFT-#41, behind only #31 39-fold and the #30 59-fold record); "
    "c2617 = DRIFT-#42 verification 12; ",
    "chain",
)

# 4) constants
text = rep(
    'BASELINE_COMP = {"total": 22, "honest_paid": 0, "honest_free": 1, "scam": 18, "unknown": 3}',
    'BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 3}',
    "BASELINE_COMP",
)

# 5) docstring assertion preamble
text = rep(
    "Assertions encode the DRIFT-#42 baseline (22,0,1,18,3) @ 446B:",
    "Assertions encode the DRIFT-#43 baseline (21,0,0,18,3) @ 446B:",
    "assert-preamble",
)

# 6) docstring BA-composition narrative bullet
text = rep(
    "- BA composition: total=22 honest_paid=0 honest_free=1 scam=18 unknown=3\n"
    "  (honest_free=1 = the DRIFT-#42 movement — a single honest-free DEPARTURE,\n"
    "  the FIFTH of the post-DRIFT-#35 era (6->5->4->3->2->1); aggregate-only visibility —\n"
    "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
    "  the 1 honest free task is NOT taken per the PAID-only policy)",
    "- BA composition: total=21 honest_paid=0 honest_free=0 scam=18 unknown=3\n"
    "  (honest_free=0 = the DRIFT-#43 movement — a single honest-free DEPARTURE,\n"
    "  the SIXTH of the post-DRIFT-#35 era (6->5->4->3->2->1->0) — honest inventory\n"
    "  now ZERO; aggregate-only visibility —\n"
    "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
    "  nothing honest remains to take per the PAID-only policy)",
    "BA-bullet",
)

open(DST, "w").write(text)

# P-HIST WATCH post-reanchor: 2617 refs == 2 (rebadged-from + chain insert);
# 2606 == 1; 2594 == 2; py_compile gate.
def hist(s):
    return text.count(s)

for tag, expect in (("2618", None), ("2617", 2), ("2606", 1), ("2594", 2)):
    n = hist(tag)
    line = f"P-HIST {tag} refs = {n}"
    if expect is not None:
        line += f" (expect {expect}) {'OK' if n == expect else 'MISMATCH'}"
    print(line)

import py_compile
py_compile.compile(DST, doraise=True)
print("py_compile OK:", DST)
print("REANCHOR COMPLETE — run the validator now (expected PASS 10/10 on the DRIFT-#43 root)")
