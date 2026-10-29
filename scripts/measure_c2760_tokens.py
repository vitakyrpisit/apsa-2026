#!/usr/bin/env python3
"""P-HIST instrument for cycle 2760 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2760.py
(the v59->v60 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v59 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:1, c3819:1} total 39 —
the c2759 Next-block compare base) under the patch deltas — measured on
real bytes, never forecast. Patch delta forecast (for accounting only, the
MEASUREMENT governs): the P2 'Baseline for c2759' prose rebadges to c2760
(-1 c2759, +1 c2760) while the pass-9 prose RE-INTRODUCES c2759 in the
historical phrase ('pass-8 repeat recorded at c2759') -> c2759 net 0; the
v59->v60 carry swap retires the c3819e9 commit-hash ARTIFACT (c3819 -1 —
the b867cb7 hash produces NO c-token artifact: b-8-6-7-c-b-7, no 'c'
immediately followed by 4+ digits — the 21c55c5/7563b44/2848a78/fe2e08c/
d990e91 no-artifact precedent classes, per the c3819e9 lesson the fresh
c2760 commit hash gets checked BEFORE the next forecast); P3 evidence prose
gains 'c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759' (+1 c2759) and
'pass-8 repeats at c2759' (+1 c2759); P8 the SIZE_BAND comment rebadges
'observed c2752/c2753/c2754/c2755/c2756/c2757/c2758' -> 'observed
c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759' (c2758 -1, c2759 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (c2759 -3,
c2760 +3); the c2746 GOLD-CHECK comment carries unchanged. Forecast:
c2758 4->3, c2759 1->1, c2760 0->4, c3819 1->0, total 39 -> 41 (+2). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2760.py"
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
