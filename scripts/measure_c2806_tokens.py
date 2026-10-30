#!/usr/bin/env python3
"""P-HIST instrument for cycle 2806 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2806.py
(the v105->v106 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v105 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2803: 4, c2804: 4, c2805: 1}
total 222 — the c2805 Next-block compare base, re-verified live at this
cycle's census on the actual v105 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2805' prose rebadges to
c2806 (-1 c2805, +1 c2806 born-ONE — the forward-token lesson: the ONLY
c2806 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2805 in
the historical phrase ('pass-54 repeat recorded at c2805' — +1 c2805);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2805' in the observed list (+1 c2805) and 'pass-54 repeats at c2805'
(+1 c2805); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2804'
-> 'observed c2752/.../c2804/c2805' (c2805 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v105 Step-4 surfaces carry 'cycle2805'/'e2805'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2805 commit hash ee9e3cd short form =
e-e-9-e-3-c-d carries a 'c' character (position 5) followed by 'd' — NO
c+4-digit run, zero exposure; the v105 P2 'the cbdb675 commit object'
rebadges away to 'the ee9e3cd commit object' with ZERO token deaths
(cbdb675 carries a 'c' character (position 0) followed by 'b' — the c7947
class does NOT fire, c7947 stays exited); the foreign TOP 35ba192 short
form = 3-5-b-a-1-9-2 carries NO 'c' character at all — NO c+4-digit run,
zero exposure for the validator surface.
Forecast: c2805 1->4 (+3 net), c2806 0->1 (+1 born-ONE), total 222 -> 226 (+4).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2806.py"
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
