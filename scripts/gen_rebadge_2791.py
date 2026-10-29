#!/usr/bin/env python3
"""Build rebadge_cycle2791.py from the v90 source with byte-exact paragraphs.

Constructs the 11-patch rebadge (v90 -> v91) embedding the P2/P3/P8 paragraph
old-strings extracted VERBATIM from validate_cycle2790.py (measured, never
hand-copied). The generator applies the transform rules to produce the new
strings, verifies each old string count==1 in the v90 source and each new
string count==1 in the transformed output, then writes rebadge_cycle2791.py.
"""
SRC = "/home/z/my-project/scripts/validate_cycle2790.py"
OUT = "/home/z/my-project/scripts/rebadge_cycle2791.py"

src = open(SRC).read()

# --- extract exact paragraphs ---
i = src.index('DRIFT-#49 pass-39 CLASS')
j = src.index('(the v45 76/76 off-by-one class is retired).') + len('(the v45 76/76 off-by-one class is retired).')
P2_OLD = src[i:j]
k = src.index('DRIFT-#49 pass-38 evidence (on disk):')
l = src.index('scam block 18 stands). The') + len('scam block 18 stands). The')
P3_OLD = src[k:l]
P8_OLD = [ln for ln in src.splitlines() if ln.startswith('SIZE_BAND =')][0]

assert src.count(P2_OLD) == 1 and src.count(P3_OLD) == 1 and src.count(P8_OLD) == 1


def lit(s):
    """Render a string as a python literal split into readable chunks."""
    return repr(s)


P2_NEW = (P2_OLD
          .replace('DRIFT-#49 pass-39 CLASS', 'DRIFT-#49 pass-40 CLASS')
          .replace('from the v89 pass-38 carry (the v89 source survived on disk and in the\n2af9fd7 commit object',
                   'from the v90 pass-39 carry (the v90 source survived on disk and in the\ne4a79df commit object')
          .replace('Baseline for c2790 = the', 'Baseline for c2791 = the')
          .replace('at c2788; pass-38 repeat recorded\nat c2789); a repeat records pass-39',
                   'at c2788; pass-38 repeat recorded\nat c2789; pass-39 repeat recorded\nat c2790); a repeat records pass-40')
          .replace('inherited from the v89 class (itself\ninheriting the v88/',
                   'inherited from the v90 class (itself\ninheriting the v89/v88/'))
P3_NEW = (P3_OLD
          .replace('DRIFT-#49 pass-38 evidence', 'DRIFT-#49 pass-39 evidence')
          .replace('c2787/c2788/c2789 (pass-1 opens at c2752',
                   'c2787/c2788/c2789/c2790 (pass-1 opens at c2752')
          .replace('at c2788; pass-38 repeats\nat c2789, movement',
                   'at c2788; pass-38 repeats\nat c2789; pass-39 repeats\nat c2790, movement'))
P8_NEW = (P8_OLD
          .replace('pass-38 band', 'pass-39 band')
          .replace('/c2788/c2789; the DRIFT-#48 root band', '/c2788/c2789/c2790; the DRIFT-#48 root band'))

assert P2_NEW != P2_OLD and P3_NEW != P3_OLD and P8_NEW != P8_OLD

PATCHES = [
    ("P1 title", '"""Validator for cycle 2790.', '"""Validator for cycle 2791.'),
    ("P2 provenance paragraph", P2_OLD, P2_NEW),
    ("P3 evidence paragraph (lag-1)", P3_OLD, P3_NEW),
    ("P4 contract sentence",
     'Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-39 recorded,',
     'Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-40 recorded,'),
    ("P5 cycle constant", "CYCLE = 2790", "CYCLE = 2791"),
    ("P6 raw path",
     'RAW = "/home/z/my-project/scripts/scan_cycle2790_raw.json"',
     'RAW = "/home/z/my-project/scripts/scan_cycle2791_raw.json"'),
    ("P7 pretty path",
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2790.json"',
     'PRETTY = "/home/z/my-project/scripts/scan_cycle2791.json"'),
    ("P8 size band comment (lag-1)", P8_OLD, P8_NEW),
    ("P9 gate rename",
     'check("drift49_pass39_match", comp_ok,',
     'check("drift49_pass40_match", comp_ok,'),
    ("P10 classification comment",
     '# --- classification gates (SOFT — DRIFT-#49 pass-39 vs RESTORATION vs newest-observation) ---',
     '# --- classification gates (SOFT — DRIFT-#49 pass-40 vs RESTORATION vs newest-observation) ---'),
    ("P11 classification block",
     'if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-39 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-39 (movement repeat-class, size drifted) - size movement noted"',
     'if comp_ok and size_ok:\n    classification = "DRIFT-#49 pass-40 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"\nelif comp_ok:\n    classification = "DRIFT-#49 pass-40 (movement repeat-class, size drifted) - size movement noted"'),
]

# verify every old count==1 and every new count==1 post-transform
probe = src
for name, old, new in PATCHES:
    c = probe.count(old)
    assert c == 1, f"{name}: old count={c}"
    probe = probe.replace(old, new)
for name, old, new in PATCHES:
    c = probe.count(new)
    assert c == 1, f"{name}: new count={c} post-transform"
    assert probe.count(old) == 0, f"{name}: old remains"

# render the rebadge script
def q(s):
    """Python literal with safe line wrapping (single quoted repr)."""
    return repr(s)

lines = []
lines.append('#!/usr/bin/env python3')
lines.append('"""Rebadge gate for cycle 2791: validate_cycle2790.py -> validate_cycle2791.py.')
lines.append('')
lines.append('The REBADGE-CLASS continues (the v90 source survived on disk and in the')
lines.append('e4a79df commit object — object-verified at guard time). Every patch asserts')
lines.append('its old string occurs EXACTLY once in the source BEFORE any mutation;')
lines.append('abort = zero files written. Post-patch: selective no-old-token assertions +')
lines.append('py_compile. Patch count is counted programmatically.')
lines.append('DRIFT-#49 pass-40 spec (per the c2790 Next-block): baseline = the pass-1')
lines.append('observation (18,0,0,18,0) @ 446B (opened at c2752 — the first market movement')
lines.append('since LOSS-#83; pass-2 repeat recorded at c2753; ... pass-38 repeat recorded')
lines.append('at c2789; pass-39 repeat recorded at c2790); a repeat -> pass-40 recorded')
lines.append('(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never')
lines.append('rewritten); a return to (20,0,2,18,0) -> the RESTORATION event recorded (the')
lines.append('root stands, the pass-1 excursion closes as a transient); any other')
lines.append('composition -> newest-observation evidence with the full delta chain printed.')
lines.append('The lag-1 pattern spans BOTH instrument surfaces (the c2772..c2790')
lines.append('attempt-1 clean runs + the c2770 attempt-1 P3 abort lesson + the c2761')
lines.append('attempt-1 P8 lesson): the v90 source carries \'pass-38 band\' AND \'pass-38')
lines.append("evidence' — this rebadge's P3/P8 old-strings expect the lag, not the class")
lines.append('name.')
lines.append('Hash-artifact watch (the c3819e9 + c7947 lessons — checked BEFORE patching):')
lines.append('the official c2790 commit hash e4a79df short form = e-4-a-7-9-d-f — it')
lines.append("carries NO 'c' character at all, so NO c+4-digit run is present and the")
lines.append('hash-artifact class does NOT fire this cycle; the v91 P2 paragraph carries')
lines.append("'the e4a79df commit object' (zero new hash-artifact birth), while the v90 P2")
lines.append("carry 'the 2af9fd7 commit object' rebadges AWAY (2af9fd7 also carries no")
lines.append("'c', so zero token deaths — the c7947 class does NOT fire); the foreign TOP")
lines.append('3b69581 short form = 3-b-6-9-5-8-1 — it carries NO \'c\' character either')
lines.append('(zero c+4-digit run, zero exposure); the c2791 commit hash is unborn at')
lines.append('patch time, checked post-commit.')
lines.append('"""')
lines.append('import py_compile')
lines.append('import sys')
lines.append('')
lines.append('SRC = "/home/z/my-project/scripts/validate_cycle2790.py"')
lines.append('DST = "/home/z/my-project/scripts/validate_cycle2791.py"')
lines.append('')
lines.append('PATCHES = [')
for name, old, new in PATCHES:
    lines.append(f'    # {name}')
    lines.append(f'    ({q(old)},')
    lines.append(f'     {q(new)}),')
lines.append(']')
lines.append('''
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
for token in ("CYCLE = 2790", "scan_cycle2790", "Validator for cycle 2790",
              "drift49_pass39_match", "pass-39 (movement repeat-class recorded",
              "pass-39 (movement repeat-class, size drifted",
              "pass-38 band", "pass-38 evidence"):
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
if "drift49_pass40_match" not in out or "pass-40" not in out:
    print("FAIL: pass-40 class wiring lost")
    failures.append("pass40-wiring")
if "c7947" in out:
    print("FAIL: the c7947 hash-artifact token remains (dead since v88)")
    failures.append("c7947-remains")

py_compile.compile(DST, doraise=True)
print(f"PATCH_COUNT={len(PATCHES)} (programmatic)")
print(f"py_compile=CLEAN dst={DST}")
if failures:
    print(f"REBADGE_POST_RED: {len(failures)}")
    sys.exit(1)
print("REBADGE_GREEN: validate_cycle2790.py -> validate_cycle2791.py (11 patches, pass-40 spec)")''')

open(OUT, "w").write("\n".join(lines) + "\n")
print(f"written {OUT} bytes={len(chr(10).join(lines)) + 1}")
print("P2_old bytes:", len(P2_OLD), "| P3_old bytes:", len(P3_OLD), "| P8_old bytes:", len(P8_OLD))
