#!/usr/bin/env python3
"""Guarded worklog append for the c2748 entry (12 lines).

Follows the append_cycle2747.py (attempt-3 GREEN) precedent: ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact), block
structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method; rg line-counts undercount),
pre-state (8704 lines, tail = the c2748 Next bullet, zero serviced c2748
entries, anchors 425/358/60/28), post-state (8716 lines, tail = the c2749
Next bullet, anchors 426/359/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2748.txt"
EXPECT_BEFORE = 8704
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (decimal-exact)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


checks = [
    ("trigger stamp 00:11:04 +08 = 1793290264.000", utc_epoch(2026, 10, 29, 16, 11, 4), 1793290264.000),
    ("loop-open echo 00:20:47.543393112 +08", utc_epoch(2026, 10, 29, 16, 20, 47, 543393112), 1793290847.543393112),
    ("pre-echo epoch 1793290955.003916149", utc_epoch(2026, 10, 29, 16, 22, 35, 3916149), 1793290955.003916149),
    ("post-echo 00:22:37.030814043 +08 (epoch ns)", utc_epoch(2026, 10, 29, 16, 22, 37, 30814043), 1793290957.030814043),
    ("scanned_at 00:22:37.024 +08 (decimal)", utc_epoch(2026, 10, 29, 16, 22, 37) + 0.024, 1793290957.024),
    ("c2747 scanned_at 00:12:03.665 +08 (decimal)", utc_epoch(2026, 10, 29, 16, 12, 3) + 0.665, 1793290323.665),
    ("window-2748 open 00:17:03.671843758 +08", utc_epoch(2026, 10, 29, 16, 17, 3, 671843758), 1793290623.671843758),
    ("window-2749 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 16, 27, 37, 30814043), 1793291257.030814043),
    ("skew decimal-exact +6.814043ms", 1793290957.030814043 - 1793290957.024, 0.006814043),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2748"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2748"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2749 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8704", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2748_next_bullet", last_nonempty.startswith("- Next: the c2748 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2748",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2748")]) == 0,
      f"c2748 substring mentions={wl.count('c2748')} (expect 4, all Next-block pre-declaration)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==425", tid_pre == 425, f"got={tid_pre}")
guard("anchor_nogold_pre==358", gold_pre == 358, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")

if failures:
    print(f"APPEND_ABORTED: {len(failures)} guard failures - worklog UNTOUCHED")
    sys.exit(1)

# 4) append with newline normalization
if not wl.endswith("\n"):
    wl += "\n"
block_norm = block if block.endswith("\n") else block + "\n"
with open(WL, "a") as f:
    f.write(block_norm)

# 5) post-append assertions
wl2 = open(WL).read()
n_after = wl2.count("\n")
guard("post_worklog_lines==8716", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2749_next_bullet", last2.startswith("- Next: the c2749 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==426", tid_post == 426, f"got={tid_post}")
guard("anchor_nogold_post==359", gold_post == 359, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2748_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2748")]) == 1)

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print("WORKLOG_APPEND_GREEN: 8704 -> 8716 (+12), c2748 entry landed (first-pass clean)")
