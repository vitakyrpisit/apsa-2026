#!/usr/bin/env python3
"""Claim-scope correction for validate_cycle2623.py (DRIFT-#45 ROOT harness).

The reanchor initially wrote "the FIRST unknown=0 print ... of the on-disk ledger
era (c2453..)". Worklog grep archaeology (pre-commit) found 34 prior unknown=0
prints at worklog lines 6214..6808 — the pre-LOSS-#5 snapshot portion, an earlier
market regime with composition (40,1,9,30,0). The post-LOSS-#5 regrown ledger
(c2568.., lines 7859+) has ZERO unknown=0 hits (verified). The c2454..c2567 span
is context-carried with no unknown values cited. The claim is re-scoped
accordingly — the (18,0,0,18,0) five-tuple first-print claim is UNCHANGED (0 prior
literal hits across the ENTIRE on-disk file, verified).
"""
import py_compile

DST = "/home/z/my-project/scripts/validate_cycle2623.py"
text = open(DST).read()

def rep(old, new, label):
    c = text.count(old)
    assert c == 1, f"{label} pre-patch count != 1: {c}"
    return text.replace(old, new)

# Site 1: chain narrative (line 9)
text = rep(
    "the unknown category EXITS the board entirely — the FIRST unknown=0 print "
    "and FIRST (18,0,0,18,0) five-tuple of the on-disk ledger era (c2453..), "
    "landing on the LOWER EDGE of the predicted DRIFT-#45 live band",
    "the unknown category EXITS the board entirely — the FIRST unknown=0 print "
    "and FIRST (18,0,0,18,0) five-tuple of the post-LOSS-#5 on-disk ledger "
    "(c2568..; 34 prior unknown=0 prints exist in the pre-LOSS-#5 snapshot "
    "portion — an earlier (40,1,9,30,0) regime — and the c2454..c2567 span is "
    "context-carried with no unknown values cited), landing on the LOWER EDGE "
    "of the predicted DRIFT-#45 live band",
    "chain-scope",
)

# Site 2: BA-composition bullet (lines 30-31)
text = rep(
    "zero honest, zero unknown — the FIRST unknown=0 print of the on-disk ledger\n"
    "  era); honest_free=0 HOLDS at zero",
    "zero honest, zero unknown — the FIRST unknown=0 print of the post-LOSS-#5\n"
    "  on-disk ledger (c2568..)); honest_free=0 HOLDS at zero",
    "bullet-scope",
)

open(DST, "w").write(text)
py_compile.compile(DST, doraise=True)
print("scope correction complete: both sites re-patched, py_compile OK")
