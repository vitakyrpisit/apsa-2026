#!/usr/bin/env python3
"""Recursive diff for scan cycle archives (rebuilt post-rollback-#7).

Prior era tool was erased by rollback event #7 (2026-10-20 ~11:07-11:31
outage). This reconstruction canonicalizes both scan archives
(compact JSON, sorted keys) and compares bytes.

Volatile fields (scanned_at, scan_duration_ms) are STRIPPED before
diffing — otherwise every cycle would false-positive MARKET_CHANGED
on timestamps (observed during reconstruction testing).

Post-rollback-#7 era normalization constant: 41116 bytes for the
(25,4,1,17,3) baseline archive (stripped, default separators,
sort_keys=True). The pre-rollback constant 41087 is UNRECOVERABLE
(original tool's exact canonicalization unknown; reconstruction
tested: no-strip sort_keys default-sep = 41184, compact-sep = 40435,
neither matches 41087). New era baseline is self-consistent going
forward; drift sensor = stripped-canonical byte equality + validator
composition match.

Usage: python3 recursive_diff.py <new_archive> <old_archive>
Prints MARKET_UNCHANGED (byte-identical after normalization) or
MARKET_CHANGED (same length, different bytes / length drift), exit 0
either way; exit 2 on IO/parse errors.
"""
import json
import sys


VOLATILE_KEYS = ("scanned_at", "scan_duration_ms")


def canonical(path):
    with open(path) as f:
        d = json.load(f)
    for k in VOLATILE_KEYS:
        d.pop(k, None)
    return json.dumps(d, sort_keys=True)


def main():
    new_path, old_path = sys.argv[1], sys.argv[2]
    try:
        new_norm = canonical(new_path)
        old_norm = canonical(old_path)
    except (OSError, ValueError) as e:
        print(f"DIFF_ERROR: {e}")
        sys.exit(2)
    print(f"normalized_len_old={len(old_norm)} normalized_len_new={len(new_norm)}")
    if new_norm == old_norm:
        print("MARKET_UNCHANGED (normalized byte-identical)")
    elif len(new_norm) == len(old_norm):
        print("MARKET_CHANGED (normalized same-length different-bytes)")
    else:
        print(f"MARKET_CHANGED (normalized {len(old_norm)} -> {len(new_norm)})")
    sys.exit(0)


if __name__ == "__main__":
    main()
