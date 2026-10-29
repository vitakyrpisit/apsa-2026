#!/usr/bin/env python3
"""P-HIST instrument for cycle 2750 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2750.py
(the v49->v50 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v49 measured series
({c2738:1, c2739:1, c2746:1, c2747:3, c2748:3, c2749:2}; the c2749 Next-block
compare base excludes the c5190 hash artifact — note the Next-block's
'total 12' arithmetic includes that artifact, an honest carry discrepancy
recorded at measurement time) under the patch deltas — measured on real
bytes, never forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2750.py"
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
