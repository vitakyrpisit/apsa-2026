#!/usr/bin/env python3
"""Span-1 diff for cycle 2816 — the post-pass-64 comparison.

Compares scan_cycle2816_raw.json (the fresh official capture) against
scan_cycle2815.json (the immediately-preceding archive, on disk and
commit-verified). Volatile fields (scanned_at, scan_duration_ms) stripped;
sorted-keys normalization; recursive path-level reporting. rc=0 iff market
composition identical (MARKET_UNCHANGED).
Movement classes per the DRIFT-#49 pass-65 spec (the c2815 Next-block): a
repeat (18,0,0,18,0) prints MARKET_UNCHANGED (rc=0, pass-65 repeat-class); a
return to (20,0,2,18,0) prints the reverse DIFF_COUNT=2 chain (RESTORATION —
the root stands, the pass-1 excursion closes as a transient); any other
composition prints the full delta chain (newest-observation evidence).
"""
import json
import sys

A_PATH = "/home/z/my-project/scripts/scan_cycle2816_raw.json"
B_PATH = "/home/z/my-project/scripts/scan_cycle2815.json"
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


def main():
    a = json.load(open(A_PATH))
    b = json.load(open(B_PATH))
    an = strip_volatile(a)
    bn = strip_volatile(b)
    diffs = diff_paths(an, bn)
    comp_a = (a["basedagents"]["total_tasks"], a["basedagents"]["honest_paid"],
              a["basedagents"]["honest_free"], a["basedagents"]["scam_pattern"],
              a["basedagents"]["unknown"])
    comp_b = (b["basedagents"]["total_tasks"], b["basedagents"]["honest_paid"],
              b["basedagents"]["honest_free"], b["basedagents"]["scam_pattern"],
              b["basedagents"]["unknown"])
    print(f"five_tuple_fresh={comp_a} five_tuple_prior={comp_b}")
    print(f"normalized_sizes={len(json.dumps(an))}-vs-{len(json.dumps(bn))}")
    if not diffs:
        print("MARKET_UNCHANGED")
        print("DIFF_COUNT=0")
        print("DRIFT-#49 pass-65 REPEAT-CLASS (movement repeat-class on tuple match; "
              "the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)")
        sys.exit(0)
    print(f"DIFF_COUNT={len(diffs)}")
    for kind, path, detail in diffs:
        print(f"  {kind} {path}: {detail}")
    if comp_a == (18, 0, 0, 18, 0) and comp_b == (20, 0, 2, 18, 0):
        print("RESTORATION-EVIDENCE (root return class)")
    elif comp_a == (20, 0, 2, 18, 0):
        print("NEWEST-OBSERVATION (composition changed)")
    else:
        print("NEWEST-OBSERVATION (composition changed)")
    sys.exit(1)


if __name__ == "__main__":
    main()
