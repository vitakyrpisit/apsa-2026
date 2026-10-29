#!/usr/bin/env python3
"""Guarded worklog append for the c2759 entry (12 lines).

Follows the append_cycle2758.py (first-pass GREEN) precedent: ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 15 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and the dual echo decomposition),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8836 lines,
tail = the c2759 Next bullet, zero serviced c2759 entries, c2759 mention
census per-line {8824: 1, 8828: 2, 8836: 4}, anchors 436/369/60/28), post-state
(8848 lines, tail = the c2760 Next bullet, anchors 437/370/60/28). Zero
mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2759.txt"
EXPECT_BEFORE = 8836
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


POST = 1793296785.198174593   # c2759 post-echo (EPOCH-governs)
SCAN = 1793296785.192         # c2759 scanned_at (decimal)
TRIG = 1793296265.000         # c2759 trigger stamp
WIN = 1793296822.769039789    # window-2759 open (c2758 prophecy)
ECHO = 1793296705.948594770   # loop-open in-batch echo (EPOCH-governs)
C2758_SCAN = 1793296522.763   # c2758 scanned_at

checks = [
    ("trigger stamp 01:51:05 +08 = 1793296265.000", utc_epoch(2026, 10, 29, 17, 51, 5), TRIG),
    ("loop-open echo ISO 17:58:25.947860871 +0000", utc_epoch(2026, 10, 29, 17, 58, 25, 947860871), 1793296705.947860871),
    ("loop-open echo EPOCH 1793296705.948594770 (EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 58, 25, 948594770), ECHO),
    ("pre-echo EPOCH 1793296783.568103048 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 59, 43, 568103048), 1793296783.568103048),
    ("post-echo 17:59:45.198174593 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 17, 59, 45, 198174593), POST),
    ("scanned_at 17:59:45.192 +0000 (decimal)", utc_epoch(2026, 10, 29, 17, 59, 45) + 0.192, SCAN),
    ("c2758 scanned_at 17:55:22.763 +0000 (decimal)", utc_epoch(2026, 10, 29, 17, 55, 22) + 0.763, C2758_SCAN),
    ("window-2759 open 02:00:22.769039789 +08", utc_epoch(2026, 10, 29, 18, 0, 22, 769039789), WIN),
    ("window-2760 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 18, 4, 45, 198174593), POST + 300.0),
    ("skew decimal-exact +6.174593ms", POST - SCAN, 0.006174593),
    ("echo_vs_window -116.820445019 (PRE-WINDOW class, 2nd consecutive)", ECHO - WIN, -116.820445019),
    ("dd#333 = 262.429000000", SCAN - C2758_SCAN, 262.429),
    ("INTERVAL#333 = 520.192", SCAN - TRIG, 520.192),
    ("LAG#333 = INTERVAL + dd - dd#332 = +449.056", (SCAN - TRIG) + (SCAN - C2758_SCAN) - 333.565, 449.056),
    ("LATE#333 = trigger - window-open = -557.769039789", TRIG - WIN, -557.769039789),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2759"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2759"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2760 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8836", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2759_next_bullet", last_nonempty.startswith("- Next: the c2759 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2759",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2759")]) == 0,
      f"c2759 substring mentions={wl.count('c2759')} (expect 7)")
c2759_lines = {i + 1: l.count("c2759") for i, l in enumerate(wl.splitlines()) if "c2759" in l}
guard("c2759_mention_census_pre", wl.count("c2759") == 7 and c2759_lines == {8824: 1, 8828: 2, 8836: 4},
      f"per-line={c2759_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==436", tid_pre == 436, f"got={tid_pre}")
guard("anchor_nogold_pre==369", gold_pre == 369, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
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
guard("post_worklog_lines==8848", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2760_next_bullet", last2.startswith("- Next: the c2760 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==437", tid_post == 437, f"got={tid_post}")
guard("anchor_nogold_post==370", gold_post == 370, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2759_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2759")]) == 1)
expect_c2759_mentions = 7 + block.count("c2759")
guard("c2759_mention_accounting", wl2.count("c2759") == expect_c2759_mentions,
      f"pre=7 + block={block.count('c2759')} -> expect={expect_c2759_mentions} got={wl2.count('c2759')}")
expect_c2760_mentions = 1 + block.count("c2760")
guard("c2760_mention_accounting", wl2.count("c2760") == expect_c2760_mentions,
      f"pre=1 + block={block.count('c2760')} -> expect={expect_c2760_mentions} got={wl2.count('c2760')}")
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
print(f"WORKLOG_APPEND_GREEN: 8836 -> 8848 (+12), c2759 entry + DRIFT-#49 pass-8 block landed (first-pass clean, {n_guards}/{n_guards} guards)")
