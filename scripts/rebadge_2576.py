#!/usr/bin/env python3
"""Rebadge validate_cycle2575.py -> validate_cycle2576.py (DRIFT-#34 verification-14).

Per the c2575 Next block: sed 2575->2576 + docstring verification-13->14 bump +
chain insert c2575 = verification 13 before the c2574 citation +
rebadged-from 2574->2575 + P-HIST WATCH (expect exactly 2 intentional 2575 refs).
REBADGE LESSON (c2573 incident, applied first-pass three cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch — post-sed
the header still names validate_cycle2574.py (the global sed does not migrate the
source-name token, which contains no "2575").
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2575.py"
DST = "/home/z/my-project/scripts/validate_cycle2576.py"

text = open(SRC).read()

# 1) global sed 2575->2576
text = text.replace("2575", "2576")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#34 verification-13 CARRY (post-loss rebadge lineage): "
          "rebadged from validate_cycle2574.py")
p1_new = ("DRIFT-#34 verification-14 CARRY (post-loss rebadge lineage): "
          "rebadged from validate_cycle2575.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump: c2576 = verification 13 -> 14 (post-sed state)
ch_old = "c2576 = verification 13\n"
ch_new = "c2576 = verification 14\n"
c = text.count(ch_old)
assert c == 1, f"chain-head pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

# 4) chain insert: c2575 = verification 13 before the c2574 citation
ci_old = "(c2574 = verification 12;"
ci_new = "(c2575 = verification 13; c2574 = verification 12;"
c = text.count(ci_old)
assert c == 1, f"chain-insert pre-patch count != 1: {c}"
text = text.replace(ci_old, ci_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2575 references post-rebadge
sites = [m.start() for m in re.finditer("2575", text)]
print(f"P-HIST 2575 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2575 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
