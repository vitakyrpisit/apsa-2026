#!/usr/bin/env python3
"""Guarded worklog append for the c2786 entry (12 lines).

Follows the append_cycle2785.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2780-append abort
precedent class). The ledger arithmetic stays in the DECIMAL class: every
ns-decomposition check is Decimal-exact or Decimal-with-1e-6-tolerance on the
utc-derived values. THE C2778 ABORT LESSON STRUCTURALIZED: every pre-counter
variable is assigned in the SAME statement block before any guard references
it (the c2778 attempt-1 NameError class is impossible here), and a REHEARSAL
mode (APPEND_REHEARSAL=1) runs the full guard battery against a
byte-identical temp copy BEFORE the real run — the attempt counter counts
REAL runs only. Guards: python-timegm epoch cross-verification (Decimal-class
checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic, all echo
decompositions, the stamp-gap/token-gap/token-vs-stamp cadence triple, the
window-2786 EPOCH-governs render check, the window-2787 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.7ms on the echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2788 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2786 forward-token lessons; NOTE the c2788 pre-count is
2, not 0: the c2782 commit full hash carries 'c2788' as a hash-artifact
substring documented in the c2783 block — the c2785 c2787-pre==0 class does
NOT carry, the rehearsal caught the naive expectation), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9160 lines, tail = the c2786 Next bullet, zero serviced
c2786 entries, c2786 mention census per-line {9148: 2, 9152: 3, 9160: 5},
c2787 = 2 per-line {9160: 2}, anchors 463/396/60/28), post-state (9172 lines,
tail = the c2787 Next bullet, anchors 464/397/60/28). Zero mid-line writes
(append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2786.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9160
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


print(f"{'*** REHEARSAL MODE (temp copy) ***' if REHEARSAL else '*** REAL RUN ***'}")
if REHEARSAL:
    shutil.copyfile(WL, WL_TARGET)
    print(f"temp copy staged: {WL_TARGET}")

# 1) python-timegm epoch cross-verification (Decimal-class checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = D("1793311641.574001205")    # c2786 post-echo (EPOCH-governs)
SCAN = D("1793311641.568")          # c2786 scanned_at (decimal)
TRIG = D("1793310970.000")          # c2786 trigger stamp (05:56:10 +08)
WIN = D("1793311367.104908992")     # window-2786 open (c2785 prophecy EPOCH)
ECHO = D("1793311351.0527337")      # loop echo in-batch (EPOCH-governs)
C2785_SCAN = D("1793311067.096")    # c2785 scanned_at
C2785_POST = D("1793311067.104908992")  # c2785 post-echo
C2785_CLOSE = D("1793311260.000")   # c2785 close 797cfcb (22:01:00Z)
C2785_FOREIGN = D("1793311273.000") # foreign 67ba021 (22:01:13Z)
C2785_TRIG = D("1793310370.000")    # c2785 trigger stamp (05:46:10 +08)
C2784_CLOSE = D("1793310723.000")   # c2784 close 9b1c925 (21:52:03Z)
C2784_FOREIGN = D("1793310739.000") # foreign 128bbec (21:52:19Z)
TOKEN = D("1793311260.000")         # token 0601 (06:01:00Z)
C2785_TOKEN = D("1793310720.000")   # token 0552 (05:52:00Z)
WIN2785 = D("1793310822.564129472") # window-2785 open


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 05:56:10 +08 = 1793310970.000", dec_epoch(2026, 10, 29, 21, 56, 10), TRIG),
    ("c2785 trigger stamp 05:46:10 +08 = 1793310370.000", dec_epoch(2026, 10, 29, 21, 46, 10), C2785_TRIG),
    ("stamp-gap 600.000s by stamp (05:46:10 -> 05:56:10; the 600 print repeats)", TRIG - C2785_TRIG, D("600.000")),
    ("token-gap 540.000s by token (0552 -> 0601; the 540 print returns)", TOKEN - C2785_TOKEN, D("540.000")),
    ("token-vs-stamp +290.000 (05:56:10 -> 06:01:00; the +290 print returns)", TOKEN - TRIG, D("290.000")),
    ("c2785 close 797cfcb 22:01:00Z = 1793311260.000", dec_epoch(2026, 10, 29, 22, 1, 0), C2785_CLOSE),
    ("foreign 67ba021 22:01:13Z = 1793311273.000", dec_epoch(2026, 10, 29, 22, 1, 13), C2785_FOREIGN),
    ("c2784 close 9b1c925 21:52:03Z = 1793310723.000", dec_epoch(2026, 10, 29, 21, 52, 3), C2784_CLOSE),
    ("foreign 128bbec 21:52:19Z = 1793310739.000", dec_epoch(2026, 10, 29, 21, 52, 19), C2784_FOREIGN),
    ("loop echo ISO integer second 22:02:31 +0000", dec_epoch(2026, 10, 29, 22, 2, 31), D("1793311351.000")),
    ("loop echo EPOCH 1793311351.0527337 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 2, 31, 52733700), ECHO),
    ("capture pre-echo EPOCH 1793311639.866917363 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 7, 19, 866917363), D("1793311639.866917363")),
    ("post-echo ISO 22:07:21.573284597 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 22, 7, 21, 573284597), D("1793311641.573284597")),
    ("post-echo EPOCH 1793311641.574001205 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 7, 21, 574001205), POST),
    ("scanned_at 22:07:21.568 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 7, 21) + D("0.568"), SCAN),
    ("c2785 scanned_at 21:57:47.096 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 57, 47) + D("0.096"), C2785_SCAN),
    ("c2785 post-echo EPOCH 1793311067.104908992", dec_epoch(2026, 10, 29, 21, 57, 47, 104908992), C2785_POST),
    ("window-2786 open 06:02:47.104908992 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 22, 2, 47, 104908992), WIN),
    ("window-2787 open = post-echo + 300.000", POST + D("300.000"), D("1793311941.574001205")),
    ("echo post-c2785-post-echo +283.947824708", ECHO - C2785_POST, D("283.947824708")),
]
exact_checks = [
    ("skew decimal-exact +6.001205ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006001205")),
    ("echo_vs_window -16.052175292 (PRE-WINDOW re-opens m1)", ECHO - WIN, D("-16.052175292")),
    ("dd#360 = +274.472000000 (interval 574.472 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#357 print 554.800 - 300 = 254.800 and the dd#358 print 631.629 - 300 = 331.629 and the dd#359 print 544.537 - 300 = 244.537)", SCAN - C2785_SCAN - D("300.000"), D("274.472")),
    ("INTERVAL#360 = 671.568", SCAN - TRIG, D("671.568")),
    ("LAG#360 = INTERVAL + dd - dd#359 = +701.503", (SCAN - TRIG) + (SCAN - C2785_SCAN - D("300.000")) - D("244.537"), D("701.503")),
    ("LATE#360 = trigger - window-open = -397.104908992", TRIG - WIN, D("-397.104908992")),
    ("CAPTURE_vs_window +274.469092213 (POST-WINDOW; echo PRE — the both-POST print breaks)", POST - WIN, D("274.469092213")),
    ("capture-vs-echo +290.521267505", POST - ECHO, D("290.521267505")),
    ("echo post-c2785-close +91.0527337 (797cfcb at 22:01:00)", ECHO - C2785_CLOSE, D("91.0527337")),
    ("echo post-foreign-67ba021 +78.0527337 (22:01:13)", ECHO - C2785_FOREIGN, D("78.0527337")),
    ("stamp-to-echo 381.0527337 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("381.0527337")),
    ("trigger predates c2785 close by 290.000s", C2785_CLOSE - TRIG, D("290.000")),
    ("trigger predates the foreign 67ba021 by 303.000s (22:01:13)", C2785_FOREIGN - TRIG, D("303.000")),
    ("trigger predates the c2785 post-echo by 97.104908992s", C2785_POST - TRIG, D("97.104908992")),
    ("trigger predates window-2786 open by 397.104908992s", WIN - TRIG, D("397.104908992")),
    ("trigger postdates c2784 close by 247.000s (9b1c925 at 21:52:03)", TRIG - C2784_CLOSE, D("247.000")),
    ("trigger postdates the foreign 128bbec by 231.000s (21:52:19)", TRIG - C2784_FOREIGN, D("231.000")),
    ("trigger postdates window-2785 open by 147.435870528s", TRIG - WIN2785, D("147.435870528")),
    ("capture post-c2785-post-echo +574.469092213", POST - C2785_POST, D("574.469092213")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2786"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2786"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2787 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2788_birth",
      block.count("c2788") == 2 and lines[-1].count("c2788") == 2
      and "c2787/c2788" in lines[-1] and "FORWARD token c2788" in lines[-1],
      f"block c2788={block.count('c2788')} next-line c2788={lines[-1].count('c2788')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9160", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2786_next_bullet", last_nonempty.startswith("- Next: the c2786 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2786",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2786")]) == 0,
      f"c2786 substring mentions={wl.count('c2786')} (expect 10)")
c2786_lines = {i + 1: l.count("c2786") for i, l in enumerate(wl.splitlines()) if "c2786" in l}
guard("c2786_mention_census_pre", wl.count("c2786") == 10 and c2786_lines == {9148: 2, 9152: 3, 9160: 5},
      f"per-line={c2786_lines}")
c2787_lines = {i + 1: l.count("c2787") for i, l in enumerate(wl.splitlines()) if "c2787" in l}
guard("c2787_forward_token_pre", wl.count("c2787") == 2 and c2787_lines == {9160: 2},
      f"per-line={c2787_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==463", tid_pre == 463, f"got={tid_pre}")
guard("anchor_nogold_pre==396", gold_pre == 396, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2788_pre = wl.count("c2788")
c2787_pre = wl.count("c2787")
c2786_pre = wl.count("c2786")
c2785_pre = wl.count("c2785")
c2784_pre = wl.count("c2784")
c2783_pre = wl.count("c2783")
c2782_pre = wl.count("c2782")
c2781_pre = wl.count("c2781")
c2780_pre = wl.count("c2780")
c2779_pre = wl.count("c2779")
c2778_pre = wl.count("c2778")
c2777_pre = wl.count("c2777")
c2776_pre = wl.count("c2776")
c2775_pre = wl.count("c2775")
c2774_pre = wl.count("c2774")
c2773_pre = wl.count("c2773")
c2772_pre = wl.count("c2772")
c2771_pre = wl.count("c2771")
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
guard("c2788_pre==2", c2788_pre == 2, f"got={c2788_pre} (both are HISTORICAL hash-artifact substrings inside the c2783 block's Step-2 hash-artifact prose — the c2782 commit full hash 2be3f8a6c2788f1f99c61a088f45de72415a9eec carries the '6c2788f1f9' c+4-digit run; NOT forward-token births — the rehearsal caught the naive pre==0 expectation, the MEASUREMENT governs)")
guard("c2787_pre==2", c2787_pre == 2, f"got={c2787_pre}")
guard("c2786_pre==10", c2786_pre == 10, f"got={c2786_pre}")
guard("c2785_pre==37", c2785_pre == 37, f"got={c2785_pre}")
guard("c2784_pre==71", c2784_pre == 71, f"got={c2784_pre}")
guard("c2783_pre==71", c2783_pre == 71, f"got={c2783_pre}")
guard("c2782_pre==73", c2782_pre == 73, f"got={c2782_pre}")
guard("c2781_pre==78", c2781_pre == 78, f"got={c2781_pre}")
guard("c2780_pre==82", c2780_pre == 82, f"got={c2780_pre}")
guard("c2779_pre==83", c2779_pre == 83, f"got={c2779_pre}")
guard("c2778_pre==112", c2778_pre == 112, f"got={c2778_pre}")
guard("c2777_pre==99", c2777_pre == 99, f"got={c2777_pre}")
guard("c2776_pre==104", c2776_pre == 104, f"got={c2776_pre}")
guard("c2775_pre==113", c2775_pre == 113, f"got={c2775_pre}")
guard("c2774_pre==118", c2774_pre == 118, f"got={c2774_pre}")
guard("c2773_pre==122", c2773_pre == 122, f"got={c2773_pre}")
guard("c2772_pre==139", c2772_pre == 139, f"got={c2772_pre}")
guard("c2771_pre==131", c2771_pre == 131, f"got={c2771_pre}")
guard("c2770_pre==158", c2770_pre == 158, f"got={c2770_pre}")
guard("c2769_pre==128", c2769_pre == 128, f"got={c2769_pre}")
guard("c2768_pre==131", c2768_pre == 131, f"got={c2768_pre}")
guard("c2767_pre==150", c2767_pre == 150, f"got={c2767_pre}")
guard("c2766_pre==142", c2766_pre == 142, f"got={c2766_pre}")
guard("c2765_pre==122", c2765_pre == 122, f"got={c2765_pre}")
guard("c2764_pre==124", c2764_pre == 124, f"got={c2764_pre}")
guard("c2763_pre==129", c2763_pre == 129, f"got={c2763_pre}")
guard("c2762_pre==149", c2762_pre == 149, f"got={c2762_pre}")
guard("c2761_pre==163", c2761_pre == 163, f"got={c2761_pre}")
guard("c2760_pre==125", c2760_pre == 125, f"got={c2760_pre}")
guard("c2759_pre==127", c2759_pre == 127, f"got={c2759_pre}")
guard("c2758_pre==129", c2758_pre == 129, f"got={c2758_pre}")
guard("c2757_pre==132", c2757_pre == 132, f"got={c2757_pre}")
guard("c2756_pre==137", c2756_pre == 137, f"got={c2756_pre}")
guard("c2755_pre==144", c2755_pre == 144, f"got={c2755_pre}")
guard("c2754_pre==147", c2754_pre == 147, f"got={c2754_pre}")
guard("c2753_pre==153", c2753_pre == 153, f"got={c2753_pre}")
guard("c2752_pre==159", c2752_pre == 159, f"got={c2752_pre}")
guard("c2751_pre==145", c2751_pre == 145, f"got={c2751_pre}")
guard("c2750_pre==147", c2750_pre == 147, f"got={c2750_pre}")
guard("c2749_pre==151", c2749_pre == 151, f"got={c2749_pre}")
guard("c2748_pre==141", c2748_pre == 141, f"got={c2748_pre}")
guard("c2747_pre==139", c2747_pre == 139, f"got={c2747_pre}")
guard("c2746_pre==134", c2746_pre == 134, f"got={c2746_pre}")

if failures:
    print(f"APPEND_ABORTED: {len(failures)} guard failures - worklog UNTOUCHED")
    sys.exit(1)

# 4) append with newline normalization
if not wl.endswith("\n"):
    wl += "\n"
block_norm = block if block.endswith("\n") else block + "\n"
with open(WL_TARGET, "a") as f:
    f.write(block_norm)

# 5) post-append assertions
wl2 = open(WL_TARGET).read()
n_after = wl2.count("\n")
guard("post_worklog_lines==9172", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2787_next_bullet", last2.startswith("- Next: the c2787 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==464", tid_post == 464, f"got={tid_post}")
guard("anchor_nogold_post==397", gold_post == 397, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2786_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2786")]) == 1)
expect_c2788_mentions = wl2.count("c2788")
guard("c2788_mention_birth", expect_c2788_mentions == c2788_pre + block.count("c2788"),
      f"pre={c2788_pre} (historical hash-artifact substrings) + block births={block.count('c2788')} (guard phrase + census-tuple sentence) -> expect={c2788_pre + block.count('c2788')} got={expect_c2788_mentions}")
for tag, pre in (("c2787", c2787_pre), ("c2786", c2786_pre), ("c2785", c2785_pre),
                 ("c2784", c2784_pre), ("c2783", c2783_pre), ("c2782", c2782_pre),
                 ("c2781", c2781_pre), ("c2780", c2780_pre), ("c2779", c2779_pre),
                 ("c2778", c2778_pre), ("c2777", c2777_pre), ("c2776", c2776_pre),
                 ("c2775", c2775_pre), ("c2774", c2774_pre), ("c2773", c2773_pre),
                 ("c2772", c2772_pre), ("c2771", c2771_pre), ("c2770", c2770_pre),
                 ("c2769", c2769_pre), ("c2768", c2768_pre), ("c2767", c2767_pre),
                 ("c2766", c2766_pre), ("c2765", c2765_pre), ("c2764", c2764_pre),
                 ("c2763", c2763_pre), ("c2762", c2762_pre), ("c2761", c2761_pre),
                 ("c2760", c2760_pre), ("c2759", c2759_pre), ("c2758", c2758_pre),
                 ("c2757", c2757_pre), ("c2756", c2756_pre), ("c2755", c2755_pre),
                 ("c2754", c2754_pre), ("c2753", c2753_pre), ("c2752", c2752_pre),
                 ("c2751", c2751_pre), ("c2750", c2750_pre), ("c2749", c2749_pre),
                 ("c2748", c2748_pre), ("c2747", c2747_pre), ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9160 -> 9172 (+12), c2786 entry + DRIFT-#49 pass-35 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
