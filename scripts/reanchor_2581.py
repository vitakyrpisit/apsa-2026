#!/usr/bin/env python3
"""Re-anchor validate_cycle2581.py: DRIFT-#36 verification-2 (match-path, FAILED on
baseline_match) -> DRIFT-#37 ROOT validator (baseline (27,0,5,18,4) @ 446B).

The match-path run is the DRIFT-#37 declaration evidence: exactly ONE assertion
failure (baseline_match), all other 9 assertions passing. This script re-anchors
the docstring narrative + BASELINE_COMP to the new root. P-HIST invariant: the
count of historical 2580 references is 3 post-re-anchor (rebadged-from + DRIFT-#36
closure root cite + chain re-attach) — ONE MORE than the standard 2-ref invariant
because the closed drift's ROOT (c2580) IS the immediate predecessor cycle, so the
closure note legitimately cites it. All three sites are intentional and enumerated.
"""
import re
import sys

PATH = "/home/z/my-project/scripts/validate_cycle2581.py"
text = open(PATH).read()

edits = [
    # 1) header provenance
    ("DRIFT-#36 verification-2 CARRY (root declared 2026-10-27 ~00:33 +08): "
     "rebadged from validate_cycle2580.py (the match-path rebadge was executed FIRST "
     "and FAILED on baseline_match — that run is the DRIFT-#36 declaration evidence "
     "— then re-anchored to the new root baseline)",
     "DRIFT-#37 ROOT validator (declared at c2581, 2026-10-27 ~00:49 +08): "
     "rebadged from validate_cycle2580.py (the match-path rebadge was executed FIRST "
     "and FAILED on baseline_match — that run is the DRIFT-#37 declaration evidence "
     "— then re-anchored to the new root baseline)", 1),
    # 2) baseline line
    ("(26,0,5,18,3) @ 446B DRIFT-#36 root; c2581 = DRIFT-#36 verification 1",
     "(27,0,5,18,4) @ 446B DRIFT-#37 root; c2581 = DRIFT-#37 verification 1", 1),
    # 3) chain head — declare DRIFT-#37 root, close DRIFT-#36
    ("(c2581 = DRIFT-#36 verification 2; c2580 = DRIFT-#36 verification 1, ROOT — the movement:",
     "(c2581 = DRIFT-#37 verification 1, ROOT — the movement: total 26->27 (+1), "
     "unknown 3->4 (+1) UNKNOWN ARRIVAL (a single unknown-category arrival accounts "
     "for BOTH deltas — the second inventory movement of the DRIFT-#36 span; "
     "honest_free 5 HOLDS — the DRIFT-#36 honest-free DEPARTURE did NOT reverse; "
     "honest_paid=0 = NO GOLD), scam 18 + honest_free 5 unchanged, SIZE 446B streak "
     "intact; DRIFT-#36 CLOSED at 1-fold (root c2580, verification 1 only — 1-of-59 "
     "= 1.7% of the DRIFT-#30 record span, the SHORTEST recorded closure of the "
     "tracked chain, undercutting DRIFT-#32's 3-fold; chain context-carried "
     "post-LOSS-#5: DRIFT-#35 closed at 3-fold, DRIFT-#34 at 14-fold, DRIFT-#33 at "
     "7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 record 59-fold); "
     "c2580 = DRIFT-#36 verification 1, ROOT — the movement:", 1),
    # 4) assertions preamble
    ("Assertions encode the DRIFT-#36 baseline (26,0,5,18,3) @ 446B:",
     "Assertions encode the DRIFT-#37 baseline (27,0,5,18,4) @ 446B:", 1),
    # 5) composition bullet
    ("- BA composition: total=26 honest_paid=0 honest_free=5 scam=18 unknown=3\n"
     "  (honest_free=5 = the DRIFT-#36 movement — a single honest-free DEPARTURE\n"
     "  from the 6-task inventory; aggregate-only visibility —\n"
     "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
     "  the 5 honest free tasks are NOT taken per the PAID-only policy)",
     "- BA composition: total=27 honest_paid=0 honest_free=5 scam=18 unknown=4\n"
     "  (unknown=4 = the DRIFT-#37 movement — a single unknown ARRIVAL from\n"
     "  the 3-task unknown inventory; honest_free=5 HOLDS — the DRIFT-#36\n"
     "  departure did NOT reverse; aggregate-only visibility —\n"
     "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
     "  the 5 honest free tasks are NOT taken per the PAID-only policy)", 1),
    # 6) code baseline
    ('BASELINE_COMP = {"total": 26, "honest_paid": 0, "honest_free": 5, "scam": 18, "unknown": 3}',
     'BASELINE_COMP = {"total": 27, "honest_paid": 0, "honest_free": 5, "scam": 18, "unknown": 4}', 1),
]

for old, new, expected in edits:
    c = text.count(old)
    assert c == expected, f"pre-patch count != {expected} for: {old[:60]!r} (got {c})"
    text = text.replace(old, new)

open(PATH, "w").write(text)

# P-HIST invariant: exactly 3 intentional 2580 references post-re-anchor
# (rebadged-from + DRIFT-#36 closure root cite + chain re-attach — see docstring)
sites = [m.start() for m in re.finditer("2580", text)]
print(f"P-HIST 2580 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 3:
    print("P-HIST WATCH FAILED: expected exactly 3 intentional 2580 references post-re-anchor")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + closure root cite + chain re-attach; no new historical refs)")
print(f"reanchored_ok={PATH}")
