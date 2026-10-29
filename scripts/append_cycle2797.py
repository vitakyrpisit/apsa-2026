#!/usr/bin/env python3
"""Guarded worklog append for the c2797 entry (12 lines).

Follows the append_cycle2796.py precedent — ALL asserts precede the
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
window-2797 EPOCH-governs render check, the window-2798 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.65ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2799 = 4 block births: the Step-7 rehearsal pre-count print 'the
c2799 pre==0 expectation' + the Step-7 census-time print 'c2799_pre = 0' +
the Next bullet's guard phrase 'c2798/c2799' AND census-tuple sentence 'FORWARD
token c2799' — the c2767..c2797 forward-token lessons; NOTE the c2799
pre-count is 0 (unborn) while the c2798 pre-count is 3 (born: the c2796
Step-7 rehearsal print + TWICE inside the c2796 Next-block) — the c2783
c2788-pre==2 class EVOLVED: the c2798 forward token was born THRICE across
the c2796 block, measured at census time per-line {9290: 1, 9292: 2}, NOT
the unborn class), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9292 lines,
tail = the c2797 Next bullet, zero serviced c2797 entries, c2797 mention
census per-line {9278: 1, 9280: 2, 9284: 3, 9290: 1, 9292: 4} total 11,
c2798 = 3 per-line {9290: 1, 9292: 2}, c2799 = 0 UNBORN, anchors 474/407/
60/28), post-state (9304 lines, tail = the c2798 Next bullet, anchors 475/
408/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2797.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9292
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


POST = D("1793317517.553325554")    # c2797 post-echo (EPOCH-governs)
SCAN = D("1793317517.547")          # c2797 scanned_at (decimal)
TRIG = D("1793316672.000")          # c2797 trigger stamp (07:31:12 +08)
WIN = D("1793317251.519917938")     # window-2797 open (c2796 prophecy EPOCH)
ECHO = D("1793317384.121961127")    # loop echo #518 POST read (EPOCH-governs)
ECHO_ISO = D("1793317384.121242580")  # loop echo #518 ISO read FIRST (the bracket)
PRE = D("1793317515.656092809")     # c2797 capture pre-echo (EPOCH-governs)
C2796_SCAN = D("1793316951.514")    # c2796 scanned_at
C2796_POST = D("1793316951.519917938")  # c2796 post-echo
C2796_CLOSE = D("1793317207.000")   # c2796 close 1baacec (23:40:07Z)
C2796_FOREIGN = D("1793317219.000")  # foreign 7efc24d (23:40:19Z)
C2796_TRIG = D("1793316372.000")    # c2796 trigger stamp (07:26:12 +08)
C2796_ECHO = D("1793316802.548723451")  # c2796 loop echo #517 (23:33:22.548723451)
C2796_ECHO_ISO = D("1793316802.547975200")  # c2796 echo ISO bracket
C2796_PRE = D("1793316949.778423329")  # c2796 capture pre-echo (EPOCH-governs)
C2795_SCAN = D("1793316379.163")    # c2795 scanned_at
C2795_POST = D("1793316379.170480455")  # c2795 post-echo
C2795_CLOSE = D("1793316615.000")   # c2795 close 0d844fa (23:30:15Z)
C2795_FOREIGN = D("1793316631.000")  # foreign 615fc1c (23:30:31Z)
C2795_TRIG = D("1793315471.000")    # c2795 trigger stamp (07:11:11 +08)
C2795_ECHO = D("1793316141.062851709")  # c2795 loop echo #516 (23:22:21.062851709)
C2795_ECHO_ISO = D("1793316141.062208970")  # c2795 echo ISO bracket
C2795_PRE = D("1793316377.499476469")  # c2795 capture pre-echo (EPOCH-governs)
TOKEN = D("1793317200.000")         # token 0740 (07:40:00 +08)
C2796_TOKEN = D("1793316600.000")   # token 0730 (07:30:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 07:31:12 +08 = 1793316672.000", dec_epoch(2026, 10, 29, 23, 31, 12), TRIG),
    ("c2796 trigger stamp 07:26:12 +08 = 1793316372.000", dec_epoch(2026, 10, 29, 23, 26, 12), C2796_TRIG),
    ("stamp-gap 300.000s by stamp (07:26:12 -> 07:31:12; the 901-by-stamp print BROKE)", TRIG - C2796_TRIG, D("300.000")),
    ("token-gap 600.000s by token (0730 -> 0740; the 600 print REPEATS, 16 priors)", TOKEN - C2796_TOKEN, D("600.000")),
    ("token-vs-stamp +528.000 (07:31:12 -> 07:40:00; the +528 print is NEW)", TOKEN - TRIG, D("528.000")),
    ("c2796 close 1baacec 23:40:07Z = 1793317207.000", dec_epoch(2026, 10, 29, 23, 40, 7), C2796_CLOSE),
    ("foreign 7efc24d 23:40:19Z = 1793317219.000", dec_epoch(2026, 10, 29, 23, 40, 19), C2796_FOREIGN),
    ("c2795 close 0d844fa 23:30:15Z = 1793316615.000", dec_epoch(2026, 10, 29, 23, 30, 15), C2795_CLOSE),
    ("foreign 615fc1c 23:30:31Z = 1793316631.000", dec_epoch(2026, 10, 29, 23, 30, 31), C2795_FOREIGN),
    ("c2796 loop echo #517 EPOCH 1793316802.548723451 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 33, 22, 548723451), C2796_ECHO),
    ("c2796 echo ISO-bracket 1793316802.547975200 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 33, 22, 547975200), C2796_ECHO_ISO),
    ("c2796 capture pre-echo EPOCH 1793316949.778423329 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 35, 49, 778423329), C2796_PRE),
    ("c2796 post-echo ISO 23:35:51.519209414 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 35, 51, 519209414), D("1793316951.519209414")),
    ("c2796 post-echo EPOCH 1793316951.519917938 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 35, 51, 519917938), C2796_POST),
    ("c2796 scanned_at 23:35:51.514 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 35, 51) + D("0.514"), C2796_SCAN),
    ("c2795 loop echo #516 EPOCH 1793316141.062851709 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 22, 21, 62851709), C2795_ECHO),
    ("c2795 echo ISO-bracket 1793316141.062208970 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 22, 21, 62208970), C2795_ECHO_ISO),
    ("c2795 capture pre-echo EPOCH 1793316377.499476469 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 26, 17, 499476469), C2795_PRE),
    ("c2795 post-echo ISO 23:26:19.169778054 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 26, 19, 169778054), D("1793316379.169778054")),
    ("c2795 post-echo EPOCH 1793316379.170480455 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 26, 19, 170480455), C2795_POST),
    ("c2795 scanned_at 23:26:19.163 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 26, 19) + D("0.163"), C2795_SCAN),
    ("loop echo #518 ISO integer second 23:43:04 +0000", dec_epoch(2026, 10, 29, 23, 43, 4), D("1793317384.000")),
    ("loop echo #518 EPOCH 1793317384.121961127 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 23, 43, 4, 121961127), ECHO),
    ("loop echo #518 ISO-bracket read 1793317384.121242580 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 43, 4, 121242580), ECHO_ISO),
    ("capture pre-echo EPOCH 1793317515.656092809 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 45, 15, 656092809), PRE),
    ("pre-echo ISO 23:45:15.655437786 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 45, 15, 655437786), D("1793317515.655437786")),
    ("post-echo ISO 23:45:17.552670564 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 45, 17, 552670564), D("1793317517.552670564")),
    ("post-echo EPOCH 1793317517.553325554 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 45, 17, 553325554), POST),
    ("scanned_at 23:45:17.547 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 45, 17) + D("0.547"), SCAN),
    ("window-2797 open 07:40:51.519917938 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 23, 40, 51, 519917938), WIN),
    ("window-2798 open = post-echo + 300.000", POST + D("300.000"), D("1793317817.553325554")),
    ("echo post-c2796-post-echo +432.602043189", ECHO - C2796_POST, D("432.602043189")),
]
exact_checks = [
    ("skew decimal-exact +6.325554ms (EPOCH-governs decomposition; SUB-10 extends m5)", POST - SCAN, D("0.006325554")),
    ("echo_vs_window +132.602043189 (POST-WINDOW extends m4; the c2796 prophecy held)", ECHO - WIN, D("132.602043189")),
    ("dd#371 = +266.033000000 (interval 566.033 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#368 print 625.759 - 300 = 325.759 and the dd#370 print 572.351 - 300 = 272.351)", SCAN - C2796_SCAN - D("300.000"), D("266.033")),
    ("dd formula re-verification: 572.351 - 300 = 272.351", D("572.351") - D("300.000"), D("272.351")),
    ("dd formula re-verification: 586.505 - 300 = 286.505", D("586.505") - D("300.000"), D("286.505")),
    ("INTERVAL#371 = 845.547", SCAN - TRIG, D("845.547")),
    ("LAG#371 = INTERVAL + dd - dd#370 = +839.229", (SCAN - TRIG) + (SCAN - C2796_SCAN - D("300.000")) - D("272.351"), D("839.229")),
    ("LATE#371 = trigger - window-open = -579.519917938", TRIG - WIN, D("-579.519917938")),
    ("CAPTURE_vs_window +266.033407616 (POST-WINDOW; echo POST — BOTH-POST extends m4)", POST - WIN, D("266.033407616")),
    ("capture-vs-echo +133.431364427", POST - ECHO, D("133.431364427")),
    ("capture post-c2796-post-echo +566.033407616", POST - C2796_POST, D("566.033407616")),
    ("echo post-c2796-close +177.121961127 (1baacec at 23:40:07)", ECHO - C2796_CLOSE, D("177.121961127")),
    ("echo post-foreign-7efc24d +165.121961127 (23:40:19)", ECHO - C2796_FOREIGN, D("165.121961127")),
    ("stamp-to-echo 712.121961127 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("712.121961127")),
    ("trigger PREDATES the c2796 loop echo #517 by 130.548723451s (the trigger stamp landed INSIDE the c2796 servicing window, PRE-echo — the inside-window class in its pre-echo phase)", C2796_ECHO - TRIG, D("130.548723451")),
    ("trigger predates the c2796 capture pre-echo by 277.778423329s", C2796_PRE - TRIG, D("277.778423329")),
    ("trigger predates the c2796 post-echo by 279.519917938s", C2796_POST - TRIG, D("279.519917938")),
    ("trigger predates the c2796 scanned_at by 279.514s", C2796_SCAN - TRIG, D("279.514")),
    ("trigger predates window-2797 open by 579.519917938s", WIN - TRIG, D("579.519917938")),
    ("c2796 close POSTDATES the trigger by 535.000s (1baacec at 23:40:07)", C2796_CLOSE - TRIG, D("535.000")),
    ("foreign 7efc24d POSTDATES the trigger by 547.000s (23:40:19)", C2796_FOREIGN - TRIG, D("547.000")),
    ("trigger postdates the foreign 615fc1c by 41.000s (23:30:31)", TRIG - C2795_FOREIGN, D("41.000")),
    ("trigger postdates the c2795 close 0d844fa by 57.000s (23:30:15)", TRIG - C2795_CLOSE, D("57.000")),
    ("c2796 close landed 7.000s AFTER the token-0740 second (23:40:07 vs 23:40:00)", C2796_CLOSE - TOKEN, D("7.000")),
    ("foreign 7efc24d landed 19.000s AFTER the token second (23:40:19)", C2796_FOREIGN - TOKEN, D("19.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2797"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2797"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2798 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2799_birth",
      block.count("c2799") == 4 and lines[-1].count("c2799") == 2
      and "c2798/c2799" in lines[-1] and "FORWARD token c2799" in lines[-1]
      and "the c2799 pre==0 expectation" in block,
      f"block c2799={block.count('c2799')} next-line c2799={lines[-1].count('c2799')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2799_pre = 0' + the Next bullet's guard phrase 'c2798/c2799' AND "
      f"census-tuple sentence 'FORWARD token c2799')")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9292", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2797_next_bullet", last_nonempty.startswith("- Next: the c2797 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2797",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2797")]) == 0,
      f"c2797 substring mentions={wl.count('c2797')} (expect 11)")
c2797_lines = {i + 1: l.count("c2797") for i, l in enumerate(wl.splitlines()) if "c2797" in l}
guard("c2797_mention_census_pre", wl.count("c2797") == 11
      and c2797_lines == {9278: 1, 9280: 2, 9284: 3, 9290: 1, 9292: 4},
      f"per-line={c2797_lines}")
c2798_lines = {i + 1: l.count("c2798") for i, l in enumerate(wl.splitlines()) if "c2798" in l}
guard("c2798_forward_token_pre", wl.count("c2798") == 3 and c2798_lines == {9290: 1, 9292: 2},
      f"per-line={c2798_lines} (1 birth in the c2796 Step-7 rehearsal print + 2 "
      f"FORWARD-token births inside the c2796 Next-block — the born-thrice class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==474", tid_pre == 474, f"got={tid_pre}")
guard("anchor_nogold_pre==407", gold_pre == 407, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2799_pre = wl.count("c2799")
c2798_pre = wl.count("c2798")
c2797_pre = wl.count("c2797")
c2796_pre = wl.count("c2796")
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
guard("c2799_pre==0", c2799_pre == 0, f"got={c2799_pre} (the forward token c2799 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2798_pre==3", c2798_pre == 3, f"got={c2798_pre} (born THRICE: the c2796 Step-7 "
      f"rehearsal print + TWICE inside the c2796 Next-block — NOT the unborn class)")
guard("c2797_pre==11", c2797_pre == 11, f"got={c2797_pre}")
guard("c2796_pre==42", c2796_pre == 42, f"got={c2796_pre}")
guard("c2795_pre==88", c2795_pre == 88, f"got={c2795_pre}")
guard("c2794_pre==98", c2794_pre == 98, f"got={c2794_pre}")
guard("c2793_pre==100", c2793_pre == 100, f"got={c2793_pre}")
guard("c2792_pre==105", c2792_pre == 105, f"got={c2792_pre}")
guard("c2791_pre==100", c2791_pre == 100, f"got={c2791_pre}")
guard("c2790_pre==103", c2790_pre == 103, f"got={c2790_pre}")
guard("c2789_pre==103", c2789_pre == 103, f"got={c2789_pre}")
guard("c2788_pre==114", c2788_pre == 114, f"got={c2788_pre}")
guard("c2787_pre==115", c2787_pre == 115, f"got={c2787_pre}")
guard("c2786_pre==127", c2786_pre == 127, f"got={c2786_pre}")
guard("c2785_pre==119", c2785_pre == 119, f"got={c2785_pre}")
guard("c2784_pre==117", c2784_pre == 117, f"got={c2784_pre}")
guard("c2783_pre==118", c2783_pre == 118, f"got={c2783_pre}")
guard("c2782_pre==117", c2782_pre == 117, f"got={c2782_pre}")
guard("c2781_pre==122", c2781_pre == 122, f"got={c2781_pre}")
guard("c2780_pre==126", c2780_pre == 126, f"got={c2780_pre}")
guard("c2779_pre==127", c2779_pre == 127, f"got={c2779_pre}")
guard("c2778_pre==171", c2778_pre == 171, f"got={c2778_pre}")
guard("c2777_pre==143", c2777_pre == 143, f"got={c2777_pre}")
guard("c2776_pre==148", c2776_pre == 148, f"got={c2776_pre}")
guard("c2775_pre==157", c2775_pre == 157, f"got={c2775_pre}")
guard("c2774_pre==162", c2774_pre == 162, f"got={c2774_pre}")
guard("c2773_pre==166", c2773_pre == 166, f"got={c2773_pre}")
guard("c2772_pre==185", c2772_pre == 185, f"got={c2772_pre}")
guard("c2771_pre==175", c2771_pre == 175, f"got={c2771_pre}")
guard("c2770_pre==213", c2770_pre == 213, f"got={c2770_pre}")
guard("c2769_pre==164", c2769_pre == 164, f"got={c2769_pre}")
guard("c2768_pre==167", c2768_pre == 167, f"got={c2768_pre}")
guard("c2767_pre==208", c2767_pre == 208, f"got={c2767_pre}")
guard("c2766_pre==189", c2766_pre == 189, f"got={c2766_pre}")
guard("c2765_pre==158", c2765_pre == 158, f"got={c2765_pre}")
guard("c2764_pre==160", c2764_pre == 160, f"got={c2764_pre}")
guard("c2763_pre==168", c2763_pre == 168, f"got={c2763_pre}")
guard("c2762_pre==196", c2762_pre == 196, f"got={c2762_pre}")
guard("c2761_pre==210", c2761_pre == 210, f"got={c2761_pre}")
guard("c2760_pre==163", c2760_pre == 163, f"got={c2760_pre}")
guard("c2759_pre==163", c2759_pre == 163, f"got={c2759_pre}")
guard("c2758_pre==165", c2758_pre == 165, f"got={c2758_pre}")
guard("c2757_pre==168", c2757_pre == 168, f"got={c2757_pre}")
guard("c2756_pre==173", c2756_pre == 173, f"got={c2756_pre}")
guard("c2755_pre==180", c2755_pre == 180, f"got={c2755_pre}")
guard("c2754_pre==183", c2754_pre == 183, f"got={c2754_pre}")
guard("c2753_pre==189", c2753_pre == 189, f"got={c2753_pre}")
guard("c2752_pre==195", c2752_pre == 195, f"got={c2752_pre}")
guard("c2751_pre==181", c2751_pre == 181, f"got={c2751_pre}")
guard("c2750_pre==183", c2750_pre == 183, f"got={c2750_pre}")
guard("c2749_pre==187", c2749_pre == 187, f"got={c2749_pre}")
guard("c2748_pre==177", c2748_pre == 177, f"got={c2748_pre}")
guard("c2747_pre==175", c2747_pre == 175, f"got={c2747_pre}")
guard("c2746_pre==181", c2746_pre == 181, f"got={c2746_pre}")

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
guard("post_worklog_lines==9304", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2798_next_bullet", last2.startswith("- Next: the c2798 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==475", tid_post == 475, f"got={tid_post}")
guard("anchor_nogold_post==408", gold_post == 408, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2797_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2797")]) == 1)
expect_c2799_mentions = wl2.count("c2799")
guard("c2799_mention_birth", expect_c2799_mentions == c2799_pre + block.count("c2799"),
      f"pre={c2799_pre} (unborn) + block births={block.count('c2799')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2799_pre + block.count('c2799')} got={expect_c2799_mentions}")
for tag, pre in (("c2798", c2798_pre), ("c2797", c2797_pre), ("c2796", c2796_pre),
                 ("c2795", c2795_pre), ("c2794", c2794_pre), ("c2793", c2793_pre),
                 ("c2792", c2792_pre), ("c2791", c2791_pre), ("c2790", c2790_pre),
                 ("c2789", c2789_pre), ("c2788", c2788_pre), ("c2787", c2787_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9292 -> 9304 (+12), c2797 entry + DRIFT-#49 pass-46 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
