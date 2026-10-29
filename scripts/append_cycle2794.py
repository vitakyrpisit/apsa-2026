#!/usr/bin/env python3
"""Guarded worklog append for the c2794 entry (12 lines).

Follows the append_cycle2793.py precedent — ALL asserts precede the
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
window-2794 EPOCH-governs render check, the window-2795 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.7ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2796 = 3 block births: the Step-7 rehearsal pre-count print 'the
c2796 pre==0 expectation' + the Next bullet's guard phrase 'c2795/c2796' AND
census-tuple sentence 'FORWARD token c2796' — the c2767..c2794 forward-token
lessons; NOTE the c2796 pre-count is 0 (unborn) while the c2795 pre-count is
3 (born: the c2793 Step-7 rehearsal print + TWICE inside the c2793
Next-block) — the c2783 c2788-pre==2 class EVOLVED: the c2795 forward token
was born THRICE across the c2793 block, measured at census time per-line
{9254: 1, 9256: 2}, NOT the unborn class), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9256 lines, tail = the c2794 Next bullet, zero serviced c2794
entries, c2794 mention census per-line {9242: 1, 9244: 2, 9248: 1, 9254: 1,
9256: 4}, c2795 = 3 per-line {9254: 1, 9256: 2}, anchors 471/404/60/28),
post-state (9268 lines, tail = the c2795 Next bullet, anchors 472/405/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2794.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9256
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


POST = D("1793315792.663933005")    # c2794 post-echo (EPOCH-governs)
SCAN = D("1793315792.658")          # c2794 scanned_at (decimal)
TRIG = D("1793314871.000")          # c2794 trigger stamp (07:01:11 +08)
WIN = D("1793315466.905636634")     # window-2794 open (c2793 prophecy EPOCH)
ECHO = D("1793315790.726705467")    # loop echo #515 POST read (EPOCH-governs)
ECHO_ISO = D("1793315790.725965515")  # loop echo #515 ISO read FIRST (the bracket)
PRE = D("1793315790.730105682")     # c2794 capture pre-echo (EPOCH-governs)
C2793_SCAN = D("1793315166.899")    # c2793 scanned_at
C2793_POST = D("1793315166.905636634")  # c2793 post-echo
C2793_CLOSE = D("1793315434.000")   # c2793 close a27965c (23:10:34Z)
C2793_FOREIGN = D("1793315452.000")  # foreign 4477b73 (23:10:52Z)
C2793_TRIG = D("1793314581.000")    # c2793 trigger stamp (06:56:21 +08)
C2793_ECHO = D("1793315019.627789461")  # c2793 loop echo #514 (23:03:39.627789461)
C2793_ECHO_ISO = D("1793315019.627192770")  # c2793 echo ISO bracket
C2793_PRE = D("1793315165.054329661")  # c2793 capture pre-echo (EPOCH-governs)
C2792_SCAN = D("1793314722.153")    # c2792 scanned_at
C2792_CLOSE = D("1793314950.000")   # c2792 close 99f6ee6 (23:02:30Z)
C2791_CLOSE = D("1793314387.000")   # c2791 close f6f24d7 (22:53:07Z)
C2791_FOREIGN = D("1793314407.000")  # foreign 18522dc (22:53:27Z)
TOKEN = D("1793315400.000")         # token 0710 (07:10:00 +08)
C2793_TOKEN = D("1793314920.000")   # token 0702 (07:02:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 07:01:11 +08 = 1793314871.000", dec_epoch(2026, 10, 29, 23, 1, 11), TRIG),
    ("c2793 trigger stamp 06:56:21 +08 = 1793314581.000", dec_epoch(2026, 10, 29, 22, 56, 21), C2793_TRIG),
    ("stamp-gap 290.000s by stamp (06:56:21 -> 07:01:11; the 290 print is NEW, zero priors)", TRIG - C2793_TRIG, D("290.000")),
    ("token-gap 480.000s by token (0702 -> 0710; the 480 print REPEATS, 20 priors)", TOKEN - C2793_TOKEN, D("480.000")),
    ("token-vs-stamp +529.000 (07:01:11 -> 07:10:00; the +529 print REPEATS, 9 multi-surface priors)", TOKEN - TRIG, D("529.000")),
    ("c2793 close a27965c 23:10:34Z = 1793315434.000", dec_epoch(2026, 10, 29, 23, 10, 34), C2793_CLOSE),
    ("foreign 4477b73 23:10:52Z = 1793315452.000", dec_epoch(2026, 10, 29, 23, 10, 52), C2793_FOREIGN),
    ("c2792 close 99f6ee6 23:02:30Z = 1793314950.000", dec_epoch(2026, 10, 29, 23, 2, 30), C2792_CLOSE),
    ("c2791 close f6f24d7 22:53:07Z = 1793314387.000", dec_epoch(2026, 10, 29, 22, 53, 7), C2791_CLOSE),
    ("foreign 18522dc 22:53:27Z = 1793314407.000", dec_epoch(2026, 10, 29, 22, 53, 27), C2791_FOREIGN),
    ("c2793 loop echo EPOCH 1793315019.627789461 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 3, 39, 627789461), C2793_ECHO),
    ("c2793 echo ISO-bracket 1793315019.627192770 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 3, 39, 627192770), C2793_ECHO_ISO),
    ("c2793 capture pre-echo EPOCH 1793315165.054329661 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 6, 5, 54329661), C2793_PRE),
    ("c2793 post-echo ISO 23:06:06.904955343 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 6, 6, 904955343), D("1793315166.904955343")),
    ("c2793 post-echo EPOCH 1793315166.905636634 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 6, 6, 905636634), C2793_POST),
    ("c2793 scanned_at 23:06:06.899 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 6, 6) + D("0.899"), C2793_SCAN),
    ("c2792 scanned_at 22:58:42.153 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 58, 42) + D("0.153"), C2792_SCAN),
    ("loop echo #515 ISO integer second 23:16:30 +0000", dec_epoch(2026, 10, 29, 23, 16, 30), D("1793315790.000")),
    ("loop echo #515 EPOCH 1793315790.726705467 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 23, 16, 30, 726705467), ECHO),
    ("loop echo #515 ISO-bracket read 1793315790.725965515 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 16, 30, 725965515), ECHO_ISO),
    ("capture pre-echo EPOCH 1793315790.730105682 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 30, 730105682), PRE),
    ("pre-echo ISO 23:16:30.729455766 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 16, 30, 729455766), D("1793315790.729455766")),
    ("post-echo ISO 23:16:32.663244336 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 16, 32, 663244336), D("1793315792.663244336")),
    ("post-echo EPOCH 1793315792.663933005 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 32, 663933005), POST),
    ("scanned_at 23:16:32.658 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 16, 32) + D("0.658"), SCAN),
    ("window-2794 open 07:11:06.905636634 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 23, 11, 6, 905636634), WIN),
    ("window-2795 open = post-echo + 300.000", POST + D("300.000"), D("1793316092.663933005")),
    ("echo post-c2793-post-echo +623.821068833", ECHO - C2793_POST, D("623.821068833")),
]
exact_checks = [
    ("skew decimal-exact +5.933005ms (EPOCH-governs decomposition; SUB-10 extends m2)", POST - SCAN, D("0.005933005")),
    ("echo_vs_window +323.821068833 (POST-WINDOW re-opens m1; the PRE-WINDOW m3 TERMINATES)", ECHO - WIN, D("323.821068833")),
    ("dd#368 = +325.759000000 (interval 625.759 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#366 print 499.913 - 300 = 199.913 and the dd#367 print 444.746 - 300 = 144.746)", SCAN - C2793_SCAN - D("300.000"), D("325.759")),
    ("dd formula re-verification: 499.913 - 300 = 199.913", D("499.913") - D("300.000"), D("199.913")),
    ("dd formula re-verification: 444.746 - 300 = 144.746", D("444.746") - D("300.000"), D("144.746")),
    ("INTERVAL#368 = 921.658", SCAN - TRIG, D("921.658")),
    ("LAG#368 = INTERVAL + dd - dd#367 = +1102.671", (SCAN - TRIG) + (SCAN - C2793_SCAN - D("300.000")) - D("144.746"), D("1102.671")),
    ("LATE#368 = trigger - window-open = -595.905636634", TRIG - WIN, D("-595.905636634")),
    ("CAPTURE_vs_window +325.758296371 (POST-WINDOW; echo POST — BOTH-POST opens m1)", POST - WIN, D("325.758296371")),
    ("capture-vs-echo +1.937227538", POST - ECHO, D("1.937227538")),
    ("capture post-c2793-post-echo +625.758296371", POST - C2793_POST, D("625.758296371")),
    ("echo post-c2793-close +356.726705467 (a27965c at 23:10:34)", ECHO - C2793_CLOSE, D("356.726705467")),
    ("echo post-foreign-4477b73 +338.726705467 (23:10:52)", ECHO - C2793_FOREIGN, D("338.726705467")),
    ("stamp-to-echo 919.726705467 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("919.726705467")),
    ("trigger predates the c2793 loop echo #514 by 148.627789461s (the trigger landed INSIDE the c2793 servicing window, pre-echo pre-capture)", C2793_ECHO - TRIG, D("148.627789461")),
    ("trigger predates the c2793 capture pre-echo by 294.054329661s", C2793_PRE - TRIG, D("294.054329661")),
    ("trigger predates the c2793 post-echo by 295.905636634s", C2793_POST - TRIG, D("295.905636634")),
    ("trigger predates window-2794 open by 595.905636634s", WIN - TRIG, D("595.905636634")),
    ("c2793 close POSTDATES the trigger by 563.000s (a27965c at 23:10:34)", C2793_CLOSE - TRIG, D("563.000")),
    ("foreign 4477b73 POSTDATES the trigger by 581.000s (23:10:52)", C2793_FOREIGN - TRIG, D("581.000")),
    ("c2792 close POSTDATES the trigger by 79.000s (99f6ee6 at 23:02:30)", C2792_CLOSE - TRIG, D("79.000")),
    ("trigger postdates c2791 close by 484.000s (f6f24d7 at 22:53:07)", TRIG - C2791_CLOSE, D("484.000")),
    ("trigger postdates the foreign 18522dc by 464.000s (22:53:27)", TRIG - C2791_FOREIGN, D("464.000")),
    ("c2793 close landed 34.000s AFTER the token second (23:10:34 vs 23:10:00)", C2793_CLOSE - TOKEN, D("34.000")),
    ("foreign 4477b73 landed 52.000s AFTER the token second (23:10:52)", C2793_FOREIGN - TOKEN, D("52.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2794"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2794"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2795 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2796_birth",
      block.count("c2796") == 3 and lines[-1].count("c2796") == 2
      and "c2795/c2796" in lines[-1] and "FORWARD token c2796" in lines[-1]
      and "the c2796 pre==0 expectation" in block,
      f"block c2796={block.count('c2796')} next-line c2796={lines[-1].count('c2796')} "
      f"(expect 3: the Step-7 rehearsal pre-count print + the Next bullet's guard "
      f"phrase 'c2795/c2796' AND census-tuple sentence 'FORWARD token c2796')")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9256", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2794_next_bullet", last_nonempty.startswith("- Next: the c2794 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2794",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2794")]) == 0,
      f"c2794 substring mentions={wl.count('c2794')} (expect 9)")
c2794_lines = {i + 1: l.count("c2794") for i, l in enumerate(wl.splitlines()) if "c2794" in l}
guard("c2794_mention_census_pre", wl.count("c2794") == 9
      and c2794_lines == {9242: 1, 9244: 2, 9248: 1, 9254: 1, 9256: 4},
      f"per-line={c2794_lines}")
c2795_lines = {i + 1: l.count("c2795") for i, l in enumerate(wl.splitlines()) if "c2795" in l}
guard("c2795_forward_token_pre", wl.count("c2795") == 3 and c2795_lines == {9254: 1, 9256: 2},
      f"per-line={c2795_lines} (1 birth in the c2793 Step-7 rehearsal print + 2 "
      f"FORWARD-token births inside the c2793 Next-block — the born-thrice class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==471", tid_pre == 471, f"got={tid_pre}")
guard("anchor_nogold_pre==404", gold_pre == 404, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2796_pre==0", c2796_pre == 0, f"got={c2796_pre} (the forward token c2796 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2795_pre==3", c2795_pre == 3, f"got={c2795_pre} (born THRICE: the c2793 Step-7 "
      f"rehearsal print + TWICE inside the c2793 Next-block — NOT the unborn class)")
guard("c2794_pre==9", c2794_pre == 9, f"got={c2794_pre}")
guard("c2793_pre==36", c2793_pre == 36, f"got={c2793_pre}")
guard("c2792_pre==81", c2792_pre == 81, f"got={c2792_pre}")
guard("c2791_pre==87", c2791_pre == 87, f"got={c2791_pre}")
guard("c2790_pre==87", c2790_pre == 87, f"got={c2790_pre}")
guard("c2789_pre==91", c2789_pre == 91, f"got={c2789_pre}")
guard("c2788_pre==102", c2788_pre == 102, f"got={c2788_pre}")
guard("c2787_pre==103", c2787_pre == 103, f"got={c2787_pre}")
guard("c2786_pre==112", c2786_pre == 112, f"got={c2786_pre}")
guard("c2785_pre==107", c2785_pre == 107, f"got={c2785_pre}")
guard("c2784_pre==105", c2784_pre == 105, f"got={c2784_pre}")
guard("c2783_pre==106", c2783_pre == 106, f"got={c2783_pre}")
guard("c2782_pre==105", c2782_pre == 105, f"got={c2782_pre}")
guard("c2781_pre==110", c2781_pre == 110, f"got={c2781_pre}")
guard("c2780_pre==114", c2780_pre == 114, f"got={c2780_pre}")
guard("c2779_pre==115", c2779_pre == 115, f"got={c2779_pre}")
guard("c2778_pre==154", c2778_pre == 154, f"got={c2778_pre}")
guard("c2777_pre==131", c2777_pre == 131, f"got={c2777_pre}")
guard("c2776_pre==136", c2776_pre == 136, f"got={c2776_pre}")
guard("c2775_pre==145", c2775_pre == 145, f"got={c2775_pre}")
guard("c2774_pre==150", c2774_pre == 150, f"got={c2774_pre}")
guard("c2773_pre==154", c2773_pre == 154, f"got={c2773_pre}")
guard("c2772_pre==173", c2772_pre == 173, f"got={c2772_pre}")
guard("c2771_pre==163", c2771_pre == 163, f"got={c2771_pre}")
guard("c2770_pre==198", c2770_pre == 198, f"got={c2770_pre}")
guard("c2769_pre==152", c2769_pre == 152, f"got={c2769_pre}")
guard("c2768_pre==155", c2768_pre == 155, f"got={c2768_pre}")
guard("c2767_pre==190", c2767_pre == 190, f"got={c2767_pre}")
guard("c2766_pre==174", c2766_pre == 174, f"got={c2766_pre}")
guard("c2765_pre==146", c2765_pre == 146, f"got={c2765_pre}")
guard("c2764_pre==148", c2764_pre == 148, f"got={c2764_pre}")
guard("c2763_pre==156", c2763_pre == 156, f"got={c2763_pre}")
guard("c2762_pre==181", c2762_pre == 181, f"got={c2762_pre}")
guard("c2761_pre==195", c2761_pre == 195, f"got={c2761_pre}")
guard("c2760_pre==151", c2760_pre == 151, f"got={c2760_pre}")
guard("c2759_pre==151", c2759_pre == 151, f"got={c2759_pre}")
guard("c2758_pre==153", c2758_pre == 153, f"got={c2758_pre}")
guard("c2757_pre==156", c2757_pre == 156, f"got={c2757_pre}")
guard("c2756_pre==161", c2756_pre == 161, f"got={c2756_pre}")
guard("c2755_pre==168", c2755_pre == 168, f"got={c2755_pre}")
guard("c2754_pre==171", c2754_pre == 171, f"got={c2754_pre}")
guard("c2753_pre==177", c2753_pre == 177, f"got={c2753_pre}")
guard("c2752_pre==183", c2752_pre == 183, f"got={c2752_pre}")
guard("c2751_pre==169", c2751_pre == 169, f"got={c2751_pre}")
guard("c2750_pre==171", c2750_pre == 171, f"got={c2750_pre}")
guard("c2749_pre==175", c2749_pre == 175, f"got={c2749_pre}")
guard("c2748_pre==165", c2748_pre == 165, f"got={c2748_pre}")
guard("c2747_pre==163", c2747_pre == 163, f"got={c2747_pre}")
guard("c2746_pre==166", c2746_pre == 166, f"got={c2746_pre}")

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
guard("post_worklog_lines==9268", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2795_next_bullet", last2.startswith("- Next: the c2795 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==472", tid_post == 472, f"got={tid_post}")
guard("anchor_nogold_post==405", gold_post == 405, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2794_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2794")]) == 1)
expect_c2796_mentions = wl2.count("c2796")
guard("c2796_mention_birth", expect_c2796_mentions == c2796_pre + block.count("c2796"),
      f"pre={c2796_pre} (unborn) + block births={block.count('c2796')} (Step-7 pre-count "
      f"print + guard phrase + census-tuple sentence) -> expect={c2796_pre + block.count('c2796')} got={expect_c2796_mentions}")
for tag, pre in (("c2795", c2795_pre), ("c2794", c2794_pre), ("c2793", c2793_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9256 -> 9268 (+12), c2794 entry + DRIFT-#49 pass-43 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")

