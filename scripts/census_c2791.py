#!/usr/bin/env python3
"""Pre-guard census for cycle 2791 — MEASURED, never predicted.

Per-line census first (the c2752..c2790 per-line-census-first lessons): the
c2791/c2792 token-guard lives INSIDE the c2790 Next-block (line 9220), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2791.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2790 instrument-set presence, the
entry-cycle2790 template integrity (block == worklog lines 9209-9220), the
v90 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 300 / stamp-gap 600 /
token-gap 540 / token-vs-stamp +529 / +289).
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

for cyc in ("c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2791={len([l for l in lines if l.startswith('Task ID: 446189-c2791')])}")
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
C2790_SET = [
    "census_c2790.py", "arrival_guard_c2790.py", "rebadge_cycle2790.py",
    "capture_cycle2790.sh", "measure_c2790_tokens.py", "recursive_diff_2790.py",
    "validate_cycle2790.py", "entry_cycle2790.txt", "append_cycle2790.py",
    "scan_cycle2790_raw.json", "scan_cycle2790.json",
]
print("c2790_instrument_set_object_presence:")
for name in C2790_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2790.txt == worklog lines 9209-9220
entry = open("/home/z/my-project/scripts/entry_cycle2790.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9208:9220]) + "\n"
print(f"entry_cycle2790_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v90 source size + lag-1 carries (the rebadge old-string expectations)
v90 = open("/home/z/my-project/scripts/validate_cycle2790.py", "rb").read()
print(f"v90_bytes={len(v90)} pass38_band={'pass-38 band'.encode() in v90} "
      f"pass38_evidence={'pass-38 evidence'.encode() in v90} "
      f"pass39_band={'pass-39 band'.encode() in v90} "
      f"pass39_evidence={'pass-39 evidence'.encode() in v90} "
      f"cycle2790={'CYCLE = 2790'.encode() in v90} "
      f"gate_pass39={'drift49_pass39_match'.encode() in v90} "
      f"gate_pass40={'drift49_pass40_match'.encode() in v90}")

# cadence-print prior-occurrence counts (honest series accounting)
print(f"stamp600_priors={text.count('600.000s by stamp')}")
print(f"stamp300_priors={text.count('300.000s by stamp')}")
print(f"token540_priors={text.count('540s by token')}")
print(f"token290_priors={text.count('290s by token')}")
i = 0
n = 0
while True:
    j = text.find("+529", i)
    if j < 0:
        break
    if not text.startswith("+529.", j):
        n += 1
    i = j + 1
print(f"plus529_priors={n}")
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
