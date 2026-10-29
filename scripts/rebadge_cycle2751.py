#!/usr/bin/env python3
"""Rebadge gate for cycle 2751: validate_cycle2750.py -> validate_cycle2751.py.

The REBADGE-CLASS continues (the v50 source survived on disk and in the 113dbc1
commit object). Every patch asserts its old string occurs EXACTLY once in the
source BEFORE any mutation; abort = zero files written. Post-patch: selective
no-old-token assertions + py_compile. Patch count is counted programmatically.
DRIFT-#48 verification-3 spec: baseline = the LOCKED root (20,0,2,18,0) @ 446B
(c2747 pass-1 / c2748 pass-2; verification-1 = c2749 held; verification-2 =
c2750 held); a match extends the record with baseline CARRY UNCHANGED; any
other composition opens DRIFT-#49 pass-1 (movement evidence only, never
rewrite). The baseline VALUES are unchanged from v50 (the root carried).
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2750.py"
DST = "/home/z/my-project/scripts/validate_cycle2751.py"

PATCHES = [
    # P1 title
    ('"""Validator for cycle 2750.',
     '"""Validator for cycle 2751.'),
    # P2 class/provenance paragraph
    ('''DRIFT-#48 verification-2 CLASS (record extends on tuple match) — sed-rebadge
from the v49 verification-1 carry (the v49 source survived on disk and in the
bfc3579 commit object, so the REBADGE-CLASS continues). Baseline for c2750 = the
DRIFT-#48 LOCKED root (20,0,2,18,0) @ 446B (locked at c2747 pass-1 / c2748 pass-2
per the c2738/c2739 two-pass precedent — the first fully disk-grounded root since
LOSS-#83); a match extends the verification record with baseline CARRY UNCHANGED;
any other composition opens DRIFT-#49 pass-1 (movement evidence only, never
rewrite). Structural conventions inherited from the v49 class (itself inheriting
the v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY (the v45
76/76 off-by-one class is retired).''',
     '''DRIFT-#48 verification-3 CLASS (record extends on tuple match) — sed-rebadge
from the v50 verification-2 carry (the v50 source survived on disk and in the
113dbc1 commit object, so the REBADGE-CLASS continues). Baseline for c2751 = the
DRIFT-#48 LOCKED root (20,0,2,18,0) @ 446B (locked at c2747 pass-1 / c2748 pass-2
per the c2738/c2739 two-pass precedent — the first fully disk-grounded root since
LOSS-#83); a match extends the verification record with baseline CARRY UNCHANGED;
any other composition opens DRIFT-#49 pass-1 (movement evidence only, never
rewrite). Structural conventions inherited from the v50 class (itself inheriting
the v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY (the
v45 76/76 off-by-one class is retired).'''),
    # P3 root paragraph
    ('''DRIFT-#48 root (on disk, LOCKED): five-tuple (20,0,2,18,0) @ 446B LOCKED at
c2747 pass-1 / c2748 pass-2; verification-1 = c2749 held; verification-2 = c2750
(the second post-root carry). The DRIFT-#47 root (21,0,3,18,0) remains
CONTEXT-CARRIED, superseded. Tuple components:
(total_tasks, honest_paid, honest_free, scam_pattern, unknown).''',
     '''DRIFT-#48 root (on disk, LOCKED): five-tuple (20,0,2,18,0) @ 446B LOCKED at
c2747 pass-1 / c2748 pass-2; verification-1 = c2749 held; verification-2 = c2750
held; verification-3 = c2751 (the third post-root carry). The DRIFT-#47 root
(21,0,3,18,0) remains CONTEXT-CARRIED, superseded. Tuple components:
(total_tasks, honest_paid, honest_free, scam_pattern, unknown).'''),
    # P4 contract sentence
    ('''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#48 verification-2
record extends, baseline CARRY UNCHANGED; any other composition/size -> DRIFT-#49
pass-1 opened, movement evidence recorded, archive still written — pass-1 never
rewrites the root).''',
     '''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#48 verification-3
record extends, baseline CARRY UNCHANGED; any other composition/size -> DRIFT-#49
pass-1 opened, movement evidence recorded, archive still written — pass-1 never
rewrites the root).'''),
    # P5 cycle constant
    ("CYCLE = 2750", "CYCLE = 2751"),
    # P6/P7 paths
    ('RAW = "/home/z/my-project/scripts/scan_cycle2750_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2751_raw.json"'),
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2750.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2751.json"'),
    # P8 size band comment
    ('SIZE_BAND = (446, 447)  # DRIFT-#48 root band @ 446B (locked c2747/c2748; ver-1 held c2749)',
     'SIZE_BAND = (446, 447)  # DRIFT-#48 root band @ 446B (locked c2747/c2748; ver-1..2 held c2749/c2750)'),
    # P9 classification comment
    ('# --- classification gates (SOFT — DRIFT-#48 verification-2 vs DRIFT-#49 pass-1) ---',
     '# --- classification gates (SOFT — DRIFT-#48 verification-3 vs DRIFT-#49 pass-1) ---'),
    # P10 tuple-match gate rename (expected tuple detail unchanged — the root carried)
    ('''check("drift48_ver2_match", comp_ok,''',
     '''check("drift48_ver3_match", comp_ok,'''),
    # P11a/b classification strings
    ('classification = "DRIFT-#48 verification-2 (record extends; baseline CARRY UNCHANGED)"',
     'classification = "DRIFT-#48 verification-3 (record extends; baseline CARRY UNCHANGED)"'),
    ('classification = "DRIFT-#48 verification-2 (tuple match, size drifted) - size movement noted"',
     'classification = "DRIFT-#48 verification-3 (tuple match, size drifted) - size movement noted"'),
]

src = open(SRC).read()
failures = []
for i, (old, new) in enumerate(PATCHES, 1):
    n = src.count(old)
    tag = f"P{i}"
    if n != 1:
        failures.append(f"{tag}: old string count={n} (expect 1)")
        print(f"FAIL: {tag} old-count={n}")
    else:
        print(f"ok: {tag} old-count=1")

if failures:
    print(f"REBADGE_ABORTED: {len(failures)} patch-gate failures - NO files written")
    sys.exit(1)

out = src
for old, new in PATCHES:
    out = out.replace(old, new)
open(DST, "w").write(out)

# post-patch selective assertions
for token in ("CYCLE = 2750", "scan_cycle2750", "Validator for cycle 2750",
              "drift48_ver2_match"):
    if token in out:
        print(f"FAIL: old token remains: {token}")
        failures.append(token)
if "(20,0,2,18,0)" not in out:
    print("FAIL: locked-root reference lost")
    failures.append("root-reference")
if "(21,0,3,18,0)" not in out:
    print("FAIL: context-carried superseded root reference lost")
    failures.append("superseded-root-reference")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2750.py -> validate_cycle2751.py (12 patches, verification-3 spec)")
