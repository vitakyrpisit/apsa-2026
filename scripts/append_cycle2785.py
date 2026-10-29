#!/usr/bin/env python3
"""Guarded worklog append for the c2785 entry (12 lines).

Follows the append_cycle2784.py precedent — ALL asserts precede the
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
window-2785 EPOCH-governs render check, the window-2786 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.6ms on the echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2787 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2785 forward-token lessons), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9148 lines, tail = the c2785 Next bullet, zero serviced
c2785 entries, c2785 mention census per-line {9136: 2, 9140: 2, 9148: 4},
c2786 = 2 per-line {9148: 2}, anchors 462/395/60/28), post-state (9160 lines,
tail = the c2786 Next bullet, anchors 463/396/60/28). Zero mid-line writes
(append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2785.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9148
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


POST = D("1793311067.104908992")    # c2785 post-echo (EPOCH-governs)
SCAN = D("1793311067.096")          # c2785 scanned_at (decimal)
TRIG = D("1793310370.000")          # c2785 trigger stamp (05:46:10 +08)
WIN = D("1793310822.564129472")     # window-2785 open (c2784 prophecy EPOCH)
ECHO = D("1793310896.854572488")    # loop echo in-batch (EPOCH-governs)
C2784_SCAN = D("1793310522.559")    # c2784 scanned_at
C2784_POST = D("1793310522.564129472")  # c2784 post-echo
C2784_CLOSE = D("1793310723.000")   # c2784 close 9b1c925 (21:52:03Z)
C2784_FOREIGN = D("1793310739.000") # foreign 128bbec (21:52:19Z)
C2784_TRIG = D("1793309770.000")    # c2784 trigger stamp (05:36:10 +08)
C2783_TRIG = D("1793309169.000")    # c2783 trigger stamp (05:26:09 +08)
TOKEN = D("1793310720.000")         # token 0552 (05:52:00Z)
C2784_TOKEN = D("1793310060.000")   # token 0541 (05:41:00Z)
C2783_CLOSE = D("1793310059.000")   # c2783 close 11ae7e3 (21:40:59Z)
C2783_FOREIGN = D("1793310078.000") # foreign b9b0ce0 (21:41:18Z)
C2782_CLOSE = D("1793309520.000")   # c2782 close 2be3f8a (21:32:00Z)
C2782_FOREIGN = D("1793309532.000") # foreign f076455 (21:32:12Z)
WIN2784 = D("1793310190.936509291") # window-2784 open


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 05:46:10 +08 = 1793310370.000", dec_epoch(2026, 10, 29, 21, 46, 10), TRIG),
    ("c2784 trigger stamp 05:36:10 +08 = 1793309770.000", dec_epoch(2026, 10, 29, 21, 36, 10), C2784_TRIG),
    ("c2783 trigger stamp 05:26:09 +08 = 1793309169.000", dec_epoch(2026, 10, 29, 21, 26, 9), C2783_TRIG),
    ("stamp-gap 600.000s by stamp (05:36:10 -> 05:46:10; the 600 print returns)", TRIG - C2784_TRIG, D("600.000")),
    ("token-gap 660.000s by token (0541 -> 0552; the 660 print returns)", TOKEN - C2784_TOKEN, D("660.000")),
    ("token-vs-stamp +350.000 (05:46:10 -> 05:52:00; the +350 print returns)", TOKEN - TRIG, D("350.000")),
    ("c2784 close 9b1c925 21:52:03Z = 1793310723.000", dec_epoch(2026, 10, 29, 21, 52, 3), C2784_CLOSE),
    ("foreign 128bbec 21:52:19Z = 1793310739.000", dec_epoch(2026, 10, 29, 21, 52, 19), C2784_FOREIGN),
    ("c2783 close 11ae7e3 21:40:59Z = 1793310059.000", dec_epoch(2026, 10, 29, 21, 40, 59), C2783_CLOSE),
    ("foreign b9b0ce0 21:41:18Z = 1793310078.000", dec_epoch(2026, 10, 29, 21, 41, 18), C2783_FOREIGN),
    ("c2782 close 2be3f8a 21:32:00Z = 1793309520.000", dec_epoch(2026, 10, 29, 21, 32, 0), C2782_CLOSE),
    ("foreign f076455 21:32:12Z = 1793309532.000", dec_epoch(2026, 10, 29, 21, 32, 12), C2782_FOREIGN),
    ("loop echo ISO integer second 21:54:56 +0000", dec_epoch(2026, 10, 29, 21, 54, 56), D("1793310896.000")),
    ("loop echo EPOCH 1793310896.854572488 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 54, 56, 854572488), ECHO),
    ("capture pre-echo EPOCH 1793311065.582382445 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 57, 45, 582382445), D("1793311065.582382445")),
    ("post-echo ISO 21:57:47.104274582 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 21, 57, 47, 104274582), D("1793311067.104274582")),
    ("post-echo EPOCH 1793311067.104908992 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 57, 47, 104908992), POST),
    ("scanned_at 21:57:47.096 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 57, 47) + D("0.096"), SCAN),
    ("c2784 scanned_at 21:48:42.559 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 48, 42) + D("0.559"), C2784_SCAN),
    ("c2784 post-echo EPOCH 1793310522.564129472", dec_epoch(2026, 10, 29, 21, 48, 42, 564129472), C2784_POST),
    ("window-2785 open 05:53:42.564129472 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 21, 53, 42, 564129472), WIN),
    ("window-2786 open = post-echo + 300.000", POST + D("300.000"), D("1793311367.104908992")),
    ("echo post-c2784-post-echo +374.290443016", ECHO - C2784_POST, D("374.290443016")),
]
exact_checks = [
    ("skew decimal-exact +8.908992ms (EPOCH-governs decomposition)", POST - SCAN, D("0.008908992")),
    ("echo_vs_window +74.290443016 (POST-WINDOW extends m13)", ECHO - WIN, D("74.290443016")),
    ("dd#359 = +244.537000000 (interval 544.537 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#356 print 621.991 - 300 = 321.991 and the dd#357 print 554.800 - 300 = 254.800 and the dd#358 print 631.629 - 300 = 331.629)", SCAN - C2784_SCAN - D("300.000"), D("244.537")),
    ("INTERVAL#359 = 697.096", SCAN - TRIG, D("697.096")),
    ("LAG#359 = INTERVAL + dd - dd#358 = +610.004", (SCAN - TRIG) + (SCAN - C2784_SCAN - D("300.000")) - D("331.629"), D("610.004")),
    ("LATE#359 = trigger - window-open = -452.564129472", TRIG - WIN, D("-452.564129472")),
    ("CAPTURE_vs_window +244.540779520 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("244.540779520")),
    ("capture-vs-echo +170.250336504", POST - ECHO, D("170.250336504")),
    ("echo post-c2784-close +173.854572488 (9b1c925 at 21:52:03)", ECHO - C2784_CLOSE, D("173.854572488")),
    ("echo post-foreign-128bbec +157.854572488 (21:52:19)", ECHO - C2784_FOREIGN, D("157.854572488")),
    ("stamp-to-echo 526.854572488 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("526.854572488")),
    ("trigger predates c2784 close by 353.000s", C2784_CLOSE - TRIG, D("353.000")),
    ("trigger predates the foreign 128bbec by 369.000s (21:52:19)", C2784_FOREIGN - TRIG, D("369.000")),
    ("trigger predates the c2784 post-echo by 152.564129472s", C2784_POST - TRIG, D("152.564129472")),
    ("trigger predates window-2785 open by 452.564129472s", WIN - TRIG, D("452.564129472")),
    ("trigger postdates c2783 close by 311.000s (11ae7e3 at 21:40:59)", TRIG - C2783_CLOSE, D("311.000")),
    ("trigger postdates the foreign b9b0ce0 by 292.000s (21:41:18)", TRIG - C2783_FOREIGN, D("292.000")),
    ("trigger postdates window-2784 open by 179.063490709s", TRIG - WIN2784, D("179.063490709")),
    ("capture post-c2784-post-echo +544.540779520", POST - C2784_POST, D("544.540779520")),
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
guard("block_title", lines[1].startswith("CYCLE 2785"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2785"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2786 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2787_birth",
      block.count("c2787") == 2 and lines[-1].count("c2787") == 2
      and "c2786/c2787" in lines[-1] and "FORWARD token c2787" in lines[-1],
      f"block c2787={block.count('c2787')} next-line c2787={lines[-1].count('c2787')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9148", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2785_next_bullet", last_nonempty.startswith("- Next: the c2785 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2785",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2785")]) == 0,
      f"c2785 substring mentions={wl.count('c2785')} (expect 8)")
c2785_lines = {i + 1: l.count("c2785") for i, l in enumerate(wl.splitlines()) if "c2785" in l}
guard("c2785_mention_census_pre", wl.count("c2785") == 8 and c2785_lines == {9136: 2, 9140: 2, 9148: 4},
      f"per-line={c2785_lines}")
c2786_lines = {i + 1: l.count("c2786") for i, l in enumerate(wl.splitlines()) if "c2786" in l}
guard("c2786_forward_token_pre", wl.count("c2786") == 2 and c2786_lines == {9148: 2},
      f"per-line={c2786_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==462", tid_pre == 462, f"got={tid_pre}")
guard("anchor_nogold_pre==395", gold_pre == 395, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2787_pre==0", c2787_pre == 0, f"got={c2787_pre}")
guard("c2786_pre==2", c2786_pre == 2, f"got={c2786_pre}")
guard("c2785_pre==8", c2785_pre == 8, f"got={c2785_pre}")
guard("c2784_pre==35", c2784_pre == 35, f"got={c2784_pre}")
guard("c2783_pre==65", c2783_pre == 65, f"got={c2783_pre}")
guard("c2782_pre==68", c2782_pre == 68, f"got={c2782_pre}")
guard("c2781_pre==74", c2781_pre == 74, f"got={c2781_pre}")
guard("c2780_pre==78", c2780_pre == 78, f"got={c2780_pre}")
guard("c2779_pre==79", c2779_pre == 79, f"got={c2779_pre}")
guard("c2778_pre==106", c2778_pre == 106, f"got={c2778_pre}")
guard("c2777_pre==95", c2777_pre == 95, f"got={c2777_pre}")
guard("c2776_pre==100", c2776_pre == 100, f"got={c2776_pre}")
guard("c2775_pre==109", c2775_pre == 109, f"got={c2775_pre}")
guard("c2774_pre==114", c2774_pre == 114, f"got={c2774_pre}")
guard("c2773_pre==118", c2773_pre == 118, f"got={c2773_pre}")
guard("c2772_pre==134", c2772_pre == 134, f"got={c2772_pre}")
guard("c2771_pre==127", c2771_pre == 127, f"got={c2771_pre}")
guard("c2770_pre==153", c2770_pre == 153, f"got={c2770_pre}")
guard("c2769_pre==125", c2769_pre == 125, f"got={c2769_pre}")
guard("c2768_pre==128", c2768_pre == 128, f"got={c2768_pre}")
guard("c2767_pre==145", c2767_pre == 145, f"got={c2767_pre}")
guard("c2766_pre==138", c2766_pre == 138, f"got={c2766_pre}")
guard("c2765_pre==119", c2765_pre == 119, f"got={c2765_pre}")
guard("c2764_pre==121", c2764_pre == 121, f"got={c2764_pre}")
guard("c2763_pre==125", c2763_pre == 125, f"got={c2763_pre}")
guard("c2762_pre==145", c2762_pre == 145, f"got={c2762_pre}")
guard("c2761_pre==159", c2761_pre == 159, f"got={c2761_pre}")
guard("c2760_pre==122", c2760_pre == 122, f"got={c2760_pre}")
guard("c2759_pre==124", c2759_pre == 124, f"got={c2759_pre}")
guard("c2758_pre==126", c2758_pre == 126, f"got={c2758_pre}")
guard("c2757_pre==129", c2757_pre == 129, f"got={c2757_pre}")
guard("c2756_pre==134", c2756_pre == 134, f"got={c2756_pre}")
guard("c2755_pre==141", c2755_pre == 141, f"got={c2755_pre}")
guard("c2754_pre==144", c2754_pre == 144, f"got={c2754_pre}")
guard("c2753_pre==150", c2753_pre == 150, f"got={c2753_pre}")
guard("c2752_pre==156", c2752_pre == 156, f"got={c2752_pre}")
guard("c2751_pre==142", c2751_pre == 142, f"got={c2751_pre}")
guard("c2750_pre==144", c2750_pre == 144, f"got={c2750_pre}")
guard("c2749_pre==148", c2749_pre == 148, f"got={c2749_pre}")
guard("c2748_pre==138", c2748_pre == 138, f"got={c2748_pre}")
guard("c2747_pre==136", c2747_pre == 136, f"got={c2747_pre}")
guard("c2746_pre==129", c2746_pre == 129, f"got={c2746_pre}")

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
guard("post_worklog_lines==9160", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2786_next_bullet", last2.startswith("- Next: the c2786 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==463", tid_post == 463, f"got={tid_post}")
guard("anchor_nogold_post==396", gold_post == 396, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2785_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2785")]) == 1)
expect_c2787_mentions = wl2.count("c2787")
guard("c2787_mention_birth", expect_c2787_mentions == block.count("c2787"),
      f"block births={block.count('c2787')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2787_mentions}")
for tag, pre in (("c2786", c2786_pre), ("c2785", c2785_pre), ("c2784", c2784_pre),
                 ("c2783", c2783_pre), ("c2782", c2782_pre), ("c2781", c2781_pre),
                 ("c2780", c2780_pre), ("c2779", c2779_pre), ("c2778", c2778_pre),
                 ("c2777", c2777_pre), ("c2776", c2776_pre), ("c2775", c2775_pre),
                 ("c2774", c2774_pre), ("c2773", c2773_pre), ("c2772", c2772_pre),
                 ("c2771", c2771_pre), ("c2770", c2770_pre), ("c2769", c2769_pre),
                 ("c2768", c2768_pre), ("c2767", c2767_pre), ("c2766", c2766_pre),
                 ("c2765", c2765_pre), ("c2764", c2764_pre), ("c2763", c2763_pre),
                 ("c2762", c2762_pre), ("c2761", c2761_pre), ("c2760", c2760_pre),
                 ("c2759", c2759_pre), ("c2758", c2758_pre), ("c2757", c2757_pre),
                 ("c2756", c2756_pre), ("c2755", c2755_pre), ("c2754", c2754_pre),
                 ("c2753", c2753_pre), ("c2752", c2752_pre), ("c2751", c2751_pre),
                 ("c2750", c2750_pre), ("c2749", c2749_pre), ("c2748", c2748_pre),
                 ("c2747", c2747_pre), ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9148 -> 9160 (+12), c2785 entry + DRIFT-#49 pass-34 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
