#!/usr/bin/env python3
"""Guarded worklog append for the c2756 entry (12 lines).

Follows the append_cycle2755.py (first-pass GREEN) precedent: ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 15 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and the dual echo decomposition),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8800 lines,
tail = the c2756 Next bullet, zero serviced c2756 entries, c2756 mention
census per-line {8788: 1, 8792: 2, 8800: 4}, anchors 433/366/60/28), post-state
(8812 lines, tail = the c2757 Next bullet, anchors 434/367/60/28). Zero
mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2756.txt"
EXPECT_BEFORE = 8800
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


POST = 1793295734.547156243   # c2756 post-echo (EPOCH-governs)
SCAN = 1793295734.541         # c2756 scanned_at (decimal)
TRIG = 1793295065.000         # c2756 trigger stamp
WIN = 1793295535.387245275    # window-2756 open (c2755 prophecy)
ECHO = 1793295603.929118370   # loop-open in-batch echo (EPOCH-governs)
C2755_SCAN = 1793295235.380   # c2755 scanned_at

checks = [
    ("trigger stamp 01:31:05 +08 = 1793295065.000", utc_epoch(2026, 10, 29, 17, 31, 5), TRIG),
    ("loop-open echo ISO 17:40:03.928455244 +0000", utc_epoch(2026, 10, 29, 17, 40, 3, 928455244), 1793295603.928455244),
    ("loop-open echo EPOCH 1793295603.929118370 (EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 40, 3, 929118370), ECHO),
    ("pre-echo EPOCH 1793295732.922410604 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 42, 12, 922410604), 1793295732.922410604),
    ("post-echo 17:42:14.547156243 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 17, 42, 14, 547156243), POST),
    ("scanned_at 17:42:14.541 +0000 (decimal)", utc_epoch(2026, 10, 29, 17, 42, 14) + 0.541, SCAN),
    ("c2755 scanned_at 17:33:55.380 +0000 (decimal)", utc_epoch(2026, 10, 29, 17, 33, 55) + 0.380, C2755_SCAN),
    ("window-2756 open 01:38:55.387245275 +08", utc_epoch(2026, 10, 29, 17, 38, 55, 387245275), WIN),
    ("window-2757 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 17, 47, 14, 547156243), POST + 300.0),
    ("skew decimal-exact +6.156243ms", POST - SCAN, 0.006156243),
    ("echo_vs_window 68.541873095", ECHO - WIN, 68.541873095),
    ("dd#330 = 499.161000000", SCAN - C2755_SCAN, 499.161),
    ("INTERVAL#330 = 669.541", SCAN - TRIG, 669.541),
    ("LAG#330 = INTERVAL + dd - dd#329 = +568.279", (SCAN - TRIG) + (SCAN - C2755_SCAN) - 600.423, 568.279),
    ("LATE#330 = trigger - window-open = -470.387245275", TRIG - WIN, -470.387245275),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2756"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2756"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2757 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8800", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2756_next_bullet", last_nonempty.startswith("- Next: the c2756 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2756",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2756")]) == 0,
      f"c2756 substring mentions={wl.count('c2756')} (expect 7)")
c2756_lines = {i + 1: l.count("c2756") for i, l in enumerate(wl.splitlines()) if "c2756" in l}
guard("c2756_mention_census_pre", wl.count("c2756") == 7 and c2756_lines == {8788: 1, 8792: 2, 8800: 4},
      f"per-line={c2756_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==433", tid_pre == 433, f"got={tid_pre}")
guard("anchor_nogold_pre==366", gold_pre == 366, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2755_pre = wl.count("c2755")
c2754_pre = wl.count("c2754")
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
guard("post_worklog_lines==8812", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2757_next_bullet", last2.startswith("- Next: the c2757 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==434", tid_post == 434, f"got={tid_post}")
guard("anchor_nogold_post==367", gold_post == 367, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2756_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2756")]) == 1)
expect_c2756_mentions = 7 + block.count("c2756")
guard("c2756_mention_accounting", wl2.count("c2756") == expect_c2756_mentions,
      f"pre=7 + block={block.count('c2756')} -> expect={expect_c2756_mentions} got={wl2.count('c2756')}")
expect_c2755_mentions = c2755_pre + block.count("c2755")
guard("c2755_mention_accounting", wl2.count("c2755") == expect_c2755_mentions,
      f"pre={c2755_pre} + block={block.count('c2755')} -> expect={expect_c2755_mentions} got={wl2.count('c2755')}")
expect_c2754_mentions = c2754_pre + block.count("c2754")
guard("c2754_mention_accounting", wl2.count("c2754") == expect_c2754_mentions,
      f"pre={c2754_pre} + block={block.count('c2754')} -> expect={expect_c2754_mentions} got={wl2.count('c2754')}")
expect_c2752_mentions = c2752_pre + block.count("c2752")
guard("c2752_mention_accounting", wl2.count("c2752") == expect_c2752_mentions,
      f"pre={c2752_pre} + block={block.count('c2752')} -> expect={expect_c2752_mentions} got={wl2.count('c2752')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print(f"WORKLOG_APPEND_GREEN: 8800 -> 8812 (+12), c2756 entry + DRIFT-#49 pass-5 block landed (first-pass clean, {n_guards}/{n_guards} guards)")
