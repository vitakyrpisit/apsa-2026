#!/usr/bin/env python3
"""Pre-guard census for cycle 2794 — MEASURED, never predicted.

Per-line census first (the c2752..c2793 per-line-census-first lessons): the
c2794/c2795 token-guard lives INSIDE the c2793 Next-block (line 9256), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2794.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2793 instrument-set presence, the
entry-cycle2793 template integrity (block == worklog lines 9245-9256), the
v93 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 290 / token-gap 480 /
token-vs-stamp +529 / the series tail prints).
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

for cyc in ("c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2794={len([l for l in lines if l.startswith('Task ID: 446189-c2794')])}")
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
C2793_SET = [
    "census_c2793.py", "arrival_guard_c2793.py", "rebadge_cycle2793.py",
    "capture_cycle2793.sh", "measure_c2793_tokens.py", "recursive_diff_2793.py",
    "validate_cycle2793.py", "entry_cycle2793.txt", "append_cycle2793.py",
    "scan_cycle2793_raw.json", "scan_cycle2793.json",
]
print("c2793_instrument_set_object_presence:")
for name in C2793_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2793.txt == worklog lines 9245-9256
entry = open("/home/z/my-project/scripts/entry_cycle2793.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9244:9256]) + "\n"
print(f"entry_cycle2793_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v93 source size + lag-1 carries (the rebadge old-string expectations)
v93 = open("/home/z/my-project/scripts/validate_cycle2793.py", "rb").read()
print(f"v93_bytes={len(v93)} pass41_band={'pass-41 band'.encode() in v93} "
      f"pass41_evidence={'pass-41 evidence'.encode() in v93} "
      f"pass42_band={'pass-42 band'.encode() in v93} "
      f"pass42_evidence={'pass-42 evidence'.encode() in v93} "
      f"cycle2793={'CYCLE = 2793'.encode() in v93} "
      f"gate_pass42={'drift49_pass42_match'.encode() in v93} "
      f"gate_pass43={'drift49_pass43_match'.encode() in v93}")

# cadence-print prior-occurrence counts (honest series accounting)
print(f"stamp290_priors={text.count('290.000s by stamp')}")
print(f"token480_priors={text.count('480s by token')}")
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
    j = text.find("+339", i)
    if j < 0:
        break
    if not text.startswith("+339.", j):
        n += 1
    i = j + 1
print(f"plus339_priors={n}")
