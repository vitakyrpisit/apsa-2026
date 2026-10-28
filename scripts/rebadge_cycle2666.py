#!/usr/bin/env python3
"""Rebadge validate_cycle2665.py -> validate_cycle2666.py.

DRIFT-#45 verification-44 carry class (post-LOSS-#6 twentieth sed-carry).
P-HIST WATCH asserted on ACTUAL bytes pre- and post-patch (the c2573 LESSON, carried).
Rebadge = sed 2665->2666 (5 tokens) + four patches:
  P1b  self-verification bump: c2666 = verification 43 -> 44
  CHAIN insert: c2665 = verification 43 before the c2664 citation
  P1a  class bump verification-43->44 + nineteenth->twentieth sed-carry
  SRC  rebadged-from -> validate_cycle2665.py (verification-43 carry)
HIST-restore NOT invoked (NO-OP class as prophesied - the LOSS block history keeps
cite c2646, sed-immune).
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2665.py"
DST = "/home/z/my-project/scripts/validate_cycle2666.py"

PRE_HIST = {"2665": 5, "2664": 2, "2663": 1, "2662": 1, "2661": 1, "2660": 1, "2659": 1,
            "2658": 1, "2657": 1, "2656": 1, "2655": 1, "2654": 1, "2653": 1, "2652": 1,
            "2651": 1, "2650": 1, "2649": 1, "2648": 1, "2647": 1, "2646": 3, "2645": 7,
            "2644": 1, "2643": 1, "2624": 1, "2623": 2, "2576": 4, "2577": 3}
POST_HIST = {"2666": 5, "2665": 2, "2664": 1, "2663": 1, "2662": 1, "2661": 1, "2660": 1,
             "2659": 1, "2658": 1, "2657": 1, "2656": 1, "2655": 1, "2654": 1, "2653": 1,
             "2652": 1, "2651": 1, "2650": 1, "2649": 1, "2648": 1, "2647": 1, "2646": 3,
             "2645": 7, "2644": 1, "2643": 1, "2624": 1, "2623": 2, "2576": 4, "2577": 3}


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

# sed 2665 -> 2666 (5 tokens)
n_sed = text.count("2665")
if n_sed != 5:
    print(f"FAIL: sed token count expected 5, found {n_sed}")
    sys.exit(1)
t = text.replace("2665", "2666")
if t.count("2665") != 0:
    print("FAIL: residual 2665 after sed")
    sys.exit(1)
print(f"sed ok: 2665->2666 ({n_sed} tokens)")

# P1b self-verification bump
t = patch(t, "c2666 = verification 43", "c2666 = verification 44", "P1b self-verification bump 43->44")
# CHAIN insert before the c2664 citation
t = patch(t, "(c2664 = verification 42;", "(c2665 = verification 43; c2664 = verification 42;",
          "CHAIN insert c2665 = verification 43")
# P1a class bump + sed-carry ordinal
t = patch(t, "DRIFT-#45 verification-43 CARRY", "DRIFT-#45 verification-44 CARRY", "P1a class bump verification-43->44")
t = patch(t, "nineteenth sed-carry", "twentieth sed-carry", "P1a sed-carry ordinal nineteenth->twentieth")
# SRC rebadged-from
t = patch(t, "rebuilt from the\nverification-42 carry validate_cycle2664.py",
          "rebuilt from the\nverification-43 carry validate_cycle2665.py", "SRC rebadged-from -> validate_cycle2665.py")

post = hist(t)
bad = {k: (post.get(k), v) for k, v in POST_HIST.items() if post.get(k) != v}
if bad:
    print(f"FAIL: post-patch P-HIST mismatch on ACTUAL bytes: {bad}")
    sys.exit(1)
print(f"post-patch P-HIST asserted on ACTUAL bytes: {dict(sorted(post.items(), reverse=True))}")
if post.get("2665") != 2:
    print("FAIL: rebadged-from lineage citations != 2")
    sys.exit(1)
print("rebadged-from lineage citations == 2 (the c2573 LESSON, carried)")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)
py_compile.compile(DST, doraise=True)
print(f"py_compile clean: {DST}")
print("REBADGE FIRST-PASS CLEAN: validate_cycle2665.py -> validate_cycle2666.py (twentieth sed-rebadge of the post-loss lineage)")
