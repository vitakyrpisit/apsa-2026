#!/usr/bin/env python3
"""Cross-loss continuity diff for LOSS EVENT #79 (span 67 — loss-substituted baseline).

Compares scan_cycle2735_raw.json (the rebuilt pre-loss c2735 capture, byte-faithful)
against scan_cycle2668.json (the last DISK-RECOVERABLE archive, c2668-era). The
c2669..c2734 archives are LOST (LOSS-#79 span) — this span-67 diff is loss-substituted
from the suspended span-1 streak, per the LOSS-#5 recon precedent (entry_recon_loss5.txt:
"recursive_diff vs scan_cycle2453.json (span 115, loss-substituted)").
Volatile fields (scanned_at, scan_duration_ms) stripped; sorted-keys normalization;
recursive path-level reporting. rc=0 iff market composition identical.
"""
import json
import sys

A_PATH = "/home/z/my-project/scripts/scan_cycle2735_raw.json"
B_PATH = "/home/z/my-project/scripts/scan_cycle2668.json"
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
print(f"normalized_bytes: c2735={len(json.dumps(na, sort_keys=True))} "
      f"c2668={len(json.dumps(nb, sort_keys=True))}")
diffs = diff_paths(na, nb)
if not diffs:
    print("MARKET_UNCHANGED (span 67, loss-substituted baseline c2668)")
    sys.exit(0)

print(f"DIFF_COUNT={len(diffs)} (c2668 -> c2735, span 67)")
for kind, path, detail in diffs:
    print(f"  {kind}: {path} = {detail}")
sys.exit(1)
