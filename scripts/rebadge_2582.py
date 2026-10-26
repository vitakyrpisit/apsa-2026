#!/usr/bin/env python3
"""Rebadge validate_cycle2581.py -> validate_cycle2582.py (DRIFT-#37 verification-2, match-path).

Per the c2581 Next block: sed 2581->2582 + docstring DRIFT-#37 ROOT -> verification-2 CARRY
bump + chain insert c2581 = DRIFT-#37 verification 1 before the c2580 citation + rebadged-from
2580->2581 + P-HIST WATCH (expect exactly 2 intentional 2581 refs post-rebadge).
REBADGE LESSON (c2573 incident, applied first-pass nine cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2580.py (unmigrated by the sed).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2581.py"
DST = "/home/z/my-project/scripts/validate_cycle2582.py"

text = open(SRC).read()

# 1) global sed 2581->2582
text = text.replace("2581", "2582")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#37 ROOT validator (declared at c2582, 2026-10-27 ~00:49 +08): "
          "rebadged from validate_cycle2580.py")
p1_new = ("DRIFT-#37 verification-2 CARRY (root declared 2026-10-27 ~00:49 +08): "
          "rebadged from validate_cycle2581.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump + chain insert in ONE patch
ch_old = "(c2582 = DRIFT-#37 verification 1, ROOT — the movement:"
ch_new = "(c2582 = DRIFT-#37 verification 2; c2581 = DRIFT-#37 verification 1, ROOT — the movement:"
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2581 references post-rebadge
sites = [m.start() for m in re.finditer("2581", text)]
print(f"P-HIST 2581 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2581 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
