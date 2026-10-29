#!/usr/bin/env python3
"""P-HIST instrument for cycle 2753 — MEASURE, never predict.

Counts cycle tokens (cNNNN) in the ACTUAL bytes of validate_cycle2753.py
(the v52->v53 rebadge output). The rebadge is a real sed-carry this cycle,
so the measured histogram continues the v52 measured series
({c2738:1, c2739:1, c2746:1, c2747:3, c2748:3, c2749:2, c2750:2, c2751:2,
c2752:2} total 17 — the c2752 Next-block compare base) under the patch
deltas — measured on real bytes, never forecast. Patch delta forecast (for
accounting only, the MEASUREMENT governs): c2752 docstring tokens partially
rebadged (P2 'Baseline for c2752' -> c2753) while the pass-2 prose RE-INTRODUCES
the verification series c2749/c2750/c2751/c2752 (+1 each) and the c2752
observation mentions (P2 'opened at c2752', P3 'observed at c2752' + series);
c2753 tokens born (P2 'Baseline for c2753'); the 2dae73c hash produces no
c-token artifact (trailing-c, no digits after; the 2708896 digits-leading
precedent class). The b6a94e3 HEAD hash is NOT referenced.
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2753.py"
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
