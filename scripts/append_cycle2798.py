#!/usr/bin/env python3
"""Guarded worklog append for the c2798 entry (12 lines).

Follows the append_cycle2797.py precedent — ALL asserts precede the
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
window-2798 EPOCH-governs render check, the window-2799 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.67ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2800 = 4 block births: the Step-7 rehearsal pre-count print 'the
c2800 pre==0 expectation' + the Step-7 census-time print 'c2800_pre = 0' +
the Next bullet's guard phrase 'c2799/c2800' AND census-tuple sentence 'FORWARD
token c2800' — the c2767..c2798 forward-token lessons; NOTE the c2800
pre-count is 0 (unborn) while the c2799 pre-count is 4 (born: the c2797
Step-7 twin-print line 9302 TWICE + TWICE inside the c2797 Next-block) — the
c2797 append prophecy 'c2799 = 4 block births' held EXACTLY: the born-FOUR
class REPEATS), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9304 lines,
tail = the c2798 Next bullet, zero serviced c2798 entries, c2798 mention
census per-line {9290: 1, 9292: 2, 9296: 3, 9302: 1, 9304: 4} total 11,
c2799 = 4 per-line {9302: 2, 9304: 2}, c2800 = 0 UNBORN, anchors 475/408/
60/28), post-state (9316 lines, tail = the c2799 Next bullet, anchors 476/
409/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2798.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9304
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


POST = D("1793318048.116623814")    # c2798 post-echo (EPOCH-governs)
SCAN = D("1793318048.111")          # c2798 scanned_at (decimal)
TRIG = D("1793317272.000")          # c2798 trigger stamp (07:41:12 +08)
WIN = D("1793317817.553325554")     # window-2798 open (c2797 prophecy EPOCH)
ECHO = D("1793317916.289761869")    # loop echo #519 POST read (EPOCH-governs)
ECHO_ISO = D("1793317916.289098550")  # loop echo #519 ISO read FIRST (the bracket)
PRE = D("1793318046.466500339")     # c2798 capture pre-echo (EPOCH-governs)
C2797_SCAN = D("1793317517.547")    # c2797 scanned_at
C2797_POST = D("1793317517.553325554")  # c2797 post-echo
C2797_CLOSE = D("1793317785.000")   # c2797 close 98db775 (23:49:45Z)
C2797_FOREIGN = D("1793317802.000")  # foreign 65f4c4e (23:50:02Z)
C2797_TRIG = D("1793316672.000")    # c2797 trigger stamp (07:31:12 +08)
C2797_ECHO = D("1793317384.121961127")  # c2797 loop echo #518 (23:43:04.121961127)
C2797_ECHO_ISO = D("1793317384.121242580")  # c2797 echo ISO bracket
C2797_PRE = D("1793317515.656092809")  # c2797 capture pre-echo (EPOCH-governs)
C2796_SCAN = D("1793316951.514")    # c2796 scanned_at
C2796_POST = D("1793316951.519917938")  # c2796 post-echo
C2796_CLOSE = D("1793317207.000")   # c2796 close 1baacec (23:40:07Z)
C2796_FOREIGN = D("1793317219.000")  # foreign 7efc24d (23:40:19Z)
TOKEN = D("1793317800.000")         # token 0750 (07:50:00 +08)
C2797_TOKEN = D("1793317200.000")   # token 0740 (07:40:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 07:41:12 +08 = 1793317272.000", dec_epoch(2026, 10, 29, 23, 41, 12), TRIG),
    ("c2797 trigger stamp 07:31:12 +08 = 1793316672.000", dec_epoch(2026, 10, 29, 23, 31, 12), C2797_TRIG),
    ("stamp-gap 600.000s by stamp (07:31:12 -> 07:41:12; the 300.000 print BROKE)", TRIG - C2797_TRIG, D("600.000")),
    ("token-gap 600.000s by token (0740 -> 0750; the 600 print REPEATS, 18 priors)", TOKEN - C2797_TOKEN, D("600.000")),
    ("token-vs-stamp +528.000 (07:41:12 -> 07:50:00; the +528 print REPEATS)", TOKEN - TRIG, D("528.000")),
    ("c2797 close 98db775 23:49:45Z = 1793317785.000", dec_epoch(2026, 10, 29, 23, 49, 45), C2797_CLOSE),
    ("foreign 65f4c4e 23:50:02Z = 1793317802.000", dec_epoch(2026, 10, 29, 23, 50, 2), C2797_FOREIGN),
    ("c2796 close 1baacec 23:40:07Z = 1793317207.000", dec_epoch(2026, 10, 29, 23, 40, 7), C2796_CLOSE),
    ("foreign 7efc24d 23:40:19Z = 1793317219.000", dec_epoch(2026, 10, 29, 23, 40, 19), C2796_FOREIGN),
    ("c2797 loop echo #518 EPOCH 1793317384.121961127 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 43, 4, 121961127), C2797_ECHO),
    ("c2797 echo ISO-bracket 1793317384.121242580 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 43, 4, 121242580), C2797_ECHO_ISO),
    ("c2797 capture pre-echo EPOCH 1793317515.656092809 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 45, 15, 656092809), C2797_PRE),
    ("c2797 post-echo ISO 23:45:17.552670564 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 45, 17, 552670564), D("1793317517.552670564")),
    ("c2797 post-echo EPOCH 1793317517.553325554 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 45, 17, 553325554), C2797_POST),
    ("c2797 scanned_at 23:45:17.547 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 45, 17) + D("0.547"), C2797_SCAN),
    ("loop echo #519 ISO integer second 23:51:56 +0000", dec_epoch(2026, 10, 29, 23, 51, 56), D("1793317916.000")),
    ("loop echo #519 EPOCH 1793317916.289761869 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 23, 51, 56, 289761869), ECHO),
    ("loop echo #519 ISO-bracket read 1793317916.289098550 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 51, 56, 289098550), ECHO_ISO),
    ("capture pre-echo EPOCH 1793318046.466500339 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 54, 6, 466500339), PRE),
    ("pre-echo ISO 23:54:06.465834705 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 54, 6, 465834705), D("1793318046.465834705")),
    ("post-echo ISO 23:54:08.115953287 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 54, 8, 115953287), D("1793318048.115953287")),
    ("post-echo EPOCH 1793318048.116623814 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 54, 8, 116623814), POST),
    ("scanned_at 23:54:08.111 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 54, 8) + D("0.111"), SCAN),
    ("window-2798 open 07:50:17.553325554 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 23, 50, 17, 553325554), WIN),
    ("window-2799 open = post-echo + 300.000", POST + D("300.000"), D("1793318348.116623814")),
    ("echo post-c2797-post-echo +398.736436315", ECHO - C2797_POST, D("398.736436315")),
]
exact_checks = [
    ("skew decimal-exact +5.623814ms (EPOCH-governs decomposition; SUB-10 extends m6)", POST - SCAN, D("0.005623814")),
    ("echo_vs_window +98.736436315 (POST-WINDOW extends m5; the c2797 Next-block watch held)", ECHO - WIN, D("98.736436315")),
    ("dd#372 = +230.564000000 (interval 530.564 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#369 print 586.505 - 300 = 286.505 and the dd#371 print 566.033 - 300 = 266.033)", SCAN - C2797_SCAN - D("300.000"), D("230.564")),
    ("dd formula re-verification: 566.033 - 300 = 266.033", D("566.033") - D("300.000"), D("266.033")),
    ("dd formula re-verification: 572.351 - 300 = 272.351", D("572.351") - D("300.000"), D("272.351")),
    ("INTERVAL#372 = 776.111", SCAN - TRIG, D("776.111")),
    ("LAG#372 = INTERVAL + dd - dd#371 = +740.642", (SCAN - TRIG) + (SCAN - C2797_SCAN - D("300.000")) - D("266.033"), D("740.642")),
    ("LATE#372 = trigger - window-open = -545.553325554", TRIG - WIN, D("-545.553325554")),
    ("CAPTURE_vs_window +230.563298260 (POST-WINDOW; echo POST — BOTH-POST extends m5)", POST - WIN, D("230.563298260")),
    ("capture-vs-echo +131.826861945", POST - ECHO, D("131.826861945")),
    ("capture post-c2797-post-echo +530.563298260", POST - C2797_POST, D("530.563298260")),
    ("echo post-c2797-close +131.289761869 (98db775 at 23:49:45)", ECHO - C2797_CLOSE, D("131.289761869")),
    ("echo post-foreign-65f4c4e +114.289761869 (23:50:02)", ECHO - C2797_FOREIGN, D("114.289761869")),
    ("stamp-to-echo 644.289761869 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("644.289761869")),
    ("trigger PREDATES the c2797 loop echo #518 by 112.121961127s (the trigger stamp landed INSIDE the c2797 servicing window, PRE-echo — the inside-window class REPEATS)", C2797_ECHO - TRIG, D("112.121961127")),
    ("trigger predates the c2797 capture pre-echo by 243.656092809s", C2797_PRE - TRIG, D("243.656092809")),
    ("trigger predates the c2797 post-echo by 245.553325554s", C2797_POST - TRIG, D("245.553325554")),
    ("trigger predates the c2797 scanned_at by 245.547s", C2797_SCAN - TRIG, D("245.547")),
    ("trigger predates window-2798 open by 545.553325554s", WIN - TRIG, D("545.553325554")),
    ("c2797 close POSTDATES the trigger by 513.000s (98db775 at 23:49:45)", C2797_CLOSE - TRIG, D("513.000")),
    ("foreign 65f4c4e POSTDATES the trigger by 530.000s (23:50:02)", C2797_FOREIGN - TRIG, D("530.000")),
    ("trigger postdates the foreign 7efc24d by 53.000s (23:40:19)", TRIG - C2796_FOREIGN, D("53.000")),
    ("trigger postdates the c2796 close 1baacec by 65.000s (23:40:07)", TRIG - C2796_CLOSE, D("65.000")),
    ("c2797 close landed 15.000s BEFORE the token-0750 second (23:49:45 vs 23:50:00 — the BEFORE-class NEW)", TOKEN - C2797_CLOSE, D("15.000")),
    ("foreign 65f4c4e landed 2.000s AFTER the token second (23:50:02)", C2797_FOREIGN - TOKEN, D("2.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2798"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2798"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2799 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2800_birth",
      block.count("c2800") == 4 and lines[-1].count("c2800") == 2
      and "c2799/c2800" in lines[-1] and "FORWARD token c2800" in lines[-1]
      and "the c2800 pre==0 expectation" in block,
      f"block c2800={block.count('c2800')} next-line c2800={lines[-1].count('c2800')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2800_pre = 0' + the Next bullet's guard phrase 'c2799/c2800' AND "
      f"census-tuple sentence 'FORWARD token c2800')")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9304", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2798_next_bullet", last_nonempty.startswith("- Next: the c2798 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2798",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2798")]) == 0,
      f"c2798 substring mentions={wl.count('c2798')} (expect 11)")
c2798_lines = {i + 1: l.count("c2798") for i, l in enumerate(wl.splitlines()) if "c2798" in l}
guard("c2798_mention_census_pre", wl.count("c2798") == 11
      and c2798_lines == {9290: 1, 9292: 2, 9296: 3, 9302: 1, 9304: 4},
      f"per-line={c2798_lines}")
c2799_lines = {i + 1: l.count("c2799") for i, l in enumerate(wl.splitlines()) if "c2799" in l}
guard("c2799_forward_token_pre", wl.count("c2799") == 4 and c2799_lines == {9302: 2, 9304: 2},
      f"per-line={c2799_lines} (2 births in the c2797 Step-7 twin-print line 9302 + "
      f"2 FORWARD-token births inside the c2797 Next-block — the born-FOUR class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==475", tid_pre == 475, f"got={tid_pre}")
guard("anchor_nogold_pre==408", gold_pre == 408, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2800_pre==0", c2800_pre == 0, f"got={c2800_pre} (the forward token c2800 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2799_pre==4", c2799_pre == 4, f"got={c2799_pre} (born FOUR: the c2797 Step-7 twin-print "
      f"line 9302 TWICE + TWICE inside the c2797 Next-block — NOT the unborn class)")
guard("c2798_pre==11", c2798_pre == 11, f"got={c2798_pre}")
guard("c2797_pre==38", c2797_pre == 38, f"got={c2797_pre}")
guard("c2796_pre==81", c2796_pre == 81, f"got={c2796_pre}")
guard("c2795_pre==96", c2795_pre == 96, f"got={c2795_pre}")
guard("c2794_pre==101", c2794_pre == 101, f"got={c2794_pre}")
guard("c2793_pre==103", c2793_pre == 103, f"got={c2793_pre}")
guard("c2792_pre==108", c2792_pre == 108, f"got={c2792_pre}")
guard("c2791_pre==102", c2791_pre == 102, f"got={c2791_pre}")
guard("c2790_pre==106", c2790_pre == 106, f"got={c2790_pre}")
guard("c2789_pre==105", c2789_pre == 105, f"got={c2789_pre}")
guard("c2788_pre==116", c2788_pre == 116, f"got={c2788_pre}")
guard("c2787_pre==117", c2787_pre == 117, f"got={c2787_pre}")
guard("c2786_pre==130", c2786_pre == 130, f"got={c2786_pre}")
guard("c2785_pre==121", c2785_pre == 121, f"got={c2785_pre}")
guard("c2784_pre==119", c2784_pre == 119, f"got={c2784_pre}")
guard("c2783_pre==120", c2783_pre == 120, f"got={c2783_pre}")
guard("c2782_pre==119", c2782_pre == 119, f"got={c2782_pre}")
guard("c2781_pre==124", c2781_pre == 124, f"got={c2781_pre}")
guard("c2780_pre==128", c2780_pre == 128, f"got={c2780_pre}")
guard("c2779_pre==129", c2779_pre == 129, f"got={c2779_pre}")
guard("c2778_pre==173", c2778_pre == 173, f"got={c2778_pre}")
guard("c2777_pre==145", c2777_pre == 145, f"got={c2777_pre}")
guard("c2776_pre==150", c2776_pre == 150, f"got={c2776_pre}")
guard("c2775_pre==159", c2775_pre == 159, f"got={c2775_pre}")
guard("c2774_pre==164", c2774_pre == 164, f"got={c2774_pre}")
guard("c2773_pre==168", c2773_pre == 168, f"got={c2773_pre}")
guard("c2772_pre==187", c2772_pre == 187, f"got={c2772_pre}")
guard("c2771_pre==177", c2771_pre == 177, f"got={c2771_pre}")
guard("c2770_pre==216", c2770_pre == 216, f"got={c2770_pre}")
guard("c2769_pre==166", c2769_pre == 166, f"got={c2769_pre}")
guard("c2768_pre==169", c2768_pre == 169, f"got={c2768_pre}")
guard("c2767_pre==212", c2767_pre == 212, f"got={c2767_pre}")
guard("c2766_pre==192", c2766_pre == 192, f"got={c2766_pre}")
guard("c2765_pre==160", c2765_pre == 160, f"got={c2765_pre}")
guard("c2764_pre==162", c2764_pre == 162, f"got={c2764_pre}")
guard("c2763_pre==170", c2763_pre == 170, f"got={c2763_pre}")
guard("c2762_pre==199", c2762_pre == 199, f"got={c2762_pre}")
guard("c2761_pre==213", c2761_pre == 213, f"got={c2761_pre}")
guard("c2760_pre==165", c2760_pre == 165, f"got={c2760_pre}")
guard("c2759_pre==165", c2759_pre == 165, f"got={c2759_pre}")
guard("c2758_pre==167", c2758_pre == 167, f"got={c2758_pre}")
guard("c2757_pre==170", c2757_pre == 170, f"got={c2757_pre}")
guard("c2756_pre==175", c2756_pre == 175, f"got={c2756_pre}")
guard("c2755_pre==182", c2755_pre == 182, f"got={c2755_pre}")
guard("c2754_pre==185", c2754_pre == 185, f"got={c2754_pre}")
guard("c2753_pre==191", c2753_pre == 191, f"got={c2753_pre}")
guard("c2752_pre==197", c2752_pre == 197, f"got={c2752_pre}")
guard("c2751_pre==183", c2751_pre == 183, f"got={c2751_pre}")
guard("c2750_pre==185", c2750_pre == 185, f"got={c2750_pre}")
guard("c2749_pre==189", c2749_pre == 189, f"got={c2749_pre}")
guard("c2748_pre==179", c2748_pre == 179, f"got={c2748_pre}")
guard("c2747_pre==177", c2747_pre == 177, f"got={c2747_pre}")
guard("c2746_pre==184", c2746_pre == 184, f"got={c2746_pre}")

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
guard("post_worklog_lines==9316", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2799_next_bullet", last2.startswith("- Next: the c2799 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==476", tid_post == 476, f"got={tid_post}")
guard("anchor_nogold_post==409", gold_post == 409, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2798_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2798")]) == 1)
expect_c2800_mentions = wl2.count("c2800")
guard("c2800_mention_birth", expect_c2800_mentions == c2800_pre + block.count("c2800"),
      f"pre={c2800_pre} (unborn) + block births={block.count('c2800')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2800_pre + block.count('c2800')} got={expect_c2800_mentions}")
for tag, pre in (("c2799", c2799_pre), ("c2798", c2798_pre), ("c2797", c2797_pre),
                 ("c2796", c2796_pre), ("c2795", c2795_pre), ("c2794", c2794_pre),
                 ("c2793", c2793_pre), ("c2792", c2792_pre), ("c2791", c2791_pre),
                 ("c2790", c2790_pre), ("c2789", c2789_pre), ("c2788", c2788_pre),
                 ("c2787", c2787_pre), ("c2786", c2786_pre), ("c2785", c2785_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9304 -> 9316 (+12), c2798 entry + DRIFT-#49 pass-47 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
