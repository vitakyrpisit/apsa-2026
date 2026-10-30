#!/usr/bin/env python3
"""Diff-verify post-check for the c2810 rebadge (v109 -> v110).

Diffs validate_cycle2809.py against validate_cycle2810.py line-by-line,
counts changed lines + hunks, and verifies EVERY changed line falls inside
the expected patch regions (the region table MEASURED against the actual
v110 bytes pre-run — the c2800 region-table pre-run lesson re-armed: the
c2806 attempt-1 coordinate-class CONTAINMENT_FAIL lesson honored: removed
lines live in v109 coordinates, added lines in v110 coordinates — validate
each side in its own coordinates).
"""
import difflib
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2809.py"
DST = "/home/z/my-project/scripts/validate_cycle2810.py"

a = open(SRC, encoding="utf-8").read().splitlines()
b = open(DST, encoding="utf-8").read().splitlines()

sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
removed, added, hunks = [], [], 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    hunks += 1
    removed.extend(range(i1 + 1, i2 + 1))
    added.extend(range(j1 + 1, j2 + 1))

print(f"changed_lines: removed={len(removed)} added={len(added)} total={len(removed) + len(added)} hunks={hunks}")
print(f"removed_lines={removed}")
print(f"added_lines={added}")


# region tables MEASURED against BOTH sides' actual bytes (the attempt-1
# coordinate-class lesson: removed lines live in v109 coordinates, added
# lines in v110 coordinates — validate each side in its own coordinates).
def measure_regions(lines, cycle_const, raw_name, pretty_name, gate_tag):
    r = {}
    for n, line in enumerate(lines, 1):
        if cycle_const in line:
            r.setdefault("cycle", n)
        if raw_name in line:
            r.setdefault("raw", n)
        if pretty_name in line:
            r.setdefault("pretty", n)
        if "SIZE_BAND = (446, 447)" in line:
            r.setdefault("size_band", n)
        if "Baseline gates are CLASSIFICATION gates" in line:
            r.setdefault("contract", n)
        if "# --- classification gates (SOFT" in line:
            r.setdefault("soft_comment", n)
        if f'check("drift49_pass{gate_tag}_match"' in line:
            r.setdefault("gate", n)
        if f'classification = "DRIFT-#49 pass-{gate_tag}' in line:
            r.setdefault("block", n)
    return r


regions_v110 = measure_regions(b, "CYCLE = 2810", "scan_cycle2810_raw.json",
                               'PRETTY = "/home/z/my-project/scripts/scan_cycle2810.json"', "59")
regions_v109 = measure_regions(a, "CYCLE = 2809", "scan_cycle2809_raw.json",
                               'PRETTY = "/home/z/my-project/scripts/scan_cycle2809.json"', "58")
print(f"region_table_v110_measured={regions_v110}")
print(f"region_table_v109_measured={regions_v109}")


def span(lines, start_anchor, end_anchor):
    i_s = next((n for n, l in enumerate(lines, 1) if start_anchor in l), None)
    if i_s is None:
        return None
    i_e = next((n for n, l in enumerate(lines[i_s:], i_s) if end_anchor in l), None)
    return (i_s, i_e) if i_e else None


def allowed_set(lines, regions, title_cycle, evid_tag, class_tag):
    allowed = set()
    p1 = next((n for n, l in enumerate(lines, 1) if f'"""Validator for cycle {title_cycle}' in l), None)
    p2 = span(lines, f"DRIFT-#49 pass-{class_tag} CLASS (movement repeat-class on tuple match)",
              "(the v45 76/76 off-by-one class is retired).")
    p3 = span(lines, f"DRIFT-#49 pass-{evid_tag} evidence (on disk):", "the scam block 18 stands). The")
    if p1:
        allowed.add(p1)
    if p2:
        allowed.update(range(p2[0], p2[1] + 1))
    if p3:
        allowed.update(range(p3[0], p3[1] + 1))
    if regions.get("size_band"):
        allowed.add(regions["size_band"])
    for key in ("contract", "cycle", "raw", "pretty", "soft_comment", "gate"):
        if regions.get(key):
            allowed.add(regions[key])
    blk = regions.get("block")
    if blk:
        for n in range(blk, blk + 3):
            if n <= len(lines) and f'DRIFT-#49 pass-{class_tag}' in lines[n - 1]:
                allowed.add(n)
    return allowed


# v110: class tag 59 (P2/P10/P11), evidence tag 58 (P3 heading)
allowed_v110 = allowed_set(b, regions_v110, "2810", "58", "59")
# v109: class tag 58 (P2/P10/P11), evidence tag 57 (P3 heading)
allowed_v109 = allowed_set(a, regions_v109, "2809", "57", "58")
print(f"allowed_v110_lines={sorted(allowed_v110)}")
print(f"allowed_v109_lines={sorted(allowed_v109)}")

stray_added = [n for n in sorted(set(added)) if n not in allowed_v110]
stray_removed = [n for n in sorted(set(removed)) if n not in allowed_v109]
print(f"stray_added_lines={stray_added}")
print(f"stray_removed_lines={stray_removed}")
stray = stray_added + stray_removed
if stray:
    print("DIFF_VERIFY_RED: changed lines outside the expected patch regions")
    sys.exit(1)
print(f"DIFF_VERIFY_GREEN: {len(removed) + len(added)} changed lines "
      f"({len(removed)} removed + {len(added)} added, {hunks} hunks) every changed "
      f"line inside the expected patch regions")
sys.exit(0)
