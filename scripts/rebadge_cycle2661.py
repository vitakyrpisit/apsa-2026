#!/usr/bin/env python3
"""Rebadge validate_cycle2660.py -> validate_cycle2661.py.

DRIFT-#45 verification-39 carry class (post-LOSS-#6 fifteenth sed-carry).
P-HIST WATCH asserted on ACTUAL bytes pre- and post-patch (the c2573 LESSON, carried).
Rebadge = sed 2660->2661 (5 tokens) + four patches:
  P1b  self-verification bump: c2661 = verification 38 -> 39
  CHAIN insert: c2660 = verification 38 before the c2659 citation
  P1a  class bump verification-38->39 + fourteenth->fifteenth sed-carry
  SRC  rebadged-from -> validate_cycle2660.py (verification-38 carry)
HIST-restore NOT invoked (NO-OP class as prophesied - the LOSS block history keeps
cite c2646, sed-immune).
"""
import py_compile
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2660.py"
DST = "/home/z/my-project/scripts/validate_cycle2661.py"

PRE_HIST = {"2660": 5, "2659": 2, "2658": 1, "2657": 1, "2656": 1, "2655": 1, "2654": 1,
            "2653": 1, "2652": 1, "2651": 1, "2650": 1, "2649": 1, "2648": 1, "2647": 1,
            "2646": 3, "2645": 7, "2644": 1, "2643": 1, "2624": 1, "2623": 2, "2576": 4,
            "2577": 3}
POST_HIST = {"2661": 5, "2660": 2, "2659": 1, "2658": 1, "2657": 1, "2656": 1, "2655": 1,
             "2654": 1, "2653": 1, "2652": 1, "2651": 1, "2650": 1, "2649": 1, "2648": 1,
             "2647": 1, "2646": 3, "2645": 7, "2644": 1, "2643": 1, "2624": 1, "2623": 2,
             "2576": 4, "2577": 3}


def hist(text):
    return {tok: text.count(tok) for tok in set(PRE_HIST) | set(POST_HIST)}


def patch(t, old, new, label):
    n = t.count(old)
    if n != 1:
        print(f"FAIL: {label}: expected exactly 1 occurrence of pattern, found {n}")
        sys.exit(1)
    print(f"patch ok: {label}")
    return t.replace(old, new, 1)


with open(SRC, "r", encoding="utf-8") as f:
    text = f.read()

pre = hist(text)
bad = {k: (pre.get(k), v) for k, v in PRE_HIST.items() if pre.get(k) != v}
if bad:
    print(f"FAIL: pre-patch P-HIST mismatch on ACTUAL bytes: {bad}")
    sys.exit(1)
print(f"pre-patch P-HIST asserted on ACTUAL bytes: {dict(sorted(pre.items(), reverse=True))}")

# sed 2660 -> 2661 (5 tokens)
n_sed = text.count("2660")
if n_sed != 5:
    print(f"FAIL: sed token count expected 5, found {n_sed}")
    sys.exit(1)
t = text.replace("2660", "2661")
if t.count("2660") != 0:
    print("FAIL: residual 2660 after sed")
    sys.exit(1)
print(f"sed ok: 2660->2661 ({n_sed} tokens)")

# P1b self-verification bump
t = patch(t, "c2661 = verification 38", "c2661 = verification 39", "P1b self-verification bump 38->39")
# CHAIN insert before the c2659 citation
t = patch(t, "(c2659 = verification 37;", "(c2660 = verification 38; c2659 = verification 37;",
          "CHAIN insert c2660 = verification 38")
# P1a class bump + sed-carry ordinal
t = patch(t, "DRIFT-#45 verification-38 CARRY", "DRIFT-#45 verification-39 CARRY", "P1a class bump verification-38->39")
t = patch(t, "fourteenth sed-carry", "fifteenth sed-carry", "P1a sed-carry ordinal fourteenth->fifteenth")
# SRC rebadged-from
t = patch(t, "rebuilt from the\nverification-37 carry validate_cycle2659.py",
          "rebuilt from the\nverification-38 carry validate_cycle2660.py", "SRC rebadged-from -> validate_cycle2660.py")

post = hist(t)
bad = {k: (post.get(k), v) for k, v in POST_HIST.items() if post.get(k) != v}
if bad:
    print(f"FAIL: post-patch P-HIST mismatch on ACTUAL bytes: {bad}")
    sys.exit(1)
print(f"post-patch P-HIST asserted on ACTUAL bytes: {dict(sorted(post.items(), reverse=True))}")
if post.get("2660") != 2:
    print("FAIL: rebadged-from lineage citations != 2")
    sys.exit(1)
print("rebadged-from lineage citations == 2 (the c2573 LESSON, carried)")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)
py_compile.compile(DST, doraise=True)
print(f"py_compile clean: {DST}")
print("REBADGE FIRST-PASS CLEAN: validate_cycle2660.py -> validate_cycle2661.py (fifteenth sed-rebadge of the post-loss lineage)")
