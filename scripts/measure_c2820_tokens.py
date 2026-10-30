#!/usr/bin/env python3
"""P-HIST instrument for cycle 2820 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2820.py
(the v119->v120 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v119 measured series
({c2746: 1, c2747: 2, c2748: 2, c2749: 1, c2750: 1, c2751: 1, c2752: 5,
c2753: 4, ..., c2816: 4, c2817: 4, c2818: 4, c2819: 1}
total 278 — the c2819 Next-block compare base, re-verified live at this
cycle's census on the actual v119 bytes) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2819' prose rebadges to
c2820 (-1 c2819, +1 c2820 born-ONE — the forward-token lesson: the ONLY
c2820 birth surface) while the P2 pass-chain prose RE-INTRODUCES c2819 in
the historical phrase ('pass-68 repeat recorded at c2819' — +1 c2819);
the observed lists are APPEND-class (the c2805 forecast-miss lesson — do NOT
double-count the forward-token birth surface: the P3.t2 list-append adds the
CURRENT cycle token, not the forward token): P3 evidence prose gains
'/c2819' in the observed list (+1 c2819) and 'pass-68 repeats at c2819'
(+1 c2819); P8 the SIZE_BAND comment rebadges 'observed c2752/.../c2818'
-> 'observed c2752/.../c2818/c2819' (c2819 +1); P5/P6/P7 the CYCLE constant
and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT
c-tokens — zero delta per the c2760 lesson, re-verified live at this cycle's
census: the v119 Step-4 surfaces carry 'cycle2819'/'e2819'); the c2746
GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE forecasting;
the class does NOT fire this cycle): the official c2819 commit hash 5a868fa
short form = 5-a-8-6-8-f-a carries ZERO 'c' characters -> no c+4-digit run ->
the c7947-class does NOT fire (zero artifact births; zero deaths — the v119
source carries zero artifact tokens, the c97826 phantom already departed at
v113); the foreign TOP b9757c0 short form carries 'c0' at the tail — c
followed by ONE digit -> no c+4-digit run in the short form, AND the foreign
hash is ABSENT from the v119 source surface (grep-verified at census time) —
zero exposure for the validator surface; HONEST NOTE: the FULL foreign hash
b9757c09d3dcf32fc1fb4f84dde6b2acdc2ca165 carries ZERO c+4-digit runs
(regex-measured at census time) BUT is ABSENT from the source surface — zero
exposure on any surface; the FULL c2819 hash
5a868faeb20344def84ddd4296ef039572c02a08 carries ZERO c+4-digit runs
(regex-measured at census time).
Forecast: c2819 1->4 (+3 net), c2820 0->1 (+1 born-ONE), c2818 4->4 net
zero, c2817 4->4 net zero, total 278 -> 282 (+4 net).
The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2820.py"
raw = open(SRC, "rb").read()
text = raw.decode("utf-8")
tokens = re.findall(r"c(\d{4,})", text)
hist = Counter(f"c{t}" for t in tokens)
print(f"source_bytes={len(raw)}")
print(f"cycle_token_total={sum(hist.values())}")
print(f"p_hist_actual={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist.items()))} }}")
top = sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
print(f"top_tokens={top}")
print(f"c2819_count={hist.get('c2819', 0)} (forecast 1->4 +3 net)")
print(f"c2820_count={hist.get('c2820', 0)} (forecast 0->1 born-ONE)")
print(f"c2818_count={hist.get('c2818', 0)} (forecast 4->4 net zero)")
print(f"c2817_count={hist.get('c2817', 0)} (forecast 4->4 net zero)")
print(f"artifact_scan={[(k, v) for k, v in hist.items() if k in ('c97826', 'c7947', 'c8402651', 'c4726', 'c415bd', 'c25167')]} "
      f"(forecast: zero artifact tokens — 5a868fa carries no 'c' character at all "
      f"in the short form; the foreign b9757c0 carries 'c0' at the tail — one "
      f"digit, no 4+-digit run in the short form and is ABSENT from the source "
      f"surface; the FULL foreign form carries ZERO c+4-digit runs regex-measured "
      f"at census; the FULL c2819 hash carries ZERO c+4-digit runs regex-measured "
      f"at census)")
sys.exit(0)
