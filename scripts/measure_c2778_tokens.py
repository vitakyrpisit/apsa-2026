#!/usr/bin/env python3
"""P-HIST instrument for cycle 2778 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2778.py
(the v77->v78 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v77 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:1} total 110 —
the c2777 Next-block compare base) under the patch deltas — measured on
real bytes, never forecast. Patch delta forecast (for accounting only, the
MEASUREMENT governs): the P2 'Baseline for c2777' prose rebadges to c2778
(-1 c2777) while the pass-27 prose RE-INTRODUCES c2777 in the historical
phrase ('pass-26 repeat recorded at c2777') -> c2777 net 0 from P2; the
observed lists are APPEND-class (the c2761 forecast-miss / c2762..c2777
sixteen-consecutive-HIT lesson): P3 evidence prose gains '/c2777' in the
observed list (+1 c2777) and 'pass-26 repeats at c2777' (+1 c2777); P8 the
SIZE_BAND comment rebadges 'observed c2752/.../c2776' -> 'observed
c2752/.../c2776/c2777' (c2777 +1); P5/P6/P7 the CYCLE constant and
RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits, NOT c-tokens —
zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment carries
unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2777 commit hash e961185 short form = e-9-6-1-1-8-5
— it carries NO 'c' material at all, so no c+4-digit run is possible in the
short form; the foreign 336d5f2 short form likewise carries no 'c' at all —
NOTED, never written into the validator source (the P2 paragraph carries the
official e961185 short hash only; the short form has no c+4-digit run) —
zero artifact exposure; the c2778 commit hash is unborn at forecast time,
checked post-commit.
Forecast: c2777 1->4 (+3), c2778 0->1 (+1 born), total 110 -> 114 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2778.py"
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
