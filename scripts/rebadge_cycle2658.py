#!/usr/bin/env python3
"""Rebadge validate_cycle2657.py -> validate_cycle2658.py (c2658 staging, pre-POST).

Recipe per the c2657 Next-block: sed 2657->2658 (5 tokens) + P1a class bump
(verification-35->36, eleventh->twelfth sed-carry) + P1b self-verification bump
(c2658 = verification 36) + CHAIN insert (c2657 = verification 35 before the
c2656 citation) + SRC rebadged-from -> validate_cycle2657.py.
P-HIST WATCH asserted on ACTUAL bytes pre- and post-patch (the c2573 LESSON).
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2657.py"
DST = "/home/z/my-project/scripts/validate_cycle2658.py"

PRE_EXPECT = {2657: 5, 2656: 2, 2655: 1, 2654: 1, 2653: 1, 2652: 1, 2651: 1,
              2650: 1, 2649: 1, 2648: 1, 2647: 1, 2646: 3, 2645: 7, 2644: 1,
              2643: 1, 2624: 1, 2623: 2, 2576: 4, 2577: 3}
POST_EXPECT = {2658: 5, 2657: 2, 2656: 1, 2655: 1, 2654: 1, 2653: 1, 2652: 1,
               2651: 1, 2650: 1, 2649: 1, 2648: 1, 2647: 1, 2646: 3, 2645: 7,
               2644: 1, 2643: 1, 2624: 1, 2623: 2, 2576: 4, 2577: 3}

failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"ok: {name}" + (f" ({detail})" if detail else ""))
    else:
        failures.append(name)
        print(f"FAIL: {name} ({detail})")


with open(SRC, "rb") as f:
    text = f.read().decode("utf-8")


def hist(t):
    out = {}
    for c in sorted(set(PRE_EXPECT) | set(POST_EXPECT)):
        out[c] = t.count(str(c))
    return out


pre = hist(text)
pre_core = {k: v for k, v in pre.items() if k in PRE_EXPECT}
check("pre_patch_P-HIST", pre_core == PRE_EXPECT, str(pre_core))

# sed 2657 -> 2658 (5 tokens)
t = text.replace("2657", "2658")
# P1b self-verification bump FIRST (before CHAIN insert adds a spaced "verification 35")
old = "c2658 = verification 35"
assert t.count(old) == 1, f"P1b anchor count {t.count(old)}"
t = t.replace(old, "c2658 = verification 36")
print("ok: P1b self-bump c2658 = verification 35 -> 36")
# CHAIN insert c2657 = verification 35 before the c2656 citation
old = "(c2656 = verification 34;"
assert t.count(old) == 1, f"CHAIN anchor count {t.count(old)}"
t = t.replace(old, "(c2657 = verification 35; c2656 = verification 34;")
print("ok: CHAIN insert c2657 = verification 35 before c2656 citation")
# P1a class bump verification-35 -> verification-36 + eleventh -> twelfth sed-carry
old = "DRIFT-#45 verification-35 CARRY"
assert t.count(old) == 1, f"P1a anchor count {t.count(old)}"
t = t.replace(old, "DRIFT-#45 verification-36 CARRY")
old = "eleventh sed-carry"
assert t.count(old) == 1, f"P1a-b anchor count {t.count(old)}"
t = t.replace(old, "twelfth sed-carry")
print("ok: P1a verification-35 -> 36 class bump + eleventh -> twelfth sed-carry")
# SRC rebadged-from -> validate_cycle2657.py
old = "verification-34 carry validate_cycle2656.py"
assert t.count(old) == 1, f"SRC anchor count {t.count(old)}"
t = t.replace(old, "verification-35 carry validate_cycle2657.py")
print("ok: SRC rebadged-from -> validate_cycle2657.py")

post = hist(t)
check("post_patch_P-HIST", post == POST_EXPECT, str(post))
check("rebadged_from_lineage_citations", t.count("2657") == 2, f"count={t.count('2657')}")

with open(DST, "w") as f:
    f.write(t)
print(f"written={DST}")

py_compile.compile(DST, doraise=True)
print("ok: py_compile clean")

if failures:
    print(f"REBADGE_FAILURES: {len(failures)}")
    sys.exit(1)
print("REBADGE_OK c2658 = verification 36 (twelfth sed-carry, post-LOSS-#6 lineage)")
