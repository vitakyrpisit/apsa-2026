#!/usr/bin/env python3
"""Pre-measurement batch for cycle 2808 — every constant the c2808 tools need,
MEASURED against the actual bytes/objects (the MEASUREMENT GOVERNS).
Run AFTER the echo POST, BEFORE authoring the census/guard tools.
"""
import subprocess
import os
import re
from collections import Counter

WL = "/home/z/my-project/worklog.md"
DEVLOG = "/home/z/my-project/dev.log"

text = open(WL, encoding="utf-8").read()
lines = text.splitlines()
print(f"worklog_lines={len(lines)} newline_count={text.count(chr(10))}")
print(f"trailing_single_newline={text.endswith(chr(10)) and not text.endswith(chr(10)+chr(10))}")

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
print(f"anchor_TaskID={tid} anchor_nogold={gold}")
print(f"LOSS-#6_occ={text.count('LOSS-#6')} LOSS-#15_occ={text.count('LOSS-#15')}")

last = [l for l in lines if l.strip()][-1]
print(f"tail_head={last[:60]!r}")

# per-line dicts for the dict-class tokens + totals for the totals-class
for cyc in ("c2809", "c2808", "c2807", "c2806", "c2805", "c2804", "c2803",
            "c2802", "c2801", "c2800", "c2799", "c2798", "c2797", "c2796",
            "c2795", "c2794", "c2793", "c2792", "c2791", "c2790", "c2789",
            "c2788", "c2787", "c2786", "c2785", "c2784", "c2783", "c2782",
            "c2781", "c2780", "c2779", "c2778", "c2777", "c2776", "c2775",
            "c2774", "c2773", "c2772", "c2771", "c2770", "c2769", "c2768",
            "c2767", "c2766", "c2765", "c2764", "c2763", "c2762", "c2761",
            "c2760", "c2759", "c2758", "c2757", "c2756", "c2755", "c2754",
            "c2753", "c2752", "c2751", "c2750", "c2749", "c2748", "c2747"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2808={len([l for l in lines if l.startswith('Task ID: 446189-c2808')])}")

# dev.log POST census + the echo latency-match
dl = open(DEVLOG, errors="replace").read()
entries = [l for l in dl.splitlines() if "POST /api/marketplaces/scan" in l]
print(f"dev_log_post_scan_entries={len(entries)}")
for e in entries[-4:]:
    print(f"  dev_tail: {e.strip()[:110]}")

# v107 source checks
v107 = open("/home/z/my-project/scripts/validate_cycle2807.py", "rb").read()
print(f"v107_bytes={len(v107)} "
      f"pass55_band={'pass-55 band'.encode() in v107} "
      f"pass55_evidence={'pass-55 evidence'.encode() in v107} "
      f"pass56_band={'pass-56 band'.encode() in v107} "
      f"pass56_evidence={'pass-56 evidence'.encode() in v107} "
      f"cycle2807={'CYCLE = 2807'.encode() in v107} "
      f"gate_pass56={'drift49_pass56_match'.encode() in v107} "
      f"gate_pass57={'drift49_pass57_match'.encode() in v107}")

# v107 P-HIST fresh
v107_text = v107.decode("utf-8")
hist107 = Counter(f"c{t}" for t in re.findall(r"c(\d{4,})", v107_text))
print(f"v107_p_hist_total={sum(hist107.values())}")
print(f"v107_p_hist={{ {', '.join(f'{k}: {v}' for k, v in sorted(hist107.items()))} }}")

# v107 commit-object integrity vs the c2807 commit 276a60a
obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "276a60a:scripts/validate_cycle2807.py"], capture_output=True)
print(f"v107_object_intact={obj.returncode == 0 and obj.stdout == v107} "
      f"object_bytes={len(obj.stdout)}")

# c2807 instrument set presence (11 files)
C2807_SET = [
    "census_c2807.py", "arrival_guard_c2807.py", "rebadge_cycle2807.py",
    "capture_cycle2807.sh", "measure_c2807_tokens.py", "recursive_diff_2807.py",
    "validate_cycle2807.py", "entry_cycle2807.txt", "append_cycle2807.py",
    "scan_cycle2807_raw.json", "scan_cycle2807.json",
]
print("c2807_instrument_set_object_presence:")
missing = []
for name in C2807_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    ok = os.path.isfile(p)
    if not ok:
        missing.append(name)
    print(f"  {'ok' if ok else 'MISSING'} {name} bytes={os.path.getsize(p) if ok else '-'}")
print(f"instrument_missing={missing}")

# entry_cycle2807 template integrity == worklog lines 9413-9424
entry = open("/home/z/my-project/scripts/entry_cycle2807.txt", encoding="utf-8").read()
expected_block = "\n".join(lines[9412:9424]) + "\n"
print(f"entry_cycle2807_lines={len(entry.splitlines())} "
      f"matches_worklog_block={entry == expected_block}")

# cadence-print prior counts (non-decimal-preceded occurrences)
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

for form in ("901.000s by stamp", "780s by token", "600.000s by stamp",
             "660s by token", "+405s AHEAD", "-> +405", "+526s AHEAD", "-> +526",
             "+466s AHEAD", "-> +466", "137-for-528", "137-for-527",
             "1025.631018606", "864.862424272", "1.678441", "359.481742590",
             "507.104795547", "444.012641186", "417.810145543", "511.706",
             "811.706", "363.092", "+6.145543ms", "1167.418", "1219.305",
             "564.552241212", "3708.066631432", "close 276a60a", "close cceafc6",
             "1.707628", "1.947628", "1641.000", "1801.000"):
    print(f"priors[{form}]={count_non_decimal(form)}")

# echo fresh prints (this cycle's forms — expect 0 priors pre-entry)
for form in ("753.082631784", "1.700810710", "336.973296951", "1.691576"):
    print(f"priors_fresh[{form}]={count_non_decimal(form)}")

# epoch arithmetic for the entry constants
from decimal import Decimal as D
import calendar
def ep(y, mo, d, h, mi, s, ns=0):
    return D(str(calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9))

TRIG = ep(2026, 10, 30, 1, 31, 15)
TOKEN = ep(2026, 10, 30, 1, 38, 0)
C7_TRIG = ep(2026, 10, 30, 1, 16, 14)
C7_TOKEN = ep(2026, 10, 30, 1, 25, 0)
WIN2808 = D("1793324292.810145543")
WIN2807 = D("1793323481.104795547")
C7_POST = D("1793323992.810145543")
C7_SCAN = D("1793323992.804")
C7_PRE = D("1793323991.072783920")
C7_ECHO_PRE = D("1793323838.862424272")
C7_ECHO_POST = D("1793323840.586538137")
C2806_POST = D("1793323181.104795547")
C7_CLOSE = D("1793324268.000")
FOREIGN_NOW = D("1793324285.000")
E_PRE = D("1793324628.082631784")
E_POST = D("1793324629.783442494")
E_SCAN = D("1793324629.778")

print("---EPOCH ARITHMETIC---")
print(f"TRIG={TRIG} TOKEN={TOKEN}")
print(f"stamp_gap={TRIG - C7_TRIG} token_gap={TOKEN - C7_TOKEN} ahead={TOKEN - TRIG}")
print(f"LATE382={TRIG - WIN2808}")
print(f"trig_vs_c7_echo_post={TRIG - C7_ECHO_POST} (POSTDATES if +)")
print(f"trig_vs_c7_pre={C7_PRE - TRIG} (PREDATES if +)")
print(f"trig_vs_c7_scan={C7_SCAN - TRIG} (PREDATES if +)")
print(f"trig_vs_win2807={TRIG - WIN2807} (POSTDATES if +)")
print(f"c7_close_vs_trig={C7_CLOSE - TRIG} foreign_vs_trig={FOREIGN_NOW - TRIG}")
print(f"c7_close_vs_token_sec={C7_CLOSE - TOKEN} foreign_vs_token_sec={FOREIGN_NOW - TOKEN}")
print(f"c7_close_vs_win2808={C7_CLOSE - WIN2808} foreign_vs_win2808={FOREIGN_NOW - WIN2808}")
print(f"echo_postwindow={E_POST - WIN2808}")
print(f"stamp_to_echo={E_PRE - TRIG}")
print(f"echo_wall={E_POST - E_PRE}")
print(f"echo_skew={E_POST - E_SCAN}")
print(f"window2809_prophecy_base={E_POST}+300={E_POST + D('300.000')}")
