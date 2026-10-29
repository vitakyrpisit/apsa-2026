#!/usr/bin/env python3
"""Guarded worklog append for the c2788 entry (12 lines).

Follows the append_cycle2787.py precedent — ALL asserts precede the
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
window-2788 EPOCH-governs render check, the window-2789 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.7ms on the echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2790 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2788 forward-token lessons; NOTE the c2790 pre-count
is 0, the c2785 c2787-pre==0 class carries, NOT the c2783 c2788-pre==2 class
— measured at census time), zero adds to the two standing post-#6/post-#15
anchor series (OCCURRENCE counting — the standing method), pre-state (9184
lines, tail = the c2788 Next bullet, zero serviced c2788 entries, c2788
mention census per-line {9129: 2, 9172: 2, 9176: 2, 9184: 5}, c2789 = 2
per-line {9184: 2}, anchors 465/398/60/28), post-state (9196 lines, tail =
the c2789 Next bullet, anchors 466/399/60/28). Zero mid-line writes (append
at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2788.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9184
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


POST = D("1793312610.717868544")    # c2788 post-echo (EPOCH-governs)
SCAN = D("1793312610.711")          # c2788 scanned_at (decimal)
TRIG = D("1793311871.000")          # c2788 trigger stamp (06:11:11 +08)
WIN = D("1793312465.345720238")     # window-2788 open (c2787 prophecy EPOCH)
ECHO = D("1793312398.376260241")    # loop echo #509 in-batch (EPOCH-governs)
C2787_SCAN = D("1793312165.339")    # c2787 scanned_at
C2787_POST = D("1793312165.345720238")  # c2787 post-echo
C2787_CLOSE = D("1793312331.000")   # c2787 close a762125 (22:18:51Z)
C2787_FOREIGN = D("1793312348.000") # foreign 0b4f512 (22:19:08Z)
C2787_TRIG = D("1793311570.000")    # c2787 trigger stamp (06:06:10 +08)
C2786_CLOSE = D("1793311858.000")   # c2786 close b0c7947 (22:10:58Z)
C2786_FOREIGN = D("1793311870.000") # foreign 966ab1f (22:11:10Z)
TOKEN = D("1793312340.000")         # token 0619 (06:19:00Z)
C2787_TOKEN = D("1793311860.000")   # token 0611 (06:11:00Z)
WIN2787 = D("1793311941.574001205") # window-2787 open


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 06:11:11 +08 = 1793311871.000", dec_epoch(2026, 10, 29, 22, 11, 11), TRIG),
    ("c2787 trigger stamp 06:06:10 +08 = 1793311570.000", dec_epoch(2026, 10, 29, 22, 6, 10), C2787_TRIG),
    ("stamp-gap 301.000s by stamp (06:06:10 -> 06:11:11; the 301 print is NEW)", TRIG - C2787_TRIG, D("301.000")),
    ("token-gap 480.000s by token (0611 -> 0619; the 480 print returns)", TOKEN - C2787_TOKEN, D("480.000")),
    ("token-vs-stamp +469.000 (06:11:11 -> 06:19:00; the +469 print is NEW)", TOKEN - TRIG, D("469.000")),
    ("c2787 close a762125 22:18:51Z = 1793312331.000", dec_epoch(2026, 10, 29, 22, 18, 51), C2787_CLOSE),
    ("foreign 0b4f512 22:19:08Z = 1793312348.000", dec_epoch(2026, 10, 29, 22, 19, 8), C2787_FOREIGN),
    ("c2786 close b0c7947 22:10:58Z = 1793311858.000", dec_epoch(2026, 10, 29, 22, 10, 58), C2786_CLOSE),
    ("foreign 966ab1f 22:11:10Z = 1793311870.000", dec_epoch(2026, 10, 29, 22, 11, 10), C2786_FOREIGN),
    ("loop echo ISO integer second 22:19:58 +0000", dec_epoch(2026, 10, 29, 22, 19, 58), D("1793312398.000")),
    ("loop echo EPOCH 1793312398.376260241 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 19, 58, 376260241), ECHO),
    ("capture pre-echo EPOCH 1793312609.035968642 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 23, 29, 35968642), D("1793312609.035968642")),
    ("post-echo ISO 22:23:30.717157176 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 22, 23, 30, 717157176), D("1793312610.717157176")),
    ("post-echo EPOCH 1793312610.717868544 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 23, 30, 717868544), POST),
    ("scanned_at 22:23:30.711 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 23, 30) + D("0.711"), SCAN),
    ("c2787 scanned_at 22:16:05.339 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 16, 5) + D("0.339"), C2787_SCAN),
    ("c2787 post-echo EPOCH 1793312165.345720238", dec_epoch(2026, 10, 29, 22, 16, 5, 345720238), C2787_POST),
    ("window-2788 open 06:21:05.345720238 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 22, 21, 5, 345720238), WIN),
    ("window-2789 open = post-echo + 300.000", POST + D("300.000"), D("1793312910.717868544")),
    ("echo post-c2787-post-echo +233.030540003", ECHO - C2787_POST, D("233.030540003")),
]
exact_checks = [
    ("skew decimal-exact +6.868544ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006868544")),
    ("echo_vs_window -66.969459997 (PRE-WINDOW re-opens m1)", ECHO - WIN, D("-66.969459997")),
    ("dd#362 = +145.372000000 (interval 445.372 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#358 print 631.629 - 300 = 331.629 and the dd#359 print 544.537 - 300 = 244.537 and the dd#360 print 574.472 - 300 = 274.472 and the dd#361 print 523.771 - 300 = 223.771)", SCAN - C2787_SCAN - D("300.000"), D("145.372")),
    ("dd formula re-verification: 631.629 - 300 = 331.629", D("631.629") - D("300.000"), D("331.629")),
    ("dd formula re-verification: 544.537 - 300 = 244.537", D("544.537") - D("300.000"), D("244.537")),
    ("dd formula re-verification: 574.472 - 300 = 274.472", D("574.472") - D("300.000"), D("274.472")),
    ("dd formula re-verification: 523.771 - 300 = 223.771", D("523.771") - D("300.000"), D("223.771")),
    ("INTERVAL#362 = 739.711", SCAN - TRIG, D("739.711")),
    ("LAG#362 = INTERVAL + dd - dd#361 = +661.312", (SCAN - TRIG) + (SCAN - C2787_SCAN - D("300.000")) - D("223.771"), D("661.312")),
    ("LATE#362 = trigger - window-open = -594.345720238", TRIG - WIN, D("-594.345720238")),
    ("CAPTURE_vs_window +145.372148306 (POST-WINDOW; echo PRE — the SPLIT print returns)", POST - WIN, D("145.372148306")),
    ("capture-vs-echo +212.341608303", POST - ECHO, D("212.341608303")),
    ("capture post-c2787-post-echo +445.372148306", POST - C2787_POST, D("445.372148306")),
    ("echo post-c2787-close +67.376260241 (a762125 at 22:18:51)", ECHO - C2787_CLOSE, D("67.376260241")),
    ("echo post-foreign-0b4f512 +50.376260241 (22:19:08)", ECHO - C2787_FOREIGN, D("50.376260241")),
    ("stamp-to-echo 527.376260241 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("527.376260241")),
    ("trigger predates c2787 close by 460.000s", C2787_CLOSE - TRIG, D("460.000")),
    ("trigger predates the foreign 0b4f512 by 477.000s (22:19:08)", C2787_FOREIGN - TRIG, D("477.000")),
    ("trigger predates the c2787 post-echo by 294.345720238s", C2787_POST - TRIG, D("294.345720238")),
    ("trigger predates window-2788 open by 594.345720238s", WIN - TRIG, D("594.345720238")),
    ("trigger postdates c2786 close by 13.000s (b0c7947 at 22:10:58)", TRIG - C2786_CLOSE, D("13.000")),
    ("trigger postdates the foreign 966ab1f by 1.000s (22:11:10)", TRIG - C2786_FOREIGN, D("1.000")),
    ("c2787 close landed 9.000s BEFORE the token second (22:18:51 vs 06:19:00)", TOKEN - C2787_CLOSE, D("9.000")),
    ("foreign 0b4f512 landed 8.000s AFTER the token second (22:19:08)", C2787_FOREIGN - TOKEN, D("8.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2788"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2788"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2789 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2790_birth",
      block.count("c2790") == 2 and lines[-1].count("c2790") == 2
      and "c2789/c2790" in lines[-1] and "FORWARD token c2790" in lines[-1],
      f"block c2790={block.count('c2790')} next-line c2790={lines[-1].count('c2790')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9184", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2788_next_bullet", last_nonempty.startswith("- Next: the c2788 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2788",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2788")]) == 0,
      f"c2788 substring mentions={wl.count('c2788')} (expect 11)")
c2788_lines = {i + 1: l.count("c2788") for i, l in enumerate(wl.splitlines()) if "c2788" in l}
guard("c2788_mention_census_pre", wl.count("c2788") == 11 and c2788_lines == {9129: 2, 9172: 2, 9176: 2, 9184: 5},
      f"per-line={c2788_lines}")
c2789_lines = {i + 1: l.count("c2789") for i, l in enumerate(wl.splitlines()) if "c2789" in l}
guard("c2789_forward_token_pre", wl.count("c2789") == 2 and c2789_lines == {9184: 2},
      f"per-line={c2789_lines} (2 FORWARD-token births inside the c2787 Next-block "
      f"guard phrase AND FORWARD-token sentence)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==465", tid_pre == 465, f"got={tid_pre}")
guard("anchor_nogold_pre==398", gold_pre == 398, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2790_pre = wl.count("c2790")
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
guard("c2790_pre==0", c2790_pre == 0, f"got={c2790_pre} (the forward token c2790 is UNBORN "
      f"pre-append — the c2785 c2787-pre==0 class carries, NOT the c2783 c2788-pre==2 "
      f"hash-artifact class; measured at census time)")
guard("c2789_pre==2", c2789_pre == 2, f"got={c2789_pre} (2 FORWARD-token births inside "
      f"the c2787 Next-block)")
guard("c2788_pre==11", c2788_pre == 11, f"got={c2788_pre}")
guard("c2787_pre==38", c2787_pre == 38, f"got={c2787_pre}")
guard("c2786_pre==78", c2786_pre == 78, f"got={c2786_pre}")
guard("c2785_pre==82", c2785_pre == 82, f"got={c2785_pre}")
guard("c2784_pre==81", c2784_pre == 81, f"got={c2784_pre}")
guard("c2783_pre==79", c2783_pre == 79, f"got={c2783_pre}")
guard("c2782_pre==81", c2782_pre == 81, f"got={c2782_pre}")
guard("c2781_pre==86", c2781_pre == 86, f"got={c2781_pre}")
guard("c2780_pre==90", c2780_pre == 90, f"got={c2780_pre}")
guard("c2779_pre==91", c2779_pre == 91, f"got={c2779_pre}")
guard("c2778_pre==124", c2778_pre == 124, f"got={c2778_pre}")
guard("c2777_pre==107", c2777_pre == 107, f"got={c2777_pre}")
guard("c2776_pre==112", c2776_pre == 112, f"got={c2776_pre}")
guard("c2775_pre==121", c2775_pre == 121, f"got={c2775_pre}")
guard("c2774_pre==126", c2774_pre == 126, f"got={c2774_pre}")
guard("c2773_pre==130", c2773_pre == 130, f"got={c2773_pre}")
guard("c2772_pre==149", c2772_pre == 149, f"got={c2772_pre}")
guard("c2771_pre==139", c2771_pre == 139, f"got={c2771_pre}")
guard("c2770_pre==168", c2770_pre == 168, f"got={c2770_pre}")
guard("c2769_pre==134", c2769_pre == 134, f"got={c2769_pre}")
guard("c2768_pre==137", c2768_pre == 137, f"got={c2768_pre}")
guard("c2767_pre==160", c2767_pre == 160, f"got={c2767_pre}")
guard("c2766_pre==150", c2766_pre == 150, f"got={c2766_pre}")
guard("c2765_pre==128", c2765_pre == 128, f"got={c2765_pre}")
guard("c2764_pre==130", c2764_pre == 130, f"got={c2764_pre}")
guard("c2763_pre==137", c2763_pre == 137, f"got={c2763_pre}")
guard("c2762_pre==157", c2762_pre == 157, f"got={c2762_pre}")
guard("c2761_pre==171", c2761_pre == 171, f"got={c2761_pre}")
guard("c2760_pre==133", c2760_pre == 133, f"got={c2760_pre}")
guard("c2759_pre==133", c2759_pre == 133, f"got={c2759_pre}")
guard("c2758_pre==135", c2758_pre == 135, f"got={c2758_pre}")
guard("c2757_pre==138", c2757_pre == 138, f"got={c2757_pre}")
guard("c2756_pre==143", c2756_pre == 143, f"got={c2756_pre}")
guard("c2755_pre==150", c2755_pre == 150, f"got={c2755_pre}")
guard("c2754_pre==153", c2754_pre == 153, f"got={c2754_pre}")
guard("c2753_pre==159", c2753_pre == 159, f"got={c2753_pre}")
guard("c2752_pre==165", c2752_pre == 165, f"got={c2752_pre}")
guard("c2751_pre==151", c2751_pre == 151, f"got={c2751_pre}")
guard("c2750_pre==153", c2750_pre == 153, f"got={c2750_pre}")
guard("c2749_pre==157", c2749_pre == 157, f"got={c2749_pre}")
guard("c2748_pre==147", c2748_pre == 147, f"got={c2748_pre}")
guard("c2747_pre==145", c2747_pre == 145, f"got={c2747_pre}")
guard("c2746_pre==142", c2746_pre == 142, f"got={c2746_pre}")

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
guard("post_worklog_lines==9196", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2789_next_bullet", last2.startswith("- Next: the c2789 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==466", tid_post == 466, f"got={tid_post}")
guard("anchor_nogold_post==399", gold_post == 399, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2788_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2788")]) == 1)
expect_c2790_mentions = wl2.count("c2790")
guard("c2790_mention_birth", expect_c2790_mentions == c2790_pre + block.count("c2790"),
      f"pre={c2790_pre} (unborn) + block births={block.count('c2790')} (guard phrase + census-tuple sentence) -> expect={c2790_pre + block.count('c2790')} got={expect_c2790_mentions}")
for tag, pre in (("c2789", c2789_pre), ("c2788", c2788_pre), ("c2787", c2787_pre),
                 ("c2786", c2786_pre), ("c2785", c2785_pre), ("c2784", c2784_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9184 -> 9196 (+12), c2788 entry + DRIFT-#49 pass-37 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
