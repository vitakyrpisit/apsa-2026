#!/usr/bin/env python3
"""Pre-guard census for cycle 2805 — MEASURED, never predicted.

Per-line census first (the c2752..c2804 per-line-census-first lessons): the
c2805/c2806 token-guard lives INSIDE the c2804 Next-block (line 9388), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2805.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2804 instrument-set presence, the
entry_cycle2804 template integrity (block == worklog lines 9377-9388), the
v104 source lag-1 carries (the rebadge old-string expectations), the v104
P-HIST compare base (fresh measure on actual bytes), and the cadence-print
prior-occurrence counts (stamp-gap 901 / token-gap 660 / the ahead-series tail
prints + the +286 form / the echo-account carry forms).
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

for cyc in ("c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2805={len([l for l in lines if l.startswith('Task ID: 446189-c2805')])}")
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
C2804_SET = [
    "census_c2804.py", "arrival_guard_c2804.py", "rebadge_cycle2804.py",
    "capture_cycle2804.sh", "measure_c2804_tokens.py", "recursive_diff_2804.py",
    "validate_cycle2804.py", "entry_cycle2804.txt", "append_cycle2804.py",
    "scan_cycle2804_raw.json", "scan_cycle2804.json",
]
print("c2804_instrument_set_object_presence:")
for name in C2804_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2804.txt == worklog lines 9377-9388
entry = open("/home/z/my-project/scripts/entry_cycle2804.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9376:9388]) + "\n"
print(f"entry_cycle2804_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v104 source size + lag-1 carries (the rebadge old-string expectations)
v104 = open("/home/z/my-project/scripts/validate_cycle2804.py", "rb").read()
print(f"v104_bytes={len(v104)} pass52_band={'pass-52 band'.encode() in v104} "
      f"pass52_evidence={'pass-52 evidence'.encode() in v104} "
      f"pass53_band={'pass-53 band'.encode() in v104} "
      f"pass53_evidence={'pass-53 evidence'.encode() in v104} "
      f"cycle2804={'CYCLE = 2804'.encode() in v104} "
      f"gate_pass53={'drift49_pass53_match'.encode() in v104} "
      f"gate_pass54={'drift49_pass54_match'.encode() in v104}")

# v104 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v104_text = v104.decode("utf-8")
hist104 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v104_text))
print(f"v104_p_hist_total={sum(hist104.values())}")
print(f"v104_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist104.items()))} }}")

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

print(f"stamp901_priors={count_non_decimal('901.000s by stamp')}")
print(f"stamp600_priors={count_non_decimal('600.000s by stamp')}")
print(f"token660_priors={count_non_decimal('660s by token')}")
print(f"token720_priors={count_non_decimal('720s by token')}")
print(f"plus286_priors={count_non_decimal('+286s AHEAD')}")
print(f"plus286_series_priors={count_non_decimal('-> +286')}")
print(f"plus527_priors={count_non_decimal('+527s AHEAD')}")
print(f"plus527_series_priors={count_non_decimal('-> +527')}")
print(f"echo137_524_priors={count_non_decimal('137-for-524')}")
print(f"echo137_525_priors={count_non_decimal('137-for-525')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
