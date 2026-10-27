#!/usr/bin/env python3
"""Rebadge validate_cycle2646.py -> validate_cycle2647.py (DRIFT-#45 verification-25 CARRY).

First sed-rebadge of the post-LOSS-#6 lineage. Patch order:
  sed 2646->2647 (assert 7 literal tokens pre-patch)
  P1  docstring verification-24->25 bump (self-verification line)
  L8  "; c2647 = verification 24" -> "; c2647 = verification 25"
  CHAIN insert "c2646 = verification 24; " before the c2645 citation
  HIST restore the two LOSS-#6 narrative citations (c2646 executing session /
       fresh c2646 capture) that the sed corrupts — history keeps, declared
  SRC rebadged-from: ancestor citation validate_cycle2576.py -> validate_cycle2646.py
P-HIST WATCH (c2573 LESSON): verify token table post-rebadge; lineage citations
(provenance + chain) == 2; total '2646' == 4 (2 lineage + 2 history keeps).
py_compile gate; exits non-zero on any assertion failure.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2646.py"
DST = "/home/z/my-project/scripts/validate_cycle2647.py"

s = open(SRC).read()

# --- pre-patch P-HIST (ACTUAL bytes) ---
expected_pre = {"2646": 7, "2645": 7, "2644": 1, "2643": 1, "2624": 1, "2623": 2,
                "2576": 5, "2577": 3, "2647": 0, "2648": 0}
pre = {t: s.count(t) for t in expected_pre}
bad = {t: (pre[t], exp) for t, exp in expected_pre.items() if pre[t] != exp}
if bad:
    print(f"PRE-PATCH P-HIST MISMATCH (c2573-lesson abort): {bad}")
    sys.exit(1)
print("pre-patch P-HIST OK:", pre)

# --- sed 2646->2647 (all 7 literal tokens) ---
assert s.count("2646") == 7
s = s.replace("2646", "2647")
assert s.count("2647") == 7 and s.count("2646") == 0

patches = []

def patch(name, old, new, expect=1):
    global s
    n = s.count(old)
    if n != expect:
        print(f"PATCH {name} FAILED: found {n} occurrences (expect {expect}) of: {old[:70]!r}")
        sys.exit(1)
    s = s.replace(old, new)
    patches.append(name)
    print(f"patch {name}: OK")

# P1a docstring class bump
patch("P1a-verclass",
      "DRIFT-#45 verification-24 CARRY (context-carried post-LOSS-#6 rebadge lineage): rebuilt from the",
      "DRIFT-#45 verification-25 CARRY (post-LOSS-#6 rebadge lineage, first sed-carry): rebuilt from the")

# P1b self-verification bump (post-sed line 8 still says verification 24)
patch("P1b-selfver",
      "@ 446B DRIFT-#45 root; c2647 = verification 24",
      "@ 446B DRIFT-#45 root; c2647 = verification 25")

# CHAIN insert c2646 = verification 24 before the c2645 citation
patch("CHAIN-insert",
      "(c2645 = verification 23;",
      "(c2646 = verification 24; c2645 = verification 23;")

# HIST restores (sed corrupted two historical citations)
patch("HIST-session",
      "LOSS EVENT #6 (declared 2026-10-27 ~09:00 +08 by the c2647 executing session)",
      "LOSS EVENT #6 (declared 2026-10-27 ~09:00 +08 by the c2646 executing session)")
patch("HIST-capture",
      "the fresh c2647 capture returned (18,0,0,18,0) @ 446B",
      "the fresh c2646 capture returned (18,0,0,18,0) @ 446B")

# SRC rebadged-from: ancestor citation now validate_cycle2646.py
patch("SRC-rebadgedfrom",
      "disk-recoverable ancestor validate_cycle2576.py (LOSS-#5 precedent class — lineage restart, honest",
      "post-loss reconstruction validate_cycle2646.py (LOSS-#6 carry class — first sed-rebadge, honest")

# --- post-patch P-HIST ---
expected_post = {"2647": 5, "2646": 4, "2645": 7, "2644": 1, "2643": 1, "2624": 1,
                 "2623": 2, "2576": 4, "2577": 3, "2648": 0}
post = {t: s.count(t) for t in expected_post}
bad = {t: (post[t], exp) for t, exp in expected_post.items() if post[t] != exp}
if bad:
    print(f"POST-PATCH P-HIST MISMATCH: {bad}")
    sys.exit(1)
print("post-patch P-HIST OK:", post)

# P-HIST WATCH: lineage citations == 2 (provenance + chain node)
lineage = s.count("validate_cycle2646.py") + s.count("c2646 = verification 24")
print(f"P-HIST WATCH rebadged-from lineage citations: {lineage} (expect 2)")
if lineage != 2:
    print("P-HIST WATCH FAILED")
    sys.exit(1)

with open(DST, "w") as f:
    f.write(s)
py_compile.compile(DST, doraise=True)
print(f"py_compile OK -> {DST}")
print("PATCHES APPLIED:", patches)
print("REBADGE COMPLETE: verification-25 CARRY (c2647 = v25; c2646 = v24; c2645 = v23; ...)")
