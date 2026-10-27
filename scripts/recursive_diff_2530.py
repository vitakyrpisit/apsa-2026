#!/usr/bin/env python3
"""recursive_diff for cycle 2530 vs cycle 2529 (span 1).

Normalization (canonical, DRIFT-#30 lineage):
  - parse raw scan body
  - pop scan_duration_ms (volatile)
  - mask scanned_at value to fixed 21-char token (volatile, width-stable)
  - re-serialize compact with sort_keys=True
Both sides normalized identically -> byte counts + equality.
"""
import json
import sys

CUR = "/home/z/my-project/scripts/scan_cycle2530_raw.json"
PREV = "/home/z/my-project/scripts/scan_cycle2529_raw.json"
MASK = "X" * 21  # canonical mask width: 446 raw - 24B duration field - 3B vs 24ch = 419B canon


def normalize(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scan_duration_ms", None)
    if "scanned_at" in d:
        d["scanned_at"] = MASK
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


cur = normalize(CUR)
prev = normalize(PREV)
print(f"normalized_cur={len(cur)}B normalized_prev={len(prev)}B")
same = cur == prev
print("recursive_diff_result=" + ("MARKET_UNCHANGED (byte-identical)" if same else "MARKET_CHANGED"))
if not same:
    for i, (a, b) in enumerate(zip(cur, prev)):
        if a != b:
            print(f"first_diff_at_byte={i} cur={cur[i:i+40]!r} prev={prev[i:i+40]!r}")
            break
    print("len_delta=", len(cur) - len(prev))
    sys.exit(1)
print(f"streak_span=1 (c2529-to-c2530)")
print(f"normalized {len(cur)}-vs-{len(prev)} byte-identical, rc=0")
