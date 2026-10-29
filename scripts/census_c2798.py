#!/usr/bin/env python3
"""Pre-guard census for cycle 2798 — MEASURED, never predicted.

Per-line census first (the c2752..c2797 per-line-census-first lessons): the
c2798/c2799 token-guard lives INSIDE the c2797 Next-block (line 9304), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2798.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2797 instrument-set presence, the
entry_cycle2797 template integrity (block == worklog lines 9293-9304), the
v97 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 600 / token-gap 600 /
ahead-series tail prints).
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

for cyc in ("c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2798={len([l for l in lines if l.startswith('Task ID: 446189-c2798')])}")
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
C2797_SET = [
    "census_c2797.py", "arrival_guard_c2797.py", "rebadge_cycle2797.py",
    "capture_cycle2797.sh", "measure_c2797_tokens.py", "recursive_diff_2797.py",
    "validate_cycle2797.py", "entry_cycle2797.txt", "append_cycle2797.py",
    "scan_cycle2797_raw.json", "scan_cycle2797.json",
]
print("c2797_instrument_set_object_presence:")
for name in C2797_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2797.txt == worklog lines 9293-9304
entry = open("/home/z/my-project/scripts/entry_cycle2797.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9292:9304]) + "\n"
print(f"entry_cycle2797_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v97 source size + lag-1 carries (the rebadge old-string expectations)
v97 = open("/home/z/my-project/scripts/validate_cycle2797.py", "rb").read()
print(f"v97_bytes={len(v97)} pass45_band={'pass-45 band'.encode() in v97} "
      f"pass45_evidence={'pass-45 evidence'.encode() in v97} "
      f"pass46_band={'pass-46 band'.encode() in v97} "
      f"pass46_evidence={'pass-46 evidence'.encode() in v97} "
      f"cycle2797={'CYCLE = 2797'.encode() in v97} "
      f"gate_pass46={'drift49_pass46_match'.encode() in v97} "
      f"gate_pass47={'drift49_pass47_match'.encode() in v97}")

# cadence-print prior-occurrence counts (honest series accounting)
def count_non_decimal(s):
    n = 0
    i = 0
    while True:
        j = text.find(s, i)
        if j < 0:
            break
        if j == 0 or not text[j - 1].isdigit():
            n += 1
        i = j + 1
    return n

print(f"stamp300_priors={count_non_decimal('300.000s by stamp')}")
print(f"stamp600_priors={count_non_decimal('600.000s by stamp')}")
print(f"token600_priors={count_non_decimal('600s by token')}")
print(f"plus528_priors={count_non_decimal('+528s AHEAD')}")
print(f"plus528_series_priors={count_non_decimal('-> +528')}")
