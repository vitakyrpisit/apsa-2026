#!/usr/bin/env python3
"""Pre-guard census for cycle 2787 — MEASURED, never predicted.

Per-line census first (the c2752..c2786 per-line-census-first lessons): the
c2787/c2788 token-guard lives INSIDE the c2786 Next-block (line 9172), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2787.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2786 instrument-set presence, the
entry-cycle2786 template integrity (block == worklog lines 9161-9172), the
v86 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 600 / token-gap 600 / +290).
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

for cyc in ("c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2787={len([l for l in lines if l.startswith('Task ID: 446189-c2787')])}")
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
C2786_SET = [
    "census_c2786.py", "arrival_guard_c2786.py", "rebadge_cycle2786.py",
    "capture_cycle2786.sh", "measure_c2786_tokens.py", "recursive_diff_2786.py",
    "validate_cycle2786.py", "entry_cycle2786.txt", "append_cycle2786.py",
    "scan_cycle2786_raw.json", "scan_cycle2786.json",
]
print("c2786_instrument_set_object_presence:")
for name in C2786_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2786.txt == worklog lines 9161-9172
entry = open("/home/z/my-project/scripts/entry_cycle2786.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9160:9172]) + "\n"
print(f"entry_cycle2786_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v86 source size + lag-1 carries (the rebadge old-string expectations)
v86 = open("/home/z/my-project/scripts/validate_cycle2786.py", "rb").read()
print(f"v86_bytes={len(v86)} pass34_band={'pass-34 band'.encode() in v86} "
      f"pass34_evidence={'pass-34 evidence'.encode() in v86} "
      f"pass35_band={'pass-35 band'.encode() in v86} "
      f"pass35_evidence={'pass-35 evidence'.encode() in v86} "
      f"cycle2786={'CYCLE = 2786'.encode() in v86} "
      f"gate_pass35={'drift49_pass35_match'.encode() in v86} "
      f"gate_pass36={'drift49_pass36_match'.encode() in v86}")

# cadence-print prior-occurrence counts (honest series accounting)
print(f"stamp600_priors={text.count('600.000s by stamp')}")
print(f"token600_priors={text.count('600s by token')}")
print(f"plus290_priors={len([i for i in range(len(text)) if text.startswith('+290', i) and not text.startswith('+290.', i)])}")
