#!/usr/bin/env python3
"""Guarded worklog append for the c2761 entry (12 lines).

Follows the append_cycle2760.py precedent (attempt-1 RED on a digit
transposition — the interception guard held, attempt-2 GREEN): ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 15 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and the echo decomposition),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8860 lines,
tail = the c2761 Next bullet, zero serviced c2761 entries, c2761 mention
census per-line {8848: 1, 8852: 2, 8860: 4}, anchors 438/371/60/28),
post-state (8872 lines, tail = the c2762 Next bullet, anchors 439/372/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2761.txt"
EXPECT_BEFORE = 8860
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


POST = 1793297861.548327619   # c2761 post-echo (EPOCH-governs)
SCAN = 1793297861.542         # c2761 scanned_at (decimal)
TRIG = 1793297165.000         # c2761 trigger stamp
WIN = 1793297550.198476184    # window-2761 open (c2760 prophecy)
ECHO = 1793297707.166817100   # loop-open in-batch echo (EPOCH-governs)
C2760_SCAN = 1793297250.192   # c2760 scanned_at

checks = [
    ("trigger stamp 02:06:05 +08 = 1793297165.000", utc_epoch(2026, 10, 29, 18, 6, 5), TRIG),
    ("loop-open echo ISO 18:15:07.166817100 +0000", utc_epoch(2026, 10, 29, 18, 15, 7, 166817100), 1793297707.1668171),
    ("loop-open echo EPOCH 1793297707.166817100 (EPOCH-governs)", utc_epoch(2026, 10, 29, 18, 15, 7, 166817100), ECHO),
    ("pre-echo EPOCH 1793297859.391564545 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 18, 17, 39, 391564545), 1793297859.391564545),
    ("post-echo 18:17:41.548327619 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 18, 17, 41, 548327619), POST),
    ("scanned_at 18:17:41.542 +0000 (decimal)", utc_epoch(2026, 10, 29, 18, 17, 41) + 0.542, SCAN),
    ("c2760 scanned_at 18:07:30.192 +0000 (decimal)", utc_epoch(2026, 10, 29, 18, 7, 30) + 0.192, C2760_SCAN),
    ("window-2761 open 02:12:30.198476184 +08", utc_epoch(2026, 10, 29, 18, 12, 30, 198476184), WIN),
    ("window-2762 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 18, 22, 41, 548327619), POST + 300.0),
    ("skew decimal-exact +6.327619ms", POST - SCAN, 0.006327619),
    ("echo_vs_window +156.968340916 (POST-WINDOW sign-flip)", ECHO - WIN, 156.968340916),
    ("dd#335 = 611.350000000", SCAN - C2760_SCAN, 611.35),
    ("INTERVAL#335 = 696.542", SCAN - TRIG, 696.542),
    ("LAG#335 = INTERVAL + dd - dd#334 = +842.892", (SCAN - TRIG) + (SCAN - C2760_SCAN) - 465.000, 842.892),
    ("LATE#335 = trigger - window-open = -385.198476184", TRIG - WIN, -385.198476184),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2761"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2761"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2762 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8860", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2761_next_bullet", last_nonempty.startswith("- Next: the c2761 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2761",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2761")]) == 0,
      f"c2761 substring mentions={wl.count('c2761')} (expect 7)")
c2761_lines = {i + 1: l.count("c2761") for i, l in enumerate(wl.splitlines()) if "c2761" in l}
guard("c2761_mention_census_pre", wl.count("c2761") == 7 and c2761_lines == {8848: 1, 8852: 2, 8860: 4},
      f"per-line={c2761_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==438", tid_pre == 438, f"got={tid_pre}")
guard("anchor_nogold_pre==371", gold_pre == 371, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2760_pre = wl.count("c2760")
c2759_pre = wl.count("c2759")
c2758_pre = wl.count("c2758")
c2757_pre = wl.count("c2757")
c2756_pre = wl.count("c2756")
c2755_pre = wl.count("c2755")
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
guard("post_worklog_lines==8872", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2762_next_bullet", last2.startswith("- Next: the c2762 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==439", tid_post == 439, f"got={tid_post}")
guard("anchor_nogold_post==372", gold_post == 372, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2761_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2761")]) == 1)
expect_c2761_mentions = 7 + block.count("c2761")
guard("c2761_mention_accounting", wl2.count("c2761") == expect_c2761_mentions,
      f"pre=7 + block={block.count('c2761')} -> expect={expect_c2761_mentions} got={wl2.count('c2761')}")
expect_c2762_mentions = 1 + block.count("c2762")
guard("c2762_mention_accounting", wl2.count("c2762") == expect_c2762_mentions,
      f"pre=1 + block={block.count('c2762')} -> expect={expect_c2762_mentions} got={wl2.count('c2762')}")
expect_c2760_mentions = c2760_pre + block.count("c2760")
guard("c2760_mention_accounting", wl2.count("c2760") == expect_c2760_mentions,
      f"pre={c2760_pre} + block={block.count('c2760')} -> expect={expect_c2760_mentions} got={wl2.count('c2760')}")
expect_c2759_mentions = c2759_pre + block.count("c2759")
guard("c2759_mention_accounting", wl2.count("c2759") == expect_c2759_mentions,
      f"pre={c2759_pre} + block={block.count('c2759')} -> expect={expect_c2759_mentions} got={wl2.count('c2759')}")
expect_c2758_mentions = c2758_pre + block.count("c2758")
guard("c2758_mention_accounting", wl2.count("c2758") == expect_c2758_mentions,
      f"pre={c2758_pre} + block={block.count('c2758')} -> expect={expect_c2758_mentions} got={wl2.count('c2758')}")
expect_c2757_mentions = c2757_pre + block.count("c2757")
guard("c2757_mention_accounting", wl2.count("c2757") == expect_c2757_mentions,
      f"pre={c2757_pre} + block={block.count('c2757')} -> expect={expect_c2757_mentions} got={wl2.count('c2757')}")
expect_c2756_mentions = c2756_pre + block.count("c2756")
guard("c2756_mention_accounting", wl2.count("c2756") == expect_c2756_mentions,
      f"pre={c2756_pre} + block={block.count('c2756')} -> expect={expect_c2756_mentions} got={wl2.count('c2756')}")
expect_c2755_mentions = c2755_pre + block.count("c2755")
guard("c2755_mention_accounting", wl2.count("c2755") == expect_c2755_mentions,
      f"pre={c2755_pre} + block={block.count('c2755')} -> expect={expect_c2755_mentions} got={wl2.count('c2755')}")
expect_c2752_mentions = c2752_pre + block.count("c2752")
guard("c2752_mention_accounting", wl2.count("c2752") == expect_c2752_mentions,
      f"pre={c2752_pre} + block={block.count('c2752')} -> expect={expect_c2752_mentions} got={wl2.count('c2752')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print(f"WORKLOG_APPEND_GREEN: 8860 -> 8872 (+12), c2761 entry + DRIFT-#49 pass-10 block landed ({n_guards}/{n_guards} guards)")
