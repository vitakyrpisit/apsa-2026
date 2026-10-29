#!/usr/bin/env python3
"""Authoring harness for rebadge_cycle2798.py — the c2797 gen_rebadge_2797.py
precedent. Extracts the P2/P3/P8 old-paragraphs VERBATIM from the ACTUAL v97
source bytes (measured, never hand-copied), builds the new-strings via
asserted unique replacements, and EMITS rebadge_cycle2798.py with all eleven
patches embedded. The emitted rebadge script re-validates every old-string
count==1 before mutating (abort = zero files written)."""
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2797.py"
OUT = "/home/z/my-project/scripts/rebadge_cycle2798.py"

src = open(SRC, encoding="utf-8").read()
fail = []


def extract(start, end, tag):
    i = src.find(start)
    j = src.find(end, i if i >= 0 else 0)
    if i < 0 or j < 0 or src.count(start) != 1 or src.count(end) != 1:
        fail.append(f"{tag}: anchor not unique/found (start={src.count(start)} end={src.count(end)})")
        return ""
    return src[i:j + len(end)]


p2_old = extract("DRIFT-#49 pass-46 CLASS (movement repeat-class on tuple match) — sed-rebadge",
                 "(the v45 76/76 off-by-one class is retired).", "P2")
p3_old = extract("DRIFT-#49 pass-45 evidence (on disk): five-tuple",
                 "repeat-class — the scam block 18 stands). The", "P3")
p8_old = extract("SIZE_BAND = (446, 447)  # DRIFT-#49 pass-45 band @ 446B (observed ",
                 "locked c2747/c2748)", "P8")

if fail:
    print("GEN_ABORTED:", "; ".join(fail))
    sys.exit(1)


def replace_once(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        fail.append(f"{tag}: transform anchor count={n} (expect 1): {old[:60]!r}")
        return text
    return text.replace(old, new)


p2_new = p2_old
p2_new = replace_once(p2_new, "pass-46 CLASS", "pass-47 CLASS", "P2-t1")
p2_new = replace_once(p2_new, "from the v96 pass-45 carry", "from the v97 pass-46 carry", "P2-t2")
p2_new = replace_once(p2_new, "the v96 source survived on disk and in the\n1baacec commit object",
                      "the v97 source survived on disk and in the\n98db775 commit object", "P2-t3")
p2_new = replace_once(p2_new, "Baseline for c2797 = the", "Baseline for c2798 = the", "P2-t4")
p2_new = replace_once(p2_new, "at c2794; pass-44 repeat recorded\nat c2795; pass-45 repeat recorded\nat c2796); a repeat records pass-46",
                      "at c2794; pass-44 repeat recorded\nat c2795; pass-45 repeat recorded\nat c2796; pass-46 repeat recorded\nat c2797); a repeat records pass-47", "P2-t5")
p2_new = replace_once(p2_new, "Structural conventions inherited from the v96 class (itself\ninheriting the v95/v94/v93/v92/v91/v90/v89/",
                      "Structural conventions inherited from the v97 class (itself\ninheriting the v96/v95/v94/v93/v92/v91/v90/v89/", "P2-t6")

p3_new = p3_old
p3_new = replace_once(p3_new, "pass-45 evidence (on disk)", "pass-46 evidence (on disk)", "P3-t1")
p3_new = replace_once(p3_new, "c2790/c2791/c2792/c2793/c2794/c2795/c2796 (pass-1 opens", "c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797 (pass-1 opens", "P3-t2")
p3_new = replace_once(p3_new, "pass-45 repeats\nat c2796, movement",
                      "pass-45 repeats\nat c2796; pass-46 repeats\nat c2797, movement", "P3-t3")

p8_new = p8_old
p8_new = replace_once(p8_new, "pass-45 band @ 446B", "pass-46 band @ 446B", "P8-t1")
p8_new = replace_once(p8_new, "c2790/c2791/c2792/c2793/c2794/c2795/c2796; the DRIFT-#48 root band",
                      "c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797; the DRIFT-#48 root band", "P8-t2")

if fail:
    print("GEN_ABORTED:", "; ".join(fail))
    sys.exit(1)

P1_OLD = '"""Validator for cycle 2797.'
P1_NEW = '"""Validator for cycle 2798.'
P4_OLD = "Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-46 recorded,"
P4_NEW = "Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-47 recorded,"
P5_OLD = "CYCLE = 2797"
P5_NEW = "CYCLE = 2798"
P6_OLD = 'RAW = "/home/z/my-project/scripts/scan_cycle2797_raw.json"'
P6_NEW = 'RAW = "/home/z/my-project/scripts/scan_cycle2798_raw.json"'
P7_OLD = 'PRETTY = "/home/z/my-project/scripts/scan_cycle2797.json"'
P7_NEW = 'PRETTY = "/home/z/my-project/scripts/scan_cycle2798.json"'
P9_OLD = 'check("drift49_pass46_match", comp_ok,'
P9_NEW = 'check("drift49_pass47_match", comp_ok,'
P10_OLD = "# --- classification gates (SOFT — DRIFT-#49 pass-46 vs RESTORATION vs newest-observation) ---"
P10_NEW = "# --- classification gates (SOFT — DRIFT-#49 pass-47 vs RESTORATION vs newest-observation) ---"
P11_OLD = ('if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-46 '
           '(movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) '
           'remains LOCKED, never rewritten)"\nelif comp_ok:\n    '
           'classification = "DRIFT-#49 pass-46 (movement repeat-class, size '
           'drifted) - size movement noted"')
P11_NEW = ('if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-47 '
           '(movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) '
           'remains LOCKED, never rewritten)"\nelif comp_ok:\n    '
           'classification = "DRIFT-#49 pass-47 (movement repeat-class, size '
           'drifted) - size movement noted"')

patches = [("P1 title", P1_OLD, P1_NEW), ("P2 provenance", p2_old, p2_new),
           ("P3 evidence (lag-1)", p3_old, p3_new), ("P4 contract", P4_OLD, P4_NEW),
           ("P5 cycle", P5_OLD, P5_NEW), ("P6 raw path", P6_OLD, P6_NEW),
           ("P7 pretty path", P7_OLD, P7_NEW), ("P8 size band (lag-1)", p8_old, p8_new),
           ("P9 gate rename", P9_OLD, P9_NEW), ("P10 comment", P10_OLD, P10_NEW),
           ("P11 block", P11_OLD, P11_NEW)]

for tag, old, new in patches:
    if src.count(old) != 1:
        fail.append(f"{tag}: old count={src.count(old)} (expect 1)")
    if new in src:
        fail.append(f"{tag}: new already present in src")
if fail:
    print("GEN_ABORTED:", "; ".join(fail))
    sys.exit(1)

DOC = '''#!/usr/bin/env python3
"""Rebadge gate for cycle 2798: validate_cycle2797.py -> validate_cycle2798.py.

The REBADGE-CLASS continues (the v97 source survived on disk and in the
98db775 commit object — object-verified at guard time). Every patch asserts
its old string occurs EXACTLY once in the source BEFORE any mutation;
abort = zero files written. Post-patch: selective no-old-token assertions +
py_compile. Patch count is counted programmatically.
DRIFT-#49 pass-47 spec (per the c2797 Next-block): baseline = the pass-1
observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement
since LOSS-#83; pass-2 repeat recorded at c2753; ... pass-45 repeat recorded
at c2796; pass-46 repeat recorded at c2797); a repeat -> pass-47 recorded
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never
rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the
root stands, the pass-1 excursion closes as a transient); any other
composition -> newest-observation evidence with the full delta chain printed.
The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2797
attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761
attempt-1 P8 lesson): the v97 source carries 'pass-45 band' AND 'pass-45
evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class
name.
Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching):
the official c2797 commit hash 98db775 short form = 9-8-d-b-7-7-5 carries NO
'c' character at all — NO c+4-digit run possible, zero hash-artifact exposure;
the v98 P2 paragraph carries 'the 98db775 commit object' (zero new
hash-artifact birth), while the v97 P2 carry 'the 1baacec commit object'
rebadges AWAY (1baacec carries its 'c' characters WITHOUT a following 4-digit
run — 'ce' after the position-5 'c' + the final 'c' digitless — zero token
deaths — the c7947 class does NOT fire); the foreign TOP 65f4c4e short
form = 6-5-f-4-c-4-e — its 'c' character sits at position 5 followed by the
single digit '4' then 'e', so NO c+4-digit run is present (zero exposure); the
c2798 commit hash is unborn at patch time, checked post-commit.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2797.py"
DST = "/home/z/my-project/scripts/validate_cycle2798.py"

PATCHES = [
'''

TAIL = ''']

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
for token in ("CYCLE = 2797", "scan_cycle2797", "Validator for cycle 2797",
              "drift49_pass46_match", "pass-46 (movement repeat-class recorded",
              "pass-46 (movement repeat-class, size drifted",
              "pass-45 band", "pass-45 evidence"):
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
if "drift49_pass47_match" not in out or "pass-47" not in out:
    print("FAIL: pass-47 class wiring lost")
    failures.append("pass47-wiring")
if "c7947" in out:
    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")
    failures.append("c7947-remains")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2797.py -> validate_cycle2798.py (11 patches, pass-47 spec)")
'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(DOC)
    for tag, old, new in patches:
        f.write(f"    # {tag}\n")
        f.write(f"    ({old!r},\n     {new!r}),\n")
    f.write(TAIL)
print(f"generated {OUT}")
