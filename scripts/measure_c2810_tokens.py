#!/usr/bin/env python3
"""P-HIST instrument for cycle 2810 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2810.py
(the v109->v110 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v109 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2807: 4, c2808: 4, c2809: 1}
total 238 — the c2809 Next-block compare base, re-verified live at this
cycle's census on the actual v109 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2809' prose rebadges to
c2810 (-1 c2809, +1 c2810 born-ONE — the forward-token lesson: the ONLY
c2810 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2809 in
the historical phrase ('pass-58 repeat recorded at c2809' — +1 c2809);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2809' in the observed list (+1 c2809) and 'pass-58 repeats at c2809'
(+1 c2809); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2808'
-> 'observed c2752/.../c2808/c2809' (c2809 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v109 Step-4 surfaces carry 'cycle2809'/'e2809'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2809 commit hash d19b6ac short form =
d-1-9-b-6-a-c carries a 'c' character (position 6, terminal) — NO c+4-digit
run, zero exposure; the v109 P2 'the 3c0fe6c commit object' rebadged away to
'the d19b6ac commit object' with ZERO token deaths (3c0fe6c carries 'c'
characters (positions 1 and 6) — NO c+4-digit run, the c7947 class does NOT
fire, c7947 stays exited); the foreign 1288d7f short form carries NO 'c'
character at all — zero exposure for the validator surface.
Forecast: c2809 1->4 (+3 net), c2810 0->1 (+1 born-ONE), total 238 -> 242 (+4).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2810.py"
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
