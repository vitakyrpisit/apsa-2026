#!/usr/bin/env python3
"""P-HIST instrument for cycle 2754 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2754.py
(the v53->v54 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v53 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:4, c2753:1}
total 13 — the c2753 Next-block compare base) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for
accounting only, the MEASUREMENT governs): the P2 'Baseline for c2753'
prose rebadges to c2754 (-1 c2753, +1 c2754) while the pass-3 prose
RE-INTRODUCES c2753 in the historical phrase ('pass-2 repeat recorded at
c2753'); P3 evidence prose gains 'c2752/c2753' (+1 c2753, c2752 unchanged
via the series form); the SIZE_BAND comment rebadges 'observed c2752' ->
'observed c2752/c2753' (+1 c2753); the c2746 GOLD-CHECK comment carries
unchanged. The d89bbea hash produces no c-token artifact (d-8-9-b-b-e-a:
no 'c' immediately followed by digits — the 2708896 digits-leading /
2dae73c trailing-c precedent classes); the b6a94e3/9bdccb2 HEAD hashes
are NOT referenced. The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2754.py"
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
