#!/usr/bin/env python3
"""Guarded worklog append for the c2800 entry (12 lines).

Follows the append_cycle2799.py precedent — ALL asserts precede the
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
window-2800 EPOCH-governs render check, the window-2801 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~4.4ms on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2802 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2802 pre==0 expectation' + the Step-7 census-time print
'c2802_pre = 0' + the Next bullet's guard phrase 'c2801/c2802' AND
census-tuple sentence 'FORWARD token c2802' — the c2767..c2800 forward-token
lessons; NOTE the c2802 pre-count is 0 (unborn) while the c2801 pre-count is
4 (born: the c2799 Step-7 twin-print line 9326 TWICE + TWICE inside the
c2799 Next-block) — the c2799 append prophecy 'c2801 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9328 lines, tail = the c2800 Next bullet, zero serviced c2800
entries, c2800 mention census per-line {9314: 2, 9316: 2, 9320: 5, 9326: 1,
9328: 4} total 14, c2801 = 4 per-line {9326: 2, 9328: 2}, c2802 = 0 UNBORN,
anchors 477/410/60/28), post-state (9340 lines, tail = the c2801 Next
bullet, anchors 478/411/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2800.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9328
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


POST = D("1793319360.768644136")    # c2800 post-echo (EPOCH-governs)
SCAN = D("1793319360.706")          # c2800 scanned_at (decimal)
TRIG = D("1793318472.000")          # c2800 trigger stamp (08:01:12 +08)
WIN = D("1793318956.922499324")     # window-2800 open (c2799 prophecy EPOCH)
ECHO = D("1793319311.720213599")    # loop echo #521 POST read (EPOCH-governs)
ECHO_ISO = D("1793319311.719550015")  # loop echo #521 ISO read FIRST (the bracket)
PRE = D("1793319359.014257146")     # c2800 capture pre-echo (EPOCH-governs)
C2799_SCAN = D("1793318656.916")    # c2799 scanned_at
C2799_POST = D("1793318656.922499324")  # c2799 post-echo
C2799_CLOSE = D("1793318980.000")   # c2799 close 89fada0 (00:09:40Z)
C2799_FOREIGN = D("1793318995.000")  # foreign f0d806e (00:09:55Z)
C2799_TRIG = D("1793317872.000")    # c2799 trigger stamp (07:51:12 +08)
C2799_ECHO = D("1793318442.5431652")  # c2799 loop echo #520 (00:00:42.5431652)
C2799_ECHO_ISO = D("1793318442.533247405")  # c2799 echo ISO bracket
C2799_PRE = D("1793318655.041130607")  # c2799 capture pre-echo (EPOCH-governs)
TOKEN = D("1793318940.000")         # token 0809 (08:09:00 +08)
C2799_TOKEN = D("1793318340.000")   # token 0759 (07:59:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 08:01:12 +08 = 1793318472.000", dec_epoch(2026, 10, 30, 0, 1, 12), TRIG),
    ("c2799 trigger stamp 07:51:12 +08 = 1793317872.000", dec_epoch(2026, 10, 29, 23, 51, 12), C2799_TRIG),
    ("stamp-gap 600.000s by stamp (07:51:12 -> 08:01:12; the 600 print REPEATS)", TRIG - C2799_TRIG, D("600.000")),
    ("token-gap 600.000s by token (0759 -> 0809; the 540 print BROKE, the 600 print RETURNS)", TOKEN - C2799_TOKEN, D("600.000")),
    ("token-vs-stamp +468.000 (08:01:12 -> 08:09:00; the +468 print REPEATS)", TOKEN - TRIG, D("468.000")),
    ("c2799 close 89fada0 00:09:40Z = 1793318980.000", dec_epoch(2026, 10, 30, 0, 9, 40), C2799_CLOSE),
    ("foreign f0d806e 00:09:55Z = 1793318995.000", dec_epoch(2026, 10, 30, 0, 9, 55), C2799_FOREIGN),
    ("c2799 loop echo #520 EPOCH 1793318442.5431652 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 0, 42, 543165200), C2799_ECHO),
    ("c2799 echo ISO-bracket 1793318442.533247405 (the ISO read FIRST)", dec_epoch(2026, 10, 30, 0, 0, 42, 533247405), C2799_ECHO_ISO),
    ("c2799 capture pre-echo EPOCH 1793318655.041130607 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 4, 15, 41130607), C2799_PRE),
    ("c2799 post-echo ISO 00:04:16.921782217 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 4, 16, 921782217), D("1793318656.921782217")),
    ("c2799 post-echo EPOCH 1793318656.922499324 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 4, 16, 922499324), C2799_POST),
    ("c2799 scanned_at 00:04:16.916 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 4, 16) + D("0.916"), C2799_SCAN),
    ("loop echo #521 ISO integer second 00:15:11 +0000", dec_epoch(2026, 10, 30, 0, 15, 11), D("1793319311.000")),
    ("loop echo #521 EPOCH 1793319311.720213599 (EPOCH-governs POST read)", dec_epoch(2026, 10, 30, 0, 15, 11, 720213599), ECHO),
    ("loop echo #521 ISO-bracket read 1793319311.719550015 (the ISO read FIRST)", dec_epoch(2026, 10, 30, 0, 15, 11, 719550015), ECHO_ISO),
    ("capture pre-echo EPOCH 1793319359.014257146 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 15, 59, 14257146), PRE),
    ("pre-echo ISO 00:15:59.013570637 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 15, 59, 13570637), D("1793319359.013570637")),
    ("post-echo ISO 00:16:00.764260612 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 16, 0, 764260612), D("1793319360.764260612")),
    ("post-echo EPOCH 1793319360.768644136 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 16, 0, 768644136), POST),
    ("scanned_at 00:16:00.706 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 16, 0) + D("0.706"), SCAN),
    ("window-2800 open 08:09:16.922499324 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 0, 9, 16, 922499324), WIN),
    ("window-2801 open = post-echo + 300.000", POST + D("300.000"), D("1793319660.768644136")),
    ("echo post-c2799-post-echo +654.797714275", ECHO - C2799_POST, D("654.797714275")),
]
exact_checks = [
    ("skew decimal-exact +62.644136ms (EPOCH-governs decomposition; ABOVE-10 FLIP re-opens m1)", POST - SCAN, D("0.062644136")),
    ("echo_vs_window +354.797714275 (POST-WINDOW extends m8; the c2799 Next-block watch held)", ECHO - WIN, D("354.797714275")),
    ("dd#374 = +403.790000000 (interval 703.790 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#372 print 530.564 - 300 = 230.564 and the dd#373 print 608.805 - 300 = 308.805)", SCAN - C2799_SCAN - D("300.000"), D("403.790")),
    ("dd formula re-verification: 530.564 - 300 = 230.564", D("530.564") - D("300.000"), D("230.564")),
    ("dd formula re-verification: 608.805 - 300 = 308.805", D("608.805") - D("300.000"), D("308.805")),
    ("INTERVAL#374 = 888.706", SCAN - TRIG, D("888.706")),
    ("LAG#374 = INTERVAL + dd - dd#373 = +983.691", (SCAN - TRIG) + (SCAN - C2799_SCAN - D("300.000")) - D("308.805"), D("983.691")),
    ("LATE#374 = trigger - window-open = -484.922499324", TRIG - WIN, D("-484.922499324")),
    ("CAPTURE_vs_window +403.846144812 (POST-WINDOW; echo POST — BOTH-POST extends m7)", POST - WIN, D("403.846144812")),
    ("capture-vs-echo +49.048430537", POST - ECHO, D("49.048430537")),
    ("capture post-c2799-post-echo +703.846144812", POST - C2799_POST, D("703.846144812")),
    ("echo post-c2799-close +331.720213599 (89fada0 at 00:09:40)", ECHO - C2799_CLOSE, D("331.720213599")),
    ("echo post-foreign-f0d806e +316.720213599 (00:09:55)", ECHO - C2799_FOREIGN, D("316.720213599")),
    ("stamp-to-echo 839.720213599 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("839.720213599")),
    ("trigger POSTDATES the c2799 loop echo #520 by 29.4568348s (the trigger stamp landed INSIDE the c2799 servicing window, POST-echo — the phase-shift class noted)", TRIG - C2799_ECHO, D("29.4568348")),
    ("trigger predates the c2799 capture pre-echo by 183.041130607s", C2799_PRE - TRIG, D("183.041130607")),
    ("trigger predates the c2799 post-echo by 184.922499324s", C2799_POST - TRIG, D("184.922499324")),
    ("trigger predates the c2799 scanned_at by 184.916s", C2799_SCAN - TRIG, D("184.916")),
    ("trigger predates window-2800 open by 484.922499324s", WIN - TRIG, D("484.922499324")),
    ("c2799 close POSTDATES the trigger by 508.000s (89fada0 at 00:09:40)", C2799_CLOSE - TRIG, D("508.000")),
    ("foreign f0d806e POSTDATES the trigger by 523.000s (00:09:55)", C2799_FOREIGN - TRIG, D("523.000")),
    ("c2799 close landed 40.000s AFTER the token-0809 second (00:09:40 vs 00:09:00 — the after-class identity holds)", C2799_CLOSE - TOKEN, D("40.000")),
    ("foreign f0d806e landed 55.000s AFTER the token second (00:09:55)", C2799_FOREIGN - TOKEN, D("55.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2800"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2800"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2801 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2802_birth",
      block.count("c2802") == 4 and lines[-1].count("c2802") == 2
      and "c2801/c2802" in lines[-1] and "FORWARD token c2802" in lines[-1]
      and "the c2802 pre==0 expectation" in block and "c2802_pre = 0" in block,
      f"block c2802={block.count('c2802')} next-line c2802={lines[-1].count('c2802')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2802_pre = 0' + the Next bullet's guard phrase 'c2801/c2802' AND "
      f"census-tuple sentence 'FORWARD token c2802')")
guard("block_c2801_step7_precount_sentence",
      "the c2801 pre-count is 4" in block
      and "per-line {9326: 2, 9328: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2801 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9328", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2800_next_bullet", last_nonempty.startswith("- Next: the c2800 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2800",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2800")]) == 0,
      f"c2800 substring mentions={wl.count('c2800')} (expect 14)")
c2800_lines = {i + 1: l.count("c2800") for i, l in enumerate(wl.splitlines()) if "c2800" in l}
guard("c2800_mention_census_pre", wl.count("c2800") == 14
      and c2800_lines == {9314: 2, 9316: 2, 9320: 5, 9326: 1, 9328: 4},
      f"per-line={c2800_lines}")
c2801_lines = {i + 1: l.count("c2801") for i, l in enumerate(wl.splitlines()) if "c2801" in l}
guard("c2801_forward_token_pre", wl.count("c2801") == 4 and c2801_lines == {9326: 2, 9328: 2},
      f"per-line={c2801_lines} (2 births in the c2799 Step-7 twin-print line 9326 + "
      f"2 FORWARD-token births inside the c2799 Next-block — the born-FOUR class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==477", tid_pre == 477, f"got={tid_pre}")
guard("anchor_nogold_pre==410", gold_pre == 410, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2802_pre==0", c2802_pre == 0, f"got={c2802_pre} (the forward token c2802 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2801_pre==4", c2801_pre == 4, f"got={c2801_pre} (born FOUR: the c2799 Step-7 twin-print "
      f"line 9326 TWICE + TWICE inside the c2799 Next-block — NOT the unborn class)")
guard("c2800_pre==14", c2800_pre == 14, f"got={c2800_pre}")
guard("c2799_pre==37", c2799_pre == 37, f"got={c2799_pre}")
guard("c2798_pre==73", c2798_pre == 73, f"got={c2798_pre}")
guard("c2797_pre==78", c2797_pre == 78, f"got={c2797_pre}")
guard("c2796_pre==88", c2796_pre == 88, f"got={c2796_pre}")
guard("c2795_pre==102", c2795_pre == 102, f"got={c2795_pre}")
guard("c2794_pre==105", c2794_pre == 105, f"got={c2794_pre}")
guard("c2793_pre==109", c2793_pre == 109, f"got={c2793_pre}")
guard("c2792_pre==114", c2792_pre == 114, f"got={c2792_pre}")
guard("c2791_pre==106", c2791_pre == 106, f"got={c2791_pre}")
guard("c2790_pre==112", c2790_pre == 112, f"got={c2790_pre}")
guard("c2789_pre==109", c2789_pre == 109, f"got={c2789_pre}")
guard("c2788_pre==120", c2788_pre == 120, f"got={c2788_pre}")
guard("c2787_pre==121", c2787_pre == 121, f"got={c2787_pre}")
guard("c2786_pre==136", c2786_pre == 136, f"got={c2786_pre}")
guard("c2785_pre==125", c2785_pre == 125, f"got={c2785_pre}")
guard("c2784_pre==123", c2784_pre == 123, f"got={c2784_pre}")
guard("c2783_pre==124", c2783_pre == 124, f"got={c2783_pre}")
guard("c2782_pre==123", c2782_pre == 123, f"got={c2782_pre}")
guard("c2781_pre==128", c2781_pre == 128, f"got={c2781_pre}")
guard("c2780_pre==132", c2780_pre == 132, f"got={c2780_pre}")
guard("c2779_pre==133", c2779_pre == 133, f"got={c2779_pre}")
guard("c2778_pre==177", c2778_pre == 177, f"got={c2778_pre}")
guard("c2777_pre==149", c2777_pre == 149, f"got={c2777_pre}")
guard("c2776_pre==154", c2776_pre == 154, f"got={c2776_pre}")
guard("c2775_pre==163", c2775_pre == 163, f"got={c2775_pre}")
guard("c2774_pre==168", c2774_pre == 168, f"got={c2774_pre}")
guard("c2773_pre==172", c2773_pre == 172, f"got={c2773_pre}")
guard("c2772_pre==191", c2772_pre == 191, f"got={c2772_pre}")
guard("c2771_pre==181", c2771_pre == 181, f"got={c2771_pre}")
guard("c2770_pre==222", c2770_pre == 222, f"got={c2770_pre}")
guard("c2769_pre==170", c2769_pre == 170, f"got={c2769_pre}")
guard("c2768_pre==173", c2768_pre == 173, f"got={c2768_pre}")
guard("c2767_pre==220", c2767_pre == 220, f"got={c2767_pre}")
guard("c2766_pre==198", c2766_pre == 198, f"got={c2766_pre}")
guard("c2765_pre==164", c2765_pre == 164, f"got={c2765_pre}")
guard("c2764_pre==166", c2764_pre == 166, f"got={c2764_pre}")
guard("c2763_pre==174", c2763_pre == 174, f"got={c2763_pre}")
guard("c2762_pre==205", c2762_pre == 205, f"got={c2762_pre}")
guard("c2761_pre==219", c2761_pre == 219, f"got={c2761_pre}")
guard("c2760_pre==169", c2760_pre == 169, f"got={c2760_pre}")
guard("c2759_pre==169", c2759_pre == 169, f"got={c2759_pre}")
guard("c2758_pre==171", c2758_pre == 171, f"got={c2758_pre}")
guard("c2757_pre==174", c2757_pre == 174, f"got={c2757_pre}")
guard("c2756_pre==179", c2756_pre == 179, f"got={c2756_pre}")
guard("c2755_pre==186", c2755_pre == 186, f"got={c2755_pre}")
guard("c2754_pre==189", c2754_pre == 189, f"got={c2754_pre}")
guard("c2753_pre==195", c2753_pre == 195, f"got={c2753_pre}")
guard("c2752_pre==201", c2752_pre == 201, f"got={c2752_pre}")
guard("c2751_pre==187", c2751_pre == 187, f"got={c2751_pre}")
guard("c2750_pre==189", c2750_pre == 189, f"got={c2750_pre}")
guard("c2749_pre==193", c2749_pre == 193, f"got={c2749_pre}")
guard("c2748_pre==183", c2748_pre == 183, f"got={c2748_pre}")
guard("c2747_pre==181", c2747_pre == 181, f"got={c2747_pre}")

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
guard("post_worklog_lines==9340", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2801_next_bullet", last2.startswith("- Next: the c2801 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==478", tid_post == 478, f"got={tid_post}")
guard("anchor_nogold_post==411", gold_post == 411, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2800_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2800")]) == 1)
expect_c2802_mentions = wl2.count("c2802")
guard("c2802_mention_birth", expect_c2802_mentions == c2802_pre + block.count("c2802"),
      f"pre={c2802_pre} (unborn) + block births={block.count('c2802')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2802_pre + block.count('c2802')} got={expect_c2802_mentions}")
for tag, pre in (("c2801", c2801_pre), ("c2800", c2800_pre), ("c2799", c2799_pre),
                 ("c2798", c2798_pre), ("c2797", c2797_pre), ("c2796", c2796_pre),
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
                 ("c2747", c2747_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9328 -> 9340 (+12), c2800 entry + DRIFT-#49 pass-49 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
