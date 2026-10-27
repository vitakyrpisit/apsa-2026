#!/usr/bin/env python3
"""Dump FULL details of the 5 honest paid tasks from c1506 (gold evaluation).

Prints every field of each task, esp. escrow/reward/deadline fields for scam check.
NEVER prints private keys - task data only.
"""
import json

RAW = "/home/z/my-project/scripts/scan_cycle1506_raw.json"
d = json.load(open(RAW))
tasks = d["basedagents"]["all_honest_paid"]

print(f"n_tasks={len(tasks)}")
for i, t in enumerate(tasks):
    print(f"\n===== TASK [{i}] ALL FIELDS =====")
    print(f"keys={sorted(t.keys())}")
    for k, v in t.items():
        s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
        if k == "description":
            print(f"{k}: (len={len(v)})")
            print(v)
        else:
            print(f"{k}: {s}")

# Escrow / reward related fields across all tasks
print("\n===== ESCROW/REWARD FIELD SURVEY =====")
allkeys = set()
for t in tasks:
    allkeys.update(t.keys())
escrow_like = [k for k in sorted(allkeys) if any(w in k.lower() for w in ["escrow", "reward", "bounty", "amount", "price", "usdc", "bond", "deadline", "window", "expires", "status"])]
print(f"escrow_like_keys={escrow_like}")
for t in tasks:
    row = {k: t.get(k) for k in escrow_like}
    print(f"{t.get('task_id')}: {json.dumps(row)}")
