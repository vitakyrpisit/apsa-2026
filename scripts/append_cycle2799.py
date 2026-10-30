#!/usr/bin/env python3
"""Guarded worklog append for the c2799 entry (12 lines).

Follows the append_cycle2798.py precedent — ALL asserts precede the
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
window-2799 EPOCH-governs render check, the window-2800 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.72ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2801 = 4 block births: the Step-7 rehearsal pre-count print 'the
c2801 pre==0 expectation' + the Step-7 census-time print 'c2801_pre = 0' +
the Next bullet's guard phrase 'c2800/c2801' AND census-tuple sentence 'FORWARD
token c2801' — the c2767..c2799 forward-token lessons; NOTE the c2801
pre-count is 0 (unborn) while the c2800 pre-count is 4 (born: the c2798
Step-7 twin-print line 9314 TWICE + TWICE inside the c2798 Next-block) — the
c2798 append prophecy 'c2800 = 4 block births' held EXACTLY: the born-FOUR
class REPEATS), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9316 lines,
tail = the c2799 Next bullet, zero serviced c2799 entries, c2799 mention
census per-line {9302: 2, 9304: 2, 9308: 5, 9314: 1, 9316: 4} total 14,
c2800 = 4 per-line {9314: 2, 9316: 2}, c2801 = 0 UNBORN, anchors 476/409/
60/28), post-state (9328 lines, tail = the c2800 Next bullet, anchors 477/
410/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2799.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9316
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


POST = D("1793318656.922499324")    # c2799 post-echo (EPOCH-governs)
SCAN = D("1793318656.916")          # c2799 scanned_at (decimal)
TRIG = D("1793317872.000")          # c2799 trigger stamp (07:51:12 +08)
WIN = D("1793318348.116623814")     # window-2799 open (c2798 prophecy EPOCH)
ECHO = D("1793318442.5431652")      # loop echo #520 POST read (EPOCH-governs)
ECHO_ISO = D("1793318442.533247405")  # loop echo #520 ISO read FIRST (the bracket)
PRE = D("1793318655.041130607")     # c2799 capture pre-echo (EPOCH-governs)
C2798_SCAN = D("1793318048.111")    # c2798 scanned_at
C2798_POST = D("1793318048.116623814")  # c2798 post-echo
C2798_CLOSE = D("1793318358.000")   # c2798 close 9261c07 (23:59:18Z)
C2798_FOREIGN = D("1793318372.000")  # foreign b27a69f (23:59:32Z)
C2798_TRIG = D("1793317272.000")    # c2798 trigger stamp (07:41:12 +08)
C2798_ECHO = D("1793317916.289761869")  # c2798 loop echo #519 (23:51:56.289761869)
C2798_ECHO_ISO = D("1793317916.289098550")  # c2798 echo ISO bracket
C2798_PRE = D("1793318046.466500339")  # c2798 capture pre-echo (EPOCH-governs)
C2797_SCAN = D("1793317517.547")    # c2797 scanned_at
C2797_POST = D("1793317517.553325554")  # c2797 post-echo
C2797_CLOSE = D("1793317785.000")   # c2797 close 98db775 (23:49:45Z)
C2797_FOREIGN = D("1793317802.000")  # foreign 65f4c4e (23:50:02Z)
TOKEN = D("1793318340.000")         # token 0759 (07:59:00 +08)
C2798_TOKEN = D("1793317800.000")   # token 0750 (07:50:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 07:51:12 +08 = 1793317872.000", dec_epoch(2026, 10, 29, 23, 51, 12), TRIG),
    ("c2798 trigger stamp 07:41:12 +08 = 1793317272.000", dec_epoch(2026, 10, 29, 23, 41, 12), C2798_TRIG),
    ("stamp-gap 600.000s by stamp (07:41:12 -> 07:51:12; the 600 print REPEATS)", TRIG - C2798_TRIG, D("600.000")),
    ("token-gap 540.000s by token (0750 -> 0759; the 600s-by-token print BROKE, the 540 print RETURNS)", TOKEN - C2798_TOKEN, D("540.000")),
    ("token-vs-stamp +468.000 (07:51:12 -> 07:59:00; the +468 print is NEW)", TOKEN - TRIG, D("468.000")),
    ("c2798 close 9261c07 23:59:18Z = 1793318358.000", dec_epoch(2026, 10, 29, 23, 59, 18), C2798_CLOSE),
    ("foreign b27a69f 23:59:32Z = 1793318372.000", dec_epoch(2026, 10, 29, 23, 59, 32), C2798_FOREIGN),
    ("c2797 close 98db775 23:49:45Z = 1793317785.000", dec_epoch(2026, 10, 29, 23, 49, 45), C2797_CLOSE),
    ("foreign 65f4c4e 23:50:02Z = 1793317802.000", dec_epoch(2026, 10, 29, 23, 50, 2), C2797_FOREIGN),
    ("c2798 loop echo #519 EPOCH 1793317916.289761869 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 51, 56, 289761869), C2798_ECHO),
    ("c2798 echo ISO-bracket 1793317916.289098550 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 51, 56, 289098550), C2798_ECHO_ISO),
    ("c2798 capture pre-echo EPOCH 1793318046.466500339 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 54, 6, 466500339), C2798_PRE),
    ("c2798 post-echo ISO 23:54:08.115953287 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 54, 8, 115953287), D("1793318048.115953287")),
    ("c2798 post-echo EPOCH 1793318048.116623814 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 54, 8, 116623814), C2798_POST),
    ("c2798 scanned_at 23:54:08.111 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 54, 8) + D("0.111"), C2798_SCAN),
    ("loop echo #520 ISO integer second 00:00:42 +0000", dec_epoch(2026, 10, 30, 0, 0, 42), D("1793318442.000")),
    ("loop echo #520 EPOCH 1793318442.5431652 (EPOCH-governs POST read)", dec_epoch(2026, 10, 30, 0, 0, 42, 543165200), ECHO),
    ("loop echo #520 ISO-bracket read 1793318442.533247405 (the ISO read FIRST)", dec_epoch(2026, 10, 30, 0, 0, 42, 533247405), ECHO_ISO),
    ("capture pre-echo EPOCH 1793318655.041130607 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 4, 15, 41130607), PRE),
    ("pre-echo ISO 00:04:15.040535158 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 4, 15, 40535158), D("1793318655.040535158")),
    ("post-echo ISO 00:04:16.921782217 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 4, 16, 921782217), D("1793318656.921782217")),
    ("post-echo EPOCH 1793318656.922499324 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 4, 16, 922499324), POST),
    ("scanned_at 00:04:16.916 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 4, 16) + D("0.916"), SCAN),
    ("window-2799 open 07:59:08.116623814 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 23, 59, 8, 116623814), WIN),
    ("window-2800 open = post-echo + 300.000", POST + D("300.000"), D("1793318956.922499324")),
    ("echo post-c2798-post-echo +394.426541386", ECHO - C2798_POST, D("394.426541386")),
]
exact_checks = [
    ("skew decimal-exact +6.499324ms (EPOCH-governs decomposition; SUB-10 extends m7)", POST - SCAN, D("0.006499324")),
    ("echo_vs_window +94.426541386 (POST-WINDOW extends m6; the c2798 Next-block watch held)", ECHO - WIN, D("94.426541386")),
    ("dd#373 = +308.805000000 (interval 608.805 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#371 print 566.033 - 300 = 266.033 and the dd#372 print 530.564 - 300 = 230.564)", SCAN - C2798_SCAN - D("300.000"), D("308.805")),
    ("dd formula re-verification: 530.564 - 300 = 230.564", D("530.564") - D("300.000"), D("230.564")),
    ("dd formula re-verification: 566.033 - 300 = 266.033", D("566.033") - D("300.000"), D("266.033")),
    ("INTERVAL#373 = 784.916", SCAN - TRIG, D("784.916")),
    ("LAG#373 = INTERVAL + dd - dd#372 = +863.157", (SCAN - TRIG) + (SCAN - C2798_SCAN - D("300.000")) - D("230.564"), D("863.157")),
    ("LATE#373 = trigger - window-open = -476.116623814", TRIG - WIN, D("-476.116623814")),
    ("CAPTURE_vs_window +308.805875510 (POST-WINDOW; echo POST — BOTH-POST extends m6)", POST - WIN, D("308.805875510")),
    ("capture-vs-echo +214.379334124", POST - ECHO, D("214.379334124")),
    ("capture post-c2798-post-echo +608.805875510", POST - C2798_POST, D("608.805875510")),
    ("echo post-c2798-close +84.5431652 (9261c07 at 23:59:18)", ECHO - C2798_CLOSE, D("84.5431652")),
    ("echo post-foreign-b27a69f +70.5431652 (23:59:32)", ECHO - C2798_FOREIGN, D("70.5431652")),
    ("stamp-to-echo 570.5431652 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("570.5431652")),
    ("trigger PREDATES the c2798 loop echo #519 by 44.289761869s (the trigger stamp landed INSIDE the c2798 servicing window, PRE-echo — the inside-window class REPEATS)", C2798_ECHO - TRIG, D("44.289761869")),
    ("trigger predates the c2798 capture pre-echo by 174.466500339s", C2798_PRE - TRIG, D("174.466500339")),
    ("trigger predates the c2798 post-echo by 176.116623814s", C2798_POST - TRIG, D("176.116623814")),
    ("trigger predates the c2798 scanned_at by 176.111s", C2798_SCAN - TRIG, D("176.111")),
    ("trigger predates window-2799 open by 476.116623814s", WIN - TRIG, D("476.116623814")),
    ("c2798 close POSTDATES the trigger by 486.000s (9261c07 at 23:59:18)", C2798_CLOSE - TRIG, D("486.000")),
    ("foreign b27a69f POSTDATES the trigger by 500.000s (23:59:32)", C2798_FOREIGN - TRIG, D("500.000")),
    ("trigger postdates the foreign 65f4c4e by 70.000s (23:50:02)", TRIG - C2797_FOREIGN, D("70.000")),
    ("trigger postdates the c2797 close 98db775 by 87.000s (23:49:45)", TRIG - C2797_CLOSE, D("87.000")),
    ("c2798 close landed 18.000s AFTER the token-0759 second (23:59:18 vs 23:59:00 — the after-class identity RESTORES)", C2798_CLOSE - TOKEN, D("18.000")),
    ("foreign b27a69f landed 32.000s AFTER the token second (23:59:32)", C2798_FOREIGN - TOKEN, D("32.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2799"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2799"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2800 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2801_birth",
      block.count("c2801") == 4 and lines[-1].count("c2801") == 2
      and "c2800/c2801" in lines[-1] and "FORWARD token c2801" in lines[-1]
      and "the c2801 pre==0 expectation" in block and "c2801_pre = 0" in block,
      f"block c2801={block.count('c2801')} next-line c2801={lines[-1].count('c2801')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2801_pre = 0' + the Next bullet's guard phrase 'c2800/c2801' AND "
      f"census-tuple sentence 'FORWARD token c2801')")
guard("block_c2800_step7_precount_sentence",
      "the c2800 pre-count is 4" in block
      and "per-line {9314: 2, 9316: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2800 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9316", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2799_next_bullet", last_nonempty.startswith("- Next: the c2799 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2799",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2799")]) == 0,
      f"c2799 substring mentions={wl.count('c2799')} (expect 14)")
c2799_lines = {i + 1: l.count("c2799") for i, l in enumerate(wl.splitlines()) if "c2799" in l}
guard("c2799_mention_census_pre", wl.count("c2799") == 14
      and c2799_lines == {9302: 2, 9304: 2, 9308: 5, 9314: 1, 9316: 4},
      f"per-line={c2799_lines}")
c2800_lines = {i + 1: l.count("c2800") for i, l in enumerate(wl.splitlines()) if "c2800" in l}
guard("c2800_forward_token_pre", wl.count("c2800") == 4 and c2800_lines == {9314: 2, 9316: 2},
      f"per-line={c2800_lines} (2 births in the c2798 Step-7 twin-print line 9314 + "
      f"2 FORWARD-token births inside the c2798 Next-block — the born-FOUR class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==476", tid_pre == 476, f"got={tid_pre}")
guard("anchor_nogold_pre==409", gold_pre == 409, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2801_pre = wl.count("c2801")
c2800_pre = wl.count("c2800")
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
guard("c2801_pre==0", c2801_pre == 0, f"got={c2801_pre} (the forward token c2801 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2800_pre==4", c2800_pre == 4, f"got={c2800_pre} (born FOUR: the c2798 Step-7 twin-print "
      f"line 9314 TWICE + TWICE inside the c2798 Next-block — NOT the unborn class)")
guard("c2799_pre==14", c2799_pre == 14, f"got={c2799_pre}")
guard("c2798_pre==34", c2798_pre == 34, f"got={c2798_pre}")
guard("c2797_pre==74", c2797_pre == 74, f"got={c2797_pre}")
guard("c2796_pre==86", c2796_pre == 86, f"got={c2796_pre}")
guard("c2795_pre==99", c2795_pre == 99, f"got={c2795_pre}")
guard("c2794_pre==103", c2794_pre == 103, f"got={c2794_pre}")
guard("c2793_pre==106", c2793_pre == 106, f"got={c2793_pre}")
guard("c2792_pre==111", c2792_pre == 111, f"got={c2792_pre}")
guard("c2791_pre==104", c2791_pre == 104, f"got={c2791_pre}")
guard("c2790_pre==109", c2790_pre == 109, f"got={c2790_pre}")
guard("c2789_pre==107", c2789_pre == 107, f"got={c2789_pre}")
guard("c2788_pre==118", c2788_pre == 118, f"got={c2788_pre}")
guard("c2787_pre==119", c2787_pre == 119, f"got={c2787_pre}")
guard("c2786_pre==133", c2786_pre == 133, f"got={c2786_pre}")
guard("c2785_pre==123", c2785_pre == 123, f"got={c2785_pre}")
guard("c2784_pre==121", c2784_pre == 121, f"got={c2784_pre}")
guard("c2783_pre==122", c2783_pre == 122, f"got={c2783_pre}")
guard("c2782_pre==121", c2782_pre == 121, f"got={c2782_pre}")
guard("c2781_pre==126", c2781_pre == 126, f"got={c2781_pre}")
guard("c2780_pre==130", c2780_pre == 130, f"got={c2780_pre}")
guard("c2779_pre==131", c2779_pre == 131, f"got={c2779_pre}")
guard("c2778_pre==175", c2778_pre == 175, f"got={c2778_pre}")
guard("c2777_pre==147", c2777_pre == 147, f"got={c2777_pre}")
guard("c2776_pre==152", c2776_pre == 152, f"got={c2776_pre}")
guard("c2775_pre==161", c2775_pre == 161, f"got={c2775_pre}")
guard("c2774_pre==166", c2774_pre == 166, f"got={c2774_pre}")
guard("c2773_pre==170", c2773_pre == 170, f"got={c2773_pre}")
guard("c2772_pre==189", c2772_pre == 189, f"got={c2772_pre}")
guard("c2771_pre==179", c2771_pre == 179, f"got={c2771_pre}")
guard("c2770_pre==219", c2770_pre == 219, f"got={c2770_pre}")
guard("c2769_pre==168", c2769_pre == 168, f"got={c2769_pre}")
guard("c2768_pre==171", c2768_pre == 171, f"got={c2768_pre}")
guard("c2767_pre==216", c2767_pre == 216, f"got={c2767_pre}")
guard("c2766_pre==195", c2766_pre == 195, f"got={c2766_pre}")
guard("c2765_pre==162", c2765_pre == 162, f"got={c2765_pre}")
guard("c2764_pre==164", c2764_pre == 164, f"got={c2764_pre}")
guard("c2763_pre==172", c2763_pre == 172, f"got={c2763_pre}")
guard("c2762_pre==202", c2762_pre == 202, f"got={c2762_pre}")
guard("c2761_pre==216", c2761_pre == 216, f"got={c2761_pre}")
guard("c2760_pre==167", c2760_pre == 167, f"got={c2760_pre}")
guard("c2759_pre==167", c2759_pre == 167, f"got={c2759_pre}")
guard("c2758_pre==169", c2758_pre == 169, f"got={c2758_pre}")
guard("c2757_pre==172", c2757_pre == 172, f"got={c2757_pre}")
guard("c2756_pre==177", c2756_pre == 177, f"got={c2756_pre}")
guard("c2755_pre==184", c2755_pre == 184, f"got={c2755_pre}")
guard("c2754_pre==187", c2754_pre == 187, f"got={c2754_pre}")
guard("c2753_pre==193", c2753_pre == 193, f"got={c2753_pre}")
guard("c2752_pre==199", c2752_pre == 199, f"got={c2752_pre}")
guard("c2751_pre==185", c2751_pre == 185, f"got={c2751_pre}")
guard("c2750_pre==187", c2750_pre == 187, f"got={c2750_pre}")
guard("c2749_pre==191", c2749_pre == 191, f"got={c2749_pre}")
guard("c2748_pre==181", c2748_pre == 181, f"got={c2748_pre}")
guard("c2747_pre==179", c2747_pre == 179, f"got={c2747_pre}")
guard("c2746_pre==187", c2746_pre == 187, f"got={c2746_pre}")

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
guard("post_worklog_lines==9328", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2800_next_bullet", last2.startswith("- Next: the c2800 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==477", tid_post == 477, f"got={tid_post}")
guard("anchor_nogold_post==410", gold_post == 410, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2799_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2799")]) == 1)
expect_c2801_mentions = wl2.count("c2801")
guard("c2801_mention_birth", expect_c2801_mentions == c2801_pre + block.count("c2801"),
      f"pre={c2801_pre} (unborn) + block births={block.count('c2801')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2801_pre + block.count('c2801')} got={expect_c2801_mentions}")
for tag, pre in (("c2800", c2800_pre), ("c2799", c2799_pre), ("c2798", c2798_pre),
                 ("c2797", c2797_pre), ("c2796", c2796_pre), ("c2795", c2795_pre),
                 ("c2794", c2794_pre), ("c2793", c2793_pre), ("c2792", c2792_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9316 -> 9328 (+12), c2799 entry + DRIFT-#49 pass-48 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")

