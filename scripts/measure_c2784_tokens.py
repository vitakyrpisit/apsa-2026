#!/usr/bin/env python3
"""P-HIST instrument for cycle 2784 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2784.py
(the v83->v84 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v83 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:1} total 134 — the c2783 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2783' prose rebadges to c2784 (-1 c2783) while the pass-33
prose RE-INTRODUCES c2783 in the historical phrase ('pass-32 repeat recorded
at c2783') -> c2783 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2783 twenty-two-consecutive-HIT lesson): P3
evidence prose gains '/c2783' in the observed list (+1 c2783) and 'pass-32
repeats at c2783' (+1 c2783); P8 the SIZE_BAND comment rebadges 'observed
c2752/.../c2782' -> 'observed c2752/.../c2782/c2783' (c2783 +1); P5/P6/P7 the
CYCLE constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2783 commit hash 11ae7e3 short form = 1-1-a-e-7-e-3
— ZERO 'c' characters in the short form, no c+4-digit run possible; the FULL
hash 11ae7e3c7d158ba4906a1a96f34fd25e294ba361 carries its single 'c' as 'c7d15'
(c followed by '7d15' — c+digit then a letter, NO c+4-digit run) — exposure
NIL because only the SHORT hash (zero 'c') enters the v84 P2 paragraph (the
P2 paragraph carries the official 11ae7e3 short hash only); the foreign
b9b0ce0 short form carries its 'c' as 'ce0' (c+letter, no digit run) and the
FULL hash b9b0ce07a8213f17a59f929065924d9bfc330dd3 carries its 'c's as
'ce07'/'bfc33'/'c330d' (c+letter and c+3-digit classes, no c+4-digit run) —
zero exposure either way; the c2784 commit hash is unborn at forecast time,
checked post-commit.
Forecast: c2783 1->4 (+3), c2784 0->1 (+1 born), total 134 -> 138 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2784.py"
raw = open(SRC, "rb").read()
text = raw.decode("utf-8")
tokens = re.findall(r"c(\d{4,})", text)
hist = Counter(f"c{t}" for t in tokens)
print(f"source_bytes={len(raw)}")
print(f"cycle_token_total={sum(hist.values())}")
print(f"p_hist_actual={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist.items()))} }}")
top = sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
print(f"top_tokens={top}")
sys.exit(0)
