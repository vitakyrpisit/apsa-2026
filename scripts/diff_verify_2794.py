#!/usr/bin/env python3
"""Diff-verification post-check for the v93->v94 rebadge (the c2793 precedent):
counts changed lines / hunks via difflib.unified_diff and asserts every changed
line number falls inside the eleven expected patch regions (P1 title / P2
provenance / P3 evidence / P4 contract / P5 CYCLE / P6-P7 paths / P8 band /
P9 gate / P10 comment / P11 block). Ghost-class instrument (untracked, the
foreign-absorption path like gen_rebadge_2794.py)."""
import difflib
import re
import sys

a = open("/home/z/my-project/scripts/validate_cycle2793.py", encoding="utf-8").read().splitlines(keepends=True)
b = open("/home/z/my-project/scripts/validate_cycle2794.py", encoding="utf-8").read().splitlines(keepends=True)

hunks = []
rem = add = 0
cur = None
for line in difflib.unified_diff(a, b, n=0):
    if line.startswith("@@"):
        cur = {"hunk": line.strip(), "old": [], "new": []}
        hunks.append(cur)
    elif line.startswith("-") and cur is not None:
        rem += 1
        cur["old"].append(line[1:].rstrip("\n"))
    elif line.startswith("+") and cur is not None:
        add += 1
        cur["new"].append(line[1:].rstrip("\n"))

print(f"changed_lines={rem + add} ({rem} removed + {add} added, {len(hunks)} hunks)")
for h in hunks:
    print(f"  {h['hunk']}")

# expected regions (v94 line numbers, 1-indexed, inclusive — the two
# docstring insertions P2-t5/P3-t3 shift every v93 line >= 94 by +2; the
# P1/P2 boundary is merged because difflib block-replaces the adjacent lines)
REGIONS = [
    ("P1 title + P2 provenance", 2, 50), ("P3 evidence", 51, 93),
    ("P4 contract", 94, 98), ("P5 CYCLE", 104, 106), ("P6 raw path", 107, 107),
    ("P7 pretty path", 108, 108), ("P8 band", 109, 109), ("P10 comment", 205, 208),
    ("P9 gate", 209, 214), ("P11 block", 215, 222),
]
in_region = lambda n: any(lo <= n <= hi for _, lo, hi in REGIONS)

bad = []
for h in hunks:
    m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", h["hunk"])
    start = int(m.group(1))
    for k in range(len(h["new"])):
        n = start + k
        if not in_region(n):
            bad.append((h["hunk"], n, h["new"][k][:60]))

if bad:
    print(f"DIFF_VERIFY_RED: {len(bad)} stray changed lines outside the 11 regions:")
    for hunk, n, txt in bad:
        print(f"  {hunk} line {n}: {txt!r}")
    sys.exit(1)
print("DIFF_VERIFY_GREEN: every changed line inside the eleven expected patch regions (no stray edits)")
