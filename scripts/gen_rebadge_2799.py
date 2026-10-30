#!/usr/bin/env python3
"""Authoring harness for rebadge_cycle2799.py — the c2798 gen_rebadge_2798.py
precedent. Extracts the P2/P3/P8 old-paragraphs VERBATIM from the ACTUAL v98
source bytes (measured, never hand-copied), builds the new-strings via
asserted unique replacements, and EMITS rebadge_cycle2799.py with all eleven
patches embedded. The emitted rebadge script re-validates every old-string
count==1 before mutating (abort = zero files written)."""
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2798.py"
OUT = "/home/z/my-project/scripts/rebadge_cycle2799.py"

src = open(SRC, encoding="utf-8").read()
fail = []


def extract(start, end, tag):
    i = src.find(start)
    j = src.find(end, i if i >= 0 else 0)
    if i < 0 or j < 0 or src.count(start) != 1 or src.count(end) != 1:
        fail.append(f"{tag}: anchor not unique/found (start={src.count(start)} end={src.count(end)})")
        return ""
    return src[i:j + len(end)]


p2_old = extract("DRIFT-#49 pass-47 CLASS (movement repeat-class on tuple match) — sed-rebadge",
                 "(the v45 76/76 off-by-one class is retired).", "P2")
p3_old = extract("DRIFT-#49 pass-46 evidence (on disk): five-tuple",
                 "repeat-class — the scam block 18 stands). The", "P3")
p8_old = extract("SIZE_BAND = (446, 447)  # DRIFT-#49 pass-46 band @ 446B (observed ",
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
p2_new = replace_once(p2_new, "pass-47 CLASS", "pass-48 CLASS", "P2-t1")
p2_new = replace_once(p2_new, "from the v97 pass-46 carry", "from the v98 pass-47 carry", "P2-t2")
p2_new = replace_once(p2_new, "the v97 source survived on disk and in the\n98db775 commit object",
                      "the v98 source survived on disk and in the\n9261c07 commit object", "P2-t3")
p2_new = replace_once(p2_new, "Baseline for c2798 = the", "Baseline for c2799 = the", "P2-t4")
p2_new = replace_once(p2_new, "at c2795; pass-45 repeat recorded\nat c2796; pass-46 repeat recorded\nat c2797); a repeat records pass-47",
                      "at c2795; pass-45 repeat recorded\nat c2796; pass-46 repeat recorded\nat c2797; pass-47 repeat recorded\nat c2798); a repeat records pass-48", "P2-t5")
p2_new = replace_once(p2_new, "Structural conventions inherited from the v97 class (itself\ninheriting the v96/v95/v94/v93/v92/v91/v90/v89/",
                      "Structural conventions inherited from the v98 class (itself\ninheriting the v97/v96/v95/v94/v93/v92/v91/v90/v89/", "P2-t6")

p3_new = p3_old
p3_new = replace_once(p3_new, "pass-46 evidence (on disk)", "pass-47 evidence (on disk)", "P3-t1")
p3_new = replace_once(p3_new, "c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797 (pass-1 opens",
                      "c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798 (pass-1 opens", "P3-t2")
p3_new = replace_once(p3_new, "pass-46 repeats\nat c2797, movement",
                      "pass-46 repeats\nat c2797; pass-47 repeats\nat c2798, movement", "P3-t3")

p8_new = p8_old
p8_new = replace_once(p8_new, "pass-46 band @ 446B", "pass-47 band @ 446B", "P8-t1")
p8_new = replace_once(p8_new, "c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797; the DRIFT-#48 root band",
                      "c2790/c2791/c2792/c2793/c2794/c2795/c2796/c2797/c2798; the DRIFT-#48 root band", "P8-t2")

if fail:
    print("GEN_ABORTED:", "; ".join(fail))
    sys.exit(1)

P1_OLD = '"""Validator for cycle 2798.'
P1_NEW = '"""Validator for cycle 2799.'
P4_OLD = "Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-47 recorded,"
P4_NEW = "Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-48 recorded,"
P5_OLD = "CYCLE = 2798"
P5_NEW = "CYCLE = 2799"
P6_OLD = 'RAW = "/home/z/my-project/scripts/scan_cycle2798_raw.json"'
P6_NEW = 'RAW = "/home/z/my-project/scripts/scan_cycle2799_raw.json"'
P7_OLD = 'PRETTY = "/home/z/my-project/scripts/scan_cycle2798.json"'
P7_NEW = 'PRETTY = "/home/z/my-project/scripts/scan_cycle2799.json"'
P9_OLD = 'check("drift49_pass47_match", comp_ok,'
P9_NEW = 'check("drift49_pass48_match", comp_ok,'
P10_OLD = "# --- classification gates (SOFT — DRIFT-#49 pass-47 vs RESTORATION vs newest-observation) ---"
P10_NEW = "# --- classification gates (SOFT — DRIFT-#49 pass-48 vs RESTORATION vs newest-observation) ---"
P11_OLD = ('if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-47 '
           '(movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) '
           'remains LOCKED, never rewritten)"\nelif comp_ok:\n    '
           'classification = "DRIFT-#49 pass-47 (movement repeat-class, size '
           'drifted) - size movement noted"')
P11_NEW = ('if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-48 '
           '(movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) '
           'remains LOCKED, never rewritten)"\nelif comp_ok:\n    '
           'classification = "DRIFT-#49 pass-48 (movement repeat-class, size '
           'drifted) - size movement noted"')

patches = [("P1 title", P1_OLD, P1_NEW), ("P2 provenance", p2_old, p2_new),
           ("P3 evidence (lag-1)", p3_old, p3_new), ("P4 contract", P4_OLD, P4_NEW),
           ("P5 cycle", P5_OLD, P5_NEW), ("P6 raw path", P6_OLD, P6_NEW),
           ("P7 pretty path", P7_OLD, P7_NEW), ("P8 size band (lag-1)", p8_old, p8_new),
           ("P9 gate rename", P9_OLD, P9_NEW), ("P10 comment", P10_OLD, P10_NEW),
           ("P11 block", P11_OLD, P11_NEW)]

POST_OLD_TOKENS = ["CYCLE = 2798", "scan_cycle2798", "Validator for cycle 2798",
                   "drift49_pass47_match", "pass-47 (movement repeat-class recorded",
                   "pass-47 (movement repeat-class, size drifted",
                   "pass-46 band", "pass-46 evidence"]
POST_MUST = ["(20,0,2,18,0)", "(21,0,3,18,0)", "(18,0,0,18,0)", "DRIFT48_ROOT",
             "restoration_ok", "drift49_pass48_match", "pass-48"]

# --- emit rebadge_cycle2799.py ---
lines = []
lines.append('#!/usr/bin/env python3')
lines.append('"""Rebadge gate for cycle 2799: validate_cycle2798.py -> validate_cycle2799.py.')
lines.append('')
lines.append('The REBADGE-CLASS continues (the v98 source survived on disk and in the')
lines.append('9261c07 commit object — object-verified at guard time). Every patch asserts')
lines.append('its old string occurs EXACTLY once in the source BEFORE any mutation;')
lines.append('abort = zero files written. Post-patch: selective no-old-token assertions +')
lines.append('py_compile. Patch count is counted programmatically.')
lines.append('DRIFT-#49 pass-48 spec (per the c2798 Next-block): baseline = the pass-1')
lines.append('observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement')
lines.append('since LOSS-#83; pass-2 repeat recorded at c2753; ... pass-46 repeat recorded')
lines.append('at c2797; pass-47 repeat recorded at c2798); a repeat -> pass-48 recorded')
lines.append('(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never')
lines.append('rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the')
lines.append('root stands, the pass-1 excursion closes as a transient); any other')
lines.append('composition -> newest-observation evidence with the full delta chain printed.')
lines.append('The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2798')
lines.append('attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761')
lines.append('attempt-1 P8 lesson): the v98 source carries \'pass-46 band\' AND \'pass-46')
lines.append("evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class")
lines.append('name.')
lines.append('Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching):')
lines.append('the official c2798 commit hash 9261c07 short form = 9-2-6-1-c-0-7 carries its')
lines.append("'c' character at position 5 followed by the TWO digits '07' then '4' (full")
lines.append("form 'c074d') — NO c+4-digit run possible, zero hash-artifact exposure;")
lines.append("the v99 P2 paragraph carries 'the 9261c07 commit object' (zero new")
lines.append("hash-artifact birth), while the v98 P2 carry 'the 98db775 commit object'")
lines.append("rebadges AWAY (98db775 carries NO 'c' character at all — zero token deaths")
lines.append('— the c7947 class does NOT fire); the foreign TOP b27a69f short')
lines.append('form = b-2-7-a-6-9-f carries NO \'c\' character at all (zero exposure); the')
lines.append('c2799 commit hash is unborn at patch time, checked post-commit.')
lines.append('"""')
lines.append('import py_compile')
lines.append('import sys')
lines.append('')
lines.append('SRC = "/home/z/my-project/scripts/validate_cycle2798.py"')
lines.append('DST = "/home/z/my-project/scripts/validate_cycle2799.py"')
lines.append('')
lines.append('PATCHES = [')


def lit(s):
    return repr(s)


for name, old, new in patches:
    lines.append(f"    # {name}")
    lines.append(f"    ({lit(old)},")
    lines.append(f"     {lit(new)}),")
lines.append(']')
lines.append('')
lines.append('src_data = open(SRC).read()')
lines.append('failures = []')
lines.append('for i, (old, new) in enumerate(PATCHES, 1):')
lines.append('    n = src_data.count(old)')
lines.append('    tag = f"P{i}"')
lines.append('    if n != 1:')
lines.append('        failures.append(f"{tag}: old string count={n} (expect 1)")')
lines.append('        print(f"FAIL: {tag} old-count={n}")')
lines.append('    else:')
lines.append('        print(f"ok: {tag} old-count=1")')
lines.append('')
lines.append('if failures:')
lines.append('    print(f"REBADGE_ABORTED: {len(failures)} patch-gate failures - NO files written")')
lines.append('    sys.exit(1)')
lines.append('')
lines.append('out = src_data')
lines.append('for old, new in PATCHES:')
lines.append('    out = out.replace(old, new)')
lines.append('open(DST, "w").write(out)')
lines.append('')
lines.append('# post-patch selective assertions')
lines.append('for token in (' + ", ".join(repr(t) for t in POST_OLD_TOKENS) + '):')
lines.append('    if token in out:')
lines.append('        print(f"FAIL: old token remains: {token}")')
lines.append('        failures.append(token)')
lines.append('if "(20,0,2,18,0)" not in out:')
lines.append('    print("FAIL: locked-root reference lost")')
lines.append('    failures.append("root-reference")')
lines.append('if "(21,0,3,18,0)" not in out:')
lines.append('    print("FAIL: context-carried superseded root reference lost")')
lines.append('    failures.append("superseded-root-reference")')
lines.append('if "(18,0,0,18,0)" not in out:')
lines.append('    print("FAIL: pass-1 observation baseline reference lost")')
lines.append('    failures.append("pass1-observation-reference")')
lines.append('if "DRIFT48_ROOT" not in out or "restoration_ok" not in out:')
lines.append('    print("FAIL: RESTORATION gate wiring lost")')
lines.append('    failures.append("restoration-wiring")')
lines.append('if "drift49_pass48_match" not in out or "pass-48" not in out:')
lines.append('    print("FAIL: pass-48 class wiring lost")')
lines.append('    failures.append("pass48-wiring")')
lines.append('if "c7947" in out:')
lines.append('    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")')
lines.append('    failures.append("c7947-remains")')
lines.append('')
lines.append('py_compile.compile(DST, doraise=True)')
lines.append('print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")')
lines.append('print(f"py_compile=CLEAN dst={DST}")')
lines.append('if failures:')
lines.append('    print(f"REBADGE_POST_RED: {len(failures)}")')
lines.append('    sys.exit(1)')
lines.append('print("REBADGE_GREEN: validate_cycle2798.py -> validate_cycle2799.py (11 patches, pass-48 spec)")')

open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"rebadge_cycle2799.py emitted: {len(lines)} lines")
print("P2 old-paragraph bytes:", len(p2_old))
print("P3 old-paragraph bytes:", len(p3_old))
print("P8 old-paragraph bytes:", len(p8_old))
