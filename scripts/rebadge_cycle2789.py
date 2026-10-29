#!/usr/bin/env python3
"""Rebadge gate for cycle 2789: validate_cycle2788.py -> validate_cycle2789.py.

The REBADGE-CLASS continues (the v88 source survived on disk and in the
6253361 commit object — object-verified at guard time). Every patch asserts
its old string occurs EXACTLY once in the source BEFORE any mutation;
abort = zero files written. Post-patch: selective no-old-token assertions +
py_compile. Patch count is counted programmatically.
DRIFT-#49 pass-38 spec (per the c2788 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83; pass-2 repeat recorded at c2753; ... pass-36 repeat recorded
at c2787; pass-37 repeat recorded at c2788); a repeat -> pass-38 recorded
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never
rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the
root stands, the pass-1 excursion closes as a transient); any other
composition -> newest-observation evidence with the full delta chain printed.
The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2788
attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761
attempt-1 P8 lesson): the v88 source carries 'pass-36 band' AND 'pass-36
evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class
name.
Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching):
the official c2788 commit hash 6253361 short form = 6-2-5-3-3-6-1 — it
carries NO 'c' character at all, so NO c+4-digit run is present and the
hash-artifact class does NOT fire this cycle; the v89 P2 paragraph carries
'the 6253361 commit object' (zero new hash-artifact birth), while the v88 P2
carry 'the a762125 commit object' rebadges AWAY (a762125 also carries no
'c', so zero token deaths — the c7947 class does NOT fire); the foreign TOP
ffa527c short form = f-f-a-5-2-7-c — the trailing 'c' is letter-preceded and
line-terminal, NO c+4-digit run (zero exposure), no foreign hash enters v89
source; the c2789 commit hash is unborn at patch time, checked post-commit.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2788.py"
DST = "/home/z/my-project/scripts/validate_cycle2789.py"

PATCHES = [
    # P1 title
    ('"""Validator for cycle 2788.',
     '"""Validator for cycle 2789.'),
    # P2 class/provenance paragraph
    ('''DRIFT-#49 pass-37 CLASS (movement repeat-class on tuple match) — sed-rebadge
from the v87 pass-36 carry (the v87 source survived on disk and in the
a762125 commit object, so the REBADGE-CLASS continues). Baseline for c2788 = the
DRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first
market movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat
recorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at
c2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;
pass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10
repeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat
recorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded
at c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded
at c2767; pass-17 repeat recorded
at c2768; pass-18 repeat recorded
at c2769; pass-19 repeat recorded
at c2770; pass-20 repeat recorded
at c2771; pass-21 repeat recorded
at c2772; pass-22 repeat recorded
at c2773; pass-23 repeat recorded
at c2774; pass-24 repeat recorded
at c2775; pass-25 repeat recorded
at c2776; pass-26 repeat recorded
at c2777; pass-27 repeat recorded
at c2778; pass-28 repeat recorded
at c2779; pass-29 repeat recorded
at c2780; pass-30 repeat recorded
at c2781; pass-31 repeat recorded
at c2782; pass-32 repeat recorded
at c2783; pass-33 repeat recorded
at c2784; pass-34 repeat recorded
at c2785; pass-35 repeat recorded
at c2786; pass-36 repeat recorded
at c2787); a repeat records pass-37
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,
never rewritten); a return to (20,0,2,18,0) records the RESTORATION event
(the root stands, the pass-1 excursion closes as a transient); any other
composition records newest-observation evidence with the full delta chain
printed. Structural conventions inherited from the v87 class (itself
inheriting the v86/v85/v84/v83/v82/v81/v80/v79/v78/v77/v76/v75/v74/v73/v72/v71/v70/v69/v68/v67/v66/v65/v64/
v63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY
(the v45 76/76 off-by-one class is retired).''',
     '''DRIFT-#49 pass-38 CLASS (movement repeat-class on tuple match) — sed-rebadge
from the v88 pass-37 carry (the v88 source survived on disk and in the
6253361 commit object, so the REBADGE-CLASS continues). Baseline for c2789 = the
DRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first
market movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat
recorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at
c2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;
pass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10
repeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat
recorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded
at c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded
at c2767; pass-17 repeat recorded
at c2768; pass-18 repeat recorded
at c2769; pass-19 repeat recorded
at c2770; pass-20 repeat recorded
at c2771; pass-21 repeat recorded
at c2772; pass-22 repeat recorded
at c2773; pass-23 repeat recorded
at c2774; pass-24 repeat recorded
at c2775; pass-25 repeat recorded
at c2776; pass-26 repeat recorded
at c2777; pass-27 repeat recorded
at c2778; pass-28 repeat recorded
at c2779; pass-29 repeat recorded
at c2780; pass-30 repeat recorded
at c2781; pass-31 repeat recorded
at c2782; pass-32 repeat recorded
at c2783; pass-33 repeat recorded
at c2784; pass-34 repeat recorded
at c2785; pass-35 repeat recorded
at c2786; pass-36 repeat recorded
at c2787; pass-37 repeat recorded
at c2788); a repeat records pass-38
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,
never rewritten); a return to (20,0,2,18,0) records the RESTORATION event
(the root stands, the pass-1 excursion closes as a transient); any other
composition records newest-observation evidence with the full delta chain
printed. Structural conventions inherited from the v88 class (itself
inheriting the v87/v86/v85/v84/v83/v82/v81/v80/v79/v78/v77/v76/v75/v74/v73/v72/v71/v70/v69/v68/v67/v66/v65/v64/
v63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY
(the v45 76/76 off-by-one class is retired).'''),
    # P3 evidence paragraph (the HEADING follows the same lag-1 pattern as the SIZE_BAND: v88 carries 'pass-36 evidence' while the class name is pass-37 — the c2770 attempt-1 P3 abort lesson applied cleanly eighteen cycles running; the class heading moves pass-36 -> pass-37 while the repeats prose appends 'pass-37 repeats at c2788')
    ('''DRIFT-#49 pass-36 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed
at c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/
c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/
c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total
20->18, honest_free 2->0, the two honest-free tasks EXITED the market;
pass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;
pass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;
pass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;
pass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at
c2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats
at c2767; pass-17 repeats
at c2768; pass-18 repeats
at c2769; pass-19 repeats
at c2770; pass-20 repeats
at c2771; pass-21 repeats
at c2772; pass-22 repeats
at c2773; pass-23 repeats
at c2774; pass-24 repeats
at c2775; pass-25 repeats
at c2776; pass-26 repeats
at c2777; pass-27 repeats
at c2778; pass-28 repeats
at c2779; pass-29 repeats
at c2780; pass-30 repeats
at c2781; pass-31 repeats
at c2782; pass-32 repeats
at c2783; pass-33 repeats
at c2784; pass-34 repeats
at c2785; pass-35 repeats
at c2786; pass-36 repeats
at c2787, movement
repeat-class — the scam block 18 stands). The''',
     '''DRIFT-#49 pass-37 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed
at c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/
c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/
c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total
20->18, honest_free 2->0, the two honest-free tasks EXITED the market;
pass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;
pass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;
pass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;
pass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at
c2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats
at c2767; pass-17 repeats
at c2768; pass-18 repeats
at c2769; pass-19 repeats
at c2770; pass-20 repeats
at c2771; pass-21 repeats
at c2772; pass-22 repeats
at c2773; pass-23 repeats
at c2774; pass-24 repeats
at c2775; pass-25 repeats
at c2776; pass-26 repeats
at c2777; pass-27 repeats
at c2778; pass-28 repeats
at c2779; pass-29 repeats
at c2780; pass-30 repeats
at c2781; pass-31 repeats
at c2782; pass-32 repeats
at c2783; pass-33 repeats
at c2784; pass-34 repeats
at c2785; pass-35 repeats
at c2786; pass-36 repeats
at c2787; pass-37 repeats
at c2788, movement
repeat-class — the scam block 18 stands). The'''),
    # P4 contract sentence
    ('''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-37 recorded,
movement repeat-class; return to the DRIFT-#48 root -> RESTORATION recorded; any''',
     '''Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-38 recorded,
movement repeat-class; return to the DRIFT-#48 root -> RESTORATION recorded; any'''),
    # P5 cycle constant
    ("CYCLE = 2788", "CYCLE = 2789"),
    # P6/P7 paths
    ('RAW = "/home/z/my-project/scripts/scan_cycle2788_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2789_raw.json"'),
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2788.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2789.json"'),
    # P8 size band comment (band-name follows the evidence-paragraph lag-1 pattern: pass-36 -> pass-37 while the class name moves to pass-38)
    ('SIZE_BAND = (446, 447)  # DRIFT-#49 pass-36 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787; the DRIFT-#48 root band 446B locked c2747/c2748)',
     'SIZE_BAND = (446, 447)  # DRIFT-#49 pass-37 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788; the DRIFT-#48 root band 446B locked c2747/c2748)'),
    # P9 tuple-match gate rename (pass-37 -> pass-38; the observation literal unchanged)
    ('''check("drift49_pass37_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (18,0,0,18,0)", hard=False)''',
     '''check("drift49_pass38_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (18,0,0,18,0)", hard=False)'''),
    # P10 classification comment
    ('# --- classification gates (SOFT — DRIFT-#49 pass-37 vs RESTORATION vs newest-observation) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-38 vs RESTORATION vs newest-observation) ---'),
    # P11 classification block (pass-38 / RESTORATION / newest-observation)
    ('''if comp_ok and size_ok:
    classification = "DRIFT-#49 pass-37 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"
elif comp_ok:
    classification = "DRIFT-#49 pass-37 (movement repeat-class, size drifted) - size movement noted"''',
     '''if comp_ok and size_ok:
    classification = "DRIFT-#49 pass-38 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"
elif comp_ok:
    classification = "DRIFT-#49 pass-38 (movement repeat-class, size drifted) - size movement noted"'''),
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
for token in ("CYCLE = 2788", "scan_cycle2788", "Validator for cycle 2788",
              "drift49_pass37_match", "pass-37 (movement repeat-class recorded",
              "pass-37 (movement repeat-class, size drifted",
              "pass-36 band", "pass-36 evidence"):
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
if "drift49_pass38_match" not in out or "pass-38" not in out:
    print("FAIL: pass-38 class wiring lost")
    failures.append("pass38-wiring")
if "c7947" in out:
    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")
    failures.append("c7947-remains")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2788.py -> validate_cycle2789.py (11 patches, pass-38 spec)")
