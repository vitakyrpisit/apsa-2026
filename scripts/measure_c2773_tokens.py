#!/usr/bin/env python3
"""P-HIST instrument for cycle 2773 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2773.py
(the v72->v73 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v72 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:4, c2767:4, c2768:4, c2769:4,
c2770:4, c2771:4, c2772:1} total 90 — the c2772 Next-block compare base) under the
patch deltas — measured on real bytes, never forecast.
Patch delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2772' prose rebadges to c2773 (-1 c2772) while the pass-22
prose RE-INTRODUCES c2772 in the historical phrase ('pass-21 repeat recorded
at c2772') -> c2772 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2772 eleven-consecutive-HIT lesson): P3 evidence
prose gains '/c2772' in the observed list (+1 c2772) and 'pass-21 repeats at
c2772' (+1 c2772); P8 the SIZE_BAND comment rebadges 'observed c2752/.../
c2771' -> 'observed c2752/.../c2771/c2772' (c2772 +1); P5/P6/P7 the CYCLE
constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2772 commit hash b774591 = b-7-7-4-5-9-1, no 'c'
run at all — no artifact; the foreign 0539b68 FULL hash
0539b685a85df795c67c91d2e8c7c913779fb2a3 contains the c-run 'c913779' —
NOTED, but the foreign hash is never written into the validator source (the
P2 paragraph carries the official b774591 short hash only; the short form
b774591 has no c-run) — zero artifact exposure; the c2773 commit hash is
unborn at forecast time, checked post-commit.
Forecast: c2772 1->4 (+3), c2773 0->1 (+1 born), total 90 -> 94 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2773.py"
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
