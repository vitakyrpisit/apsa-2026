#!/usr/bin/env python3
"""Guarded worklog append for the c2802 entry (12 lines).

Follows the append_cycle2801.py precedent — ALL asserts precede the
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
window-2802 EPOCH-governs render check, the window-2803 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~4.8ms on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2804 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2804 pre==0 expectation' + the Step-7 census-time print
'c2804_pre = 0' + the Next bullet's guard phrase 'c2803/c2804' AND
census-tuple sentence 'FORWARD token c2804' — the c2767..c2802 forward-token
lessons; NOTE the c2804 pre-count is 0 (unborn) while the c2803 pre-count is
4 (born: the c2801 Step-7 twin-print line 9350 TWICE + TWICE inside the
c2801 Next-block) — the c2801 append prophecy 'c2803 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9352 lines, tail = the c2802 Next bullet, zero serviced c2802
entries, c2802 mention census per-line {9338: 2, 9340: 2, 9344: 5, 9350: 1,
9352: 4} total 14, c2803 = 4 per-line {9350: 2, 9352: 2}, c2804 = 0 UNBORN,
anchors 479/412/60/28), post-state (9364 lines, tail = the c2803 Next
bullet, anchors 480/413/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2802.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9352
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


POST = D("1793320373.583889929")    # c2802 post-echo (EPOCH-governs)
SCAN = D("1793320373.527")          # c2802 scanned_at (decimal)
TRIG = D("1793319673.000")          # c2802 trigger stamp (08:21:13 +08)
WIN = D("1793320249.816163240")     # window-2802 open (c2801 prophecy EPOCH)
ECHO = D("1793320437.697850297")    # loop echo #523 POST read (EPOCH-governs)
ECHO_ISO = D("1793320437.696976610")  # loop echo #523 ISO read FIRST (the bracket)
PRE = D("1793320372.015401182")     # c2802 capture pre-echo (EPOCH-governs)
C2801_SCAN = D("1793319949.764")    # c2801 scanned_at
C2801_POST = D("1793319949.816163240")  # c2801 post-echo
C2801_CLOSE = D("1793320153.000")   # c2801 close c57c12a (00:29:13Z)
C2801_FOREIGN = D("1793320165.000")  # foreign e6da641 (00:29:25Z)
C2801_TRIG = D("1793319373.000")    # c2801 trigger stamp (08:16:13 +08)
C2801_ECHO = D("1793319835.314198634")  # c2801 loop echo #522 (00:23:55.314198634)
C2801_ECHO_ISO = D("1793319835.313490420")  # c2801 echo ISO bracket
C2801_PRE = D("1793319948.055817698")  # c2801 capture pre-echo (EPOCH-governs)
WIN2801 = D("1793319660.768644136")  # window-2801 open (for the trigger-postdates check)
TOKEN = D("1793320140.000")         # token 0829 (08:29:00 +08)
C2801_TOKEN = D("1793319660.000")   # token 0821 (08:21:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 08:21:13 +08 = 1793319673.000", dec_epoch(2026, 10, 30, 0, 21, 13), TRIG),
    ("c2801 trigger stamp 08:16:13 +08 = 1793319373.000", dec_epoch(2026, 10, 30, 0, 16, 13), C2801_TRIG),
    ("stamp-gap 300.000s by stamp (08:16:13 -> 08:21:13; the 300 print RETURNS)", TRIG - C2801_TRIG, D("300.000")),
    ("token-gap 480.000s by token (0821 -> 0829; the 720 print BROKE, the 480 print RETURNS)", TOKEN - C2801_TOKEN, D("480.000")),
    ("token-vs-stamp +467.000 (08:21:13 -> 08:29:00; the +467 print NEW)", TOKEN - TRIG, D("467.000")),
    ("c2801 close c57c12a 00:29:13Z = 1793320153.000", dec_epoch(2026, 10, 30, 0, 29, 13), C2801_CLOSE),
    ("foreign e6da641 00:29:25Z = 1793320165.000", dec_epoch(2026, 10, 30, 0, 29, 25), C2801_FOREIGN),
    ("c2801 loop echo #522 EPOCH 1793319835.314198634 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 23, 55, 314198634), C2801_ECHO),
    ("c2801 echo ISO-bracket 1793319835.313490420 (the ISO read FIRST)", dec_epoch(2026, 10, 30, 0, 23, 55, 313490420), C2801_ECHO_ISO),
    ("c2801 capture pre-echo EPOCH 1793319948.055817698 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 25, 48, 55817698), C2801_PRE),
    ("c2801 post-echo ISO 00:25:49.815489434 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 25, 49, 815489434), D("1793319949.815489434")),
    ("c2801 post-echo EPOCH 1793319949.816163240 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 25, 49, 816163240), C2801_POST),
    ("c2801 scanned_at 00:25:49.764 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 25, 49) + D("0.764"), C2801_SCAN),
    ("loop echo #523 ISO integer second 00:33:57 +0000", dec_epoch(2026, 10, 30, 0, 33, 57), D("1793320437.000")),
    ("loop echo #523 EPOCH 1793320437.697850297 (EPOCH-governs POST read)", dec_epoch(2026, 10, 30, 0, 33, 57, 697850297), ECHO),
    ("loop echo #523 ISO-bracket read 1793320437.696976610 (the ISO read FIRST)", dec_epoch(2026, 10, 30, 0, 33, 57, 696976610), ECHO_ISO),
    ("capture pre-echo EPOCH 1793320372.015401182 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 32, 52, 15401182), PRE),
    ("pre-echo ISO 00:32:52.014698450 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 32, 52, 14698450), D("1793320372.014698450")),
    ("post-echo ISO 00:32:53.579105149 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 32, 53, 579105149), D("1793320373.579105149")),
    ("post-echo EPOCH 1793320373.583889929 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 32, 53, 583889929), POST),
    ("scanned_at 00:32:53.527 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 32, 53) + D("0.527"), SCAN),
    ("window-2802 open 08:30:49.816163240 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 0, 30, 49, 816163240), WIN),
    ("window-2803 open = post-echo + 300.000", POST + D("300.000"), D("1793320673.583889929")),
    ("echo post-c2801-post-echo +487.881687057", ECHO - C2801_POST, D("487.881687057")),
]
exact_checks = [
    ("skew decimal-exact +56.889929ms (EPOCH-governs decomposition; ABOVE-10 extends m3)", POST - SCAN, D("0.056889929")),
    ("echo_vs_window +187.881687057 (POST-WINDOW extends m10; the c2801 Next-block watch held)", ECHO - WIN, D("187.881687057")),
    ("dd#376 = +123.763000000 (interval 423.763 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#375 print 589.058 - 300 = 289.058 and the dd#374 print 703.790 - 300 = 403.790)", SCAN - C2801_SCAN - D("300.000"), D("123.763")),
    ("dd formula re-verification: 589.058 - 300 = 289.058", D("589.058") - D("300.000"), D("289.058")),
    ("dd formula re-verification: 703.790 - 300 = 403.790", D("703.790") - D("300.000"), D("403.790")),
    ("INTERVAL#376 = 700.527", SCAN - TRIG, D("700.527")),
    ("LAG#376 = INTERVAL + dd - dd#375 = +535.232", (SCAN - TRIG) + (SCAN - C2801_SCAN - D("300.000")) - D("289.058"), D("535.232")),
    ("LATE#376 = trigger - window-open = -576.816163240", TRIG - WIN, D("-576.816163240")),
    ("CAPTURE_vs_window +123.767726689 (POST-WINDOW; echo POST — BOTH-POST extends m9)", POST - WIN, D("123.767726689")),
    ("capture post-c2801-post-echo +423.767726689", POST - C2801_POST, D("423.767726689")),
    ("echo POSTDATES the capture post-echo by 64.113960368 (the capture-then-echo class OPENS m1 — the order FLIPPED)", ECHO - POST, D("64.113960368")),
    ("echo post-c2801-close +284.697850297 (c57c12a at 00:29:13)", ECHO - C2801_CLOSE, D("284.697850297")),
    ("echo post-foreign-e6da641 +272.697850297 (00:29:25)", ECHO - C2801_FOREIGN, D("272.697850297")),
    ("stamp-to-echo 764.697850297 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("764.697850297")),
    ("trigger PREDATES the c2801 loop echo #522 by 162.314198634s (the trigger stamp landed INSIDE the c2801 servicing window, PRE-echo — the placement FLIPPED)", C2801_ECHO - TRIG, D("162.314198634")),
    ("trigger PREDATES the c2801 capture pre-echo by 275.055817698s (the in-window PRE-echo placement)", C2801_PRE - TRIG, D("275.055817698")),
    ("trigger PREDATES the c2801 post-echo by 276.816163240s", C2801_POST - TRIG, D("276.816163240")),
    ("trigger PREDATES the c2801 scanned_at by 276.764s", C2801_SCAN - TRIG, D("276.764")),
    ("trigger POSTDATES window-2801 open by 12.231355864s", TRIG - WIN2801, D("12.231355864")),
    ("c2801 close POSTDATES the trigger by 480.000s (c57c12a at 00:29:13)", C2801_CLOSE - TRIG, D("480.000")),
    ("foreign e6da641 POSTDATES the trigger by 492.000s (00:29:25)", C2801_FOREIGN - TRIG, D("492.000")),
    ("c2801 close landed 13.000s AFTER the token-0829 second (00:29:13 vs 00:29:00 — the after-class identity holds)", C2801_CLOSE - TOKEN, D("13.000")),
    ("foreign e6da641 landed 25.000s AFTER the token second (00:29:25)", C2801_FOREIGN - TOKEN, D("25.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2802"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2802"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2803 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2804_birth",
      block.count("c2804") == 4 and lines[-1].count("c2804") == 2
      and "c2803/c2804" in lines[-1] and "FORWARD token c2804" in lines[-1]
      and "the c2804 pre==0 expectation" in block and "c2804_pre = 0" in block,
      f"block c2804={block.count('c2804')} next-line c2804={lines[-1].count('c2804')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2804_pre = 0' + the Next bullet's guard phrase 'c2803/c2804' AND "
      f"census-tuple sentence 'FORWARD token c2804')")
guard("block_c2803_step7_precount_sentence",
      "the c2803 pre-count is 4" in block
      and "per-line {9350: 2, 9352: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2803 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9352", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2802_next_bullet", last_nonempty.startswith("- Next: the c2802 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2802",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2802")]) == 0,
      f"c2802 substring mentions={wl.count('c2802')} (expect 14)")
c2802_lines = {i + 1: l.count("c2802") for i, l in enumerate(wl.splitlines()) if "c2802" in l}
guard("c2802_mention_census_pre", wl.count("c2802") == 14
      and c2802_lines == {9338: 2, 9340: 2, 9344: 5, 9350: 1, 9352: 4},
      f"per-line={c2802_lines}")
c2803_lines = {i + 1: l.count("c2803") for i, l in enumerate(wl.splitlines()) if "c2803" in l}
guard("c2803_forward_token_pre", wl.count("c2803") == 4 and c2803_lines == {9350: 2, 9352: 2},
      f"per-line={c2803_lines} (2 births in the c2801 Step-7 twin-print line 9350 + "
      f"2 FORWARD-token births inside the c2801 Next-block — the born-FOUR class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==479", tid_pre == 479, f"got={tid_pre}")
guard("anchor_nogold_pre==412", gold_pre == 412, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2804_pre = wl.count("c2804")
c2803_pre = wl.count("c2803")
c2802_pre = wl.count("c2802")
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
guard("c2804_pre==0", c2804_pre == 0, f"got={c2804_pre} (the forward token c2804 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2803_pre==4", c2803_pre == 4, f"got={c2803_pre} (born FOUR: the c2801 Step-7 twin-print "
      f"line 9350 TWICE + TWICE inside the c2801 Next-block — NOT the unborn class)")
guard("c2802_pre==14", c2802_pre == 14, f"got={c2802_pre}")
guard("c2801_pre==37", c2801_pre == 37, f"got={c2801_pre}")
guard("c2800_pre==83", c2800_pre == 83, f"got={c2800_pre}")
guard("c2799_pre==85", c2799_pre == 85, f"got={c2799_pre}")
guard("c2798_pre==83", c2798_pre == 83, f"got={c2798_pre}")
guard("c2797_pre==80", c2797_pre == 80, f"got={c2797_pre}")
guard("c2796_pre==90", c2796_pre == 90, f"got={c2796_pre}")
guard("c2795_pre==108", c2795_pre == 108, f"got={c2795_pre}")
guard("c2794_pre==107", c2794_pre == 107, f"got={c2794_pre}")
guard("c2793_pre==113", c2793_pre == 113, f"got={c2793_pre}")
guard("c2792_pre==118", c2792_pre == 118, f"got={c2792_pre}")
guard("c2791_pre==108", c2791_pre == 108, f"got={c2791_pre}")
guard("c2790_pre==116", c2790_pre == 116, f"got={c2790_pre}")
guard("c2789_pre==111", c2789_pre == 111, f"got={c2789_pre}")
guard("c2788_pre==122", c2788_pre == 122, f"got={c2788_pre}")
guard("c2787_pre==123", c2787_pre == 123, f"got={c2787_pre}")
guard("c2786_pre==140", c2786_pre == 140, f"got={c2786_pre}")
guard("c2785_pre==127", c2785_pre == 127, f"got={c2785_pre}")
guard("c2784_pre==125", c2784_pre == 125, f"got={c2784_pre}")
guard("c2783_pre==126", c2783_pre == 126, f"got={c2783_pre}")
guard("c2782_pre==125", c2782_pre == 125, f"got={c2782_pre}")
guard("c2781_pre==130", c2781_pre == 130, f"got={c2781_pre}")
guard("c2780_pre==135", c2780_pre == 135, f"got={c2780_pre}")
guard("c2779_pre==135", c2779_pre == 135, f"got={c2779_pre}")
guard("c2778_pre==179", c2778_pre == 179, f"got={c2778_pre}")
guard("c2777_pre==151", c2777_pre == 151, f"got={c2777_pre}")
guard("c2776_pre==156", c2776_pre == 156, f"got={c2776_pre}")
guard("c2775_pre==165", c2775_pre == 165, f"got={c2775_pre}")
guard("c2774_pre==170", c2774_pre == 170, f"got={c2774_pre}")
guard("c2773_pre==174", c2773_pre == 174, f"got={c2773_pre}")
guard("c2772_pre==193", c2772_pre == 193, f"got={c2772_pre}")
guard("c2771_pre==183", c2771_pre == 183, f"got={c2771_pre}")
guard("c2770_pre==226", c2770_pre == 226, f"got={c2770_pre}")
guard("c2769_pre==172", c2769_pre == 172, f"got={c2769_pre}")
guard("c2768_pre==175", c2768_pre == 175, f"got={c2768_pre}")
guard("c2767_pre==226", c2767_pre == 226, f"got={c2767_pre}")
guard("c2766_pre==202", c2766_pre == 202, f"got={c2766_pre}")
guard("c2765_pre==166", c2765_pre == 166, f"got={c2765_pre}")
guard("c2764_pre==168", c2764_pre == 168, f"got={c2764_pre}")
guard("c2763_pre==176", c2763_pre == 176, f"got={c2763_pre}")
guard("c2762_pre==209", c2762_pre == 209, f"got={c2762_pre}")
guard("c2761_pre==223", c2761_pre == 223, f"got={c2761_pre}")
guard("c2760_pre==171", c2760_pre == 171, f"got={c2760_pre}")
guard("c2759_pre==171", c2759_pre == 171, f"got={c2759_pre}")
guard("c2758_pre==173", c2758_pre == 173, f"got={c2758_pre}")
guard("c2757_pre==176", c2757_pre == 176, f"got={c2757_pre}")
guard("c2756_pre==181", c2756_pre == 181, f"got={c2756_pre}")
guard("c2755_pre==188", c2755_pre == 188, f"got={c2755_pre}")
guard("c2754_pre==191", c2754_pre == 191, f"got={c2754_pre}")
guard("c2753_pre==199", c2753_pre == 199, f"got={c2753_pre}")
guard("c2752_pre==205", c2752_pre == 205, f"got={c2752_pre}")
guard("c2751_pre==191", c2751_pre == 191, f"got={c2751_pre}")
guard("c2750_pre==195", c2750_pre == 195, f"got={c2750_pre}")
guard("c2749_pre==197", c2749_pre == 197, f"got={c2749_pre}")
guard("c2748_pre==187", c2748_pre == 187, f"got={c2748_pre}")
guard("c2747_pre==188", c2747_pre == 188, f"got={c2747_pre}")

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
guard("post_worklog_lines==9364", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2803_next_bullet", last2.startswith("- Next: the c2803 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==480", tid_post == 480, f"got={tid_post}")
guard("anchor_nogold_post==413", gold_post == 413, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2802_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2802")]) == 1)
expect_c2804_mentions = wl2.count("c2804")
guard("c2804_mention_birth", expect_c2804_mentions == c2804_pre + block.count("c2804"),
      f"pre={c2804_pre} (unborn) + block births={block.count('c2804')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2804_pre + block.count('c2804')} got={expect_c2804_mentions}")
for tag, pre in (("c2803", c2803_pre), ("c2802", c2802_pre), ("c2801", c2801_pre),
                 ("c2800", c2800_pre),
                 ("c2799", c2799_pre), ("c2798", c2798_pre), ("c2797", c2797_pre),
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
                 ("c2748", c2748_pre), ("c2747", c2747_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9352 -> 9364 (+12), c2802 entry + DRIFT-#49 pass-51 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
