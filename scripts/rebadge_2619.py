#!/usr/bin/env python3
"""Rebadge validate_cycle2618.py -> validate_cycle2619.py (DRIFT-#43 verification-2, match-path).

Per the c2618 Next block: sed 2618->2619 + header ROOT DECLARATION -> verification-2 CARRY
bump (rebadged-from 2617->2618) + chain insert c2618 = DRIFT-#43 verification 1, ROOT +
line-8 bump + P-HIST WATCH (UPDATED steady-state rule, c2618-established: rebadged-from
2618 refs == 2 post-rebadge; 2606 == 2 (DRIFT-#42 closure cite); 2594 == 2 (DRIFT-#41
closure cite); all other predecessors == 1 each — spot-check 2617, which drops to 1 once
the rebadged-from pointer moves to 2618).
REBADGE LESSON (c2573 incident, applied first-pass forty-six cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS post-sed — post-sed the
header still names validate_cycle2617.py (unmigrated by the sed; 2617 is untouched by
the 2618->2619 sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#43 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2619 = DRIFT-#43 verification 2, the
root extends 1-fold -> 2-fold (five-tuple (21,0,0,18,3) reproduced @ 446B). Any
five-tuple move = DRIFT-#44 declaration (two-pass). honest_paid>0 = GOLD.
STAGING NOTE: staged PRE-POST this cycle (the law held at c2612..c2618 — carried);
rebadge EXECUTED pre-POST (validator exists before the capture POST).
"""
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2618.py"
DST = "/home/z/my-project/scripts/validate_cycle2619.py"

text = open(SRC).read()

# 1) global sed 2618->2619
text = text.replace("2618", "2619")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated);
#    the ROOT parenthetical narrative is KEPT (it accurately cites the declaration event).
p1_old = ("DRIFT-#43 ROOT DECLARATION (declared 2026-10-27 ~05:18 +08): "
          "rebadged from validate_cycle2617.py")
p1_new = ("DRIFT-#43 verification-2 CARRY (root declared 2026-10-27 ~05:18 +08): "
          "rebadged from validate_cycle2618.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump (post-sed form)
l8_old = "(21,0,0,18,3) @ 446B DRIFT-#43 root; c2619 = DRIFT-#43 verification 1, ROOT"
l8_new = "(21,0,0,18,3) @ 446B DRIFT-#43 root; c2619 = DRIFT-#43 verification 2"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain insert (post-sed form): restore c2618 ahead of the movement cite
ch_old = "(c2619 = DRIFT-#43 verification 1, ROOT — "
ch_new = ("(c2619 = DRIFT-#43 verification 2; "
          "c2618 = DRIFT-#43 verification 1, ROOT — ")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH (UPDATED steady-state rule): rebadged-from 2618 == 2; 2606 == 2
# (closure cite); 2594 == 2 (closure cite); 2617 == 1 (predecessor, pointer moved).
def hist(s):
    n = text.count(s)
    sites = []
    i = text.find(s)
    while i != -1 and len(sites) < 4:
        sites.append(text[max(0, i - 45):i + 28].replace("\n", "|"))
        i = text.find(s, i + 1)
    return n, sites

for tag, expect in (("2619", None), ("2618", 2), ("2617", 1), ("2606", 2), ("2594", 2)):
    n, sites = hist(tag)
    line = f"P-HIST {tag} refs = {n}"
    if expect is not None:
        line += f" (expect {expect}) {'OK' if n == expect else 'MISMATCH'}"
    print(line)
    for s in sites:
        print("  ctx:", s)

# syntax gate: the rebadged validator must compile before it is trusted
import py_compile
py_compile.compile(DST, doraise=True)
print("py_compile OK:", DST)
