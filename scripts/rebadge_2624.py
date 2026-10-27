#!/usr/bin/env python3
"""rebadge c2624: validate_cycle2623.py -> validate_cycle2624.py (DRIFT-#45 verification-2 CARRY).

REBADGE-CARRY NOTE (c2622/c2623 lessons): patterns derived from the ACTUAL
validate_cycle2623.py bytes (all three anchors pre-verified count==1; the
f-string caveat is explicit — baseline_match_c{CYCLE} is a TEMPLATE, only
literal cycle tokens are counted). The chain is 5-DEEP "(c2623 = v1 ROOT (with
the DRIFT-#45 movement cite + DRIFT-#44 closure cite); c2622 = v4; c2621 = v3;
c2620 = v2; c2619 = v1 ROOT)"; the global sed 2623->2624 migrates ONLY the head
INCLUDING its full ROOT narrative, dissolving the c2623 line into the head. The
insert below matches THAT actual post-sed form, fixes the head to verification 2,
and RESTORES the c2623 ROOT line (narrative re-anchored onto it).
Assert containment: every patch asserts its match count BEFORE any byte is
written; a failure aborts with zero bytes written and zero POSTs consumed.
"""
import py_compile

SRC = "/home/z/my-project/scripts/validate_cycle2623.py"
DST = "/home/z/my-project/scripts/validate_cycle2624.py"

text = open(SRC).read()

# 1) global sed 2623 -> 2624
pre = text.count("2623")
assert pre == 6, f"sed source literal 2623 count {pre} != 6"
text = text.replace("2623", "2624")

# 2) P1 header patch (post-sed form; parenthetical run-narrative carries VERBATIM)
P1_OLD = ("DRIFT-#45 ROOT DECLARATION (declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2622.py")
P1_NEW = ("DRIFT-#45 verification-2 CARRY (root declared 2026-10-27 ~06:04 +08): "
          "rebadged from validate_cycle2623.py")
c = text.count(P1_OLD)
assert c == 1, f"P1 post-sed count {c} != 1"
text = text.replace(P1_OLD, P1_NEW)

# 3) line-8 bump (post-sed form; strip the ", ROOT")
L8_OLD = "(18,0,0,18,0) @ 446B DRIFT-#45 root; c2624 = DRIFT-#45 verification 1, ROOT"
L8_NEW = "(18,0,0,18,0) @ 446B DRIFT-#45 root; c2624 = DRIFT-#45 verification 2"
c = text.count(L8_OLD)
assert c == 1, f"line-8 post-sed count {c} != 1"
text = text.replace(L8_OLD, L8_NEW)

# 4) chain insert (post-sed form): fix head to v2, RESTORE the c2623 ROOT line
CH_OLD = "(c2624 = DRIFT-#45 verification 1, ROOT — the movement:"
CH_NEW = ("(c2624 = DRIFT-#45 verification 2; "
          "c2623 = DRIFT-#45 verification 1, ROOT — the movement:")
c = text.count(CH_OLD)
assert c == 1, f"chain post-sed count {c} != 1"
text = text.replace(CH_OLD, CH_NEW)

# 5) P-HIST WATCH (final text; str.count loops, no comprehension-display hazard)
expected = {"2624": 6, "2623": 2, "2622": 1, "2621": 1, "2620": 1,
            "2619": 2, "2618": 2, "2606": 2, "2594": 2}
ok = True
for tok in sorted(expected):
    n = text.count(tok)
    status = "OK" if n == expected[tok] else "MISMATCH"
    if n != expected[tok]:
        ok = False
    print(f"P-HIST {tok}: {n} (expected {expected[tok]}) {status}")
assert ok, "P-HIST steady-state violated — aborting pre-write"

with open(DST, "w") as f:
    f.write(text)
py_compile.compile(DST, doraise=True)
print(f"rebadge complete: {DST} (py_compile OK)")
