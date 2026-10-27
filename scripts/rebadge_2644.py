#!/usr/bin/env python3
"""Rebadge validate_cycle2643.py -> validate_cycle2644.py (DRIFT-#45 verification-22 CARRY).

PROACTIVE lesson applied (twentieth cycle running): all anchors pre-verified against the
ACTUAL validate_cycle2643.py bytes BEFORE this script was written:
  - sed source: 6 literal '2643' tokens (docstring + line-8 + chain head + CYCLE +
    RAW + PRETTY); the f-string baseline_match_c{CYCLE} is a TEMPLATE and NOT counted.
    VERIFIED count == 6.
  - P1 anchor 'verification-21 CARRY (root declared 2026-10-27 ~06:04 +08): rebadged
    from validate_cycle2642.py' VERIFIED count == 1.
  - line-8 anchor 'root; c2643 = DRIFT-#45 verification 21' — the 'root; ' prefix is
    the disambiguator; bare head appears 2x (line-8 + chain '(' form) VERIFIED == 2.
  - chain anchor '(c2643 = DRIFT-#45 verification 21; c2642 = DRIFT-#45 verification 20'
    VERIFIED count == 1 (the '(' disambiguator).
Post-sed ambiguity notes: the bare head string appears 2x post-sed (line-8 'root; '
form + chain '(' form) — both patches use their disambiguators; expected order:
P1 FIRST (before line-8/chain bumps renumber verification levels), then line-8 bump,
then chain insert (anchors do not collide).
"""
import py_compile
import shutil

SRC = "/home/z/my-project/scripts/validate_cycle2643.py"
DST = "/home/z/my-project/scripts/validate_cycle2644.py"

shutil.copyfile(SRC, DST)
with open(DST, "r") as f:
    txt = f.read()

def assert_count(s, sub, n, label):
    c = s.count(sub)
    assert c == n, f"{label}: expected {n}, got {c}"

# --- Stage 1: sed 2643 -> 2644 (assert exactly 6 replacements) ---
assert_count(txt, "2643", 6, "sed source literal '2643' tokens")
txt = txt.replace("2643", "2644")
assert_count(txt, "2644", 6, "post-sed literal '2644' tokens")

# --- Stage 2: P1 header patch (verification-21 -> verification-22 CARRY, pointer 2642 -> 2643) ---
P1_OLD = ("verification-21 CARRY (root declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2642.py")
P1_NEW = ("verification-22 CARRY (root declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2643.py")
assert_count(txt, P1_OLD, 1, "P1 anchor")
txt = txt.replace(P1_OLD, P1_NEW)
assert_count(txt, P1_NEW, 1, "P1 patched")

# --- Stage 3: line-8 bump (root; disambiguator) ---
L8_OLD = "root; c2644 = DRIFT-#45 verification 21"
L8_NEW = "root; c2644 = DRIFT-#45 verification 22"
assert_count(txt, L8_OLD, 1, "line-8 anchor ('root; ' form)")
txt = txt.replace(L8_OLD, L8_NEW)

# --- Stage 4: chain insert ('(' disambiguator) — restore the c2643 line, head 21 -> 22 ---
CH_OLD = ("(c2644 = DRIFT-#45 verification 21; "
          "c2642 = DRIFT-#45 verification 20")
CH_NEW = ("(c2644 = DRIFT-#45 verification 22; "
          "c2643 = DRIFT-#45 verification 21; "
          "c2642 = DRIFT-#45 verification 20")
assert_count(txt, CH_OLD, 1, "chain anchor ('(' form)")
txt = txt.replace(CH_OLD, CH_NEW)

# --- P-HIST spot checks (steady-state rule) ---
CHECKS = [
    ("2644", 6),   # self (docstring + line-8 + chain head + CYCLE + RAW + PRETTY)
    ("2643", 2),   # rebadged-from pointer + restored chain line
    ("2642", 1),   # chain verification line only (pointer moved off)
    ("2641", 1),   # chain
    ("2640", 1),   # chain
    ("2639", 1),   # chain
    ("2638", 1),   # chain
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
