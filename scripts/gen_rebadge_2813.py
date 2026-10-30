#!/usr/bin/env python3
"""Authoring harness for the c2813 rebadge — gen_rebadge_2813.py.

Extracts the P2/P3/P8 old-paragraphs VERBATIM from the v112 source bytes
(the c2812 authoring-harness class), applies the targeted sub-replacements to
build the new strings, and emits rebadge_cycle2813.py with the 11-patch
PATCHES list embedded as repr() literals. The generator is left untracked for
the foreign-absorption path. Abort = zero files written on any mismatch.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2812.py"
GEN = "/home/z/my-project/scripts/rebadge_cycle2813.py"

src = open(SRC, encoding="utf-8").read()

# --- P2 provenance paragraph (verbatim extraction) ---
P2_HEAD = "DRIFT-#49 pass-61 CLASS"
P2_TAIL = "(the v45 76/76 off-by-one class is retired)."
i = src.find(P2_HEAD)
j = src.find(P2_TAIL)
assert i != -1 and j != -1 and i < j, "P2 anchors not found"
P2_OLD = src[i:j + len(P2_TAIL)]
assert src.count(P2_OLD) == 1, f"P2 old count={src.count(P2_OLD)}"

# --- P3 evidence paragraph (verbatim extraction, lag-1) ---
P3_HEAD = "DRIFT-#49 pass-60 evidence"
P3_TAIL = "repeat-class — the scam block 18 stands). The"
i = src.find(P3_HEAD)
j = src.find(P3_TAIL)
assert i != -1 and j != -1 and i < j, "P3 anchors not found"
P3_OLD = src[i:j + len(P3_TAIL)]
assert src.count(P3_OLD) == 1, f"P3 old count={src.count(P3_OLD)}"

# --- P8 SIZE_BAND line (verbatim extraction, lag-1) ---
P8_HEAD = "SIZE_BAND = (446, 447)  # DRIFT-#49 pass-60 band"
P8_TAIL = "the DRIFT-#48 root band 446B locked c2747/c2748)"
i = src.find(P8_HEAD)
j = src.find(P8_TAIL)
assert i != -1 and j != -1 and i < j, "P8 anchors not found"
P8_OLD = src[i:j + len(P8_TAIL)]
assert src.count(P8_OLD) == 1, f"P8 old count={src.count(P8_OLD)}"


def apply1(text, old, new, tag):
    n = text.count(old)
    assert n == 1, f"{tag}: sub-old count={n}"
    return text.replace(old, new)


# --- P2 old -> new (5 targeted sub-replacements) ---
P2_NEW = P2_OLD
P2_NEW = apply1(P2_NEW, "DRIFT-#49 pass-61 CLASS", "DRIFT-#49 pass-62 CLASS", "P2.a")
P2_NEW = apply1(P2_NEW,
                "from the v111 pass-60 carry (the v111 source survived on disk and in the\n2c97826 commit object",
                "from the v112 pass-61 carry (the v112 source survived on disk and in the\nfcd7b1c commit object", "P2.b")
P2_NEW = apply1(P2_NEW, "Baseline for c2812 = the", "Baseline for c2813 = the", "P2.c")
P2_NEW = apply1(P2_NEW,
                "at c2811); a repeat records pass-61\n(movement repeat-class",
                "at c2811; pass-61 repeat recorded\nat c2812); a repeat records pass-62\n(movement repeat-class", "P2.d")
P2_NEW = apply1(P2_NEW,
                "inherited from the v111 class (itself\ninheriting the v110/v109/",
                "inherited from the v112 class (itself\ninheriting the v111/v109/", "P2.e")

# --- P3 old -> new (3 targeted sub-replacements) ---
P3_NEW = P3_OLD
P3_NEW = apply1(P3_NEW, "DRIFT-#49 pass-60 evidence", "DRIFT-#49 pass-61 evidence", "P3.a")
P3_NEW = apply1(P3_NEW, "c2809/c2810/c2811 (pass-1 opens", "c2809/c2810/c2811/c2812 (pass-1 opens", "P3.b")
P3_NEW = apply1(P3_NEW,
                "at c2811, movement\nrepeat-class",
                "at c2811; pass-61 repeats\nat c2812, movement\nrepeat-class", "P3.c")

# --- P8 old -> new (2 targeted sub-replacements) ---
P8_NEW = P8_OLD
P8_NEW = apply1(P8_NEW, "pass-60 band @ 446B (observed", "pass-61 band @ 446B (observed", "P8.a")
P8_NEW = apply1(P8_NEW, "c2809/c2810/c2811; the DRIFT-#48 root band",
                "c2809/c2810/c2811/c2812; the DRIFT-#48 root band", "P8.b")

# --- the 8 simple patches (verbatim old strings from the v112 source) ---
SIMPLE = [
    # P1 title
    ('"""Validator for cycle 2812.',
     '"""Validator for cycle 2813.'),
    # P4 contract
    ('Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-61 recorded,',
     'Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-62 recorded,'),
    # P5 cycle
    ('CYCLE = 2812',
     'CYCLE = 2813'),
    # P6 raw path
    ('RAW = "/home/z/my-project/scripts/scan_cycle2812_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2813_raw.json"'),
    # P7 pretty path
    ('PRETTY = "/home/z/my-project/scripts/scan_cycle2812.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2813.json"'),
    # P9 gate rename
    ('check("drift49_pass61_match", comp_ok,',
     'check("drift49_pass62_match", comp_ok,'),
    # P10 comment
    ('# --- classification gates (SOFT — DRIFT-#49 pass-61 vs RESTORATION vs newest-observation) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-62 vs RESTORATION vs newest-observation) ---'),
    # P11 block
    ('if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-61 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-61 (movement repeat-class, size drifted) - size movement noted"',
     'if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-62 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-62 (movement repeat-class, size drifted) - size movement noted"'),
]

# --- verify every simple old string occurs EXACTLY once in v112 ---
for k, (old, _new) in enumerate(SIMPLE, 1):
    n = src.count(old)
    assert n == 1, f"simple patch {k}: old count={n}"

DOCSTRING = '''#!/usr/bin/env python3
"""Rebadge gate for cycle 2813: validate_cycle2812.py -> validate_cycle2813.py.

The REBADGE-CLASS continues (the v112 source survived on disk and in the
fcd7b1c commit object — object-verified at guard time). Every patch asserts
its old string occurs EXACTLY once in the source BEFORE any mutation;
abort = zero files written. Post-patch: selective no-old-token assertions +
py_compile. Patch count is counted programmatically.
DRIFT-#49 pass-62 spec (per the c2812 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83; pass-2 repeat recorded at c2753; pass-59 repeat recorded at
c2810; pass-60 repeat recorded at c2811); a repeat -> pass-62 recorded
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never
rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the
root stands, the pass-1 excursion closes as a transient); any other
composition -> newest-observation evidence with the full delta chain printed.
The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2812
attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761
attempt-1 P8 lesson): the v112 source carries 'pass-60 band' AND 'pass-60
evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class
name.
Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching;
the class does NOT fire this cycle): the official c2812 commit hash fcd7b1c
short form = f-c-d-7-b-1-c carries 'c' characters (positions 1 and 6) —
position 1 'c' is followed by 'd' (non-digit, the run breaks) and position 6
'c' is TERMINAL -> NO c+4-digit run -> the c7947-class does NOT fire (zero
artifact births); the v112 P2 carry 'the 2c97826 commit object' rebadges AWAY
— the c97826 phantom token DEPARTS (ONE token death, declared here and
verified at measure time, the MEASUREMENT GOVERNS); the foreign TOP 30a3440
short form carries NO 'c' character at all (3-0-a-3-4-4-0) — zero exposure;
the c2813 commit hash is unborn at patch time, checked post-commit.
P-HIST patch delta forecast (for accounting only, the MEASUREMENT governs):
the P2 'Baseline for c2812' prose rebadges to c2813 (-1 c2812, +1 c2813
born-ONE — the forward-token lesson: the ONLY c2813 birth surface) while the
P2 pass-chain prose RE-INTRODUCES c2812 in the historical phrase ('pass-61
repeat recorded at c2812' — +1 c2812); the observed lists are APPEND-class
(the c2805 forecast-miss lesson — do NOT double-count the forward-token birth
surface: the P3.t2 list-append adds the CURRENT cycle token, not the forward
token): P3 evidence prose gains '/c2812' in the observed list (+1 c2812) and
'pass-61 repeats at c2812' (+1 c2812); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2811' -> 'observed c2752/.../c2811/c2812' (c2812 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson, re-verified
live at this cycle's census: the v112 Step-4 surfaces carry
'cycle2812'/'e2812'); the c2746 GOLD-CHECK comment carries unchanged.
Forecast: c2812 1->4 (+3 net), c2813 0->1 (+1 born-ONE), c97826 1->0 (ONE
token DEATH — the phantom departs with the v112 P2 hash carry), total
251 -> 254 (+3 net).
The MEASUREMENT governs over this forecast.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2812.py"
DST = "/home/z/my-project/scripts/validate_cycle2813.py"

PATCHES = [
'''

BODY = ''']

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
for token in ('CYCLE = 2812', 'scan_cycle2812', 'Validator for cycle 2812', 'drift49_pass61_match', 'pass-61 (movement repeat-class recorded', 'pass-61 (movement repeat-class, size drifted', 'pass-60 band', 'pass-60 evidence'):
    if token in out:
        print(f"FAIL: old token remains: {token}")
        failures.append(token)
if "c97826" in out:
    print("FAIL: the c97826 phantom token remains (the v112 P2 hash carry rebadged away)")
    failures.append("c97826-remains")
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
if "drift49_pass62_match" not in out or "pass-62" not in out:
    print("FAIL: pass-62 class wiring lost")
    failures.append("pass62-wiring")
if "fcd7b1c" not in out:
    print("FAIL: the c2812 commit-object hash carry lost (the P2 provenance)")
    failures.append("c2812-hash-carry-lost")
if "c7947" in out:
    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")
    failures.append("c7947-remains")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2812.py -> validate_cycle2813.py (11 patches, pass-62 spec)")
'''

# assemble the PATCHES entries in the c2812 order:
# P1 title, P2 provenance, P3 evidence (lag-1), P8 size band (lag-1),
# P4 contract, P5 cycle, P6 raw, P7 pretty, P9 gate, P10 comment, P11 block
patch_entries = [
    ("# P1 title", SIMPLE[0]),
    ("# P2 provenance", (P2_OLD, P2_NEW)),
    ("# P3 evidence (lag-1)", (P3_OLD, P3_NEW)),
    ("# P8 size band (lag-1)", (P8_OLD, P8_NEW)),
    ("# P4 contract", SIMPLE[1]),
    ("# P5 cycle", SIMPLE[2]),
    ("# P6 raw path", SIMPLE[3]),
    ("# P7 pretty path", SIMPLE[4]),
    ("# P9 gate rename", SIMPLE[5]),
    ("# P10 comment", SIMPLE[6]),
    ("# P11 block", SIMPLE[7]),
]

parts = [DOCSTRING]
for comment, (old, new) in patch_entries:
    parts.append(f"    {comment}\n    ({old!r},\n     {new!r}),\n")
parts.append(BODY)
gen_src = "".join(parts)
open(GEN, "w", encoding="utf-8").write(gen_src)
py_compile.compile(GEN, doraise=True)
print(f"gen_rebadge_2813: wrote {GEN} bytes={len(gen_src)} py_compile=CLEAN")
print(f"P2_old={len(P2_OLD)}B P3_old={len(P3_OLD)}B P8_old={len(P8_OLD)}B")
print(f"P2_new={len(P2_NEW)}B P3_new={len(P3_NEW)}B P8_new={len(P8_NEW)}B")
