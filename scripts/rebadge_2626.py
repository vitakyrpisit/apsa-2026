#!/usr/bin/env python3
"""Rebadge validate_cycle2625.py -> validate_cycle2626.py (DRIFT-#45 verification-4 CARRY).

STAGING ORDER LAW: run PRE-POST so the validator exists before the capture.
Anchors pre-verified against the ACTUAL validate_cycle2625.py bytes (c2624/c2625
proactive lesson; f-string caveat applied — baseline_match_c{CYCLE} is a TEMPLATE,
only literal cycle tokens counted):
  - sed source '2625' literal tokens == 6 (lines 2/8/9/44/45/46)
  - P1 anchor count == 1
  - line-8 anchor count == 1 (disambiguated by 'root; ' prefix)
  - chain head anchor count == 1 (disambiguated by '(' prefix)
"""
import py_compile

SRC = "/home/z/my-project/scripts/validate_cycle2625.py"
DST = "/home/z/my-project/scripts/validate_cycle2626.py"

text = open(SRC).read()

# Stage 1: global cycle-token migration 2625 -> 2626
n = text.count("2625")
assert n == 6, f"sed source count {n} != 6"
text = text.replace("2625", "2626")

# Stage 2: P1 docstring header patch (parenthetical carries VERBATIM per CARRY precedent)
P1_OLD = ("DRIFT-#45 verification-3 CARRY (root declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2624.py")
P1_NEW = ("DRIFT-#45 verification-4 CARRY (root declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2625.py")
n = text.count(P1_OLD)
assert n == 1, f"P1 anchor count {n} != 1"
text = text.replace(P1_OLD, P1_NEW)

# Stage 3: line-8 bump (disambiguated by 'root; ' prefix — bare probe is 2x post-sed)
L8_OLD = "DRIFT-#45 root; c2626 = DRIFT-#45 verification 3"
L8_NEW = "DRIFT-#45 root; c2626 = DRIFT-#45 verification 4"
n = text.count(L8_OLD)
assert n == 1, f"line-8 anchor count {n} != 1"
text = text.replace(L8_OLD, L8_NEW)

# Stage 4: chain insert (disambiguated by '(' prefix) — head bump 3->4 + restore c2625 line
CH_OLD = "(c2626 = DRIFT-#45 verification 3; c2624 = DRIFT-#45 verification 2"
CH_NEW = ("(c2626 = DRIFT-#45 verification 4; c2625 = DRIFT-#45 verification 3; "
          "c2624 = DRIFT-#45 verification 2")
n = text.count(CH_OLD)
assert n == 1, f"chain anchor count {n} != 1"
text = text.replace(CH_OLD, CH_NEW)

open(DST, "w").write(text)
py_compile.compile(DST, doraise=True)

# Post-rebadge P-HIST spot checks (steady-state rule, c2626 form)
for tok, want in (("2625", 2), ("2624", 1), ("2623", 1), ("2619", 2),
                  ("2618", 2), ("2606", 2), ("2594", 2), ("2626", 6)):
    got = text.count(tok)
    assert got == want, f"P-HIST {tok}: {got} != {want}"
print("rebadge OK: validate_cycle2626.py written; py_compile OK; P-HIST steady-state CONFIRMED")
