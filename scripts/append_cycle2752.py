#!/usr/bin/env python3
"""Guarded worklog append for the c2752 entry (12 lines).

Follows the append_cycle2751.py (first-pass GREEN) precedent: ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 14 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
zero adds to the two standing post-#6/post-#15 anchor series (OCCURRENCE
counting — the standing method), pre-state (8752 lines, tail = the c2752 Next
bullet, zero serviced c2752 entries, c2752 mention census per-line
{8740: 1, 8752: 4}, anchors 429/362/60/28), post-state (8764 lines, tail =
the c2753 Next bullet, anchors 430/363/60/28). Zero mid-line writes (append
at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2752.txt"
EXPECT_BEFORE = 8752
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (decimal-exact, 14 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = 1793293467.195530263   # c2752 post-echo (EPOCH-governs)
SCAN = 1793293467.189         # c2752 scanned_at (decimal)
TRIG = 1793292364.000         # c2752 trigger stamp
WIN = 1793293005.101509114    # window-2752 open (c2751 prophecy)
C2751_SCAN = 1793292705.095   # c2751 scanned_at

checks = [
    ("trigger stamp 00:46:04 +08 = 1793292364.000", utc_epoch(2026, 10, 29, 16, 46, 4), TRIG),
    ("loop-open echo ISO 01:02:33.290929194 +08", utc_epoch(2026, 10, 29, 17, 2, 33, 290929194), 1793293353.290929194),
    ("loop-open echo EPOCH 1793293353.291660232 (EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 2, 33, 291660232), 1793293353.291660232),
    ("pre-echo EPOCH 1793293465.408775120 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 17, 4, 25, 408775120), 1793293465.408775120),
    ("post-echo 01:04:27.195530263 +08 (epoch ns)", utc_epoch(2026, 10, 29, 17, 4, 27, 195530263), POST),
    ("scanned_at 01:04:27.189 +08 (decimal)", utc_epoch(2026, 10, 29, 17, 4, 27) + 0.189, SCAN),
    ("c2751 scanned_at 00:51:45.095 +08 (decimal)", utc_epoch(2026, 10, 29, 16, 51, 45) + 0.095, C2751_SCAN),
    ("window-2752 open 00:56:45.101509114 +08", utc_epoch(2026, 10, 29, 16, 56, 45, 101509114), WIN),
    ("window-2753 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 17, 9, 27, 195530263), POST + 300.0),
    ("skew decimal-exact +6.530263ms", POST - SCAN, 0.006530263),
    ("echo_vs_window 348.190151118", 1793293353.291660232 - WIN, 348.190151118),
    ("dd#326 = 762.094000000", SCAN - C2751_SCAN, 762.094),
    ("INTERVAL#326 = 1103.189", SCAN - TRIG, 1103.189),
    ("LAG#326 = INTERVAL + dd - dd#325 = +1264.885", (SCAN - TRIG) + (SCAN - C2751_SCAN) - 600.398, 1264.885),
    ("LATE#326 = trigger - window-open = -641.101509114", TRIG - WIN, -641.101509114),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2752"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2752"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2753 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8752", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2752_next_bullet", last_nonempty.startswith("- Next: the c2752 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2752",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2752")]) == 0,
      f"c2752 substring mentions={wl.count('c2752')} (expect 5)")
c2752_lines = {i + 1: l.count("c2752") for i, l in enumerate(wl.splitlines()) if "c2752" in l}
guard("c2752_mention_census_pre", wl.count("c2752") == 5 and c2752_lines == {8740: 1, 8752: 4},
      f"per-line={c2752_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==429", tid_pre == 429, f"got={tid_pre}")
guard("anchor_nogold_pre==362", gold_pre == 362, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2751_pre = wl.count("c2751")
c2750_pre = wl.count("c2750")

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
guard("post_worklog_lines==8764", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2753_next_bullet", last2.startswith("- Next: the c2753 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==430", tid_post == 430, f"got={tid_post}")
guard("anchor_nogold_post==363", gold_post == 363, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2752_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2752")]) == 1)
expect_c2752_mentions = 5 + block.count("c2752")
guard("c2752_mention_accounting", wl2.count("c2752") == expect_c2752_mentions,
      f"pre=5 + block={block.count('c2752')} -> expect={expect_c2752_mentions} got={wl2.count('c2752')}")
expect_c2751_mentions = c2751_pre + block.count("c2751")
guard("c2751_mention_accounting", wl2.count("c2751") == expect_c2751_mentions,
      f"pre={c2751_pre} + block={block.count('c2751')} -> expect={expect_c2751_mentions} got={wl2.count('c2751')}")
expect_c2750_mentions = c2750_pre + block.count("c2750")
guard("c2750_mention_accounting", wl2.count("c2750") == expect_c2750_mentions,
      f"pre={c2750_pre} + block={block.count('c2750')} -> expect={expect_c2750_mentions} got={wl2.count('c2750')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print("WORKLOG_APPEND_GREEN: 8752 -> 8764 (+12), c2752 entry + DRIFT-#49 pass-1 block landed (first-pass clean)")
