#!/usr/bin/env python3
"""Guarded worklog append for the c2755 entry (12 lines).

Follows the append_cycle2754.py (first-pass GREEN) precedent: ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 15 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and the dual echo decomposition),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8788 lines,
tail = the c2755 Next bullet, zero serviced c2755 entries, c2755 mention
census per-line {8776: 1, 8780: 2, 8788: 4}, anchors 432/365/60/28), post-state
(8800 lines, tail = the c2756 Next bullet, anchors 433/366/60/28). Zero
mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2755.txt"
EXPECT_BEFORE = 8788
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (decimal-exact, 15 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = 1793295235.387245275   # c2755 post-echo (EPOCH-governs)
SCAN = 1793295235.380         # c2755 scanned_at (decimal)
TRIG = 1793294465.000         # c2755 trigger stamp
WIN = 1793294934.964190626    # window-2755 open (c2754 prophecy)
ECHO = 1793295116.988399785   # loop-open in-batch echo (EPOCH-governs)
C2754_SCAN = 1793294634.957   # c2754 scanned_at

checks = [
    ("trigger stamp 01:21:05 +08 = 1793294465.000", utc_epoch(2026, 10, 29, 17, 21, 5), TRIG),
    ("loop-open echo ISO 01:31:56.987724964 +08", utc_epoch(2026, 10, 29, 17, 31, 56, 987724964), 1793295116.987724964),
    ("loop-open echo EPOCH 1793295116.988399785 (EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 31, 56, 988399785), ECHO),
    ("pre-echo EPOCH 1793295233.706407358 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 33, 53, 706407358), 1793295233.706407358),
    ("post-echo 01:33:55.387245275 +08 (epoch ns)", utc_epoch(2026, 10, 29, 17, 33, 55, 387245275), POST),
    ("scanned_at 01:33:55.380 +08 (decimal)", utc_epoch(2026, 10, 29, 17, 33, 55) + 0.380, SCAN),
    ("c2754 scanned_at 01:23:54.957 +08 (decimal)", utc_epoch(2026, 10, 29, 17, 23, 54) + 0.957, C2754_SCAN),
    ("window-2755 open 01:28:54.964190626 +08", utc_epoch(2026, 10, 29, 17, 28, 54, 964190626), WIN),
    ("window-2756 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 17, 38, 55, 387245275), POST + 300.0),
    ("skew decimal-exact +7.245275ms", POST - SCAN, 0.007245275),
    ("echo_vs_window 182.024209159", ECHO - WIN, 182.024209159),
    ("dd#329 = 600.423000000", SCAN - C2754_SCAN, 600.423),
    ("INTERVAL#329 = 770.380", SCAN - TRIG, 770.380),
    ("LAG#329 = INTERVAL + dd - dd#328 = +809.818", (SCAN - TRIG) + (SCAN - C2754_SCAN) - 560.985, 809.818),
    ("LATE#329 = trigger - window-open = -469.964190626", TRIG - WIN, -469.964190626),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2755"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2755"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2756 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8788", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2755_next_bullet", last_nonempty.startswith("- Next: the c2755 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2755",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2755")]) == 0,
      f"c2755 substring mentions={wl.count('c2755')} (expect 7)")
c2755_lines = {i + 1: l.count("c2755") for i, l in enumerate(wl.splitlines()) if "c2755" in l}
guard("c2755_mention_census_pre", wl.count("c2755") == 7 and c2755_lines == {8776: 1, 8780: 2, 8788: 4},
      f"per-line={c2755_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==432", tid_pre == 432, f"got={tid_pre}")
guard("anchor_nogold_pre==365", gold_pre == 365, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2754_pre = wl.count("c2754")
c2753_pre = wl.count("c2753")
c2752_pre = wl.count("c2752")

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
guard("post_worklog_lines==8800", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2756_next_bullet", last2.startswith("- Next: the c2756 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==433", tid_post == 433, f"got={tid_post}")
guard("anchor_nogold_post==366", gold_post == 366, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2755_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2755")]) == 1)
expect_c2755_mentions = 7 + block.count("c2755")
guard("c2755_mention_accounting", wl2.count("c2755") == expect_c2755_mentions,
      f"pre=7 + block={block.count('c2755')} -> expect={expect_c2755_mentions} got={wl2.count('c2755')}")
expect_c2754_mentions = c2754_pre + block.count("c2754")
guard("c2754_mention_accounting", wl2.count("c2754") == expect_c2754_mentions,
      f"pre={c2754_pre} + block={block.count('c2754')} -> expect={expect_c2754_mentions} got={wl2.count('c2754')}")
expect_c2753_mentions = c2753_pre + block.count("c2753")
guard("c2753_mention_accounting", wl2.count("c2753") == expect_c2753_mentions,
      f"pre={c2753_pre} + block={block.count('c2753')} -> expect={expect_c2753_mentions} got={wl2.count('c2753')}")
expect_c2752_mentions = c2752_pre + block.count("c2752")
guard("c2752_mention_accounting", wl2.count("c2752") == expect_c2752_mentions,
      f"pre={c2752_pre} + block={block.count('c2752')} -> expect={expect_c2752_mentions} got={wl2.count('c2752')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print(f"WORKLOG_APPEND_GREEN: 8788 -> 8800 (+12), c2755 entry + DRIFT-#49 pass-4 block landed (first-pass clean, {n_guards}/{n_guards} guards)")
