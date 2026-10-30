#!/usr/bin/env python3
"""Pre-guard census for cycle 2813 — MEASURED, never predicted.

Per-line census first (the c2752..c2812 per-line-census-first lessons): the
c2814/c2815 token-guard lives INSIDE the c2812 Next-block (line 9484), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2813.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2812 instrument-set presence, the
entry_cycle2812 template integrity (block == worklog lines 9473-9484), the
v112 source lag-1 carries (the rebadge old-string expectations), the v112
P-HIST compare base (fresh measure on actual bytes), the v112 commit-object
integrity against fcd7b1c, and the cadence-print prior-occurrence counts
(stamp-gap 1200 / token-gap 1320 / the ahead-series tail prints + the +583
form / the echo-account carry forms / this cycle's fresh echo prints /
the placement-class counts).
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

for cyc in ("c2815", "c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2813={len([l for l in lines if l.startswith('Task ID: 446189-c2813')])}")
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
C2812_SET = [
    "census_c2812.py", "arrival_guard_c2812.py", "rebadge_cycle2812.py",
    "capture_cycle2812.sh", "measure_c2812_tokens.py", "recursive_diff_2812.py",
    "validate_cycle2812.py", "entry_cycle2812.txt", "append_cycle2812.py",
    "scan_cycle2812_raw.json", "scan_cycle2812.json",
]
print("c2812_instrument_set_object_presence:")
for name in C2812_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2812.txt == worklog lines 9473-9484
entry = open("/home/z/my-project/scripts/entry_cycle2812.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9472:9484]) + "\n"
print(f"entry_cycle2812_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v112 source size + lag-1 carries (the rebadge old-string expectations)
v112 = open("/home/z/my-project/scripts/validate_cycle2812.py", "rb").read()
print(f"v112_bytes={len(v112)} pass60_band={'pass-60 band'.encode() in v112} "
      f"pass60_evidence={'pass-60 evidence'.encode() in v112} "
      f"pass61_band={'pass-61 band'.encode() in v112} "
      f"pass61_evidence={'pass-61 evidence'.encode() in v112} "
      f"pass61_class={'pass-61 CLASS'.encode() in v112} "
      f"cycle2812={'CYCLE = 2812'.encode() in v112} "
      f"gate_pass61={'drift49_pass61_match'.encode() in v112} "
      f"gate_pass62={'drift49_pass62_match'.encode() in v112}")

# v112 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v112_text = v112.decode("utf-8")
hist112 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v112_text))
print(f"v112_p_hist_total={sum(hist112.values())}")
print(f"v112_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist112.items()))} }}")

# v112 commit-object integrity (the fcd7b1c c2812 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "fcd7b1c:scripts/validate_cycle2812.py"], capture_output=True)
print(f"v112_object_intact={obj.returncode == 0 and obj.stdout == v112} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v113 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2812 commit hash
# short form fcd7b1c = f-c-d-7-b-1-c — position 1 'c' is followed by 'd'
# (non-digit, the run breaks), position 6 'c' is TERMINAL -> NO c+4-digit run
# -> the c7947-class does NOT fire; the c97826 phantom DEPARTS at v113 (the
# v112 P2 'the 2c97826 commit object' carry rebadges to 'the fcd7b1c commit
# object' — one token DEATH, the only exit surface).
m = re.findall(r"c\d{4,}", "fcd7b1c")
print(f"hash_artifact_fcd7b1c_runs={m} (c7947-class does NOT fire: no c+4-digit "
      f"run in fcd7b1c; the c97826 phantom departs at v113 — one token death)")

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

print(f"stamp1200_priors={count_non_decimal('1200.000s by stamp')}")
print(f"stamp1201_priors={count_non_decimal('1201.000s by stamp')}")
print(f"token1320_priors={count_non_decimal('1320s by token')}")
print(f"token900_priors={count_non_decimal('900s by token')}")
print(f"plus583_priors={count_non_decimal('+583s AHEAD')}")
print(f"plus583_series_priors={count_non_decimal('-> +583')}")
print(f"plus463_priors={count_non_decimal('+463s AHEAD')}")
print(f"plus463_series_priors={count_non_decimal('-> +463')}")
print(f"echo137_529_priors={count_non_decimal('137-for-529')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"echo138_531_priors={count_non_decimal('138-for-531')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_994_priors={count_non_decimal('994.491053914')}")
print(f"fresh_echo_latency_1562_priors={count_non_decimal('1.562345')}")
print(f"fresh_echo_postwindow_684_priors={count_non_decimal('684.844840298')}")
print(f"late386_49_priors={count_non_decimal('49.818599805')}")
print(f"lag386_1712_priors={count_non_decimal('1712.596')}")
print(f"dd386_1161_priors={count_non_decimal('1161.399')}")
print(f"close_priors_c2812={count_non_decimal('close fcd7b1c')}")
print(f"c2812hash_priors={count_non_decimal('fcd7b1c')}")
print(f"foreign_30a3440_priors={count_non_decimal('30a3440')}")
print(f"foreign_c5fb5cc_priors={count_non_decimal('c5fb5cc')}")
print(f"placement_precapture_priors={count_non_decimal('PRE-capture placement')}")
print(f"placement_postcapture_priors={count_non_decimal('POST-capture placement')}")
