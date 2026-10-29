#!/usr/bin/env python3
"""P-HIST instrument for cycle 2747 — MEASURE, never predict.

Counts cycle tokens (cNNNN, 4+ digits after 'c') in the ACTUAL bytes of
validate_cycle2747.py. The context-carried c2747 pre-patch prophecy series
({2747:0, 2746:5, 2745:2, ...}) is VOID — the v46 source it described was wiped
by LOSS EVENT #83 before any measurement could land. This instrument measures
the actual rebuilt validator distribution; the entry records the measured
histogram verbatim with the VOID note (SELF-REFERENTIAL-TOKEN LESSON: measure
on real bytes, never forecast the histogram).
"""
import re
import sys
from collections import Counter

SRC = "/home/z/my-project/scripts/validate_cycle2747.py"
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
