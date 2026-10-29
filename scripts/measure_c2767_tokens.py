#!/usr/bin/env python3
"""P-HIST instrument for cycle 2767 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2767.py
(the v66->v67 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v66 measured series
({c2746:1, c2747:2, c2748:2, c2749:1, c2750:1, c2751:1, c2752:5, c2753:4,
c2754:4, c2755:4, c2756:4, c2757:4, c2758:4, c2759:4, c2760:4, c2761:4,
c2762:4, c2763:4, c2764:4, c2765:4, c2766:1} total 66 — the c2766 Next-block
compare base) under the patch deltas — measured on real bytes, never forecast.
Patch delta forecast (for accounting only, the MEASUREMENT governs): the P2
'Baseline for c2766' prose rebadges to c2767 (-1 c2766) while the pass-16
prose RE-INTRODUCES c2766 in the historical phrase ('pass-15 repeat recorded
at c2766') -> c2766 net 0 from P2; the observed lists are APPEND-class (the
c2761 forecast-miss / c2762..c2766 five-consecutive-HIT lesson): P3 evidence
prose gains '/c2766' in the observed list (+1 c2766) and 'pass-15 repeats at
c2766' (+1 c2766); P8 the SIZE_BAND comment rebadges 'observed c2752/.../
c2765' -> 'observed c2752/.../c2765/c2766' (c2766 +1); P5/P6/P7 the CYCLE
constant and RAW/PRETTY paths rebadge (path tokens are 'e'-before-digits,
NOT c-tokens — zero delta per the c2760 lesson); the c2746 GOLD-CHECK comment
carries unchanged. Hash-artifact watch (the c3819e9 lesson — checked BEFORE
forecasting): the fresh c2766 commit hash bc701a6 = b-c-7-0-1-a-6, the only
'c' run is 'c701' = c+3 digits (the c-token regex needs c+4 digits) — no
artifact; the foreign 19ff74c = 1-9-f-f-7-4-c, no 'c'+digits run — no
artifact; the c2767 commit hash is unborn at forecast time, checked
post-commit.
Forecast: c2766 1->4 (+3), c2767 0->1 (+1 born), total 66 -> 70 (+4). The
MEASUREMENT governs over this forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2767.py"
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
