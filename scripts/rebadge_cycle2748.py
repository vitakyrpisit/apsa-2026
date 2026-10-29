#!/usr/bin/env python3
"""Rebadge gate for cycle 2748: validate_cycle2747.py -> validate_cycle2748.py.

The REBADGE-CLASS resumes this cycle (the v47 source survived LOSS-#83 on disk
and in the 9fd8152 commit object). Every patch asserts its old string occurs
EXACTLY once in the source BEFORE any mutation; abort = zero files written.
Post-patch: selective no-old-token assertions + py_compile. Patch count is
counted programmatically. DRIFT-#48 pass-2 spec: baseline = the c2747 pass-1
tuple (20,0,2,18,0); a repeat locks the new-root candidate; any other
composition continues pass-1 (movement evidence only, never rewrite).
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2747.py"
DST = "/home/z/my-project/scripts/validate_cycle2748.py"

PATCHES = [
    # P1 title
    ('"""Validator for cycle 2747.',
     '"""Validator for cycle 2748.'),
    # P2 class/provenance paragraph
    ('''DRIFT-#47 verification-9 CLASS (record extends on tuple match) — REBUILT-FROM-CONTEXT
post-LOSS-#83: the v46 source (validate_cycle2746.py) and the entire c2736..c2746
corpus were WIPED by the LOSS EVENT #83 snapshot rollback (environment re-provisioned
2026-10-29 ~16:01 UTC to the post-LOSS-#79-recon state). This validator is a FRESH
reconstruction implementing the context-carried DRIFT-#47 verification-9 gate; it is
NOT a byte-exact rebadge (the rebadge source does not exist on disk). Structural
conventions inherited from the disk-surviving validate_cycle2735.py (v113-class,
DRIFT-#45 verification-113 carry). Gate count is computed PROGRAMMATICALLY (the
v45 76/76 off-by-one class is retired).''',
     '''DRIFT-#48 pass-2 CLASS (LOCK candidate on tuple repeat) — sed-rebadge from the
v47 REBUILT-FROM-CONTEXT carry (validate_cycle2746.py and the c2736..c2746 corpus
remain WIPED by LOSS EVENT #83; the v47 source survived on disk and in the 9fd8152
commit object, so the REBADGE-CLASS resumes). Baseline for c2748 = the DRIFT-#48
pass-1 tuple (the c2747 capture, on disk); a repeat locks the new-root candidate
per the c2738/c2739 precedent; any other composition continues pass-1 (movement
evidence only, never rewrite). Structural conventions inherited from the v47 class
(itself inheriting the disk-surviving v113 conventions). Gate count is computed
PROGRAMMATICALLY (the v45 76/76 off-by-one class is retired).'''),
    # P3 root paragraph
    ('''DRIFT-#47 root (CONTEXT-CARRIED): five-tuple (21,0,3,18,0) @ 446B LOCKED at
c2738 pass-1 / c2739 pass-2; verifications 1-8 = c2738..c2746, all honest_paid=0
(context-carried; disk record lost). Tuple components:
(total_tasks, honest_paid, honest_free, scam_pattern, unknown).''',
     '''DRIFT-#48 pass-1 tuple (the c2747 capture, on disk): five-tuple (20,0,2,18,0)
@ 446B. The DRIFT-#47 root (21,0,3,18,0) LOCKED at c2738/c2739 remains
CONTEXT-CARRIED (verifications 1-8 = c2738..c2746, all honest_paid=0; the disk
record was lost to LOSS EVENT #83). Tuple components:
(total_tasks, honest_paid, honest_free, scam_pattern, unknown).'''),
    # P4 contract sentence
    ('''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#47 verification-9 record
extends; any other composition/size -> DRIFT-#48 pass-1 opened, movement evidence
recorded, archive still written — pass-1 never rewrites the root).''',
     '''Baseline gates are CLASSIFICATION gates (repeat -> DRIFT-#48 pass-2 LOCK
candidate; any other composition/size -> pass-1 continues, movement evidence
recorded, archive still written — the two-pass law never rewrites mid-stream).'''),
    # P5 cycle constant
    ("CYCLE = 2747", "CYCLE = 2748"),
    # P6/P7 paths
    ('RAW = "/home/z/my-project/scripts/scan_cycle2747_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2748_raw.json"'),
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2747.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2748.json"'),
    # P8 size band comment
    ('SIZE_BAND = (446, 447)  # context-carried DRIFT-#47 band @ 446B',
     'SIZE_BAND = (446, 447)  # DRIFT-#47-carried band @ 446B (held through the #48 pass-1)'),
    # P9 baseline composition
    ('''BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 3,
                 "scam": 18, "unknown": 0}''',
     '''BASELINE_COMP = {"total": 20, "honest_paid": 0, "honest_free": 2,
                 "scam": 18, "unknown": 0}'''),
    # P10 classification comment
    ('# --- classification gates (SOFT — DRIFT-#47 verification-9 vs DRIFT-#48 pass-1) ---',
     '# --- classification gates (SOFT — DRIFT-#48 pass-2 LOCK candidate vs pass-1 continues) ---'),
    # P11 tuple-match gate rename + expected tuple
    ('''check("drift47_tuple_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (21,0,3,18,0)", hard=False)''',
     '''check("drift48_tuple_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (20,0,2,18,0)", hard=False)'''),
    # P12a/b/c classification strings
    ('classification = "DRIFT-#47 verification-9 (record extends, eighth post-root carry; baseline CARRY UNCHANGED)"',
     'classification = "DRIFT-#48 PASS-2 LOCK CANDIDATE (tuple repeat; new root (20,0,2,18,0) @ 446B per the c2738/c2739 precedent)"'),
    ('classification = "DRIFT-#47 verification-9 (tuple match, size drifted) - size movement noted"',
     'classification = "DRIFT-#48 PASS-2 candidate (tuple repeat, size drifted) - size movement noted"'),
    ('classification = "DRIFT-#48 PASS-1 (movement evidence recorded; root NOT rewritten)"',
     'classification = "DRIFT-#48 PASS-1 CONTINUES (composition moved again; movement evidence only)"'),
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
for token in ("CYCLE = 2747", "scan_cycle2747", "Validator for cycle 2747",
              "drift47_tuple_match"):
    if token in out:
        print(f"FAIL: old token remains: {token}")
        failures.append(token)
if "(21,0,3,18,0)" not in out:
    print("FAIL: context-carried root reference lost")
    failures.append("root-reference")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2747.py -> validate_cycle2748.py (14 patches, pass-2 spec)")
