#!/usr/bin/env python3
"""P-HIST instrument for cycle 2802 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2802.py
(the v101->v102 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v101 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
..., c2798:4, c2799:4, c2800:4, c2801:1}
total 206 — the c2801 Next-block compare base) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2801' prose rebadges to
c2802 (-1 c2801, +1 c2802 born) while the P2 pass-chain prose RE-INTRODUCES
c2801 in the historical phrase ('pass-50 repeat recorded at c2801' — +1
c2801, c2801 net +3 with the P3/P8 surfaces); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2801 forty-consecutive-HIT
lesson): P3 evidence prose gains '/c2801' in the observed list (+1 c2801)
and 'pass-50 repeats at c2801' (+1 c2801); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2800' -> 'observed c2752/.../c2800/c2801' (c2801 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson,
re-verified live at this cycle's census: the v101 Step-4 surfaces carry
'cycle2801'/'e2801'); the c2746 GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2801 commit hash c57c12a short form =
c-5-7-c-1-2-a carries TWO 'c' characters but NO c+4-digit run (both runs
break before 4 digits: 'c57c' and 'c12a') — zero new hash-artifact birth,
zero exposure; the v101 P2 'the e829f19 commit object' rebadges away to
'the c57c12a commit object' and since e829f19 carries NO 'c' character at
all there is NO token death (the c7947 class does NOT fire — c7947 already
exited the histogram at v88); the foreign TOP e6da641 short form =
e-6-d-a-6-4-1 carries NO 'c' character at all — zero c+4-digit run, zero
exposure for the validator surface.
Forecast: c2801 1->4 (+3 net), c2802 0->1 (+1 born), total 206 -> 210 (+4).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2802.py"
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
