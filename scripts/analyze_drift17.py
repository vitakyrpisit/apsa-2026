#!/usr/bin/env python3
"""Drift-#17 analysis: diff raw scan payloads c1796 (old baseline) vs c1797 (drift).

Reads both raw archives, reports:
- top-level delta (composition fields, sizes)
- task-level ID set diff per category (honest_paid / honest_free / scam / unknown)
- details of any newly appeared tasks (title, creator, bounty, escrow, pattern flags)
"""
import json

OLD = "/home/z/my-project/scripts/scan_cycle1796_raw.json"
NEW = "/home/z/my-project/scripts/scan_cycle1797_raw.json"

with open(OLD, "rb") as f:
    old_raw = f.read()
with open(NEW, "rb") as f:
    new_raw = f.read()

old = json.loads(old_raw)
new = json.loads(new_raw)

print(f"old_raw_bytes={len(old_raw)} new_raw_bytes={len(new_raw)} delta={len(new_raw)-len(old_raw):+d}B")
print(f"old scanned_at={old.get('scanned_at')} new scanned_at={new.get('scanned_at')}")

ob = old.get("basedagents", {})
nb = new.get("basedagents", {})

comp_keys = ["total_tasks", "honest_paid", "honest_free", "scam_pattern", "unknown"]
print("\n-- composition delta --")
for k in comp_keys:
    o, n = ob.get(k), nb.get(k)
    mark = "  ==" if o == n else "  !!"
    print(f"{mark} {k}: {o} -> {n}")

# Discover per-task list keys present in basedagents payload
print("\n-- basedagents keys --")
print("old:", sorted(ob.keys()))
print("new:", sorted(nb.keys()))

# Try to locate the full task list
list_key = None
for k in ("all_tasks", "tasks", "task_list", "marketplace_tasks"):
    if isinstance(nb.get(k), list):
        list_key = k
        break
print(f"\nlist_key={list_key}")

def task_index(payload_ba):
    """Map task_id -> task dict for the full task list if found."""
    idx = {}
    if list_key:
        for t in payload_ba.get(list_key) or []:
            if isinstance(t, dict) and t.get("task_id"):
                idx[t["task_id"]] = t
    return idx

old_idx = task_index(ob)
new_idx = task_index(nb)

if old_idx or new_idx:
    added = sorted(set(new_idx) - set(old_idx))
    removed = sorted(set(old_idx) - set(new_idx))
    print(f"\n-- task id set diff (list_key={list_key}) --")
    print(f"added ({len(added)}): {added}")
    print(f"removed ({len(removed)}): {removed}")
    for tid in added:
        t = new_idx[tid]
        print(f"\nADDED {tid}:")
        for field in ("title", "creator", "created_by", "bounty", "escrow", "status",
                      "classification", "category", "scam_reason", "risk_flags",
                      "scam_pattern", "description", "pilot"):
            if field in t:
                v = t[field]
                if isinstance(v, str) and len(v) > 300:
                    v = v[:300] + "...<trunc>"
                print(f"  {field}={json.dumps(v, ensure_ascii=False)}")
else:
    # Fall back: classification fields may be per-task inside all_honest_paid only;
    # scam tasks may be itemized elsewhere. Print raw key structure for manual follow-up.
    print("\nNo full task list key found; dumping per-key types for both payloads:")
    for name, ba in (("old", ob), ("new", nb)):
        for k, v in sorted(ba.items()):
            kind = type(v).__name__
            ln = len(v) if isinstance(v, (list, dict)) else ""
            print(f"  {name}.{k}: {kind} {ln}")

# honest_paid stability check
ohp = [t.get("task_id") for t in (ob.get("all_honest_paid") or [])]
nhp = [t.get("task_id") for t in (nb.get("all_honest_paid") or [])]
print(f"\n-- honest_paid ids --")
print(f"old: {ohp}")
print(f"new: {nhp}")
print(f"honest_paid unchanged: {sorted(ohp) == sorted(nhp)}")

# Whole-payload key delta (top level)
print("\n-- top-level keys delta --")
print("only_old:", sorted(set(old) - set(new)))
print("only_new:", sorted(set(new) - set(old)))
