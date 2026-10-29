#!/usr/bin/env python3
"""Rebadge gate for cycle 2753: validate_cycle2752.py -> validate_cycle2753.py.

The REBADGE-CLASS continues (the v52 source survived on disk and in the
2dae73c commit object). Every patch asserts its old string occurs EXACTLY once
in the source BEFORE any mutation; abort = zero files written. Post-patch:
selective no-old-token assertions + py_compile. Patch count is counted
programmatically.
DRIFT-#49 pass-2 spec (per the c2752 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83); a repeat -> pass-2 recorded (movement repeat-class, the
DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten); a return to
(20,0,2,18,0) -> the RESTORATION event recorded (the root stands, the pass-1
excursion closes as a transient); any other composition -> newest-observation
evidence with the full delta chain printed.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2752.py"
DST = "/home/z/my-project/scripts/validate_cycle2753.py"

PATCHES = [
    # P1 title
    ('"""Validator for cycle 2752.',
     '"""Validator for cycle 2753.'),
    # P2 class/provenance paragraph
    ('''DRIFT-#48 verification-4 CLASS (record extends on tuple match) — sed-rebadge
from the v51 verification-3 carry (the v51 source survived on disk and in the
2708896 commit object, so the REBADGE-CLASS continues). Baseline for c2752 = the
DRIFT-#48 LOCKED root (20,0,2,18,0) @ 446B (locked at c2747 pass-1 / c2748 pass-2
per the c2738/c2739 two-pass precedent — the first fully disk-grounded root since
LOSS-#83); a match extends the verification record with baseline CARRY UNCHANGED;
any other composition opens DRIFT-#49 pass-1 (movement evidence only, never
rewrite). Structural conventions inherited from the v51 class (itself inheriting
the v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY (the
v45 76/76 off-by-one class is retired).''',
     '''DRIFT-#49 pass-2 CLASS (movement repeat-class on tuple match) — sed-rebadge
from the v52 pass-1 observation carry (the v52 source survived on disk and in the
2dae73c commit object, so the REBADGE-CLASS continues). Baseline for c2753 = the
DRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first
market movement since LOSS-#83); a repeat records pass-2 (movement repeat-class,
the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten); a return to
(20,0,2,18,0) records the RESTORATION event (the root stands, the pass-1
excursion closes as a transient); any other composition records
newest-observation evidence with the full delta chain printed. Structural
conventions inherited from the v52 class (itself inheriting the v51/v50/v49/v48/
v47/v113 conventions). Gate count is computed PROGRAMMATICALLY (the v45 76/76
off-by-one class is retired).'''),
    # P3 root paragraph
    ('''DRIFT-#48 root (on disk, LOCKED): five-tuple (20,0,2,18,0) @ 446B LOCKED at
c2747 pass-1 / c2748 pass-2; verification-1 = c2749 held; verification-2 = c2750
held; verification-3 = c2751 held; verification-4 = c2752 (the fourth post-root
carry). The DRIFT-#47 root (21,0,3,18,0) remains CONTEXT-CARRIED, superseded.
Tuple components: (total_tasks, honest_paid, honest_free, scam_pattern, unknown).''',
     '''DRIFT-#49 pass-1 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed
at c2752 (pass-1 opens — the first market movement since LOSS-#83: total 20->18,
honest_free 2->0, the two honest-free tasks EXITED the market; the scam block 18
stands). The DRIFT-#48 root (20,0,2,18,0) @ 446B remains LOCKED at c2747 pass-1 /
c2748 pass-2 (verification series 1-4 = c2749/c2750/c2751/c2752 held) — pass-1
never rewrites; the DRIFT-#47 root (21,0,3,18,0) remains CONTEXT-CARRIED,
superseded. Tuple components: (total_tasks, honest_paid, honest_free,
scam_pattern, unknown).'''),
    # P4 contract sentence
    ('''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#48 verification-4
record extends, baseline CARRY UNCHANGED; any other composition/size -> DRIFT-#49
pass-1 opened, movement evidence recorded, archive still written — pass-1 never
rewrites the root).''',
     '''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-2 recorded,
movement repeat-class; return to the DRIFT-#48 root -> RESTORATION recorded; any
other composition/size -> newest-observation evidence with the full delta chain
printed, archive still written — the root is never rewritten).'''),
    # P5 cycle constant
    ("CYCLE = 2752", "CYCLE = 2753"),
    # P6/P7 paths
    ('RAW = "/home/z/my-project/scripts/scan_cycle2752_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2753_raw.json"'),
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2752.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2753.json"'),
    # P8 size band comment
    ('SIZE_BAND = (446, 447)  # DRIFT-#48 root band @ 446B (locked c2747/c2748; ver-1..3 held c2749/c2750/c2751)',
     'SIZE_BAND = (446, 447)  # DRIFT-#49 pass-1 band @ 446B (observed c2752; the DRIFT-#48 root band 446B locked c2747/c2748)'),
    # P9 baseline constants (pass-2 spec: baseline flips to the pass-1 observation;
    # the DRIFT-#48 root kept as DRIFT48_ROOT for the RESTORATION check)
    ('''BASELINE_COMP = {"total": 20, "honest_paid": 0, "honest_free": 2,
                 "scam": 18, "unknown": 0}''',
     '''BASELINE_COMP = {"total": 18, "honest_paid": 0, "honest_free": 0,
                 "scam": 18, "unknown": 0}
DRIFT48_ROOT = {"total": 20, "honest_paid": 0, "honest_free": 2,
                "scam": 18, "unknown": 0}'''),
    # P10 classification comment
    ('# --- classification gates (SOFT — DRIFT-#48 verification-4 vs DRIFT-#49 pass-1) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-2 vs RESTORATION vs newest-observation) ---'),
    # P11 tuple-match gate rename (baseline detail flips to the pass-1 observation)
    ('''check("drift48_ver4_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (20,0,2,18,0)", hard=False)''',
     '''check("drift49_pass2_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (18,0,0,18,0)", hard=False)'''),
    # P12 classification block (pass-2 / RESTORATION / newest-observation)
    ('''if comp_ok and size_ok:
    classification = "DRIFT-#48 verification-4 (record extends; baseline CARRY UNCHANGED)"
elif comp_ok:
    classification = "DRIFT-#48 verification-4 (tuple match, size drifted) - size movement noted"
else:
    classification = "DRIFT-#49 PASS-1 (movement evidence recorded; root NOT rewritten)"''',
     '''restoration_ok = comp == DRIFT48_ROOT
if comp_ok and size_ok:
    classification = "DRIFT-#49 pass-2 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"
elif comp_ok:
    classification = "DRIFT-#49 pass-2 (movement repeat-class, size drifted) - size movement noted"
elif restoration_ok and size_ok:
    classification = "RESTORATION (the DRIFT-#48 root stands; the pass-1 excursion closes as a transient)"
elif restoration_ok:
    classification = "RESTORATION (the DRIFT-#48 root stands; size drifted) - size movement noted"
else:
    classification = "DRIFT-#49 newest-observation evidence (full delta chain via recursive_diff; root NOT rewritten)"'''),
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
for token in ("CYCLE = 2752", "scan_cycle2752", "Validator for cycle 2752",
              "drift48_ver4_match", "verification-4"):
    if token in out:
        print(f"FAIL: old token remains: {token}")
        failures.append(token)
if "(20,0,2,18,0)" not in out:
    print("FAIL: locked-root reference lost")
    failures.append("root-reference")
if "(21,0,3,18,0)" not in out:
    print("FAIL: context-carried superseded root reference lost")
    failures.append("superseded-root-reference")
if "(18,0,0,18,0)" not in out:
    print("FAIL: pass-1 observation baseline reference lost")
    failures.append("pass1-observation-reference")
if "DRIFT48_ROOT" not in out or "restoration_ok" not in out:
    print("FAIL: RESTORATION gate wiring lost")
    failures.append("restoration-wiring")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2752.py -> validate_cycle2753.py (12 patches, pass-2 spec)")
