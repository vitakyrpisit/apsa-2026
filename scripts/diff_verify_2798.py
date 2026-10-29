#!/usr/bin/env python3
"""Diff-verification post-check for the v97->v98 rebadge (the c2797 precedent):
counts changed lines / hunks via difflib.unified_diff and asserts every changed
line number falls inside the eleven expected patch regions (P1 title / P2
provenance / P3 evidence / P4 contract / P5 CYCLE / P6-P7 paths / P8 band /
P9 gate / P10 comment / P11 block). Region edges MEASURED against the actual
v98 bytes (the c2797 measured-region-table lesson). Ghost-class instrument
(untracked, the foreign-absorption path like gen_rebadge_2798.py)."""
import difflib
import re
import sys

A = "/home/z/my-project/scripts/validate_cycle2797.py"
B = "/home/z/my-project/scripts/validate_cycle2798.py"
a = open(A, encoding="utf-8").read().splitlines(keepends=True)
b = open(B, encoding="utf-8").read().splitlines(keepends=True)

# --- measure the region anchors in the ACTUAL v98 bytes ---
def find_line(needle):
    hits = [i + 1 for i, l in enumerate(b) if needle in l]
    return hits

cy = find_line("CYCLE = 2798")
raw_l = find_line('RAW = "/home/z/my-project/scripts/scan_cycle2798_raw.json"')
pretty_l = find_line('PRETTY = "/home/z/my-project/scripts/scan_cycle2798.json"')
band_l = find_line("SIZE_BAND = (446, 447)")
p4_l = find_line("Baseline gates are CLASSIFICATION gates")
soft_l = find_line("# --- classification gates (SOFT")
gate_l = find_line('check("drift49_pass47_match"')
block_l = find_line("if comp_ok and size_ok:")
p3_end_l = find_line("repeat-class — the scam block 18 stands). The")
print(f"measured_v98_anchors: CYCLE={cy} RAW={raw_l} PRETTY={pretty_l} BAND={band_l} "
      f"P4={p4_l} SOFT={soft_l} GATE={gate_l} BLOCK={block_l} P3END={p3_end_l}")
assert len(cy) == 1 and len(raw_l) == 1 and len(pretty_l) == 1 and len(band_l) == 1 \
    and len(p4_l) == 1 and len(soft_l) == 1 and len(gate_l) == 1 \
    and len(block_l) == 1 and len(p3_end_l) == 1, "anchor not unique"
cy, raw_l, pretty_l, band_l = cy[0], raw_l[0], pretty_l[0], band_l[0]
band = band_l
p4, soft, gate, block, p3_end = p4_l[0], soft_l[0], gate_l[0], block_l[0], p3_end_l[0]

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

# expected regions (v98 line numbers, 1-indexed, inclusive — MEASURED above;
# the P1/P2 boundary is merged because difflib block-replaces the adjacent
# lines; P5/P6/P7/P8 are adjacent so their region is the CYCLE..BAND span)
REGIONS = [
    ("P1 title + P2 provenance", 2, p3_end - 1), ("P3 evidence", p3_end, p4 - 1),
    ("P4 contract", p4, p4 + 4), ("P5-P8 cycle+paths+band", cy, band),
    ("P10 comment", soft, gate - 1), ("P9 gate", gate, block - 1),
    ("P11 block", block, block + 7),
]
print("region_table:", [(t, lo, hi) for t, lo, hi in REGIONS])
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
