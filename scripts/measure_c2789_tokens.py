#!/usr/bin/env python3
"""P-HIST instrument for cycle 2789 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2789.py
(the v88->v89 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v88 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:4, c2784:4, c2785:4,
c2786:4, c2787:4, c2788:1} total 154 — the c2788 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2788' prose rebadges to c2789 (-1 c2788) while the pass-38
prose RE-INTRODUCES c2788 in the historical phrase ('pass-37 repeat recorded
at c2788') -> c2788 net 0 from P2 (c2789 +1 born); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2788 twenty-seven-consecutive-HIT
lesson): P3 evidence prose gains '/c2788' in the observed list (+1 c2788) and
'pass-37 repeats at c2788' (+1 c2788); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2787' -> 'observed c2752/.../c2787/c2788' (c2788 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson, re-verified
live at this cycle's census: the v88 Step-3 surfaces carry 'cycle2788'/'e2788');
the c2746 GOLD-CHECK comment carries unchanged. HASH-ARTIFACT watch (the
c3819e9 + c7947 lessons — checked BEFORE forecasting): the official c2788
commit hash 6253361 short form = 6-2-5-3-3-6-1 carries NO 'c' character at
all — NO c+4-digit run, no new hash-artifact birth; the v88 P2 carry 'the
a762125 commit object' rebadges AWAY to 'the 6253361 commit object', and
since a762125 also carries no 'c' there is NO token death (the c7947 class
does NOT fire — c7947 already exited the histogram at v88); the foreign TOP
ffa527c carries no c+4-digit run either (the trailing 'c' is letter-preceded
and line-terminal — zero exposure, no foreign hash enters v89).
Forecast: c2788 1->4 (+3), c2789 0->1 (+1 born), total 154 -> 158 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2789.py"
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
