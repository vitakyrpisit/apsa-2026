#!/usr/bin/env python3
"""Span-1 diff for cycle 2751 — the consecutive-archive streak continues.

Compares scan_cycle2751_raw.json (the fresh official capture) against
scan_cycle2750.json (the immediately-preceding archive, on disk and
commit-verified). Span-1 for the fourth consecutive cycle since LOSS-#83
(the c2748 rdiff was the streak-resuming span-1). Volatile fields
(scanned_at, scan_duration_ms) stripped; sorted-keys normalization;
recursive path-level reporting. rc=0 iff market composition identical
(MARKET_UNCHANGED). Expected: MARKET_UNCHANGED on the DRIFT-#48
verification-3 path (baseline CARRY UNCHANGED), else the movement
evidence prints (DRIFT-#49 pass-1 opens).
"""
import json
import sys

A_PATH = "/home/z/my-project/scripts/scan_cycle2751_raw.json"
B_PATH = "/home/z/my-project/scripts/scan_cycle2750.json"
VOLATILE = {"scanned_at", "scan_duration_ms"}


def strip_volatile(node):
    if isinstance(node, dict):
        return {k: strip_volatile(v) for k, v in sorted(node.items()) if k not in VOLATILE}
    if isinstance(node, list):
        return [strip_volatile(v) for v in node]
    return node


def diff_paths(a, b, prefix=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            p = f"{prefix}.{k}" if prefix else k
            if k not in a:
                out.append(("ADDED", p, b[k]))
            elif k not in b:
                out.append(("REMOVED", p, a[k]))
            else:
                out.extend(diff_paths(a[k], b[k], p))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(("LEN", prefix, f"{len(a)} vs {len(b)}"))
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(diff_paths(x, y, f"{prefix}[{i}]"))
    else:
        if a != b:
            out.append(("CHANGED", prefix, f"{a!r} -> {b!r}"))
    return out


with open(A_PATH, "rb") as f:
    a_raw = f.read()
a = json.loads(a_raw)
with open(B_PATH, "rb") as f:
    b = json.loads(f.read())

na, nb = strip_volatile(a), strip_volatile(b)
print(f"normalized_bytes: c2751={len(json.dumps(na, sort_keys=True))} "
      f"c2750={len(json.dumps(nb, sort_keys=True))}")
diffs = diff_paths(na, nb)
if not diffs:
    print("MARKET_UNCHANGED (span 1, baseline c2750 — consecutive-archive streak continues)")
    sys.exit(0)

print(f"DIFF_COUNT={len(diffs)} (c2750 -> c2751, span 1)")
for kind, path, detail in diffs:
    print(f"  {kind}: {path} = {detail}")
sys.exit(1)
