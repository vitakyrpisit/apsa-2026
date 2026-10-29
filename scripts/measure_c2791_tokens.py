#!/usr/bin/env python3
"""P-HIST instrument for cycle 2791 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2791.py
(the v90->v91 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v90 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:4, c2784:4, c2785:4,
c2786:4, c2787:4, c2788:4, c2789:4, c2790:1} total 162 — the c2790 Next-block
compare base) under the patch deltas — measured on real bytes, never
forecast. Patch delta forecast (for accounting only, the MEASUREMENT
governs): the P2 'Baseline for c2790' prose rebadges to c2791 (-1 c2790,
+1 c2791 born) while the P2 pass-chain prose RE-INTRODUCES c2790 in the
historical phrase ('pass-39 repeat recorded at c2790' — +1 c2790, c2789 net
0 from the chain rewrite); the observed lists are APPEND-class (the c2761
forecast-miss / c2762..c2790 twenty-nine-consecutive-HIT lesson): P3 evidence
prose gains '/c2790' in the observed list (+1 c2790) and 'pass-39 repeats at
c2790' (+1 c2790); P8 the SIZE_BAND comment rebadges 'observed c2752/.../
c2789' -> 'observed c2752/.../c2789/c2790' (c2790 +1); P5/P6/P7 the CYCLE
constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson, re-verified live at this
cycle's census: the v90 Step-3 surfaces carry 'cycle2790'/'e2790'); the
c2746 GOLD-CHECK comment carries unchanged. HASH-ARTIFACT watch (the
c3819e9 + c7947 lessons — checked BEFORE forecasting): the official c2790
commit hash e4a79df short form = e-4-a-7-9-d-f carries NO 'c' character at
all — NO c+4-digit run, no new hash-artifact birth; the v90 P2 carry 'the
2af9fd7 commit object' rebadges AWAY to 'the e4a79df commit object', and
since 2af9fd7 also carries no 'c' there is NO token death (the c7947 class
does NOT fire — c7947 already exited the histogram at v88); the foreign TOP
3b69581 short form = 3-b-6-9-5-8-1 carries NO 'c' either — zero exposure for
the validator surface.
Forecast: c2790 1->4 (+3), c2791 0->1 (+1 born), total 162 -> 166 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2791.py"
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
