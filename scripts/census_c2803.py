#!/usr/bin/env python3
"""Pre-guard census for cycle 2803 — MEASURED, never predicted.

Per-line census first (the c2752..c2802 per-line-census-first lessons): the
c2803/c2804 token-guard lives INSIDE the c2802 Next-block (line 9364), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2803.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2802 instrument-set presence, the
entry_cycle2802 template integrity (block == worklog lines 9353-9364), the
v102 source lag-1 carries (the rebadge old-string expectations), and the
cadence-print prior-occurrence counts (stamp-gap 600/300 / token-gap 540/480 /
the ahead-series tail prints + the +407 form on its first print).
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

for cyc in ("c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2803={len([l for l in lines if l.startswith('Task ID: 446189-c2803')])}")
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
C2802_SET = [
    "census_c2802.py", "arrival_guard_c2802.py", "rebadge_cycle2802.py",
    "capture_cycle2802.sh", "measure_c2802_tokens.py", "recursive_diff_2802.py",
    "validate_cycle2802.py", "entry_cycle2802.txt", "append_cycle2802.py",
    "scan_cycle2802_raw.json", "scan_cycle2802.json",
]
print("c2802_instrument_set_object_presence:")
for name in C2802_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2802.txt == worklog lines 9353-9364
entry = open("/home/z/my-project/scripts/entry_cycle2802.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9352:9364]) + "\n"
print(f"entry_cycle2802_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v102 source size + lag-1 carries (the rebadge old-string expectations)
v102 = open("/home/z/my-project/scripts/validate_cycle2802.py", "rb").read()
print(f"v102_bytes={len(v102)} pass50_band={'pass-50 band'.encode() in v102} "
      f"pass50_evidence={'pass-50 evidence'.encode() in v102} "
      f"pass51_band={'pass-51 band'.encode() in v102} "
      f"pass51_evidence={'pass-51 evidence'.encode() in v102} "
      f"cycle2802={'CYCLE = 2802'.encode() in v102} "
      f"gate_pass51={'drift49_pass51_match'.encode() in v102} "
      f"gate_pass52={'drift49_pass52_match'.encode() in v102}")

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
print(f"token540_priors={count_non_decimal('540s by token')}")
print(f"token480_priors={count_non_decimal('480s by token')}")
print(f"plus407_priors={count_non_decimal('+407s AHEAD')}")
print(f"plus407_series_priors={count_non_decimal('-> +407')}")
print(f"plus467_priors={count_non_decimal('+467s AHEAD')}")
print(f"plus467_series_priors={count_non_decimal('-> +467')}")
