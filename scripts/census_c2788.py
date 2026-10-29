#!/usr/bin/env python3
"""Pre-guard census for cycle 2788 — MEASURED, never predicted.

Per-line census first (the c2752..c2787 per-line-census-first lessons): the
c2788/c2789 token-guard lives INSIDE the c2787 Next-block (line 9184), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2788.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2787 instrument-set presence, the
entry-cycle2787 template integrity (block == worklog lines 9173-9184), the
v87 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 301 / token-gap 480 / +469).
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

for cyc in ("c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2788={len([l for l in lines if l.startswith('Task ID: 446189-c2788')])}")
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
C2787_SET = [
    "census_c2787.py", "arrival_guard_c2787.py", "rebadge_cycle2787.py",
    "capture_cycle2787.sh", "measure_c2787_tokens.py", "recursive_diff_2787.py",
    "validate_cycle2787.py", "entry_cycle2787.txt", "append_cycle2787.py",
    "scan_cycle2787_raw.json", "scan_cycle2787.json",
]
print("c2787_instrument_set_object_presence:")
for name in C2787_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2787.txt == worklog lines 9173-9184
entry = open("/home/z/my-project/scripts/entry_cycle2787.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9172:9184]) + "\n"
print(f"entry_cycle2787_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v87 source size + lag-1 carries (the rebadge old-string expectations)
v87 = open("/home/z/my-project/scripts/validate_cycle2787.py", "rb").read()
print(f"v87_bytes={len(v87)} pass35_band={'pass-35 band'.encode() in v87} "
      f"pass35_evidence={'pass-35 evidence'.encode() in v87} "
      f"pass36_band={'pass-36 band'.encode() in v87} "
      f"pass36_evidence={'pass-36 evidence'.encode() in v87} "
      f"cycle2787={'CYCLE = 2787'.encode() in v87} "
      f"gate_pass36={'drift49_pass36_match'.encode() in v87} "
      f"gate_pass37={'drift49_pass37_match'.encode() in v87}")

# cadence-print prior-occurrence counts (honest series accounting)
print(f"stamp600_priors={text.count('600.000s by stamp')}")
print(f"token600_priors={text.count('600s by token')}")
print(f"stamp301_priors={len([i for i in range(len(text)) if text.startswith('301.000s by stamp', i)])}")
print(f"token480_priors={len([i for i in range(len(text)) if text.startswith('480s by token', i)])}")
print(f"plus469_priors={len([i for i in range(len(text)) if text.startswith('+469', i) and not text.startswith('+469.', i)])}")
