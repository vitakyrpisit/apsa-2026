#!/usr/bin/env python3
"""P-HIST instrument for cycle 2751 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2751.py
(the v50->v51 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v50 measured series
({c2738:1, c2739:1, c2746:1, c2747:3, c2748:3, c2749:2, c2750:2, c3579:1(hash
artifact)} total 14 — the c2750 Next-block compare base) under the patch
deltas — measured on real bytes, never forecast. Patch delta forecast (for
accounting only, the MEASUREMENT governs): bfc3579 -> 113dbc1 retires the
c3579 hash artifact (-1); c2751 docstring/path tokens born (+2); the
113dbc1 hash produces no c-token artifact.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2751.py"
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
