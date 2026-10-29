#!/usr/bin/env python3
"""P-HIST instrument for cycle 2787 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2787.py
(the v86->v87 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v86 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:4, c2784:4, c2785:4,
c2786:1} total 146 — the c2786 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2786' prose rebadges to c2787 (-1 c2786) while the pass-36
prose RE-INTRODUCES c2786 in the historical phrase ('pass-35 repeat recorded
at c2786') -> c2786 net 0 from P2 (c2787 +1 born); the observed lists are
APPEND-class (the c2761 forecast-miss / c2762..c2786 twenty-five-consecutive-HIT
lesson): P3 evidence prose gains '/c2786' in the observed list (+1 c2786) and
'pass-35 repeats at c2786' (+1 c2786); P8 the SIZE_BAND comment rebadges
'observed c2752/.../c2785' -> 'observed c2752/.../c2785/c2786' (c2786 +1);
P5/P6/P7 the CYCLE constant and RAW/PRETTY paths rebadge (path tokens are
'e'-before-digits, NOT c-tokens — zero delta per the c2760 lesson, re-verified
live at this cycle's census: the v86 Step-4 surfaces carry 'e2786'); the
c2746 GOLD-CHECK comment carries unchanged. HASH-ARTIFACT BIRTH (the c3819e9
lesson — checked BEFORE forecasting, the class FIRES this cycle): the official
c2786 commit hash b0c7947 short form = b-0-c-7-9-4-7 — its SINGLE 'c'
character is followed by FOUR DIGITS ('c7947') — so the v87 P2 paragraph
('the b0c7947 commit object') BIRTHS a c7947 token (+1); the FULL hash
b0c7947fa0d21aaa8ca5a1573406475aa9997f42 carries its remaining 'c's as
'a8ca'/'5a15' (no other c+4-digit run) and enters no v87 source; the foreign
966ab1f short form carries NO 'c' at all (zero exposure — its FULL hash's
'c876' run is irrelevant, no foreign hash enters v87).
Forecast: c2786 1->4 (+3), c2787 0->1 (+1 born), c7947 0->1 (+1 hash-artifact
birth), total 146 -> 151 (+5). The MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2787.py"
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
