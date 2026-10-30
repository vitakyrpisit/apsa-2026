#!/usr/bin/env python3
"""Rebadge gate for cycle 2820: validate_cycle2819.py -> validate_cycle2820.py.

The REBADGE-CLASS continues (the v119 source survived on disk and in the
5a868fa commit object — object-verified at guard time). Every patch asserts
its old string occurs EXACTLY once in the source BEFORE any mutation;
abort = zero files written. Post-patch: selective no-old-token assertions +
py_compile. Patch count is counted programmatically.
DRIFT-#49 pass-69 spec (per the c2819 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83; pass-2 repeat recorded at c2753; pass-65 repeat recorded at
c2816; pass-66 repeat recorded at c2817; pass-67 repeat recorded
at c2818; pass-68 repeat recorded
at c2819); a repeat -> pass-69 recorded
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never
rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the
root stands, the pass-1 excursion closes as a transient); any other
composition -> newest-observation evidence with the full delta chain printed.
The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2819
attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761
attempt-1 P8 lesson): the v119 source carries 'pass-67 band' AND 'pass-67
evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class
name.
Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching;
the class does NOT fire this cycle): the official c2819 commit hash 5a868fa
short form = 5-a-8-6-8-f-a carries ZERO 'c' characters -> no c+4-digit run ->
the c7947-class does NOT fire (zero artifact births; zero deaths too — the
v119 source carries zero artifact tokens, the c97826 phantom already departed
at v113); the foreign TOP b9757c0 short form = b-9-7-5-7-c-0 carries 'c0' at
the tail — c followed by ONE digit -> no c+4-digit run in the short form, AND
the foreign hash is ABSENT from the v119 source surface (grep-verified at
census time) — zero exposure for the validator surface; HONEST NOTE: the FULL
foreign hash b9757c09d3dcf32fc1fb4f84dde6b2acdc2ca165 carries ZERO c+4-digit
runs (regex-measured at census time) BUT the foreign hash is ABSENT from the
source surface — zero exposure on any surface, the phantom is not born (the
c3819e9 lesson: the phantom class fires only when the hash form actually
written into the source carries the run); the FULL c2819 hash
5a868faeb20344def84ddd4296ef039572c02a08 carries ZERO c+4-digit runs
(regex-measured at census time); the c2820 commit hash is unborn at patch
time, checked post-commit.
P-HIST patch delta forecast (for accounting only, the MEASUREMENT governs):
the P2 'Baseline for c2819' prose rebadges to c2820 (-1 c2819, +1 c2820
born-ONE — the forward-token lesson: the ONLY c2820 birth surface) while the
P2 pass-chain prose RE-INTRODUCES c2819 in the historical phrase ('pass-68
repeat recorded at c2819' — +1 c2819); the observed lists are APPEND-class
(the c2805 forecast-miss lesson — do NOT double-count the forward-token birth
surface: the P3.t2 list-append adds the CURRENT cycle token, not the forward
token): P3 evidence prose gains '/c2819' in the observed list (+1 c2819) and
'pass-68 repeats at c2819' (+1 c2819); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2818' -> 'observed c2752/.../c2818/c2819' (c2819 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson, re-verified
live at this cycle's census: the v119 Step-4 surfaces carry
'cycle2819'/'e2819'); the c2746 GOLD-CHECK comment carries unchanged.
Forecast: c2819 1->4 (+3 net: -1 P2.c Baseline + 1 P2.d chain + 2 P3 + 1 P8),
c2820 0->1 (+1 born-ONE), c2818 4->4 net zero, c2817 4->4 net zero,
total 278 -> 282 (+4 net).
The MEASUREMENT governs over this forecast.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2819.py"
DST = "/home/z/my-project/scripts/validate_cycle2820.py"

PATCHES = [
    # P1 title
    ('"""Validator for cycle 2819.',
     '"""Validator for cycle 2820.'),
    # P2 provenance
    ('DRIFT-#49 pass-68 CLASS (movement repeat-class on tuple match) — sed-rebadge\nfrom the v118 pass-67 carry (the v118 source survived on disk and in the\n290adbb commit object, so the REBADGE-CLASS continues). Baseline for c2819 = the\nDRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first\nmarket movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat\nrecorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at\nc2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;\npass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10\nrepeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat\nrecorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded\nat c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded\nat c2767; pass-17 repeat recorded\nat c2768; pass-18 repeat recorded\nat c2769; pass-19 repeat recorded\nat c2770; pass-20 repeat recorded\nat c2771; pass-21 repeat recorded\nat c2772; pass-22 repeat recorded\nat c2773; pass-23 repeat recorded\nat c2774; pass-24 repeat recorded\nat c2775; pass-25 repeat recorded\nat c2776; pass-26 repeat recorded\nat c2777; pass-27 repeat recorded\nat c2778; pass-28 repeat recorded\nat c2779; pass-29 repeat recorded\nat c2780; pass-30 repeat recorded\nat c2781; pass-31 repeat recorded\nat c2782; pass-32 repeat recorded\nat c2783; pass-33 repeat recorded\nat c2784; pass-34 repeat recorded\nat c2785; pass-35 repeat recorded\nat c2786; pass-36 repeat recorded\nat c2787; pass-37 repeat recorded\nat c2788; pass-38 repeat recorded\nat c2789; pass-39 repeat recorded\nat c2790; pass-40 repeat recorded\nat c2791; pass-41 repeat recorded\nat c2792; pass-42 repeat recorded\nat c2793; pass-43 repeat recorded\nat c2794; pass-44 repeat recorded\nat c2795; pass-45 repeat recorded\nat c2796; pass-46 repeat recorded\nat c2797; pass-47 repeat recorded\nat c2798; pass-48 repeat recorded\nat c2799; pass-49 repeat recorded\nat c2800; pass-50 repeat recorded\nat c2801; pass-51 repeat recorded\nat c2802; pass-52 repeat recorded\nat c2803; pass-53 repeat recorded\nat c2804; pass-54 repeat recorded\nat c2805; pass-55 repeat recorded\nat c2806; pass-56 repeat recorded\nat c2807; pass-57 repeat recorded\nat c2808; pass-58 repeat recorded\nat c2809; pass-59 repeat recorded\nat c2810; pass-60 repeat recorded\nat c2811; pass-61 repeat recorded\nat c2812; pass-62 repeat recorded\nat c2813; pass-63 repeat recorded\nat c2814; pass-64 repeat recorded\nat c2815; pass-65 repeat recorded\nat c2816; pass-66 repeat recorded\nat c2817; pass-67 repeat recorded\nat c2818); a repeat records pass-68\n(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,\nnever rewritten); a return to (20,0,2,18,0) records the RESTORATION event\n(the root stands, the pass-1 excursion closes as a transient); any other\ncomposition records newest-observation evidence with the full delta chain\nprinted. Structural conventions inherited from the v118 class (itself\ninheriting the v117/v109/v95/v94/v93/v92/v91/v90/v89/v88/v87/v86/v85/v84/v83/v82/v81/v80/v79/v78/v77/v76/v75/v74/v73/v72/v71/v70/v69/v68/v67/v66/v65/v64/\nv63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY\n(the v45 76/76 off-by-one class is retired).',
     'DRIFT-#49 pass-69 CLASS (movement repeat-class on tuple match) — sed-rebadge\nfrom the v119 pass-68 carry (the v119 source survived on disk and in the\n5a868fa commit object, so the REBADGE-CLASS continues). Baseline for c2820 = the\nDRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first\nmarket movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat\nrecorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at\nc2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;\npass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10\nrepeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat\nrecorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded\nat c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded\nat c2767; pass-17 repeat recorded\nat c2768; pass-18 repeat recorded\nat c2769; pass-19 repeat recorded\nat c2770; pass-20 repeat recorded\nat c2771; pass-21 repeat recorded\nat c2772; pass-22 repeat recorded\nat c2773; pass-23 repeat recorded\nat c2774; pass-24 repeat recorded\nat c2775; pass-25 repeat recorded\nat c2776; pass-26 repeat recorded\nat c2777; pass-27 repeat recorded\nat c2778; pass-28 repeat recorded\nat c2779; pass-29 repeat recorded\nat c2780; pass-30 repeat recorded\nat c2781; pass-31 repeat recorded\nat c2782; pass-32 repeat recorded\nat c2783; pass-33 repeat recorded\nat c2784; pass-34 repeat recorded\nat c2785; pass-35 repeat recorded\nat c2786; pass-36 repeat recorded\nat c2787; pass-37 repeat recorded\nat c2788; pass-38 repeat recorded\nat c2789; pass-39 repeat recorded\nat c2790; pass-40 repeat recorded\nat c2791; pass-41 repeat recorded\nat c2792; pass-42 repeat recorded\nat c2793; pass-43 repeat recorded\nat c2794; pass-44 repeat recorded\nat c2795; pass-45 repeat recorded\nat c2796; pass-46 repeat recorded\nat c2797; pass-47 repeat recorded\nat c2798; pass-48 repeat recorded\nat c2799; pass-49 repeat recorded\nat c2800; pass-50 repeat recorded\nat c2801; pass-51 repeat recorded\nat c2802; pass-52 repeat recorded\nat c2803; pass-53 repeat recorded\nat c2804; pass-54 repeat recorded\nat c2805; pass-55 repeat recorded\nat c2806; pass-56 repeat recorded\nat c2807; pass-57 repeat recorded\nat c2808; pass-58 repeat recorded\nat c2809; pass-59 repeat recorded\nat c2810; pass-60 repeat recorded\nat c2811; pass-61 repeat recorded\nat c2812; pass-62 repeat recorded\nat c2813; pass-63 repeat recorded\nat c2814; pass-64 repeat recorded\nat c2815; pass-65 repeat recorded\nat c2816; pass-66 repeat recorded\nat c2817; pass-67 repeat recorded\nat c2818; pass-68 repeat recorded\nat c2819); a repeat records pass-69\n(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,\nnever rewritten); a return to (20,0,2,18,0) records the RESTORATION event\n(the root stands, the pass-1 excursion closes as a transient); any other\ncomposition records newest-observation evidence with the full delta chain\nprinted. Structural conventions inherited from the v119 class (itself\ninheriting the v118/v109/v95/v94/v93/v92/v91/v90/v89/v88/v87/v86/v85/v84/v83/v82/v81/v80/v79/v78/v77/v76/v75/v74/v73/v72/v71/v70/v69/v68/v67/v66/v65/v64/\nv63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY\n(the v45 76/76 off-by-one class is retired).'),
    # P3 evidence (lag-1)
    ('DRIFT-#49 pass-67 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed\nat c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/\nc2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/\nc2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815/c2816/c2817/c2818 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total\n20->18, honest_free 2->0, the two honest-free tasks EXITED the market;\npass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;\npass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;\npass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;\npass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at\nc2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats\nat c2767; pass-17 repeats\nat c2768; pass-18 repeats\nat c2769; pass-19 repeats\nat c2770; pass-20 repeats\nat c2771; pass-21 repeats\nat c2772; pass-22 repeats\nat c2773; pass-23 repeats\nat c2774; pass-24 repeats\nat c2775; pass-25 repeats\nat c2776; pass-26 repeats\nat c2777; pass-27 repeats\nat c2778; pass-28 repeats\nat c2779; pass-29 repeats\nat c2780; pass-30 repeats\nat c2781; pass-31 repeats\nat c2782; pass-32 repeats\nat c2783; pass-33 repeats\nat c2784; pass-34 repeats\nat c2785; pass-35 repeats\nat c2786; pass-36 repeats\nat c2787; pass-37 repeats\nat c2788; pass-38 repeats\nat c2789; pass-39 repeats\nat c2790; pass-40 repeats\nat c2791; pass-41 repeats\nat c2792; pass-42 repeats\nat c2793; pass-43 repeats\nat c2794; pass-44 repeats\nat c2795; pass-45 repeats\nat c2796; pass-46 repeats\nat c2797; pass-47 repeats\nat c2798; pass-48 repeats\nat c2799; pass-49 repeats\nat c2800; pass-50 repeats\nat c2801; pass-51 repeats\nat c2802; pass-52 repeats\nat c2803; pass-53 repeats\nat c2804; pass-54 repeats\nat c2805; pass-55 repeats\nat c2806; pass-56 repeats\nat c2807; pass-57 repeats\nat c2808; pass-58 repeats\nat c2809; pass-59 repeats\nat c2810; pass-60 repeats\nat c2811; pass-61 repeats\nat c2812; pass-62 repeats\nat c2813; pass-63 repeats\nat c2814; pass-64 repeats\nat c2815; pass-65 repeats\nat c2816; pass-66 repeats\nat c2817; pass-67 repeats\nat c2818, movement\nrepeat-class — the scam block 18 stands). The',
     'DRIFT-#49 pass-68 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed\nat c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/\nc2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/\nc2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815/c2816/c2817/c2818/c2819 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total\n20->18, honest_free 2->0, the two honest-free tasks EXITED the market;\npass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;\npass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;\npass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;\npass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at\nc2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats\nat c2767; pass-17 repeats\nat c2768; pass-18 repeats\nat c2769; pass-19 repeats\nat c2770; pass-20 repeats\nat c2771; pass-21 repeats\nat c2772; pass-22 repeats\nat c2773; pass-23 repeats\nat c2774; pass-24 repeats\nat c2775; pass-25 repeats\nat c2776; pass-26 repeats\nat c2777; pass-27 repeats\nat c2778; pass-28 repeats\nat c2779; pass-29 repeats\nat c2780; pass-30 repeats\nat c2781; pass-31 repeats\nat c2782; pass-32 repeats\nat c2783; pass-33 repeats\nat c2784; pass-34 repeats\nat c2785; pass-35 repeats\nat c2786; pass-36 repeats\nat c2787; pass-37 repeats\nat c2788; pass-38 repeats\nat c2789; pass-39 repeats\nat c2790; pass-40 repeats\nat c2791; pass-41 repeats\nat c2792; pass-42 repeats\nat c2793; pass-43 repeats\nat c2794; pass-44 repeats\nat c2795; pass-45 repeats\nat c2796; pass-46 repeats\nat c2797; pass-47 repeats\nat c2798; pass-48 repeats\nat c2799; pass-49 repeats\nat c2800; pass-50 repeats\nat c2801; pass-51 repeats\nat c2802; pass-52 repeats\nat c2803; pass-53 repeats\nat c2804; pass-54 repeats\nat c2805; pass-55 repeats\nat c2806; pass-56 repeats\nat c2807; pass-57 repeats\nat c2808; pass-58 repeats\nat c2809; pass-59 repeats\nat c2810; pass-60 repeats\nat c2811; pass-61 repeats\nat c2812; pass-62 repeats\nat c2813; pass-63 repeats\nat c2814; pass-64 repeats\nat c2815; pass-65 repeats\nat c2816; pass-66 repeats\nat c2817; pass-67 repeats\nat c2818; pass-68 repeats\nat c2819, movement\nrepeat-class — the scam block 18 stands). The'),
    # P8 size band (lag-1)
    ('SIZE_BAND = (446, 447)  # DRIFT-#49 pass-67 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815/c2816/c2817/c2818; the DRIFT-#48 root band 446B locked c2747/c2748)',
     'SIZE_BAND = (446, 447)  # DRIFT-#49 pass-68 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/c2777/c2778/c2779/c2780/c2781/c2782/c2783/c2784/c2785/c2786/c2787/c2788/c2789/c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798/c2799/c2800/c2801/c2802/c2803/c2804/c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815/c2816/c2817/c2818/c2819; the DRIFT-#48 root band 446B locked c2747/c2748)'),
    # P4 contract
    ('Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-68 recorded,',
     'Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-69 recorded,'),
    # P5 cycle
    ('CYCLE = 2819',
     'CYCLE = 2820'),
    # P6 raw path
    ('RAW = "/home/z/my-project/scripts/scan_cycle2819_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2820_raw.json"'),
    # P7 pretty path
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2819.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2820.json"'),
    # P9 gate rename
    ('check("drift49_pass68_match", comp_ok,',
     'check("drift49_pass69_match", comp_ok,'),
    # P10 comment
    ('# --- classification gates (SOFT — DRIFT-#49 pass-68 vs RESTORATION vs newest-observation) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-69 vs RESTORATION vs newest-observation) ---'),
    # P11 block
    ('if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-68 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-68 (movement repeat-class, size drifted) - size movement noted"',
     'if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-69 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-69 (movement repeat-class, size drifted) - size movement noted"'),
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
for token in ('CYCLE = 2819', 'scan_cycle2819', 'Validator for cycle 2819', 'drift49_pass68_match', 'pass-68 (movement repeat-class recorded', 'pass-68 (movement repeat-class, size drifted', 'pass-67 band', 'pass-67 evidence'):
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
if "drift49_pass69_match" not in out or "pass-69" not in out:
    print("FAIL: pass-69 class wiring lost")
    failures.append("pass69-wiring")
if "5a868fa" not in out:
    print("FAIL: the c2819 commit-object hash carry lost (the P2 provenance)")
    failures.append("c2819-hash-carry-lost")
if "c7947" in out:
    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")
    failures.append("c7947-remains")
if "c97826" in out:
    print("FAIL: the c97826 phantom token remains (departed at v113)")
    failures.append("c97826-remains")
if "c8402651" in out:
    print("FAIL: the c8402651 full-hash phantom landed on the source surface (the short-form P2 carry must not import it)")
    failures.append("c8402651-remains")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2819.py -> validate_cycle2820.py (11 patches, pass-69 spec)")
