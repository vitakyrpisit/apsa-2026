#!/usr/bin/env python3
"""P-HIST instrument for cycle 2748 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2748.py
(the v47->v48 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v47 measured series
({c2736:1, c2738:2, c2739:1, c2746:3} total 7) under the patch deltas —
measured on real bytes, never forecast.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2748.py"
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
