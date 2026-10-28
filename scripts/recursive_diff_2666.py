#!/usr/bin/env python3
"""Recursive market diff for cycle 2666 (span 1 — post-LOSS-#6 carry class).

Compares scan_cycle2666_raw.json (fresh capture) against scan_cycle2665.json
(the verification-43 archive). Volatile fields (scanned_at, scan_duration_ms)
stripped; sorted-keys normalization; recursive path-level reporting.
rc=0 iff market composition identical.
"""
import json
import sys

A_PATH = "/home/z/my-project/scripts/scan_cycle2666_raw.json"
B_PATH = "/home/z/my-project/scripts/scan_cycle2665.json"
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
print(f"normalized_bytes: c2666={len(json.dumps(na, sort_keys=True))} "
      f"c2665={len(json.dumps(nb, sort_keys=True))}")
diffs = diff_paths(na, nb)
if not diffs:
    print("MARKET_UNCHANGED (span 1)")
    sys.exit(0)

print(f"DIFF_COUNT={len(diffs)} (c2665 -> c2666, span 1)")
for kind, path, detail in diffs:
    print(f"  {kind}: {path} = {detail}")
sys.exit(1)
