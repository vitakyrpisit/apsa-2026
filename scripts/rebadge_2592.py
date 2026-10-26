#!/usr/bin/env python3
"""Rebadge validate_cycle2591.py -> validate_cycle2592.py (DRIFT-#40 verification-2, match-path).

Per the c2591 Next block: sed 2591->2592 + docstring DRIFT-#40 ROOT DECLARED ->
verification-2 CARRY bump (header "DRIFT-#40 ROOT DECLARED" -> "DRIFT-#40 verification-2
CARRY (root declared 2026-10-27 ~02:28 +08)") + chain insert c2591 = DRIFT-#40
verification 1, ROOT before the DRIFT-#39 closure citation + rebadged-from 2590->2591 +
P-HIST WATCH (expect exactly 2 intentional 2591 refs post-rebadge).
REBADGE LESSON (c2573 incident, applied first-pass nineteen cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2590.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#40 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2592 = DRIFT-#40 verification 2, the
root extends 1-fold -> 2-fold (five-tuple (24,0,3,18,3) reproduced @ 446B).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2591.py"
DST = "/home/z/my-project/scripts/validate_cycle2592.py"

text = open(SRC).read()

# 1) global sed 2591->2592
text = text.replace("2591", "2592")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#40 ROOT DECLARED (2026-10-27 ~02:28 +08): rebadged from "
          "validate_cycle2590.py")
p1_new = ("DRIFT-#40 verification-2 CARRY (root declared 2026-10-27 ~02:28 +08): "
          "rebadged from validate_cycle2591.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump + chain insert in ONE patch
ch_old = "(c2592 = DRIFT-#40 verification 1, ROOT — the movement: total 25->24 (-1),"
ch_new = ("(c2592 = DRIFT-#40 verification 2; c2591 = DRIFT-#40 verification 1, ROOT — "
          "the movement: total 25->24 (-1),")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2591 references post-rebadge
sites = [m.start() for m in re.finditer("2591", text)]
print(f"P-HIST 2591 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2591 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
