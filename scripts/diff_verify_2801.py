#!/usr/bin/env python3
"""Ghost diff-verify for the v100 -> v101 rebadge (untracked, foreign-absorption).

Prints the changed-line table between validate_cycle2800.py (v100) and
validate_cycle2801.py (v101) and verifies every changed line falls inside the
eleven expected patch regions (the region table MEASURED against the actual
v101 bytes pre-run). rc=0 iff containment holds.
"""
import difflib
import sys

A = "/home/z/my-project/scripts/validate_cycle2800.py"
B = "/home/z/my-project/scripts/validate_cycle2801.py"

a = open(A, encoding="utf-8").read().splitlines()
b = open(B, encoding="utf-8").read().splitlines()
sm = difflib.SequenceMatcher(None, a, b)
removed, added = [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "delete":
        removed += list(range(i1 + 1, i2 + 1))
    elif tag == "insert":
        added += list(range(j1 + 1, j2 + 1))
    elif tag == "replace":
        removed += list(range(i1 + 1, i2 + 1))
        added += list(range(j1 + 1, j2 + 1))

print(f"changed lines: {len(removed)} removed + {len(added)} added "
      f"= {len(removed) + len(added)} total")
print(f"removed={removed}")
print(f"added={added}")

# hunks (coalesced spans over the union of changed lines in B coordinates)
spans = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        if spans and j1 + 1 <= spans[-1][1] + 1:
            spans[-1] = (spans[-1][0], j2)
        else:
            spans.append((j1 + 1, j2))
print(f"hunks={len(spans)} spans={spans}")

# expected regions in the v101 (B) coordinates — docstring +2 shift class:
# the P2 chain insert (+1 line) and the P3 chain insert (+1 line) shift the
# code below the docstring by +2 vs the v100 region table.
EXPECTED = [
    (2, 60),      # P1/P2 docstring title+provenance (the big P2 paragraph)
    (56, 105),    # P3 evidence paragraph (overlaps the P2 docstring band)
    (109, 111),   # P4 contract line (the docstring Contract paragraph, MEASURED at 110)
    (119, 123),   # P5 CYCLE / P6 RAW / P7 PRETTY / P8 SIZE_BAND
    (221, 221),   # P10 SOFT comment
    (225, 225),   # P9 gate rename line
    (228, 232),   # P11 classification block (both branches MEASURED at 230/232)
]
bad = []
for ln in added:
    if not any(lo <= ln <= hi for lo, hi in EXPECTED):
        bad.append(ln)
if bad:
    print(f"CONTAINMENT_FAIL: added lines outside expected regions: {bad}")
    sys.exit(1)
print("CONTAINMENT_OK: every changed line inside the expected patch regions")
sys.exit(0)
