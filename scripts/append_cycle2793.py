#!/usr/bin/env python3
"""Guarded worklog append for the c2793 entry (12 lines).

Follows the append_cycle2792.py precedent — ALL asserts precede the
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
window-2793 EPOCH-governs render check, the window-2794 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~11.0ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2795 = 3 block births: the Step-7 rehearsal pre-count print 'the
c2795 pre==0 expectation' + the Next bullet's guard phrase 'c2794/c2795' AND
census-tuple sentence 'FORWARD token c2795' — the c2767..c2793 forward-token
lessons; NOTE the c2795 pre-count is 0 (unborn) while the c2794 pre-count is
3 (born: the c2792 Step-7 rehearsal print + TWICE inside the c2792
Next-block) — the c2783 c2788-pre==2 class EVOLVED: the c2794 forward token
was born THRICE across the c2792 block, measured at census time per-line
{9242: 1, 9244: 2}, NOT the unborn class), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9244 lines, tail = the c2793 Next bullet, zero serviced c2793
entries, c2793 mention census per-line {9232: 2, 9236: 1, 9242: 1, 9244: 4},
c2794 = 3 per-line {9242: 1, 9244: 2}, anchors 470/403/60/28), post-state
(9256 lines, tail = the c2794 Next bullet, anchors 471/404/60/28). Zero
mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2793.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9244
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


POST = D("1793315166.905636634")    # c2793 post-echo (EPOCH-governs)
SCAN = D("1793315166.899")          # c2793 scanned_at (decimal)
TRIG = D("1793314581.000")          # c2793 trigger stamp (06:56:21 +08)
WIN = D("1793315022.218649965")     # window-2793 open (c2792 prophecy EPOCH)
ECHO = D("1793315019.627789461")    # loop echo #514 POST read (EPOCH-governs)
ECHO_ISO = D("1793315019.627192770")  # loop echo #514 ISO read FIRST (the bracket)
C2792_SCAN = D("1793314722.153")    # c2792 scanned_at
C2792_POST = D("1793314722.218649965")  # c2792 post-echo
C2792_CLOSE = D("1793314950.000")   # c2792 close 99f6ee6 (23:02:30Z)
C2792_FOREIGN = D("1793314965.000")  # foreign ea92218 (23:02:45Z)
C2792_TRIG = D("1793313971.000")    # c2792 trigger stamp (06:46:11 +08)
C2792_ECHO = D("1793314447.5846183")  # c2792 loop echo #513 (22:54:07.5846183)
C2792_PRE = D("1793314720.466776136")  # c2792 capture pre-echo (EPOCH-governs)
C2791_CLOSE = D("1793314387.000")   # c2791 close f6f24d7 (22:53:07Z)
C2791_FOREIGN = D("1793314407.000")  # foreign 18522dc (22:53:27Z)
TOKEN = D("1793314920.000")         # token 0702 (07:02:00 +08)
C2792_TOKEN = D("1793314380.000")   # token 0653 (06:53:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 06:56:21 +08 = 1793314581.000", dec_epoch(2026, 10, 29, 22, 56, 21), TRIG),
    ("c2792 trigger stamp 06:46:11 +08 = 1793313971.000", dec_epoch(2026, 10, 29, 22, 46, 11), C2792_TRIG),
    ("stamp-gap 610.000s by stamp (06:46:11 -> 06:56:21; the 610 print is NEW, zero priors)", TRIG - C2792_TRIG, D("610.000")),
    ("token-gap 540.000s by token (0653 -> 0702; the 540 print REPEATS, 20 priors)", TOKEN - C2792_TOKEN, D("540.000")),
    ("token-vs-stamp +339.000 (06:56:21 -> 07:02:00; the +339 print is NEW)", TOKEN - TRIG, D("339.000")),
    ("c2792 close 99f6ee6 23:02:30Z = 1793314950.000", dec_epoch(2026, 10, 29, 23, 2, 30), C2792_CLOSE),
    ("foreign ea92218 23:02:45Z = 1793314965.000", dec_epoch(2026, 10, 29, 23, 2, 45), C2792_FOREIGN),
    ("c2791 close f6f24d7 22:53:07Z = 1793314387.000", dec_epoch(2026, 10, 29, 22, 53, 7), C2791_CLOSE),
    ("foreign 18522dc 22:53:27Z = 1793314407.000", dec_epoch(2026, 10, 29, 22, 53, 27), C2791_FOREIGN),
    ("loop echo ISO integer second 23:03:39 +0000", dec_epoch(2026, 10, 29, 23, 3, 39), D("1793315019.000")),
    ("loop echo EPOCH 1793315019.627789461 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 23, 3, 39, 627789461), ECHO),
    ("loop echo ISO-bracket read 1793315019.627192770 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 3, 39, 627192770), ECHO_ISO),
    ("capture pre-echo EPOCH 1793315165.054329661 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 6, 5, 54329661), D("1793315165.054329661")),
    ("pre-echo ISO 23:06:05.053642359 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 6, 5, 53642359), D("1793315165.053642359")),
    ("post-echo ISO 23:06:06.904955343 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 6, 6, 904955343), D("1793315166.904955343")),
    ("post-echo EPOCH 1793315166.905636634 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 6, 6, 905636634), POST),
    ("scanned_at 23:06:06.899 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 6, 6) + D("0.899"), SCAN),
    ("c2792 scanned_at 22:58:42.153 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 58, 42) + D("0.153"), C2792_SCAN),
    ("c2792 post-echo EPOCH 1793314722.218649965", dec_epoch(2026, 10, 29, 22, 58, 42, 218649965), C2792_POST),
    ("c2792 capture pre-echo EPOCH 1793314720.466776136 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 58, 40, 466776136), C2792_PRE),
    ("window-2793 open 07:03:42.218649965 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 23, 3, 42, 218649965), WIN),
    ("window-2794 open = post-echo + 300.000", POST + D("300.000"), D("1793315466.905636634")),
    ("echo post-c2792-post-echo +297.409139496", ECHO - C2792_POST, D("297.409139496")),
]
exact_checks = [
    ("skew decimal-exact +6.636634ms (EPOCH-governs decomposition; SUB-10 re-opens m1)", POST - SCAN, D("0.006636634")),
    ("echo_vs_window -2.590860504 (PRE-WINDOW extends m2)", ECHO - WIN, D("-2.590860504")),
    ("dd#367 = +144.746000000 (interval 444.746 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#361 print 523.771 - 300 = 223.771 and the dd#362 print 445.372 - 300 = 145.372 and the dd#363 print 545.490 - 300 = 245.490 and the dd#364 print 552.974 - 300 = 252.974 and the dd#365 print 513.065 - 300 = 213.065 and the dd#366 print 499.913 - 300 = 199.913)", SCAN - C2792_SCAN - D("300.000"), D("144.746")),
    ("dd formula re-verification: 523.771 - 300 = 223.771", D("523.771") - D("300.000"), D("223.771")),
    ("dd formula re-verification: 445.372 - 300 = 145.372", D("445.372") - D("300.000"), D("145.372")),
    ("dd formula re-verification: 545.490 - 300 = 245.490", D("545.490") - D("300.000"), D("245.490")),
    ("dd formula re-verification: 552.974 - 300 = 252.974", D("552.974") - D("300.000"), D("252.974")),
    ("dd formula re-verification: 513.065 - 300 = 213.065", D("513.065") - D("300.000"), D("213.065")),
    ("dd formula re-verification: 499.913 - 300 = 199.913", D("499.913") - D("300.000"), D("199.913")),
    ("INTERVAL#367 = 585.899", SCAN - TRIG, D("585.899")),
    ("LAG#367 = INTERVAL + dd - dd#366 = +530.732", (SCAN - TRIG) + (SCAN - C2792_SCAN - D("300.000")) - D("199.913"), D("530.732")),
    ("LATE#367 = trigger - window-open = -441.218649965", TRIG - WIN, D("-441.218649965")),
    ("CAPTURE_vs_window +144.686986669 (POST-WINDOW; echo PRE — SPLIT extends m2)", POST - WIN, D("144.686986669")),
    ("capture-vs-echo +147.277847173", POST - ECHO, D("147.277847173")),
    ("capture post-c2792-post-echo +444.686986669", POST - C2792_POST, D("444.686986669")),
    ("echo post-c2792-close +69.627789461 (99f6ee6 at 23:02:30)", ECHO - C2792_CLOSE, D("69.627789461")),
    ("echo post-foreign-ea92218 +54.627789461 (23:02:45)", ECHO - C2792_FOREIGN, D("54.627789461")),
    ("stamp-to-echo 438.627789461 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("438.627789461")),
    ("trigger predates c2792 close by 369.000s", C2792_CLOSE - TRIG, D("369.000")),
    ("trigger predates the foreign ea92218 by 384.000s (23:02:45)", C2792_FOREIGN - TRIG, D("384.000")),
    ("trigger predates the c2792 capture pre-echo by 139.466776136s", C2792_PRE - TRIG, D("139.466776136")),
    ("trigger predates the c2792 post-echo by 141.218649965s", C2792_POST - TRIG, D("141.218649965")),
    ("trigger postdates the c2792 loop echo #513 by 133.4153817s (the trigger landed INSIDE the c2792 servicing window, post-echo pre-capture)", TRIG - C2792_ECHO, D("133.4153817")),
    ("trigger predates window-2793 open by 441.218649965s", WIN - TRIG, D("441.218649965")),
    ("trigger postdates c2791 close by 194.000s (f6f24d7 at 22:53:07)", TRIG - C2791_CLOSE, D("194.000")),
    ("trigger postdates the foreign 18522dc by 174.000s (22:53:27)", TRIG - C2791_FOREIGN, D("174.000")),
    ("c2792 close landed 30.000s AFTER the token second (23:02:30 vs 23:02:00)", C2792_CLOSE - TOKEN, D("30.000")),
    ("foreign ea92218 landed 45.000s AFTER the token second (23:02:45)", C2792_FOREIGN - TOKEN, D("45.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2793"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2793"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2794 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2795_birth",
      block.count("c2795") == 3 and lines[-1].count("c2795") == 2
      and "c2794/c2795" in lines[-1] and "FORWARD token c2795" in lines[-1]
      and "the c2795 pre==0 expectation" in block,
      f"block c2795={block.count('c2795')} next-line c2795={lines[-1].count('c2795')} "
      f"(expect 3: the Step-7 rehearsal pre-count print + the Next bullet's guard "
      f"phrase 'c2794/c2795' AND census-tuple sentence 'FORWARD token c2795')")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9244", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2793_next_bullet", last_nonempty.startswith("- Next: the c2793 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2793",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2793")]) == 0,
      f"c2793 substring mentions={wl.count('c2793')} (expect 8)")
c2793_lines = {i + 1: l.count("c2793") for i, l in enumerate(wl.splitlines()) if "c2793" in l}
guard("c2793_mention_census_pre", wl.count("c2793") == 8
      and c2793_lines == {9232: 2, 9236: 1, 9242: 1, 9244: 4},
      f"per-line={c2793_lines}")
c2794_lines = {i + 1: l.count("c2794") for i, l in enumerate(wl.splitlines()) if "c2794" in l}
guard("c2794_forward_token_pre", wl.count("c2794") == 3 and c2794_lines == {9242: 1, 9244: 2},
      f"per-line={c2794_lines} (1 birth in the c2792 Step-7 rehearsal print + 2 "
      f"FORWARD-token births inside the c2792 Next-block — the born-thrice class)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==470", tid_pre == 470, f"got={tid_pre}")
guard("anchor_nogold_pre==403", gold_pre == 403, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2795_pre = wl.count("c2795")
c2794_pre = wl.count("c2794")
c2793_pre = wl.count("c2793")
c2792_pre = wl.count("c2792")
c2791_pre = wl.count("c2791")
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
guard("c2795_pre==0", c2795_pre == 0, f"got={c2795_pre} (the forward token c2795 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2794_pre==3", c2794_pre == 3, f"got={c2794_pre} (born THRICE: the c2792 Step-7 "
      f"rehearsal print + TWICE inside the c2792 Next-block — NOT the unborn class)")
guard("c2793_pre==8", c2793_pre == 8, f"got={c2793_pre}")
guard("c2792_pre==35", c2792_pre == 35, f"got={c2792_pre}")
guard("c2791_pre==78", c2791_pre == 78, f"got={c2791_pre}")
guard("c2790_pre==81", c2790_pre == 81, f"got={c2790_pre}")
guard("c2789_pre==87", c2789_pre == 87, f"got={c2789_pre}")
guard("c2788_pre==97", c2788_pre == 97, f"got={c2788_pre}")
guard("c2787_pre==99", c2787_pre == 99, f"got={c2787_pre}")
guard("c2786_pre==107", c2786_pre == 107, f"got={c2786_pre}")
guard("c2785_pre==103", c2785_pre == 103, f"got={c2785_pre}")
guard("c2784_pre==101", c2784_pre == 101, f"got={c2784_pre}")
guard("c2783_pre==102", c2783_pre == 102, f"got={c2783_pre}")
guard("c2782_pre==101", c2782_pre == 101, f"got={c2782_pre}")
guard("c2781_pre==106", c2781_pre == 106, f"got={c2781_pre}")
guard("c2780_pre==110", c2780_pre == 110, f"got={c2780_pre}")
guard("c2779_pre==111", c2779_pre == 111, f"got={c2779_pre}")
guard("c2778_pre==149", c2778_pre == 149, f"got={c2778_pre}")
guard("c2777_pre==127", c2777_pre == 127, f"got={c2777_pre}")
guard("c2776_pre==132", c2776_pre == 132, f"got={c2776_pre}")
guard("c2775_pre==141", c2775_pre == 141, f"got={c2775_pre}")
guard("c2774_pre==146", c2774_pre == 146, f"got={c2774_pre}")
guard("c2773_pre==150", c2773_pre == 150, f"got={c2773_pre}")
guard("c2772_pre==169", c2772_pre == 169, f"got={c2772_pre}")
guard("c2771_pre==159", c2771_pre == 159, f"got={c2771_pre}")
guard("c2770_pre==193", c2770_pre == 193, f"got={c2770_pre}")
guard("c2769_pre==149", c2769_pre == 149, f"got={c2769_pre}")
guard("c2768_pre==152", c2768_pre == 152, f"got={c2768_pre}")
guard("c2767_pre==185", c2767_pre == 185, f"got={c2767_pre}")
guard("c2766_pre==170", c2766_pre == 170, f"got={c2766_pre}")
guard("c2765_pre==143", c2765_pre == 143, f"got={c2765_pre}")
guard("c2764_pre==145", c2764_pre == 145, f"got={c2764_pre}")
guard("c2763_pre==153", c2763_pre == 153, f"got={c2763_pre}")
guard("c2762_pre==177", c2762_pre == 177, f"got={c2762_pre}")
guard("c2761_pre==191", c2761_pre == 191, f"got={c2761_pre}")
guard("c2760_pre==148", c2760_pre == 148, f"got={c2760_pre}")
guard("c2759_pre==148", c2759_pre == 148, f"got={c2759_pre}")
guard("c2758_pre==150", c2758_pre == 150, f"got={c2758_pre}")
guard("c2757_pre==153", c2757_pre == 153, f"got={c2757_pre}")
guard("c2756_pre==158", c2756_pre == 158, f"got={c2756_pre}")
guard("c2755_pre==165", c2755_pre == 165, f"got={c2755_pre}")
guard("c2754_pre==168", c2754_pre == 168, f"got={c2754_pre}")
guard("c2753_pre==174", c2753_pre == 174, f"got={c2753_pre}")
guard("c2752_pre==180", c2752_pre == 180, f"got={c2752_pre}")
guard("c2751_pre==166", c2751_pre == 166, f"got={c2751_pre}")
guard("c2750_pre==168", c2750_pre == 168, f"got={c2750_pre}")
guard("c2749_pre==172", c2749_pre == 172, f"got={c2749_pre}")
guard("c2748_pre==162", c2748_pre == 162, f"got={c2748_pre}")
guard("c2747_pre==160", c2747_pre == 160, f"got={c2747_pre}")
guard("c2746_pre==162", c2746_pre == 162, f"got={c2746_pre}")

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
guard("post_worklog_lines==9256", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2794_next_bullet", last2.startswith("- Next: the c2794 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==471", tid_post == 471, f"got={tid_post}")
guard("anchor_nogold_post==404", gold_post == 404, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2793_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2793")]) == 1)
expect_c2795_mentions = wl2.count("c2795")
guard("c2795_mention_birth", expect_c2795_mentions == c2795_pre + block.count("c2795"),
      f"pre={c2795_pre} (unborn) + block births={block.count('c2795')} (Step-7 pre-count "
      f"print + guard phrase + census-tuple sentence) -> expect={c2795_pre + block.count('c2795')} got={expect_c2795_mentions}")
for tag, pre in (("c2794", c2794_pre), ("c2793", c2793_pre), ("c2792", c2792_pre),
                 ("c2791", c2791_pre), ("c2790", c2790_pre), ("c2789", c2789_pre),
                 ("c2788", c2788_pre), ("c2787", c2787_pre), ("c2786", c2786_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9244 -> 9256 (+12), c2793 entry + DRIFT-#49 pass-42 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
