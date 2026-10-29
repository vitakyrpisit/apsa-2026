#!/usr/bin/env python3
"""Guarded worklog append for the c2769 entry (12 lines).

Follows the append_cycle2768.py precedent (attempt-1 GREEN 58/58): ALL asserts
precede the mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED.
THIS RUN IS ATTEMPT-2: the attempt-1 pre-mutation abort caught the TRIG
stale-epoch typo (1793301168.000 vs the correct 1793300768.000) and the echo
ISO mis-render (+20s) — worklog UNTOUCHED during the abort (the c2766/c2767
abort precedent; the decimal-exact guard design is the last line of defense).
Guards: python-timegm epoch cross-verification (decimal-exact, 17 checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic and both echo decompositions — the
c2766 attempt-1 abort lesson: the SKEW check must use the EPOCH-governs
print's own ns decomposition, the ISO/EPOCH clock reads differ ~0.6-0.7ms),
block structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (8956 lines,
tail = the c2769 Next bullet, zero serviced c2769 entries, c2769 mention
census per-line {8944: 2, 8948: 2, 8956: 4}, anchors 446/379/60/28),
post-state (8968 lines, tail = the c2770 Next bullet, anchors 447/380/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2769.txt"
EXPECT_BEFORE = 8956
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


POST = 1793301593.468131508   # c2769 post-echo (EPOCH-governs)
SCAN = 1793301593.462         # c2769 scanned_at (decimal)
TRIG = 1793300768.000         # c2769 trigger stamp (03:06:08 +08; the attempt-1
                              # abort fixed the stale-epoch typo 1793301168.000)
WIN = 1793301379.638220192    # window-2769 open (c2768 prophecy)
ECHO = 1793301319.837967992   # loop-open in-batch echo (EPOCH-governs; ISO
                              # rendering 19:15:19.837967992 — the attempt-1
                              # abort fixed the +20s ISO mis-render)
C2768_SCAN = 1793301079.632   # c2768 scanned_at

checks = [
    ("trigger stamp 03:06:08 +08 = 1793300768.000", utc_epoch(2026, 10, 29, 19, 6, 8), TRIG),
    ("loop-open echo ISO integer second 19:15:19 +0000", float(calendar.timegm((2026, 10, 29, 19, 15, 19, 0, 0, 0))), 1793301319.0),
    ("loop-open echo EPOCH 1793301319.837967992 (EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 15, 19, 837967992), ECHO),
    ("pre-echo EPOCH 1793301591.782937207 (epoch ns, EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 19, 51, 782937207), 1793301591.7829372),
    ("post-echo ISO 19:19:53.467482847 +0000 (epoch ns)", utc_epoch(2026, 10, 29, 19, 19, 53, 467482847), 1793301593.4674828),
    ("post-echo EPOCH 1793301593.468131508 (EPOCH-governs)", utc_epoch(2026, 10, 29, 19, 19, 53, 468131508), POST),
    ("scanned_at 19:19:53.462 +0000 (decimal)", utc_epoch(2026, 10, 29, 19, 19, 53) + 0.462, SCAN),
    ("c2768 scanned_at 19:11:19.632 +0000 (decimal)", utc_epoch(2026, 10, 29, 19, 11, 19) + 0.632, C2768_SCAN),
    ("window-2769 open 03:16:19.638220192 +08", utc_epoch(2026, 10, 29, 19, 16, 19, 638220192), WIN),
    ("window-2770 open = post-echo + 300.000", utc_epoch(2026, 10, 29, 19, 24, 53, 468131508), POST + 300.0),
    ("skew decimal-exact +6.131508ms (EPOCH-governs decomposition)", POST - SCAN, 0.006131508),
    ("echo_vs_window -59.800252200 (PRE-WINDOW re-opens m1)", ECHO - WIN, -59.8002522),
    ("dd#343 = +213.830000000 (interval 513.830 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson)", SCAN - C2768_SCAN - 300.0, 213.830),
    ("INTERVAL#343 = 825.462", SCAN - TRIG, 825.462),
    ("LAG#343 = INTERVAL + dd - dd#342 = +726.357", (SCAN - TRIG) + (SCAN - C2768_SCAN - 300.0) - 312.935, 726.357),
    ("LATE#343 = trigger - window-open = -611.638220192", TRIG - WIN, -611.638220192),
    ("CAPTURE_vs_window +213.829911316 (POST-WINDOW; echo PRE — the split print)", POST - WIN, 213.829911316),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2769"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2769"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2770 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==8956", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2769_next_bullet", last_nonempty.startswith("- Next: the c2769 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2769",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2769")]) == 0,
      f"c2769 substring mentions={wl.count('c2769')} (expect 8)")
c2769_lines = {i + 1: l.count("c2769") for i, l in enumerate(wl.splitlines()) if "c2769" in l}
guard("c2769_mention_census_pre", wl.count("c2769") == 8 and c2769_lines == {8944: 2, 8948: 2, 8956: 4},
      f"per-line={c2769_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==446", tid_pre == 446, f"got={tid_pre}")
guard("anchor_nogold_pre==379", gold_pre == 379, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
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
c2771_pre = wl.count("c2771")
c2770_pre = wl.count("c2770")

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
guard("post_worklog_lines==8968", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2770_next_bullet", last2.startswith("- Next: the c2770 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==447", tid_post == 447, f"got={tid_post}")
guard("anchor_nogold_post==380", gold_post == 380, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2769_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2769")]) == 1)
expect_c2771_mentions = c2771_pre + block.count("c2771")
guard("c2771_mention_accounting", wl2.count("c2771") == expect_c2771_mentions,
      f"pre={c2771_pre} + block={block.count('c2771')} -> expect={expect_c2771_mentions} got={wl2.count('c2771')}")
expect_c2770_mentions = c2770_pre + block.count("c2770")
guard("c2770_mention_accounting", wl2.count("c2770") == expect_c2770_mentions,
      f"pre={c2770_pre} + block={block.count('c2770')} -> expect={expect_c2770_mentions} got={wl2.count('c2770')}")
expect_c2769_mentions = 8 + block.count("c2769")
guard("c2769_mention_accounting", wl2.count("c2769") == expect_c2769_mentions,
      f"pre=8 + block={block.count('c2769')} -> expect={expect_c2769_mentions} got={wl2.count('c2769')}")
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

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print(f"WORKLOG_APPEND_GREEN: 8956 -> 8968 (+12), c2769 entry + DRIFT-#49 pass-18 block landed ({n_guards}/{n_guards} guards)")
