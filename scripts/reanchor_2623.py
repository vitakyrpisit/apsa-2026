#!/usr/bin/env python3
"""Reanchor validate_cycle2623.py to the DRIFT-#45 ROOT (second pass of the two-pass protocol).

DRIFT-#45 DECLARATION EVIDENCE (first pass, booked): the verification-5 CARRY run of
validate_cycle2623.py FAILED on baseline_match (validator exit 1, the ONLY failure of
10 assertions) — captured five-tuple (18,0,0,18,0) @ 446B vs the DRIFT-#44 baseline
(19,0,0,18,1): total 19->18 (-1), unknown 1->0 (-1) UNKNOWN POOL DRAIN TO ZERO (a
single unknown-category departure accounts for BOTH deltas — the unknown category
EXITS the board entirely — the FIRST unknown=0 print and FIRST (18,0,0,18,0)
five-tuple of the on-disk ledger era (c2453..), landing on the LOWER EDGE of the
predicted DRIFT-#45 live band "total 19->18/20, unknown 1->0/2"); honest_free 0 HOLDS
at zero; honest_paid=0 — NO GOLD; scam 18 unchanged; SIZE 446B band HELD across the
movement; recursive_diff_2623.py confirmed MARKET_CHANGED with EXACTLY 2 field-level
moves (basedagents.total_tasks 19->18; basedagents.unknown 1->0), 382-vs-382
otherwise. DRIFT-#44 CLOSES at 4-fold (root c2619, verifications 1-4, 4-of-59 = 6.8%
of the DRIFT-#30 record span).

THIS script performs the re-anchor: baseline -> (18,0,0,18,0), DRIFT-#45 root
narrative, chain insert with the movement cite + DRIFT-#44 closure cite, constants
updated, py_compile gate. The validator run that follows is the RE-ANCHOR
CONFIRMATION (expected PASS 10/10 on the new root).
"""
import sys

DST = "/home/z/my-project/scripts/validate_cycle2623.py"
text = open(DST).read()

def rep(old, new, label):
    c = text.count(old)
    assert c == 1, f"{label} pre-patch count != 1: {c}"
    return text.replace(old, new)

# 1) P1 header -> DRIFT-#45 ROOT declaration (full line incl. parenthetical)
text = rep(
    "DRIFT-#44 verification-5 CARRY (root declared 2026-10-27 ~05:23 +08): "
    "rebadged from validate_cycle2622.py (the match-path rebadge was executed FIRST "
    "and FAILED on baseline_match — that run (validator exit 1, five-tuple "
    "(19,0,0,18,1) @ 446B vs the DRIFT-#43 baseline (21,0,0,18,3)) is the DRIFT-#44 "
    "declaration evidence — then re-anchored to the new root baseline; this second "
    "pass is the re-anchor confirmation)",
    "DRIFT-#45 ROOT DECLARATION (declared 2026-10-27 ~06:04 +08): "
    "rebadged from validate_cycle2622.py (the match-path rebadge was executed FIRST "
    "and FAILED on baseline_match — that run (validator exit 1, five-tuple "
    "(18,0,0,18,0) @ 446B vs the DRIFT-#44 baseline (19,0,0,18,1)) is the DRIFT-#45 "
    "declaration evidence — then re-anchored to the new root baseline; this second "
    "pass is the re-anchor confirmation)",
    "P1",
)

# 2) baseline line (line-8 instance)
text = rep(
    "(19,0,0,18,1) @ 446B DRIFT-#44 root; c2623 = DRIFT-#44 verification 5",
    "(18,0,0,18,0) @ 446B DRIFT-#45 root; c2623 = DRIFT-#45 verification 1, ROOT",
    "baseline-line",
)

# 3) chain head -> DRIFT-#45 root insert with movement cite + DRIFT-#44 closure
text = rep(
    "(c2623 = DRIFT-#44 verification 5; c2622 = DRIFT-#44 verification 4; "
    "c2621 = DRIFT-#44 verification 3;",
    "(c2623 = DRIFT-#45 verification 1, ROOT — the movement: total 19->18 (-1), "
    "unknown 1->0 (-1) UNKNOWN POOL DRAIN TO ZERO (a single unknown-category "
    "departure accounts for BOTH deltas — the unknown category EXITS the board "
    "entirely — the FIRST unknown=0 print and FIRST (18,0,0,18,0) five-tuple of the "
    "on-disk ledger era (c2453..), landing on the LOWER EDGE of the predicted "
    "DRIFT-#45 live band; honest_free 0 HOLDS at zero, honest_paid=0 = NO GOLD), "
    "scam 18 unchanged, SIZE 446B streak intact (the size band HELD across the "
    "movement); DRIFT-#44 CLOSED at 4-fold (root c2619, verifications 1-4, 4-of-59 "
    "= 6.8% of the DRIFT-#30 record span); c2622 = DRIFT-#44 verification 4; "
    "c2621 = DRIFT-#44 verification 3;",
    "chain",
)

# 4) constants
text = rep(
    'BASELINE_COMP = {"total": 19, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 1}',
    'BASELINE_COMP = {"total": 18, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 0}',
    "BASELINE_COMP",
)

# 5) docstring assertion preamble
text = rep(
    "Assertions encode the DRIFT-#44 baseline (19,0,0,18,1) @ 446B:",
    "Assertions encode the DRIFT-#45 baseline (18,0,0,18,0) @ 446B:",
    "assert-preamble",
)

# 6) docstring BA-composition narrative bullet
text = rep(
    "- BA composition: total=19 honest_paid=0 honest_free=0 scam=18 unknown=1\n"
    "  (unknown 3->1 = the DRIFT-#44 movement — TWO unknown-category DEPARTURES,\n"
    "  the first DOUBLE-category movement of the tracked chain; honest_free=0 HOLDS\n"
    "  at zero; aggregate-only visibility —\n"
    "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
    "  nothing honest remains to take per the PAID-only policy)",
    "- BA composition: total=18 honest_paid=0 honest_free=0 scam=18 unknown=0\n"
    "  (unknown 1->0 = the DRIFT-#45 movement — a single unknown-category DEPARTURE\n"
    "  drains the unknown pool to ZERO — the inventory is now scam-pure (18 scam,\n"
    "  zero honest, zero unknown — the FIRST unknown=0 print of the on-disk ledger\n"
    "  era); honest_free=0 HOLDS at zero; aggregate-only visibility —\n"
    "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
    "  nothing honest remains to take per the PAID-only policy)",
    "BA-bullet",
)

open(DST, "w").write(text)

# P-HIST WATCH post-reanchor: 2622 refs == 2 (rebadged-from + chain insert);
# 2619 == 2 (chain ROOT line + DRIFT-#44 closure cite — joins the closure-cite
# pattern); 2618 == 2 (DRIFT-#43 closure cite); 2606 == 2; 2594 == 2; py_compile gate.
def hist(s):
    return text.count(s)

for tag, expect in (("2623", None), ("2622", 2), ("2621", 1), ("2620", 1),
                    ("2619", 2), ("2618", 2), ("2606", 2), ("2594", 2)):
    n = hist(tag)
    line = f"P-HIST {tag} refs = {n}"
    if expect is not None:
        line += f" (expect {expect}) {'OK' if n == expect else 'MISMATCH'}"
    print(line)

import py_compile
py_compile.compile(DST, doraise=True)
print("py_compile OK:", DST)
print("REANCHOR COMPLETE — run the validator now (expected PASS 10/10 on the DRIFT-#45 root)")
