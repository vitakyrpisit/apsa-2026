#!/usr/bin/env python3
"""Compare c1831 vs c1832 raw payloads to localize DRIFT-#19 changes."""
import json

old = json.load(open("/home/z/my-project/scripts/scan_cycle1831_raw.json"))
new = json.load(open("/home/z/my-project/scripts/scan_cycle1832_raw.json"))

def flat(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flat(v, key + "."))
        else:
            out[key] = v
    return out

fo, fn = flat(old), flat(new)
diffs = []
for k in sorted(set(fo) | set(fn)):
    a, b = fo.get(k, "<absent>"), fn.get(k, "<absent>")
    if a != b:
        diffs.append(f"  {k}: {a!r} -> {b!r}")
print(f"changed_fields={len(diffs)}")
print("\n".join(diffs) if diffs else "  (none)")
so, sn = json.dumps(old, sort_keys=True), json.dumps(new, sort_keys=True)
print(f"normalized_len_old={len(so)} normalized_len_new={len(sn)}")
print("MARKET_CHANGED" if so != sn else "MARKET_UNCHANGED")
