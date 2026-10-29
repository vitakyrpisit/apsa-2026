#!/usr/bin/env python3
"""P-HIST instrument for cycle 2752 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2752.py
(the v51->v52 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v51 measured series
({c2738:1, c2739:1, c2746:1, c2747:3, c2748:3, c2749:2, c2750:2, c2751:2}
total 15 — the c2751 Next-block compare base) under the patch deltas —
measured on real bytes, never forecast. Patch delta forecast (for
accounting only, the MEASUREMENT governs): c2751 docstring tokens rebadged
(-2 via P2 'Baseline for c2751' and P3 'verification-3 = c2751'), partially
offset by the P8 band-comment carry (+1 -> net -1); c2752 docstring/root
tokens born (+2 via P2/P3); the 2708896 hash produces no c-token artifact
(digits-leading, the 113dbc1 precedent).
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2752.py"
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
