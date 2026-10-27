#!/usr/bin/env python3
"""Rebadge validate_cycle2578.py -> validate_cycle2579.py (DRIFT-#35 verification-3).

Per the c2578 Next block: sed 2578->2579 + docstring DRIFT-#35 verification-2->3 bump +
chain insert c2578 = DRIFT-#35 verification 2 before the c2577 citation +
rebadged-from 2577->2578 + P-HIST WATCH (expect exactly 2 intentional 2578 refs).
REBADGE LESSON (c2573 incident, applied first-pass six cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2577.py (unmigrated by the sed).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2578.py"
DST = "/home/z/my-project/scripts/validate_cycle2579.py"

text = open(SRC).read()

# 1) global sed 2578->2579
text = text.replace("2578", "2579")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#35 verification-2 CARRY (root declared 2026-10-27 ~00:08 +08): "
          "rebadged from validate_cycle2577.py")
p1_new = ("DRIFT-#35 verification-3 CARRY (root declared 2026-10-27 ~00:08 +08): "
          "rebadged from validate_cycle2578.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump + chain insert in ONE patch
ch_old = "(c2579 = DRIFT-#35 verification 2; c2577"
ch_new = "(c2579 = DRIFT-#35 verification 3; c2578 = DRIFT-#35 verification 2; c2577"
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2578 references post-rebadge
sites = [m.start() for m in re.finditer("2578", text)]
print(f"P-HIST 2578 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2578 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
