#!/usr/bin/env python3
"""Rebadge validate_cycle2606.py -> validate_cycle2607.py (DRIFT-#42 verification-2, match-path).

Per the c2606 Next block: sed 2606->2607 + header DRIFT-#42 ROOT -> verification-2 CARRY
bump (rebadged-from 2605->2606) + chain insert c2607 = DRIFT-#42 verification 2 + line-8
bump + P-HIST WATCH (expect exactly 2 intentional 2606 refs post-rebadge; 2605, 2604,
2603, 2602, 2601, 2600, 2599, 2598, 2597, 2596, 2595 and 2594 keep 1 each — chain history;
2594 is the DRIFT-#41 closure root cite).
REBADGE LESSON (c2573 incident, applied first-pass thirty-four cycles running): the P1
patch pattern must match the source-file name AS IT EXISTS post-sed — post-sed the
header still names validate_cycle2605.py (unmigrated by the sed).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#42 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2607 = DRIFT-#42 verification 2, the
root extends 1-fold -> 2-fold (five-tuple (22,0,1,18,3) reproduced @ 446B). Any
five-tuple move = DRIFT-#43 declaration (two-pass).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2606.py"
DST = "/home/z/my-project/scripts/validate_cycle2607.py"

text = open(SRC).read()

# 1) global sed 2606->2607
text = text.replace("2606", "2607")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#42 ROOT DECLARED (2026-10-27 ~04:07 +08): rebadged from validate_cycle2605.py")
p1_new = ("DRIFT-#42 verification-2 CARRY (root declared 2026-10-27 ~04:07 +08): "
          "rebadged from validate_cycle2606.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump
l8_old = "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2607 = DRIFT-#42 verification 1"
l8_new = "(22,0,1,18,3) @ 446B DRIFT-#42 root; c2607 = DRIFT-#42 verification 2"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain-head bump + chain insert in ONE patch
ch_old = "(c2607 = DRIFT-#42 verification 1, ROOT — the movement: total 23->22 (-1), "
ch_new = ("(c2607 = DRIFT-#42 verification 2; c2606 = DRIFT-#42 verification 1, ROOT — "
          "the movement: total 23->22 (-1), ")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2606 references post-rebadge
# (rebadged-from header + chain insert); 2605..2594 keep 1 each (chain history).
sites_06 = [m.start() for m in re.finditer("2606", text)]
sites_05 = [m.start() for m in re.finditer("2605", text)]
sites_04 = [m.start() for m in re.finditer("2604", text)]
sites_03 = [m.start() for m in re.finditer("2603", text)]
sites_02 = [m.start() for m in re.finditer("2602", text)]
sites_01 = [m.start() for m in re.finditer("2601", text)]
sites_00 = [m.start() for m in re.finditer("2600", text)]
sites_99 = [m.start() for m in re.finditer("2599", text)]
sites_98 = [m.start() for m in re.finditer("2598", text)]
sites_97 = [m.start() for m in re.finditer("2597", text)]
sites_96 = [m.start() for m in re.finditer("2596", text)]
sites_95 = [m.start() for m in re.finditer("2595", text)]
sites_94 = [m.start() for m in re.finditer("2594", text)]
print(f"P-HIST 2606 refs = {len(sites_06)}")
for s in sites_06:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
print(f"P-HIST 2605 refs = {len(sites_05)} (chain history)")
print(f"P-HIST 2604 refs = {len(sites_04)} (chain history)")
print(f"P-HIST 2603 refs = {len(sites_03)} (chain history)")
print(f"P-HIST 2602 refs = {len(sites_02)} (chain history)")
print(f"P-HIST 2601 refs = {len(sites_01)} (chain history)")
print(f"P-HIST 2600 refs = {len(sites_00)} (chain history)")
print(f"P-HIST 2599 refs = {len(sites_99)} (chain history)")
print(f"P-HIST 2598 refs = {len(sites_98)} (chain history)")
print(f"P-HIST 2597 refs = {len(sites_97)} (chain history)")
print(f"P-HIST 2596 refs = {len(sites_96)} (chain history)")
print(f"P-HIST 2595 refs = {len(sites_95)} (chain history)")
print(f"P-HIST 2594 refs = {len(sites_94)} (chain history)")
if len(sites_06) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2606 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
