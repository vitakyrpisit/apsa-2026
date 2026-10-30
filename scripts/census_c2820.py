#!/usr/bin/env python3
"""Pre-guard census for cycle 2820 — MEASURED, never predicted.

Per-line census first (the c2752..c2819 per-line-census-first lessons): the
c2822/c2821 token-guard lives INSIDE the c2819 Next-block (line 9568), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2820.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2819 instrument-set presence, the
entry_cycle2819 template integrity (block == worklog lines 9557-9568), the
v119 source lag-1 carries (the rebadge old-string expectations), the v119
P-HIST compare base (fresh measure on actual bytes), the v119 commit-object
integrity against 5a868fa, and the cadence-print prior-occurrence counts
(stamp-gap 901 / token-gap 840 / the ahead-series tail prints + the +521 form
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

for cyc in ("c2822", "c2821", "c2820", "c2819", "c2818", "c2817", "c2816", "c2815", "c2814", "c2813", "c2812", "c2811", "c2810", "c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803", "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796", "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789", "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782", "c2781", "c2780", "c2779", "c2778",
            "c2777", "c2776", "c2775", "c2774", "c2773", "c2772", "c2771", "c2770",
            "c2769", "c2768", "c2767", "c2766", "c2765", "c2764", "c2763", "c2762",
            "c2761", "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2820={len([l for l in lines if l.startswith('Task ID: 446189-c2820')])}")
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
C2819_SET = [
    "census_c2819.py", "arrival_guard_c2819.py", "rebadge_cycle2819.py",
    "capture_cycle2819.sh", "measure_c2819_tokens.py", "recursive_diff_2819.py",
    "validate_cycle2819.py", "entry_cycle2819.txt", "append_cycle2819.py",
    "scan_cycle2819_raw.json", "scan_cycle2819.json",
]
print("c2819_instrument_set_object_presence:")
for name in C2819_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2819.txt == worklog lines 9557-9568
entry = open("/home/z/my-project/scripts/entry_cycle2819.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9556:9568]) + "\n"
print(f"entry_cycle2819_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v119 source size + lag-1 carries (the rebadge old-string expectations)
v119 = open("/home/z/my-project/scripts/validate_cycle2819.py", "rb").read()
print(f"v119_bytes={len(v119)} pass67_band={'pass-67 band'.encode() in v119} "
      f"pass67_evidence={'pass-67 evidence'.encode() in v119} "
      f"pass68_band={'pass-68 band'.encode() in v119} "
      f"pass68_evidence={'pass-68 evidence'.encode() in v119} "
      f"pass68_class={'pass-68 CLASS'.encode() in v119} "
      f"cycle2819={'CYCLE = 2819'.encode() in v119} "
      f"gate_pass68={'drift49_pass68_match'.encode() in v119} "
      f"gate_pass69={'drift49_pass69_match'.encode() in v119}")

# v119 P-HIST compare base (fresh measure on actual bytes — the MEASUREMENT GOVERNS)
import re
from collections import Counter
v119_text = v119.decode("utf-8")
hist119 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v119_text))
print(f"v119_p_hist_total={sum(hist119.values())}")
print(f"v119_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist119.items()))} }}")

# v119 commit-object integrity (the 5a868fa c2819 commit)
import subprocess
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "5a868fa:scripts/validate_cycle2819.py"], capture_output=True)
print(f"v119_object_intact={obj.returncode == 0 and obj.stdout == v119} "
      f"object_bytes={len(obj.stdout)}")

# HASH-ARTIFACT watch for v120 (the c3819e9 + c7947 lessons — the prophecy
# requires this check BEFORE forecasting): the fresh c2819 commit hash
# short form 5a868fa = 5-a-8-6-8-f-a — ZERO 'c' characters -> no c+4-digit
# run -> the c7947-class does NOT fire (zero artifact births); NO token deaths
# either (the v119 source carries zero artifact tokens — the c97826 phantom
# already departed at v113).
full_hash = subprocess.run(["git", "-C", "/home/z/my-project", "rev-parse",
                            "5a868fa"], capture_output=True, text=True).stdout.strip()
foreign_full = subprocess.run(["git", "-C", "/home/z/my-project", "rev-parse",
                               "b9757c0"], capture_output=True, text=True).stdout.strip()
m = re.findall(r"c\d{4,}", "5a868fa")
mf = re.findall(r"c\d{4,}", "b9757c0")
mfull = re.findall(r"c\d{4,}", full_hash)
mff = re.findall(r"c\d{4,}", foreign_full)
print(f"c2819_full_hash={full_hash}")
print(f"foreign_full_hash={foreign_full}")
print(f"hash_artifact_5a868fa_runs={m} (c7947-class does NOT fire: no 'c' "
      f"character at all in 5a868fa; zero births, zero deaths)")
print(f"hash_artifact_full_c2819_hash_runs={mfull}")
print(f"hash_artifact_foreign_b9757c0_runs={mf} full_foreign_runs={mff} "
      f"(the foreign TOP carries 'c0' at the tail — c followed by ONE digit, "
      f"no 4+-digit run in the short form; the foreign hash is ABSENT from the "
      f"v119 source surface, zero exposure; grep 5a868fa/b9757c0 in v119: "
      f"{('5a868fa' in v119_text) or ('b9757c0' in v119_text)})")

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
print(f"stamp901_priors={count_non_decimal('901.000s by stamp')}")
print(f"stamp901_bare_priors={count_non_decimal('901s by stamp')}")
print(f"token840_priors={count_non_decimal('840.000s by token')}")
print(f"token840_bare_priors={count_non_decimal('840s by token')}")
print(f"plus582_priors={count_non_decimal('+582s AHEAD')}")
print(f"plus582_series_priors={count_non_decimal('-> +582')}")
print(f"plus521_priors={count_non_decimal('+521s AHEAD')}")
print(f"plus521_series_priors={count_non_decimal('-> +521')}")
print(f"plus342_series_priors={count_non_decimal('-> +342')}")
print(f"echo137_530_priors={count_non_decimal('137-for-530')}")
print(f"for539_priors={count_non_decimal('-for-539')}")
print(f"for540_priors={count_non_decimal('-for-540')}")
print(f"for541_priors={count_non_decimal('-for-541')}")
print(f"deepest_1025_priors={count_non_decimal('1025.631018606')}")
print(f"prior_stamp_to_echo_756_priors={count_non_decimal('756.454358605')}")
print(f"fresh_stamp_to_echo_740_priors={count_non_decimal('740.899924115')}")
print(f"prior_echo_wall_1699_priors={count_non_decimal('1.699207044')}")
print(f"fresh_echo_wall_1670_priors={count_non_decimal('1.670891758')}")
print(f"prior_echo_curl_1689_priors={count_non_decimal('1.689836')}")
print(f"fresh_echo_curl_1661_priors={count_non_decimal('1.661584')}")
print(f"prior_echo_server_1679_priors={count_non_decimal('1679ms')}")
print(f"fresh_echo_server_1655_priors={count_non_decimal('1655ms')}")
print(f"prior_echo_postwindow_219_priors={count_non_decimal('219.650162558')}")
print(f"fresh_echo_postwindow_265_priors={count_non_decimal('265.212868478')}")
print(f"late391_366_priors={count_non_decimal('366.708518331')}")
print(f"late392_323_priors={count_non_decimal('323.674751215')}")
print(f"late393_538_priors={count_non_decimal('538.503403091')}")
print(f"lag393_779_priors={count_non_decimal('779.708')}")
print(f"dd392_514_priors={count_non_decimal('514.829')}")
print(f"dd393_539_priors={count_non_decimal('539.854')}")
print(f"ddband_lo_564_priors={count_non_decimal('564.552241212')}")
print(f"ddband_hi_3708_priors={count_non_decimal('3708.066631432')}")
print(f"runhigh_1712_priors={count_non_decimal('1712.596')}")
print(f"interval392_838_priors={count_non_decimal('838.498')}")
print(f"interval393_1078_priors={count_non_decimal('1078.352')}")
print(f"interval391_923_priors={count_non_decimal('923.669')}")
print(f"close_priors_c2819={count_non_decimal('close 5a868fa')}")
print(f"c2819hash_priors={count_non_decimal('5a868fa')}")
print(f"foreign_b9757c0_priors={count_non_decimal('b9757c0')}")
print(f"c2818hash_priors={count_non_decimal('290adbb')}")
print(f"foreign_724e4a0_priors={count_non_decimal('724e4a0')}")
print(f"placement_precapture_priors={count_non_decimal('PRE-capture placement')}")
print(f"placement_postcapture_priors={count_non_decimal('POST-capture placement')}")
print(f"bothafter_priors={count_non_decimal('BOTH-AFTER')}")
print(f"twodeep_priors={count_non_decimal('two-deep class')}")
print(f"split_priors={count_non_decimal('SPLIT official-BEFORE/foreign-AFTER')}")
print(f"ep14_s412_priors={count_non_decimal('s412')}")
print(f"ep14_s411_priors={count_non_decimal('s411')}")
print(f"sweep_client_band_priors={count_non_decimal('1.575880..1.815880')}")
print(f"sweep_server_band_priors={count_non_decimal('1609.000..1769.000')}")
print(f"sweep_client_prev_band_priors={count_non_decimal('1.677099..1.917099')}")
print(f"sweep_server_prev_band_priors={count_non_decimal('1711.000..1871.000')}")
print(f"token1241_priors={count_non_decimal('1241')}")
print(f"token1255_priors={count_non_decimal('1255')}")
print(f"token1227_priors={count_non_decimal('1227')}")
print(f"capture_wall_1705_priors={count_non_decimal('1.705305415')}")
print(f"echo_predates_318_priors={count_non_decimal('318.499076331')}")
