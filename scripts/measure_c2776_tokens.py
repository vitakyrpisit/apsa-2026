#!/usr/bin/env python3
"""P-HIST instrument for cycle 2776 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2776.py
(the v75->v76 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v75 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:1} total 102 — the c2775
Next-block compare base) under the patch deltas — measured on real bytes,
never forecast. Patch delta forecast (for accounting only, the MEASUREMENT
governs): the P2 'Baseline for c2775' prose rebadges to c2776 (-1 c2775)
while the pass-25 prose RE-INTRODUCES c2775 in the historical phrase
('pass-24 repeat recorded at c2775') -> c2775 net 0 from P2; the observed
lists are APPEND-class (the c2761 forecast-miss / c2762..c2775
fourteen-consecutive-HIT lesson): P3 evidence prose gains '/c2775' in the
observed list (+1 c2775) and 'pass-24 repeats at c2775' (+1 c2775); P8 the
SIZE_BAND comment rebadges 'observed c2752/.../c2774' -> 'observed
c2752/.../c2774/c2775' (c2775 +1); P5/P6/P7 the CYCLE constant and
RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT c-tokens —
zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment carries
unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2775 commit hash 932b4cc short form = 9-3-2-b-4-c-c
— the only 'c' material is the terminal 'cc' run, which is not a c+4-digit
run — no c+4-digit run possible in the short form; the FULL hash
932b4cc1dbdf74f352d7fdacf5d618f3b7a675c6 carries the c-runs 'cc1' (c
followed by c), 'cf5d' (c followed by f) and the 'c6'-terminal (c followed
by one digit) — none are c+4-digit runs; the foreign f9ecf31 short form
carries a single 'c' followed by 'f' — no c+4-digit run either — NOTED,
never written into the validator source (the P2 paragraph carries the
official 932b4cc short hash only; the short form has no c+4-digit run) —
zero artifact exposure; the c2776 commit hash is unborn at forecast time,
checked post-commit.
Forecast: c2775 1->4 (+3), c2776 0->1 (+1 born), total 102 -> 106 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2776.py"
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
