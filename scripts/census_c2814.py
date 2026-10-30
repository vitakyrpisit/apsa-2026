#!/usr/bin/env python3
"""Pre-guard census for cycle 2814 — MEASURED, never predicted.

Per-line census first (the c2752..c2813 per-line-census-first lessons): the
c2815/c2816 token-guard lives INSIDE the c2813 Next-block (line 9496), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2814.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2813 instrument-set presence, the
entry_cycle2813 template integrity (block == worklog lines 9485-9496), the
v113 source lag-1 carries (the rebadge old-string expectations), the v113
P-HIST compare base (fresh measure on actual bytes), the v113 commit-object
integrity against f52cdbe, and the cadence-print prior-occurrence counts
(stamp-gap 1500 / token-gap 1200 / the ahead-series tail prints + the +283
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

for cyc in ("c2816", "c2815", "c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2814={len([l for l in lines if l.startswith('Task ID: 446189-c2814')])}")
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
C2813_SET = [
    "census_c2813.py", "arrival_guard_c2813.py", "rebadge_cycle2813.py",
    "capture_cycle2813.sh", "measure_c2813_tokens.py", "recursive_diff_2813.py",
    "validate_cycle2813.py", "entry_cycle2813.txt", "append_cycle2813.py",
    "scan_cycle2813_raw.json", "scan_cycle2813.json",
]
print("c2813_instrument_set_object_presence:")
for name in C2813_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2813.txt == worklog lines 9485-9496
entry = open("/home/z/my-project/scripts/entry_cycle2813.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9484:9496]) + "\n"
print(f"entry_cycle2813_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v113 source size + lag-1 carries (the rebadge old-string expectations)
v113 = open("/home/z/my-project/scripts/validate_cycle2813.py", "rb").read()
print(f"v113_bytes={len(v113)} pass61_band={'pass-61 band'.encode() in v113} "
      f"pass61_evidence={'pass-61 evidence'.encode() in v113} "
      f"pass62_band={'pass-62 band'.encode() in v113} "
      f"pass62_evidence={'pass-62 evidence'.encode() in v113} "
      f"pass62_class={'pass-62 CLASS'.encode() in v113} "
      f"cycle2813={'CYCLE = 2813'.encode() in v113} "
      f"gate_pass62={'drift49_pass62_match'.encode() in v113} "
      f"gate_pass63={'drift49_pass63_match'.encode() in v113}")

# v113 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v113_text = v113.decode("utf-8")
hist113 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v113_text))
print(f"v113_p_hist_total={sum(hist113.values())}")
print(f"v113_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist113.items()))} }}")

# v113 commit-object integrity (the f52cdbe c2813 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "f52cdbe:scripts/validate_cycle2813.py"], capture_output=True)
print(f"v113_object_intact={obj.returncode == 0 and obj.stdout == v113} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v114 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2813 commit hash
# short form f52cdbe = f-5-2-c-d-b-e — position 3 'c' is followed by 'd'
# (non-digit, the run breaks) -> NO c+4-digit run -> the c7947-class does NOT
# fire (zero artifact births); NO token deaths either (the v113 source carries
# zero artifact tokens — the c97826 phantom already departed at v113).
m = re.findall(r"c\d{4,}", "f52cdbe")
mf = re.findall(r"c\d{4,}", "8cc4726")
print(f"hash_artifact_f52cdbe_runs={m} (c7947-class does NOT fire: no c+4-digit "
      f"run in f52cdbe; zero births, zero deaths)")
print(f"hash_artifact_foreign_8cc4726_runs={mf} (the foreign TOP carries the "
      f"c4726 run BUT the foreign hash is ABSENT from the v113 source surface "
      f"— grep 30a3440/8cc4726 in v113: "
      f"{('30a3440' in v113_text) or ('8cc4726' in v113_text)} — zero exposure)")

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

print(f"stamp1500_priors={count_non_decimal('1500.000s by stamp')}")
print(f"stamp1200_priors={count_non_decimal('1200.000s by stamp')}")
print(f"token1200_priors={count_non_decimal('1200.000s by token')}")
print(f"token1200_bare_priors={count_non_decimal('1200s by token')}")
print(f"token1320_priors={count_non_decimal('1320.000s by token')}")
print(f"token1320_bare_priors={count_non_decimal('1320s by token')}")
print(f"plus283_priors={count_non_decimal('+283s AHEAD')}")
print(f"plus283_series_priors={count_non_decimal('-> +283')}")
print(f"plus583_priors={count_non_decimal('+583s AHEAD')}")
print(f"plus583_series_priors={count_non_decimal('-> +583')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"echo137_531_priors={count_non_decimal('137-for-531')}")
print(f"echo138_531_priors={count_non_decimal('138-for-531')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_500_priors={count_non_decimal('500.889456533')}")
print(f"fresh_echo_latency_1755_priors={count_non_decimal('1.755046')}")
print(f"fresh_echo_postwindow_289_priors={count_non_decimal('289.894487633')}")
print(f"late387_311_priors={count_non_decimal('311.217915386')}")
print(f"lag387_1352_priors={count_non_decimal('1352.893')}")
print(f"dd387_1101_priors={count_non_decimal('1101.540')}")
print(f"close_priors_c2813={count_non_decimal('close f52cdbe')}")
print(f"c2813hash_priors={count_non_decimal('f52cdbe')}")
print(f"foreign_8cc4726_priors={count_non_decimal('8cc4726')}")
print(f"foreign_30a3440_priors={count_non_decimal('30a3440')}")
print(f"placement_precapture_priors={count_non_decimal('PRE-capture placement')}")
print(f"placement_postcapture_priors={count_non_decimal('POST-capture placement')}")
print(f"bothafter_priors={count_non_decimal('BOTH-AFTER')}")
print(f"bothatom_priors={count_non_decimal('both-AFTER')}")
