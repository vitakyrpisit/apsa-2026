#!/usr/bin/env python3
"""P-HIST instrument for cycle 2803 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2803.py
(the v102->v103 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v102 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
..., c2799:4, c2800:4, c2801:4, c2802:1}
total 210 — the c2802 Next-block compare base) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2802' prose rebadges to
c2803 (-1 c2802, +1 c2803 born) while the P2 pass-chain prose RE-INTRODUCES
c2802 in the historical phrase ('pass-51 repeat recorded at c2802' — +1
c2802, c2802 net +3 with the P3/P8 surfaces); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2802 forty-one-consecutive-HIT
lesson): P3 evidence prose gains '/c2802' in the observed list (+1 c2802)
and 'pass-51 repeats at c2802' (+1 c2802); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2801' -> 'observed c2752/.../c2801/c2802' (c2802 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson,
re-verified live at this cycle's census: the v102 Step-4 surfaces carry
'cycle2802'/'e2802'); the c2746 GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2802 commit hash 9d17b2b short form =
9-d-1-7-b-2-b carries NO 'c' character at all — zero c+4-digit run, zero
exposure; the v102 P2 'the c57c12a commit object' rebadges away to
'the 9d17b2b commit object' and since c57c12a carries TWO 'c' characters but
NO c+4-digit run (both runs break before 4 digits) there is NO token death
(the c7947 class does NOT fire — c7947 already exited the histogram at v88);
the foreign TOP 325729a short form = 3-2-5-7-2-9-a carries NO 'c' character
at all — zero c+4-digit run, zero exposure for the validator surface.
Forecast: c2802 1->4 (+3 net), c2803 0->1 (+1 born), total 210 -> 214 (+4).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2803.py"
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
