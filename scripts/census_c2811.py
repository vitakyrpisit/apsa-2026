#!/usr/bin/env python3
"""Pre-guard census for cycle 2811 — MEASURED, never predicted.

Per-line census first (the c2752..c2810 per-line-census-first lessons): the
c2812/c2813 token-guard lives INSIDE the c2810 Next-block (line 9460), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2811.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2810 instrument-set presence, the
entry_cycle2810 template integrity (block == worklog lines 9449-9460), the
v110 source lag-1 carries (the rebadge old-string expectations), the v110
P-HIST compare base (fresh measure on actual bytes), the v110 commit-object
integrity against d228cc8, and the cadence-print prior-occurrence counts
(stamp-gap 901 / token-gap 900 / the ahead-series tail prints + the +344 form
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

for cyc in ("c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2811={len([l for l in lines if l.startswith('Task ID: 446189-c2811')])}")
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
C2810_SET = [
    "census_c2810.py", "arrival_guard_c2810.py", "rebadge_cycle2810.py",
    "capture_cycle2810.sh", "measure_c2810_tokens.py", "recursive_diff_2810.py",
    "validate_cycle2810.py", "entry_cycle2810.txt", "append_cycle2810.py",
    "scan_cycle2810_raw.json", "scan_cycle2810.json",
]
print("c2810_instrument_set_object_presence:")
for name in C2810_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2810.txt == worklog lines 9449-9460
entry = open("/home/z/my-project/scripts/entry_cycle2810.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9448:9460]) + "\n"
print(f"entry_cycle2810_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v110 source size + lag-1 carries (the rebadge old-string expectations)
v110 = open("/home/z/my-project/scripts/validate_cycle2810.py", "rb").read()
print(f"v110_bytes={len(v110)} pass58_band={'pass-58 band'.encode() in v110} "
      f"pass58_evidence={'pass-58 evidence'.encode() in v110} "
      f"pass59_band={'pass-59 band'.encode() in v110} "
      f"pass59_evidence={'pass-59 evidence'.encode() in v110} "
      f"cycle2810={'CYCLE = 2810'.encode() in v110} "
      f"gate_pass59={'drift49_pass59_match'.encode() in v110} "
      f"gate_pass60={'drift49_pass60_match'.encode() in v110}")

# v110 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v110_text = v110.decode("utf-8")
hist110 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v110_text))
print(f"v110_p_hist_total={sum(hist110.values())}")
print(f"v110_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist110.items()))} }}")

# v110 commit-object integrity (the d228cc8 c2810 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "d228cc8:scripts/validate_cycle2810.py"], capture_output=True)
print(f"v110_object_intact={obj.returncode == 0 and obj.stdout == v110} "
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

print(f"stamp901_priors={count_non_decimal('901.000s by stamp')}")
print(f"stamp599_priors={count_non_decimal('599.000s by stamp')}")
print(f"token900_priors={count_non_decimal('900s by token')}")
print(f"token600_priors={count_non_decimal('600s by token')}")
print(f"plus344_priors={count_non_decimal('+344s AHEAD')}")
print(f"plus344_series_priors={count_non_decimal('-> +344')}")
print(f"plus345_priors={count_non_decimal('+345s AHEAD')}")
print(f"plus345_series_priors={count_non_decimal('-> +345')}")
print(f"echo137_529_priors={count_non_decimal('137-for-529')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"echo138_531_priors={count_non_decimal('138-for-531')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_413_priors={count_non_decimal('413.371235484')}")
print(f"fresh_echo_latency_1790_priors={count_non_decimal('1.790832')}")
print(f"fresh_echo_postwindow_124_priors={count_non_decimal('124.364968476')}")
print(f"late384_312_priors={count_non_decimal('312.842975825')}")
print(f"close_priors_c2810={count_non_decimal('close d228cc8')}")
print(f"close_priors_d19b6ac={count_non_decimal('close d19b6ac')}")
print(f"foreign_92b5acc_priors={count_non_decimal('92b5acc')}")
print(f"d228cc8_priors={count_non_decimal('d228cc8')}")
