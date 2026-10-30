#!/usr/bin/env python3
"""Pre-guard census for cycle 2808 — MEASURED, never predicted.

Per-line census first (the c2752..c2807 per-line-census-first lessons): the
c2808/c2809 token-guard lives INSIDE the c2807 Next-block (line 9424), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2808.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2807 instrument-set presence, the
entry_cycle2807 template integrity (block == worklog lines 9413-9424), the
v107 source lag-1 carries (the rebadge old-string expectations), the v107
P-HIST compare base (fresh measure on actual bytes), the v107 commit-object
integrity against 276a60a, and the cadence-print prior-occurrence counts
(stamp-gap 901 / token-gap 780 / the ahead-series tail prints + the +405 form
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

for cyc in ("c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2808={len([l for l in lines if l.startswith('Task ID: 446189-c2808')])}")
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
C2807_SET = [
    "census_c2807.py", "arrival_guard_c2807.py", "rebadge_cycle2807.py",
    "capture_cycle2807.sh", "measure_c2807_tokens.py", "recursive_diff_2807.py",
    "validate_cycle2807.py", "entry_cycle2807.txt", "append_cycle2807.py",
    "scan_cycle2807_raw.json", "scan_cycle2807.json",
]
print("c2807_instrument_set_object_presence:")
for name in C2807_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2807.txt == worklog lines 9413-9424
entry = open("/home/z/my-project/scripts/entry_cycle2807.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9412:9424]) + "\n"
print(f"entry_cycle2807_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v107 source size + lag-1 carries (the rebadge old-string expectations)
v107 = open("/home/z/my-project/scripts/validate_cycle2807.py", "rb").read()
print(f"v107_bytes={len(v107)} pass55_band={'pass-55 band'.encode() in v107} "
      f"pass55_evidence={'pass-55 evidence'.encode() in v107} "
      f"pass56_band={'pass-56 band'.encode() in v107} "
      f"pass56_evidence={'pass-56 evidence'.encode() in v107} "
      f"cycle2807={'CYCLE = 2807'.encode() in v107} "
      f"gate_pass56={'drift49_pass56_match'.encode() in v107} "
      f"gate_pass57={'drift49_pass57_match'.encode() in v107}")

# v107 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v107_text = v107.decode("utf-8")
hist107 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v107_text))
print(f"v107_p_hist_total={sum(hist107.values())}")
print(f"v107_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist107.items()))} }}")

# v107 commit-object integrity (the 276a60a c2807 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "276a60a:scripts/validate_cycle2807.py"], capture_output=True)
print(f"v107_object_intact={obj.returncode == 0 and obj.stdout == v107} "
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
print(f"token780_priors={count_non_decimal('780s by token')}")
print(f"token660_priors={count_non_decimal('660s by token')}")
print(f"plus405_priors={count_non_decimal('+405s AHEAD')}")
print(f"plus405_series_priors={count_non_decimal('-> +405')}")
print(f"plus526_priors={count_non_decimal('+526s AHEAD')}")
print(f"plus526_series_priors={count_non_decimal('-> +526')}")
print(f"echo137_528_priors={count_non_decimal('137-for-528')}")
print(f"echo137_527_priors={count_non_decimal('137-for-527')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_753_priors={count_non_decimal('753.082631784')}")
print(f"fresh_echo_latency_1691_priors={count_non_decimal('1.691576')}")
print(f"fresh_echo_postwindow_336_priors={count_non_decimal('336.973296951')}")
print(f"late381_507_priors={count_non_decimal('507.104795547')}")
print(f"close_priors_c2807={count_non_decimal('close 276a60a')}")
