#!/usr/bin/env python3
"""P-HIST instrument for cycle 2756 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2756.py
(the v55->v56 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v55 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:1} total 22 — the c2755 Next-block compare base) under the
patch deltas — measured on real bytes, never forecast. Patch delta forecast
(for accounting only, the MEASUREMENT governs): the P2 'Baseline for c2755'
prose rebadges to c2756 (-1 c2755, +1 c2756) while the pass-5 prose
RE-INTRODUCES c2755 in the historical phrase ('pass-4 repeat recorded at
c2755'); P3 evidence prose gains 'c2752/c2753/c2754/c2755' (+1 c2755) and
'pass-4 repeats at c2755' (+1 c2755); P8 the SIZE_BAND comment rebadges
'observed c2752/c2753/c2754' -> 'observed c2752/c2753/c2754/c2755' (+1
c2755); the c2746 GOLD-CHECK comment carries unchanged. The 7563b44 hash
produces no c-token artifact (7-5-6-3-b-4-4: no 'c' immediately followed by
4+ digits — the 2708896 digits-leading / 2dae73c trailing-c / d89bbea /
21c55c5 no-artifact precedent classes); the 95eaed7 HEAD hash is NOT
referenced. The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2756.py"
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
