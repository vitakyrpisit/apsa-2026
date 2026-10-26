#!/usr/bin/env python3
"""Rebadge validate_cycle2617.py -> validate_cycle2618.py (DRIFT-#42 verification-13, match-path).

Per the c2617 Next block: sed 2617->2618 + header verification-12 CARRY -> verification-13
CARRY bump (rebadged-from 2616->2617) + chain insert c2617 = DRIFT-#42 verification 12 +
line-8 bump + P-HIST WATCH (steady-state rule: rebadged-from 2617 refs == 2 post-rebadge;
all older predecessors 2616..2595 == 1 each; 2594 == 2 — the DRIFT-#41 closure root cite).
REBADGE LESSON (c2573 incident, applied first-pass forty-five cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS post-sed — post-sed the
header still names validate_cycle2616.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#42 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2618 = DRIFT-#42 verification 13, the
root extends 12-fold -> 13-fold (five-tuple (22,0,1,18,3) reproduced @ 446B). A PASS
here makes DRIFT-#42 the SOLE SECOND-LONGEST outright (breaking the tie with #41 at
12). Any five-tuple move = DRIFT-#43 declaration (two-pass).
STAGING NOTE: staged PRE-POST this cycle (the law held at c2612..c2617 — carried);
rebadge EXECUTED pre-POST (validator exists before the capture POST).
P-HIST implemented with str.count / str.find loops (no comprehension-display hazard).
"""
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2617.py"
DST = "/home/z/my-project/scripts/validate_cycle2618.py"

text = open(SRC).read()

# 1) global sed 2617->2618
text = text.replace("2617", "2618")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#42 verification-12 CARRY (root declared 2026-10-27 ~04:07 +08): "
          "rebadged from validate_cycle2616.py")
p1_new = ("DRIFT-#42 verification-13 CARRY (root declared 2026-10-27 ~04:07 +08): "
          "rebadged from validate_cycle2617.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump (post-sed form)
l8_old = "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2618 = DRIFT-#42 verification 12"
l8_new = "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2618 = DRIFT-#42 verification 13"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain-head bump + chain insert in ONE patch (post-sed form)
ch_old = ("(c2618 = DRIFT-#42 verification 12; c2616 = DRIFT-#42 verification 11; ")
ch_new = ("(c2618 = DRIFT-#42 verification 13; c2617 = DRIFT-#42 verification 12; "
          "c2616 = DRIFT-#42 verification 11; ")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH (steady-state rule): rebadged-from 2617 == 2; predecessors 2616..2595
# == 1 each (spot-check 2616, 2606); 2594 == 2 (closure cite).
def hist(s):
    n = text.count(s)
    sites = []
    i = text.find(s)
    while i != -1 and len(sites) < 4:
        sites.append(text[max(0, i - 45):i + 28].replace("\n", "|"))
        i = text.find(s, i + 1)
    return n, sites

for tag, expect in (("2618", None), ("2617", 2), ("2616", 1), ("2606", 1), ("2594", 2)):
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
