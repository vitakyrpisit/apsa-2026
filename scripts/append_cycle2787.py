#!/usr/bin/env python3
"""Guarded worklog append for the c2787 entry (12 lines).

Follows the append_cycle2786.py precedent — ALL asserts precede the
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
window-2787 EPOCH-governs render check, the window-2788 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.7ms on the echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2789 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2787 forward-token lessons; NOTE the c2789 pre-count
is 0, the c2785 c2787-pre==0 class carries, NOT the c2783 c2788-pre==2 class
— measured at census time), zero adds to the two standing post-#6/post-#15
anchor series (OCCURRENCE counting — the standing method), pre-state (9172
lines, tail = the c2787 Next bullet, zero serviced c2787 entries, c2787
mention census per-line {9160: 2, 9164: 3, 9172: 5}, c2788 = 4 per-line
{9129: 2, 9172: 2}, anchors 464/397/60/28), post-state (9184 lines, tail =
the c2788 Next bullet, anchors 465/398/60/28). Zero mid-line writes (append
at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2787.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9172
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


POST = D("1793312165.345720238")    # c2787 post-echo (EPOCH-governs)
SCAN = D("1793312165.339")          # c2787 scanned_at (decimal)
TRIG = D("1793311570.000")          # c2787 trigger stamp (06:06:10 +08)
WIN = D("1793311941.574001205")     # window-2787 open (c2786 prophecy EPOCH)
ECHO = D("1793312016.730255803")    # loop echo #508 in-batch (EPOCH-governs)
C2786_SCAN = D("1793311641.568")    # c2786 scanned_at
C2786_POST = D("1793311641.574001205")  # c2786 post-echo
C2786_CLOSE = D("1793311858.000")   # c2786 close b0c7947 (22:10:58Z)
C2786_FOREIGN = D("1793311870.000") # foreign 966ab1f (22:11:10Z)
C2786_TRIG = D("1793310970.000")    # c2786 trigger stamp (05:56:10 +08)
C2785_CLOSE = D("1793311260.000")   # c2785 close 797cfcb (22:01:00Z)
C2785_FOREIGN = D("1793311273.000") # foreign 67ba021 (22:01:13Z)
TOKEN = D("1793311860.000")         # token 0611 (06:11:00Z)
C2786_TOKEN = D("1793311260.000")   # token 0601 (06:01:00Z)
WIN2786 = D("1793311367.104908992") # window-2786 open


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 06:06:10 +08 = 1793311570.000", dec_epoch(2026, 10, 29, 22, 6, 10), TRIG),
    ("c2786 trigger stamp 05:56:10 +08 = 1793310970.000", dec_epoch(2026, 10, 29, 21, 56, 10), C2786_TRIG),
    ("stamp-gap 600.000s by stamp (05:56:10 -> 06:06:10; the 600 print repeats)", TRIG - C2786_TRIG, D("600.000")),
    ("token-gap 600.000s by token (0601 -> 0611; the 600 print returns on the token surface)", TOKEN - C2786_TOKEN, D("600.000")),
    ("token-vs-stamp +290.000 (06:06:10 -> 06:11:00; the +290 print repeats)", TOKEN - TRIG, D("290.000")),
    ("c2786 close b0c7947 22:10:58Z = 1793311858.000", dec_epoch(2026, 10, 29, 22, 10, 58), C2786_CLOSE),
    ("foreign 966ab1f 22:11:10Z = 1793311870.000", dec_epoch(2026, 10, 29, 22, 11, 10), C2786_FOREIGN),
    ("c2785 close 797cfcb 22:01:00Z = 1793311260.000", dec_epoch(2026, 10, 29, 22, 1, 0), C2785_CLOSE),
    ("foreign 67ba021 22:01:13Z = 1793311273.000", dec_epoch(2026, 10, 29, 22, 1, 13), C2785_FOREIGN),
    ("loop echo ISO integer second 22:13:36 +0000", dec_epoch(2026, 10, 29, 22, 13, 36), D("1793312016.000")),
    ("loop echo EPOCH 1793312016.730255803 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 13, 36, 730255803), ECHO),
    ("capture pre-echo EPOCH 1793312163.654496361 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 16, 3, 654496361), D("1793312163.654496361")),
    ("post-echo ISO 22:16:05.345043831 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 22, 16, 5, 345043831), D("1793312165.345043831")),
    ("post-echo EPOCH 1793312165.345720238 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 16, 5, 345720238), POST),
    ("scanned_at 22:16:05.339 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 16, 5) + D("0.339"), SCAN),
    ("c2786 scanned_at 22:07:21.568 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 7, 21) + D("0.568"), C2786_SCAN),
    ("c2786 post-echo EPOCH 1793311641.574001205", dec_epoch(2026, 10, 29, 22, 7, 21, 574001205), C2786_POST),
    ("window-2787 open 06:12:21.574001205 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 22, 12, 21, 574001205), WIN),
    ("window-2788 open = post-echo + 300.000", POST + D("300.000"), D("1793312465.345720238")),
    ("echo post-c2786-post-echo +375.156254598", ECHO - C2786_POST, D("375.156254598")),
]
exact_checks = [
    ("skew decimal-exact +6.720238ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006720238")),
    ("echo_vs_window +75.156254598 (POST-WINDOW re-opens m1)", ECHO - WIN, D("75.156254598")),
    ("dd#361 = +223.771000000 (interval 523.771 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#358 print 631.629 - 300 = 331.629 and the dd#359 print 544.537 - 300 = 244.537 and the dd#360 print 574.472 - 300 = 274.472)", SCAN - C2786_SCAN - D("300.000"), D("223.771")),
    ("dd formula re-verification: 631.629 - 300 = 331.629", D("631.629") - D("300.000"), D("331.629")),
    ("dd formula re-verification: 544.537 - 300 = 244.537", D("544.537") - D("300.000"), D("244.537")),
    ("dd formula re-verification: 574.472 - 300 = 274.472", D("574.472") - D("300.000"), D("274.472")),
    ("INTERVAL#361 = 595.339", SCAN - TRIG, D("595.339")),
    ("LAG#361 = INTERVAL + dd - dd#360 = +544.638", (SCAN - TRIG) + (SCAN - C2786_SCAN - D("300.000")) - D("274.472"), D("544.638")),
    ("LATE#361 = trigger - window-open = -371.574001205", TRIG - WIN, D("-371.574001205")),
    ("CAPTURE_vs_window +223.771719033 (POST-WINDOW; echo POST — the both-POST print returns)", POST - WIN, D("223.771719033")),
    ("capture-vs-echo +148.615464435", POST - ECHO, D("148.615464435")),
    ("echo post-c2786-close +158.730255803 (b0c7947 at 22:10:58)", ECHO - C2786_CLOSE, D("158.730255803")),
    ("echo post-foreign-966ab1f +146.730255803 (22:11:10)", ECHO - C2786_FOREIGN, D("146.730255803")),
    ("stamp-to-echo 446.730255803 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("446.730255803")),
    ("trigger predates c2786 close by 288.000s", C2786_CLOSE - TRIG, D("288.000")),
    ("trigger predates the foreign 966ab1f by 300.000s (22:11:10)", C2786_FOREIGN - TRIG, D("300.000")),
    ("trigger predates the c2786 post-echo by 71.574001205s", C2786_POST - TRIG, D("71.574001205")),
    ("trigger predates window-2787 open by 371.574001205s", WIN - TRIG, D("371.574001205")),
    ("trigger postdates c2785 close by 310.000s (797cfcb at 22:01:00)", TRIG - C2785_CLOSE, D("310.000")),
    ("trigger postdates the foreign 67ba021 by 297.000s (22:01:13)", TRIG - C2785_FOREIGN, D("297.000")),
    ("trigger postdates window-2786 open by 202.895091008s", TRIG - WIN2786, D("202.895091008")),
    ("capture post-c2786-post-echo +523.771719033", POST - C2786_POST, D("523.771719033")),
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
guard("block_title", lines[1].startswith("CYCLE 2787"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2787"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2788 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2789_birth",
      block.count("c2789") == 2 and lines[-1].count("c2789") == 2
      and "c2788/c2789" in lines[-1] and "FORWARD token c2789" in lines[-1],
      f"block c2789={block.count('c2789')} next-line c2789={lines[-1].count('c2789')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9172", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2787_next_bullet", last_nonempty.startswith("- Next: the c2787 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2787",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2787")]) == 0,
      f"c2787 substring mentions={wl.count('c2787')} (expect 10)")
c2787_lines = {i + 1: l.count("c2787") for i, l in enumerate(wl.splitlines()) if "c2787" in l}
guard("c2787_mention_census_pre", wl.count("c2787") == 10 and c2787_lines == {9160: 2, 9164: 3, 9172: 5},
      f"per-line={c2787_lines}")
c2788_lines = {i + 1: l.count("c2788") for i, l in enumerate(wl.splitlines()) if "c2788" in l}
guard("c2788_forward_token_pre", wl.count("c2788") == 4 and c2788_lines == {9129: 2, 9172: 2},
      f"per-line={c2788_lines} (2 HISTORICAL hash-artifact substrings at 9129 + 2 "
      f"FORWARD-token births in the c2786 Next-block at 9172)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==464", tid_pre == 464, f"got={tid_pre}")
guard("anchor_nogold_pre==397", gold_pre == 397, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2789_pre = wl.count("c2789")
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
guard("c2789_pre==0", c2789_pre == 0, f"got={c2789_pre} (the forward token c2789 is UNBORN "
      f"pre-append — the c2785 c2787-pre==0 class carries, NOT the c2783 c2788-pre==2 "
      f"hash-artifact class; measured at census time)")
guard("c2788_pre==4", c2788_pre == 4, f"got={c2788_pre} (2 HISTORICAL hash-artifact "
      f"substrings + 2 FORWARD-token births in the c2786 Next-block)")
guard("c2787_pre==10", c2787_pre == 10, f"got={c2787_pre}")
guard("c2786_pre==38", c2786_pre == 38, f"got={c2786_pre}")
guard("c2785_pre==74", c2785_pre == 74, f"got={c2785_pre}")
guard("c2784_pre==77", c2784_pre == 77, f"got={c2784_pre}")
guard("c2783_pre==75", c2783_pre == 75, f"got={c2783_pre}")
guard("c2782_pre==77", c2782_pre == 77, f"got={c2782_pre}")
guard("c2781_pre==82", c2781_pre == 82, f"got={c2781_pre}")
guard("c2780_pre==86", c2780_pre == 86, f"got={c2780_pre}")
guard("c2779_pre==87", c2779_pre == 87, f"got={c2779_pre}")
guard("c2778_pre==118", c2778_pre == 118, f"got={c2778_pre}")
guard("c2777_pre==103", c2777_pre == 103, f"got={c2777_pre}")
guard("c2776_pre==108", c2776_pre == 108, f"got={c2776_pre}")
guard("c2775_pre==117", c2775_pre == 117, f"got={c2775_pre}")
guard("c2774_pre==122", c2774_pre == 122, f"got={c2774_pre}")
guard("c2773_pre==126", c2773_pre == 126, f"got={c2773_pre}")
guard("c2772_pre==145", c2772_pre == 145, f"got={c2772_pre}")
guard("c2771_pre==135", c2771_pre == 135, f"got={c2771_pre}")
guard("c2770_pre==163", c2770_pre == 163, f"got={c2770_pre}")
guard("c2769_pre==131", c2769_pre == 131, f"got={c2769_pre}")
guard("c2768_pre==134", c2768_pre == 134, f"got={c2768_pre}")
guard("c2767_pre==155", c2767_pre == 155, f"got={c2767_pre}")
guard("c2766_pre==146", c2766_pre == 146, f"got={c2766_pre}")
guard("c2765_pre==125", c2765_pre == 125, f"got={c2765_pre}")
guard("c2764_pre==127", c2764_pre == 127, f"got={c2764_pre}")
guard("c2763_pre==133", c2763_pre == 133, f"got={c2763_pre}")
guard("c2762_pre==153", c2762_pre == 153, f"got={c2762_pre}")
guard("c2761_pre==167", c2761_pre == 167, f"got={c2761_pre}")
guard("c2760_pre==129", c2760_pre == 129, f"got={c2760_pre}")
guard("c2759_pre==130", c2759_pre == 130, f"got={c2759_pre}")
guard("c2758_pre==132", c2758_pre == 132, f"got={c2758_pre}")
guard("c2757_pre==135", c2757_pre == 135, f"got={c2757_pre}")
guard("c2756_pre==140", c2756_pre == 140, f"got={c2756_pre}")
guard("c2755_pre==147", c2755_pre == 147, f"got={c2755_pre}")
guard("c2754_pre==150", c2754_pre == 150, f"got={c2754_pre}")
guard("c2753_pre==156", c2753_pre == 156, f"got={c2753_pre}")
guard("c2752_pre==162", c2752_pre == 162, f"got={c2752_pre}")
guard("c2751_pre==148", c2751_pre == 148, f"got={c2751_pre}")
guard("c2750_pre==150", c2750_pre == 150, f"got={c2750_pre}")
guard("c2749_pre==154", c2749_pre == 154, f"got={c2749_pre}")
guard("c2748_pre==144", c2748_pre == 144, f"got={c2748_pre}")
guard("c2747_pre==142", c2747_pre == 142, f"got={c2747_pre}")
guard("c2746_pre==138", c2746_pre == 138, f"got={c2746_pre}")

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
guard("post_worklog_lines==9184", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2788_next_bullet", last2.startswith("- Next: the c2788 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==465", tid_post == 465, f"got={tid_post}")
guard("anchor_nogold_post==398", gold_post == 398, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2787_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2787")]) == 1)
expect_c2789_mentions = wl2.count("c2789")
guard("c2789_mention_birth", expect_c2789_mentions == c2789_pre + block.count("c2789"),
      f"pre={c2789_pre} (unborn) + block births={block.count('c2789')} (guard phrase + census-tuple sentence) -> expect={c2789_pre + block.count('c2789')} got={expect_c2789_mentions}")
for tag, pre in (("c2788", c2788_pre), ("c2787", c2787_pre), ("c2786", c2786_pre),
                 ("c2785", c2785_pre), ("c2784", c2784_pre), ("c2783", c2783_pre),
                 ("c2782", c2782_pre), ("c2781", c2781_pre), ("c2780", c2780_pre),
                 ("c2779", c2779_pre), ("c2778", c2778_pre), ("c2777", c2777_pre),
                 ("c2776", c2776_pre), ("c2775", c2775_pre), ("c2774", c2774_pre),
                 ("c2773", c2773_pre), ("c2772", c2772_pre), ("c2771", c2771_pre),
                 ("c2770", c2770_pre), ("c2769", c2769_pre), ("c2768", c2768_pre),
                 ("c2767", c2767_pre), ("c2766", c2766_pre), ("c2765", c2765_pre),
                 ("c2764", c2764_pre), ("c2763", c2763_pre), ("c2762", c2762_pre),
                 ("c2761", c2761_pre), ("c2760", c2760_pre), ("c2759", c2759_pre),
                 ("c2758", c2758_pre), ("c2757", c2757_pre), ("c2756", c2756_pre),
                 ("c2755", c2755_pre), ("c2754", c2754_pre), ("c2753", c2753_pre),
                 ("c2752", c2752_pre), ("c2751", c2751_pre), ("c2750", c2750_pre),
                 ("c2749", c2749_pre), ("c2748", c2748_pre), ("c2747", c2747_pre),
                 ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9172 -> 9184 (+12), c2787 entry + DRIFT-#49 pass-36 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
