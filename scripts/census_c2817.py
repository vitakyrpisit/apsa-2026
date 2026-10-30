#!/usr/bin/env python3
"""Pre-guard census for cycle 2817 — MEASURED, never predicted.

Per-line census first (the c2752..c2816 per-line-census-first lessons): the
c2818/c2819 token-guard lives INSIDE the c2816 Next-block (line 9532), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2817.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2816 instrument-set presence, the
entry_cycle2816 template integrity (block == worklog lines 9521-9532), the
v116 source lag-1 carries (the rebadge old-string expectations), the v116
P-HIST compare base (fresh measure on actual bytes), the v116 commit-object
integrity against f3695b7, and the cadence-print prior-occurrence counts
(stamp-gap 900 / token-gap 900 / the ahead-series tail prints + the +402 form
/ the echo-account carry forms / this cycle's fresh echo prints / the
placement-class counts).
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

for cyc in ("c2819", "c2818", "c2817", "c2816", "c2815", "c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2817={len([l for l in lines if l.startswith('Task ID: 446189-c2817')])}")
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
C2816_SET = [
    "census_c2816.py", "arrival_guard_c2816.py", "rebadge_cycle2816.py",
    "capture_cycle2816.sh", "measure_c2816_tokens.py", "recursive_diff_2816.py",
    "validate_cycle2816.py", "entry_cycle2816.txt", "append_cycle2816.py",
    "scan_cycle2816_raw.json", "scan_cycle2816.json",
]
print("c2816_instrument_set_object_presence:")
for name in C2816_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2816.txt == worklog lines 9521-9532
entry = open("/home/z/my-project/scripts/entry_cycle2816.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9520:9532]) + "\n"
print(f"entry_cycle2816_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v116 source size + lag-1 carries (the rebadge old-string expectations)
v116 = open("/home/z/my-project/scripts/validate_cycle2816.py", "rb").read()
print(f"v116_bytes={len(v116)} pass64_band={'pass-64 band'.encode() in v116} "
      f"pass64_evidence={'pass-64 evidence'.encode() in v116} "
      f"pass65_band={'pass-65 band'.encode() in v116} "
      f"pass65_evidence={'pass-65 evidence'.encode() in v116} "
      f"pass65_class={'pass-65 CLASS'.encode() in v116} "
      f"cycle2816={'CYCLE = 2816'.encode() in v116} "
      f"gate_pass65={'drift49_pass65_match'.encode() in v116} "
      f"gate_pass66={'drift49_pass66_match'.encode() in v116}")

# v116 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v116_text = v116.decode("utf-8")
hist116 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v116_text))
print(f"v116_p_hist_total={sum(hist116.values())}")
print(f"v116_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist116.items()))} }}")

# v116 commit-object integrity (the f3695b7 c2816 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "f3695b7:scripts/validate_cycle2816.py"], capture_output=True)
print(f"v116_object_intact={obj.returncode == 0 and obj.stdout == v116} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v117 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2816 commit hash
# short form f3695b7 = f-3-6-9-5-b-7 — ZERO 'c' characters -> no c+4-digit
# run -> the c7947-class does NOT fire (zero artifact births); NO token deaths
# either (the v116 source carries zero artifact tokens — the c97826 phantom
# already departed at v113).
full_hash = subprocess.run(["git", "-C", "/home/z/my-project", "rev-parse",
                            "f3695b7"], capture_output=True, text=True).stdout.strip()
m = re.findall(r"c\d{4,}", "f3695b7")
mf = re.findall(r"c\d{4,}", "68117e3")
mfull = re.findall(r"c\d{4,}", full_hash)
mff = re.findall(r"c\d{4,}", "68117e3ceeb9af0f881ac24c91d09a6ac2ebe6a6")
print(f"c2816_full_hash={full_hash}")
print(f"hash_artifact_f3695b7_runs={m} (c7947-class does NOT fire: no 'c' "
      f"character at all in f3695b7; zero births, zero deaths)")
print(f"hash_artifact_full_c2816_hash_runs={mfull}")
print(f"hash_artifact_foreign_68117e3_runs={mf} full_foreign_runs={mff} "
      f"(the foreign TOP carries NO 'c' character -> no c+4-digit run; AND the "
      f"foreign hash is ABSENT from the v116 source surface — grep f3695b7/"
      f"68117e3 in v116: {('f3695b7' in v116_text) or ('68117e3' in v116_text)} "
      f"— zero exposure)")

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
print(f"stamp900_bare_priors={count_non_decimal('900s by stamp')}")
print(f"stamp1201_priors={count_non_decimal('1201.000s by stamp')}")
print(f"token900_priors={count_non_decimal('900.000s by token')}")
print(f"token900_bare_priors={count_non_decimal('900s by token')}")
print(f"token1080_priors={count_non_decimal('1080.000s by token')}")
print(f"plus402_priors={count_non_decimal('+402s AHEAD')}")
print(f"plus402_series_priors={count_non_decimal('-> +402')}")
print(f"plus523_priors={count_non_decimal('+523s AHEAD')}")
print(f"plus523_series_priors={count_non_decimal('-> +523')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"for531_priors={count_non_decimal('-for-531')}")
print(f"for530_priors={count_non_decimal('-for-530')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_539_priors={count_non_decimal('539.838339414')}")
print(f"fresh_stamp_to_echo_648_priors={count_non_decimal('648.556031485')}")
print(f"fresh_echo_wall_1699_priors={count_non_decimal('1.699002106')}")
print(f"fresh_echo_curl_1690_priors={count_non_decimal('1.690023')}")
print(f"fresh_echo_server_1683_priors={count_non_decimal('1683ms')}")
print(f"fresh_echo_postwindow_283_priors={count_non_decimal('283.546515260')}")
print(f"fresh_echo_postwindow_299_priors={count_non_decimal('299.829814544')}")
print(f"late390_241_priors={count_non_decimal('241.697817944')}")
print(f"late391_366_priors={count_non_decimal('366.708518331')}")
print(f"lag390_549_priors={count_non_decimal('549.022')}")
print(f"dd390_725_priors={count_non_decimal('725.011')}")
print(f"ddband_lo_564_priors={count_non_decimal('564.552241212')}")
print(f"ddband_hi_3708_priors={count_non_decimal('3708.066631432')}")
print(f"runhigh_1712_priors={count_non_decimal('1712.596')}")
print(f"interval390_966_priors={count_non_decimal('966.703')}")
print(f"interval389_1142_priors={count_non_decimal('1142.692')}")
print(f"close_priors_c2816={count_non_decimal('close f3695b7')}")
print(f"c2816hash_priors={count_non_decimal('f3695b7')}")
print(f"foreign_68117e3_priors={count_non_decimal('68117e3')}")
print(f"c2815hash_priors={count_non_decimal('80e165e')}")
print(f"foreign_42f95e4_priors={count_non_decimal('42f95e4')}")
print(f"placement_precapture_priors={count_non_decimal('PRE-capture placement')}")
print(f"placement_postcapture_priors={count_non_decimal('POST-capture placement')}")
print(f"bothafter_priors={count_non_decimal('BOTH-AFTER')}")
print(f"bothatom_priors={count_non_decimal('both-AFTER')}")
print(f"twodeep_priors={count_non_decimal('two-deep class')}")
print(f"split_priors={count_non_decimal('SPLIT official-BEFORE/foreign-AFTER')}")
print(f"ep14_s409_priors={count_non_decimal('s409')}")
print(f"ep14_s408_priors={count_non_decimal('s408')}")
print(f"sweep_client_band_priors={count_non_decimal('1.592498..1.832498')}")
print(f"sweep_server_band_priors={count_non_decimal('1624.000..1784.000')}")
print(f"sweep_client_old_band_priors={count_non_decimal('1.680504..1.920504')}")
print(f"sweep_server_old_band_priors={count_non_decimal('1711.000..1871.000')}")
print(f"token1213_priors={count_non_decimal('1213')}")
print(f"echo_wall_1689_priors={count_non_decimal('1.689293074')}")
