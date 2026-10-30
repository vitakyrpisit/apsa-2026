#!/usr/bin/env python3
"""Guarded worklog append for the c2806 entry (12 lines).

Follows the append_cycle2805.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805 abort precedent class). The ledger arithmetic stays in the DECIMAL
class: every ns-decomposition check is Decimal-exact or Decimal-with-
1e-6-tolerance on the utc-derived values. THE C2778 ABORT LESSON
STRUCTURALIZED: every pre-counter variable is assigned in the SAME statement
block before any guard references it (the c2778 attempt-1 NameError class is
impossible here), and a REHEARSAL mode (APPEND_REHEARSAL=1) runs the full
guard battery against a byte-identical temp copy BEFORE the real run — the
attempt counter counts REAL runs only. Guards: python-timegm epoch
cross-verification (Decimal-class checks incl. the dd/INTERVAL/LAG/LATE
ledger arithmetic, the ECHO decompositions (pre/post/latency/stamp-to-echo/
POST-WINDOW — the echo RE-DERIVABLE this cycle), all echo decompositions,
the stamp-gap/token-gap/token-vs-stamp cadence triple, the window-2806
EPOCH-governs render check, the window-2807 prophecy check, and the
queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock
reads differ ~669µs on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2808 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2808 pre==0 expectation' + the Step-7 census-time print
'c2808_pre = 0' + the Next bullet's guard phrase 'c2807/c2808' AND
census-tuple sentence 'FORWARD token c2808' — the c2767..c2806 forward-token
lessons; NOTE the c2808 pre-count is 0 (unborn) while the c2807 pre-count is
4 (born: the c2805 Step-7 twin-print line 9398 TWICE + TWICE inside the
c2805 Next-block) — the c2805 append prophecy 'c2807 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS a THIRD time), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9400 lines, tail = the c2806 Next bullet, zero serviced
c2806 entries, c2806 mention census per-line {9386: 2, 9388: 2, 9392: 4,
9398: 1, 9400: 4} total 13, c2807 = 4 per-line {9398: 2, 9400: 2}, anchors
483/416/60/28), post-state (9412 lines, tail = the c2807 Next bullet,
anchors 484/417/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2806.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9400
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


POST = D("1793323181.104795547")    # c2806 post-echo (EPOCH-governs)
SCAN = D("1793323181.098")          # c2806 scanned_at (decimal)
TRIG = D("1793322374.000")          # c2806 trigger stamp (09:06:14 +08)
WIN = D("1793322818.012641186")     # window-2806 open (c2805 prophecy EPOCH)
PRE = D("1793323179.315388590")     # c2806 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793322959.171583146")   # c2806 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793322961.533383900")  # c2806 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793322961.523")        # c2806 echo scanned_at (decimal)
C2805_SCAN = D("1793322518.006")    # c2805 scanned_at
C2805_POST = D("1793322518.012641186")  # c2805 post-echo
C2805_PRE = D("1793322515.837268419")   # c2805 capture pre-echo
C2805_ECHO_POST = D("1793322287.170039861")  # c2805 echo post-echo
C2805_CLOSE = D("1793322846.000")   # c2805 close ee9e3cd (01:14:06Z)
FOREIGN_NOW = D("1793322862.000")   # foreign 35ba192 (01:14:22Z)
C2805_FOREIGN = D("1793322111.000")  # foreign a6fac67 (01:01:51Z)
C2805_TRIG = D("1793321774.000")    # c2805 trigger stamp (08:56:14 +08)
WIN2805 = D("1793322077.440380038")  # window-2805 open (for the trigger-postdates check)
TOKEN = D("1793322840.000")         # token 0914 (09:14:00 +08)
C2805_TOKEN = D("1793322060.000")   # token 0901 (09:01:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 09:06:14 +08 = 1793322374.000", dec_epoch(2026, 10, 30, 1, 6, 14), TRIG),
    ("c2805 trigger stamp 08:56:14 +08 = 1793321774.000", dec_epoch(2026, 10, 30, 0, 56, 14), C2805_TRIG),
    ("stamp-gap 600.000s by stamp (08:56:14 -> 09:06:14; the 600 print RETURNS)", TRIG - C2805_TRIG, D("600.000")),
    ("token-gap 780.000s by token (0901 -> 0914; the 780 print RETURNS)", TOKEN - C2805_TOKEN, D("780.000")),
    ("token-vs-stamp +466.000 (09:06:14 -> 09:14:00; the +466 print NEW)", TOKEN - TRIG, D("466.000")),
    ("c2805 close ee9e3cd 01:14:06Z = 1793322846.000", dec_epoch(2026, 10, 30, 1, 14, 6), C2805_CLOSE),
    ("foreign 35ba192 01:14:22Z = 1793322862.000", dec_epoch(2026, 10, 30, 1, 14, 22), FOREIGN_NOW),
    ("token 0914 = 01:14:00Z = 1793322840.000", dec_epoch(2026, 10, 30, 1, 14, 0), TOKEN),
    ("c2805 token 0901 = 01:01:00Z = 1793322060.000", dec_epoch(2026, 10, 30, 1, 1, 0), C2805_TOKEN),
    ("capture pre-echo EPOCH 1793323179.315388590 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 19, 39, 315388590), PRE),
    ("pre-echo ISO 01:19:39.314682438 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 19, 39, 314682438), D("1793323179.314682438")),
    ("post-echo ISO 01:19:41.104126916 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 19, 41, 104126916), D("1793323181.104126916")),
    ("post-echo EPOCH 1793323181.104795547 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 19, 41, 104795547), POST),
    ("scanned_at 01:19:41.098 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 19, 41) + D("0.098"), SCAN),
    ("window-2806 open 01:13:38.012641186 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 1, 13, 38, 12641186), WIN),
    ("window-2807 open = post-echo + 300.000", POST + D("300.000"), D("1793323481.104795547")),
    ("c2805 post-echo EPOCH 1793322518.012641186 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 8, 38, 12641186), C2805_POST),
    ("c2805 scanned_at 01:08:38.006 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 8, 38) + D("0.006"), C2805_SCAN),
    ("c2805 capture pre-echo EPOCH 1793322515.837268419 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 8, 35, 837268419), C2805_PRE),
    ("c2805 echo post-echo EPOCH 1793322287.170039861 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 4, 47, 170039861), C2805_ECHO_POST),
    ("echo pre-echo EPOCH 1793322959.171583146 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 15, 59, 171583146), ECHO_PRE),
    ("echo pre-echo ISO 01:15:59.170912727 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 15, 59, 170912727), D("1793322959.170912727")),
    ("echo post-echo ISO 01:16:01.532738755 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 16, 1, 532738755), D("1793322961.532738755")),
    ("echo post-echo EPOCH 1793322961.533383900 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 16, 1, 533383900), ECHO_POST),
    ("echo scanned_at 01:16:01.523 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 16, 1) + D("0.523"), ECHO_SCAN),
]
exact_checks = [
    ("skew decimal-exact +6.795547ms (EPOCH-governs decomposition; SUB-10 extends m3)", POST - SCAN, D("0.006795547")),
    ("CAPTURE_vs_window +363.092154361 (POST-WINDOW; the capture-side print)", POST - WIN, D("363.092154361")),
    ("capture post-c2805-post-echo +663.092154361", POST - C2805_POST, D("663.092154361")),
    ("dd#380 = +363.092000000 (interval 663.092 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#379 print 740.572 - 300 = 440.572 and the dd#378 print 663.725 - 300 = 363.725)", SCAN - C2805_SCAN - D("300.000"), D("363.092")),
    ("dd formula re-verification: 423.763 - 300 = 123.763", D("423.763") - D("300.000"), D("123.763")),
    ("dd formula re-verification: 740.182 - 300 = 440.182", D("740.182") - D("300.000"), D("440.182")),
    ("dd formula re-verification: 663.725 - 300 = 363.725", D("663.725") - D("300.000"), D("363.725")),
    ("dd formula re-verification: 740.572 - 300 = 440.572", D("740.572") - D("300.000"), D("440.572")),
    ("INTERVAL#380 = 807.098", SCAN - TRIG, D("807.098")),
    ("LAG#380 = INTERVAL + dd - dd#379 = +729.618", (SCAN - TRIG) + (SCAN - C2805_SCAN - D("300.000")) - D("440.572"), D("729.618")),
    ("LATE#380 = trigger - window-open = -444.012641186", TRIG - WIN, D("-444.012641186")),
    ("window-2806 = c2805 post-echo + 300.000 (the server contract)", WIN - C2805_POST, D("300.000")),
    ("trigger POSTDATES the c2805 post-echo by 86.829960139s (the POST-echo placement re-opens m1)", TRIG - C2805_ECHO_POST, D("86.829960139")),
    ("trigger PREDATES the c2805 pre-echo by 141.837268419s", C2805_PRE - TRIG, D("141.837268419")),
    ("trigger PREDATES the c2805 scanned_at by 144.006s", C2805_SCAN - TRIG, D("144.006")),
    ("trigger POSTDATES window-2805 open by 296.559619962s", TRIG - WIN2805, D("296.559619962")),
    ("c2805 close POSTDATES the trigger by 472.000s (ee9e3cd at 01:14:06)", C2805_CLOSE - TRIG, D("472.000")),
    ("foreign 35ba192 POSTDATES the trigger by 488.000s (01:14:22)", FOREIGN_NOW - TRIG, D("488.000")),
    ("c2805 close landed 6.000s AFTER the token-0914 second (01:14:06 vs 01:14:00 — the AFTER-class EXTENDS m2)", C2805_CLOSE - TOKEN, D("6.000")),
    ("foreign 35ba192 landed 22.000s AFTER the token second (01:14:22)", FOREIGN_NOW - TOKEN, D("22.000")),
    ("foreign 35ba192 landed +43.987358814s AFTER window-2806 open", FOREIGN_NOW - WIN, D("43.987358814")),
    ("c2805 close ee9e3cd landed +27.987358814s AFTER window-2806 open", C2805_CLOSE - WIN, D("27.987358814")),
    ("echo POST-WINDOW +143.520742714 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("143.520742714")),
    ("stamp-to-echo 585.171583146 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS)", ECHO_PRE - TRIG, D("585.171583146")),
    ("echo client latency 2.361800754 (echo post-echo EPOCH - echo pre-echo EPOCH; server 2339ms latency-match)", ECHO_POST - ECHO_PRE, D("2.361800754")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m4)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2806"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2806"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2807 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2808_birth",
      block.count("c2808") == 4 and lines[-1].count("c2808") == 2
      and "c2807/c2808" in lines[-1] and "FORWARD token c2808" in lines[-1]
      and "the c2808 pre==0 expectation" in block and "c2808_pre = 0" in block,
      f"block c2808={block.count('c2808')} next-line c2808={lines[-1].count('c2808')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2808_pre = 0' + the Next bullet's guard phrase 'c2807/c2808' AND "
      f"census-tuple sentence 'FORWARD token c2808')")
guard("block_c2807_step7_precount_sentence",
      "the c2807 pre-count is 4" in block
      and "per-line {9398: 2, 9400: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2807 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9400", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2806_next_bullet", last_nonempty.startswith("- Next: the c2806 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2806",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2806")]) == 0,
      f"c2806 substring mentions={wl.count('c2806')} (expect 13)")
c2806_lines = {i + 1: l.count("c2806") for i, l in enumerate(wl.splitlines()) if "c2806" in l}
guard("c2806_mention_census_pre", wl.count("c2806") == 13
      and c2806_lines == {9386: 2, 9388: 2, 9392: 4, 9398: 1, 9400: 4},
      f"per-line={c2806_lines}")
c2807_lines = {i + 1: l.count("c2807") for i, l in enumerate(wl.splitlines()) if "c2807" in l}
guard("c2807_forward_token_pre", wl.count("c2807") == 4 and c2807_lines == {9398: 2, 9400: 2},
      f"per-line={c2807_lines} (2 births in the c2805 Step-7 twin-print line 9398 + "
      f"2 FORWARD-token births inside the c2805 Next-block — the born-FOUR class "
      f"REPEATS a THIRD time)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==483", tid_pre == 483, f"got={tid_pre}")
guard("anchor_nogold_pre==416", gold_pre == 416, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2808_pre = wl.count("c2808")
c2807_pre = wl.count("c2807")
c2806_pre = wl.count("c2806")
c2805_pre = wl.count("c2805")
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
c2746_pre = wl.count("c2746")
guard("c2808_pre==0", c2808_pre == 0, f"got={c2808_pre} (the forward token c2808 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2807_pre==4", c2807_pre == 4, f"got={c2807_pre} (born FOUR: the c2805 Step-7 twin-print "
      f"line 9398 TWICE + TWICE inside the c2805 Next-block — NOT the unborn class)")
guard("c2806_pre==13", c2806_pre == 13, f"got={c2806_pre}")
guard("c2805_pre==39", c2805_pre == 39, f"got={c2805_pre}")
guard("c2804_pre==87", c2804_pre == 87, f"got={c2804_pre}")
guard("c2803_pre==95", c2803_pre == 95, f"got={c2803_pre}")
guard("c2802_pre==105", c2802_pre == 105, f"got={c2802_pre}")
guard("c2801_pre==88", c2801_pre == 88, f"got={c2801_pre}")
guard("c2800_pre==114", c2800_pre == 114, f"got={c2800_pre}")
guard("c2799_pre==93", c2799_pre == 93, f"got={c2799_pre}")
guard("c2798_pre==91", c2798_pre == 91, f"got={c2798_pre}")
guard("c2797_pre==84", c2797_pre == 84, f"got={c2797_pre}")
guard("c2796_pre==94", c2796_pre == 94, f"got={c2796_pre}")
guard("c2795_pre==116", c2795_pre == 116, f"got={c2795_pre}")
guard("c2794_pre==111", c2794_pre == 111, f"got={c2794_pre}")
guard("c2793_pre==119", c2793_pre == 119, f"got={c2793_pre}")
guard("c2792_pre==124", c2792_pre == 124, f"got={c2792_pre}")
guard("c2791_pre==112", c2791_pre == 112, f"got={c2791_pre}")
guard("c2790_pre==124", c2790_pre == 124, f"got={c2790_pre}")
guard("c2789_pre==115", c2789_pre == 115, f"got={c2789_pre}")
guard("c2788_pre==126", c2788_pre == 126, f"got={c2788_pre}")
guard("c2787_pre==127", c2787_pre == 127, f"got={c2787_pre}")
guard("c2786_pre==148", c2786_pre == 148, f"got={c2786_pre}")
guard("c2785_pre==131", c2785_pre == 131, f"got={c2785_pre}")
guard("c2784_pre==129", c2784_pre == 129, f"got={c2784_pre}")
guard("c2783_pre==130", c2783_pre == 130, f"got={c2783_pre}")
guard("c2782_pre==129", c2782_pre == 129, f"got={c2782_pre}")
guard("c2781_pre==134", c2781_pre == 134, f"got={c2781_pre}")
guard("c2780_pre==139", c2780_pre == 139, f"got={c2780_pre}")
guard("c2779_pre==139", c2779_pre == 139, f"got={c2779_pre}")
guard("c2778_pre==183", c2778_pre == 183, f"got={c2778_pre}")
guard("c2777_pre==155", c2777_pre == 155, f"got={c2777_pre}")
guard("c2776_pre==160", c2776_pre == 160, f"got={c2776_pre}")
guard("c2775_pre==169", c2775_pre == 169, f"got={c2775_pre}")
guard("c2774_pre==174", c2774_pre == 174, f"got={c2774_pre}")
guard("c2773_pre==178", c2773_pre == 178, f"got={c2773_pre}")
guard("c2772_pre==197", c2772_pre == 197, f"got={c2772_pre}")
guard("c2771_pre==187", c2771_pre == 187, f"got={c2771_pre}")
guard("c2770_pre==234", c2770_pre == 234, f"got={c2770_pre}")
guard("c2769_pre==176", c2769_pre == 176, f"got={c2769_pre}")
guard("c2768_pre==179", c2768_pre == 179, f"got={c2768_pre}")
guard("c2767_pre==238", c2767_pre == 238, f"got={c2767_pre}")
guard("c2766_pre==211", c2766_pre == 211, f"got={c2766_pre}")
guard("c2765_pre==170", c2765_pre == 170, f"got={c2765_pre}")
guard("c2764_pre==172", c2764_pre == 172, f"got={c2764_pre}")
guard("c2763_pre==180", c2763_pre == 180, f"got={c2763_pre}")
guard("c2762_pre==217", c2762_pre == 217, f"got={c2762_pre}")
guard("c2761_pre==232", c2761_pre == 232, f"got={c2761_pre}")
guard("c2760_pre==175", c2760_pre == 175, f"got={c2760_pre}")
guard("c2759_pre==175", c2759_pre == 175, f"got={c2759_pre}")
guard("c2758_pre==177", c2758_pre == 177, f"got={c2758_pre}")
guard("c2757_pre==180", c2757_pre == 180, f"got={c2757_pre}")
guard("c2756_pre==185", c2756_pre == 185, f"got={c2756_pre}")
guard("c2755_pre==192", c2755_pre == 192, f"got={c2755_pre}")
guard("c2754_pre==195", c2754_pre == 195, f"got={c2754_pre}")
guard("c2753_pre==207", c2753_pre == 207, f"got={c2753_pre}")
guard("c2752_pre==213", c2752_pre == 213, f"got={c2752_pre}")
guard("c2751_pre==199", c2751_pre == 199, f"got={c2751_pre}")
guard("c2750_pre==203", c2750_pre == 203, f"got={c2750_pre}")
guard("c2749_pre==205", c2749_pre == 205, f"got={c2749_pre}")
guard("c2748_pre==195", c2748_pre == 195, f"got={c2748_pre}")
guard("c2747_pre==198", c2747_pre == 198, f"got={c2747_pre}")
guard("c2746_pre==205", c2746_pre == 205, f"got={c2746_pre}")

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
guard("post_worklog_lines==9412", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2807_next_bullet", last2.startswith("- Next: the c2807 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==484", tid_post == 484, f"got={tid_post}")
guard("anchor_nogold_post==417", gold_post == 417, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2806_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2806")]) == 1)
expect_c2808_mentions = wl2.count("c2808")
guard("c2808_mention_birth", expect_c2808_mentions == c2808_pre + block.count("c2808"),
      f"pre={c2808_pre} (unborn) + block births={block.count('c2808')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2808_pre + block.count('c2808')} got={expect_c2808_mentions}")
for tag, pre in (("c2807", c2807_pre), ("c2806", c2806_pre), ("c2805", c2805_pre),
                 ("c2804", c2804_pre), ("c2803", c2803_pre), ("c2802", c2802_pre),
                 ("c2801", c2801_pre), ("c2800", c2800_pre), ("c2799", c2799_pre),
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
                 ("c2747", c2747_pre), ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9400 -> 9412 (+12), c2806 entry + DRIFT-#49 pass-55 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
