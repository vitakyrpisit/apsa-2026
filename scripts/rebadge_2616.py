#!/usr/bin/env python3
"""Rebadge validate_cycle2615.py -> validate_cycle2616.py (DRIFT-#42 verification-11, match-path).

Per the c2615 Next block: sed 2615->2616 + header verification-10 CARRY -> verification-11
CARRY bump (rebadged-from 2614->2615) + chain insert c2615 = DRIFT-#42 verification 10 +
line-8 bump + P-HIST WATCH (expect exactly 2 intentional 2615 refs post-rebadge; 2614
keeps 2; 2613..2595 keep 1 each; 2594 keeps 2 — the DRIFT-#41 closure root cite).
REBADGE LESSON (c2573 incident, applied first-pass forty-three cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS post-sed — post-sed the
header still names validate_cycle2614.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#42 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2616 = DRIFT-#42 verification 11, the
root extends 10-fold -> 11-fold (five-tuple (22,0,1,18,3) reproduced @ 446B). Any
five-tuple move = DRIFT-#43 declaration (two-pass).
STAGING NOTE: staged PRE-POST this cycle (the law held at c2612..c2615 — carried);
rebadge EXECUTED pre-POST this cycle (validator exists before the capture POST).
P-HIST implemented with str.count / str.find loops (no comprehension-display hazard).
"""
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2615.py"
DST = "/home/z/my-project/scripts/validate_cycle2616.py"

text = open(SRC).read()

# 1) global sed 2615->2616
text = text.replace("2615", "2616")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#42 verification-10 CARRY (root declared 2026-10-27 ~04:07 +08): "
          "rebadged from validate_cycle2614.py")
p1_new = ("DRIFT-#42 verification-11 CARRY (root declared 2026-10-27 ~04:07 +08): "
          "rebadged from validate_cycle2615.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump (post-sed form)
l8_old = "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2616 = DRIFT-#42 verification 10"
l8_new = "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2616 = DRIFT-#42 verification 11"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain-head bump + chain insert in ONE patch (post-sed form)
ch_old = ("(c2616 = DRIFT-#42 verification 10; c2614 = DRIFT-#42 verification 9; ")
ch_new = ("(c2616 = DRIFT-#42 verification 11; c2615 = DRIFT-#42 verification 10; "
          "c2614 = DRIFT-#42 verification 9; ")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: post-rebadge expect 2615 refs == 2 (rebadged-from header + chain
# insert); 2614 keeps 2 (carried); 2594 keeps 2 (DRIFT-#41 closure root cite);
# others in the deep history keep their carried counts (printed, not asserted).
def hist(s):
    n = text.count(s)
    sites = []
    i = text.find(s)
    while i != -1 and len(sites) < 8:
        sites.append(text[max(0, i - 45):i + 28].replace("\n", "|"))
        i = text.find(s, i + 1)
    return n, sites

for tag, expect in (("2616", None), ("2615", 2), ("2614", 2), ("2594", 2)):
    n, sites = hist(tag)
    line = f"P-HIST {tag} refs = {n}"
    if expect is not None:
        line += f" (expect {expect}) {'OK' if n == expect else 'MISMATCH'}"
    print(line)
    for s in sites:
        print("  ctx:", s)
        if len(sites) > 4:
            break

# syntax gate: the rebadged validator must compile before it is trusted
import py_compile
py_compile.compile(DST, doraise=True)
print("py_compile OK:", DST)
