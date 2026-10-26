#!/usr/bin/env python3
"""recursive_diff c2619: scan_cycle2619.json vs scan_cycle2618.json (span 1).

Volatile fields (scanned_at, scan_duration_ms) stripped; normalized (sorted-keys)
canonical JSON compared. rc=0 MARKET_UNCHANGED / rc=1 MARKET_CHANGED with the exact
field-level moves printed.

c2619 RESULT (DRIFT-#43 verification-2 candidate, on-disk): PENDING — filled at run
time. MARKET_UNCHANGED extends the DRIFT-#43-root on-disk streak 1 -> 2; any move
= DRIFT-#44 declaration (two-pass).
"""
import json
import sys

VOLATILE = {"scanned_at", "scan_duration_ms"}

def strip_norm(path):
    d = json.load(open(path))
    def walk(o):
        if isinstance(o, dict):
            return {k: walk(v) for k, v in sorted(o.items()) if k not in VOLATILE}
        if isinstance(o, list):
            return [walk(v) for v in o]
        return o
    return walk(d)

a = strip_norm("/home/z/my-project/scripts/scan_cycle2618.json")
b = strip_norm("/home/z/my-project/scripts/scan_cycle2619.json")
sa = json.dumps(a, sort_keys=True, separators=(",", ":"))
sb = json.dumps(b, sort_keys=True, separators=(",", ":"))
print(f"volatile-stripped normalized lengths: {len(sa)}-vs-{len(sb)}")

moves = []
def diff(x, y, path=""):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            diff(x.get(k), y.get(k), f"{path}.{k}" if path else k)
    elif x != y:
        moves.append((path, x, y))

diff(a, b)
if not moves:
    print("MARKET_UNCHANGED (zero field-level moves)")
    sys.exit(0)
print(f"MARKET_CHANGED rc=1 — {len(moves)} field-level move(s):")
for p, x, y in moves:
    print(f"  {p}: {x} -> {y}")
sys.exit(1)
