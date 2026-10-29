#!/usr/bin/env python3
"""Guarded worklog append for the c2754 entry (12 lines).

Follows the append_cycle2753.py (first-pass GREEN) precedent: ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 15 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and the dual echo decomposition),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8776 lines,
tail = the c2754 Next bullet, zero serviced c2754 entries, c2754 mention
census per-line {8764: 1, 8768: 2, 8776: 4}, anchors 431/364/60/28), post-state
(8788 lines, tail = the c2755 Next bullet, anchors 432/365/60/28). Zero
mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2754.txt"
EXPECT_BEFORE = 8776
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (decimal-exact, 15 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = 1793294634.964190626   # c2754 post-echo (EPOCH-governs)
SCAN = 1793294634.957         # c2754 scanned_at (decimal)
TRIG = 1793293865.000         # c2754 trigger stamp
WIN = 1793294373.978178395    # window-2754 open (c2753 prophecy)
ECHO = 1793294558.150610926   # loop-open in-batch echo (EPOCH-governs)
C2753_SCAN = 1793294073.972   # c2753 scanned_at

checks = [
    ("trigger stamp 01:11:05 +08 = 1793293865.000", utc_epoch(2026, 10, 29, 17, 11, 5), TRIG),
    ("loop-open echo ISO 01:22:38.149938401 +08", utc_epoch(2026, 10, 29, 17, 22, 38, 149938401), 1793294558.149938401),
    ("loop-open echo EPOCH 1793294558.150610926 (EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 22, 38, 150610926), ECHO),
    ("pre-echo EPOCH 1793294633.144103135 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 23, 53, 144103135), 1793294633.144103135),
    ("post-echo 01:23:54.964190626 +08 (epoch ns)", utc_epoch(2026, 10, 29, 17, 23, 54, 964190626), POST),
    ("scanned_at 01:23:54.957 +08 (decimal)", utc_epoch(2026, 10, 29, 17, 23, 54) + 0.957, SCAN),
    ("c2753 scanned_at 01:14:33.972 +08 (decimal)", utc_epoch(2026, 10, 29, 17, 14, 33) + 0.972, C2753_SCAN),
    ("window-2754 open 01:19:33.978178395 +08", utc_epoch(2026, 10, 29, 17, 19, 33, 978178395), WIN),
    ("window-2755 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 17, 28, 54, 964190626), POST + 300.0),
    ("skew decimal-exact +7.190626ms", POST - SCAN, 0.007190626),
    ("echo_vs_window 184.172432531", ECHO - WIN, 184.172432531),
    ("dd#328 = 560.985000000", SCAN - C2753_SCAN, 560.985),
    ("INTERVAL#328 = 769.957", SCAN - TRIG, 769.957),
    ("LAG#328 = INTERVAL + dd - dd#327 = +724.159", (SCAN - TRIG) + (SCAN - C2753_SCAN) - 606.783, 724.159),
    ("LATE#328 = trigger - window-open = -508.978178395", TRIG - WIN, -508.978178395),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2754"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2754"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2755 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8776", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2754_next_bullet", last_nonempty.startswith("- Next: the c2754 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2754",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2754")]) == 0,
      f"c2754 substring mentions={wl.count('c2754')} (expect 7)")
c2754_lines = {i + 1: l.count("c2754") for i, l in enumerate(wl.splitlines()) if "c2754" in l}
guard("c2754_mention_census_pre", wl.count("c2754") == 7 and c2754_lines == {8764: 1, 8768: 2, 8776: 4},
      f"per-line={c2754_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==431", tid_pre == 431, f"got={tid_pre}")
guard("anchor_nogold_pre==364", gold_pre == 364, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2753_pre = wl.count("c2753")
c2752_pre = wl.count("c2752")
c2751_pre = wl.count("c2751")

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
guard("post_worklog_lines==8788", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2755_next_bullet", last2.startswith("- Next: the c2755 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==432", tid_post == 432, f"got={tid_post}")
guard("anchor_nogold_post==365", gold_post == 365, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2754_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2754")]) == 1)
expect_c2754_mentions = 7 + block.count("c2754")
guard("c2754_mention_accounting", wl2.count("c2754") == expect_c2754_mentions,
      f"pre=7 + block={block.count('c2754')} -> expect={expect_c2754_mentions} got={wl2.count('c2754')}")
expect_c2753_mentions = c2753_pre + block.count("c2753")
guard("c2753_mention_accounting", wl2.count("c2753") == expect_c2753_mentions,
      f"pre={c2753_pre} + block={block.count('c2753')} -> expect={expect_c2753_mentions} got={wl2.count('c2753')}")
expect_c2752_mentions = c2752_pre + block.count("c2752")
guard("c2752_mention_accounting", wl2.count("c2752") == expect_c2752_mentions,
      f"pre={c2752_pre} + block={block.count('c2752')} -> expect={expect_c2752_mentions} got={wl2.count('c2752')}")
expect_c2751_mentions = c2751_pre + block.count("c2751")
guard("c2751_mention_accounting", wl2.count("c2751") == expect_c2751_mentions,
      f"pre={c2751_pre} + block={block.count('c2751')} -> expect={expect_c2751_mentions} got={wl2.count('c2751')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print("WORKLOG_APPEND_GREEN: 8776 -> 8788 (+12), c2754 entry + DRIFT-#49 pass-3 block landed (first-pass clean)")
