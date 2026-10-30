#!/usr/bin/env python3
"""Diff-verify post-check for the c2819 rebadge (v118 -> v119).

Verifies the rebadge changed ONLY the expected patch regions: unified diff of
validate_cycle2818.py vs validate_cycle2819.py; counts removed/added lines and
hunks; asserts every changed line sits inside one of the 11 patch regions
(measured against both sides' bytes pre-run). Expected shape per the standing
class: 40 changed lines (19 removed + 21 added, 13 hunks) — the +2 net lines
come from the P2 pass-chain growth and the P3 pass-chain growth.
"""
import difflib
import sys

A = "/home/z/my-project/scripts/validate_cycle2818.py"
B = "/home/z/my-project/scripts/validate_cycle2819.py"

a_lines = open(A, encoding="utf-8").read().splitlines()
b_lines = open(B, encoding="utf-8").read().splitlines()
print(f"v118_lines={len(a_lines)} v119_lines={len(b_lines)}")
print(f"v118_bytes={len(open(A, 'rb').read())} v119_bytes={len(open(B, 'rb').read())}")


def region_of(line):
    if "Validator for cycle" in line:
        return "title"
    if line.startswith("CYCLE = "):
        return "CYCLE"
    if line.startswith("RAW = "):
        return "RAW"
    if line.startswith("PRETTY = "):
        return "PRETTY"
    if line.startswith("SIZE_BAND = "):
        return "SIZE_BAND"
    if "--- classification gates (SOFT" in line:
        return "SOFT-comment"
    if "drift49_pass" in line and "comp_ok" in line:
        return "gate"
    if "classification = " in line or line.startswith("if comp_ok"):
        return "block"
    if "Baseline gates are CLASSIFICATION" in line:
        return "contract"
    # P2/P3 provenance + evidence prose (the docstring region)
    p2p3_markers = (
        "DRIFT-#49 pass-", "sed-rebadge", "carry (the v1", "commit object",
        "Baseline for c28", "repeat recorded", "repeats", "at c2", "movement",
        "repeat-class", "a repeat records pass-", "a return to", "any other",
        "composition records newest-observation", "printed. Structural",
        "Structural conventions inherited", "inheriting the v", "conventions). Gate count",
        "the v45 76/76 off-by-one", "pass-1 opens", "market movement since LOSS-#83",
        "EXITED the market", "scam block 18 stands", "LOCKED", "RESTORATION",
        "superseded", "Tuple components", "the DRIFT-#48 root",
        "evidence (on disk)", "observation", "5-tuple", "five-tuple",
    )
    if any(m in line for m in p2p3_markers):
        return "P2/P3-prose"
    # pure observed-list path lines (c-token chains)
    import re as _re
    if _re.fullmatch(r"[a-z0-9/]*c\d{4}[/a-z0-9]*", line.strip()) and "/" in line:
        return "observed-list"
    return None


sm = difflib.SequenceMatcher(None, a_lines, b_lines, autojunk=False)
removed = []
added = []
hunks = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    hunks += 1
    removed.extend((i1 + k + 1, a_lines[i1 + k]) for k in range(i2 - i1))
    added.extend((j1 + k + 1, b_lines[j1 + k]) for k in range(i2 - i1 if False else j2 - j1))

print(f"changed_lines={len(removed) + len(added)} (removed={len(removed)} + added={len(added)}) hunks={hunks}")

failures = []
print("removed lines (v118 line numbers):")
for ln, txt in removed:
    r = region_of(txt)
    print(f"  -{ln} [{r}] {txt[:96]}")
    if r is None:
        failures.append(f"removed line {ln} outside regions: {txt[:60]!r}")
print("added lines (v119 line numbers):")
for ln, txt in added:
    r = region_of(txt)
    print(f"  +{ln} [{r}] {txt[:96]}")
    if r is None:
        failures.append(f"added line {ln} outside regions: {txt[:60]!r}")

print("region table (measured):")
for name, lines_ in (("v118", a_lines), ("v119", b_lines)):
    marks = {}
    for i, l in enumerate(lines_, 1):
        if "Baseline gates are CLASSIFICATION" in l:
            marks.setdefault("contract", i)
        if l.startswith("CYCLE = "):
            marks.setdefault("CYCLE", i)
        if l.startswith("RAW = "):
            marks.setdefault("RAW", i)
        if l.startswith("PRETTY = "):
            marks.setdefault("PRETTY", i)
        if l.startswith("SIZE_BAND = "):
            marks.setdefault("SIZE_BAND", i)
        if "--- classification gates (SOFT" in l:
            marks.setdefault("SOFT-comment", i)
        if "drift49_pass" in l and "comp_ok" in l:
            marks.setdefault("gate", i)
        if l.startswith("if comp_ok and size_ok:"):
            marks.setdefault("block-if", i)
        if "classification = " in l and "size drifted" in l:
            marks.setdefault("block-elif", i)
    print(f"  {name}: " + " / ".join(f"{k} {v}" for k, v in sorted(marks.items(), key=lambda kv: kv[1])))

if failures:
    print(f"DIFF_VERIFY_RED: {len(failures)}")
    for f_ in failures:
        print(f"  - {f_}")
    sys.exit(1)
print("DIFF_VERIFY_GREEN: every changed line inside the expected patch regions")
