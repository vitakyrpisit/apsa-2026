#!/usr/bin/env python3
"""Pre-guard census for cycle 2815 — MEASURED, never predicted.

Per-line census first (the c2752..c2814 per-line-census-first lessons): the
c2816/c2817 token-guard lives INSIDE the c2814 Next-block (line 9508), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2815.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2814 instrument-set presence, the
entry_cycle2814 template integrity (block == worklog lines 9497-9508), the
v114 source lag-1 carries (the rebadge old-string expectations), the v114
P-HIST compare base (fresh measure on actual bytes), the v114 commit-object
integrity against 9fcdbae, and the cadence-print prior-occurrence counts
(stamp-gap 900 / token-gap 1140 / the ahead-series tail prints + the +523
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

for cyc in ("c2817", "c2816", "c2815", "c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2815={len([l for l in lines if l.startswith('Task ID: 446189-c2815')])}")
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
C2814_SET = [
    "census_c2814.py", "arrival_guard_c2814.py", "rebadge_cycle2814.py",
    "capture_cycle2814.sh", "measure_c2814_tokens.py", "recursive_diff_2814.py",
    "validate_cycle2814.py", "entry_cycle2814.txt", "append_cycle2814.py",
    "scan_cycle2814_raw.json", "scan_cycle2814.json",
]
print("c2814_instrument_set_object_presence:")
for name in C2814_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2814.txt == worklog lines 9497-9508
entry = open("/home/z/my-project/scripts/entry_cycle2814.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9496:9508]) + "\n"
print(f"entry_cycle2814_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v114 source size + lag-1 carries (the rebadge old-string expectations)
v114 = open("/home/z/my-project/scripts/validate_cycle2814.py", "rb").read()
print(f"v114_bytes={len(v114)} pass62_band={'pass-62 band'.encode() in v114} "
      f"pass62_evidence={'pass-62 evidence'.encode() in v114} "
      f"pass63_band={'pass-63 band'.encode() in v114} "
      f"pass63_evidence={'pass-63 evidence'.encode() in v114} "
      f"pass63_class={'pass-63 CLASS'.encode() in v114} "
      f"cycle2814={'CYCLE = 2814'.encode() in v114} "
      f"gate_pass63={'drift49_pass63_match'.encode() in v114} "
      f"gate_pass64={'drift49_pass64_match'.encode() in v114}")

# v114 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v114_text = v114.decode("utf-8")
hist114 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v114_text))
print(f"v114_p_hist_total={sum(hist114.values())}")
print(f"v114_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist114.items()))} }}")

# v114 commit-object integrity (the 9fcdbae c2814 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "9fcdbae:scripts/validate_cycle2814.py"], capture_output=True)
print(f"v114_object_intact={obj.returncode == 0 and obj.stdout == v114} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v115 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2814 commit hash
# short form 9fcdbae = 9-f-c-d-b-a-e — position 2 'c' is followed by 'd'
# (non-digit, the run breaks) -> NO c+4-digit run -> the c7947-class does NOT
# fire (zero artifact births); NO token deaths either (the v114 source carries
# zero artifact tokens — the c97826 phantom already departed at v113).
m = re.findall(r"c\d{4,}", "9fcdbae")
mf = re.findall(r"c\d{4,}", "ef415bd")
mfull = re.findall(r"c\d{4,}", "9fcdbae5b06255e33e90f416f64cc9fbf8d6cbd2")
print(f"hash_artifact_9fcdbae_runs={m} (c7947-class does NOT fire: no c+4-digit "
      f"run in 9fcdbae; zero births, zero deaths)")
print(f"hash_artifact_full_c2814_hash_runs={mfull}")
print(f"hash_artifact_foreign_ef415bd_runs={mf} (the foreign TOP carries NO 'c' "
      f"character at all -> no c+4-digit run; AND the foreign hash is ABSENT from "
      f"the v114 source surface — grep 8cc4726/ef415bd in v114: "
      f"{('8cc4726' in v114_text) or ('ef415bd' in v114_text)} — zero exposure)")

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

print(f"stamp900_priors={count_non_decimal('900.000s by stamp')}")
print(f"stamp1500_priors={count_non_decimal('1500.000s by stamp')}")
print(f"token1140_priors={count_non_decimal('1140.000s by token')}")
print(f"token1140_bare_priors={count_non_decimal('1140s by token')}")
print(f"token1200_priors={count_non_decimal('1200.000s by token')}")
print(f"token1200_bare_priors={count_non_decimal('1200s by token')}")
print(f"plus523_priors={count_non_decimal('+523s AHEAD')}")
print(f"plus523_series_priors={count_non_decimal('-> +523')}")
print(f"plus283_priors={count_non_decimal('+283s AHEAD')}")
print(f"plus283_series_priors={count_non_decimal('-> +283')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"echo137_531_priors={count_non_decimal('137-for-531')}")
print(f"echo138_531_priors={count_non_decimal('138-for-531')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_500_priors={count_non_decimal('500.889456533')}")
print(f"fresh_echo_latency_1755_priors={count_non_decimal('1.755046')}")
print(f"fresh_echo_latency_2321_priors={count_non_decimal('2.321600')}")
print(f"fresh_echo_postwindow_289_priors={count_non_decimal('289.894487633')}")
print(f"fresh_echo_postwindow_463_priors={count_non_decimal('463.315162342')}")
print(f"late388_212_priors={count_non_decimal('212.757462242')}")
print(f"lag388_746_priors={count_non_decimal('746.666')}")
print(f"dd388_817_priors={count_non_decimal('817.727')}")
print(f"close_priors_c2814={count_non_decimal('close 9fcdbae')}")
print(f"c2814hash_priors={count_non_decimal('9fcdbae')}")
print(f"foreign_ef415bd_priors={count_non_decimal('ef415bd')}")
print(f"foreign_8cc4726_priors={count_non_decimal('8cc4726')}")
print(f"placement_precapture_priors={count_non_decimal('PRE-capture placement')}")
print(f"placement_postcapture_priors={count_non_decimal('POST-capture placement')}")
print(f"bothafter_priors={count_non_decimal('BOTH-AFTER')}")
print(f"bothatom_priors={count_non_decimal('both-AFTER')}")
print(f"twodeep_priors={count_non_decimal('two-deep class')}")
print(f"split_priors={count_non_decimal('SPLIT official-BEFORE/foreign-AFTER')}")
