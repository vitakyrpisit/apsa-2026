#!/usr/bin/env python3
"""P-HIST instrument for cycle 2755 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2755.py
(the v54->v55 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v54 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:1} total 18 — the c2754 Next-block compare base) under the patch
deltas — measured on real bytes, never forecast. Patch delta forecast (for
accounting only, the MEASUREMENT governs): the P2 'Baseline for c2754'
prose rebadges to c2755 (-1 c2754, +1 c2755) while the pass-4 prose
RE-INTRODUCES c2754 in the historical phrase ('pass-3 repeat recorded at
c2754'); P3 evidence prose gains 'c2752/c2753/c2754' (+1 c2754) and 'pass-3
repeats at c2754' (+1 c2754); P8 the SIZE_BAND comment rebadges 'observed
c2752/c2753' -> 'observed c2752/c2753/c2754' (+1 c2754); the c2746
GOLD-CHECK comment carries unchanged. The 21c55c5 hash produces no c-token
artifact (2-1-c-5-5-c-5: no 'c' immediately followed by 4+ digits — the
2708896 digits-leading / 2dae73c trailing-c / d89bbea no-artifact precedent
classes); the c0f8578 HEAD hash is NOT referenced. The MEASUREMENT governs
over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2755.py"
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
