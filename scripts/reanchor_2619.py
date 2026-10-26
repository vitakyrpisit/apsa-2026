#!/usr/bin/env python3
"""Reanchor validate_cycle2619.py to the DRIFT-#44 ROOT (second pass of the two-pass protocol).

DRIFT-#44 DECLARATION EVIDENCE (first pass, booked): the match-path rebadge run of
validate_cycle2619.py FAILED on baseline_match (validator exit 1) — captured five-tuple
(19,0,0,18,1) @ 446B vs the DRIFT-#43 baseline (21,0,0,18,3): total 21->19 (-2),
unknown 3->1 (-2) UNKNOWN DOUBLE-DEPARTURE (TWO unknown-category departures account for
BOTH deltas — the first DOUBLE-category movement of the tracked chain); honest_free 0
HOLDS at zero; honest_paid=0 — NO GOLD; scam 18 unchanged; SIZE 446B band HELD across
the movement; recursive diff confirmed exactly 2 field-level moves
(basedagents.total_tasks 21->19; basedagents.unknown 3->1). DRIFT-#43 CLOSES at 1-fold
(root c2618, verification 1 only — 1-of-59 = 1.7% of the DRIFT-#30 record span,
TIED-SHORTEST with DRIFT-#36 and DRIFT-#39).

THIS script performs the re-anchor: baseline -> (19,0,0,18,1), DRIFT-#44 root narrative,
chain insert with the movement cite + DRIFT-#43 closure cite, constants updated,
py_compile gate. The validator run that follows is the RE-ANCHOR CONFIRMATION
(expected PASS 10/10 on the new root).
"""
import sys

DST = "/home/z/my-project/scripts/validate_cycle2619.py"
text = open(DST).read()

def rep(old, new, label):
    c = text.count(old)
    assert c == 1, f"{label} pre-patch count != 1: {c}"
    return text.replace(old, new)

# 1) P1 header -> DRIFT-#44 ROOT declaration (full line incl. parenthetical)
text = rep(
    "DRIFT-#43 verification-2 CARRY (root declared 2026-10-27 ~05:18 +08): "
    "rebadged from validate_cycle2618.py (the match-path rebadge was executed FIRST "
    "and FAILED on baseline_match — that run (validator exit 1, five-tuple "
    "(21,0,0,18,3) @ 446B vs the DRIFT-#42 baseline (22,0,1,18,3)) is the DRIFT-#43 "
    "declaration evidence — then re-anchored to the new root baseline; this second "
    "pass is the re-anchor confirmation)",
    "DRIFT-#44 ROOT DECLARATION (declared 2026-10-27 ~05:23 +08): "
    "rebadged from validate_cycle2618.py (the match-path rebadge was executed FIRST "
    "and FAILED on baseline_match — that run (validator exit 1, five-tuple "
    "(19,0,0,18,1) @ 446B vs the DRIFT-#43 baseline (21,0,0,18,3)) is the DRIFT-#44 "
    "declaration evidence — then re-anchored to the new root baseline; this second "
    "pass is the re-anchor confirmation)",
    "P1",
)

# 2) baseline line (line-8 instance)
text = rep(
    "(21,0,0,18,3) @ 446B DRIFT-#43 root; c2619 = DRIFT-#43 verification 2",
    "(19,0,0,18,1) @ 446B DRIFT-#44 root; c2619 = DRIFT-#44 verification 1, ROOT",
    "baseline-line",
)

# 3) chain head -> DRIFT-#44 root insert with movement cite + DRIFT-#43 closure
text = rep(
    "(c2619 = DRIFT-#43 verification 2; c2618 = DRIFT-#43 verification 1, ROOT — ",
    "(c2619 = DRIFT-#44 verification 1, ROOT — the movement: total 21->19 (-2), "
    "unknown 3->1 (-2) UNKNOWN DOUBLE-DEPARTURE (TWO unknown-category departures "
    "account for BOTH deltas — the first DOUBLE-category movement of the tracked "
    "chain; honest_free 0 HOLDS at zero, honest_paid=0 = NO GOLD), scam 18 unchanged, "
    "SIZE 446B streak intact (the size band HELD across the movement); DRIFT-#43 "
    "CLOSED at 1-fold (root c2618, verification 1 only — 1-of-59 = 1.7% of the "
    "DRIFT-#30 record span, TIED-SHORTEST with DRIFT-#36 and DRIFT-#39); "
    "c2618 = DRIFT-#43 verification 1, ROOT — ",
    "chain",
)

# 4) constants
text = rep(
    'BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 3}',
    'BASELINE_COMP = {"total": 19, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 1}',
    "BASELINE_COMP",
)

# 5) docstring assertion preamble
text = rep(
    "Assertions encode the DRIFT-#43 baseline (21,0,0,18,3) @ 446B:",
    "Assertions encode the DRIFT-#44 baseline (19,0,0,18,1) @ 446B:",
    "assert-preamble",
)

# 6) docstring BA-composition narrative bullet
text = rep(
    "- BA composition: total=21 honest_paid=0 honest_free=0 scam=18 unknown=3\n"
    "  (honest_free=0 = the DRIFT-#43 movement — a single honest-free DEPARTURE,\n"
    "  the SIXTH of the post-DRIFT-#35 era (6->5->4->3->2->1->0) — honest inventory\n"
    "  now ZERO; aggregate-only visibility —\n"
    "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
    "  nothing honest remains to take per the PAID-only policy)",
    "- BA composition: total=19 honest_paid=0 honest_free=0 scam=18 unknown=1\n"
    "  (unknown 3->1 = the DRIFT-#44 movement — TWO unknown-category DEPARTURES,\n"
    "  the first DOUBLE-category movement of the tracked chain; honest_free=0 HOLDS\n"
    "  at zero; aggregate-only visibility —\n"
    "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
    "  nothing honest remains to take per the PAID-only policy)",
    "BA-bullet",
)

open(DST, "w").write(text)

# P-HIST WATCH post-reanchor: 2618 refs == 2 (rebadged-from + chain insert);
# 2617 == 1 (predecessor); 2606 == 2 (DRIFT-#42 closure cite); 2594 == 2 (DRIFT-#41
# closure cite); py_compile gate.
def hist(s):
    return text.count(s)

for tag, expect in (("2619", None), ("2618", 2), ("2617", 1), ("2606", 2), ("2594", 2)):
    n = hist(tag)
    line = f"P-HIST {tag} refs = {n}"
    if expect is not None:
        line += f" (expect {expect}) {'OK' if n == expect else 'MISMATCH'}"
    print(line)

import py_compile
py_compile.compile(DST, doraise=True)
print("py_compile OK:", DST)
print("REANCHOR COMPLETE — run the validator now (expected PASS 10/10 on the DRIFT-#44 root)")
