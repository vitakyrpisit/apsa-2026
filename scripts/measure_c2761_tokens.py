#!/usr/bin/env python3
"""P-HIST instrument for cycle 2761 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2761.py
(the v60->v61 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v60 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:1} total 42 —
the c2760 Next-block compare base) under the patch deltas — measured on
real bytes, never forecast. Patch delta forecast (for accounting only, the
MEASUREMENT governs): the P2 'Baseline for c2760' prose rebadges to c2761
(-1 c2760, +1 c2761) while the pass-10 prose RE-INTRODUCES c2760 in the
historical phrase ('pass-9 repeat recorded at c2760') -> c2760 net 0; the
v60->v61 carry swap retires NO hash artifact unless the fresh c2760 commit
hash (b20837e) or the c2761 commit hash carries 'c'+4-digits (checked BEFORE
forecast per the c3819e9 lesson: b20837e = b-2-0-8-3-7-e, no 'c' immediately
followed by 4+ digits — no artifact); P3 evidence prose gains '/c2760' in the
observed list (+1 c2760) and 'pass-9 repeats at c2760' (+1 c2760); P8 the
SIZE_BAND comment rebadges 'observed c2752/.../c2759' -> 'observed
c2752/.../c2760' (c2760 +1); P5/P6/P7 the CYCLE constant and RAW/PRETTY
paths rebadge (path tokens are 'e'-before-digits, NOT c-tokens — zero delta
per the c2760 lesson); the c2746 GOLD-CHECK comment carries unchanged.
Forecast: c2759 4->3, c2760 1->3, c2761 0->2, total 42 -> 43 (+1). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2761.py"
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
