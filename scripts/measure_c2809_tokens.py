#!/usr/bin/env python3
"""P-HIST instrument for cycle 2809 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2809.py
(the v108->v109 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v108 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2806: 4, c2807: 4, c2808: 1}
total 234 — the c2808 Next-block compare base, re-verified live at this
cycle's census on the actual v108 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2808' prose rebadges to
c2809 (-1 c2808, +1 c2809 born-ONE — the forward-token lesson: the ONLY
c2809 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2808 in
the historical phrase ('pass-57 repeat recorded at c2808' — +1 c2808);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2808' in the observed list (+1 c2808) and 'pass-57 repeats at c2808'
(+1 c2808); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2807'
-> 'observed c2752/.../c2807/c2808' (c2808 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v108 Step-4 surfaces carry 'cycle2808'/'e2808'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2808 commit hash 3c0fe6c short form =
3-c-0-f-e-6-c carries a 'c' character (position 1) followed by '0' (a single
digit then 'f') and a terminal 'c' (position 6) — NO c+4-digit run, zero
exposure; the v108 P2 'the 276a60a commit object' rebadged away to 'the
3c0fe6c commit object' with ZERO token deaths (276a60a carries NO 'c'
character at all — the c7947 class does NOT fire, c7947 stays exited); the
foreign 7f7a022 short form carries NO 'c' character at all — zero exposure
for the validator surface.
Forecast: c2808 1->4 (+3 net), c2809 0->1 (+1 born-ONE), total 234 -> 238 (+4).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2809.py"
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
