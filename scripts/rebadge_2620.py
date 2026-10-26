#!/usr/bin/env python3
"""Rebadge validate_cycle2619.py -> validate_cycle2620.py (DRIFT-#44 verification-2, match-path).

Per the c2619 Next block: sed 2619->2620 + header ROOT DECLARATION -> verification-2 CARRY
bump (rebadged-from 2618->2619) + chain insert c2619 = DRIFT-#44 verification 1, ROOT +
line-8 bump + P-HIST WATCH (UPDATED steady-state rule, c2619-established: rebadged-from
2619 refs == 2 post-rebadge; 2618 == 2 (chain line + DRIFT-#43 closure cite); 2606 == 2
(chain root line + DRIFT-#42 closure cite); 2594 == 2 (chain root line + DRIFT-#41
closure cite); all other predecessors == 1 each — spot-check 2617, which drops to 1 once
the rebadged-from pointer moves to 2619).
REBADGE LESSON (c2573 incident, applied first-pass forty-seven cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS post-sed — post-sed the
header still names validate_cycle2618.py (unmigrated by the sed; 2618 is untouched by
the 2619->2620 sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#44 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2620 = DRIFT-#44 verification 2, the
root extends 1-fold -> 2-fold (five-tuple (19,0,0,18,1) reproduced @ 446B). Any
five-tuple move = DRIFT-#45 declaration (two-pass). honest_paid>0 = GOLD.
STAGING NOTE: staged PRE-POST this cycle (the law held at c2612..c2619 — carried);
rebadge EXECUTED pre-POST (validator exists before the capture POST).
"""
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2619.py"
DST = "/home/z/my-project/scripts/validate_cycle2620.py"

text = open(SRC).read()

# 1) global sed 2619->2620
text = text.replace("2619", "2620")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated);
#    the ROOT parenthetical narrative is KEPT (it accurately cites the declaration event).
p1_old = ("DRIFT-#44 ROOT DECLARATION (declared 2026-10-27 ~05:23 +08): "
          "rebadged from validate_cycle2618.py")
p1_new = ("DRIFT-#44 verification-2 CARRY (root declared 2026-10-27 ~05:23 +08): "
          "rebadged from validate_cycle2619.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump (post-sed form)
l8_old = "(19,0,0,18,1) @ 446B DRIFT-#44 root; c2620 = DRIFT-#44 verification 1, ROOT"
l8_new = "(19,0,0,18,1) @ 446B DRIFT-#44 root; c2620 = DRIFT-#44 verification 2"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain insert (post-sed form): restore c2619 ahead of the movement cite
ch_old = "(c2620 = DRIFT-#44 verification 1, ROOT — "
ch_new = ("(c2620 = DRIFT-#44 verification 2; "
          "c2619 = DRIFT-#44 verification 1, ROOT — ")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH (UPDATED steady-state rule): rebadged-from 2619 == 2; 2618 == 2
# (chain line + DRIFT-#43 closure cite); 2606 == 2; 2594 == 2; 2617 == 1.
def hist(s):
    n = text.count(s)
    sites = []
    i = text.find(s)
    while i != -1 and len(sites) < 4:
        sites.append(text[max(0, i - 45):i + 28].replace("\n", "|"))
        i = text.find(s, i + 1)
    return n, sites

for tag, expect in (("2620", None), ("2619", 2), ("2618", 2), ("2617", 1), ("2606", 2), ("2594", 2)):
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
