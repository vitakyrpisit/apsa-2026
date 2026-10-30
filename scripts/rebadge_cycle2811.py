#!/usr/bin/env python3
"""Rebadge gate for cycle 2811: validate_cycle2810.py -> validate_cycle2811.py.

The REBADGE-CLASS continues (the v110 source survived on disk and in the
d228cc8 commit object — object-verified at guard time). Every patch asserts
its old string occurs EXACTLY once in the source BEFORE any mutation;
abort = zero files written. Post-patch: selective no-old-token assertions +
py_compile. Patch count is counted programmatically.
DRIFT-#49 pass-60 spec (per the c2810 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83; pass-2 repeat recorded at c2753; ... pass-58 repeat recorded
at c2809; pass-59 repeat recorded at c2810); a repeat -> pass-60 recorded
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never
rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the
root stands, the pass-1 excursion closes as a transient); any other
composition -> newest-observation evidence with the full delta chain printed.
The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2810
attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761
attempt-1 P8 lesson): the v110 source carries 'pass-58 band' AND 'pass-58
evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class
name.
Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching):
the official c2810 commit hash d228cc8 short form = d-2-2-8-c-c-8 carries 'c'
characters (positions 4 and 5) — position 4 'c' is followed by 'c' (not a
digit), position 5 'c' is followed by '8' then END — NO c+4-digit run (zero
hash-artifact exposure); the v111 P2 paragraph carries 'the d228cc8 commit
object' (zero new hash-artifact birth), while the v110 P2 carry 'the d19b6ac
commit object' rebadges AWAY (d19b6ac carries a 'c' character (position 6,
terminal) — NO c+4-digit run, zero token deaths, the c7947 class does NOT
fire); the foreign TOP 92b5acc short form = 9-2-b-5-a-c-c carries 'c'
characters (positions 6 and 7, terminal) — NO c+4-digit run (zero exposure);
the c2811 commit hash is unborn at patch time, checked post-commit.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2810.py"
DST = "/home/z/my-project/scripts/validate_cycle2811.py"

PATCHES = [
    # P1 title
    ('"""Validator for cycle 2810.',
     '"""Validator for cycle 2811.'),
    # P2 provenance
    ('DRIFT-#49 pass-59 CLASS (movement repeat-class on tuple match) — sed-rebadge\nfrom the v109 pass-58 carry (the v109 source survived on disk and in the\nd19b6ac commit object, so the REBADGE-CLASS continues). Baseline for c2810 = the\nDRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first\nmarket movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat\nrecorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at\nc2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;\npass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10\nrepeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat\nrecorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded\nat c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded\nat c2767; pass-17 repeat recorded\nat c2768; pass-18 repeat recorded\nat c2769; pass-19 repeat recorded\nat c2770; pass-20 repeat recorded\nat c2771; pass-21 repeat recorded\nat c2772; pass-22 repeat recorded\nat c2773; pass-23 repeat recorded\nat c2774; pass-24 repeat recorded\nat c2775; pass-25 repeat recorded\nat c2776; pass-26 repeat recorded\nat c2777; pass-27 repeat recorded\nat c2778; pass-28 repeat recorded\nat c2779; pass-29 repeat recorded\nat c2780; pass-30 repeat recorded\nat c2781; pass-31 repeat recorded\nat c2782; pass-32 repeat recorded\nat c2783; pass-33 repeat recorded\nat c2784; pass-34 repeat recorded\nat c2785; pass-35 repeat recorded\nat c2786; pass-36 repeat recorded\nat c2787; pass-37 repeat recorded\nat c2788; pass-38 repeat recorded\nat c2789; pass-39 repeat recorded\nat c2790; pass-40 repeat recorded\nat c2791; pass-41 repeat recorded\nat c2792; pass-42 repeat recorded\nat c2793; pass-43 repeat recorded\nat c2794; pass-44 repeat recorded\nat c2795; pass-45 repeat recorded\nat c2796; pass-46 repeat recorded\nat c2797; pass-47 repeat recorded\nat c2798; pass-48 repeat recorded\nat c2799; pass-49 repeat recorded\nat c2800; pass-50 repeat recorded\nat c2801; pass-51 repeat recorded\nat c2802; pass-52 repeat recorded\nat c2803; pass-53 repeat recorded\nat c2804; pass-54 repeat recorded\nat c2805; pass-55 repeat recorded\nat c2806; pass-56 repeat recorded\nat c2807; pass-57 repeat recorded\nat c2808; pass-58 repeat recorded\nat c2809); a repeat records pass-59\n(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,\nnever rewritten); a return to (20,0,2,18,0) records the RESTORATION event\n(the root stands, the pass-1 excursion closes as a transient); any other\ncomposition records newest-observation evidence with the full delta chain\nprinted. Structural conventions inherited from the v109 class (itself\ninheriting the v108/v107/v95/v94/v93/v92/v91/v90/v89/v88/v87/v86/v85/v84/v83/v82/v81/v80/v79/v78/v77/v76/v75/v74/v73/v72/v71/v70/v69/v68/v67/v66/v65/v64/\nv63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY\n(the v45 76/76 off-by-one class is retired).',
     'DRIFT-#49 pass-60 CLASS (movement repeat-class on tuple match) — sed-rebadge\nfrom the v110 pass-59 carry (the v110 source survived on disk and in the\nd228cc8 commit object, so the REBADGE-CLASS continues). Baseline for c2811 = the\nDRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first\nmarket movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat\nrecorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at\nc2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;\npass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10\nrepeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat\nrecorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded\nat c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded\nat c2767; pass-17 repeat recorded\nat c2768; pass-18 repeat recorded\nat c2769; pass-19 repeat recorded\nat c2770; pass-20 repeat recorded\nat c2771; pass-21 repeat recorded\nat c2772; pass-22 repeat recorded\nat c2773; pass-23 repeat recorded\nat c2774; pass-24 repeat recorded\nat c2775; pass-25 repeat recorded\nat c2776; pass-26 repeat recorded\nat c2777; pass-27 repeat recorded\nat c2778; pass-28 repeat recorded\nat c2779; pass-29 repeat recorded\nat c2780; pass-30 repeat recorded\nat c2781; pass-31 repeat recorded\nat c2782; pass-32 repeat recorded\nat c2783; pass-33 repeat recorded\nat c2784; pass-34 repeat recorded\nat c2785; pass-35 repeat recorded\nat c2786; pass-36 repeat recorded\nat c2787; pass-37 repeat recorded\nat c2788; pass-38 repeat recorded\nat c2789; pass-39 repeat recorded\nat c2790; pass-40 repeat recorded\nat c2791; pass-41 repeat recorded\nat c2792; pass-42 repeat recorded\nat c2793; pass-43 repeat recorded\nat c2794; pass-44 repeat recorded\nat c2795; pass-45 repeat recorded\nat c2796; pass-46 repeat recorded\nat c2797; pass-47 repeat recorded\nat c2798; pass-48 repeat recorded\nat c2799; pass-49 repeat recorded\nat c2800; pass-50 repeat recorded\nat c2801; pass-51 repeat recorded\nat c2802; pass-52 repeat recorded\nat c2803; pass-53 repeat recorded\nat c2804; pass-54 repeat recorded\nat c2805; pass-55 repeat recorded\nat c2806; pass-56 repeat recorded\nat c2807; pass-57 repeat recorded\nat c2808; pass-58 repeat recorded\nat c2809; pass-59 repeat recorded\nat c2810); a repeat records pass-60\n(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,\nnever rewritten); a return to (20,0,2,18,0) records the RESTORATION event\n(the root stands, the pass-1 excursion closes as a transient); any other\ncomposition records newest-observation evidence with the full delta chain\nprinted. Structural conventions inherited from the v110 class (itself\ninheriting the v109/v108/v95/v94/v93/v92/v91/v90/v89/v88/v87/v86/v85/v84/v83/v82/v81/v80/v79/v78/v77/v76/v75/v74/v73/v72/v71/v70/v69/v68/v67/v66/v65/v64/\nv63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY\n(the v45 76/76 off-by-one class is retired).'),
    # P3 evidence (lag-1)
    ('DRIFT-#49 pass-58 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed\nat c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/\nc2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/\nc2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total\n20->18, honest_free 2->0, the two honest-free tasks EXITED the market;\npass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;\npass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;\npass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;\npass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at\nc2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats\nat c2767; pass-17 repeats\nat c2768; pass-18 repeats\nat c2769; pass-19 repeats\nat c2770; pass-20 repeats\nat c2771; pass-21 repeats\nat c2772; pass-22 repeats\nat c2773; pass-23 repeats\nat c2774; pass-24 repeats\nat c2775; pass-25 repeats\nat c2776; pass-26 repeats\nat c2777; pass-27 repeats\nat c2778; pass-28 repeats\nat c2779; pass-29 repeats\nat c2780; pass-30 repeats\nat c2781; pass-31 repeats\nat c2782; pass-32 repeats\nat c2783; pass-33 repeats\nat c2784; pass-34 repeats\nat c2785; pass-35 repeats\nat c2786; pass-36 repeats\nat c2787; pass-37 repeats\nat c2788; pass-38 repeats\nat c2789; pass-39 repeats\nat c2790; pass-40 repeats\nat c2791; pass-41 repeats\nat c2792; pass-42 repeats\nat c2793; pass-43 repeats\nat c2794; pass-44 repeats\nat c2795; pass-45 repeats\nat c2796; pass-46 repeats\nat c2797; pass-47 repeats\nat c2798; pass-48 repeats\nat c2799; pass-49 repeats\nat c2800; pass-50 repeats\nat c2801; pass-51 repeats\nat c2802; pass-52 repeats\nat c2803; pass-53 repeats\nat c2804; pass-54 repeats\nat c2805; pass-55 repeats\nat c2806; pass-56 repeats\nat c2807; pass-57 repeats\nat c2808; pass-58 repeats\nat c2809, movement\nrepeat-class — the scam block 18 stands). The',
     'DRIFT-#49 pass-59 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed\nat c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/\nc2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/\nc2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809/c2810 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total\n20->18, honest_free 2->0, the two honest-free tasks EXITED the market;\npass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;\npass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;\npass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;\npass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at\nc2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats\nat c2767; pass-17 repeats\nat c2768; pass-18 repeats\nat c2769; pass-19 repeats\nat c2770; pass-20 repeats\nat c2771; pass-21 repeats\nat c2772; pass-22 repeats\nat c2773; pass-23 repeats\nat c2774; pass-24 repeats\nat c2775; pass-25 repeats\nat c2776; pass-26 repeats\nat c2777; pass-27 repeats\nat c2778; pass-28 repeats\nat c2779; pass-29 repeats\nat c2780; pass-30 repeats\nat c2781; pass-31 repeats\nat c2782; pass-32 repeats\nat c2783; pass-33 repeats\nat c2784; pass-34 repeats\nat c2785; pass-35 repeats\nat c2786; pass-36 repeats\nat c2787; pass-37 repeats\nat c2788; pass-38 repeats\nat c2789; pass-39 repeats\nat c2790; pass-40 repeats\nat c2791; pass-41 repeats\nat c2792; pass-42 repeats\nat c2793; pass-43 repeats\nat c2794; pass-44 repeats\nat c2795; pass-45 repeats\nat c2796; pass-46 repeats\nat c2797; pass-47 repeats\nat c2798; pass-48 repeats\nat c2799; pass-49 repeats\nat c2800; pass-50 repeats\nat c2801; pass-51 repeats\nat c2802; pass-52 repeats\nat c2803; pass-53 repeats\nat c2804; pass-54 repeats\nat c2805; pass-55 repeats\nat c2806; pass-56 repeats\nat c2807; pass-57 repeats\nat c2808; pass-58 repeats\nat c2809; pass-59 repeats\nat c2810, movement\nrepeat-class — the scam block 18 stands). The'),
    # P8 size band (lag-1)
    ('SIZE_BAND = (446, 447)  # DRIFT-#49 pass-58 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809; the DRIFT-#48 root band 446B locked c2747/c2748)',
     'SIZE_BAND = (446, 447)  # DRIFT-#49 pass-59 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809/c2810; the DRIFT-#48 root band 446B locked c2747/c2748)'),
    # P4 contract
    ('Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-59 recorded,',
     'Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-60 recorded,'),
    # P5 cycle
    ('CYCLE = 2810',
     'CYCLE = 2811'),
    # P6 raw path
    ('RAW = "/home/z/my-project/scripts/scan_cycle2810_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2811_raw.json"'),
    # P7 pretty path
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2810.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2811.json"'),
    # P9 gate rename
    ('check("drift49_pass59_match", comp_ok,',
     'check("drift49_pass60_match", comp_ok,'),
    # P10 comment
    ('# --- classification gates (SOFT — DRIFT-#49 pass-59 vs RESTORATION vs newest-observation) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-60 vs RESTORATION vs newest-observation) ---'),
    # P11 block
    ('if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-59 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-59 (movement repeat-class, size drifted) - size movement noted"',
     'if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-60 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-60 (movement repeat-class, size drifted) - size movement noted"'),
]

src_data = open(SRC).read()
failures = []
for i, (old, new) in enumerate(PATCHES, 1):
    n = src_data.count(old)
    tag = f"P{i}"
    if n != 1:
        failures.append(f"{tag}: old string count={n} (expect 1)")
        print(f"FAIL: {tag} old-count={n}")
    else:
        print(f"ok: {tag} old-count=1")

if failures:
    print(f"REBADGE_ABORTED: {len(failures)} patch-gate failures - NO files written")
    sys.exit(1)

out = src_data
for old, new in PATCHES:
    out = out.replace(old, new)
open(DST, "w").write(out)

# post-patch selective assertions
for token in ('CYCLE = 2810', 'scan_cycle2810', 'Validator for cycle 2810', 'drift49_pass59_match', 'pass-59 (movement repeat-class recorded', 'pass-59 (movement repeat-class, size drifted', 'pass-58 band', 'pass-58 evidence'):
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
if "drift49_pass60_match" not in out or "pass-60" not in out:
    print("FAIL: pass-60 class wiring lost")
    failures.append("pass60-wiring")
if "c7947" in out:
    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")
    failures.append("c7947-remains")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2810.py -> validate_cycle2811.py (11 patches, pass-60 spec)")
