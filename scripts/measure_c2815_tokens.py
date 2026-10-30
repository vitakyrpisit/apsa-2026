#!/usr/bin/env python3
"""P-HIST instrument for cycle 2815 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2815.py
(the v114->v115 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v114 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2812: 4, c2813: 4, c2814: 1}
total 258 — the c2814 Next-block compare base, re-verified live at this
cycle's census on the actual v114 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2814' prose rebadges to
c2815 (-1 c2814, +1 c2815 born-ONE — the forward-token lesson: the ONLY
c2815 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2814 in
the historical phrase ('pass-63 repeat recorded at c2814' — +1 c2814);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2814' in the observed list (+1 c2814) and 'pass-63 repeats at c2814'
(+1 c2814); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2813'
-> 'observed c2752/.../c2813/c2814' (c2814 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v114 Step-4 surfaces carry 'cycle2814'/'e2814'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE forecasting;
the class does NOT fire this cycle): the official c2814 commit hash 9fcdbae
short form = 9-f-c-d-b-a-e carries ONE 'c' character (position 2) — followed
by 'd' (non-digit, the run breaks) -> NO c+4-digit run -> the c7947-class
does NOT fire (zero artifact births; zero deaths — the v114 source carries
zero artifact tokens, the c97826 phantom already departed at v113); the
foreign TOP ef415bd short form carries NO 'c' character at all -> no
c+4-digit run, AND the foreign hash is ABSENT from the v114 source surface
(grep-verified at census time) — zero exposure for the validator surface.
Forecast: c2814 1->5 (+4 net), c2815 0->1 (+1 born-ONE), c2813 4->4 net
zero, total 258 -> 262 (+4 net).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2815.py"
raw = open(SRC, "rb").read()
text = raw.decode("utf-8")
tokens = re.findall(r"c(\d{4,})", text)
hist = Counter(f"c{t}" for t in tokens)
print(f"source_bytes={len(raw)}")
print(f"cycle_token_total={sum(hist.values())}")
print(f"p_hist_actual={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist.items()))} }}")
top = sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
print(f"top_tokens={top}")
print(f"c2814_count={hist.get('c2814', 0)} (forecast 1->5 +4 net)")
print(f"c2815_count={hist.get('c2815', 0)} (forecast 0->1 born-ONE)")
print(f"c2813_count={hist.get('c2813', 0)} (forecast 4->4 net zero)")
print(f"artifact_scan={[(k, v) for k, v in hist.items() if k in ('c97826', 'c7947', 'c4726', 'c415bd')]} "
      f"(forecast: zero artifact tokens — 9fcdbae carries no c+4-digit run; the "
      f"foreign ef415bd carries no 'c' character at all and is ABSENT from the source surface)")
sys.exit(0)
