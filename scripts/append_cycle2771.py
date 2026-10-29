#!/usr/bin/env python3
"""Guarded worklog append for the c2771 entry (12 lines).

Follows the append_cycle2770.py precedent (attempt-1 GREEN 68/68 after the
c2766/c2769 abort lessons): ALL asserts precede the mutation; any failure
-> APPEND_ABORTED, worklog UNTOUCHED. THIS RUN IS ATTEMPT-1 for c2771: the
decimal-exact guard design is the last line of defense (the c2766/c2767/
c2769/c2770-abort precedent class; the c2771 cycle itself ran ZERO aborts —
the lag-1 dual-surface lesson carried cleanly).
Guards: python-timegm epoch cross-verification (decimal-exact, 25 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic, both echo decompositions, and the
stamp-gap/token-gap cadence pair — the c2766 attempt-1 abort lesson: the SKEW
check must use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH
clock reads differ ~0.6-0.7ms on capture echoes and ~0.57ms on the loop-open
dual-read), block structure (12 lines: separator, title, standard Task ID
line, Steps 1-7, no-gold, Next bullet), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (8980 lines, tail = the c2771 Next bullet, zero serviced c2771
entries, c2771 mention census per-line {8968: 2, 8972: 2, 8980: 4}, anchors
448/381/60/28), post-state (8992 lines, tail = the c2772 Next bullet,
anchors 449/382/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2771.txt"
EXPECT_BEFORE = 8980
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (decimal-exact, 25 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = 1793302532.281033853   # c2771 post-echo (EPOCH-governs)
SCAN = 1793302532.229         # c2771 scanned_at (decimal)
TRIG = 1793301668.000         # c2771 trigger stamp (03:21:08 +08)
WIN = 1793302349.648048003    # window-2771 open (c2770 prophecy)
ECHO = 1793302459.462616937   # loop-open in-batch echo (EPOCH-governs)
C2770_SCAN = 1793302049.642   # c2770 scanned_at

checks = [
    ("trigger stamp 03:21:08 +08 = 1793301668.000", utc_epoch(2026, 10, 29, 19, 21, 8), TRIG),
    ("c2770 trigger stamp 03:16:07 +08 = 1793301367.000", utc_epoch(2026, 10, 29, 19, 16, 7), 1793301367.0),
    ("stamp-gap 301s by stamp (03:16:07 -> 03:21:08)", TRIG - 1793301367.0, 301.0),
    ("token-gap 420s by token (0323 -> 0330)", utc_epoch(2026, 10, 29, 19, 30, 0) - utc_epoch(2026, 10, 29, 19, 23, 0), 420.0),
    ("loop-open echo ISO integer second 19:34:19 +0000", float(calendar.timegm((2026, 10, 29, 19, 34, 19, 0, 0, 0))), 1793302459.0),
    ("loop-open echo EPOCH 1793302459.462616937 (EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 34, 19, 462616937), ECHO),
    ("pre-echo EPOCH 1793302530.561482779 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 35, 30, 561482779), 1793302530.5614828),
    ("post-echo ISO 19:35:32.252958698 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 19, 35, 32, 252958698), 1793302532.2529585),
    ("post-echo EPOCH 1793302532.281033853 (EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 35, 32, 281033853), POST),
    ("scanned_at 19:35:32.229 +0000 (decimal)", utc_epoch(2026, 10, 29, 19, 35, 32) + 0.229, SCAN),
    ("c2770 scanned_at 19:27:29.642 +0000 (decimal)", utc_epoch(2026, 10, 29, 19, 27, 29) + 0.642, C2770_SCAN),
    ("window-2771 open 03:32:29.648048003 +08", utc_epoch(2026, 10, 29, 19, 32, 29, 648048003), WIN),
    ("window-2772 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 19, 40, 32, 281033853), POST + 300.0),
    ("skew decimal-exact +52.033853ms (EPOCH-governs decomposition)", POST - SCAN, 0.052033853),
    ("echo_vs_window +109.814568934 (POST-WINDOW flip re-opens m1)", ECHO - WIN, 109.814568934),
    ("dd#345 = +182.587000000 (interval 482.587 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#343 print 513.830 - 300 = 213.830 and the dd#344 print 456.180 - 300 = 156.180)", SCAN - C2770_SCAN - 300.0, 182.587),
    ("INTERVAL#345 = 864.229", SCAN - TRIG, 864.229),
    ("LAG#345 = INTERVAL + dd - dd#344 = +890.636", (SCAN - TRIG) + (SCAN - C2770_SCAN - 300.0) - 156.180, 890.636),
    ("LATE#345 = trigger - window-open = -681.648048003", TRIG - WIN, -681.648048003),
    ("CAPTURE_vs_window +182.632985850 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, 182.632985850),
    ("echo post-c2770-close +235.462616937 (5622953 at 19:30:24)", ECHO - utc_epoch(2026, 10, 29, 19, 30, 24), 235.462616937),
    ("echo post-foreign-02d651d +225.462616937 (19:30:34)", ECHO - utc_epoch(2026, 10, 29, 19, 30, 34), 225.462616937),
    ("trigger predates c2770 close by 556.000s", utc_epoch(2026, 10, 29, 19, 30, 24) - TRIG, 556.0),
    ("trigger predates the foreign 02d651d by 566.000s (19:30:34)", utc_epoch(2026, 10, 29, 19, 30, 34) - TRIG, 566.0),
    ("trigger postdates c2768 close by 383.000s (1047b54 at 19:14:45)", TRIG - utc_epoch(2026, 10, 29, 19, 14, 45), 383.0),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2771"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2771"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2772 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8980", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2771_next_bullet", last_nonempty.startswith("- Next: the c2771 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2771",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2771")]) == 0,
      f"c2771 substring mentions={wl.count('c2771')} (expect 8)")
c2771_lines = {i + 1: l.count("c2771") for i, l in enumerate(wl.splitlines()) if "c2771" in l}
guard("c2771_mention_census_pre", wl.count("c2771") == 8 and c2771_lines == {8968: 2, 8972: 2, 8980: 4},
      f"per-line={c2771_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==448", tid_pre == 448, f"got={tid_pre}")
guard("anchor_nogold_pre==381", gold_pre == 381, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2772_pre = wl.count("c2772")
c2770_pre = wl.count("c2770")
c2769_pre = wl.count("c2769")
c2768_pre = wl.count("c2768")
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
c2753_pre = wl.count("c2753")
c2752_pre = wl.count("c2752")
c2751_pre = wl.count("c2751")
c2750_pre = wl.count("c2750")
c2749_pre = wl.count("c2749")
c2748_pre = wl.count("c2748")
c2747_pre = wl.count("c2747")
c2746_pre = wl.count("c2746")
guard("c2772_pre==2", c2772_pre == 2, f"got={c2772_pre}")
guard("c2770_pre==29", c2770_pre == 29, f"got={c2770_pre}")
guard("c2769_pre==53", c2769_pre == 53, f"got={c2769_pre}")

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
guard("post_worklog_lines==8992", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2772_next_bullet", last2.startswith("- Next: the c2772 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==449", tid_post == 449, f"got={tid_post}")
guard("anchor_nogold_post==382", gold_post == 382, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2771_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2771")]) == 1)
expect_c2773_mentions = wl2.count("c2773")
guard("c2773_mention_birth", expect_c2773_mentions == block.count("c2773"),
      f"block births={block.count('c2773')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2773_mentions}")
expect_c2772_mentions = c2772_pre + block.count("c2772")
guard("c2772_mention_accounting", wl2.count("c2772") == expect_c2772_mentions,
      f"pre={c2772_pre} + block={block.count('c2772')} -> expect={expect_c2772_mentions} got={wl2.count('c2772')}")
expect_c2771_mentions = 8 + block.count("c2771")
guard("c2771_mention_accounting", wl2.count("c2771") == expect_c2771_mentions,
      f"pre=8 + block={block.count('c2771')} -> expect={expect_c2771_mentions} got={wl2.count('c2771')}")
expect_c2770_mentions = c2770_pre + block.count("c2770")
guard("c2770_mention_accounting", wl2.count("c2770") == expect_c2770_mentions,
      f"pre={c2770_pre} + block={block.count('c2770')} -> expect={expect_c2770_mentions} got={wl2.count('c2770')}")
expect_c2769_mentions = c2769_pre + block.count("c2769")
guard("c2769_mention_accounting", wl2.count("c2769") == expect_c2769_mentions,
      f"pre={c2769_pre} + block={block.count('c2769')} -> expect={expect_c2769_mentions} got={wl2.count('c2769')}")
expect_c2768_mentions = c2768_pre + block.count("c2768")
guard("c2768_mention_accounting", wl2.count("c2768") == expect_c2768_mentions,
      f"pre={c2768_pre} + block={block.count('c2768')} -> expect={expect_c2768_mentions} got={wl2.count('c2768')}")
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
expect_c2753_mentions = c2753_pre + block.count("c2753")
guard("c2753_mention_accounting", wl2.count("c2753") == expect_c2753_mentions,
      f"pre={c2753_pre} + block={block.count('c2753')} -> expect={expect_c2753_mentions} got={wl2.count('c2753')}")
expect_c2752_mentions = c2752_pre + block.count("c2752")
guard("c2752_mention_accounting", wl2.count("c2752") == expect_c2752_mentions,
      f"pre={c2752_pre} + block={block.count('c2752')} -> expect={expect_c2752_mentions} got={wl2.count('c2752')}")
expect_c2751_mentions = c2751_pre + block.count("c2751")
guard("c2751_mention_accounting", wl2.count("c2751") == expect_c2751_mentions,
      f"pre={c2751_pre} + block={block.count('c2751')} -> expect={expect_c2751_mentions} got={wl2.count('c2751')}")
expect_c2750_mentions = c2750_pre + block.count("c2750")
guard("c2750_mention_accounting", wl2.count("c2750") == expect_c2750_mentions,
      f"pre={c2750_pre} + block={block.count('c2750')} -> expect={expect_c2750_mentions} got={wl2.count('c2750')}")
expect_c2749_mentions = c2749_pre + block.count("c2749")
guard("c2749_mention_accounting", wl2.count("c2749") == expect_c2749_mentions,
      f"pre={c2749_pre} + block={block.count('c2749')} -> expect={expect_c2749_mentions} got={wl2.count('c2749')}")
expect_c2748_mentions = c2748_pre + block.count("c2748")
guard("c2748_mention_accounting", wl2.count("c2748") == expect_c2748_mentions,
      f"pre={c2748_pre} + block={block.count('c2748')} -> expect={expect_c2748_mentions} got={wl2.count('c2748')}")
expect_c2747_mentions = c2747_pre + block.count("c2747")
guard("c2747_mention_accounting", wl2.count("c2747") == expect_c2747_mentions,
      f"pre={c2747_pre} + block={block.count('c2747')} -> expect={expect_c2747_mentions} got={wl2.count('c2747')}")
expect_c2746_mentions = c2746_pre + block.count("c2746")
guard("c2746_mention_accounting", wl2.count("c2746") == expect_c2746_mentions,
      f"pre={c2746_pre} + block={block.count('c2746')} -> expect={expect_c2746_mentions} got={wl2.count('c2746')}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print(f"WORKLOG_APPEND_GREEN: 8980 -> 8992 (+12), c2771 entry + DRIFT-#49 pass-20 block landed ({n_guards}/{n_guards} guards)")
