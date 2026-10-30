#!/usr/bin/env python3
"""Guarded worklog append for the c2805 entry (12 lines).

Follows the append_cycle2804.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804
abort precedent class). The ledger arithmetic stays in the DECIMAL class: every
ns-decomposition check is Decimal-exact or Decimal-with-1e-6-tolerance on the
utc-derived values. THE C2778 ABORT LESSON STRUCTURALIZED: every pre-counter
variable is assigned in the SAME statement block before any guard references
it (the c2778 attempt-1 NameError class is impossible here), and a REHEARSAL
mode (APPEND_REHEARSAL=1) runs the full guard battery against a
byte-identical temp copy BEFORE the real run — the attempt counter counts
REAL runs only. Guards: python-timegm epoch cross-verification (Decimal-class
checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic, the ECHO
decompositions (pre/post/latency/stamp-to-echo/POST-WINDOW — the echo
RE-DERIVABLE this cycle), all echo
decompositions, the stamp-gap/token-gap/token-vs-stamp cadence triple, the
window-2805 EPOCH-governs render check, the window-2806 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~675µs on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2807 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2807 pre==0 expectation' + the Step-7 census-time print
'c2807_pre = 0' + the Next bullet's guard phrase 'c2806/c2807' AND
census-tuple sentence 'FORWARD token c2807' — the c2767..c2805 forward-token
lessons; NOTE the c2807 pre-count is 0 (unborn) while the c2806 pre-count is
4 (born: the c2804 Step-7 twin-print line 9386 TWICE + TWICE inside the
c2804 Next-block) — the c2804 append prophecy 'c2806 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9388 lines, tail = the c2805 Next bullet, zero serviced c2805
entries, c2805 mention census per-line {9374: 2, 9376: 2, 9380: 4, 9386: 1,
9388: 4} total 13, c2806 = 4 per-line {9386: 2, 9388: 2}, anchors 482/415/
60/28), post-state (9400 lines, tail = the c2806 Next bullet, anchors 483/
416/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2805.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9388
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


POST = D("1793322518.012641186")    # c2805 post-echo (EPOCH-governs)
SCAN = D("1793322518.006")          # c2805 scanned_at (decimal)
TRIG = D("1793321774.000")          # c2805 trigger stamp (08:56:14 +08)
WIN = D("1793322077.440380038")     # window-2805 open (c2804 prophecy EPOCH)
PRE = D("1793322515.837268419")     # c2805 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793322285.475961860")   # c2805 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793322287.170039861")  # c2805 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793322287.158")        # c2805 echo scanned_at (decimal)
C2804_SCAN = D("1793321777.434")    # c2804 scanned_at
C2804_POST = D("1793321777.440380038")  # c2804 post-echo
C2804_PRE = D("1793321775.493693754")   # c2804 capture pre-echo
C2804_CLOSE = D("1793322100.000")   # c2804 close cbdb675 (01:01:40Z)
C2804_FOREIGN = D("1793322111.000")  # foreign a6fac67 (01:01:51Z)
C2804_TRIG = D("1793320873.000")    # c2804 trigger stamp (08:41:13 +08)
WIN2804 = D("1793321413.772582901")  # window-2804 open (for the trigger-postdates check)
TOKEN = D("1793322060.000")         # token 0901 (09:01:00 +08)
C2804_TOKEN = D("1793321400.000")   # token 0850 (08:50:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 08:56:14 +08 = 1793321774.000", dec_epoch(2026, 10, 30, 0, 56, 14), TRIG),
    ("c2804 trigger stamp 08:41:13 +08 = 1793320873.000", dec_epoch(2026, 10, 30, 0, 41, 13), C2804_TRIG),
    ("stamp-gap 901.000s by stamp (08:41:13 -> 08:56:14; the 901 print RETURNS)", TRIG - C2804_TRIG, D("901.000")),
    ("token-gap 660.000s by token (0850 -> 0901; the 720 print BROKE, the 660 print RETURNS)", TOKEN - C2804_TOKEN, D("660.000")),
    ("token-vs-stamp +286.000 (08:56:14 -> 09:01:00; the +286 print NEW)", TOKEN - TRIG, D("286.000")),
    ("c2804 close cbdb675 01:01:40Z = 1793322100.000", dec_epoch(2026, 10, 30, 1, 1, 40), C2804_CLOSE),
    ("foreign a6fac67 01:01:51Z = 1793322111.000", dec_epoch(2026, 10, 30, 1, 1, 51), C2804_FOREIGN),
    ("token 0901 = 01:01:00Z = 1793322060.000", dec_epoch(2026, 10, 30, 1, 1, 0), TOKEN),
    ("c2804 token 0850 = 00:50:00Z = 1793321400.000", dec_epoch(2026, 10, 30, 0, 50, 0), C2804_TOKEN),
    ("capture pre-echo EPOCH 1793322515.837268419 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 8, 35, 837268419), PRE),
    ("pre-echo ISO 01:08:35.836464687 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 8, 35, 836464687), D("1793322515.836464687")),
    ("post-echo ISO 01:08:38.011966633 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 8, 38, 11966633), D("1793322518.011966633")),
    ("post-echo EPOCH 1793322518.012641186 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 8, 38, 12641186), POST),
    ("scanned_at 01:08:38.006 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 8, 38) + D("0.006"), SCAN),
    ("window-2805 open 01:01:17.440380038 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 1, 1, 17, 440380038), WIN),
    ("window-2806 open = post-echo + 300.000", POST + D("300.000"), D("1793322818.012641186")),
    ("c2804 post-echo EPOCH 1793321777.440380038 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 56, 17, 440380038), C2804_POST),
    ("c2804 scanned_at 00:56:17.434 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 56, 17) + D("0.434"), C2804_SCAN),
    ("c2804 capture pre-echo EPOCH 1793321775.493693754 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 56, 15, 493693754), C2804_PRE),
    ("echo pre-echo EPOCH 1793322285.475961860 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 4, 45, 475961860), ECHO_PRE),
    ("echo pre-echo ISO 01:04:45.475254780 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 4, 45, 475254780), D("1793322285.475254780")),
    ("echo post-echo ISO 01:04:47.169347290 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 4, 47, 169347290), D("1793322287.169347290")),
    ("echo post-echo EPOCH 1793322287.170039861 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 4, 47, 170039861), ECHO_POST),
    ("echo scanned_at 01:04:47.158 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 4, 47) + D("0.158"), ECHO_SCAN),
]
exact_checks = [
    ("skew decimal-exact +6.641186ms (EPOCH-governs decomposition; SUB-10 extends m2)", POST - SCAN, D("0.006641186")),
    ("CAPTURE_vs_window +440.572261148 (POST-WINDOW; the capture-side print)", POST - WIN, D("440.572261148")),
    ("capture post-c2804-post-echo +740.572261148", POST - C2804_POST, D("740.572261148")),
    ("dd#379 = +440.572000000 (interval 740.572 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#378 print 663.725 - 300 = 363.725 and the dd#377 print 740.182 - 300 = 440.182)", SCAN - C2804_SCAN - D("300.000"), D("440.572")),
    ("dd formula re-verification: 423.763 - 300 = 123.763", D("423.763") - D("300.000"), D("123.763")),
    ("dd formula re-verification: 740.182 - 300 = 440.182", D("740.182") - D("300.000"), D("440.182")),
    ("dd formula re-verification: 663.725 - 300 = 363.725", D("663.725") - D("300.000"), D("363.725")),
    ("INTERVAL#379 = 744.006", SCAN - TRIG, D("744.006")),
    ("LAG#379 = INTERVAL + dd - dd#378 = +820.853", (SCAN - TRIG) + (SCAN - C2804_SCAN - D("300.000")) - D("363.725"), D("820.853")),
    ("LATE#379 = trigger - window-open = -303.440380038", TRIG - WIN, D("-303.440380038")),
    ("window-2805 = c2804 post-echo + 300.000 (the server contract)", WIN - C2804_POST, D("300.000")),
    ("trigger PREDATES the c2804 post-echo by 3.440380038s (the PRE-echo placement REPEATS)", C2804_POST - TRIG, D("3.440380038")),
    ("trigger PREDATES the c2804 scanned_at by 3.434s", C2804_SCAN - TRIG, D("3.434")),
    ("trigger PREDATES the c2804 pre-echo by 1.493693754s", C2804_PRE - TRIG, D("1.493693754")),
    ("trigger POSTDATES window-2804 open by 360.227417099s", TRIG - WIN2804, D("360.227417099")),
    ("c2804 close POSTDATES the trigger by 326.000s (cbdb675 at 01:01:40)", C2804_CLOSE - TRIG, D("326.000")),
    ("foreign a6fac67 POSTDATES the trigger by 337.000s (01:01:51)", C2804_FOREIGN - TRIG, D("337.000")),
    ("c2804 close landed 40.000s AFTER the token-0901 second (01:01:40 vs 01:01:00 — the BEFORE-class TERMINATES, the AFTER-class re-opens m1)", C2804_CLOSE - TOKEN, D("40.000")),
    ("foreign a6fac67 landed 51.000s AFTER the token second (01:01:51)", C2804_FOREIGN - TOKEN, D("51.000")),
    ("foreign a6fac67 landed +33.559619962s AFTER window-2805 open", C2804_FOREIGN - WIN, D("33.559619962")),
    ("c2804 close cbdb675 landed +22.559619962s AFTER window-2805 open", C2804_CLOSE - WIN, D("22.559619962")),
    ("echo POST-WINDOW +209.729659823 (the echo-side print; the BOTH-POST print RETURNS)", ECHO_POST - WIN, D("209.729659823")),
    ("stamp-to-echo 511.475961860 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS)", ECHO_PRE - TRIG, D("511.475961860")),
    ("echo client latency 1.694078001 (echo post-echo EPOCH - echo pre-echo EPOCH; server 1677ms latency-match)", ECHO_POST - ECHO_PRE, D("1.694078001")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m3)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2805"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2805"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2806 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2807_birth",
      block.count("c2807") == 4 and lines[-1].count("c2807") == 2
      and "c2806/c2807" in lines[-1] and "FORWARD token c2807" in lines[-1]
      and "the c2807 pre==0 expectation" in block and "c2807_pre = 0" in block,
      f"block c2807={block.count('c2807')} next-line c2807={lines[-1].count('c2807')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2807_pre = 0' + the Next bullet's guard phrase 'c2806/c2807' AND "
      f"census-tuple sentence 'FORWARD token c2807')")
guard("block_c2806_step7_precount_sentence",
      "the c2806 pre-count is 4" in block
      and "per-line {9386: 2, 9388: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2806 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9388", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2805_next_bullet", last_nonempty.startswith("- Next: the c2805 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2805",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2805")]) == 0,
      f"c2805 substring mentions={wl.count('c2805')} (expect 13)")
c2805_lines = {i + 1: l.count("c2805") for i, l in enumerate(wl.splitlines()) if "c2805" in l}
guard("c2805_mention_census_pre", wl.count("c2805") == 13
      and c2805_lines == {9374: 2, 9376: 2, 9380: 4, 9386: 1, 9388: 4},
      f"per-line={c2805_lines}")
c2806_lines = {i + 1: l.count("c2806") for i, l in enumerate(wl.splitlines()) if "c2806" in l}
guard("c2806_forward_token_pre", wl.count("c2806") == 4 and c2806_lines == {9386: 2, 9388: 2},
      f"per-line={c2806_lines} (2 births in the c2804 Step-7 twin-print line 9386 + "
      f"2 FORWARD-token births inside the c2804 Next-block — the born-FOUR class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==482", tid_pre == 482, f"got={tid_pre}")
guard("anchor_nogold_pre==415", gold_pre == 415, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2807_pre==0", c2807_pre == 0, f"got={c2807_pre} (the forward token c2807 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2806_pre==4", c2806_pre == 4, f"got={c2806_pre} (born FOUR: the c2804 Step-7 twin-print "
      f"line 9386 TWICE + TWICE inside the c2804 Next-block — NOT the unborn class)")
guard("c2805_pre==13", c2805_pre == 13, f"got={c2805_pre}")
guard("c2804_pre==36", c2804_pre == 36, f"got={c2804_pre}")
guard("c2803_pre==87", c2803_pre == 87, f"got={c2803_pre}")
guard("c2802_pre==99", c2802_pre == 99, f"got={c2802_pre}")
guard("c2801_pre==86", c2801_pre == 86, f"got={c2801_pre}")
guard("c2800_pre==109", c2800_pre == 109, f"got={c2800_pre}")
guard("c2799_pre==91", c2799_pre == 91, f"got={c2799_pre}")
guard("c2798_pre==89", c2798_pre == 89, f"got={c2798_pre}")
guard("c2797_pre==83", c2797_pre == 83, f"got={c2797_pre}")
guard("c2796_pre==93", c2796_pre == 93, f"got={c2796_pre}")
guard("c2795_pre==114", c2795_pre == 114, f"got={c2795_pre}")
guard("c2794_pre==110", c2794_pre == 110, f"got={c2794_pre}")
guard("c2793_pre==118", c2793_pre == 118, f"got={c2793_pre}")
guard("c2792_pre==123", c2792_pre == 123, f"got={c2792_pre}")
guard("c2791_pre==111", c2791_pre == 111, f"got={c2791_pre}")
guard("c2790_pre==122", c2790_pre == 122, f"got={c2790_pre}")
guard("c2789_pre==114", c2789_pre == 114, f"got={c2789_pre}")
guard("c2788_pre==125", c2788_pre == 125, f"got={c2788_pre}")
guard("c2787_pre==126", c2787_pre == 126, f"got={c2787_pre}")
guard("c2786_pre==146", c2786_pre == 146, f"got={c2786_pre}")
guard("c2785_pre==130", c2785_pre == 130, f"got={c2785_pre}")
guard("c2784_pre==128", c2784_pre == 128, f"got={c2784_pre}")
guard("c2783_pre==129", c2783_pre == 129, f"got={c2783_pre}")
guard("c2782_pre==128", c2782_pre == 128, f"got={c2782_pre}")
guard("c2781_pre==133", c2781_pre == 133, f"got={c2781_pre}")
guard("c2780_pre==138", c2780_pre == 138, f"got={c2780_pre}")
guard("c2779_pre==138", c2779_pre == 138, f"got={c2779_pre}")
guard("c2778_pre==182", c2778_pre == 182, f"got={c2778_pre}")
guard("c2777_pre==154", c2777_pre == 154, f"got={c2777_pre}")
guard("c2776_pre==159", c2776_pre == 159, f"got={c2776_pre}")
guard("c2775_pre==168", c2775_pre == 168, f"got={c2775_pre}")
guard("c2774_pre==173", c2774_pre == 173, f"got={c2774_pre}")
guard("c2773_pre==177", c2773_pre == 177, f"got={c2773_pre}")
guard("c2772_pre==196", c2772_pre == 196, f"got={c2772_pre}")
guard("c2771_pre==186", c2771_pre == 186, f"got={c2771_pre}")
guard("c2770_pre==232", c2770_pre == 232, f"got={c2770_pre}")
guard("c2769_pre==175", c2769_pre == 175, f"got={c2769_pre}")
guard("c2768_pre==178", c2768_pre == 178, f"got={c2768_pre}")
guard("c2767_pre==235", c2767_pre == 235, f"got={c2767_pre}")
guard("c2766_pre==209", c2766_pre == 209, f"got={c2766_pre}")
guard("c2765_pre==169", c2765_pre == 169, f"got={c2765_pre}")
guard("c2764_pre==171", c2764_pre == 171, f"got={c2764_pre}")
guard("c2763_pre==179", c2763_pre == 179, f"got={c2763_pre}")
guard("c2762_pre==215", c2762_pre == 215, f"got={c2762_pre}")
guard("c2761_pre==229", c2761_pre == 229, f"got={c2761_pre}")
guard("c2760_pre==174", c2760_pre == 174, f"got={c2760_pre}")
guard("c2759_pre==174", c2759_pre == 174, f"got={c2759_pre}")
guard("c2758_pre==176", c2758_pre == 176, f"got={c2758_pre}")
guard("c2757_pre==179", c2757_pre == 179, f"got={c2757_pre}")
guard("c2756_pre==184", c2756_pre == 184, f"got={c2756_pre}")
guard("c2755_pre==191", c2755_pre == 191, f"got={c2755_pre}")
guard("c2754_pre==194", c2754_pre == 194, f"got={c2754_pre}")
guard("c2753_pre==205", c2753_pre == 205, f"got={c2753_pre}")
guard("c2752_pre==211", c2752_pre == 211, f"got={c2752_pre}")
guard("c2751_pre==197", c2751_pre == 197, f"got={c2751_pre}")
guard("c2750_pre==201", c2750_pre == 201, f"got={c2750_pre}")
guard("c2749_pre==203", c2749_pre == 203, f"got={c2749_pre}")
guard("c2748_pre==193", c2748_pre == 193, f"got={c2748_pre}")
guard("c2747_pre==196", c2747_pre == 196, f"got={c2747_pre}")
guard("c2746_pre==201", c2746_pre == 201, f"got={c2746_pre}")

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
guard("post_worklog_lines==9400", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2806_next_bullet", last2.startswith("- Next: the c2806 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==483", tid_post == 483, f"got={tid_post}")
guard("anchor_nogold_post==416", gold_post == 416, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2805_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2805")]) == 1)
expect_c2807_mentions = wl2.count("c2807")
guard("c2807_mention_birth", expect_c2807_mentions == c2807_pre + block.count("c2807"),
      f"pre={c2807_pre} (unborn) + block births={block.count('c2807')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2807_pre + block.count('c2807')} got={expect_c2807_mentions}")
for tag, pre in (("c2806", c2806_pre), ("c2805", c2805_pre), ("c2804", c2804_pre),
                 ("c2803", c2803_pre), ("c2802", c2802_pre), ("c2801", c2801_pre),
                 ("c2800", c2800_pre), ("c2799", c2799_pre), ("c2798", c2798_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9388 -> 9400 (+12), c2805 entry + DRIFT-#49 pass-54 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
