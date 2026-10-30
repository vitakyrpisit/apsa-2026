#!/usr/bin/env python3
"""Pre-guard census for cycle 2812 — MEASURED, never predicted.

Per-line census first (the c2752..c2811 per-line-census-first lessons): the
c2813/c2814 token-guard lives INSIDE the c2811 Next-block (line 9472), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2812.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2811 instrument-set presence, the
entry_cycle2811 template integrity (block == worklog lines 9461-9472), the
v111 source lag-1 carries (the rebadge old-string expectations), the v111
P-HIST compare base (fresh measure on actual bytes), the v111 commit-object
integrity against 2c97826, and the cadence-print prior-occurrence counts
(stamp-gap 1201 / token-gap 1320 / the ahead-series tail prints + the +463
form / the echo-account carry forms / this cycle's fresh echo prints).
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

for cyc in ("c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2812={len([l for l in lines if l.startswith('Task ID: 446189-c2812')])}")
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
C2811_SET = [
    "census_c2811.py", "arrival_guard_c2811.py", "rebadge_cycle2811.py",
    "capture_cycle2811.sh", "measure_c2811_tokens.py", "recursive_diff_2811.py",
    "validate_cycle2811.py", "entry_cycle2811.txt", "append_cycle2811.py",
    "scan_cycle2811_raw.json", "scan_cycle2811.json",
]
print("c2811_instrument_set_object_presence:")
for name in C2811_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2811.txt == worklog lines 9461-9472
entry = open("/home/z/my-project/scripts/entry_cycle2811.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9460:9472]) + "\n"
print(f"entry_cycle2811_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v111 source size + lag-1 carries (the rebadge old-string expectations)
v111 = open("/home/z/my-project/scripts/validate_cycle2811.py", "rb").read()
print(f"v111_bytes={len(v111)} pass59_band={'pass-59 band'.encode() in v111} "
      f"pass59_evidence={'pass-59 evidence'.encode() in v111} "
      f"pass60_band={'pass-60 band'.encode() in v111} "
      f"pass60_evidence={'pass-60 evidence'.encode() in v111} "
      f"pass60_class={'pass-60 CLASS'.encode() in v111} "
      f"cycle2811={'CYCLE = 2811'.encode() in v111} "
      f"gate_pass60={'drift49_pass60_match'.encode() in v111} "
      f"gate_pass61={'drift49_pass61_match'.encode() in v111}")

# v111 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v111_text = v111.decode("utf-8")
hist111 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v111_text))
print(f"v111_p_hist_total={sum(hist111.values())}")
print(f"v111_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist111.items()))} }}")

# v111 commit-object integrity (the 2c97826 c2811 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "2c97826:scripts/validate_cycle2811.py"], capture_output=True)
print(f"v111_object_intact={obj.returncode == 0 and obj.stdout == v111} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v112 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2811 commit hash
# short form 2c97826 = 2-c-9-7-8-2-6 — position 1 'c' is followed by '9782'
# (FOUR digits) -> the c+4-digit RUN EXISTS -> the c7947-class FIRES for the
# artifact token c97826 (the regex c(\d{4,}) matches 'c97826').
m = re.findall(r"c\d{4,}", "2c97826")
print(f"hash_artifact_2c97826_runs={m} (c7947-class FIRES: c97826 phantom birth "
      f"expected in the v112 P2 hash carry)")

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

print(f"stamp1201_priors={count_non_decimal('1201.000s by stamp')}")
print(f"stamp901_priors={count_non_decimal('901.000s by stamp')}")
print(f"token1320_priors={count_non_decimal('1320s by token')}")
print(f"token900_priors={count_non_decimal('900s by token')}")
print(f"plus463_priors={count_non_decimal('+463s AHEAD')}")
print(f"plus463_series_priors={count_non_decimal('-> +463')}")
print(f"plus344_priors={count_non_decimal('+344s AHEAD')}")
print(f"plus344_series_priors={count_non_decimal('-> +344')}")
print(f"echo137_529_priors={count_non_decimal('137-for-529')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"echo138_531_priors={count_non_decimal('138-for-531')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_1531_priors={count_non_decimal('1531.765468543')}")
print(f"fresh_echo_latency_1705_priors={count_non_decimal('1.705100')}")
print(f"fresh_echo_postwindow_883_priors={count_non_decimal('883.716091807')}")
print(f"late385_290_priors={count_non_decimal('290.804677305')}")
print(f"lag385_1031_priors={count_non_decimal('1031.867')}")
print(f"dd385_660_priors={count_non_decimal('660.015')}")
print(f"close_priors_c2811={count_non_decimal('close 2c97826')}")
print(f"c2811hash_priors={count_non_decimal('2c97826')}")
print(f"foreign_c5fb5cc_priors={count_non_decimal('c5fb5cc')}")
print(f"d228cc8_priors={count_non_decimal('d228cc8')}")
print(f"foreign_92b5acc_priors={count_non_decimal('92b5acc')}")
