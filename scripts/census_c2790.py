#!/usr/bin/env python3
"""Pre-guard census for cycle 2790 — MEASURED, never predicted.

Per-line census first (the c2752..c2789 per-line-census-first lessons): the
c2790/c2791 token-guard lives INSIDE the c2789 Next-block (line 9208), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2790.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2789 instrument-set presence, the
entry-cycle2789 template integrity (block == worklog lines 9197-9208), the
v89 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 600 / token-gap 540 / +289).
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

for cyc in ("c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2790={len([l for l in lines if l.startswith('Task ID: 446189-c2790')])}")
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
C2789_SET = [
    "census_c2789.py", "arrival_guard_c2789.py", "rebadge_cycle2789.py",
    "capture_cycle2789.sh", "measure_c2789_tokens.py", "recursive_diff_2789.py",
    "validate_cycle2789.py", "entry_cycle2789.txt", "append_cycle2789.py",
    "scan_cycle2789_raw.json", "scan_cycle2789.json",
]
print("c2789_instrument_set_object_presence:")
for name in C2789_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2789.txt == worklog lines 9197-9208
entry = open("/home/z/my-project/scripts/entry_cycle2789.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9196:9208]) + "\n"
print(f"entry_cycle2789_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v89 source size + lag-1 carries (the rebadge old-string expectations)
v89 = open("/home/z/my-project/scripts/validate_cycle2789.py", "rb").read()
print(f"v89_bytes={len(v89)} pass37_band={'pass-37 band'.encode() in v89} "
      f"pass37_evidence={'pass-37 evidence'.encode() in v89} "
      f"pass38_band={'pass-38 band'.encode() in v89} "
      f"pass38_evidence={'pass-38 evidence'.encode() in v89} "
      f"cycle2789={'CYCLE = 2789'.encode() in v89} "
      f"gate_pass38={'drift49_pass38_match'.encode() in v89} "
      f"gate_pass39={'drift49_pass39_match'.encode() in v89}")

# cadence-print prior-occurrence counts (honest series accounting)
print(f"stamp600_priors={text.count('600.000s by stamp')}")
print(f"token540_priors={text.count('540s by token')}")
i = 0
n = 0
while True:
    j = text.find("+289", i)
    if j < 0:
        break
    if not text.startswith("+289.", j):
        n += 1
    i = j + 1
print(f"plus289_priors={n}")
