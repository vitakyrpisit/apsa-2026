#!/usr/bin/env python3
"""P-HIST instrument for cycle 2783 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2783.py
(the v82->v83 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v82 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:1} total 130 — the c2782 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2782' prose rebadges to c2783 (-1 c2782) while the pass-32
prose RE-INTRODUCES c2782 in the historical phrase ('pass-31 repeat recorded
at c2782') -> c2782 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2782 twenty-one-consecutive-HIT lesson): P3
evidence prose gains '/c2782' in the observed list (+1 c2782) and 'pass-31
repeats at c2782' (+1 c2782); P8 the SIZE_BAND comment rebadges 'observed
c2752/.../c2781' -> 'observed c2752/.../c2781/c2782' (c2782 +1); P5/P6/P7 the
CYCLE constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2782 commit hash 2be3f8a short form = 2-b-e-3-f-8-a
— ZERO 'c' characters in the short form, no c+4-digit run possible; the FULL
hash 2be3f8a6c2788f1f99c61a088f45de72415a9eec DOES carry a c+4-digit-class run
('6c2788f1f9' -> c followed by '2788' — the run even reads as a future-cycle
token shape, noted honestly, nothing NOTED into the validator source) — the
exposure is NIL because only the SHORT hash (zero 'c') enters the v83 P2
paragraph (the P2 paragraph carries the official 2be3f8a short hash only);
the foreign f076455 short form carries NO 'c' at all and its FULL hash
f0764553b38036c2e6506d9dc3fa3b8dbf6138f3 carries its 'c's as '6c2e6'/'9dc3f'
(c+1-digit, no c+4-digit run) — zero exposure either way; the c2783 commit
hash is unborn at forecast time, checked post-commit.
Forecast: c2782 1->4 (+3), c2783 0->1 (+1 born), total 130 -> 134 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2783.py"
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
