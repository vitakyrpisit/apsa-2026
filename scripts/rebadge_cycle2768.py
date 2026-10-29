#!/usr/bin/env python3
"""Rebadge gate for cycle 2768: validate_cycle2767.py -> validate_cycle2768.py.

The REBADGE-CLASS continues (the v67 source survived on disk and in the
e641a22 commit object — object-verified at guard time). Every patch asserts
its old string occurs EXACTLY once in the source BEFORE any mutation;
abort = zero files written. Post-patch: selective no-old-token assertions +
py_compile. Patch count is counted programmatically.
DRIFT-#49 pass-17 spec (per the c2767 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat recorded at
c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at c2756;
pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758; pass-8
repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10 repeat
recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat recorded
at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded at
c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded at c2767);
a repeat -> pass-17 recorded (movement repeat-class, the DRIFT-#48 root
(20,0,2,18,0) remains LOCKED, never rewritten); a return to (20,0,2,18,0)
-> the RESTORATION event recorded (the root stands, the pass-1 excursion
closes as a transient); any other composition -> newest-observation evidence
with the full delta chain printed.
The SIZE_BAND band-name lag-1 pattern carried: the v67 source carries
'pass-15 band' — this rebadge's P8 old-string expects the lag, not the class
name (the c2761 attempt-1 P8 RED lesson, applied cleanly at
c2762/c2763/c2764/c2765/c2766/c2767).
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2767.py"
DST = "/home/z/my-project/scripts/validate_cycle2768.py"

PATCHES = [
    # P1 title
    ('"""Validator for cycle 2767.',
     '"""Validator for cycle 2768.'),
    # P2 class/provenance paragraph
    ('''DRIFT-#49 pass-16 CLASS (movement repeat-class on tuple match) — sed-rebadge
from the v66 pass-15 carry (the v66 source survived on disk and in the
bc701a6 commit object, so the REBADGE-CLASS continues). Baseline for c2767 = the
DRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first
market movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat
recorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at
c2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;
pass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10
repeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat
recorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded
at c2765; pass-15 repeat recorded at c2766); a repeat records pass-16
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,
never rewritten); a return to (20,0,2,18,0) records the RESTORATION event
(the root stands, the pass-1 excursion closes as a transient); any other
composition records newest-observation evidence with the full delta chain
printed. Structural conventions inherited from the v66 class (itself
inheriting the v65/v64/v63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/
v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY
(the v45 76/76 off-by-one class is retired).''',
     '''DRIFT-#49 pass-17 CLASS (movement repeat-class on tuple match) — sed-rebadge
from the v67 pass-16 carry (the v67 source survived on disk and in the
e641a22 commit object, so the REBADGE-CLASS continues). Baseline for c2768 = the
DRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first
market movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat
recorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at
c2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;
pass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10
repeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat
recorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded
at c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded
at c2767); a repeat records pass-17
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,
never rewritten); a return to (20,0,2,18,0) records the RESTORATION event
(the root stands, the pass-1 excursion closes as a transient); any other
composition records newest-observation evidence with the full delta chain
printed. Structural conventions inherited from the v67 class (itself
inheriting the v66/v65/v64/v63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/
v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY
(the v45 76/76 off-by-one class is retired).'''),
    # P3 evidence paragraph
    ('''DRIFT-#49 pass-15 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed
at c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/
c2764/c2765/c2766 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total
20->18, honest_free 2->0, the two honest-free tasks EXITED the market;
pass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;
pass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;
pass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;
pass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at
c2764; pass-14 repeats at c2765; pass-15 repeats at c2766, movement
repeat-class — the scam block 18 stands). The''',
     '''DRIFT-#49 pass-16 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed
at c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/
c2764/c2765/c2766/c2767 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total
20->18, honest_free 2->0, the two honest-free tasks EXITED the market;
pass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;
pass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;
pass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;
pass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at
c2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats
at c2767, movement
repeat-class — the scam block 18 stands). The'''),
    # P4 contract sentence
    ('''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-16 recorded,
movement repeat-class; return to the DRIFT-#48 root -> RESTORATION recorded; any''',
     '''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-17 recorded,
movement repeat-class; return to the DRIFT-#48 root -> RESTORATION recorded; any'''),
    # P5 cycle constant
    ("CYCLE = 2767", "CYCLE = 2768"),
    # P6/P7 paths
    ('RAW = "/home/z/my-project/scripts/scan_cycle2767_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2768_raw.json"'),
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2767.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2768.json"'),
    # P8 size band comment (band-name follows the evidence-paragraph lag-1 pattern: pass-15 -> pass-16 while the class name moves to pass-17)
    ('SIZE_BAND = (446, 447)  # DRIFT-#49 pass-15 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766; the DRIFT-#48 root band 446B locked c2747/c2748)',
     'SIZE_BAND = (446, 447)  # DRIFT-#49 pass-16 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767; the DRIFT-#48 root band 446B locked c2747/c2748)'),
    # P9 tuple-match gate rename (pass-16 -> pass-17; the observation literal unchanged)
    ('''check("drift49_pass16_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (18,0,0,18,0)", hard=False)''',
     '''check("drift49_pass17_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (18,0,0,18,0)", hard=False)'''),
    # P10 classification comment
    ('# --- classification gates (SOFT — DRIFT-#49 pass-16 vs RESTORATION vs newest-observation) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-17 vs RESTORATION vs newest-observation) ---'),
    # P11 classification block (pass-17 / RESTORATION / newest-observation)
    ('''if comp_ok and size_ok:
    classification = "DRIFT-#49 pass-16 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"
elif comp_ok:
    classification = "DRIFT-#49 pass-16 (movement repeat-class, size drifted) - size movement noted"''',
     '''if comp_ok and size_ok:
    classification = "DRIFT-#49 pass-17 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"
elif comp_ok:
    classification = "DRIFT-#49 pass-17 (movement repeat-class, size drifted) - size movement noted"'''),
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
for token in ("CYCLE = 2767", "scan_cycle2767", "Validator for cycle 2767",
              "drift49_pass16_match", "pass-16 (movement repeat-class recorded",
              "pass-16 (movement repeat-class, size drifted"):
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
if "drift49_pass17_match" not in out or "pass-17" not in out:
    print("FAIL: pass-17 class wiring lost")
    failures.append("pass17-wiring")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2767.py -> validate_cycle2768.py (11 patches, pass-17 spec)")
