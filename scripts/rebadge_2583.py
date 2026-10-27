#!/usr/bin/env python3
"""Rebadge validate_cycle2582.py -> validate_cycle2583.py (DRIFT-#37 verification-3, match-path).

Per the c2582 Next block: sed 2582->2583 + docstring DRIFT-#37 verification-2->3 bump +
chain insert c2582 = DRIFT-#37 verification 2 before the c2581 citation + rebadged-from
2581->2582 + P-HIST WATCH (expect exactly 2 intentional 2582 refs post-rebadge).
REBADGE LESSON (c2573 incident, applied first-pass ten cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2581.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (pass 1 of the two-pass protocol). The validator
run that follows is EXPECTED TO FAIL on baseline_match — that failure is the DRIFT-#38
declaration evidence (the five-tuple moved to (26,0,4,18,4)).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2582.py"
DST = "/home/z/my-project/scripts/validate_cycle2583.py"

text = open(SRC).read()

# 1) global sed 2582->2583
text = text.replace("2582", "2583")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#37 verification-2 CARRY (root declared 2026-10-27 ~00:49 +08): "
          "rebadged from validate_cycle2581.py")
p1_new = ("DRIFT-#37 verification-3 CARRY (root declared 2026-10-27 ~00:49 +08): "
          "rebadged from validate_cycle2582.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump + chain insert in ONE patch
ch_old = "(c2583 = DRIFT-#37 verification 2; c2581"
ch_new = "(c2583 = DRIFT-#37 verification 3; c2582 = DRIFT-#37 verification 2; c2581"
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2582 references post-rebadge
sites = [m.start() for m in re.finditer("2582", text)]
print(f"P-HIST 2582 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2582 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
