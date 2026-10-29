#!/usr/bin/env python3
"""P-HIST instrument for cycle 2749 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2749.py
(the v48->v49 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v48 measured series
({c2736:1, c2738:4, c2739:3, c2746:3, c2747:2, c2748:1} total 14) under the
patch deltas — measured on real bytes, never forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2749.py"
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
