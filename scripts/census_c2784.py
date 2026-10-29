#!/usr/bin/env python3
"""Pre-guard census for cycle 2784 — MEASURED, never predicted.

Per-line census first (the c2752..c2783 per-line-census-first lessons): the
c2784/c2785 token-guard lives INSIDE the c2783 Next-block (line 9136), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2784.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2783 instrument-set presence, the
entry-cycle2783 template integrity (block == worklog lines 9125-9136), and the
v83 source lag-1 carries (the rebadge old-string expectations).
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

for cyc in ("c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2784={len([l for l in lines if l.startswith('Task ID: 446189-c2784')])}")
last = [l for l in lines if l.strip()][-1]
print(f"tail_head={last[:44]!r}")

import os
print(f"basedagents_present={os.path.isdir('/home/z/my-project/.basedagents')}")
if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, errors="replace").read()
    print(f"dev_log_post_scan_entries={dl.count('POST /api/marketplaces/scan')}")
else:
    print("dev_log: ABSENT")

# instrument-set presence (the LOSS-#83 lesson: verify FIRST)
C2783_SET = [
    "census_c2783.py", "arrival_guard_c2783.py", "rebadge_cycle2783.py",
    "capture_cycle2783.sh", "measure_c2783_tokens.py", "recursive_diff_2783.py",
    "validate_cycle2783.py", "entry_cycle2783.txt", "append_cycle2783.py",
    "scan_cycle2783_raw.json", "scan_cycle2783.json",
]
print("c2783_instrument_set_object_presence:")
for name in C2783_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2783.txt == worklog lines 9125-9136
entry = open("/home/z/my-project/scripts/entry_cycle2783.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9124:9136]) + "\n"
print(f"entry_cycle2783_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v83 source size + lag-1 carries (the rebadge old-string expectations)
v83 = open("/home/z/my-project/scripts/validate_cycle2783.py", "rb").read()
print(f"v83_bytes={len(v83)} pass31_band={'pass-31 band'.encode() in v83} "
      f"pass31_evidence={'pass-31 evidence'.encode() in v83} "
      f"pass32_band={'pass-32 band'.encode() in v83} "
      f"pass32_evidence={'pass-32 evidence'.encode() in v83}")
