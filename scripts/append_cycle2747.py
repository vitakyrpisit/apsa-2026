#!/usr/bin/env python3
"""Guarded worklog append for the c2747 entry + LOSS EVENT #83 declaration (13 lines).

Follows the append_recon_loss79.py precedent: ALL asserts precede the mutation;
any failure -> APPEND_ABORTED, worklog UNTOUCHED. Guards: python-timegm epoch
cross-verification (decimal-exact), block structure (13 lines incl. the standard
Task ID declaration line, separator first, Next bullet last, zero adds to the two
standing post-#6/post-#15 anchor series), pre-state (8691 lines, tail = the recon
Next bullet, dup-check zero c2747 keys, anchor series 424/357/60/28), post-state
(8704 lines, tail = the c2748 Next bullet, anchors 425/358/60/28). Zero mid-line
writes (append at EOF only). Attempt-3 of the c2747 append (attempt-1 aborted
clean pre-mutation; attempt-2 landed then post-RED on the missing Task ID line
and was reverted byte-exact pre-commit — all recorded in the block's Step 7).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2747.txt"
EXPECT_BEFORE = 8691
EXPECT_AFTER = EXPECT_BEFORE + 13

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (decimal-exact)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


checks = [
    ("trigger stamp 00:01:03 +08 = 1793289663.000", utc_epoch(2026, 10, 29, 16, 1, 3), 1793289663.000),
    ("loop-open echo 00:02:12.601723813 +08", utc_epoch(2026, 10, 29, 16, 2, 12, 601723813), 1793289732.601723813),
    ("pre-echo 00:12:01.660023628 +08", utc_epoch(2026, 10, 29, 16, 12, 1, 660023628), 1793290321.660023628),
    ("post-echo 00:12:03.671843758 +08", utc_epoch(2026, 10, 29, 16, 12, 3, 671843758), 1793290323.671843758),
    ("scanned_at 00:12:03.665 +08 (decimal)", utc_epoch(2026, 10, 29, 16, 12, 3) + 0.665, 1793290323.665),
    ("c2746 scanned_at 02:33:14.936 +08 (decimal)", utc_epoch(2026, 10, 28, 18, 33, 14) + 0.936, 1793212394.936),
    ("window-2747 open (prophecy epoch = c2746 post-echo + 300.000; +08 rendering 02:38:14.939926673)",
     utc_epoch(2026, 10, 28, 18, 38, 14, 939926673), 1793212694.939926673),
    ("window-2748 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 16, 17, 3, 671843758), 1793290623.671843758),
    ("skew decimal-exact +6.843758ms", 1793290323.671843758 - 1793290323.665, 0.006843758),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==13", len(lines) == 13, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2747"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2747"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2748 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))
guard("block_loss83_spelling", block.count("LOSS EVENT #83") >= 2,
      f"LOSS EVENT #83 x{block.count('LOSS EVENT #83')}")

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8691", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_recon_next_bullet", last_nonempty.endswith("first-job policy)."),
      repr(last_nonempty[:40]))
guard("dup_check_no_c2747_key", wl.count("446189-c2747") == 0 and wl.count("c2747") == 0,
      f"446189-c2747={wl.count('446189-c2747')} c2747={wl.count('c2747')}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==424", tid_pre == 424, f"got={tid_pre}")
guard("anchor_nogold_pre==357", gold_pre == 357, f"got={gold_pre}")
guard("anchor_LOSS6_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")

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
guard("post_worklog_lines==8704", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2748_next_bullet", last2.startswith("- Next: the c2748 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==425", tid_post == 425, f"got={tid_post}")
guard("anchor_nogold_post==358", gold_post == 358, f"got={gold_post}")
guard("anchor_LOSS6_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("c2747_now_present", wl2.count("c2747") > 0, f"c2747={wl2.count('c2747')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print("WORKLOG_APPEND_GREEN: 8691 -> 8704 (+13), c2747 entry + LOSS EVENT #83 block landed (attempt-3)")
