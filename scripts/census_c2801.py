#!/usr/bin/env python3
"""Pre-guard census for cycle 2801 — MEASURED, never predicted.

Per-line census first (the c2752..c2800 per-line-census-first lessons): the
c2801/c2802 token-guard lives INSIDE the c2800 Next-block (line 9340), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2801.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2800 instrument-set presence, the
entry_cycle2800 template integrity (block == worklog lines 9329-9340), the
v100 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 600 / token-gap 600 / the
ahead-series tail prints + the +287 form now on its first print).
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

for cyc in ("c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2801={len([l for l in lines if l.startswith('Task ID: 446189-c2801')])}")
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
C2800_SET = [
    "census_c2800.py", "arrival_guard_c2800.py", "rebadge_cycle2800.py",
    "capture_cycle2800.sh", "measure_c2800_tokens.py", "recursive_diff_2800.py",
    "validate_cycle2800.py", "entry_cycle2800.txt", "append_cycle2800.py",
    "scan_cycle2800_raw.json", "scan_cycle2800.json",
]
print("c2800_instrument_set_object_presence:")
for name in C2800_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2800.txt == worklog lines 9329-9340
entry = open("/home/z/my-project/scripts/entry_cycle2800.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9328:9340]) + "\n"
print(f"entry_cycle2800_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v100 source size + lag-1 carries (the rebadge old-string expectations)
v100 = open("/home/z/my-project/scripts/validate_cycle2800.py", "rb").read()
print(f"v100_bytes={len(v100)} pass48_band={'pass-48 band'.encode() in v100} "
      f"pass48_evidence={'pass-48 evidence'.encode() in v100} "
      f"pass49_band={'pass-49 band'.encode() in v100} "
      f"pass49_evidence={'pass-49 evidence'.encode() in v100} "
      f"cycle2800={'CYCLE = 2800'.encode() in v100} "
      f"gate_pass49={'drift49_pass49_match'.encode() in v100} "
      f"gate_pass50={'drift49_pass50_match'.encode() in v100}")

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

print(f"stamp600_priors={count_non_decimal('600.000s by stamp')}")
print(f"stamp300_priors={count_non_decimal('300.000s by stamp')}")
print(f"token600_priors={count_non_decimal('600s by token')}")
print(f"token540_priors={count_non_decimal('540s by token')}")
print(f"plus528_priors={count_non_decimal('+528s AHEAD')}")
print(f"plus528_series_priors={count_non_decimal('-> +528')}")
print(f"plus468_priors={count_non_decimal('+468s AHEAD')}")
print(f"plus468_series_priors={count_non_decimal('-> +468')}")
print(f"plus287_priors={count_non_decimal('+287s AHEAD')}")
print(f"plus287_series_priors={count_non_decimal('-> +287')}")
