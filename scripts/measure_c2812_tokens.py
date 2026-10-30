#!/usr/bin/env python3
"""P-HIST instrument for cycle 2812 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2812.py
(the v111->v112 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v111 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2809: 4, c2810: 4, c2811: 1}
total 246 — the c2811 Next-block compare base, re-verified live at this
cycle's census on the actual v111 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2811' prose rebadges to
c2812 (-1 c2811, +1 c2812 born-ONE — the forward-token lesson: the ONLY
c2812 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2811 in
the historical phrase ('pass-60 repeat recorded at c2811' — +1 c2811);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2811' in the observed list (+1 c2811) and 'pass-60 repeats at c2811'
(+1 c2811); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2810'
-> 'observed c2752/.../c2810/c2811' (c2811 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v111 Step-4 surfaces carry 'cycle2811'/'e2811'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — the class FIRES this
cycle, checked BEFORE forecasting): the official c2811 commit hash 2c97826
short form = 2-c-9-7-8-2-6 carries 'c' characters (positions 1, 5 and 6) —
position 1 'c' is followed by '9782' = FOUR digits -> the c+4-digit RUN
EXISTS -> the c7947-class FIRES: the v112 P2 paragraph carries 'the 2c97826
commit object' (the c(\d{4,}) surface gains the phantom artifact token
c97826 — ONE hash-artifact birth declared pre-patch; the v111 P2 carry
'the d228cc8 commit object' rebadges AWAY (d228cc8 carries 'c' at positions
4/5 — NO c+4-digit run, zero token deaths); the foreign TOP c5fb5cc short
form carries 'c' characters (positions 0, 5, 6 — the c5f run broken by 'f',
'cc' terminal) — NO c+4-digit run, zero exposure
for the validator surface.
Forecast: c2811 1->4 (+3 net), c2812 0->1 (+1 born-ONE), c97826 0->1
(+1 hash-artifact birth — the c7947-class FIRES), total 246 -> 251 (+5).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2812.py"
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
      f"forecast 0->1; the c7947-class FIRES this cycle)")
print(f"c2811_count={hist.get('c2811', 0)} (forecast 1->4 +3 net)")
print(f"c2812_count={hist.get('c2812', 0)} (forecast 0->1 born-ONE)")
sys.exit(0)
