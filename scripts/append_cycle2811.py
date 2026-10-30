#!/usr/bin/env python3
"""Guarded worklog append for the c2811 entry (12 lines).

Follows the append_cycle2810.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810 abort precedent class). The ledger arithmetic stays in the
DECIMAL class: every ns-decomposition check is Decimal-exact or Decimal-with-
1e-6-tolerance on the utc-derived values. THE C2778 ABORT LESSON
STRUCTURALIZED: every pre-counter variable is assigned in the SAME statement
block before any guard references it (the c2778 attempt-1 NameError class is
impossible here), and a REHEARSAL mode (APPEND_REHEARSAL=1) runs the full
guard battery against a byte-identical temp copy BEFORE the real run — the
attempt counter counts REAL runs only. Guards: python-timegm epoch
cross-verification (Decimal-class checks incl. the dd/INTERVAL/LAG/LATE
ledger arithmetic, the ECHO decompositions (pre/post/latency/stamp-to-echo/
POST-WINDOW — the echo RE-DERIVABLE this cycle), all echo decompositions,
the stamp-gap/token-gap/token-vs-stamp cadence triple, the window-2811
EPOCH-governs render check, the window-2812 prophecy check, and the
queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock
reads differ ~656µs on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2813 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2813 pre==0 expectation' + the Step-7 census-time print
'c2813_pre = 0' + the Next bullet's guard phrase 'c2812/c2813' AND
census-tuple sentence 'FORWARD token c2813' — the c2767..c2811 forward-token
lessons; NOTE the c2813 pre-count is 0 (unborn) while the c2812 pre-count is
4 (born: the c2810 Step-7 twin-print line 9458 TWICE + TWICE inside the
c2810 Next-block) — the c2810 append prophecy 'c2812 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS an EIGHTH time), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9460 lines, tail = the c2811 Next bullet, zero serviced
c2811 entries, c2811 mention census per-line {9446: 2, 9448: 2, 9452: 5,
9458: 1, 9460: 4} total 14, c2812 = 4 per-line {9458: 2, 9460: 2}, anchors
488/421/60/28), post-state (9472 lines, tail = the c2812 Next bullet,
anchors 489/422/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2811.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9460
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


POST = D("1793327226.818599805")    # c2811 post-echo (EPOCH-governs)
SCAN = D("1793327226.813")          # c2811 scanned_at (decimal)
TRIG = D("1793326276.000")          # c2811 trigger stamp (10:11:16 +08)
WIN = D("1793326566.804677305")     # window-2811 open (c2810 prophecy EPOCH)
PRE = D("1793327225.013423065")     # c2811 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793326689.371235484")   # c2811 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793326691.169645781")  # c2811 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793326691.166")        # c2811 echo scanned_at (decimal)
C2810_SCAN = D("1793326266.798")    # c2810 scanned_at
C2810_POST = D("1793326266.804677305")  # c2810 post-echo
C2810_PRE = D("1793326265.037661240")   # c2810 capture pre-echo
C2810_ECHO_POST = D("1793326093.975704459")  # c2810 echo post-echo
C2810_CLOSE = D("1793326618.000")   # c2810 close d228cc8 (02:16:58Z)
FOREIGN_NOW = D("1793326639.000")   # foreign 92b5acc (02:17:19Z)
C2810_TRIG = D("1793325375.000")    # c2810 trigger stamp (09:56:15 +08)
WIN2810 = D("1793325687.842975825")  # window-2810 open (for the contract re-check)
TOKEN = D("1793326620.000")         # token 1017 (10:17:00 +08)
C2810_TOKEN = D("1793325720.000")   # token 1002 (10:02:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 10:11:16 +08 = 1793326276.000", dec_epoch(2026, 10, 30, 2, 11, 16), TRIG),
    ("c2810 trigger stamp 09:56:15 +08 = 1793325375.000", dec_epoch(2026, 10, 30, 1, 56, 15), C2810_TRIG),
    ("stamp-gap 901.000s by stamp (09:56:15 -> 10:11:16; 14 priors of the exact form)", TRIG - C2810_TRIG, D("901.000")),
    ("token-gap 900.000s by token (1002 -> 1017; the 900 print NEW, 0 priors)", TOKEN - C2810_TOKEN, D("900.000")),
    ("token-vs-stamp +344.000 (10:11:16 -> 10:17:00; the +344 print, 4 priors)", TOKEN - TRIG, D("344.000")),
    ("c2810 close d228cc8 02:16:58Z = 1793326618.000", dec_epoch(2026, 10, 30, 2, 16, 58), C2810_CLOSE),
    ("foreign 92b5acc 02:17:19Z = 1793326639.000", dec_epoch(2026, 10, 30, 2, 17, 19), FOREIGN_NOW),
    ("token 1017 = 02:17:00Z = 1793326620.000", dec_epoch(2026, 10, 30, 2, 17, 0), TOKEN),
    ("c2810 token 1002 = 02:02:00Z = 1793325720.000", dec_epoch(2026, 10, 30, 2, 2, 0), C2810_TOKEN),
    ("capture pre-echo EPOCH 1793327225.013423065 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 27, 5, 13423065), PRE),
    ("pre-echo ISO 02:27:05.012844056 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 2, 27, 5, 12844056), D("1793327225.012844056")),
    ("post-echo ISO 02:27:06.817944086 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 2, 27, 6, 817944086), D("1793327226.817944086")),
    ("post-echo EPOCH 1793327226.818599805 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 27, 6, 818599805), POST),
    ("scanned_at 02:27:06.813 +0000 (decimal)", dec_epoch(2026, 10, 30, 2, 27, 6) + D("0.813"), SCAN),
    ("window-2811 open 02:16:06.804677305 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 2, 16, 6, 804677305), WIN),
    ("window-2812 open = post-echo + 300.000", POST + D("300.000"), D("1793327526.818599805")),
    ("c2810 post-echo EPOCH 1793326266.804677305 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 11, 6, 804677305), C2810_POST),
    ("c2810 scanned_at 02:11:06.798 +0000 (decimal)", dec_epoch(2026, 10, 30, 2, 11, 6) + D("0.798"), C2810_SCAN),
    ("c2810 capture pre-echo EPOCH 1793326265.037661240 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 11, 5, 37661240), C2810_PRE),
    ("c2810 echo post-echo EPOCH 1793326093.975704459 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 8, 13, 975704459), C2810_ECHO_POST),
    ("echo pre-echo EPOCH 1793326689.371235484 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 18, 9, 371235484), ECHO_PRE),
    ("echo post-echo EPOCH 1793326691.169645781 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 18, 11, 169645781), ECHO_POST),
    ("echo scanned_at 02:18:11.166 +0000 (decimal)", dec_epoch(2026, 10, 30, 2, 18, 11) + D("0.166"), ECHO_SCAN),
    ("window-2810 open 02:01:27.842975825 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 2, 1, 27, 842975825), WIN2810),
]
exact_checks = [
    ("skew decimal-exact +5.599805ms (EPOCH-governs decomposition; SUB-10 extends m8)", POST - SCAN, D("0.005599805")),
    ("CAPTURE_vs_window +660.013922500 (POST-WINDOW; the capture-side print)", POST - WIN, D("660.013922500")),
    ("capture post-c2810-post-echo +960.013922500", POST - C2810_POST, D("960.013922500")),
    ("dd#385 = +660.015000000 (interval 960.015 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#383 print 571.871 - 300 = 271.871 and the dd#384 print 878.961 - 300 = 578.961)", SCAN - C2810_SCAN - D("300.000"), D("660.015")),
    ("dd formula re-verification: 878.961 - 300 = 578.961", D("878.961") - D("300.000"), D("578.961")),
    ("dd formula re-verification: 571.871 - 300 = 271.871", D("571.871") - D("300.000"), D("271.871")),
    ("dd formula re-verification: 823.162 - 300 = 523.162", D("823.162") - D("300.000"), D("523.162")),
    ("INTERVAL#385 = 950.813", SCAN - TRIG, D("950.813")),
    ("LAG#385 = INTERVAL + dd - dd#384 = +1031.867", (SCAN - TRIG) + (SCAN - C2810_SCAN - D("300.000")) - D("578.961"), D("1031.867")),
    ("LATE#385 = trigger - window-open = -290.804677305", TRIG - WIN, D("-290.804677305")),
    ("window-2811 = c2810 capture post-echo + 300.000 (the server contract)", WIN - C2810_POST, D("300.000")),
    ("trigger POSTDATES the c2810 capture post-echo by 9.195322695s (the POST-capture placement NEW)", TRIG - C2810_POST, D("9.195322695")),
    ("trigger POSTDATES the c2810 capture pre-echo by 10.962338760s", TRIG - C2810_PRE, D("10.962338760")),
    ("trigger POSTDATES the c2810 scanned_at by 9.202s", TRIG - C2810_SCAN, D("9.202")),
    ("trigger POSTDATES the c2810 echo post-echo by 182.024295541s", TRIG - C2810_ECHO_POST, D("182.024295541")),
    ("c2810 close POSTDATES the trigger by 342.000s (d228cc8 at 02:16:58)", C2810_CLOSE - TRIG, D("342.000")),
    ("foreign 92b5acc POSTDATES the trigger by 363.000s (02:17:19)", FOREIGN_NOW - TRIG, D("363.000")),
    ("c2810 close landed 2.000s BEFORE the token-1017 second (02:16:58 vs 02:17:00 — the AFTER-class TERMINATES, a NEW before-class opens m1)", C2810_CLOSE - TOKEN, D("-2.000")),
    ("foreign 92b5acc landed 19.000s AFTER the token second (02:17:19 — the after-class REPEATS)", FOREIGN_NOW - TOKEN, D("19.000")),
    ("c2810 close landed 51.195322695s AFTER window-2811 open", C2810_CLOSE - WIN, D("51.195322695")),
    ("foreign 92b5acc landed 72.195322695s AFTER window-2811 open", FOREIGN_NOW - WIN, D("72.195322695")),
    ("echo POST-WINDOW +124.364968476 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("124.364968476")),
    ("stamp-to-echo 413.371235484 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS)", ECHO_PRE - TRIG, D("413.371235484")),
    ("echo wall latency 1.798410297 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.790832 / server 1783ms latency-match)", ECHO_POST - ECHO_PRE, D("1.798410297")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m9)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2811"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2811"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2812 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2813_birth",
      block.count("c2813") == 4 and lines[-1].count("c2813") == 2
      and "c2812/c2813" in lines[-1] and "FORWARD token c2813" in lines[-1]
      and "the c2813 pre==0 expectation" in block and "c2813_pre = 0" in block,
      f"block c2813={block.count('c2813')} next-line c2813={lines[-1].count('c2813')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2813_pre = 0' + the Next bullet's guard phrase 'c2812/c2813' AND "
      f"census-tuple sentence 'FORWARD token c2813')")
guard("block_c2812_step7_precount_sentence",
      "the c2812 pre-count is 4" in block
      and "per-line {9458: 2, 9460: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2812 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9460", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2811_next_bullet", last_nonempty.startswith("- Next: the c2811 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2811",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2811")]) == 0,
      f"c2811 substring mentions={wl.count('c2811')} (expect 14)")
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(wl.splitlines()) if "c2811" in l}
guard("c2811_mention_census_pre", wl.count("c2811") == 14
      and c2811_lines == {9446: 2, 9448: 2, 9452: 5, 9458: 1, 9460: 4},
      f"per-line={c2811_lines}")
c2812_lines = {i + 1: l.count("c2812") for i, l in enumerate(wl.splitlines()) if "c2812" in l}
guard("c2812_forward_token_pre", wl.count("c2812") == 4 and c2812_lines == {9458: 2, 9460: 2},
      f"per-line={c2812_lines} (2 births in the c2810 Step-7 twin-print line 9458 + "
      f"2 FORWARD-token births inside the c2810 Next-block — the born-FOUR class "
      f"REPEATS an EIGHTH time)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==488", tid_pre == 488, f"got={tid_pre}")
guard("anchor_nogold_pre==421", gold_pre == 421, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2813_pre = wl.count("c2813")
c2812_pre = wl.count("c2812")
c2811_pre = wl.count("c2811")
c2810_pre = wl.count("c2810")
c2809_pre = wl.count("c2809")
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
guard("c2813_pre==0", c2813_pre == 0, f"got={c2813_pre} (the forward token c2813 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2812_pre==4", c2812_pre == 4, f"got={c2812_pre} (born FOUR: the c2810 Step-7 twin-print "
      f"line 9458 TWICE + TWICE inside the c2810 Next-block — NOT the unborn class)")
guard("c2811_pre==14", c2811_pre == 14, f"got={c2811_pre}")
guard("c2810_pre==36", c2810_pre == 36, f"got={c2810_pre}")
guard("c2809_pre==75", c2809_pre == 75, f"got={c2809_pre}")
guard("c2808_pre==87", c2808_pre == 87, f"got={c2808_pre}")
guard("c2807_pre==78", c2807_pre == 78, f"got={c2807_pre}")
guard("c2806_pre==81", c2806_pre == 81, f"got={c2806_pre}")
guard("c2805_pre==88", c2805_pre == 88, f"got={c2805_pre}")
guard("c2804_pre==103", c2804_pre == 103, f"got={c2804_pre}")
guard("c2803_pre==114", c2803_pre == 114, f"got={c2803_pre}")
guard("c2802_pre==118", c2802_pre == 118, f"got={c2802_pre}")
guard("c2801_pre==94", c2801_pre == 94, f"got={c2801_pre}")
guard("c2800_pre==130", c2800_pre == 130, f"got={c2800_pre}")
guard("c2799_pre==99", c2799_pre == 99, f"got={c2799_pre}")
guard("c2798_pre==97", c2798_pre == 97, f"got={c2798_pre}")
guard("c2797_pre==89", c2797_pre == 89, f"got={c2797_pre}")
guard("c2796_pre==99", c2796_pre == 99, f"got={c2796_pre}")
guard("c2795_pre==122", c2795_pre == 122, f"got={c2795_pre}")
guard("c2794_pre==116", c2794_pre == 116, f"got={c2794_pre}")
guard("c2793_pre==124", c2793_pre == 124, f"got={c2793_pre}")
guard("c2792_pre==129", c2792_pre == 129, f"got={c2792_pre}")
guard("c2791_pre==117", c2791_pre == 117, f"got={c2791_pre}")
guard("c2790_pre==130", c2790_pre == 130, f"got={c2790_pre}")
guard("c2789_pre==120", c2789_pre == 120, f"got={c2789_pre}")
guard("c2788_pre==131", c2788_pre == 131, f"got={c2788_pre}")
guard("c2787_pre==132", c2787_pre == 132, f"got={c2787_pre}")
guard("c2786_pre==154", c2786_pre == 154, f"got={c2786_pre}")
guard("c2785_pre==136", c2785_pre == 136, f"got={c2785_pre}")
guard("c2784_pre==134", c2784_pre == 134, f"got={c2784_pre}")
guard("c2783_pre==135", c2783_pre == 135, f"got={c2783_pre}")
guard("c2782_pre==134", c2782_pre == 134, f"got={c2782_pre}")
guard("c2781_pre==139", c2781_pre == 139, f"got={c2781_pre}")
guard("c2780_pre==144", c2780_pre == 144, f"got={c2780_pre}")
guard("c2779_pre==144", c2779_pre == 144, f"got={c2779_pre}")
guard("c2778_pre==188", c2778_pre == 188, f"got={c2778_pre}")
guard("c2777_pre==160", c2777_pre == 160, f"got={c2777_pre}")
guard("c2776_pre==165", c2776_pre == 165, f"got={c2776_pre}")
guard("c2775_pre==174", c2775_pre == 174, f"got={c2775_pre}")
guard("c2774_pre==179", c2774_pre == 179, f"got={c2774_pre}")
guard("c2773_pre==183", c2773_pre == 183, f"got={c2773_pre}")
guard("c2772_pre==202", c2772_pre == 202, f"got={c2772_pre}")
guard("c2771_pre==192", c2771_pre == 192, f"got={c2771_pre}")
guard("c2770_pre==244", c2770_pre == 244, f"got={c2770_pre}")
guard("c2769_pre==181", c2769_pre == 181, f"got={c2769_pre}")
guard("c2768_pre==184", c2768_pre == 184, f"got={c2768_pre}")
guard("c2767_pre==253", c2767_pre == 253, f"got={c2767_pre}")
guard("c2766_pre==221", c2766_pre == 221, f"got={c2766_pre}")
guard("c2765_pre==175", c2765_pre == 175, f"got={c2765_pre}")
guard("c2764_pre==177", c2764_pre == 177, f"got={c2764_pre}")
guard("c2763_pre==185", c2763_pre == 185, f"got={c2763_pre}")
guard("c2762_pre==222", c2762_pre == 222, f"got={c2762_pre}")
guard("c2761_pre==242", c2761_pre == 242, f"got={c2761_pre}")
guard("c2760_pre==180", c2760_pre == 180, f"got={c2760_pre}")
guard("c2759_pre==180", c2759_pre == 180, f"got={c2759_pre}")
guard("c2758_pre==182", c2758_pre == 182, f"got={c2758_pre}")
guard("c2757_pre==185", c2757_pre == 185, f"got={c2757_pre}")
guard("c2756_pre==190", c2756_pre == 190, f"got={c2756_pre}")
guard("c2755_pre==197", c2755_pre == 197, f"got={c2755_pre}")
guard("c2754_pre==200", c2754_pre == 200, f"got={c2754_pre}")
guard("c2753_pre==217", c2753_pre == 217, f"got={c2753_pre}")
guard("c2752_pre==223", c2752_pre == 223, f"got={c2752_pre}")
guard("c2751_pre==209", c2751_pre == 209, f"got={c2751_pre}")
guard("c2750_pre==213", c2750_pre == 213, f"got={c2750_pre}")
guard("c2749_pre==216", c2749_pre == 216, f"got={c2749_pre}")

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
guard("post_worklog_lines==9472", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2812_next_bullet", last2.startswith("- Next: the c2812 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==489", tid_post == 489, f"got={tid_post}")
guard("anchor_nogold_post==422", gold_post == 422, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2811_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2811")]) == 1)
expect_c2813_mentions = wl2.count("c2813")
guard("c2813_mention_birth", expect_c2813_mentions == c2813_pre + block.count("c2813"),
      f"pre={c2813_pre} (unborn) + block births={block.count('c2813')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2813_pre + block.count('c2813')} got={expect_c2813_mentions}")
for tag, pre in (("c2812", c2812_pre), ("c2811", c2811_pre), ("c2810", c2810_pre),
                 ("c2809", c2809_pre), ("c2808", c2808_pre), ("c2807", c2807_pre),
                 ("c2806", c2806_pre), ("c2805", c2805_pre), ("c2804", c2804_pre),
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
                 ("c2749", c2749_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9460 -> 9472 (+12), c2811 entry + DRIFT-#49 pass-60 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
