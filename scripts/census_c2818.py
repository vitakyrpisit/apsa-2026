#!/usr/bin/env python3
"""Pre-guard census for cycle 2818 — MEASURED, never predicted.

Per-line census first (the c2752..c2817 per-line-census-first lessons): the
c2819/c2820 token-guard lives INSIDE the c2817 Next-block (line 9544), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2818.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2817 instrument-set presence, the
entry_cycle2817 template integrity (block == worklog lines 9533-9544), the
v117 source lag-1 carries (the rebadge old-string expectations), the v117
P-HIST compare base (fresh measure on actual bytes), the v117 commit-object
integrity against da7d469, and the cadence-print prior-occurrence counts
(stamp-gap 900 / token-gap 900 / the ahead-series tail prints + the +342 form
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

for cyc in ("c2820", "c2819", "c2818", "c2817", "c2816", "c2815", "c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2818={len([l for l in lines if l.startswith('Task ID: 446189-c2818')])}")
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
C2817_SET = [
    "census_c2817.py", "arrival_guard_c2817.py", "rebadge_cycle2817.py",
    "capture_cycle2817.sh", "measure_c2817_tokens.py", "recursive_diff_2817.py",
    "validate_cycle2817.py", "entry_cycle2817.txt", "append_cycle2817.py",
    "scan_cycle2817_raw.json", "scan_cycle2817.json",
]
print("c2817_instrument_set_object_presence:")
for name in C2817_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2817.txt == worklog lines 9533-9544
entry = open("/home/z/my-project/scripts/entry_cycle2817.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9532:9544]) + "\n"
print(f"entry_cycle2817_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v117 source size + lag-1 carries (the rebadge old-string expectations)
v117 = open("/home/z/my-project/scripts/validate_cycle2817.py", "rb").read()
print(f"v117_bytes={len(v117)} pass65_band={'pass-65 band'.encode() in v117} "
      f"pass65_evidence={'pass-65 evidence'.encode() in v117} "
      f"pass66_band={'pass-66 band'.encode() in v117} "
      f"pass66_evidence={'pass-66 evidence'.encode() in v117} "
      f"pass66_class={'pass-66 CLASS'.encode() in v117} "
      f"cycle2817={'CYCLE = 2817'.encode() in v117} "
      f"gate_pass66={'drift49_pass66_match'.encode() in v117} "
      f"gate_pass67={'drift49_pass67_match'.encode() in v117}")

# v117 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v117_text = v117.decode("utf-8")
hist117 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v117_text))
print(f"v117_p_hist_total={sum(hist117.values())}")
print(f"v117_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist117.items()))} }}")

# v117 commit-object integrity (the da7d469 c2817 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "da7d469:scripts/validate_cycle2817.py"], capture_output=True)
print(f"v117_object_intact={obj.returncode == 0 and obj.stdout == v117} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v118 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2817 commit hash
# short form da7d469 = d-a-7-d-4-6-9 — ZERO 'c' characters -> no c+4-digit
# run -> the c7947-class does NOT fire (zero artifact births); NO token deaths
# either (the v117 source carries zero artifact tokens — the c97826 phantom
# already departed at v113).
full_hash = subprocess.run(["git", "-C", "/home/z/my-project", "rev-parse",
                            "da7d469"], capture_output=True, text=True).stdout.strip()
m = re.findall(r"c\d{4,}", "da7d469")
mf = re.findall(r"c\d{4,}", "a009715")
mfull = re.findall(r"c\d{4,}", full_hash)
mff = re.findall(r"c\d{4,}", "a009715c25167e97b9ccef6666cd202725805624")
print(f"c2817_full_hash={full_hash}")
print(f"hash_artifact_da7d469_runs={m} (c7947-class does NOT fire: no 'c' "
      f"character at all in da7d469; zero births, zero deaths)")
print(f"hash_artifact_full_c2817_hash_runs={mfull}")
print(f"hash_artifact_foreign_a009715_runs={mf} full_foreign_runs={mff} "
      f"(the foreign TOP carries NO 'c' character in the short form -> no "
      f"c+4-digit run there; the FULL foreign form carries the c25167 run "
      f"regex-measured — but the foreign hash is ABSENT from the v117 source "
      f"surface, zero exposure; grep da7d469/a009715 in v117: "
      f"{('da7d469' in v117_text) or ('a009715' in v117_text)})")

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
print(f"token900_priors={count_non_decimal('900.000s by token')}")
print(f"token900_bare_priors={count_non_decimal('900s by token')}")
print(f"plus402_priors={count_non_decimal('+402s AHEAD')}")
print(f"plus402_series_priors={count_non_decimal('-> +402')}")
print(f"plus342_priors={count_non_decimal('+342s AHEAD')}")
print(f"plus342_series_priors={count_non_decimal('-> +342')}")
print(f"plus523_series_priors={count_non_decimal('-> +523')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"for538_priors={count_non_decimal('-for-538')}")
print(f"for539_priors={count_non_decimal('-for-539')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_648_priors={count_non_decimal('648.556031485')}")
print(f"fresh_stamp_to_echo_664_priors={count_non_decimal('664.515107961')}")
print(f"fresh_echo_wall_1699_priors={count_non_decimal('1.699002106')}")
print(f"fresh_echo_wall_1653_priors={count_non_decimal('1.653802954')}")
print(f"fresh_echo_curl_1644_priors={count_non_decimal('1.644084')}")
print(f"fresh_echo_server_1636_priors={count_non_decimal('1636ms')}")
print(f"fresh_echo_postwindow_283_priors={count_non_decimal('283.546515260')}")
print(f"fresh_echo_postwindow_342_priors={count_non_decimal('342.494159700')}")
print(f"late390_241_priors={count_non_decimal('241.697817944')}")
print(f"late391_366_priors={count_non_decimal('366.708518331')}")
print(f"late392_323_priors={count_non_decimal('323.674751215')}")
print(f"lag391_513_priors={count_non_decimal('513.932')}")
print(f"dd391_556_priors={count_non_decimal('556.966')}")
print(f"ddband_lo_564_priors={count_non_decimal('564.552241212')}")
print(f"ddband_hi_3708_priors={count_non_decimal('3708.066631432')}")
print(f"runhigh_1712_priors={count_non_decimal('1712.596')}")
print(f"interval391_923_priors={count_non_decimal('923.669')}")
print(f"interval390_966_priors={count_non_decimal('966.703')}")
print(f"close_priors_c2817={count_non_decimal('close da7d469')}")
print(f"c2817hash_priors={count_non_decimal('da7d469')}")
print(f"foreign_a009715_priors={count_non_decimal('a009715')}")
print(f"c2816hash_priors={count_non_decimal('f3695b7')}")
print(f"foreign_68117e3_priors={count_non_decimal('68117e3')}")
print(f"placement_precapture_priors={count_non_decimal('PRE-capture placement')}")
print(f"placement_postcapture_priors={count_non_decimal('POST-capture placement')}")
print(f"bothafter_priors={count_non_decimal('BOTH-AFTER')}")
print(f"twodeep_priors={count_non_decimal('two-deep class')}")
print(f"split_priors={count_non_decimal('SPLIT official-BEFORE/foreign-AFTER')}")
print(f"ep14_s410_priors={count_non_decimal('s410')}")
print(f"ep14_s409_priors={count_non_decimal('s409')}")
print(f"sweep_client_band_priors={count_non_decimal('1.359770..1.599770')}")
print(f"sweep_server_band_priors={count_non_decimal('1392.000..1552.000')}")
print(f"sweep_client_old_band_priors={count_non_decimal('1.592498..1.832498')}")
print(f"sweep_server_old_band_priors={count_non_decimal('1624.000..1784.000')}")
print(f"token1227_priors={count_non_decimal('1227')}")
print(f"token1213_priors={count_non_decimal('1213')}")
print(f"echo_wall_1689_priors={count_non_decimal('1.689293074')}")
