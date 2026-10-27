#!/usr/bin/env python3
"""Re-anchor validate_cycle2577.py: DRIFT-#34 verification-15 (match-path, FAILED on
baseline_match) -> DRIFT-#35 ROOT validator (baseline (27,0,6,18,3) @ 446B).

The match-path run is the DRIFT-#35 declaration evidence: exactly ONE assertion
failure (baseline_match), all other 9 assertions passing. This script re-anchors
the docstring narrative + BASELINE_COMP to the new root. P-HIST invariant: the
count of historical 2576 references stays 2 (rebadged-from + chain insert).
"""
import re
import sys

PATH = "/home/z/my-project/scripts/validate_cycle2577.py"
text = open(PATH).read()

edits = [
    # 1) header provenance
    ("DRIFT-#34 verification-15 CARRY (post-loss rebadge lineage): "
     "rebadged from validate_cycle2576.py",
     "DRIFT-#35 ROOT validator (declared at c2577, 2026-10-27 ~00:08 +08): "
     "rebadged from validate_cycle2576.py (the match-path rebadge was executed FIRST "
     "and FAILED on baseline_match — that run is the DRIFT-#35 declaration evidence "
     "— then re-anchored to the new root baseline)", 1),
    # 2) baseline line
    ("(21,0,0,18,3) @ 446B DRIFT-#34 root; c2577 = verification 15",
     "(27,0,6,18,3) @ 446B DRIFT-#35 root; c2577 = DRIFT-#35 verification 1", 1),
    # 3) chain head — declare DRIFT-#35 root, close DRIFT-#34
    ("(c2576 = verification 14;",
     "(c2577 = DRIFT-#35 verification 1, ROOT — the movement: total 21->27 (+6), "
     "honest_free 0->6 (+6) HONEST INVENTORY EMERGENCE (first honest presence of the "
     "DRIFT-#34 span), honest_paid=0 = NO GOLD, scam 18 + unknown 3 unchanged, SIZE "
     "446B streak intact; DRIFT-#34 CLOSED at 14-fold (root c2563, verifications 1-14, "
     "14-of-59 = 23.7% of the DRIFT-#30 record span; chain context-carried post-LOSS-#5: "
     "DRIFT-#33 closed at 7-fold, DRIFT-#32 at 3-fold, DRIFT-#31 at 39-fold, DRIFT-#30 "
     "record 59-fold); c2576 = verification 14;", 1),
    # 4) assertions preamble
    ("Assertions encode the DRIFT-#34 baseline (21,0,0,18,3) @ 446B:",
     "Assertions encode the DRIFT-#35 baseline (27,0,6,18,3) @ 446B:", 1),
    # 5) composition bullet
    ("- BA composition: total=21 honest_paid=0 honest_free=0 scam=18 unknown=3",
     "- BA composition: total=27 honest_paid=0 honest_free=6 scam=18 unknown=3\n"
     "  (honest_free=6 = the DRIFT-#35 movement; aggregate-only visibility —\n"
     "  all_honest_paid covers PAID tasks, no per-task detail exposed for free;\n"
     "  the 6 honest free tasks are NOT taken per the PAID-only policy)", 1),
    # 6) code baseline
    ('BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 3}',
     'BASELINE_COMP = {"total": 27, "honest_paid": 0, "honest_free": 6, "scam": 18, "unknown": 3}', 1),
]

for old, new, expected in edits:
    c = text.count(old)
    assert c == expected, f"pre-patch count != {expected} for: {old[:60]!r} (got {c})"
    text = text.replace(old, new)

open(PATH, "w").write(text)

# P-HIST invariant: exactly 2 intentional 2576 references post-re-anchor
sites = [m.start() for m in re.finditer("2576", text)]
print(f"P-HIST 2576 refs = {len(sites)}")
for s in sites:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
if len(sites) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2576 references post-re-anchor")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert; no new historical refs)")
print(f"reanchored_ok={PATH}")
