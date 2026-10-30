#!/usr/bin/env python3
"""Pre-guard census for cycle 2809 — MEASURED, never predicted.

Per-line census first (the c2752..c2808 per-line-census-first lessons): the
c2809/c2810 token-guard lives INSIDE the c2808 Next-block (line 9436), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2809.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2808 instrument-set presence, the
entry_cycle2808 template integrity (block == worklog lines 9425-9436), the
v108 source lag-1 carries (the rebadge old-string expectations), the v108
P-HIST compare base (fresh measure on actual bytes), the v108 commit-object
integrity against 3c0fe6c, and the cadence-print prior-occurrence counts
(stamp-gap 901 / token-gap 840 / the ahead-series tail prints + the +344 form
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

for cyc in ("c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2809={len([l for l in lines if l.startswith('Task ID: 446189-c2809')])}")
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
C2808_SET = [
    "census_c2808.py", "arrival_guard_c2808.py", "rebadge_cycle2808.py",
    "capture_cycle2808.sh", "measure_c2808_tokens.py", "recursive_diff_2808.py",
    "validate_cycle2808.py", "entry_cycle2808.txt", "append_cycle2808.py",
    "scan_cycle2808_raw.json", "scan_cycle2808.json",
]
print("c2808_instrument_set_object_presence:")
for name in C2808_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2808.txt == worklog lines 9425-9436
entry = open("/home/z/my-project/scripts/entry_cycle2808.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9424:9436]) + "\n"
print(f"entry_cycle2808_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v108 source size + lag-1 carries (the rebadge old-string expectations)
v108 = open("/home/z/my-project/scripts/validate_cycle2808.py", "rb").read()
print(f"v108_bytes={len(v108)} pass56_band={'pass-56 band'.encode() in v108} "
      f"pass56_evidence={'pass-56 evidence'.encode() in v108} "
      f"pass57_band={'pass-57 band'.encode() in v108} "
      f"pass57_evidence={'pass-57 evidence'.encode() in v108} "
      f"cycle2808={'CYCLE = 2808'.encode() in v108} "
      f"gate_pass57={'drift49_pass57_match'.encode() in v108} "
      f"gate_pass58={'drift49_pass58_match'.encode() in v108}")

# v108 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v108_text = v108.decode("utf-8")
hist108 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v108_text))
print(f"v108_p_hist_total={sum(hist108.values())}")
print(f"v108_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist108.items()))} }}")

# v108 commit-object integrity (the 3c0fe6c c2808 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "3c0fe6c:scripts/validate_cycle2808.py"], capture_output=True)
print(f"v108_object_intact={obj.returncode == 0 and obj.stdout == v108} "
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
print(f"token840_priors={count_non_decimal('840s by token')}")
print(f"token780_priors={count_non_decimal('780s by token')}")
print(f"plus344_priors={count_non_decimal('+344s AHEAD')}")
print(f"plus344_series_priors={count_non_decimal('-> +344')}")
print(f"plus405_priors={count_non_decimal('+405s AHEAD')}")
print(f"plus405_series_priors={count_non_decimal('-> +405')}")
print(f"echo137_529_priors={count_non_decimal('137-for-529')}")
print(f"echo137_528_priors={count_non_decimal('137-for-528')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_498_priors={count_non_decimal('498.928273000')}")
print(f"fresh_echo_latency_1661_priors={count_non_decimal('1.661472')}")
print(f"fresh_echo_postwindow_158_priors={count_non_decimal('158.956448889')}")
print(f"late382_417_priors={count_non_decimal('417.810145543')}")
print(f"close_priors_c2808={count_non_decimal('close 3c0fe6c')}")
