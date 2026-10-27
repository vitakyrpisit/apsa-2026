#!/usr/bin/env python3
"""Rebadge validate_cycle2577.py -> validate_cycle2578.py (DRIFT-#35 verification-2).

Per the c2577 Next block: sed 2577->2578 + docstring DRIFT-#35 verification-1->2 bump +
chain insert c2577 = DRIFT-#35 verification 1 before the c2576 citation +
rebadged-from 2576->2577 + P-HIST WATCH (expect exactly 2 intentional 2577 refs).
REBADGE LESSON (c2573 incident, applied first-pass five cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2576.py (the global sed does not migrate the
source-name token, which contains no "2577").
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2577.py"
DST = "/home/z/my-project/scripts/validate_cycle2578.py"

text = open(SRC).read()

# 1) global sed 2577->2578
text = text.replace("2577", "2578")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated);
#    the ROOT marker becomes the verification-2 CARRY marker in the same patch
p1_old = ("DRIFT-#35 ROOT validator (declared at c2578, 2026-10-27 ~00:08 +08): "
          "rebadged from validate_cycle2576.py")
p1_new = ("DRIFT-#35 verification-2 CARRY (root declared 2026-10-27 ~00:08 +08): "
          "rebadged from validate_cycle2577.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump + chain insert in ONE patch: the ROOT narrative re-attaches
#    to the inserted c2577 node (it reads as the root description that follows)
ch_old = "(c2578 = DRIFT-#35 verification 1, ROOT — the movement:"
ch_new = "(c2578 = DRIFT-#35 verification 2; c2577 = DRIFT-#35 verification 1, ROOT — the movement:"
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2577 references post-rebadge
sites = [m.start() for m in re.finditer("2577", text)]
print(f"P-HIST 2577 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2577 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
