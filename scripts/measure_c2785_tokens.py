#!/usr/bin/env python3
"""P-HIST instrument for cycle 2785 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2785.py
(the v84->v85 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v84 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:4, c2781:4, c2782:4, c2783:4, c2784:1} total 138 — the c2784 Next-block compare
base) under the patch deltas — measured on real bytes, never forecast. Patch
delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2784' prose rebadges to c2785 (-1 c2784) while the pass-34
prose RE-INTRODUCES c2784 in the historical phrase ('pass-33 repeat recorded
at c2784') -> c2784 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2784 twenty-three-consecutive-HIT lesson): P3
evidence prose gains '/c2784' in the observed list (+1 c2784) and 'pass-33
repeats at c2784' (+1 c2784); P8 the SIZE_BAND comment rebadges 'observed
c2752/.../c2783' -> 'observed c2752/.../c2783/c2784' (c2784 +1); P5/P6/P7 the
CYCLE constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2784 commit hash 9b1c925 short form = 9-b-1-c-9-2-5
— its single 'c' sits as 'c925' (c+3-digits, short-hash-terminated — NO
c+4-digit run possible); the FULL hash 9b1c925b7dbe237a3852af7f1ae9004641d4f849
carries its single 'c' as 'c925b' (c+3-digits then a letter, NO c+4-digit run)
— exposure NIL because only the SHORT hash enters the v85 P2 paragraph (the
P2 paragraph carries the official 9b1c925 short hash only); the foreign
128bbec short form carries its 'c' as the TERMINAL character (zero digits
after — zero exposure) and the foreign commit touches no instrument source;
the c2785 commit hash is unborn at forecast time, checked post-commit.
Forecast: c2784 1->4 (+3), c2785 0->1 (+1 born), total 138 -> 142 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2785.py"
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
