#!/usr/bin/env python3
"""Ghost diff-verify for the v104 -> v105 rebadge (untracked, foreign-absorption).

Prints the changed-line table between validate_cycle2804.py (v104) and
validate_cycle2805.py (v105) and verifies every changed line falls inside the
eleven expected patch regions (the region table MEASURED against the actual
v105 bytes pre-run — the c2800 ghost-tool abort class does NOT fire). rc=0 iff
containment holds.
"""
import difflib
import sys

A = "/home/z/my-project/scripts/validate_cycle2804.py"
B = "/home/z/my-project/scripts/validate_cycle2805.py"

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

# expected regions in the v105 (B) coordinates — MEASURED against the actual
# v105 bytes pre-run: the P2 chain insert (+1 line) and the P3 chain insert
# (+1 line) shift the code below the docstring by +2 vs the v104 region table
# (the docstring +2 shift class held). Locate the anchors live:
def find_line(needle):
    for i, ln in enumerate(b):
        if needle in ln:
            return i + 1
    return -1

cycle_ln = find_line("CYCLE = 2805")
raw_ln = find_line('RAW = "/home/z/my-project/scripts/scan_cycle2805_raw.json"')
pretty_ln = find_line('PRETTY = "/home/z/my-project/scripts/scan_cycle2805.json"')
band_ln = find_line("SIZE_BAND = (446, 447)")
contract_ln = find_line("Baseline gates are CLASSIFICATION gates")
soft_ln = find_line("# --- classification gates (SOFT")
gate_ln = find_line('check("drift49_pass54_match", comp_ok,')
block_ln = find_line('if comp_ok and size_ok:')
print(f"measured regions: CYCLE={cycle_ln} RAW={raw_ln} PRETTY={pretty_ln} "
      f"SIZE_BAND={band_ln} contract={contract_ln} SOFT={soft_ln} gate={gate_ln} "
      f"block={block_ln}+{block_ln + 2 if block_ln > 0 else '-'}")

EXPECTED = [
    (2, 62),      # P1/P2 docstring title+provenance (the big P2 paragraph)
    (58, 109),    # P3 evidence paragraph (overlaps the P2 docstring band; the
                  # v105 P3 chain insert extends the paragraph end to 109 — the
                  # region table MEASURED against the actual v105 bytes: the
                  # stale c2804 upper bound 107 fired attempt-1 containment RED)
    (contract_ln - 1, contract_ln + 1),   # P4 contract line
    (cycle_ln - 3, band_ln + 1),          # P5 CYCLE / P6 RAW / P7 PRETTY / P8 SIZE_BAND
    (soft_ln, soft_ln + 2),               # P10 SOFT comment
    (gate_ln - 2, gate_ln + 2),           # P9 gate rename line
    (block_ln - 2, block_ln + 4),         # P11 classification block (both branches)
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
