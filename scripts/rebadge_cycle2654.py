#!/usr/bin/env python3
"""Rebadge validate_cycle2653.py -> validate_cycle2654.py (c2654 staging, pre-POST).

Recipe per the c2653 Next-block: sed 2653->2654 (5 tokens) + P1a class bump
(verification-31->32, seventh->eighth sed-carry) + P1b self-verification bump
(c2654 = verification 32) + CHAIN insert (c2653 = verification 31 before the
c2652 citation) + SRC rebadged-from -> validate_cycle2653.py.
P-HIST WATCH asserted on ACTUAL bytes pre- and post-patch (the c2573 LESSON).
"""
import py_compile
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2653.py"
DST = "/home/z/my-project/scripts/validate_cycle2654.py"

PRE_EXPECT = {2653: 5, 2652: 2, 2651: 1, 2650: 1, 2649: 1, 2648: 1, 2647: 1,
              2646: 3, 2645: 7, 2644: 1, 2643: 1, 2624: 1, 2623: 2, 2576: 4, 2577: 3}
POST_EXPECT = {2654: 5, 2653: 2, 2652: 1, 2651: 1, 2650: 1, 2649: 1, 2648: 1,
               2647: 1, 2646: 3, 2645: 7, 2644: 1, 2643: 1, 2624: 1, 2623: 2,
               2576: 4, 2577: 3}

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

# sed 2653 -> 2654 (5 tokens)
t = text.replace("2653", "2654")
# P1b self-verification bump FIRST (before CHAIN insert adds a spaced "verification 31")
old = "c2654 = verification 31"
assert t.count(old) == 1, f"P1b anchor count {t.count(old)}"
t = t.replace(old, "c2654 = verification 32")
print("ok: P1b self-bump c2654 = verification 31 -> 32")
# CHAIN insert c2653 = verification 31 before the c2652 citation
old = "(c2652 = verification 30;"
assert t.count(old) == 1, f"CHAIN anchor count {t.count(old)}"
t = t.replace(old, "(c2653 = verification 31; c2652 = verification 30;")
print("ok: CHAIN insert c2653 = verification 31 before c2652 citation")
# P1a class bump verification-31 -> verification-32 + seventh -> eighth sed-carry
old = "DRIFT-#45 verification-31 CARRY"
assert t.count(old) == 1, f"P1a anchor count {t.count(old)}"
t = t.replace(old, "DRIFT-#45 verification-32 CARRY")
old = "seventh sed-carry"
assert t.count(old) == 1, f"P1a-b anchor count {t.count(old)}"
t = t.replace(old, "eighth sed-carry")
print("ok: P1a verification-31 -> 32 class bump + seventh -> eighth sed-carry")
# SRC rebadged-from -> validate_cycle2653.py
old = "verification-30 carry validate_cycle2652.py"
assert t.count(old) == 1, f"SRC anchor count {t.count(old)}"
t = t.replace(old, "verification-31 carry validate_cycle2653.py")
print("ok: SRC rebadged-from -> validate_cycle2653.py")

post = hist(t)
check("post_patch_P-HIST", post == POST_EXPECT, str(post))
check("rebadged_from_lineage_citations", t.count("2653") == 2, f"count={t.count('2653')}")

with open(DST, "w") as f:
    f.write(t)
print(f"written={DST}")

py_compile.compile(DST, doraise=True)
print("ok: py_compile clean")

if failures:
    print(f"REBADGE_FAILURES: {len(failures)}")
    sys.exit(1)
print("REBADGE_OK c2654 = verification 32 (eighth sed-carry, post-LOSS-#6 lineage)")
