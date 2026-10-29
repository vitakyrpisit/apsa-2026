#!/usr/bin/env python3
"""P-HIST instrument for cycle 2796 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2796.py
(the v95->v96 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v95 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:4, c2784:4, c2785:4,
c2786:4, c2787:4, c2788:4, c2789:4, c2790:4, c2791:4, c2792:4, c2793:4,
c2794:4, c2795:1}
total 182 — the c2795 Next-block compare base) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for accounting
only, the MEASUREMENT governs): the P2 'Baseline for c2795' prose rebadges to
c2796 (-1 c2795, +1 c2796 born) while the P2 pass-chain prose RE-INTRODUCES
c2795 in the historical phrase ('pass-44 repeat recorded at c2795' — +1
c2795, c2795 net 0 from the chain rewrite); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2795 thirty-four-consecutive-
HIT lesson): P3 evidence prose gains '/c2795' in the observed list (+1 c2795)
and 'pass-44 repeats at c2795' (+1 c2795); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2794' -> 'observed c2752/.../c2794/c2795' (c2795 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson,
re-verified live at this cycle's census: the v95 Step-4 surfaces carry
'cycle2795'/'e2795'); the c2746 GOLD-CHECK comment carries unchanged.
HASH-ARTIFACT watch (the c3819e9 + c7947 lessons — checked BEFORE
forecasting): the official c2795 commit hash 0d844fa short form =
0-d-8-4-4-f-a carries NO 'c' character at all — NO c+4-digit run, no new
hash-artifact birth; the v95 P2 carry 'the fb1d1d1 commit object' rebadges
AWAY to 'the 0d844fa commit object', and since fb1d1d1 carries NO 'c'
character at all there is NO token death (the c7947 class does NOT fire —
c7947 already exited the histogram at v88); the foreign TOP 615fc1c short
form = 6-1-5-f-c-1-c carries its 'c' characters WITHOUT a following 4-digit
run ('c1' = single digit after the position-5 'c'; the final 'c' has NO
following digits) — zero c+4-digit run, zero exposure for the validator
surface.
Forecast: c2795 1->4 (+3), c2796 0->1 (+1 born), total 182 -> 186 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2796.py"
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
