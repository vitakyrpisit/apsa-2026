#!/usr/bin/env python3
"""Re-anchor validate_cycle2583.py: DRIFT-#37 verification-3 (match-path, FAILED on
baseline_match) -> DRIFT-#38 ROOT validator (baseline (26,0,4,18,4) @ 446B).

The match-path run is the DRIFT-#38 declaration evidence: exactly ONE assertion
failure (baseline_match), all other 9 assertions passing. This script re-anchors
the docstring narrative + BASELINE_COMP to the new root. P-HIST invariant: exactly
2 intentional 2582 references post-re-anchor (rebadged-from + chain re-attach) —
the STANDARD 2-ref invariant applies here because the closed drift's ROOT (c2581,
DRIFT-#37) is TWO cycles back, so the closure root cite lands on 2581, not 2582
(the 3-ref c2581 precedent applied only when the closed ROOT was the immediate
predecessor).
"""
import re
import sys

PATH = "/home/z/my-project/scripts/validate_cycle2583.py"
text = open(PATH).read()

edits = [
    # 1) header provenance
    ("DRIFT-#37 verification-3 CARRY (root declared 2026-10-27 ~00:49 +08): "
     "rebadged from validate_cycle2582.py (the match-path rebadge was executed FIRST "
     "and FAILED on baseline_match — that run is the DRIFT-#37 declaration evidence "
     "— then re-anchored to the new root baseline)",
     "DRIFT-#38 ROOT validator (declared at c2583, 2026-10-27 ~01:06 +08): "
     "rebadged from validate_cycle2582.py (the match-path rebadge was executed FIRST "
     "and FAILED on baseline_match — that run is the DRIFT-#38 declaration evidence "
     "— then re-anchored to the new root baseline)", 1),
    # 2) baseline line
    ("(27,0,5,18,4) @ 446B DRIFT-#37 root; c2583 = DRIFT-#37 verification 1",
     "(26,0,4,18,4) @ 446B DRIFT-#38 root; c2583 = DRIFT-#38 verification 1", 1),
    # 3) chain head — declare DRIFT-#38 root, close DRIFT-#37
    ("(c2583 = DRIFT-#37 verification 3; c2582 = DRIFT-#37 verification 2; c2581 = DRIFT-#37 verification 1, ROOT — the movement:",
     "(c2583 = DRIFT-#38 verification 1, ROOT — the movement: total 27->26 (-1), "
     "honest_free 5->4 (-1) HONEST INVENTORY CONTRACTION (a single honest-free "
     "DEPARTURE — the second of the post-DRIFT-#35 era: the 6-task c2577 emergence "
     "has contracted 6->5->4; honest_paid=0 = NO GOLD), unknown 4 + scam 18 "
     "unchanged, SIZE 446B streak intact; DRIFT-#37 CLOSED at 2-fold (root c2581, "
     "verifications 1-2, 2-of-59 = 3.4% of the DRIFT-#30 record span; chain "
     "context-carried post-LOSS-#5: DRIFT-#36 closed at 1-fold, DRIFT-#35 at 3-fold, "
     "DRIFT-#34 at 14-fold, DRIFT-#33 at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at "
     "39-fold, DRIFT-#30 record 59-fold); c2582 = DRIFT-#37 verification 2; "
     "c2581 = DRIFT-#37 verification 1, ROOT — the movement:", 1),
    # 4) assertions preamble
    ("Assertions encode the DRIFT-#37 baseline (27,0,5,18,4) @ 446B:",
     "Assertions encode the DRIFT-#38 baseline (26,0,4,18,4) @ 446B:", 1),
    # 5) composition bullet
    ("- BA composition: total=27 honest_paid=0 honest_free=5 scam=18 unknown=4\n"
     "  (unknown=4 = the DRIFT-#37 movement — a single unknown ARRIVAL from\n"
     "  the 3-task unknown inventory; honest_free=5 HOLDS — the DRIFT-#36\n"
     "  departure did NOT reverse; aggregate-only visibility —\n"
     "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
     "  the 5 honest free tasks are NOT taken per the PAID-only policy)",
     "- BA composition: total=26 honest_paid=0 honest_free=4 scam=18 unknown=4\n"
     "  (honest_free=4 = the DRIFT-#38 movement — a single honest-free DEPARTURE,\n"
     "  the second of the post-DRIFT-#35 era (6->5->4); aggregate-only visibility —\n"
     "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
     "  the 4 honest free tasks are NOT taken per the PAID-only policy)", 1),
    # 6) code baseline
    ('BASELINE_COMP = {"total": 27, "honest_paid": 0, "honest_free": 5, "scam": 18, "unknown": 4}',
     'BASELINE_COMP = {"total": 26, "honest_paid": 0, "honest_free": 4, "scam": 18, "unknown": 4}', 1),
]

for old, new, expected in edits:
    c = text.count(old)
    assert c == expected, f"pre-patch count != {expected} for: {old[:60]!r} (got {c})"
    text = text.replace(old, new)

open(PATH, "w").write(text)

# P-HIST invariant: exactly 2 intentional 2582 references post-re-anchor
# (rebadged-from + chain re-attach; closure root cite lands on c2581 — see docstring)
sites = [m.start() for m in re.finditer("2582", text)]
print(f"P-HIST 2582 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2582 references post-re-anchor")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain re-attach; closure cite on c2581; no new historical refs)")
print(f"reanchored_ok={PATH}")
