#!/usr/bin/env python3
"""P-HIST instrument for cycle 2763 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2763.py
(the v62->v63 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v62 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:1} total 50 — the c2762 Next-block compare base) under the patch
deltas — measured on real bytes, never forecast. Patch delta forecast (for
accounting only, the MEASUREMENT governs): the P2 'Baseline for c2762' prose
rebadges to c2763 (-1 c2762, +1 c2763) while the pass-12 prose RE-INTRODUCES
c2762 in the historical phrase ('pass-11 repeat recorded at c2762') -> c2762
net 0 from P2; the observed lists are APPEND-class (the c2761 forecast-miss /
c2762 forecast-HIT lesson): P3 evidence prose gains '/c2762' in the observed
list (+1 c2762) and 'pass-11 repeats at c2762' (+1 c2762); P8 the SIZE_BAND
comment rebadges 'observed c2752/.../c2761' -> 'observed
c2752/.../c2761/c2762' (c2762 +1); P5/P6/P7 the CYCLE constant and
RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT c-tokens —
zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment carries
unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2762 commit hash 737476a = 7-3-7-4-7-6-a, no 'c'
immediately followed by 4+ digits — no artifact; the c2763 commit hash is
unborn at forecast time, checked post-commit.
Forecast: c2762 1->4 (+3), c2763 0->1 (+1 born), total 50 -> 54 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2763.py"
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
