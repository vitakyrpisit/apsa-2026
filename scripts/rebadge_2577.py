#!/usr/bin/env python3
"""Rebadge validate_cycle2576.py -> validate_cycle2577.py (match-path; DRIFT-#34 verification-15 candidate).

Per the c2576 Next block: sed 2576->2577 + docstring verification-14->15 bump +
chain insert c2576 = verification 14 before the c2575 citation +
rebadged-from 2575->2576 + P-HIST WATCH (expect exactly 2 intentional 2576 refs).
REBADGE LESSON (c2573 incident, applied first-pass four cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS pre-patch.
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2576.py"
DST = "/home/z/my-project/scripts/validate_cycle2577.py"

text = open(SRC).read()

# 1) global sed 2576->2577
text = text.replace("2576", "2577")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#34 verification-14 CARRY (post-loss rebadge lineage): "
          "rebadged from validate_cycle2575.py")
p1_new = ("DRIFT-#34 verification-15 CARRY (post-loss rebadge lineage): "
          "rebadged from validate_cycle2576.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) chain-head bump: c2577 = verification 14 -> 15 (post-sed state)
ch_old = "c2577 = verification 14\n"
ch_new = "c2577 = verification 15\n"
c = text.count(ch_old)
assert c == 1, f"chain-head pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

# 4) chain insert: c2576 = verification 14 before the c2575 citation
ci_old = "(c2575 = verification 13;"
ci_new = "(c2576 = verification 14; c2575 = verification 13;"
c = text.count(ci_old)
assert c == 1, f"chain-insert pre-patch count != 1: {c}"
text = text.replace(ci_old, ci_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2576 references post-rebadge
sites = [m.start() for m in re.finditer("2576", text)]
print(f"P-HIST 2576 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2576 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
