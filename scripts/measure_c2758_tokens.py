#!/usr/bin/env python3
"""P-HIST instrument for cycle 2758 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2758.py
(the v57->v58 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v57 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:1} total 30 — the c2757 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2757' prose rebadges to c2758 (-1 c2757, +1 c2758) while the
pass-7 prose RE-INTRODUCES c2757 in the historical phrase ('pass-6 repeat
recorded at c2757'); P3 evidence prose gains 'c2752/c2753/c2754/c2755/c2756/
c2757' (+1 c2757) and 'pass-6 repeats at c2757' (+1 c2757); P8 the SIZE_BAND
comment rebadges 'observed c2752/c2753/c2754/c2755/c2756' -> 'observed
c2752/c2753/c2754/c2755/c2756/c2757' (+1 c2757); the c2746 GOLD-CHECK comment
carries unchanged. The fe2e08c hash produces no c-token artifact (f-e-2-e-0-8-c:
no 'c' immediately followed by 4+ digits — the 2708896 digits-leading /
2dae73c trailing-c / d89bbea / 21c55c5 / 7563b44 / 2848a78 no-artifact
precedent classes); the d990e91 HEAD hash is NOT referenced. The MEASUREMENT
governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2758.py"
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
