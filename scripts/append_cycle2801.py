#!/usr/bin/env python3
"""Guarded worklog append for the c2801 entry (12 lines).

Follows the append_cycle2800.py precedent — ALL asserts precede the
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
window-2801 EPOCH-governs render check, the window-2802 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~4.7ms on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2803 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2803 pre==0 expectation' + the Step-7 census-time print
'c2803_pre = 0' + the Next bullet's guard phrase 'c2802/c2803' AND
census-tuple sentence 'FORWARD token c2803' — the c2767..c2801 forward-token
lessons; NOTE the c2803 pre-count is 0 (unborn) while the c2802 pre-count is
4 (born: the c2800 Step-7 twin-print line 9338 TWICE + TWICE inside the
c2800 Next-block) — the c2800 append prophecy 'c2802 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9340 lines, tail = the c2801 Next bullet, zero serviced c2801
entries, c2801 mention census per-line {9326: 2, 9328: 2, 9332: 5, 9338: 1,
9340: 4} total 14, c2802 = 4 per-line {9338: 2, 9340: 2}, c2803 = 0 UNBORN,
anchors 478/411/60/28), post-state (9352 lines, tail = the c2802 Next
bullet, anchors 479/412/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2801.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9340
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


POST = D("1793319949.816163240")    # c2801 post-echo (EPOCH-governs)
SCAN = D("1793319949.764")          # c2801 scanned_at (decimal)
TRIG = D("1793319373.000")          # c2801 trigger stamp (08:16:13 +08)
WIN = D("1793319660.768644136")     # window-2801 open (c2800 prophecy EPOCH)
ECHO = D("1793319835.314198634")    # loop echo #522 POST read (EPOCH-governs)
ECHO_ISO = D("1793319835.313490420")  # loop echo #522 ISO read FIRST (the bracket)
PRE = D("1793319948.055817698")     # c2801 capture pre-echo (EPOCH-governs)
C2800_SCAN = D("1793319360.706")    # c2800 scanned_at
C2800_POST = D("1793319360.768644136")  # c2800 post-echo
C2800_CLOSE = D("1793319663.000")   # c2800 close e829f19 (00:21:03Z)
C2800_FOREIGN = D("1793319678.000")  # foreign 87e21ad (00:21:18Z)
C2800_TRIG = D("1793318472.000")    # c2800 trigger stamp (08:01:12 +08)
C2800_ECHO = D("1793319311.720213599")  # c2800 loop echo #521 (00:15:11.720213599)
C2800_ECHO_ISO = D("1793319311.719550015")  # c2800 echo ISO bracket
C2800_PRE = D("1793319359.014257146")  # c2800 capture pre-echo (EPOCH-governs)
TOKEN = D("1793319660.000")         # token 0821 (08:21:00 +08)
C2800_TOKEN = D("1793318940.000")   # token 0809 (08:09:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 08:16:13 +08 = 1793319373.000", dec_epoch(2026, 10, 30, 0, 16, 13), TRIG),
    ("c2800 trigger stamp 08:01:12 +08 = 1793318472.000", dec_epoch(2026, 10, 30, 0, 1, 12), C2800_TRIG),
    ("stamp-gap 901.000s by stamp (08:01:12 -> 08:16:13; the 901 print RETURNS)", TRIG - C2800_TRIG, D("901.000")),
    ("token-gap 720.000s by token (0809 -> 0821; the 600 print BROKE, the 720 print RETURNS)", TOKEN - C2800_TOKEN, D("720.000")),
    ("token-vs-stamp +287.000 (08:16:13 -> 08:21:00; the +287 print NEW)", TOKEN - TRIG, D("287.000")),
    ("c2800 close e829f19 00:21:03Z = 1793319663.000", dec_epoch(2026, 10, 30, 0, 21, 3), C2800_CLOSE),
    ("foreign 87e21ad 00:21:18Z = 1793319678.000", dec_epoch(2026, 10, 30, 0, 21, 18), C2800_FOREIGN),
    ("c2800 loop echo #521 EPOCH 1793319311.720213599 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 15, 11, 720213599), C2800_ECHO),
    ("c2800 echo ISO-bracket 1793319311.719550015 (the ISO read FIRST)", dec_epoch(2026, 10, 30, 0, 15, 11, 719550015), C2800_ECHO_ISO),
    ("c2800 capture pre-echo EPOCH 1793319359.014257146 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 15, 59, 14257146), C2800_PRE),
    ("c2800 post-echo ISO 00:16:00.764260612 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 16, 0, 764260612), D("1793319360.764260612")),
    ("c2800 post-echo EPOCH 1793319360.768644136 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 16, 0, 768644136), C2800_POST),
    ("c2800 scanned_at 00:16:00.706 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 16, 0) + D("0.706"), C2800_SCAN),
    ("loop echo #522 ISO integer second 00:23:55 +0000", dec_epoch(2026, 10, 30, 0, 23, 55), D("1793319835.000")),
    ("loop echo #522 EPOCH 1793319835.314198634 (EPOCH-governs POST read)", dec_epoch(2026, 10, 30, 0, 23, 55, 314198634), ECHO),
    ("loop echo #522 ISO-bracket read 1793319835.313490420 (the ISO read FIRST)", dec_epoch(2026, 10, 30, 0, 23, 55, 313490420), ECHO_ISO),
    ("capture pre-echo EPOCH 1793319948.055817698 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 25, 48, 55817698), PRE),
    ("pre-echo ISO 00:25:48.055200745 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 25, 48, 55200745), D("1793319948.055200745")),
    ("post-echo ISO 00:25:49.815489434 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 25, 49, 815489434), D("1793319949.815489434")),
    ("post-echo EPOCH 1793319949.816163240 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 25, 49, 816163240), POST),
    ("scanned_at 00:25:49.764 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 25, 49) + D("0.764"), SCAN),
    ("window-2801 open 08:21:00.768644136 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 0, 21, 0, 768644136), WIN),
    ("window-2802 open = post-echo + 300.000", POST + D("300.000"), D("1793320249.816163240")),
    ("echo post-c2800-post-echo +474.545554498", ECHO - C2800_POST, D("474.545554498")),
]
exact_checks = [
    ("skew decimal-exact +52.163240ms (EPOCH-governs decomposition; ABOVE-10 extends m2)", POST - SCAN, D("0.052163240")),
    ("echo_vs_window +174.545554498 (POST-WINDOW extends m9; the c2800 Next-block watch held)", ECHO - WIN, D("174.545554498")),
    ("dd#375 = +289.058000000 (interval 589.058 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#373 print 608.805 - 300 = 308.805 and the dd#374 print 703.790 - 300 = 403.790)", SCAN - C2800_SCAN - D("300.000"), D("289.058")),
    ("dd formula re-verification: 608.805 - 300 = 308.805", D("608.805") - D("300.000"), D("308.805")),
    ("dd formula re-verification: 703.790 - 300 = 403.790", D("703.790") - D("300.000"), D("403.790")),
    ("INTERVAL#375 = 576.764", SCAN - TRIG, D("576.764")),
    ("LAG#375 = INTERVAL + dd - dd#374 = +462.032", (SCAN - TRIG) + (SCAN - C2800_SCAN - D("300.000")) - D("403.790"), D("462.032")),
    ("LATE#375 = trigger - window-open = -287.768644136", TRIG - WIN, D("-287.768644136")),
    ("CAPTURE_vs_window +289.047519104 (POST-WINDOW; echo POST — BOTH-POST extends m8)", POST - WIN, D("289.047519104")),
    ("capture-vs-echo +114.501964606", POST - ECHO, D("114.501964606")),
    ("capture post-c2800-post-echo +589.047519104", POST - C2800_POST, D("589.047519104")),
    ("echo post-c2800-close +172.314198634 (e829f19 at 00:21:03)", ECHO - C2800_CLOSE, D("172.314198634")),
    ("echo post-foreign-87e21ad +157.314198634 (00:21:18)", ECHO - C2800_FOREIGN, D("157.314198634")),
    ("stamp-to-echo 462.314198634 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("462.314198634")),
    ("trigger POSTDATES the c2800 loop echo #521 by 61.279786401s (the trigger stamp landed INSIDE the c2800 servicing window, POST-echo — the placement class REPEATS)", TRIG - C2800_ECHO, D("61.279786401")),
    ("trigger POSTDATES the c2800 capture pre-echo by 13.985742854s (the in-window POST-echo placement)", TRIG - C2800_PRE, D("13.985742854")),
    ("trigger POSTDATES the c2800 post-echo by 12.231355864s", TRIG - C2800_POST, D("12.231355864")),
    ("trigger POSTDATES the c2800 scanned_at by 12.294s", TRIG - C2800_SCAN, D("12.294")),
    ("trigger predates window-2801 open by 287.768644136s", WIN - TRIG, D("287.768644136")),
    ("c2800 close POSTDATES the trigger by 290.000s (e829f19 at 00:21:03)", C2800_CLOSE - TRIG, D("290.000")),
    ("foreign 87e21ad POSTDATES the trigger by 305.000s (00:21:18)", C2800_FOREIGN - TRIG, D("305.000")),
    ("c2800 close landed 3.000s AFTER the token-0821 second (00:21:03 vs 00:21:00 — the after-class identity holds)", C2800_CLOSE - TOKEN, D("3.000")),
    ("foreign 87e21ad landed 18.000s AFTER the token second (00:21:18)", C2800_FOREIGN - TOKEN, D("18.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2801"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2801"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2802 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2803_birth",
      block.count("c2803") == 4 and lines[-1].count("c2803") == 2
      and "c2802/c2803" in lines[-1] and "FORWARD token c2803" in lines[-1]
      and "the c2803 pre==0 expectation" in block and "c2803_pre = 0" in block,
      f"block c2803={block.count('c2803')} next-line c2803={lines[-1].count('c2803')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2803_pre = 0' + the Next bullet's guard phrase 'c2802/c2803' AND "
      f"census-tuple sentence 'FORWARD token c2803')")
guard("block_c2802_step7_precount_sentence",
      "the c2802 pre-count is 4" in block
      and "per-line {9338: 2, 9340: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2802 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9340", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2801_next_bullet", last_nonempty.startswith("- Next: the c2801 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2801",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2801")]) == 0,
      f"c2801 substring mentions={wl.count('c2801')} (expect 14)")
c2801_lines = {i + 1: l.count("c2801") for i, l in enumerate(wl.splitlines()) if "c2801" in l}
guard("c2801_mention_census_pre", wl.count("c2801") == 14
      and c2801_lines == {9326: 2, 9328: 2, 9332: 5, 9338: 1, 9340: 4},
      f"per-line={c2801_lines}")
c2802_lines = {i + 1: l.count("c2802") for i, l in enumerate(wl.splitlines()) if "c2802" in l}
guard("c2802_forward_token_pre", wl.count("c2802") == 4 and c2802_lines == {9338: 2, 9340: 2},
      f"per-line={c2802_lines} (2 births in the c2800 Step-7 twin-print line 9338 + "
      f"2 FORWARD-token births inside the c2800 Next-block — the born-FOUR class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==478", tid_pre == 478, f"got={tid_pre}")
guard("anchor_nogold_pre==411", gold_pre == 411, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2803_pre==0", c2803_pre == 0, f"got={c2803_pre} (the forward token c2803 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2802_pre==4", c2802_pre == 4, f"got={c2802_pre} (born FOUR: the c2800 Step-7 twin-print "
      f"line 9338 TWICE + TWICE inside the c2800 Next-block — NOT the unborn class)")
guard("c2801_pre==14", c2801_pre == 14, f"got={c2801_pre}")
guard("c2800_pre==38", c2800_pre == 38, f"got={c2800_pre}")
guard("c2799_pre==78", c2799_pre == 78, f"got={c2799_pre}")
guard("c2798_pre==81", c2798_pre == 81, f"got={c2798_pre}")
guard("c2797_pre==79", c2797_pre == 79, f"got={c2797_pre}")
guard("c2796_pre==89", c2796_pre == 89, f"got={c2796_pre}")
guard("c2795_pre==104", c2795_pre == 104, f"got={c2795_pre}")
guard("c2794_pre==106", c2794_pre == 106, f"got={c2794_pre}")
guard("c2793_pre==111", c2793_pre == 111, f"got={c2793_pre}")
guard("c2792_pre==116", c2792_pre == 116, f"got={c2792_pre}")
guard("c2791_pre==107", c2791_pre == 107, f"got={c2791_pre}")
guard("c2790_pre==114", c2790_pre == 114, f"got={c2790_pre}")
guard("c2789_pre==110", c2789_pre == 110, f"got={c2789_pre}")
guard("c2788_pre==121", c2788_pre == 121, f"got={c2788_pre}")
guard("c2787_pre==122", c2787_pre == 122, f"got={c2787_pre}")
guard("c2786_pre==138", c2786_pre == 138, f"got={c2786_pre}")
guard("c2785_pre==126", c2785_pre == 126, f"got={c2785_pre}")
guard("c2784_pre==124", c2784_pre == 124, f"got={c2784_pre}")
guard("c2783_pre==125", c2783_pre == 125, f"got={c2783_pre}")
guard("c2782_pre==124", c2782_pre == 124, f"got={c2782_pre}")
guard("c2781_pre==129", c2781_pre == 129, f"got={c2781_pre}")
guard("c2780_pre==133", c2780_pre == 133, f"got={c2780_pre}")
guard("c2779_pre==134", c2779_pre == 134, f"got={c2779_pre}")
guard("c2778_pre==178", c2778_pre == 178, f"got={c2778_pre}")
guard("c2777_pre==150", c2777_pre == 150, f"got={c2777_pre}")
guard("c2776_pre==155", c2776_pre == 155, f"got={c2776_pre}")
guard("c2775_pre==164", c2775_pre == 164, f"got={c2775_pre}")
guard("c2774_pre==169", c2774_pre == 169, f"got={c2774_pre}")
guard("c2773_pre==173", c2773_pre == 173, f"got={c2773_pre}")
guard("c2772_pre==192", c2772_pre == 192, f"got={c2772_pre}")
guard("c2771_pre==182", c2771_pre == 182, f"got={c2771_pre}")
guard("c2770_pre==224", c2770_pre == 224, f"got={c2770_pre}")
guard("c2769_pre==171", c2769_pre == 171, f"got={c2769_pre}")
guard("c2768_pre==174", c2768_pre == 174, f"got={c2768_pre}")
guard("c2767_pre==223", c2767_pre == 223, f"got={c2767_pre}")
guard("c2766_pre==200", c2766_pre == 200, f"got={c2766_pre}")
guard("c2765_pre==165", c2765_pre == 165, f"got={c2765_pre}")
guard("c2764_pre==167", c2764_pre == 167, f"got={c2764_pre}")
guard("c2763_pre==175", c2763_pre == 175, f"got={c2763_pre}")
guard("c2762_pre==207", c2762_pre == 207, f"got={c2762_pre}")
guard("c2761_pre==221", c2761_pre == 221, f"got={c2761_pre}")
guard("c2760_pre==170", c2760_pre == 170, f"got={c2760_pre}")
guard("c2759_pre==170", c2759_pre == 170, f"got={c2759_pre}")
guard("c2758_pre==172", c2758_pre == 172, f"got={c2758_pre}")
guard("c2757_pre==175", c2757_pre == 175, f"got={c2757_pre}")
guard("c2756_pre==180", c2756_pre == 180, f"got={c2756_pre}")
guard("c2755_pre==187", c2755_pre == 187, f"got={c2755_pre}")
guard("c2754_pre==190", c2754_pre == 190, f"got={c2754_pre}")
guard("c2753_pre==197", c2753_pre == 197, f"got={c2753_pre}")
guard("c2752_pre==203", c2752_pre == 203, f"got={c2752_pre}")
guard("c2751_pre==189", c2751_pre == 189, f"got={c2751_pre}")
guard("c2750_pre==191", c2750_pre == 191, f"got={c2750_pre}")
guard("c2749_pre==195", c2749_pre == 195, f"got={c2749_pre}")
guard("c2748_pre==185", c2748_pre == 185, f"got={c2748_pre}")
guard("c2747_pre==184", c2747_pre == 184, f"got={c2747_pre}")

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
guard("post_worklog_lines==9352", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2802_next_bullet", last2.startswith("- Next: the c2802 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==479", tid_post == 479, f"got={tid_post}")
guard("anchor_nogold_post==412", gold_post == 412, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2801_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2801")]) == 1)
expect_c2803_mentions = wl2.count("c2803")
guard("c2803_mention_birth", expect_c2803_mentions == c2803_pre + block.count("c2803"),
      f"pre={c2803_pre} (unborn) + block births={block.count('c2803')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2803_pre + block.count('c2803')} got={expect_c2803_mentions}")
for tag, pre in (("c2802", c2802_pre), ("c2801", c2801_pre), ("c2800", c2800_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9340 -> 9352 (+12), c2801 entry + DRIFT-#49 pass-50 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
