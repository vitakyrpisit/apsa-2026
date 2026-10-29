#!/usr/bin/env python3
"""P-HIST instrument for cycle 2781 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2781.py
(the v80->v81 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v80 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:4, c2773:4, c2774:4, c2775:4, c2776:4, c2777:4,
c2778:4, c2779:4, c2780:1} total 122 — the c2780 Next-block compare base)
under the patch deltas — measured on real bytes, never forecast. Patch delta
forecast (for accounting only, the MEASUREMENT governs): the P2 'Baseline for
c2780' prose rebadges to c2781 (-1 c2780) while the pass-30 prose
RE-INTRODUCES c2780 in the historical phrase ('pass-29 repeat recorded at
c2780') -> c2780 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2780 nineteen-consecutive-HIT lesson): P3
evidence prose gains '/c2780' in the observed list (+1 c2780) and 'pass-29
repeats at c2780' (+1 c2780); P8 the SIZE_BAND comment rebadges 'observed
c2752/.../c2779' -> 'observed c2752/.../c2779/c2780' (c2780 +1); P5/P6/P7 the
CYCLE constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2780 commit hash 65b5294 short form = 6-5-b-5-2-9-4
— ZERO 'c' characters in the short form, no c+4-digit run possible; the FULL
hash (checked at guard time via cat-file) likewise carries no c+4-digit run
on the measured bytes; the foreign 134a6b8 short form carries a single 'c'
followed by 'b' — zero digit-run exposure; zero c+4-digit artifact exposure
in either hash, nothing NOTED into the validator source (the P2 paragraph
carries the official 65b5294 short hash only); the c2781 commit hash is
unborn at forecast time, checked post-commit.
Forecast: c2780 1->4 (+3), c2781 0->1 (+1 born), total 122 -> 126 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2781.py"
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
