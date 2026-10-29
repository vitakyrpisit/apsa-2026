#!/usr/bin/env python3
"""Pre-guard census for cycle 2782 — MEASURED, never predicted.

Per-line census first (the c2752..c2781 per-line-census-first lessons): the
c2782/c2783 token-guard lives INSIDE the c2781 Next-block (line 9112), so the
guard expectations are set from MEASUREMENT before arrival_guard_c2782.py is
written. Also measures: anchors, dup-check state, dev.log foreign-POST census,
.basedagents blocker probe, the c2781 instrument-set presence, and the
entry-cycle2781 template integrity (block == worklog lines 9101-9112).
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

for cyc in ("c2783", "c2782", "c2781", "c2780", "c2779", "c2778", "c2777", "c2776",
            "c2775", "c2774", "c2773", "c2772", "c2771", "c2770", "c2769", "c2768",
            "c2767", "c2766", "c2765", "c2764", "c2763", "c2762", "c2761", "c2760",
            "c2759", "c2758", "c2757", "c2756", "c2755", "c2754", "c2753", "c2752",
            "c2751", "c2750", "c2749", "c2748", "c2747", "c2746"):
    per_line = {i + 1: l.count(cyc) for i, l in enumerate(lines) if cyc in l}
    print(f"{cyc}_total={text.count(cyc)} per_line={per_line}")

print(f"dup_serviced_c2782={len([l for l in lines if l.startswith('Task ID: 446189-c2782')])}")
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
C2781_SET = [
    "census_c2781.py", "arrival_guard_c2781.py", "rebadge_cycle2781.py",
    "capture_cycle2781.sh", "measure_c2781_tokens.py", "recursive_diff_2781.py",
    "validate_cycle2781.py", "entry_cycle2781.txt", "append_cycle2781.py",
    "scan_cycle2781_raw.json", "scan_cycle2781.json",
]
print("c2781_instrument_set_object_presence:")
for name in C2781_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    print(f"  {'ok' if os.path.isfile(p) else 'MISSING'} {name} "
          f"bytes={os.path.getsize(p) if os.path.isfile(p) else '-'}")

# entry template integrity: entry_cycle2781.txt == worklog lines 9101-9112
entry = open("/home/z/my-project/scripts/entry_cycle2781.txt", encoding="utf-8").read()
entry_lines = entry.splitlines()
expected_block = "\n".join(lines[9100:9112]) + "\n"
print(f"entry_cycle2781_lines={len(entry_lines)} "
      f"matches_worklog_block={entry == expected_block}")

# v81 source size + lag-1 carries (the rebadge old-string expectations)
v81 = open("/home/z/my-project/scripts/validate_cycle2781.py", "rb").read()
print(f"v81_bytes={len(v81)} pass29_band={'pass-29 band'.encode() in v81} "
      f"pass29_evidence={'pass-29 evidence'.encode() in v81} "
      f"pass30_band={'pass-30 band'.encode() in v81} "
      f"pass30_evidence={'pass-30 evidence'.encode() in v81}")
