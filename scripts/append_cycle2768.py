#!/usr/bin/env python3
"""Guarded worklog append for the c2768 entry (12 lines).

Follows the append_cycle2767.py precedent (attempt-2 GREEN 57/57): ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
Guards: python-timegm epoch cross-verification (decimal-exact, 17 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and both echo decompositions — the
c2766 attempt-1 abort lesson: the SKEW check must use the EPOCH-governs
print's own ns decomposition, the ISO/EPOCH clock reads differ ~0.6-0.7ms),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8944 lines,
tail = the c2768 Next bullet, zero serviced c2768 entries, c2768 mention
census per-line {8932: 1, 8936: 6, 8944: 4}, anchors 445/378/60/28),
post-state (8956 lines, tail = the c2769 Next bullet, anchors 446/379/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2768.txt"
EXPECT_BEFORE = 8944
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (decimal-exact, 17 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = 1793301079.638220192   # c2768 post-echo (EPOCH-governs)
SCAN = 1793301079.632         # c2768 scanned_at (decimal)
TRIG = 1793300468.000         # c2768 trigger stamp
WIN = 1793300766.703178724    # window-2768 open (c2767 prophecy)
ECHO = 1793301008.575190067   # loop-open in-batch echo (EPOCH-governs)
C2767_SCAN = 1793300466.697   # c2767 scanned_at

checks = [
    ("trigger stamp 03:01:08 +08 = 1793300468.000", utc_epoch(2026, 10, 29, 19, 1, 8), TRIG),
    ("loop-open echo ISO integer second 19:10:08 +0000", float(calendar.timegm((2026, 10, 29, 19, 10, 8, 0, 0, 0))), 1793301008.0),
    ("loop-open echo EPOCH 1793301008.575190067 (EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 10, 8, 575190067), ECHO),
    ("pre-echo EPOCH 1793301077.931990902 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 11, 17, 931990902), 1793301077.9319908),
    ("post-echo ISO 19:11:19.637577890 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 19, 11, 19, 637577890), 1793301079.6375778),
    ("post-echo EPOCH 1793301079.638220192 (EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 11, 19, 638220192), POST),
    ("scanned_at 19:11:19.632 +0000 (decimal)", utc_epoch(2026, 10, 29, 19, 11, 19) + 0.632, SCAN),
    ("c2767 scanned_at 19:01:06.697 +0000 (decimal)", utc_epoch(2026, 10, 29, 19, 1, 6) + 0.697, C2767_SCAN),
    ("window-2768 open 03:06:06.703178724 +08", utc_epoch(2026, 10, 29, 19, 6, 6, 703178724), WIN),
    ("window-2769 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 19, 16, 19, 638220192), POST + 300.0),
    ("skew decimal-exact +6.220192ms (EPOCH-governs decomposition)", POST - SCAN, 0.006220192),
    ("echo_vs_window +241.872011343 (POST-WINDOW extends m4)", ECHO - WIN, 241.872011343),
    ("dd#342 = +312.935000000 (interval 612.935 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson)", SCAN - C2767_SCAN - 300.0, 312.935),
    ("INTERVAL#342 = 611.632", SCAN - TRIG, 611.632),
    ("LAG#342 = INTERVAL + dd - dd#341 = +716.692", (SCAN - TRIG) + (SCAN - C2767_SCAN - 300.0) - 207.875, 716.692),
    ("LATE#342 = trigger - window-open = -298.703178724", TRIG - WIN, -298.703178724),
    ("CAPTURE_vs_window +312.935041468 (DUAL POST-WINDOW extends m4)", POST - WIN, 312.935041468),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2768"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2768"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2769 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8944", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2768_next_bullet", last_nonempty.startswith("- Next: the c2768 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2768",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2768")]) == 0,
      f"c2768 substring mentions={wl.count('c2768')} (expect 11)")
c2768_lines = {i + 1: l.count("c2768") for i, l in enumerate(wl.splitlines()) if "c2768" in l}
guard("c2768_mention_census_pre", wl.count("c2768") == 11 and c2768_lines == {8932: 1, 8936: 6, 8944: 4},
      f"per-line={c2768_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==445", tid_pre == 445, f"got={tid_pre}")
guard("anchor_nogold_pre==378", gold_pre == 378, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2767_pre = wl.count("c2767")
c2766_pre = wl.count("c2766")
c2765_pre = wl.count("c2765")
c2764_pre = wl.count("c2764")
c2763_pre = wl.count("c2763")
c2762_pre = wl.count("c2762")
c2761_pre = wl.count("c2761")
c2760_pre = wl.count("c2760")
c2759_pre = wl.count("c2759")
c2758_pre = wl.count("c2758")
c2757_pre = wl.count("c2757")
c2756_pre = wl.count("c2756")
c2755_pre = wl.count("c2755")
c2754_pre = wl.count("c2754")
c2752_pre = wl.count("c2752")
c2770_pre = wl.count("c2770")
c2769_pre = wl.count("c2769")

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
guard("post_worklog_lines==8956", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2769_next_bullet", last2.startswith("- Next: the c2769 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==446", tid_post == 446, f"got={tid_post}")
guard("anchor_nogold_post==379", gold_post == 379, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2768_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2768")]) == 1)
expect_c2770_mentions = c2770_pre + block.count("c2770")
guard("c2770_mention_accounting", wl2.count("c2770") == expect_c2770_mentions,
      f"pre={c2770_pre} + block={block.count('c2770')} -> expect={expect_c2770_mentions} got={wl2.count('c2770')}")
expect_c2769_mentions = c2769_pre + block.count("c2769")
guard("c2769_mention_accounting", wl2.count("c2769") == expect_c2769_mentions,
      f"pre={c2769_pre} + block={block.count('c2769')} -> expect={expect_c2769_mentions} got={wl2.count('c2769')}")
expect_c2768_mentions = 11 + block.count("c2768")
guard("c2768_mention_accounting", wl2.count("c2768") == expect_c2768_mentions,
      f"pre=11 + block={block.count('c2768')} -> expect={expect_c2768_mentions} got={wl2.count('c2768')}")
expect_c2767_mentions = c2767_pre + block.count("c2767")
guard("c2767_mention_accounting", wl2.count("c2767") == expect_c2767_mentions,
      f"pre={c2767_pre} + block={block.count('c2767')} -> expect={expect_c2767_mentions} got={wl2.count('c2767')}")
expect_c2766_mentions = c2766_pre + block.count("c2766")
guard("c2766_mention_accounting", wl2.count("c2766") == expect_c2766_mentions,
      f"pre={c2766_pre} + block={block.count('c2766')} -> expect={expect_c2766_mentions} got={wl2.count('c2766')}")
expect_c2765_mentions = c2765_pre + block.count("c2765")
guard("c2765_mention_accounting", wl2.count("c2765") == expect_c2765_mentions,
      f"pre={c2765_pre} + block={block.count('c2765')} -> expect={expect_c2765_mentions} got={wl2.count('c2765')}")
expect_c2764_mentions = c2764_pre + block.count("c2764")
guard("c2764_mention_accounting", wl2.count("c2764") == expect_c2764_mentions,
      f"pre={c2764_pre} + block={block.count('c2764')} -> expect={expect_c2764_mentions} got={wl2.count('c2764')}")
expect_c2763_mentions = c2763_pre + block.count("c2763")
guard("c2763_mention_accounting", wl2.count("c2763") == expect_c2763_mentions,
      f"pre={c2763_pre} + block={block.count('c2763')} -> expect={expect_c2763_mentions} got={wl2.count('c2763')}")
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
expect_c2754_mentions = c2754_pre + block.count("c2754")
guard("c2754_mention_accounting", wl2.count("c2754") == expect_c2754_mentions,
      f"pre={c2754_pre} + block={block.count('c2754')} -> expect={expect_c2754_mentions} got={wl2.count('c2754')}")
expect_c2752_mentions = c2752_pre + block.count("c2752")
guard("c2752_mention_accounting", wl2.count("c2752") == expect_c2752_mentions,
      f"pre={c2752_pre} + block={block.count('c2752')} -> expect={expect_c2752_mentions} got={wl2.count('c2752')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print(f"WORKLOG_APPEND_GREEN: 8944 -> 8956 (+12), c2768 entry + DRIFT-#49 pass-17 block landed ({n_guards}/{n_guards} guards)")
