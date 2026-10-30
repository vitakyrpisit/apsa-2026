#!/usr/bin/env python3
"""Authoring harness for the c2810 rebadge gate (gen_rebadge_2810.py).

Extracts the P2/P3/P8 old-paragraphs VERBATIM from the actual v109 source
bytes (the lag-1 dual-surface lesson: the v109 source carries 'pass-57 band'
AND 'pass-57 evidence'), applies the standard rebadge transformations, and
writes rebadge_cycle2810.py with the 11-patch battery. The generator is left
UNTRACKED for the foreign-absorption path (the gen_rebadge_2800/2801/2802/
2803/2804/2805/2806/2807/2808/2809.py class). Every transformation asserts
exactly-one fire; any miss aborts with no file written. Hash-artifact watch
(checked BEFORE writing): the official c2809 commit hash d19b6ac short form =
d-1-9-b-6-a-c carries a 'c' character (position 6, terminal) — NO c+4-digit
run, zero hash-artifact birth, zero exposure; the v110 P2 paragraph carries
'the d19b6ac commit object' (zero new hash-artifact birth), while the v109 P2
carry 'the 3c0fe6c commit object' rebadges AWAY (3c0fe6c carries 'c'
characters (positions 1 and 6) — NO c+4-digit run, zero token deaths, the
c7947 class does NOT fire — c7947 already exited the histogram at v88); the
foreign TOP 1288d7f short form = 1-2-8-8-d-7-f carries NO 'c' character at
all — NO c+4-digit run, zero exposure; the c2810 commit hash is unborn at
patch time, checked post-commit.
"""
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2809.py"
OUT = "/home/z/my-project/scripts/rebadge_cycle2810.py"

src = open(SRC, encoding="utf-8").read()
failures = []


def extract(start_anchor, end_anchor, label):
    i = src.find(start_anchor)
    if i < 0:
        failures.append(f"{label}: start anchor not found")
        return ""
    j = src.find(end_anchor, i)
    if j < 0:
        failures.append(f"{label}: end anchor not found")
        return ""
    j += len(end_anchor)
    seg = src[i:j]
    n = src.count(seg)
    if n != 1:
        failures.append(f"{label}: extracted segment count={n} (expect 1)")
    print(f"ok: {label} extracted {len(seg)}B occurrences={n}")
    return seg


P2_old = extract(
    "DRIFT-#49 pass-58 CLASS (movement repeat-class on tuple match) — sed-rebadge",
    "(the v45 76/76 off-by-one class is retired).", "P2")
P3_old = extract(
    "DRIFT-#49 pass-57 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed",
    "the scam block 18 stands). The", "P3")
P8_old = extract(
    "SIZE_BAND = (446, 447)  # DRIFT-#49 pass-57 band @ 446B (observed ",
    "the DRIFT-#48 root band 446B locked c2747/c2748)", "P8")


def apply_one(text, old, new, label):
    n = text.count(old)
    if n != 1:
        failures.append(f"{label}: transform old-count={n} (expect 1)")
        print(f"FAIL: {label} old-count={n}")
        return text
    print(f"ok: {label} transform fired")
    return text.replace(old, new)


# P2 transformations (the lag-1 chain extension + spec bump + carry refresh)
P2_new = P2_old
P2_new = apply_one(P2_new, "DRIFT-#49 pass-58 CLASS",
                   "DRIFT-#49 pass-59 CLASS", "P2.t1")
P2_new = apply_one(
    P2_new,
    "from the v108 pass-57 carry (the v108 source survived on disk and in the\n"
    "3c0fe6c commit object",
    "from the v109 pass-58 carry (the v109 source survived on disk and in the\n"
    "d19b6ac commit object", "P2.t2")
P2_new = apply_one(P2_new, "Baseline for c2809 = the",
                   "Baseline for c2810 = the", "P2.t3")
P2_new = apply_one(
    P2_new,
    "pass-57 repeat recorded\nat c2808); "
    "a repeat records pass-58",
    "pass-57 repeat recorded\nat c2808; pass-58 repeat recorded\nat c2809); "
    "a repeat records pass-59", "P2.t4")
P2_new = apply_one(
    P2_new,
    "inherited from the v108 class (itself\ninheriting the v107/v106/",
    "inherited from the v109 class (itself\ninheriting the v108/v107/", "P2.t5")

# P3 transformations (the lag-1 evidence heading + observed-list append + chain)
P3_new = P3_old
P3_new = apply_one(P3_new, "DRIFT-#49 pass-57 evidence (on disk):",
                   "DRIFT-#49 pass-58 evidence (on disk):", "P3.t1")
P3_new = apply_one(P3_new, "/c2804/c2805/c2806/c2807/c2808 (pass-1 opens at c2752",
                   "/c2804/c2805/c2806/c2807/c2808/c2809 (pass-1 opens at c2752", "P3.t2")
P3_new = apply_one(
    P3_new,
    "pass-57 repeats\nat c2808, movement\nrepeat-class",
    "pass-57 repeats\nat c2808; pass-58 repeats\nat c2809, movement\n"
    "repeat-class", "P3.t3")

# P8 transformations (the lag-1 SIZE_BAND band-name + observed-list append)
P8_new = P8_old
P8_new = apply_one(P8_new, "pass-57 band @ 446B (observed c2752/",
                   "pass-58 band @ 446B (observed c2752/", "P8.t1")
P8_new = apply_one(
    P8_new,
    "/c2804/c2805/c2806/c2807/c2808; the DRIFT-#48 root band 446B locked c2747/c2748)",
    "/c2804/c2805/c2806/c2807/c2808/c2809; the DRIFT-#48 root band 446B locked c2747/c2748)",
    "P8.t2")

if failures:
    print(f"GEN_ABORTED: {len(failures)} failures - NO file written")
    sys.exit(1)

DOCSTRING = '''#!/usr/bin/env python3
"""Rebadge gate for cycle 2810: validate_cycle2809.py -> validate_cycle2810.py.

The REBADGE-CLASS continues (the v109 source survived on disk and in the
d19b6ac commit object — object-verified at guard time). Every patch asserts
its old string occurs EXACTLY once in the source BEFORE any mutation;
abort = zero files written. Post-patch: selective no-old-token assertions +
py_compile. Patch count is counted programmatically.
DRIFT-#49 pass-59 spec (per the c2809 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83; pass-2 repeat recorded at c2753; ... pass-57 repeat recorded
at c2808; pass-58 repeat recorded at c2809); a repeat -> pass-59 recorded
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never
rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the
root stands, the pass-1 excursion closes as a transient); any other
composition -> newest-observation evidence with the full delta chain printed.
The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2809
attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761
attempt-1 P8 lesson): the v109 source carries 'pass-57 band' AND 'pass-57
evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class
name.
Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching):
the official c2809 commit hash d19b6ac short form = d-1-9-b-6-a-c carries a
'c' character (position 6, terminal) — NO c+4-digit run (zero hash-artifact
exposure); the v110 P2 paragraph carries 'the d19b6ac commit object' (zero new
hash-artifact birth), while the v109 P2 carry 'the 3c0fe6c commit object'
rebadges AWAY (3c0fe6c carries 'c' characters (positions 1 and 6) — NO
c+4-digit run, zero token deaths, the c7947 class does NOT fire); the foreign
TOP 1288d7f short form = 1-2-8-8-d-7-f carries NO 'c' character at all — NO
c+4-digit run (zero exposure); the c2810 commit hash is unborn at patch time,
checked post-commit.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2809.py"
DST = "/home/z/my-project/scripts/validate_cycle2810.py"

PATCHES = [
'''

FIXED_TAIL = '''    # P4 contract
    ('Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-58 recorded,',
     'Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-59 recorded,'),
    # P5 cycle
    ('CYCLE = 2809',
     'CYCLE = 2810'),
    # P6 raw path
    ('RAW = "/home/z/my-project/scripts/scan_cycle2809_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2810_raw.json"'),
    # P7 pretty path
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2809.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2810.json"'),
    # P9 gate rename
    ('check("drift49_pass58_match", comp_ok,',
     'check("drift49_pass59_match", comp_ok,'),
    # P10 comment
    ('# --- classification gates (SOFT — DRIFT-#49 pass-58 vs RESTORATION vs newest-observation) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-59 vs RESTORATION vs newest-observation) ---'),
    # P11 block
    ('if comp_ok and size_ok:\\n    classification = "DRIFT-#49 pass-58 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\\nelif comp_ok:\\n    classification = "DRIFT-#49 pass-58 (movement repeat-class, size drifted) - size movement noted"',
     'if comp_ok and size_ok:\\n    classification = "DRIFT-#49 pass-59 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\\nelif comp_ok:\\n    classification = "DRIFT-#49 pass-59 (movement repeat-class, size drifted) - size movement noted"'),
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
for token in ('CYCLE = 2809', 'scan_cycle2809', 'Validator for cycle 2809', 'drift49_pass58_match', 'pass-58 (movement repeat-class recorded', 'pass-58 (movement repeat-class, size drifted', 'pass-57 band', 'pass-57 evidence'):
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
if "drift49_pass59_match" not in out or "pass-59" not in out:
    print("FAIL: pass-59 class wiring lost")
    failures.append("pass59-wiring")
if "c7947" in out:
    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")
    failures.append("c7947-remains")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2809.py -> validate_cycle2810.py (11 patches, pass-59 spec)")
'''

# assemble the P1/P2/P3/P8 patch literals (repr-embedded, verbatim bytes)
p1 = ("    # P1 title\n"
      "    ('\"\"\"Validator for cycle 2809.',\n"
      "     '\"\"\"Validator for cycle 2810.'),\n")
p2 = ("    # P2 provenance\n"
      f"    ({P2_old!r},\n     {P2_new!r}),\n")
p3 = ("    # P3 evidence (lag-1)\n"
      f"    ({P3_old!r},\n     {P3_new!r}),\n")
p8 = ("    # P8 size band (lag-1)\n"
      f"    ({P8_old!r},\n     {P8_new!r}),\n")

body = DOCSTRING + p1 + p2 + p3 + p8 + FIXED_TAIL
open(OUT, "w", encoding="utf-8").write(body)
print(f"gen_rebadge_2810: wrote {OUT} ({len(body)}B) — 11 patches (P1-P11)")
