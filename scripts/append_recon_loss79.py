#!/usr/bin/env python3
"""Guarded worklog append for the LOSS EVENT #79 reconciliation block (13 lines).

Follows the entry_recon_loss5.txt precedent format. Guards: timegm epoch
cross-verification of the c2735 pre-loss epochs (decimal-exact), 13-line block
assertion, ZERO-adds assertion for the two standing anchor grep series (the block's
loss references use the 'LOSS EVENT #N' spelling), trailing-blank normalization,
post-append line-count assertion (expect 8678 + 13 = 8691). Exits non-zero on ANY
guard failure - zero worklog mutation unless all guards pass.
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_recon_loss79.txt"
EXPECT_BEFORE = 8678
EXPECT_AFTER = EXPECT_BEFORE + 13

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (the c2735 pre-loss epochs, decimal-exact)
def utc_epoch(h, m, s, ns=0):
    return calendar.timegm((2026, 10, 28, h, m, s, 0, 0, 0)) + ns / 1e9


checks = [
    ("trigger 12:00:24 +08", utc_epoch(4, 0, 24), 1793160024.0),
    ("window-2735 open 12:05:42.769241909 +08", utc_epoch(4, 5, 42, 769241909), 1793160342.769241909),
    ("loop-open echo 12:16:54.814581755 +08", utc_epoch(4, 16, 54, 814581755), 1793161014.814581755),
    ("pre-echo 12:19:21.219509722 +08", utc_epoch(4, 19, 21, 219509722), 1793161161.219509722),
    ("post-echo 12:19:28.012208950 +08", utc_epoch(4, 19, 28, 12208950), 1793161168.012208950),
    ("c2734 post-echo 12:00:42.769241909 +08", utc_epoch(4, 0, 42, 769241909), 1793160042.769241909),
    ("scanned_at 12:19:28.007 +08 (decimal)", utc_epoch(4, 19, 28) + 0.007, 1793161168.007),
    ("skew decimal-exact +5.208950ms", 1793161168.012208950 - 1793161168.007, 0.005208950),
    ("window-2736 open 12:24:28.012208950 +08", utc_epoch(4, 24, 28, 12208950), 1793161468.012208950),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==13", len(lines) == 13, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:20]))
guard("block_title", lines[1].startswith("LOSS EVENT #79"), repr(lines[1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_ends_next_bullet", lines[11].rstrip().endswith("first-job policy)."), repr(lines[11][-30:]))
guard("block_trailing_blank", block.endswith("\n\n"), repr(block[-10:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8678", n_before == EXPECT_BEFORE, f"got={n_before}")
guard("worklog_tail_is_c2667_no_gold", wl.splitlines()[-1] == "- No gold yet. Scanner continues.",
      repr(wl.splitlines()[-1][:40]))

if failures:
    print(f"APPEND_ABORTED: {len(failures)} guard failures - worklog UNTOUCHED")
    sys.exit(1)

# 4) append with newline normalization
if not wl.endswith("\n"):
    wl += "\n"
block_norm = block if block.endswith("\n") else block + "\n"
with open(WL, "a") as f:
    f.write(block_norm)

# 5) post-append assertion
n_after = open(WL).read().count("\n")
guard("post_worklog_lines==8691", n_after == EXPECT_AFTER, f"got={n_after}")
tail = open(WL).read().splitlines()[-2]
guard("tail_is_next_bullet", tail.rstrip().endswith("first-job policy)."), repr(tail[-30:]))
anchors_after = open(WL).read()
guard("anchor_series_unchanged", anchors_after.count("LOSS-#6") == 60 and anchors_after.count("LOSS-#15") == 28,
      f"LOSS-#6={anchors_after.count('LOSS-#6')} LOSS-#15={anchors_after.count('LOSS-#15')} (expect 60/28)")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print("WORKLOG_APPEND_GREEN: 8678 -> 8691 (+13), LOSS-#79 reconciliation block landed, disk ledger re-anchored")
