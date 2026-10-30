#!/usr/bin/env python3
"""Pre-guard census for cycle 2819 — MEASURED, never predicted.

Per-line census first (the c2752..c2818 per-line-census-first lessons): the
c2820/c2821 token-guard lives INSIDE the c2818 Next-block (line 9556), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2819.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2818 instrument-set presence, the
entry_cycle2818 template integrity (block == worklog lines 9545-9556), the
v118 source lag-1 carries (the rebadge old-string expectations), the v118
P-HIST compare base (fresh measure on actual bytes), the v118 commit-object
integrity against 290adbb, and the cadence-print prior-occurrence counts
(stamp-gap 600 / token-gap 840 / the ahead-series tail prints + the +582 form
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

for cyc in ("c2821", "c2820", "c2819", "c2818", "c2817", "c2816", "c2815", "c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2819={len([l for l in lines if l.startswith('Task ID: 446189-c2819')])}")
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
C2818_SET = [
    "census_c2818.py", "arrival_guard_c2818.py", "rebadge_cycle2818.py",
    "capture_cycle2818.sh", "measure_c2818_tokens.py", "recursive_diff_2818.py",
    "validate_cycle2818.py", "entry_cycle2818.txt", "append_cycle2818.py",
    "scan_cycle2818_raw.json", "scan_cycle2818.json",
]
print("c2818_instrument_set_object_presence:")
for name in C2818_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2818.txt == worklog lines 9545-9556
entry = open("/home/z/my-project/scripts/entry_cycle2818.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9544:9556]) + "\n"
print(f"entry_cycle2818_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v118 source size + lag-1 carries (the rebadge old-string expectations)
v118 = open("/home/z/my-project/scripts/validate_cycle2818.py", "rb").read()
print(f"v118_bytes={len(v118)} pass66_band={'pass-66 band'.encode() in v118} "
      f"pass66_evidence={'pass-66 evidence'.encode() in v118} "
      f"pass67_band={'pass-67 band'.encode() in v118} "
      f"pass67_evidence={'pass-67 evidence'.encode() in v118} "
      f"pass67_class={'pass-67 CLASS'.encode() in v118} "
      f"cycle2818={'CYCLE = 2818'.encode() in v118} "
      f"gate_pass67={'drift49_pass67_match'.encode() in v118} "
      f"gate_pass68={'drift49_pass68_match'.encode() in v118}")

# v118 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v118_text = v118.decode("utf-8")
hist118 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v118_text))
print(f"v118_p_hist_total={sum(hist118.values())}")
print(f"v118_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist118.items()))} }}")

# v118 commit-object integrity (the 290adbb c2818 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "290adbb:scripts/validate_cycle2818.py"], capture_output=True)
print(f"v118_object_intact={obj.returncode == 0 and obj.stdout == v118} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v119 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2818 commit hash
# short form 290adbb = 2-9-0-a-d-b-b — ZERO 'c' characters -> no c+4-digit
# run -> the c7947-class does NOT fire (zero artifact births); NO token deaths
# either (the v118 source carries zero artifact tokens — the c97826 phantom
# already departed at v113).
full_hash = subprocess.run(["git", "-C", "/home/z/my-project", "rev-parse",
                            "290adbb"], capture_output=True, text=True).stdout.strip()
m = re.findall(r"c\d{4,}", "290adbb")
mf = re.findall(r"c\d{4,}", "724e4a0")
mfull = re.findall(r"c\d{4,}", full_hash)
mff = re.findall(r"c\d{4,}", "252b901093474d3a97788517be0eb890")
print(f"c2818_full_hash={full_hash}")
print(f"hash_artifact_290adbb_runs={m} (c7947-class does NOT fire: no 'c' "
      f"character at all in 290adbb; zero births, zero deaths)")
print(f"hash_artifact_full_c2818_hash_runs={mfull}")
print(f"hash_artifact_foreign_724e4a0_runs={mf} full_foreign_runs={mff} "
      f"(the foreign TOP carries NO 'c' character in the short form -> no "
      f"c+4-digit run there; the foreign hash is ABSENT from the v118 source "
      f"surface, zero exposure; grep 290adbb/724e4a0 in v118: "
      f"{('290adbb' in v118_text) or ('724e4a0' in v118_text)})")

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

print(f"stamp600_priors={count_non_decimal('600.000s by stamp')}")
print(f"stamp600_bare_priors={count_non_decimal('600s by stamp')}")
print(f"token840_priors={count_non_decimal('840.000s by token')}")
print(f"token840_bare_priors={count_non_decimal('840s by token')}")
print(f"plus582_priors={count_non_decimal('+582s AHEAD')}")
print(f"plus582_series_priors={count_non_decimal('-> +582')}")
print(f"plus342_series_priors={count_non_decimal('-> +342')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"for539_priors={count_non_decimal('-for-539')}")
print(f"for540_priors={count_non_decimal('-for-540')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"fresh_stamp_to_echo_664_priors={count_non_decimal('664.515107961')}")
print(f"fresh_stamp_to_echo_756_priors={count_non_decimal('756.454358605')}")
print(f"fresh_echo_wall_1653_priors={count_non_decimal('1.653802954')}")
print(f"fresh_echo_wall_1699_priors={count_non_decimal('1.699207044')}")
print(f"fresh_echo_curl_1689_priors={count_non_decimal('1.689836')}")
print(f"fresh_echo_server_1679_priors={count_non_decimal('1679ms')}")
print(f"fresh_echo_postwindow_342_priors={count_non_decimal('342.494159700')}")
print(f"fresh_echo_postwindow_219_priors={count_non_decimal('219.650162558')}")
print(f"late391_366_priors={count_non_decimal('366.708518331')}")
print(f"late392_323_priors={count_non_decimal('323.674751215')}")
print(f"late393_538_priors={count_non_decimal('538.503403091')}")
print(f"lag392_429_priors={count_non_decimal('429.658')}")
print(f"dd392_514_priors={count_non_decimal('514.829')}")
print(f"ddband_lo_564_priors={count_non_decimal('564.552241212')}")
print(f"ddband_hi_3708_priors={count_non_decimal('3708.066631432')}")
print(f"runhigh_1712_priors={count_non_decimal('1712.596')}")
print(f"interval392_838_priors={count_non_decimal('838.498')}")
print(f"interval391_923_priors={count_non_decimal('923.669')}")
print(f"close_priors_c2818={count_non_decimal('close 290adbb')}")
print(f"c2818hash_priors={count_non_decimal('290adbb')}")
print(f"foreign_724e4a0_priors={count_non_decimal('724e4a0')}")
print(f"c2817hash_priors={count_non_decimal('da7d469')}")
print(f"foreign_a009715_priors={count_non_decimal('a009715')}")
print(f"placement_precapture_priors={count_non_decimal('PRE-capture placement')}")
print(f"placement_postcapture_priors={count_non_decimal('POST-capture placement')}")
print(f"bothafter_priors={count_non_decimal('BOTH-AFTER')}")
print(f"twodeep_priors={count_non_decimal('two-deep class')}")
print(f"split_priors={count_non_decimal('SPLIT official-BEFORE/foreign-AFTER')}")
print(f"ep14_s411_priors={count_non_decimal('s411')}")
print(f"ep14_s410_priors={count_non_decimal('s410')}")
print(f"sweep_client_band_priors={count_non_decimal('1.677099..1.917099')}")
print(f"sweep_server_band_priors={count_non_decimal('1711.000..1871.000')}")
print(f"sweep_client_old_band_priors={count_non_decimal('1.359770..1.599770')}")
print(f"sweep_server_old_band_priors={count_non_decimal('1392.000..1552.000')}")
print(f"token1241_priors={count_non_decimal('1241')}")
print(f"token1227_priors={count_non_decimal('1227')}")
print(f"echo_wall_1689b_priors={count_non_decimal('1.689293074')}")
