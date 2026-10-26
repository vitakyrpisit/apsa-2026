#!/usr/bin/env python3
"""Rebadge validate_cycle2587.py -> validate_cycle2588.py (DRIFT-#38 verification-6, match-path).

Per the c2587 Next block: sed 2587->2588 + docstring DRIFT-#38 verification-5->6 CARRY bump +
chain insert c2587 = DRIFT-#38 verification 5 before the c2586 citation + rebadged-from
2586->2587 + P-HIST WATCH (expect exactly 2 intentional 2587 refs post-rebadge).
REBADGE LESSON (c2573 incident, applied first-pass fifteen cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2586.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#38 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2588 = DRIFT-#38 verification 6, the
root extends 5-fold -> 6-fold (five-tuple (26,0,4,18,4) reproduced @ 446B).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2587.py"
DST = "/home/z/my-project/scripts/validate_cycle2588.py"

text = open(SRC).read()

# 1) global sed 2587->2588
text = text.replace("2587", "2588")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#38 verification-5 CARRY (root declared 2026-10-27 ~01:06 +08): "
          "rebadged from validate_cycle2586.py")
p1_new = ("DRIFT-#38 verification-6 CARRY (root declared 2026-10-27 ~01:06 +08): "
          "rebadged from validate_cycle2587.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump + chain insert in ONE patch
ch_old = "(c2588 = DRIFT-#38 verification 5; c2586 = DRIFT-#38 verification 4; c2585"
ch_new = ("(c2588 = DRIFT-#38 verification 6; c2587 = DRIFT-#38 verification 5; "
          "c2586 = DRIFT-#38 verification 4; c2585")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2587 references post-rebadge
sites = [m.start() for m in re.finditer("2587", text)]
print(f"P-HIST 2587 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2587 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
