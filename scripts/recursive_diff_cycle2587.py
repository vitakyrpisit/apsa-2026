#!/usr/bin/env python3
"""Recursive diff scan_cycle2587.json vs scan_cycle2586.json (span 1).

Volatile-stripped (scanned_at, scan_duration_ms) canonical comparison, then a
field-level diff to isolate the market movement. Exit 0 either way — the
MARKET_CHANGED/MARKET_UNCHANGED verdict is informational (MARKET_UNCHANGED
extends the DRIFT-#38-root on-disk streak 4 -> 5; the c2586 side of the diff
is the genuine captured bytes from the previous cycle).
"""
import json

A = "/home/z/my-project/scripts/scan_cycle2586.json"
B = "/home/z/my-project/scripts/scan_cycle2587.json"
VOLATILE = {"scanned_at", "scan_duration_ms"}


def load(p):
    with open(p) as f:
        return json.load(f)


def strip_volatile(d):
    out = {}
    for k, v in d.items():
        if k in VOLATILE:
            continue
        out[k] = strip_volatile(v) if isinstance(v, dict) else v
    return out


a, b = load(A), load(B)
na, nb = strip_volatile(a), strip_volatile(b)
sa = json.dumps(na, sort_keys=True, separators=(",", ":"))
sb = json.dumps(nb, sort_keys=True, separators=(",", ":"))
print(f"normalized_bytes {len(sa)}-vs-{len(sb)}")
if sa == sb:
    print("VERDICT: MARKET_UNCHANGED (normalized byte-identical)")
else:
    print("VERDICT: MARKET_CHANGED (same-length different-bytes)" if len(sa) == len(sb)
          else "VERDICT: MARKET_CHANGED (different normalized length)")

ba_a, ba_b = a["basedagents"], b["basedagents"]
fields = ["total_tasks", "honest_paid", "honest_free", "scam_pattern", "unknown"]
moves = []
for f_ in fields:
    if ba_a.get(f_) != ba_b.get(f_):
        moves.append(f"basedagents.{f_}: {ba_a.get(f_)} -> {ba_b.get(f_)}")
for k in set(a) | set(b):
    if k in VOLATILE or k == "basedagents":
        continue
    if a.get(k) != b.get(k):
        moves.append(f"{k}: {a.get(k)!r} -> {b.get(k)!r}")
print("field-level moves:" if moves else "field-level moves: NONE")
for m in moves:
    print(f"  - {m}")
