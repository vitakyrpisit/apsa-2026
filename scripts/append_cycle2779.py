#!/usr/bin/env python3
"""Guarded worklog append for the c2779 entry (12 lines).

Follows the append_cycle2778.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append abort precedent class).
The ledger arithmetic stays in the DECIMAL class: every ns-decomposition
check is Decimal-exact or Decimal-with-1e-6-tolerance on the utc-derived
values. THE C2778 ABORT LESSON STRUCTURALIZED: every pre-counter variable is
assigned in the SAME statement block before any guard references it (the
c2778 attempt-1 NameError class is impossible here), and a REHEARSAL mode
(APPEND_REHEARSAL=1) runs the full guard battery against a byte-identical
temp copy BEFORE the real run — the attempt counter counts REAL runs only.
Guards: python-timegm epoch cross-verification (31 Decimal-class checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic, all echo decompositions, the
stamp-gap/token-gap cadence pair, the window-2779 EPOCH-governs render check
(the c2778 Next-block ISO misrender +380.000s corrected), and the queue-print
check — the c2766 attempt-1 abort lesson: the SKEW check must use the
EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads differ
~0.6ms on the echo), block structure (12 lines: separator, title, standard
Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token guard
(c2781 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2779 forward-token lessons), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9076 lines, tail = the c2779 Next bullet, zero serviced
c2779 entries, c2779 mention census per-line {9064: 2, 9068: 2, 9076: 4},
anchors 456/389/60/28), post-state (9088 lines, tail = the c2780 Next
bullet, anchors 457/390/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2779.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9076
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

# 1) python-timegm epoch cross-verification (Decimal-class, 31 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = D("1793307126.486281620")    # c2779 post-echo (EPOCH-governs)
SCAN = D("1793307126.481")          # c2779 scanned_at (decimal)
TRIG = D("1793306169.000")          # c2779 trigger stamp (04:36:09 +08)
WIN = D("1793306581.565781844")     # window-2779 open (c2778 prophecy EPOCH)
ECHO = D("1793307099.579496688")    # loop echo in-batch (EPOCH-governs)
C2778_SCAN = D("1793306281.559")    # c2778 scanned_at
C2778_POST = D("1793306281.565781844")  # c2778 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 04:36:09 +08 = 1793306169.000", dec_epoch(2026, 10, 29, 20, 36, 9), TRIG),
    ("c2778 trigger stamp 04:26:08 +08 = 1793305568.000", dec_epoch(2026, 10, 29, 20, 26, 8), D("1793305568.000")),
    ("stamp-gap 601.000s by stamp (04:26:08 -> 04:36:09)", TRIG - D("1793305568.000"), D("601.000")),
    ("token-gap 600.000s by token (0431 -> 0441)", dec_epoch(2026, 10, 29, 20, 41, 0) - dec_epoch(2026, 10, 29, 20, 31, 0), D("600.000")),
    ("loop echo ISO integer second 20:51:39 +0000", dec_epoch(2026, 10, 29, 20, 51, 39), D("1793307099.000")),
    ("loop echo EPOCH 1793307099.579496688 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 51, 39, 579496688), ECHO),
    ("capture pre-echo EPOCH 1793307124.896440884 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 52, 4, 896440884), D("1793307124.896440884")),
    ("post-echo ISO 20:52:06.485656780 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 20, 52, 6, 485656780), D("1793307126.485656780")),
    ("post-echo EPOCH 1793307126.486281620 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 52, 6, 486281620), POST),
    ("scanned_at 20:52:06.481 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 52, 6) + D("0.481"), SCAN),
    ("c2778 scanned_at 20:38:01.559 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 38, 1) + D("0.559"), C2778_SCAN),
    ("window-2779 open 04:43:01.565781844 +08 (EPOCH-governs render — the c2778 Next-block ISO misprint +380.000s corrected)", dec_epoch(2026, 10, 29, 20, 43, 1, 565781844), WIN),
    ("window-2780 open = post-echo + 300.000", POST + D("300.000"), D("1793307426.486281620")),
    ("echo post-c2778-post-echo +818.013714844", ECHO - C2778_POST, D("818.013714844")),
]
exact_checks = [
    ("skew decimal-exact +5.281620ms (EPOCH-governs decomposition)", POST - SCAN, D("0.005281620")),
    ("echo_vs_window +518.013714844 (POST-WINDOW extends m7)", ECHO - WIN, D("518.013714844")),
    ("dd#353 = +544.922000000 (interval 844.922 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#351 print 546.182 - 300 = 246.182 and the dd#352 print 583.098 - 300 = 283.098)", SCAN - C2778_SCAN - D("300.000"), D("544.922")),
    ("INTERVAL#353 = 957.481", SCAN - TRIG, D("957.481")),
    ("LAG#353 = INTERVAL + dd - dd#352 = +1219.305", (SCAN - TRIG) + (SCAN - C2778_SCAN - D("300.000")) - D("283.098"), D("1219.305")),
    ("LATE#353 = trigger - window-open = -412.565781844", TRIG - WIN, D("-412.565781844")),
    ("CAPTURE_vs_window +544.920499776 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("544.920499776")),
    ("echo post-c2778-close +615.579496688 (486f086 at 20:41:24)", ECHO - D("1793306484.000"), D("615.579496688")),
    ("echo post-foreign-e54aab2 +599.579496688 (20:41:40)", ECHO - D("1793306500.000"), D("599.579496688")),
    ("stamp-to-echo 930.579496688 NEW DEEPEST (821.276190288 superseded)", ECHO - TRIG, D("930.579496688")),
    ("trigger predates c2778 close by 315.000s", D("1793306484.000") - TRIG, D("315.000")),
    ("trigger predates the foreign e54aab2 by 331.000s (20:41:40)", D("1793306500.000") - TRIG, D("331.000")),
    ("trigger predates the c2778 post-echo by 112.565781844s", C2778_POST - TRIG, D("112.565781844")),
    ("trigger predates window-2779 open by 412.565781844s", WIN - TRIG, D("412.565781844")),
    ("trigger postdates c2777 close by 265.000s (e961185 at 20:31:44)", TRIG - D("1793305904.000"), D("265.000")),
    ("trigger postdates the foreign 336d5f2 by 253.000s (20:31:56)", TRIG - D("1793305916.000"), D("253.000")),
    ("c2778 capture pre-echo fired 110.970542211s after this stamp (the queue print; EPOCH-governs 1793306279.970542211 — the ISO print .969842958 differs ~0.7ms, the ISO/EPOCH clock-reads lesson)", D("1793306279.970542211") - TRIG, D("110.970542211")),
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
guard("block_title", lines[1].startswith("CYCLE 2779"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2779"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2780 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2781_birth",
      block.count("c2781") == 2 and lines[-1].count("c2781") == 2
      and "c2780/c2781" in lines[-1] and "FORWARD token c2781" in lines[-1],
      f"block c2781={block.count('c2781')} next-line c2781={lines[-1].count('c2781')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9076", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2779_next_bullet", last_nonempty.startswith("- Next: the c2779 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2779",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2779")]) == 0,
      f"c2779 substring mentions={wl.count('c2779')} (expect 8)")
c2779_lines = {i + 1: l.count("c2779") for i, l in enumerate(wl.splitlines()) if "c2779" in l}
guard("c2779_mention_census_pre", wl.count("c2779") == 8 and c2779_lines == {9064: 2, 9068: 2, 9076: 4},
      f"per-line={c2779_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==456", tid_pre == 456, f"got={tid_pre}")
guard("anchor_nogold_pre==389", gold_pre == 389, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2780_pre==2", c2780_pre == 2, f"got={c2780_pre}")
guard("c2779_pre==8", c2779_pre == 8, f"got={c2779_pre}")
guard("c2778_pre==34", c2778_pre == 34, f"got={c2778_pre}")
guard("c2777_pre==66", c2777_pre == 66, f"got={c2777_pre}")
guard("c2776_pre==73", c2776_pre == 73, f"got={c2776_pre}")
guard("c2775_pre==82", c2775_pre == 82, f"got={c2775_pre}")
guard("c2774_pre==87", c2774_pre == 87, f"got={c2774_pre}")
guard("c2773_pre==91", c2773_pre == 91, f"got={c2773_pre}")
guard("c2772_pre==100", c2772_pre == 100, f"got={c2772_pre}")
guard("c2771_pre==100", c2771_pre == 100, f"got={c2771_pre}")
guard("c2770_pre==120", c2770_pre == 120, f"got={c2770_pre}")
guard("c2769_pre==103", c2769_pre == 103, f"got={c2769_pre}")

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
guard("post_worklog_lines==9088", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2780_next_bullet", last2.startswith("- Next: the c2780 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==457", tid_post == 457, f"got={tid_post}")
guard("anchor_nogold_post==390", gold_post == 390, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2779_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2779")]) == 1)
expect_c2781_mentions = wl2.count("c2781")
guard("c2781_mention_birth", expect_c2781_mentions == block.count("c2781"),
      f"block births={block.count('c2781')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2781_mentions}")
for tag, pre in (("c2780", c2780_pre), ("c2779", c2779_pre), ("c2778", c2778_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9076 -> 9088 (+12), c2779 entry + DRIFT-#49 pass-28 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
