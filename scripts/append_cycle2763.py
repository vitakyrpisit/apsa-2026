#!/usr/bin/env python3
"""Guarded worklog append for the c2763 entry (12 lines).

Follows the append_cycle2762.py precedent (attempt-1 GREEN 48/48): ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 15 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and the echo decomposition),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8884 lines,
tail = the c2763 Next bullet, zero serviced c2763 entries, c2763 mention
census per-line {8872: 1, 8876: 2, 8884: 4}, anchors 440/373/60/28),
post-state (8896 lines, tail = the c2764 Next bullet, anchors 441/374/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2763.txt"
EXPECT_BEFORE = 8884
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


POST = 1793298718.590872120   # c2763 post-echo (EPOCH-governs)
SCAN = 1793298718.584         # c2763 scanned_at (decimal)
TRIG = 1793298066.000         # c2763 trigger stamp
WIN = 1793298656.687865499    # window-2763 open (c2762 prophecy)
ECHO = 1793298665.770873085   # loop-open in-batch echo (EPOCH-governs)
C2762_SCAN = 1793298356.681   # c2762 scanned_at

checks = [
    ("trigger stamp 02:21:06 +08 = 1793298066.000", utc_epoch(2026, 10, 29, 18, 21, 6), TRIG),
    ("loop-open echo ISO 18:31:05.770058172 +0000", utc_epoch(2026, 10, 29, 18, 31, 5, 770058172), 1793298665.7700582),
    ("loop-open echo EPOCH 1793298665.770873085 (EPOCH-governs)", utc_epoch(2026, 10, 29, 18, 31, 5, 770873085), ECHO),
    ("pre-echo EPOCH 1793298716.866043233 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 18, 31, 56, 866043233), 1793298716.8660433),
    ("post-echo 18:31:58.590872120 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 18, 31, 58, 590872120), POST),
    ("scanned_at 18:31:58.584 +0000 (decimal)", utc_epoch(2026, 10, 29, 18, 31, 58) + 0.584, SCAN),
    ("c2762 scanned_at 18:25:56.681 +0000 (decimal)", utc_epoch(2026, 10, 29, 18, 25, 56) + 0.681, C2762_SCAN),
    ("window-2763 open 02:30:56.687865499 +08", utc_epoch(2026, 10, 29, 18, 30, 56, 687865499), WIN),
    ("window-2764 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 18, 36, 58, 590872120), POST + 300.0),
    ("skew decimal-exact +6.872120ms", POST - SCAN, 0.00687212),
    ("echo_vs_window +9.083007586 (POST-WINDOW third)", ECHO - WIN, 9.083007586),
    ("dd#337 = 361.903000000", SCAN - C2762_SCAN, 361.903),
    ("INTERVAL#337 = 652.584", SCAN - TRIG, 652.584),
    ("LAG#337 = INTERVAL + dd - dd#336 = +519.348", (SCAN - TRIG) + (SCAN - C2762_SCAN) - 495.139, 519.348),
    ("LATE#337 = trigger - window-open = -590.687865499", TRIG - WIN, -590.687865499),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2763"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2763"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2764 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8884", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2763_next_bullet", last_nonempty.startswith("- Next: the c2763 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2763",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2763")]) == 0,
      f"c2763 substring mentions={wl.count('c2763')} (expect 7)")
c2763_lines = {i + 1: l.count("c2763") for i, l in enumerate(wl.splitlines()) if "c2763" in l}
guard("c2763_mention_census_pre", wl.count("c2763") == 7 and c2763_lines == {8872: 1, 8876: 2, 8884: 4},
      f"per-line={c2763_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==440", tid_pre == 440, f"got={tid_pre}")
guard("anchor_nogold_pre==373", gold_pre == 373, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2762_pre = wl.count("c2762")
c2761_pre = wl.count("c2761")
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
guard("post_worklog_lines==8896", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2764_next_bullet", last2.startswith("- Next: the c2764 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==441", tid_post == 441, f"got={tid_post}")
guard("anchor_nogold_post==374", gold_post == 374, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2763_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2763")]) == 1)
expect_c2763_mentions = 7 + block.count("c2763")
guard("c2763_mention_accounting", wl2.count("c2763") == expect_c2763_mentions,
      f"pre=7 + block={block.count('c2763')} -> expect={expect_c2763_mentions} got={wl2.count('c2763')}")
expect_c2764_mentions = 1 + block.count("c2764")
guard("c2764_mention_accounting", wl2.count("c2764") == expect_c2764_mentions,
      f"pre=1 + block={block.count('c2764')} -> expect={expect_c2764_mentions} got={wl2.count('c2764')}")
expect_c2762_mentions = c2762_pre + block.count("c2762")
guard("c2762_mention_accounting", wl2.count("c2762") == expect_c2762_mentions,
      f"pre={c2762_pre} + block={block.count('c2762')} -> expect={expect_c2762_mentions} got={wl2.count('c2762')}")
expect_c2761_mentions = c2761_pre + block.count("c2761")
guard("c2761_mention_accounting", wl2.count("c2761") == expect_c2761_mentions,
      f"pre={c2761_pre} + block={block.count('c2761')} -> expect={expect_c2761_mentions} got={wl2.count('c2761')}")
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
print(f"WORKLOG_APPEND_GREEN: 8884 -> 8896 (+12), c2763 entry + DRIFT-#49 pass-12 block landed ({n_guards}/{n_guards} guards)")
