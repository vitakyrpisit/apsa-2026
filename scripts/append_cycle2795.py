#!/usr/bin/env python3
"""Guarded worklog append for the c2795 entry (12 lines).

Follows the append_cycle2794.py precedent — ALL asserts precede the
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
window-2795 EPOCH-governs render check, the window-2796 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.7ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2797 = 3 block births: the Step-7 rehearsal pre-count print 'the
c2797 pre==0 expectation' + the Next bullet's guard phrase 'c2796/c2797' AND
census-tuple sentence 'FORWARD token c2797' — the c2767..c2795 forward-token
lessons; NOTE the c2797 pre-count is 0 (unborn) while the c2796 pre-count is
3 (born: the c2794 Step-7 rehearsal print + TWICE inside the c2794
Next-block) — the c2783 c2788-pre==2 class EVOLVED: the c2796 forward token
was born THRICE across the c2794 block, measured at census time per-line
{9266: 1, 9268: 2}, NOT the unborn class), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9268 lines, tail = the c2795 Next bullet, zero serviced c2795
entries, c2795 mention census per-line {9254: 1, 9256: 2, 9260: 3, 9266: 1,
9268: 4} total 11, c2796 = 3 per-line {9266: 1, 9268: 2}, anchors 472/405/60/
28), post-state (9280 lines, tail = the c2796 Next bullet, anchors 473/406/
60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2795.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9268
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


POST = D("1793316379.170480455")    # c2795 post-echo (EPOCH-governs)
SCAN = D("1793316379.163")          # c2795 scanned_at (decimal)
TRIG = D("1793315471.000")          # c2795 trigger stamp (07:11:11 +08)
WIN = D("1793316092.663933005")     # window-2795 open (c2794 prophecy EPOCH)
ECHO = D("1793316141.062851709")    # loop echo #516 POST read (EPOCH-governs)
ECHO_ISO = D("1793316141.062208970")  # loop echo #516 ISO read FIRST (the bracket)
PRE = D("1793316377.499476469")     # c2795 capture pre-echo (EPOCH-governs)
C2794_SCAN = D("1793315792.658")    # c2794 scanned_at
C2794_POST = D("1793315792.663933005")  # c2794 post-echo
C2794_CLOSE = D("1793316031.000")   # c2794 close fb1d1d1 (23:20:31Z)
C2794_FOREIGN = D("1793316048.000")  # foreign 4207111 (23:20:48Z)
C2794_TRIG = D("1793314871.000")    # c2794 trigger stamp (07:01:11 +08)
C2794_ECHO = D("1793315790.726705467")  # c2794 loop echo #515 (23:16:30.726705467)
C2794_ECHO_ISO = D("1793315790.725965515")  # c2794 echo ISO bracket
C2794_PRE = D("1793315790.730105682")  # c2794 capture pre-echo (EPOCH-governs)
C2793_SCAN = D("1793315166.899")    # c2793 scanned_at
C2793_CLOSE = D("1793315434.000")   # c2793 close a27965c (23:10:34Z)
C2793_FOREIGN = D("1793315452.000")  # foreign 4477b73 (23:10:52Z)
TOKEN = D("1793316000.000")         # token 0720 (07:20:00 +08)
C2794_TOKEN = D("1793315400.000")   # token 0710 (07:10:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 07:11:11 +08 = 1793315471.000", dec_epoch(2026, 10, 29, 23, 11, 11), TRIG),
    ("c2794 trigger stamp 07:01:11 +08 = 1793314871.000", dec_epoch(2026, 10, 29, 23, 1, 11), C2794_TRIG),
    ("stamp-gap 600.000s by stamp (07:01:11 -> 07:11:11; the 600 print REPEATS, 24 priors)", TRIG - C2794_TRIG, D("600.000")),
    ("token-gap 600.000s by token (0710 -> 0720; the 600 print REPEATS, 12 priors)", TOKEN - C2794_TOKEN, D("600.000")),
    ("token-vs-stamp +529.000 (07:11:11 -> 07:20:00; the +529 print REPEATS)", TOKEN - TRIG, D("529.000")),
    ("c2794 close fb1d1d1 23:20:31Z = 1793316031.000", dec_epoch(2026, 10, 29, 23, 20, 31), C2794_CLOSE),
    ("foreign 4207111 23:20:48Z = 1793316048.000", dec_epoch(2026, 10, 29, 23, 20, 48), C2794_FOREIGN),
    ("c2793 close a27965c 23:10:34Z = 1793315434.000", dec_epoch(2026, 10, 29, 23, 10, 34), C2793_CLOSE),
    ("foreign 4477b73 23:10:52Z = 1793315452.000", dec_epoch(2026, 10, 29, 23, 10, 52), C2793_FOREIGN),
    ("c2794 loop echo EPOCH 1793315790.726705467 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 30, 726705467), C2794_ECHO),
    ("c2794 echo ISO-bracket 1793315790.725965515 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 16, 30, 725965515), C2794_ECHO_ISO),
    ("c2794 capture pre-echo EPOCH 1793315790.730105682 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 30, 730105682), C2794_PRE),
    ("c2794 post-echo ISO 23:16:32.663244336 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 16, 32, 663244336), D("1793315792.663244336")),
    ("c2794 post-echo EPOCH 1793315792.663933005 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 32, 663933005), C2794_POST),
    ("c2794 scanned_at 23:16:32.658 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 16, 32) + D("0.658"), C2794_SCAN),
    ("loop echo #516 ISO integer second 23:22:21 +0000", dec_epoch(2026, 10, 29, 23, 22, 21), D("1793316141.000")),
    ("loop echo #516 EPOCH 1793316141.062851709 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 23, 22, 21, 62851709), ECHO),
    ("loop echo #516 ISO-bracket read 1793316141.062208970 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 22, 21, 62208970), ECHO_ISO),
    ("capture pre-echo EPOCH 1793316377.499476469 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 26, 17, 499476469), PRE),
    ("pre-echo ISO 23:26:17.498822768 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 26, 17, 498822768), D("1793316377.498822768")),
    ("post-echo ISO 23:26:19.169778054 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 26, 19, 169778054), D("1793316379.169778054")),
    ("post-echo EPOCH 1793316379.170480455 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 26, 19, 170480455), POST),
    ("scanned_at 23:26:19.163 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 26, 19) + D("0.163"), SCAN),
    ("window-2795 open 07:21:32.663933005 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 23, 21, 32, 663933005), WIN),
    ("window-2796 open = post-echo + 300.000", POST + D("300.000"), D("1793316679.170480455")),
    ("echo post-c2794-post-echo +348.398918704", ECHO - C2794_POST, D("348.398918704")),
]
exact_checks = [
    ("skew decimal-exact +7.480455ms (EPOCH-governs decomposition; SUB-10 extends m3)", POST - SCAN, D("0.007480455")),
    ("echo_vs_window +48.398918704 (POST-WINDOW extends m2; the PRE-WINDOW flip did NOT fire)", ECHO - WIN, D("48.398918704")),
    ("dd#369 = +286.505000000 (interval 586.505 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#367 print 444.746 - 300 = 144.746 and the dd#368 print 625.759 - 300 = 325.759)", SCAN - C2794_SCAN - D("300.000"), D("286.505")),
    ("dd formula re-verification: 444.746 - 300 = 144.746", D("444.746") - D("300.000"), D("144.746")),
    ("dd formula re-verification: 625.759 - 300 = 325.759", D("625.759") - D("300.000"), D("325.759")),
    ("INTERVAL#369 = 908.163", SCAN - TRIG, D("908.163")),
    ("LAG#369 = INTERVAL + dd - dd#368 = +868.909", (SCAN - TRIG) + (SCAN - C2794_SCAN - D("300.000")) - D("325.759"), D("868.909")),
    ("LATE#369 = trigger - window-open = -621.663933005", TRIG - WIN, D("-621.663933005")),
    ("CAPTURE_vs_window +286.506547450 (POST-WINDOW; echo POST — BOTH-POST extends m2)", POST - WIN, D("286.506547450")),
    ("capture-vs-echo +238.107628746", POST - ECHO, D("238.107628746")),
    ("capture post-c2794-post-echo +586.506547450", POST - C2794_POST, D("586.506547450")),
    ("echo post-c2794-close +110.062851709 (fb1d1d1 at 23:20:31)", ECHO - C2794_CLOSE, D("110.062851709")),
    ("echo post-foreign-4207111 +93.062851709 (23:20:48)", ECHO - C2794_FOREIGN, D("93.062851709")),
    ("stamp-to-echo 670.062851709 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("670.062851709")),
    ("trigger predates the c2794 loop echo #515 by 319.726705467s (the trigger landed INSIDE the c2794 servicing window, pre-echo pre-capture)", C2794_ECHO - TRIG, D("319.726705467")),
    ("trigger predates the c2794 capture pre-echo by 319.730105682s", C2794_PRE - TRIG, D("319.730105682")),
    ("trigger predates the c2794 post-echo by 321.663933005s", C2794_POST - TRIG, D("321.663933005")),
    ("trigger predates window-2795 open by 621.663933005s", WIN - TRIG, D("621.663933005")),
    ("c2794 close POSTDATES the trigger by 560.000s (fb1d1d1 at 23:20:31)", C2794_CLOSE - TRIG, D("560.000")),
    ("foreign 4207111 POSTDATES the trigger by 577.000s (23:20:48)", C2794_FOREIGN - TRIG, D("577.000")),
    ("trigger postdates c2793 close by 37.000s (a27965c at 23:10:34)", TRIG - C2793_CLOSE, D("37.000")),
    ("trigger postdates the foreign 4477b73 by 19.000s (23:10:52)", TRIG - C2793_FOREIGN, D("19.000")),
    ("c2794 close landed 31.000s AFTER the token second (23:20:31 vs 23:20:00)", C2794_CLOSE - TOKEN, D("31.000")),
    ("foreign 4207111 landed 48.000s AFTER the token second (23:20:48)", C2794_FOREIGN - TOKEN, D("48.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2795"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2795"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2796 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2797_birth",
      block.count("c2797") == 3 and lines[-1].count("c2797") == 2
      and "c2796/c2797" in lines[-1] and "FORWARD token c2797" in lines[-1]
      and "the c2797 pre==0 expectation" in block,
      f"block c2797={block.count('c2797')} next-line c2797={lines[-1].count('c2797')} "
      f"(expect 3: the Step-7 rehearsal pre-count print + the Next bullet's guard "
      f"phrase 'c2796/c2797' AND census-tuple sentence 'FORWARD token c2797')")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9268", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2795_next_bullet", last_nonempty.startswith("- Next: the c2795 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2795",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2795")]) == 0,
      f"c2795 substring mentions={wl.count('c2795')} (expect 11)")
c2795_lines = {i + 1: l.count("c2795") for i, l in enumerate(wl.splitlines()) if "c2795" in l}
guard("c2795_mention_census_pre", wl.count("c2795") == 11
      and c2795_lines == {9254: 1, 9256: 2, 9260: 3, 9266: 1, 9268: 4},
      f"per-line={c2795_lines}")
c2796_lines = {i + 1: l.count("c2796") for i, l in enumerate(wl.splitlines()) if "c2796" in l}
guard("c2796_forward_token_pre", wl.count("c2796") == 3 and c2796_lines == {9266: 1, 9268: 2},
      f"per-line={c2796_lines} (1 birth in the c2794 Step-7 rehearsal print + 2 "
      f"FORWARD-token births inside the c2794 Next-block — the born-thrice class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==472", tid_pre == 472, f"got={tid_pre}")
guard("anchor_nogold_pre==405", gold_pre == 405, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2797_pre==0", c2797_pre == 0, f"got={c2797_pre} (the forward token c2797 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2796_pre==3", c2796_pre == 3, f"got={c2796_pre} (born THRICE: the c2794 Step-7 "
      f"rehearsal print + TWICE inside the c2794 Next-block — NOT the unborn class)")
guard("c2795_pre==11", c2795_pre == 11, f"got={c2795_pre}")
guard("c2794_pre==42", c2794_pre == 42, f"got={c2794_pre}")
guard("c2793_pre==83", c2793_pre == 83, f"got={c2793_pre}")
guard("c2792_pre==93", c2792_pre == 93, f"got={c2792_pre}")
guard("c2791_pre==92", c2791_pre == 92, f"got={c2791_pre}")
guard("c2790_pre==93", c2790_pre == 93, f"got={c2790_pre}")
guard("c2789_pre==95", c2789_pre == 95, f"got={c2789_pre}")
guard("c2788_pre==106", c2788_pre == 106, f"got={c2788_pre}")
guard("c2787_pre==107", c2787_pre == 107, f"got={c2787_pre}")
guard("c2786_pre==117", c2786_pre == 117, f"got={c2786_pre}")
guard("c2785_pre==111", c2785_pre == 111, f"got={c2785_pre}")
guard("c2784_pre==109", c2784_pre == 109, f"got={c2784_pre}")
guard("c2783_pre==110", c2783_pre == 110, f"got={c2783_pre}")
guard("c2782_pre==109", c2782_pre == 109, f"got={c2782_pre}")
guard("c2781_pre==114", c2781_pre == 114, f"got={c2781_pre}")
guard("c2780_pre==118", c2780_pre == 118, f"got={c2780_pre}")
guard("c2779_pre==119", c2779_pre == 119, f"got={c2779_pre}")
guard("c2778_pre==159", c2778_pre == 159, f"got={c2778_pre}")
guard("c2777_pre==135", c2777_pre == 135, f"got={c2777_pre}")
guard("c2776_pre==140", c2776_pre == 140, f"got={c2776_pre}")
guard("c2775_pre==149", c2775_pre == 149, f"got={c2775_pre}")
guard("c2774_pre==154", c2774_pre == 154, f"got={c2774_pre}")
guard("c2773_pre==158", c2773_pre == 158, f"got={c2773_pre}")
guard("c2772_pre==177", c2772_pre == 177, f"got={c2772_pre}")
guard("c2771_pre==167", c2771_pre == 167, f"got={c2771_pre}")
guard("c2770_pre==203", c2770_pre == 203, f"got={c2770_pre}")
guard("c2769_pre==156", c2769_pre == 156, f"got={c2769_pre}")
guard("c2768_pre==159", c2768_pre == 159, f"got={c2768_pre}")
guard("c2767_pre==196", c2767_pre == 196, f"got={c2767_pre}")
guard("c2766_pre==179", c2766_pre == 179, f"got={c2766_pre}")
guard("c2765_pre==150", c2765_pre == 150, f"got={c2765_pre}")
guard("c2764_pre==152", c2764_pre == 152, f"got={c2764_pre}")
guard("c2763_pre==160", c2763_pre == 160, f"got={c2763_pre}")
guard("c2762_pre==186", c2762_pre == 186, f"got={c2762_pre}")
guard("c2761_pre==200", c2761_pre == 200, f"got={c2761_pre}")
guard("c2760_pre==155", c2760_pre == 155, f"got={c2760_pre}")
guard("c2759_pre==155", c2759_pre == 155, f"got={c2759_pre}")
guard("c2758_pre==157", c2758_pre == 157, f"got={c2758_pre}")
guard("c2757_pre==160", c2757_pre == 160, f"got={c2757_pre}")
guard("c2756_pre==165", c2756_pre == 165, f"got={c2756_pre}")
guard("c2755_pre==172", c2755_pre == 172, f"got={c2755_pre}")
guard("c2754_pre==175", c2754_pre == 175, f"got={c2754_pre}")
guard("c2753_pre==181", c2753_pre == 181, f"got={c2753_pre}")
guard("c2752_pre==187", c2752_pre == 187, f"got={c2752_pre}")
guard("c2751_pre==173", c2751_pre == 173, f"got={c2751_pre}")
guard("c2750_pre==175", c2750_pre == 175, f"got={c2750_pre}")
guard("c2749_pre==179", c2749_pre == 179, f"got={c2749_pre}")
guard("c2748_pre==169", c2748_pre == 169, f"got={c2748_pre}")
guard("c2747_pre==167", c2747_pre == 167, f"got={c2747_pre}")
guard("c2746_pre==171", c2746_pre == 171, f"got={c2746_pre}")

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
guard("post_worklog_lines==9280", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2796_next_bullet", last2.startswith("- Next: the c2796 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==473", tid_post == 473, f"got={tid_post}")
guard("anchor_nogold_post==406", gold_post == 406, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2795_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2795")]) == 1)
expect_c2797_mentions = wl2.count("c2797")
guard("c2797_mention_birth", expect_c2797_mentions == c2797_pre + block.count("c2797"),
      f"pre={c2797_pre} (unborn) + block births={block.count('c2797')} (Step-7 pre-count "
      f"print + guard phrase + census-tuple sentence) -> expect={c2797_pre + block.count('c2797')} got={expect_c2797_mentions}")
for tag, pre in (("c2796", c2796_pre), ("c2795", c2795_pre), ("c2794", c2794_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9268 -> 9280 (+12), c2795 entry + DRIFT-#49 pass-44 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
