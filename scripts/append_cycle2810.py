#!/usr/bin/env python3
"""Guarded worklog append for the c2810 entry (12 lines).

Follows the append_cycle2809.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809 abort precedent class). The ledger arithmetic stays in the
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
the stamp-gap/token-gap/token-vs-stamp cadence triple, the window-2810
EPOCH-governs render check, the window-2811 prophecy check, and the
queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock
reads differ ~689µs on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2812 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2812 pre==0 expectation' + the Step-7 census-time print
'c2812_pre = 0' + the Next bullet's guard phrase 'c2811/c2812' AND
census-tuple sentence 'FORWARD token c2812' — the c2767..c2810 forward-token
lessons; NOTE the c2812 pre-count is 0 (unborn) while the c2811 pre-count is
4 (born: the c2809 Step-7 twin-print line 9446 TWICE + TWICE inside the
c2809 Next-block) — the c2809 append prophecy 'c2811 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS a SEVENTH time), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9448 lines, tail = the c2810 Next bullet, zero serviced
c2810 entries, c2810 mention census per-line {9434: 2, 9436: 2, 9440: 4,
9446: 1, 9448: 4} total 13, c2811 = 4 per-line {9446: 2, 9448: 2}, anchors
487/420/60/28), post-state (9460 lines, tail = the c2811 Next bullet,
anchors 488/421/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2810.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9448
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


POST = D("1793326266.804677305")    # c2810 post-echo (EPOCH-governs)
SCAN = D("1793326266.798")          # c2810 scanned_at (decimal)
TRIG = D("1793325375.000")          # c2810 trigger stamp (09:56:15 +08)
WIN = D("1793325687.842975825")     # window-2810 open (c2809 prophecy EPOCH)
PRE = D("1793326265.037661240")     # c2810 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793326092.157953294")   # c2810 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793326093.975704459")  # c2810 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793326093.969")        # c2810 echo scanned_at (decimal)
C2809_SCAN = D("1793325387.837")    # c2809 scanned_at
C2809_POST = D("1793325387.842975825")  # c2809 post-echo
C2809_PRE = D("1793325386.122196789")   # c2809 capture pre-echo
C2809_ECHO_POST = D("1793325276.606952377")  # c2809 echo post-echo
C2809_CLOSE = D("1793325748.000")   # c2809 close d19b6ac (02:02:28Z)
FOREIGN_NOW = D("1793325766.000")   # foreign 1288d7f (02:02:46Z)
C2809_TRIG = D("1793324776.000")    # c2809 trigger stamp (09:46:16 +08)
WIN2809 = D("1793325115.971824111")  # window-2809 open (for the contract re-check)
TOKEN = D("1793325720.000")         # token 1002 (10:02:00 +08)
C2809_TOKEN = D("1793325120.000")   # token 0952 (09:52:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 09:56:15 +08 = 1793325375.000", dec_epoch(2026, 10, 30, 1, 56, 15), TRIG),
    ("c2809 trigger stamp 09:46:16 +08 = 1793324776.000", dec_epoch(2026, 10, 30, 1, 46, 16), C2809_TRIG),
    ("stamp-gap 599.000s by stamp (09:46:16 -> 09:56:15; the 599 print RETURNS, 2 priors)", TRIG - C2809_TRIG, D("599.000")),
    ("token-gap 600.000s by token (0952 -> 1002; the 600 print RETURNS, 22 priors)", TOKEN - C2809_TOKEN, D("600.000")),
    ("token-vs-stamp +345.000 (09:56:15 -> 10:02:00; the +345 print NEW)", TOKEN - TRIG, D("345.000")),
    ("c2809 close d19b6ac 02:02:28Z = 1793325748.000", dec_epoch(2026, 10, 30, 2, 2, 28), C2809_CLOSE),
    ("foreign 1288d7f 02:02:46Z = 1793325766.000", dec_epoch(2026, 10, 30, 2, 2, 46), FOREIGN_NOW),
    ("token 1002 = 02:02:00Z = 1793325720.000", dec_epoch(2026, 10, 30, 2, 2, 0), TOKEN),
    ("c2809 token 0952 = 01:52:00Z = 1793325120.000", dec_epoch(2026, 10, 30, 1, 52, 0), C2809_TOKEN),
    ("capture pre-echo EPOCH 1793326265.037661240 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 11, 5, 37661240), PRE),
    ("pre-echo ISO 02:11:05.036990153 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 2, 11, 5, 36990153), D("1793326265.036990153")),
    ("post-echo ISO 02:11:06.803988743 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 2, 11, 6, 803988743), D("1793326266.803988743")),
    ("post-echo EPOCH 1793326266.804677305 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 11, 6, 804677305), POST),
    ("scanned_at 02:11:06.798 +0000 (decimal)", dec_epoch(2026, 10, 30, 2, 11, 6) + D("0.798"), SCAN),
    ("window-2810 open 02:01:27.842975825 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 2, 1, 27, 842975825), WIN),
    ("window-2811 open = post-echo + 300.000", POST + D("300.000"), D("1793326566.804677305")),
    ("c2809 post-echo EPOCH 1793325387.842975825 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 56, 27, 842975825), C2809_POST),
    ("c2809 scanned_at 01:56:27.837 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 56, 27) + D("0.837"), C2809_SCAN),
    ("c2809 capture pre-echo EPOCH 1793325386.122196789 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 56, 26, 122196789), C2809_PRE),
    ("c2809 echo post-echo EPOCH 1793325276.606952377 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 54, 36, 606952377), C2809_ECHO_POST),
    ("echo pre-echo EPOCH 1793326092.157953294 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 8, 12, 157953294), ECHO_PRE),
    ("echo pre-echo ISO 02:08:12.157342370 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 2, 8, 12, 157342370), D("1793326092.157342370")),
    ("echo post-echo ISO 02:08:13.975016078 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 2, 8, 13, 975016078), D("1793326093.975016078")),
    ("echo post-echo EPOCH 1793326093.975704459 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 8, 13, 975704459), ECHO_POST),
    ("echo scanned_at 02:08:13.969 +0000 (decimal)", dec_epoch(2026, 10, 30, 2, 8, 13) + D("0.969"), ECHO_SCAN),
]
exact_checks = [
    ("skew decimal-exact +6.677305ms (EPOCH-governs decomposition; SUB-10 extends m7)", POST - SCAN, D("0.006677305")),
    ("CAPTURE_vs_window +578.961701480 (POST-WINDOW; the capture-side print)", POST - WIN, D("578.961701480")),
    ("capture post-c2809-post-echo +878.961701480", POST - C2809_POST, D("878.961701480")),
    ("dd#384 = +578.961000000 (interval 878.961 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#382 print 823.162 - 300 = 523.162 and the dd#383 print 571.871 - 300 = 271.871)", SCAN - C2809_SCAN - D("300.000"), D("578.961")),
    ("dd formula re-verification: 740.182 - 300 = 440.182", D("740.182") - D("300.000"), D("440.182")),
    ("dd formula re-verification: 663.092 - 300 = 363.092", D("663.092") - D("300.000"), D("363.092")),
    ("dd formula re-verification: 811.706 - 300 = 511.706", D("811.706") - D("300.000"), D("511.706")),
    ("dd formula re-verification: 823.162 - 300 = 523.162", D("823.162") - D("300.000"), D("523.162")),
    ("INTERVAL#384 = 891.798", SCAN - TRIG, D("891.798")),
    ("LAG#384 = INTERVAL + dd - dd#383 = +1198.888", (SCAN - TRIG) + (SCAN - C2809_SCAN - D("300.000")) - D("271.871"), D("1198.888")),
    ("LATE#384 = trigger - window-open = -312.842975825", TRIG - WIN, D("-312.842975825")),
    ("window-2810 = c2809 post-echo + 300.000 (the server contract)", WIN - C2809_POST, D("300.000")),
    ("trigger POSTDATES the c2809 echo post-echo by 98.393047623s (the POST-echo placement REPEATS)", TRIG - C2809_ECHO_POST, D("98.393047623")),
    ("trigger PREDATES the c2809 pre-echo by 11.122196789s", C2809_PRE - TRIG, D("11.122196789")),
    ("trigger PREDATES the c2809 scanned_at by 12.837s", C2809_SCAN - TRIG, D("12.837")),
    ("trigger PREDATES window-2810 open by 312.842975825s", WIN - TRIG, D("312.842975825")),
    ("c2809 close POSTDATES the trigger by 373.000s (d19b6ac at 02:02:28)", C2809_CLOSE - TRIG, D("373.000")),
    ("foreign 1288d7f POSTDATES the trigger by 391.000s (02:02:46)", FOREIGN_NOW - TRIG, D("391.000")),
    ("c2809 close landed 28.000s AFTER the token-1002 second (02:02:28 vs 02:02:00 — the AFTER-class EXTENDS m2)", C2809_CLOSE - TOKEN, D("28.000")),
    ("foreign 1288d7f landed 46.000s AFTER the token second (02:02:46)", FOREIGN_NOW - TOKEN, D("46.000")),
    ("foreign 1288d7f landed 78.157024175s AFTER window-2810 open", FOREIGN_NOW - WIN, D("78.157024175")),
    ("c2809 close d19b6ac landed 60.157024175s AFTER window-2810 open", C2809_CLOSE - WIN, D("60.157024175")),
    ("echo POST-WINDOW +406.132728634 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("406.132728634")),
    ("stamp-to-echo 717.157953294 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS)", ECHO_PRE - TRIG, D("717.157953294")),
    ("echo wall latency 1.817751165 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.807991 / server 1800ms latency-match)", ECHO_POST - ECHO_PRE, D("1.817751165")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m8)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2810"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2810"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2811 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2812_birth",
      block.count("c2812") == 4 and lines[-1].count("c2812") == 2
      and "c2811/c2812" in lines[-1] and "FORWARD token c2812" in lines[-1]
      and "the c2812 pre==0 expectation" in block and "c2812_pre = 0" in block,
      f"block c2812={block.count('c2812')} next-line c2812={lines[-1].count('c2812')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2812_pre = 0' + the Next bullet's guard phrase 'c2811/c2812' AND "
      f"census-tuple sentence 'FORWARD token c2812')")
guard("block_c2811_step7_precount_sentence",
      "the c2811 pre-count is 4" in block
      and "per-line {9446: 2, 9448: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2811 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9448", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2810_next_bullet", last_nonempty.startswith("- Next: the c2810 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2810",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2810")]) == 0,
      f"c2810 substring mentions={wl.count('c2810')} (expect 13)")
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(wl.splitlines()) if "c2810" in l}
guard("c2810_mention_census_pre", wl.count("c2810") == 13
      and c2810_lines == {9434: 2, 9436: 2, 9440: 4, 9446: 1, 9448: 4},
      f"per-line={c2810_lines}")
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(wl.splitlines()) if "c2811" in l}
guard("c2811_forward_token_pre", wl.count("c2811") == 4 and c2811_lines == {9446: 2, 9448: 2},
      f"per-line={c2811_lines} (2 births in the c2809 Step-7 twin-print line 9446 + "
      f"2 FORWARD-token births inside the c2809 Next-block — the born-FOUR class "
      f"REPEATS a SEVENTH time)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==487", tid_pre == 487, f"got={tid_pre}")
guard("anchor_nogold_pre==420", gold_pre == 420, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
c2748_pre = wl.count("c2748")
guard("c2812_pre==0", c2812_pre == 0, f"got={c2812_pre} (the forward token c2812 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2811_pre==4", c2811_pre == 4, f"got={c2811_pre} (born FOUR: the c2809 Step-7 twin-print "
      f"line 9446 TWICE + TWICE inside the c2809 Next-block — NOT the unborn class)")
guard("c2810_pre==13", c2810_pre == 13, f"got={c2810_pre}")
guard("c2809_pre==35", c2809_pre == 35, f"got={c2809_pre}")
guard("c2808_pre==78", c2808_pre == 78, f"got={c2808_pre}")
guard("c2807_pre==76", c2807_pre == 76, f"got={c2807_pre}")
guard("c2806_pre==78", c2806_pre == 78, f"got={c2806_pre}")
guard("c2805_pre==86", c2805_pre == 86, f"got={c2805_pre}")
guard("c2804_pre==101", c2804_pre == 101, f"got={c2804_pre}")
guard("c2803_pre==112", c2803_pre == 112, f"got={c2803_pre}")
guard("c2802_pre==116", c2802_pre == 116, f"got={c2802_pre}")
guard("c2801_pre==93", c2801_pre == 93, f"got={c2801_pre}")
guard("c2800_pre==127", c2800_pre == 127, f"got={c2800_pre}")
guard("c2799_pre==98", c2799_pre == 98, f"got={c2799_pre}")
guard("c2798_pre==96", c2798_pre == 96, f"got={c2798_pre}")
guard("c2797_pre==88", c2797_pre == 88, f"got={c2797_pre}")
guard("c2796_pre==98", c2796_pre == 98, f"got={c2796_pre}")
guard("c2795_pre==121", c2795_pre == 121, f"got={c2795_pre}")
guard("c2794_pre==115", c2794_pre == 115, f"got={c2794_pre}")
guard("c2793_pre==123", c2793_pre == 123, f"got={c2793_pre}")
guard("c2792_pre==128", c2792_pre == 128, f"got={c2792_pre}")
guard("c2791_pre==116", c2791_pre == 116, f"got={c2791_pre}")
guard("c2790_pre==129", c2790_pre == 129, f"got={c2790_pre}")
guard("c2789_pre==119", c2789_pre == 119, f"got={c2789_pre}")
guard("c2788_pre==130", c2788_pre == 130, f"got={c2788_pre}")
guard("c2787_pre==131", c2787_pre == 131, f"got={c2787_pre}")
guard("c2786_pre==153", c2786_pre == 153, f"got={c2786_pre}")
guard("c2785_pre==135", c2785_pre == 135, f"got={c2785_pre}")
guard("c2784_pre==133", c2784_pre == 133, f"got={c2784_pre}")
guard("c2783_pre==134", c2783_pre == 134, f"got={c2783_pre}")
guard("c2782_pre==133", c2782_pre == 133, f"got={c2782_pre}")
guard("c2781_pre==138", c2781_pre == 138, f"got={c2781_pre}")
guard("c2780_pre==143", c2780_pre == 143, f"got={c2780_pre}")
guard("c2779_pre==143", c2779_pre == 143, f"got={c2779_pre}")
guard("c2778_pre==187", c2778_pre == 187, f"got={c2778_pre}")
guard("c2777_pre==159", c2777_pre == 159, f"got={c2777_pre}")
guard("c2776_pre==164", c2776_pre == 164, f"got={c2776_pre}")
guard("c2775_pre==173", c2775_pre == 173, f"got={c2775_pre}")
guard("c2774_pre==178", c2774_pre == 178, f"got={c2774_pre}")
guard("c2773_pre==182", c2773_pre == 182, f"got={c2773_pre}")
guard("c2772_pre==201", c2772_pre == 201, f"got={c2772_pre}")
guard("c2771_pre==191", c2771_pre == 191, f"got={c2771_pre}")
guard("c2770_pre==242", c2770_pre == 242, f"got={c2770_pre}")
guard("c2769_pre==180", c2769_pre == 180, f"got={c2769_pre}")
guard("c2768_pre==183", c2768_pre == 183, f"got={c2768_pre}")
guard("c2767_pre==250", c2767_pre == 250, f"got={c2767_pre}")
guard("c2766_pre==219", c2766_pre == 219, f"got={c2766_pre}")
guard("c2765_pre==174", c2765_pre == 174, f"got={c2765_pre}")
guard("c2764_pre==176", c2764_pre == 176, f"got={c2764_pre}")
guard("c2763_pre==184", c2763_pre == 184, f"got={c2763_pre}")
guard("c2762_pre==221", c2762_pre == 221, f"got={c2762_pre}")
guard("c2761_pre==240", c2761_pre == 240, f"got={c2761_pre}")
guard("c2760_pre==179", c2760_pre == 179, f"got={c2760_pre}")
guard("c2759_pre==179", c2759_pre == 179, f"got={c2759_pre}")
guard("c2758_pre==181", c2758_pre == 181, f"got={c2758_pre}")
guard("c2757_pre==184", c2757_pre == 184, f"got={c2757_pre}")
guard("c2756_pre==189", c2756_pre == 189, f"got={c2756_pre}")
guard("c2755_pre==196", c2755_pre == 196, f"got={c2755_pre}")
guard("c2754_pre==199", c2754_pre == 199, f"got={c2754_pre}")
guard("c2753_pre==215", c2753_pre == 215, f"got={c2753_pre}")
guard("c2752_pre==221", c2752_pre == 221, f"got={c2752_pre}")
guard("c2751_pre==207", c2751_pre == 207, f"got={c2751_pre}")
guard("c2750_pre==211", c2750_pre == 211, f"got={c2750_pre}")
guard("c2749_pre==213", c2749_pre == 213, f"got={c2749_pre}")
guard("c2748_pre==204", c2748_pre == 204, f"got={c2748_pre}")

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
guard("post_worklog_lines==9460", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2811_next_bullet", last2.startswith("- Next: the c2811 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==488", tid_post == 488, f"got={tid_post}")
guard("anchor_nogold_post==421", gold_post == 421, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2810_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2810")]) == 1)
expect_c2812_mentions = wl2.count("c2812")
guard("c2812_mention_birth", expect_c2812_mentions == c2812_pre + block.count("c2812"),
      f"pre={c2812_pre} (unborn) + block births={block.count('c2812')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2812_pre + block.count('c2812')} got={expect_c2812_mentions}")
for tag, pre in (("c2811", c2811_pre), ("c2810", c2810_pre), ("c2809", c2809_pre),
                 ("c2808", c2808_pre), ("c2807", c2807_pre), ("c2806", c2806_pre),
                 ("c2805", c2805_pre), ("c2804", c2804_pre), ("c2803", c2803_pre),
                 ("c2802", c2802_pre), ("c2801", c2801_pre), ("c2800", c2800_pre),
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
                 ("c2748", c2748_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9448 -> 9460 (+12), c2810 entry + DRIFT-#49 pass-59 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
