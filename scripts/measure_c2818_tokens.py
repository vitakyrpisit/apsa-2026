#!/usr/bin/env python3
"""P-HIST instrument for cycle 2818 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2818.py
(the v117->v118 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v117 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2814: 4, c2815: 4, c2816: 4, c2817: 1}
total 270 — the c2817 Next-block compare base, re-verified live at this
cycle's census on the actual v117 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2817' prose rebadges to
c2818 (-1 c2817, +1 c2818 born-ONE — the forward-token lesson: the ONLY
c2818 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2817 in
the historical phrase ('pass-66 repeat recorded at c2817' — +1 c2817);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2817' in the observed list (+1 c2817) and 'pass-66 repeats at c2817'
(+1 c2817); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2816'
-> 'observed c2752/.../c2816/c2817' (c2817 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v117 Step-4 surfaces carry 'cycle2817'/'e2817'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE forecasting;
the class does NOT fire this cycle): the official c2817 commit hash da7d469
short form = d-a-7-d-4-6-9 carries ZERO 'c' characters -> no c+4-digit run ->
the c7947-class does NOT fire (zero artifact births; zero deaths — the v117
source carries zero artifact tokens, the c97826 phantom already departed at
v113); the foreign TOP a009715 short form carries NO 'c' character at all ->
no c+4-digit run in the short form, AND the foreign hash is ABSENT from the
v117 source surface (grep-verified at census time) — zero exposure for the
validator surface; HONEST NOTE: the FULL foreign hash
a009715c25167e97b9ccef6666cd202725805624 carries ONE c+4-digit run (c25167,
regex-measured at census time) BUT is ABSENT from the source surface — zero
exposure on any surface; the FULL c2817 hash
da7d4694ce7fb6ee6b39344027a147c3d6fb494c carries ZERO c+4-digit runs
(regex-measured at census time).
Forecast: c2817 1->4 (+3 net), c2818 0->1 (+1 born-ONE), c2816 4->4 net
zero, total 270 -> 274 (+4 net).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2818.py"
raw = open(SRC, "rb").read()
text = raw.decode("utf-8")
tokens = re.findall(r"c(\d{4,})", text)
hist = Counter(f"c{t}" for t in tokens)
print(f"source_bytes={len(raw)}")
print(f"cycle_token_total={sum(hist.values())}")
print(f"p_hist_actual={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist.items()))} }}")
top = sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
print(f"top_tokens={top}")
print(f"c2817_count={hist.get('c2817', 0)} (forecast 1->4 +3 net)")
print(f"c2818_count={hist.get('c2818', 0)} (forecast 0->1 born-ONE)")
print(f"c2816_count={hist.get('c2816', 0)} (forecast 4->4 net zero)")
print(f"artifact_scan={[(k, v) for k, v in hist.items() if k in ('c97826', 'c7947', 'c8402651', 'c4726', 'c415bd', 'c25167')]} "
      f"(forecast: zero artifact tokens — da7d469 carries no 'c' character at all "
      f"in the short form; the foreign a009715 carries no 'c' character in the "
      f"short form and is ABSENT from the source surface; the FULL foreign form "
      f"carries the c25167 run BUT is absent from the source surface; the FULL "
      f"c2817 hash carries ZERO c+4-digit runs regex-measured at census)")
sys.exit(0)
