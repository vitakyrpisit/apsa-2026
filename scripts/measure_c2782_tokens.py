#!/usr/bin/env python3
"""P-HIST instrument for cycle 2782 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2782.py
(the v81->v82 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v81 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:1} total 126 — the c2781 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2781' prose rebadges to c2782 (-1 c2781) while the pass-31
prose RE-INTRODUCES c2781 in the historical phrase ('pass-30 repeat recorded
at c2781') -> c2781 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2781 twenty-consecutive-HIT lesson): P3
evidence prose gains '/c2781' in the observed list (+1 c2781) and 'pass-30
repeats at c2781' (+1 c2781); P8 the SIZE_BAND comment rebadges 'observed
c2752/.../c2780' -> 'observed c2752/.../c2780/c2781' (c2781 +1); P5/P6/P7 the
CYCLE constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2781 commit hash 8fa30df short form = 8-f-a-3-0-d-f
— ZERO 'c' characters in the short form, no c+4-digit run possible; the FULL
hash 8fa30dfd2dd1a10e69d2a3a2940aedc429009af1 DOES carry a c+digit run
('aedc429009af1' -> c followed by '429009', a c+4-digit-class run) — the
exposure is NIL because only the SHORT hash (zero 'c') enters the v82 P2
paragraph; nothing NOTED into the validator source; the foreign 51f1161 FULL
hash 51f1161d5e626629503212c94da54ad845ef8eda carries its single 'c' as
'2c94d' (c+2-digit, no c+4-digit run) and its short form carries no 'c' at
all; the c2782 commit hash is unborn at forecast time, checked post-commit.
Forecast: c2781 1->4 (+3), c2782 0->1 (+1 born), total 126 -> 130 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2782.py"
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
