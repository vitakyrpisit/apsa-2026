#!/usr/bin/env python3
"""P-HIST instrument for cycle 2790 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2790.py
(the v89->v90 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v89 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:4, c2784:4, c2785:4,
c2786:4, c2787:4, c2788:4, c2789:1} total 158 — the c2789 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2789' prose rebadges to c2790 (-1 c2789) while the pass-39
prose RE-INTRODUCES c2789 in the historical phrase ('pass-38 repeat recorded
at c2789') -> c2789 net 0 from P2 (c2790 +1 born); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2789 twenty-eight-consecutive-HIT
lesson): P3 evidence prose gains '/c2789' in the observed list (+1 c2789) and
'pass-38 repeats at c2789' (+1 c2789); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2788' -> 'observed c2752/.../c2788/c2789' (c2789 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson, re-verified
live at this cycle's census: the v89 Step-3 surfaces carry 'cycle2789'/'e2789');
the c2746 GOLD-CHECK comment carries unchanged. HASH-ARTIFACT watch (the
c3819e9 + c7947 lessons — checked BEFORE forecasting): the official c2789
commit hash 2af9fd7 short form = 2-a-f-9-f-d-7 carries NO 'c' character at
all — NO c+4-digit run, no new hash-artifact birth; the v89 P2 carry 'the
6253361 commit object' rebadges AWAY to 'the 2af9fd7 commit object', and
since 6253361 also carries no 'c' there is NO token death (the c7947 class
does NOT fire — c7947 already exited the histogram at v88); the foreign TOP
c048029 short form = c-0-4-8-0-2-9 DOES start with 'c' followed by the digit
run 048029 (a c+4-digit run 'c0480' EXISTS) — but the foreign hash enters NO
instrument source (foreign commits touch no validator bytes; the only
appearance is the worklog Step-1 prose record — no validator P-HIST weight,
no census-tag collision), so the exposure class is NIL for the validator
surface.
Forecast: c2789 1->4 (+3), c2790 0->1 (+1 born), total 158 -> 162 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2790.py"
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
