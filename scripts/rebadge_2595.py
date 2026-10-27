#!/usr/bin/env python3
"""Rebadge validate_cycle2594.py -> validate_cycle2595.py (DRIFT-#41 verification-2, match-path).

Per the c2594 Next block: sed 2594->2595 + header DRIFT-#41 ROOT DECLARED ->
verification-2 CARRY bump (header "DRIFT-#41 ROOT DECLARED" -> "DRIFT-#41 verification-2
CARRY (root declared 2026-10-27 ~03:02 +08)") + chain insert c2595 = DRIFT-#41
verification 2, ROOT re-attach c2594 = DRIFT-#41 verification 1 + rebadged-from
2593->2594 + P-HIST WATCH (expect exactly 2 intentional 2594 refs post-rebadge;
2593 keeps 1 — chain re-attach).
REBADGE LESSON (c2573 incident, applied first-pass twenty-two cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2593.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#41 baseline HOLD branch, re-anchored root
from c2594). The validator run that follows is EXPECTED TO PASS 10/10 — c2595 =
DRIFT-#41 verification 2, the root extends 1-fold -> 2-fold (five-tuple (23,0,2,18,3)
reproduced @ 446B). Any five-tuple move = DRIFT-#42 declaration (two-pass).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2594.py"
DST = "/home/z/my-project/scripts/validate_cycle2595.py"

text = open(SRC).read()

# 1) global sed 2594->2595
text = text.replace("2594", "2595")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#41 ROOT DECLARED (2026-10-27 ~03:02 +08): rebadged from "
          "validate_cycle2593.py")
p1_new = ("DRIFT-#41 verification-2 CARRY (root declared 2026-10-27 ~03:02 +08): "
          "rebadged from validate_cycle2594.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump
l8_old = "(23,0,2,18,3) @ 446B DRIFT-#41 root; c2595 = DRIFT-#41 verification 1"
l8_new = "(23,0,2,18,3) @ 446B DRIFT-#41 root; c2595 = DRIFT-#41 verification 2"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain-head bump + chain insert in ONE patch
ch_old = "(c2595 = DRIFT-#41 verification 1, ROOT — the movement: total 24->23 (-1),"
ch_new = ("(c2595 = DRIFT-#41 verification 2; c2594 = DRIFT-#41 verification 1, ROOT — "
          "the movement: total 24->23 (-1),")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2594 references post-rebadge
# (rebadged-from header + chain insert); 2593 keeps exactly 1 (chain re-attach).
sites_94 = [m.start() for m in re.finditer("2594", text)]
sites_93 = [m.start() for m in re.finditer("2593", text)]
print(f"P-HIST 2594 refs = {len(sites_94)}")
for s in sites_94:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
print(f"P-HIST 2593 refs = {len(sites_93)} (chain re-attach)")
if len(sites_94) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2594 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
