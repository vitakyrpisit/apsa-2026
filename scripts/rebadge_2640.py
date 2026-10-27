#!/usr/bin/env python3
"""Rebadge validate_cycle2639.py -> validate_cycle2640.py (DRIFT-#45 verification-18 CARRY).

PROACTIVE lesson applied (sixteenth cycle running): all anchors pre-verified against the
ACTUAL validate_cycle2639.py bytes BEFORE this script was written:
  - sed source: 6 literal '2639' tokens (lines 2/8/9/44/45/46); the f-string
    baseline_match_c{CYCLE} is a TEMPLATE and is NOT counted.
  - P1 anchor 'verification-17 CARRY (root declared 2026-10-27 ~06:04 +08): rebadged
    from validate_cycle2638.py' count == 1.
  - line-8 anchor 'root; c2639 = DRIFT-#45 verification 17' count == 1 (pre-sed).
  - chain anchor '(c2639 = DRIFT-#45 verification 17; c2638 = DRIFT-#45 verification 16'
    count == 1 (pre-sed, the '(' disambiguator vs the line-8 'root; ' form).
Post-sed ambiguity notes: the bare head string appears 2x post-sed (line-8 'root; '
form + chain '(' form) — both patches use their disambiguators; expected order:
P1 FIRST (before line-8/chain bumps renumber verification levels), then line-8 bump,
then chain insert (anchors do not collide).
"""
import py_compile
import shutil

SRC = "/home/z/my-project/scripts/validate_cycle2639.py"
DST = "/home/z/my-project/scripts/validate_cycle2640.py"

shutil.copyfile(SRC, DST)
with open(DST, "r") as f:
    txt = f.read()

def assert_count(s, sub, n, label):
    c = s.count(sub)
    assert c == n, f"{label}: expected {n}, got {c}"

# --- Stage 1: sed 2639 -> 2640 (assert exactly 6 replacements) ---
assert_count(txt, "2639", 6, "sed source literal '2639' tokens")
txt = txt.replace("2639", "2640")
assert_count(txt, "2640", 6, "post-sed literal '2640' tokens")

# --- Stage 2: P1 header patch (verification-17 -> verification-18 CARRY, pointer 2638 -> 2639) ---
P1_OLD = ("verification-17 CARRY (root declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2638.py")
P1_NEW = ("verification-18 CARRY (root declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2639.py")
assert_count(txt, P1_OLD, 1, "P1 anchor")
txt = txt.replace(P1_OLD, P1_NEW)
assert_count(txt, P1_NEW, 1, "P1 patched")

# --- Stage 3: line-8 bump (root; disambiguator) ---
L8_OLD = "root; c2640 = DRIFT-#45 verification 17"
L8_NEW = "root; c2640 = DRIFT-#45 verification 18"
assert_count(txt, L8_OLD, 1, "line-8 anchor ('root; ' form)")
txt = txt.replace(L8_OLD, L8_NEW)

# --- Stage 4: chain insert ('(' disambiguator) — restore the c2639 line, head 17 -> 18 ---
CH_OLD = ("(c2640 = DRIFT-#45 verification 17; "
          "c2638 = DRIFT-#45 verification 16")
CH_NEW = ("(c2640 = DRIFT-#45 verification 18; "
          "c2639 = DRIFT-#45 verification 17; "
          "c2638 = DRIFT-#45 verification 16")
assert_count(txt, CH_OLD, 1, "chain anchor ('(' form)")
txt = txt.replace(CH_OLD, CH_NEW)

# --- P-HIST spot checks (steady-state rule) ---
CHECKS = [
    ("2640", 6),   # self (docstring + line-8 + chain head + CYCLE + RAW + PRETTY)
    ("2639", 2),   # rebadged-from pointer + restored chain line
    ("2638", 1),   # chain verification line only (pointer moved off)
    ("2637", 1),   # chain
    ("2636", 1),   # chain
    ("2635", 1),   # chain
    ("2634", 1),   # chain
    ("2633", 1),   # chain
    ("2632", 1),   # chain
    ("2631", 1),   # chain
    ("2630", 1),   # chain
    ("2629", 1),   # chain
    ("2628", 1),   # chain
    ("2627", 1),   # chain
    ("2626", 1),   # chain
    ("2625", 1),   # chain
    ("2624", 1),   # chain
    ("2623", 1),   # chain ROOT line only
    ("2622", 1),   # DRIFT-#44 chain line
    ("2621", 1),   # DRIFT-#44 chain line
    ("2620", 1),   # DRIFT-#44 chain line
    ("2619", 2),   # chain ROOT line + DRIFT-#44 closure cite
    ("2618", 2),   # chain line + DRIFT-#43 closure cite
    ("2606", 2),   # chain root line + DRIFT-#42 closure cite
    ("2594", 2),   # chain root line + DRIFT-#41 closure cite
]
for tok, n in CHECKS:
    c = txt.count(tok)
    assert c == n, f"P-HIST {tok}: expected {n}, got {c}"
print("P-HIST spot checks PASSED:", ", ".join(f"{t}=={n}" for t, n in CHECKS))

with open(DST, "w") as f:
    f.write(txt)

py_compile.compile(DST, doraise=True)
print(f"rebadge OK: {DST} (py_compile OK)")
