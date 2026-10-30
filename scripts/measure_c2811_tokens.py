#!/usr/bin/env python3
"""P-HIST instrument for cycle 2811 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2811.py
(the v110->v111 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v110 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2808: 4, c2809: 4, c2810: 1}
total 242 — the c2810 Next-block compare base, re-verified live at this
cycle's census on the actual v110 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2810' prose rebadges to
c2811 (-1 c2810, +1 c2811 born-ONE — the forward-token lesson: the ONLY
c2811 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2810 in
the historical phrase ('pass-59 repeat recorded at c2810' — +1 c2810);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2810' in the observed list (+1 c2810) and 'pass-59 repeats at c2810'
(+1 c2810); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2809'
-> 'observed c2752/.../c2809/c2810' (c2810 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v110 Step-4 surfaces carry 'cycle2810'/'e2810'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2810 commit hash d228cc8 short form =
d-2-2-8-c-c-8 carries 'c' characters (positions 4 and 5) — position 4 'c' is
followed by 'c' (not a digit), position 5 'c' is followed by '8' then END —
NO c+4-digit run, zero hash-artifact birth, zero exposure; the v111 P2
paragraph carries 'the d228cc8 commit object' (zero new hash-artifact birth),
while the v110 P2 carry 'the d19b6ac commit object' rebadges AWAY (d19b6ac
carries a 'c' character (position 6, terminal) — NO c+4-digit run, zero token
deaths, the c7947 class does NOT fire — c7947 already exited the histogram at
v88); the foreign TOP 92b5acc short form = 9-2-b-5-a-c-c carries 'c'
characters (positions 6 and 7, terminal) — NO c+4-digit run, zero exposure
for the validator surface.
Forecast: c2810 1->4 (+3 net), c2811 0->1 (+1 born-ONE), total 242 -> 246 (+4).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2811.py"
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
