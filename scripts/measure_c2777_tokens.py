#!/usr/bin/env python3
"""P-HIST instrument for cycle 2777 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2777.py
(the v76->v77 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v76 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:1} total 106 —
the c2776 Next-block compare base) under the patch deltas — measured on
real bytes, never forecast. Patch delta forecast (for accounting only, the
MEASUREMENT governs): the P2 'Baseline for c2776' prose rebadges to c2777
(-1 c2776) while the pass-26 prose RE-INTRODUCES c2776 in the historical
phrase ('pass-25 repeat recorded at c2776') -> c2776 net 0 from P2; the
observed lists are APPEND-class (the c2761 forecast-miss / c2762..c2776
fifteen-consecutive-HIT lesson): P3 evidence prose gains '/c2776' in the
observed list (+1 c2776) and 'pass-25 repeats at c2776' (+1 c2776); P8 the
SIZE_BAND comment rebadges 'observed c2752/.../c2775' -> 'observed
c2752/.../c2775/c2776' (c2776 +1); P5/P6/P7 the CYCLE constant and
RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT c-tokens —
zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment carries
unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2776 commit hash 1ed1bdd short form = 1-e-d-1-b-d-d
— it carries NO 'c' material at all, so no c+4-digit run is possible in the
short form; the FULL hash 1ed1bdd92ab8192425419c4f916101f2aead0cfa carries
the c-runs 'c4f9' (c followed by one digit) and the terminal 'cfa' (c
followed by f) — none are c+4-digit runs; the foreign 2b2bd7b short form
carries no 'c' at all (its full hash 2b2bd7bcb03fc2be2d649ed936d4be2379e19e4a
carries 'c2b'/'fc2b' — c followed by one digit, no run) — NOTED, never
written into the validator source (the P2 paragraph carries the official
1ed1bdd short hash only; the short form has no c+4-digit run) — zero
artifact exposure; the c2777 commit hash is unborn at forecast time, checked
post-commit.
Forecast: c2776 1->4 (+3), c2777 0->1 (+1 born), total 106 -> 110 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2777.py"
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
