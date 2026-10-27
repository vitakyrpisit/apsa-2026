#!/usr/bin/env python3
"""rebadge c2623: validate_cycle2622.py -> validate_cycle2623.py (DRIFT-#44 verification-5 CARRY).

REBADGE-INCIDENT CARRY (c2622 lesson): patterns derived from the ACTUAL
validate_cycle2622.py bytes, not from carried predictions. The chain is 4-DEEP
"(c2622 = v4; c2621 = v3; c2620 = v2; c2619 = v1 ROOT)"; the global sed 2622->2623
migrates ONLY the head, leaving c2621/c2620/c2619 untouched and DISSOLVING the
c2622 line into the head (the head inherits the stale "verification 4"). The
insert below matches THAT actual post-sed form, fixes the head to verification 5,
and RESTORES the c2622 = verification 4 line.
Assert containment: every patch asserts its match count BEFORE any byte is
written; a failure aborts with zero bytes written and zero POSTs consumed.
"""
import py_compile

SRC = "/home/z/my-project/scripts/validate_cycle2622.py"
DST = "/home/z/my-project/scripts/validate_cycle2623.py"

text = open(SRC).read()

# 1) global sed 2622 -> 2623
pre = text.count("2622")
assert pre >= 1, f"sed source token 2622 count {pre} != >=1"
text = text.replace("2622", "2623")

# 2) P1 header patch (post-sed form: rebadged-from pointer moves 2621 -> 2622)
P1_OLD = ("DRIFT-#44 verification-4 CARRY (root declared 2026-10-27 ~05:23 +08): "
          "rebadged from validate_cycle2621.py")
P1_NEW = ("DRIFT-#44 verification-5 CARRY (root declared 2026-10-27 ~05:23 +08): "
          "rebadged from validate_cycle2622.py")
c = text.count(P1_OLD)
assert c == 1, f"P1 post-sed count {c} != 1"
text = text.replace(P1_OLD, P1_NEW)

# 3) line-8 bump (post-sed form)
L8_OLD = "(19,0,0,18,1) @ 446B DRIFT-#44 root; c2623 = DRIFT-#44 verification 4"
L8_NEW = "(19,0,0,18,1) @ 446B DRIFT-#44 root; c2623 = DRIFT-#44 verification 5"
c = text.count(L8_OLD)
assert c == 1, f"line-8 post-sed count {c} != 1"
text = text.replace(L8_OLD, L8_NEW)

# 4) chain insert (post-sed 4-deep form): fix head to v5, RESTORE c2622 = v4
CH_OLD = "(c2623 = DRIFT-#44 verification 4; c2621 = DRIFT-#44 verification 3;"
CH_NEW = ("(c2623 = DRIFT-#44 verification 5; c2622 = DRIFT-#44 verification 4; "
          "c2621 = DRIFT-#44 verification 3;")
c = text.count(CH_OLD)
assert c == 1, f"chain post-sed count {c} != 1"
text = text.replace(CH_OLD, CH_NEW)

# 5) P-HIST WATCH (final text; str.count loops, no comprehension-display hazard)
# NOTE: line 121 of the source is an f-string (baseline_match_c{CYCLE}) — the
# literal pre-sed "2622" count is 6 (lines 2/8/9/43/44/45), so post-sed self = 6.
expected = {"2623": 6, "2622": 2, "2621": 1, "2620": 1,
            "2619": 1, "2618": 2, "2606": 2, "2594": 2}
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
