#!/usr/bin/env python3
"""P-HIST instrument for cycle 2772 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2772.py
(the v71->v72 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v71 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:1} total 86 — the c2771 Next-block compare base) under the
patch deltas — measured on real bytes, never forecast.
Patch delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2771' prose rebadges to c2772 (-1 c2771) while the pass-21
prose RE-INTRODUCES c2771 in the historical phrase ('pass-20 repeat recorded
at c2771') -> c2771 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2771 ten-consecutive-HIT lesson): P3 evidence
prose gains '/c2771' in the observed list (+1 c2771) and 'pass-20 repeats at
c2771' (+1 c2771); P8 the SIZE_BAND comment rebadges 'observed c2752/.../
c2770' -> 'observed c2752/.../c2770/c2771' (c2771 +1); P5/P6/P7 the CYCLE
constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2771 commit hash 71880e8 = 7-1-8-8-0-e-8, no 'c'
run at all — no artifact; the foreign dd48816 FULL hash
dd4881622ee281c13918088f38723b17eb6a3e8b contains the c-run 'c13918088' —
NOTED, but the foreign hash is never written into the validator source (the
P2 paragraph carries the official 71880e8 short hash only; the short form
dd48816 has no c-run) — zero artifact exposure; the c2772 commit hash is
unborn at forecast time, checked post-commit.
Forecast: c2771 1->4 (+3), c2772 0->1 (+1 born), total 86 -> 90 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2772.py"
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
