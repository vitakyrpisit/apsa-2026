#!/usr/bin/env python3
"""Rebadge validate_cycle2574.py -> validate_cycle2575.py (DRIFT-#34 verification-13).

Per the c2574 Next block: sed 2574->2575 + docstring verification-12->13 bump +
chain insert c2574 = verification 12 before the c2573 citation +
rebadged-from 2573->2574 + P-HIST WATCH (expect exactly 2 intentional 2574 refs).
REBADGE LESSON (c2573 incident): the P1 patch pattern must match the source-file
name AS IT EXISTS pre-patch — post-sed the header still names validate_cycle2573.py
(the global sed does not migrate the source-name token, which contains no "2574").
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2574.py"
DST = "/home/z/my-project/scripts/validate_cycle2575.py"

text = open(SRC).read()

# 1) global sed 2574->2575
text = text.replace("2574", "2575")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#34 verification-12 CARRY (post-loss rebadge lineage): "
          "rebadged from validate_cycle2573.py")
p1_new = ("DRIFT-#34 verification-13 CARRY (post-loss rebadge lineage): "
          "rebadged from validate_cycle2574.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump: c2575 = verification 12 -> 13 (post-sed state)
ch_old = "c2575 = verification 12\n"
ch_new = "c2575 = verification 13\n"
c = text.count(ch_old)
assert c == 1, f"chain-head pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

# 4) chain insert: c2574 = verification 12 before the c2573 citation
ci_old = "(c2573 = verification 11;"
ci_new = "(c2574 = verification 12; c2573 = verification 11;"
c = text.count(ci_old)
assert c == 1, f"chain-insert pre-patch count != 1: {c}"
text = text.replace(ci_old, ci_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2574 references post-rebadge
sites = [m.start() for m in re.finditer("2574", text)]
print(f"P-HIST 2574 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2574 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
