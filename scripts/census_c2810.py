#!/usr/bin/env python3
"""Pre-guard census for cycle 2810 — MEASURED, never predicted.

Per-line census first (the c2752..c2809 per-line-census-first lessons): the
c2810/c2811 token-guard lives INSIDE the c2809 Next-block (line 9448), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2810.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2809 instrument-set presence, the
entry_cycle2809 template integrity (block == worklog lines 9437-9448), the
v109 source lag-1 carries (the rebadge old-string expectations), the v109
P-HIST compare base (fresh measure on actual bytes), the v109 commit-object
integrity against d19b6ac, and the cadence-print prior-occurrence counts
(stamp-gap 599 / token-gap 600 / the ahead-series tail prints + the +345 form
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

for cyc in ("c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2810={len([l for l in lines if l.startswith('Task ID: 446189-c2810')])}")
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
C2809_SET = [
    "census_c2809.py", "arrival_guard_c2809.py", "rebadge_cycle2809.py",
    "capture_cycle2809.sh", "measure_c2809_tokens.py", "recursive_diff_2809.py",
    "validate_cycle2809.py", "entry_cycle2809.txt", "append_cycle2809.py",
    "scan_cycle2809_raw.json", "scan_cycle2809.json",
]
print("c2809_instrument_set_object_presence:")
for name in C2809_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2809.txt == worklog lines 9437-9448
entry = open("/home/z/my-project/scripts/entry_cycle2809.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9436:9448]) + "\n"
print(f"entry_cycle2809_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v109 source size + lag-1 carries (the rebadge old-string expectations)
v109 = open("/home/z/my-project/scripts/validate_cycle2809.py", "rb").read()
print(f"v109_bytes={len(v109)} pass57_band={'pass-57 band'.encode() in v109} "
      f"pass57_evidence={'pass-57 evidence'.encode() in v109} "
      f"pass58_band={'pass-58 band'.encode() in v109} "
      f"pass58_evidence={'pass-58 evidence'.encode() in v109} "
      f"cycle2809={'CYCLE = 2809'.encode() in v109} "
      f"gate_pass58={'drift49_pass58_match'.encode() in v109} "
      f"gate_pass59={'drift49_pass59_match'.encode() in v109}")

# v109 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v109_text = v109.decode("utf-8")
hist109 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v109_text))
print(f"v109_p_hist_total={sum(hist109.values())}")
print(f"v109_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist109.items()))} }}")

# v109 commit-object integrity (the d19b6ac c2809 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "d19b6ac:scripts/validate_cycle2809.py"], capture_output=True)
print(f"v109_object_intact={obj.returncode == 0 and obj.stdout == v109} "
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

print(f"stamp599_priors={count_non_decimal('599.000s by stamp')}")
print(f"stamp901_priors={count_non_decimal('901.000s by stamp')}")
print(f"token600_priors={count_non_decimal('600s by token')}")
print(f"token840_priors={count_non_decimal('840s by token')}")
print(f"plus345_priors={count_non_decimal('+345s AHEAD')}")
print(f"plus345_series_priors={count_non_decimal('-> +345')}")
print(f"plus344_priors={count_non_decimal('+344s AHEAD')}")
print(f"plus344_series_priors={count_non_decimal('-> +344')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"echo138_530_priors={count_non_decimal('138-for-530')}")
print(f"echo137_529_priors={count_non_decimal('137-for-529')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_717_priors={count_non_decimal('717.157953294')}")
print(f"fresh_echo_latency_1807_priors={count_non_decimal('1.807991')}")
print(f"fresh_echo_postwindow_406_priors={count_non_decimal('406.132728634')}")
print(f"late383_339_priors={count_non_decimal('339.971824111')}")
print(f"close_priors_c2809={count_non_decimal('close d19b6ac')}")
print(f"close_priors_3c0fe6c={count_non_decimal('close 3c0fe6c')}")
