#!/usr/bin/env python3
"""Rebadge validate_cycle2652.py -> validate_cycle2653.py (DRIFT-#45 verification-31 CARRY).

Seventh sed-rebadge of the post-LOSS-#6 lineage. Patch order:
  sed 2652->2653 (assert 5 literal tokens pre-patch)
  P1a docstring verification-30->31 class bump
  P1b self-verification bump (post-sed still says verification 30)
  CHAIN insert "c2652 = verification 30; " before the c2651 citation
  SRC rebadged-from: provenance validate_cycle2651.py -> validate_cycle2652.py
  HIST-restore patches: expected NO-OPs (LOSS-#6 history keeps cite c2646 — sed-immune).
P-HIST WATCH (c2573 LESSON): post-patch lineage citations (provenance + chain) == 2.
py_compile gate; exits non-zero on any assertion failure.
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2652.py"
DST = "/home/z/my-project/scripts/validate_cycle2653.py"

s = open(SRC).read()

expected_pre = {"2652": 5, "2651": 2, "2650": 1, "2649": 1, "2648": 1, "2647": 1, "2646": 3, "2645": 7, "2644": 1,
                "2643": 1, "2624": 1, "2623": 2, "2576": 4, "2577": 3, "2653": 0, "2654": 0}
pre = {t: s.count(t) for t in expected_pre}
bad = {t: (pre[t], exp) for t, exp in expected_pre.items() if pre[t] != exp}
if bad:
    print(f"PRE-PATCH P-HIST MISMATCH (c2573-lesson abort): {bad}")
    sys.exit(1)
print("pre-patch P-HIST OK:", pre)

assert s.count("2652") == 5
s = s.replace("2652", "2653")
assert s.count("2653") == 5 and s.count("2652") == 0

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
      "DRIFT-#45 verification-30 CARRY (post-LOSS-#6 rebadge lineage, sixth sed-carry): rebuilt from the",
      "DRIFT-#45 verification-31 CARRY (post-LOSS-#6 rebadge lineage, seventh sed-carry): rebuilt from the")

patch("P1b-selfver",
      "@ 446B DRIFT-#45 root; c2653 = verification 30",
      "@ 446B DRIFT-#45 root; c2653 = verification 31")

patch("CHAIN-insert",
      "(c2651 = verification 29; c2650 = verification 28; c2649 = verification 27; c2648 = verification 26; c2647 = verification 25;",
      "(c2652 = verification 30; c2651 = verification 29; c2650 = verification 28; c2649 = verification 27; c2648 = verification 26; c2647 = verification 25;")

patch("SRC-rebadgedfrom",
      "verification-29 carry validate_cycle2651.py (post-LOSS-#6 sed-carry class, honest",
      "verification-30 carry validate_cycle2652.py (post-LOSS-#6 sed-carry class, honest")

for hist in ["c2654 executing session", "the fresh c2654 capture"]:
    if hist in s:
        print(f"HIST CORRUPTION DETECTED: {hist!r} present — aborting")
        sys.exit(1)
print("HIST NO-OP verified: zero corrupted history tokens")

expected_post = {"2653": 5, "2652": 2, "2651": 1, "2650": 1, "2649": 1, "2648": 1, "2647": 1, "2646": 3, "2645": 7,
                 "2644": 1, "2643": 1, "2624": 1, "2623": 2, "2576": 4, "2577": 3, "2654": 0}
post = {t: s.count(t) for t in expected_post}
bad = {t: (post[t], exp) for t, exp in expected_post.items() if post[t] != exp}
if bad:
    print(f"POST-PATCH P-HIST MISMATCH: {bad}")
    sys.exit(1)
print("post-patch P-HIST OK:", post)

lineage = s.count("validate_cycle2652.py") + s.count("c2652 = verification 30")
print(f"P-HIST WATCH rebadged-from lineage citations: {lineage} (expect 2)")
if lineage != 2:
    print("P-HIST WATCH FAILED")
    sys.exit(1)

with open(DST, "w") as f:
    f.write(s)
py_compile.compile(DST, doraise=True)
print(f"py_compile OK -> {DST}")
print("PATCHES APPLIED:", patches)
print("REBADGE COMPLETE: verification-31 CARRY (c2653 = v31; c2652 = v30; c2651 = v29; c2650 = v28; c2649 = v27; c2648 = v26; c2647 = v25; ...)")
