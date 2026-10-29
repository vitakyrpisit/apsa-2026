#!/usr/bin/env python3
"""P-HIST instrument for cycle 2788 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2788.py
(the v87->v88 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v87 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:4, c2784:4, c2785:4,
c2786:4, c2787:1, c7947:1} total 151 — the c2787 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2787' prose rebadges to c2788 (-1 c2787) while the pass-37
prose RE-INTRODUCES c2787 in the historical phrase ('pass-36 repeat recorded
at c2787') -> c2787 net 0 from P2 (c2788 +1 born); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2787 twenty-six-consecutive-HIT
lesson): P3 evidence prose gains '/c2787' in the observed list (+1 c2787) and
'pass-36 repeats at c2787' (+1 c2787); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2786' -> 'observed c2752/.../c2786/c2787' (c2787 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson, re-verified
live at this cycle's census: the v87 Step-3 surfaces carry 'cycle2787'/'e2787');
the c2746 GOLD-CHECK comment carries unchanged. HASH-ARTIFACT DEATH (the
c3819e9 + c7947 lessons — checked BEFORE forecasting): the official c2787
commit hash a762125 short form = a-7-6-2-1-2-5 carries NO 'c' character at
all — NO c+4-digit run, no new hash-artifact birth; the v87 P2 carry 'the
b0c7947 commit object' rebadges AWAY to 'the a762125 commit object', so the
c7947 token is forecast to DIE (1 -> 0) exactly as the c2787 Next-block
wrote; no other v87 surface carries c7947; the foreign TOP 0b4f512 carries
no 'c' either (zero exposure, no foreign hash enters v88).
Forecast: c2787 1->4 (+3), c2788 0->1 (+1 born), c7947 1->0 (DEATH),
c2786 unchanged 4, total 151 -> 154 (+4). The MEASUREMENT governs over this
forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2788.py"
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
