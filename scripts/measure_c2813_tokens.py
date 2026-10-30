#!/usr/bin/env python3
"""P-HIST instrument for cycle 2813 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2813.py
(the v112->v113 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v112 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2810: 4, c2811: 4, c2812: 1, c97826: 1}
total 251 — the c2812 Next-block compare base, re-verified live at this
cycle's census on the actual v112 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2812' prose rebadges to
c2813 (-1 c2812, +1 c2813 born-ONE — the forward-token lesson: the ONLY
c2813 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2812 in
the historical phrase ('pass-61 repeat recorded at c2812' — +1 c2812);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2812' in the observed list (+1 c2812) and 'pass-61 repeats at c2812'
(+1 c2812); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2811'
-> 'observed c2752/.../c2811/c2812' (c2812 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v112 Step-4 surfaces carry 'cycle2812'/'e2812'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE forecasting;
the class does NOT fire this cycle): the official c2812 commit hash fcd7b1c
short form = f-c-d-7-b-1-c carries 'c' characters (positions 1 and 6) —
position 1 'c' is followed by 'd' (non-digit, the run breaks), position 6 'c'
is TERMINAL -> NO c+4-digit run -> the c7947-class does NOT fire (zero
artifact births); the v112 P2 'the 2c97826 commit object' carry rebadges AWAY
(the c97826 phantom token DEPARTS — ONE token death, the only exit surface;
the foreign TOP 30a3440 short form carries NO 'c' character at all — zero
exposure for the validator surface).
Forecast: c2812 1->4 (+3 net), c2813 0->1 (+1 born-ONE), c97826 1->0 (ONE
token DEATH — the phantom departs with the v112 P2 hash carry), total
251 -> 254 (+3 net).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2813.py"
raw = open(SRC, "rb").read()
text = raw.decode("utf-8")
tokens = re.findall(r"c(\d{4,})", text)
hist = Counter(f"c{t}" for t in tokens)
print(f"source_bytes={len(raw)}")
print(f"cycle_token_total={sum(hist.values())}")
print(f"p_hist_actual={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist.items()))} }}")
top = sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
print(f"top_tokens={top}")
print(f"artifact_c97826_count={hist.get('c97826', 0)} (the hash-artifact phantom — "
      f"forecast 1->0 DEPARTS with the v112 P2 hash carry; no c+4-digit run in "
      f"fcd7b1c, the c7947-class does NOT fire)")
print(f"c2812_count={hist.get('c2812', 0)} (forecast 1->4 +3 net)")
print(f"c2813_count={hist.get('c2813', 0)} (forecast 0->1 born-ONE)")
sys.exit(0)
