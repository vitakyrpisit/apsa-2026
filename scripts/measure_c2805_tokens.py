#!/usr/bin/env python3
"""P-HIST instrument for cycle 2805 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2805.py
(the v104->v105 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v104 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2802: 4, c2803: 4, c2804: 1}
total 218 — the c2804 Next-block compare base, re-verified live at this
cycle's census on the actual v104 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2804' prose rebadges to
c2805 (-1 c2804, +1 c2805 born) while the P2 pass-chain prose RE-INTRODUCES
c2804 in the historical phrase ('pass-53 repeat recorded at c2804' — +1
c2804, c2804 net +3 with the P3/P8 surfaces); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2804 forty-three-consecutive-
HIT lesson): P3 evidence prose gains '/c2804' in the observed list (+1 c2804)
and 'pass-53 repeats at c2804' (+1 c2804); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2803' -> 'observed c2752/.../c2803/c2804' (c2804 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson,
re-verified live at this cycle's census: the v104 Step-4 surfaces carry
'cycle2804'/'e2804'); the c2746 GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2804 commit hash cbdb675 short form =
c-b-d-b-6-7-5 carries a 'c' character (position 0) followed by 'b' — NO
c+4-digit run, zero exposure; the v104 P2 'the 597a622 commit object'
rebadges away to 'the cbdb675 commit object' with ZERO token deaths (597a622
carries NO 'c' character at all, the c7947 class does NOT fire — c7947
already exited the histogram at v88); the foreign TOP a6fac67 short form =
a-6-f-a-c-6-7 — the 'c' at position 4 is followed by '6','7' (a 2-digit run
only) — NO c+4-digit run, zero exposure for the validator surface.
Forecast: c2804 1->4 (+3 net), c2805 0->2 (+2 born), total 218 -> 223 (+5).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2805.py"
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
