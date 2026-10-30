#!/usr/bin/env python3
"""Pre-guard census for cycle 2807 — MEASURED, never predicted.

Per-line census first (the c2752..c2806 per-line-census-first lessons): the
c2807/c2808 token-guard lives INSIDE the c2806 Next-block (line 9412), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2807.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2806 instrument-set presence, the
entry_cycle2806 template integrity (block == worklog lines 9401-9412), the
v106 source lag-1 carries (the rebadge old-string expectations), the v106
P-HIST compare base (fresh measure on actual bytes), the v106 commit-object
integrity against cceafc6, and the cadence-print prior-occurrence counts
(stamp-gap 600 / token-gap 660 / the ahead-series tail prints + the +526 form
/ the echo-account carry forms / this cycle's fresh echo prints).
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

for cyc in ("c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2807={len([l for l in lines if l.startswith('Task ID: 446189-c2807')])}")
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
C2806_SET = [
    "census_c2806.py", "arrival_guard_c2806.py", "rebadge_cycle2806.py",
    "capture_cycle2806.sh", "measure_c2806_tokens.py", "recursive_diff_2806.py",
    "validate_cycle2806.py", "entry_cycle2806.txt", "append_cycle2806.py",
    "scan_cycle2806_raw.json", "scan_cycle2806.json",
]
print("c2806_instrument_set_object_presence:")
for name in C2806_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2806.txt == worklog lines 9401-9412
entry = open("/home/z/my-project/scripts/entry_cycle2806.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9400:9412]) + "\n"
print(f"entry_cycle2806_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v106 source size + lag-1 carries (the rebadge old-string expectations)
v106 = open("/home/z/my-project/scripts/validate_cycle2806.py", "rb").read()
print(f"v106_bytes={len(v106)} pass54_band={'pass-54 band'.encode() in v106} "
      f"pass54_evidence={'pass-54 evidence'.encode() in v106} "
      f"pass55_band={'pass-55 band'.encode() in v106} "
      f"pass55_evidence={'pass-55 evidence'.encode() in v106} "
      f"cycle2806={'CYCLE = 2806'.encode() in v106} "
      f"gate_pass55={'drift49_pass55_match'.encode() in v106} "
      f"gate_pass56={'drift49_pass56_match'.encode() in v106}")

# v106 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v106_text = v106.decode("utf-8")
hist106 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v106_text))
print(f"v106_p_hist_total={sum(hist106.values())}")
print(f"v106_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist106.items()))} }}")

# v106 commit-object integrity (the cceafc6 c2806 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "cceafc6:scripts/validate_cycle2806.py"], capture_output=True)
print(f"v106_object_intact={obj.returncode == 0 and obj.stdout == v106} "
      f"object_bytes={len(obj.stdout)}")

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
print(f"token660_priors={count_non_decimal('660s by token')}")
print(f"token780_priors={count_non_decimal('780s by token')}")
print(f"plus526_priors={count_non_decimal('+526s AHEAD')}")
print(f"plus526_series_priors={count_non_decimal('-> +526')}")
print(f"plus466_priors={count_non_decimal('+466s AHEAD')}")
print(f"plus466_series_priors={count_non_decimal('-> +466')}")
print(f"echo137_527_priors={count_non_decimal('137-for-527')}")
print(f"echo137_526_priors={count_non_decimal('137-for-526')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_864_priors={count_non_decimal('864.862424272')}")
print(f"fresh_echo_latency_1678_priors={count_non_decimal('1.678441')}")
print(f"fresh_echo_postwindow_359_priors={count_non_decimal('359.481742590')}")
print(f"late380_444_priors={count_non_decimal('444.012641186')}")
print(f"close_priors_c2806={count_non_decimal('close cceafc6')}")
