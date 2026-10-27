#!/usr/bin/env python3
"""Rebadge validate_cycle2648.py -> validate_cycle2649.py (DRIFT-#45 verification-27 CARRY).

Third sed-rebadge of the post-LOSS-#6 lineage. Patch order:
  sed 2648->2649 (assert 5 literal tokens pre-patch)
  P1a docstring verification-26->27 class bump
  P1b self-verification bump (post-sed L8 still says verification 26)
  CHAIN insert "c2648 = verification 26; " before the c2647 citation
  SRC rebadged-from: provenance validate_cycle2647.py -> validate_cycle2648.py
  HIST-restore patches: expected NO-OPs (LOSS-#6 history keeps cite c2646 — sed-immune).
P-HIST WATCH (c2573 LESSON): post-patch lineage citations (provenance + chain) == 2.
py_compile gate; exits non-zero on any assertion failure.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2648.py"
DST = "/home/z/my-project/scripts/validate_cycle2649.py"

s = open(SRC).read()

expected_pre = {"2648": 5, "2647": 2, "2646": 3, "2645": 7, "2644": 1, "2643": 1,
                "2624": 1, "2623": 2, "2576": 4, "2577": 3, "2649": 0, "2650": 0}
pre = {t: s.count(t) for t in expected_pre}
bad = {t: (pre[t], exp) for t, exp in expected_pre.items() if pre[t] != exp}
if bad:
    print(f"PRE-PATCH P-HIST MISMATCH (c2573-lesson abort): {bad}")
    sys.exit(1)
print("pre-patch P-HIST OK:", pre)

assert s.count("2648") == 5
s = s.replace("2648", "2649")
assert s.count("2649") == 5 and s.count("2648") == 0

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

patch("P1a-verclass",
      "DRIFT-#45 verification-26 CARRY (post-LOSS-#6 rebadge lineage, second sed-carry): rebuilt from the",
      "DRIFT-#45 verification-27 CARRY (post-LOSS-#6 rebadge lineage, third sed-carry): rebuilt from the")

patch("P1b-selfver",
      "@ 446B DRIFT-#45 root; c2649 = verification 26",
      "@ 446B DRIFT-#45 root; c2649 = verification 27")

patch("CHAIN-insert",
      "(c2647 = verification 25; c2646 = verification 24;",
      "(c2648 = verification 26; c2647 = verification 25; c2646 = verification 24;")

patch("SRC-rebadgedfrom",
      "verification-25 carry validate_cycle2647.py (post-LOSS-#6 sed-carry class, honest",
      "verification-26 carry validate_cycle2648.py (post-LOSS-#6 sed-carry class, honest")

for hist in ["c2650 executing session", "the fresh c2650 capture"]:
    if hist in s:
        print(f"HIST CORRUPTION DETECTED: {hist!r} present — aborting")
        sys.exit(1)
print("HIST NO-OP verified: zero corrupted history tokens")

expected_post = {"2649": 5, "2648": 2, "2647": 1, "2646": 3, "2645": 7, "2644": 1,
                 "2643": 1, "2624": 1, "2623": 2, "2576": 4, "2577": 3, "2650": 0}
post = {t: s.count(t) for t in expected_post}
bad = {t: (post[t], exp) for t, exp in expected_post.items() if post[t] != exp}
if bad:
    print(f"POST-PATCH P-HIST MISMATCH: {bad}")
    sys.exit(1)
print("post-patch P-HIST OK:", post)

lineage = s.count("validate_cycle2648.py") + s.count("c2648 = verification 26")
print(f"P-HIST WATCH rebadged-from lineage citations: {lineage} (expect 2)")
if lineage != 2:
    print("P-HIST WATCH FAILED")
    sys.exit(1)

with open(DST, "w") as f:
    f.write(s)
py_compile.compile(DST, doraise=True)
print(f"py_compile OK -> {DST}")
print("PATCHES APPLIED:", patches)
print("REBADGE COMPLETE: verification-27 CARRY (c2649 = v27; c2648 = v26; c2647 = v25; ...)")
