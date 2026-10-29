#!/usr/bin/env python3
"""Pre-guard census for cycle 2777 — MEASURED, never predicted.

Per-line census first (the c2752..c2776 per-line-census-first lessons): the
c2777/c2778 token-guard lives INSIDE the c2776 Next-block (line 9052), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2777.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe.
"""
WL = "/home/z/my-project/worklog.md"
DEVLOG = "/home/z/my-project/dev.log"

text = open(WL, encoding="utf-8").read()
lines = text.splitlines()
print(f"worklog_lines={len(lines)} newline_count={text.count(chr(10))}")

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
print(f"anchor_TaskID={tid} anchor_nogold={gold}")
print(f"LOSS-#6_occ={text.count('LOSS-#6')} LOSS-#15_occ={text.count('LOSS-#15')}")

for cyc in ("c2778", "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771",
            "c2770", "c2769", "c2768"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2777={len([l for l in lines if l.startswith('Task ID: 446189-c2777')])}")
last = [l for l in lines if l.strip()][-1]
print(f"tail_head={last[:44]!r}")

import os
print(f"basedagents_present={os.path.isdir('/home/z/my-project/.basedagents')}")
if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, errors="replace").read()
    print(f"dev_log_post_scan_entries={dl.count('POST /api/marketplaces/scan')}")
else:
    print("dev_log: ABSENT")
