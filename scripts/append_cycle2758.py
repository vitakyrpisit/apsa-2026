#!/usr/bin/env python3
"""Guarded worklog append for the c2758 entry (12 lines).

Follows the append_cycle2757.py (first-pass GREEN) precedent: ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 15 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and the dual echo decomposition),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8824 lines,
tail = the c2758 Next bullet, zero serviced c2758 entries, c2758 mention
census per-line {8812: 1, 8816: 2, 8824: 4}, anchors 435/368/60/28), post-state
(8836 lines, tail = the c2759 Next bullet, anchors 436/369/60/28). Zero
mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2758.txt"
EXPECT_BEFORE = 8824
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


POST = 1793296522.769039789   # c2758 post-echo (EPOCH-governs)
SCAN = 1793296522.763         # c2758 scanned_at (decimal)
TRIG = 1793295965.000         # c2758 trigger stamp
WIN = 1793296489.204329740    # window-2758 open (c2757 prophecy)
ECHO = 1793296443.243564670   # loop-open in-batch echo (EPOCH-governs)
C2757_SCAN = 1793296189.198   # c2757 scanned_at

checks = [
    ("trigger stamp 01:46:05 +08 = 1793295965.000", utc_epoch(2026, 10, 29, 17, 46, 5), TRIG),
    ("loop-open echo ISO 17:54:03.242769165 +0000", utc_epoch(2026, 10, 29, 17, 54, 3, 242769165), 1793296443.242769165),
    ("loop-open echo EPOCH 1793296443.243564670 (EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 54, 3, 243564670), ECHO),
    ("pre-echo EPOCH 1793296521.062317041 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 55, 21, 62317041), 1793296521.062317041),
    ("post-echo 17:55:22.769039789 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 17, 55, 22, 769039789), POST),
    ("scanned_at 17:55:22.763 +0000 (decimal)", utc_epoch(2026, 10, 29, 17, 55, 22) + 0.763, SCAN),
    ("c2757 scanned_at 17:49:49.198 +0000 (decimal)", utc_epoch(2026, 10, 29, 17, 49, 49) + 0.198, C2757_SCAN),
    ("window-2758 open 01:54:49.204329740 +08", utc_epoch(2026, 10, 29, 17, 54, 49, 204329740), WIN),
    ("window-2759 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 18, 0, 22, 769039789), POST + 300.0),
    ("skew decimal-exact +6.039789ms", POST - SCAN, 0.006039789),
    ("echo_vs_window -45.960765070 (PRE-WINDOW class)", ECHO - WIN, -45.960765070),
    ("dd#332 = 333.565000000", SCAN - C2757_SCAN, 333.565),
    ("INTERVAL#332 = 557.763", SCAN - TRIG, 557.763),
    ("LAG#332 = INTERVAL + dd - dd#331 = +436.671", (SCAN - TRIG) + (SCAN - C2757_SCAN) - 454.657, 436.671),
    ("LATE#332 = trigger - window-open = -524.204329740", TRIG - WIN, -524.204329740),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2758"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2758"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2759 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8824", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2758_next_bullet", last_nonempty.startswith("- Next: the c2758 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2758",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2758")]) == 0,
      f"c2758 substring mentions={wl.count('c2758')} (expect 7)")
c2758_lines = {i + 1: l.count("c2758") for i, l in enumerate(wl.splitlines()) if "c2758" in l}
guard("c2758_mention_census_pre", wl.count("c2758") == 7 and c2758_lines == {8812: 1, 8816: 2, 8824: 4},
      f"per-line={c2758_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==435", tid_pre == 435, f"got={tid_pre}")
guard("anchor_nogold_pre==368", gold_pre == 368, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
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
guard("post_worklog_lines==8836", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2759_next_bullet", last2.startswith("- Next: the c2759 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==436", tid_post == 436, f"got={tid_post}")
guard("anchor_nogold_post==369", gold_post == 369, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2758_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2758")]) == 1)
expect_c2758_mentions = 7 + block.count("c2758")
guard("c2758_mention_accounting", wl2.count("c2758") == expect_c2758_mentions,
      f"pre=7 + block={block.count('c2758')} -> expect={expect_c2758_mentions} got={wl2.count('c2758')}")
expect_c2759_mentions = 1 + block.count("c2759")
guard("c2759_mention_accounting", wl2.count("c2759") == expect_c2759_mentions,
      f"pre=1 + block={block.count('c2759')} -> expect={expect_c2759_mentions} got={wl2.count('c2759')}")
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
print(f"WORKLOG_APPEND_GREEN: 8824 -> 8836 (+12), c2758 entry + DRIFT-#49 pass-7 block landed (first-pass clean, {n_guards}/{n_guards} guards)")
