#!/usr/bin/env python3
"""P-HIST instrument for cycle 2807 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2807.py
(the v106->v107 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v106 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2804: 4, c2805: 4, c2806: 1}
total 226 — the c2806 Next-block compare base, re-verified live at this
cycle's census on the actual v106 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2806' prose rebadges to
c2807 (-1 c2806, +1 c2807 born-ONE — the forward-token lesson: the ONLY
c2807 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2806 in
the historical phrase ('pass-55 repeat recorded at c2806' — +1 c2806);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2806' in the observed list (+1 c2806) and 'pass-55 repeats at c2806'
(+1 c2806); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2805'
-> 'observed c2752/.../c2805/c2806' (c2806 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v106 Step-4 surfaces carry 'cycle2806'/'e2806'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2806 commit hash cceafc6 short form =
c-c-e-a-f-c-6 carries a 'c' character (position 0) followed by 'c' — NO
digit run — and a 'c' character (position 5) followed by '6' (a single
digit) — NO c+4-digit run, zero exposure; the v106 P2 'the ee9e3cd commit
object' rebadges away to 'the cceafc6 commit object' with ZERO token deaths
(ee9e3cd carries a 'c' character (position 5) followed by 'd' — NO c+4-digit
run, the c7947 class does NOT fire, c7947 stays exited); the foreign TOP
92a8201 short form carries NO 'c' character at all — zero exposure for the
validator surface.
Forecast: c2806 1->4 (+3 net), c2807 0->1 (+1 born-ONE), total 226 -> 230 (+4).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2807.py"
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
