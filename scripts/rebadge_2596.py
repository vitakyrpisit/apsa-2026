#!/usr/bin/env python3
"""Rebadge validate_cycle2595.py -> validate_cycle2596.py (DRIFT-#41 verification-3, match-path).

Per the c2595 Next block (NOTE: the Next block labeled c2596 a "verification-2 CARRY"
cycle — an off-by-one phrasing; by the chain numbering c2594 = verification 1 ROOT,
c2595 = verification 2, so c2596 = verification 3. The rebadge follows the chain):
sed 2595->2596 + header verification-2 CARRY -> verification-3 CARRY bump (rebadged-from
2594->2595) + chain insert c2596 = DRIFT-#41 verification 3 + line-8 bump + P-HIST WATCH
(expect exactly 2 intentional 2595 refs post-rebadge; 2594 keeps 1 — chain history).
REBADGE LESSON (c2573 incident, applied first-pass twenty-three cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS post-sed — post-sed the
header still names validate_cycle2594.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#41 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2596 = DRIFT-#41 verification 3, the
root extends 2-fold -> 3-fold (five-tuple (23,0,2,18,3) reproduced @ 446B). Any
five-tuple move = DRIFT-#42 declaration (two-pass).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2595.py"
DST = "/home/z/my-project/scripts/validate_cycle2596.py"

text = open(SRC).read()

# 1) global sed 2595->2596
text = text.replace("2595", "2596")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#41 verification-2 CARRY (root declared 2026-10-27 ~03:02 +08): "
          "rebadged from validate_cycle2594.py")
p1_new = ("DRIFT-#41 verification-3 CARRY (root declared 2026-10-27 ~03:02 +08): "
          "rebadged from validate_cycle2595.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump
l8_old = "(23,0,2,18,3) @ 446B DRIFT-#41 root; c2596 = DRIFT-#41 verification 2"
l8_new = "(23,0,2,18,3) @ 446B DRIFT-#41 root; c2596 = DRIFT-#41 verification 3"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain-head bump + chain insert in ONE patch
ch_old = ("(c2596 = DRIFT-#41 verification 2; c2594 = DRIFT-#41 verification 1, ROOT — "
          "the movement:")
ch_new = ("(c2596 = DRIFT-#41 verification 3; c2595 = DRIFT-#41 verification 2; "
          "c2594 = DRIFT-#41 verification 1, ROOT — the movement:")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2595 references post-rebadge
# (rebadged-from header + chain insert); 2594 keeps exactly 1 (chain history).
sites_95 = [m.start() for m in re.finditer("2595", text)]
sites_94 = [m.start() for m in re.finditer("2594", text)]
print(f"P-HIST 2595 refs = {len(sites_95)}")
for s in sites_95:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
print(f"P-HIST 2594 refs = {len(sites_94)} (chain history)")
if len(sites_95) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2595 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
