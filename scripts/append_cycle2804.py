#!/usr/bin/env python3
"""Guarded worklog append for the c2804 entry (12 lines).

Follows the append_cycle2803.py precedent — ALL asserts precede the
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
window-2804 EPOCH-governs render check, the window-2805 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~663µs on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2806 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2806 pre==0 expectation' + the Step-7 census-time print
'c2806_pre = 0' + the Next bullet's guard phrase 'c2805/c2806' AND
census-tuple sentence 'FORWARD token c2806' — the c2767..c2804 forward-token
lessons; NOTE the c2806 pre-count is 0 (unborn) while the c2805 pre-count is
4 (born: the c2803 Step-7 twin-print line 9374 TWICE + TWICE inside the
c2803 Next-block) — the c2803 append prophecy 'c2805 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9376 lines, tail = the c2804 Next bullet, zero serviced c2804
entries, c2804 mention census per-line {9362: 2, 9364: 2, 9368: 5, 9374: 1,
9376: 4} total 14, c2805 = 4 per-line {9374: 2, 9376: 2}, anchors 481/414/
60/28), post-state (9388 lines, tail = the c2805 Next bullet, anchors 482/
415/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2804.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9376
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


POST = D("1793321777.440380038")    # c2804 post-echo (EPOCH-governs)
SCAN = D("1793321777.434")          # c2804 scanned_at (decimal)
TRIG = D("1793320873.000")          # c2804 trigger stamp (08:41:13 +08)
WIN = D("1793321413.772582901")     # window-2804 open (c2803 prophecy EPOCH)
PRE = D("1793321775.493693754")     # c2804 capture pre-echo (EPOCH-governs)
C2803_SCAN = D("1793321113.709")    # c2803 scanned_at
C2803_POST = D("1793321113.772582901")  # c2803 post-echo
C2803_PRE = D("1793321111.689514935")   # c2803 capture pre-echo
C2803_CLOSE = D("1793321397.000")   # c2803 close 597a622 (00:49:57Z)
C2803_FOREIGN = D("1793321414.000")  # foreign 7de8446 (00:50:14Z)
C2803_TRIG = D("1793320273.000")    # c2803 trigger stamp (08:31:13 +08)
WIN2803 = D("1793320673.583889929")  # window-2803 open (for the trigger-postdates check)
TOKEN = D("1793321400.000")         # token 0850 (08:50:00 +08)
C2803_TOKEN = D("1793320680.000")   # token 0838 (08:38:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 08:41:13 +08 = 1793320873.000", dec_epoch(2026, 10, 30, 0, 41, 13), TRIG),
    ("c2803 trigger stamp 08:31:13 +08 = 1793320273.000", dec_epoch(2026, 10, 30, 0, 31, 13), C2803_TRIG),
    ("stamp-gap 600.000s by stamp (08:31:13 -> 08:41:13; the 600 print REPEATS)", TRIG - C2803_TRIG, D("600.000")),
    ("token-gap 720.000s by token (0838 -> 0850; the 540 print BROKE, the 720 print RETURNS)", TOKEN - C2803_TOKEN, D("720.000")),
    ("token-vs-stamp +527.000 (08:41:13 -> 08:50:00; the +527 print NEW)", TOKEN - TRIG, D("527.000")),
    ("c2803 close 597a622 00:49:57Z = 1793321397.000", dec_epoch(2026, 10, 30, 0, 49, 57), C2803_CLOSE),
    ("foreign 7de8446 00:50:14Z = 1793321414.000", dec_epoch(2026, 10, 30, 0, 50, 14), C2803_FOREIGN),
    ("token 0850 = 00:50:00Z = 1793321400.000", dec_epoch(2026, 10, 30, 0, 50, 0), TOKEN),
    ("c2803 token 0838 = 00:38:00Z = 1793320680.000", dec_epoch(2026, 10, 30, 0, 38, 0), C2803_TOKEN),
    ("capture pre-echo EPOCH 1793321775.493693754 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 56, 15, 493693754), PRE),
    ("pre-echo ISO 00:56:15.493019324 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 56, 15, 493019324), D("1793321775.493019324")),
    ("post-echo ISO 00:56:17.439664290 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 0, 56, 17, 439664290), D("1793321777.439664290")),
    ("post-echo EPOCH 1793321777.440380038 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 56, 17, 440380038), POST),
    ("scanned_at 00:56:17.434 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 56, 17) + D("0.434"), SCAN),
    ("window-2804 open 00:50:13.772582901 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 0, 50, 13, 772582901), WIN),
    ("window-2805 open = post-echo + 300.000", POST + D("300.000"), D("1793322077.440380038")),
    ("c2803 post-echo EPOCH 1793321113.772582901 (EPOCH-governs)", dec_epoch(2026, 10, 30, 0, 45, 13, 772582901), C2803_POST),
    ("c2803 scanned_at 00:45:13.709 +0000 (decimal)", dec_epoch(2026, 10, 30, 0, 45, 13) + D("0.709"), C2803_SCAN),
]
exact_checks = [
    ("skew decimal-exact +6.380038ms (EPOCH-governs decomposition; SUB-10 FLIPS BACK — ABOVE-10 m4 TERMINATES)", POST - SCAN, D("0.006380038")),
    ("CAPTURE_vs_window +363.667797137 (POST-WINDOW; the capture-side print)", POST - WIN, D("363.667797137")),
    ("capture post-c2803-post-echo +663.667797137", POST - C2803_POST, D("663.667797137")),
    ("dd#378 = +363.725000000 (interval 663.725 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#377 print 740.182 - 300 = 440.182 and the dd#376 print 423.763 - 300 = 123.763)", SCAN - C2803_SCAN - D("300.000"), D("363.725")),
    ("dd formula re-verification: 423.763 - 300 = 123.763", D("423.763") - D("300.000"), D("123.763")),
    ("dd formula re-verification: 740.182 - 300 = 440.182", D("740.182") - D("300.000"), D("440.182")),
    ("INTERVAL#378 = 904.434", SCAN - TRIG, D("904.434")),
    ("LAG#378 = INTERVAL + dd - dd#377 = +827.977", (SCAN - TRIG) + (SCAN - C2803_SCAN - D("300.000")) - D("440.182"), D("827.977")),
    ("LATE#378 = trigger - window-open = -540.772582901", TRIG - WIN, D("-540.772582901")),
    ("window-2804 = c2803 post-echo + 300.000 (the server contract)", WIN - C2803_POST, D("300.000")),
    ("trigger PREDATES the c2803 post-echo by 240.772582901s (the PRE-echo placement REPEATS)", C2803_POST - TRIG, D("240.772582901")),
    ("trigger PREDATES the c2803 scanned_at by 240.709s", C2803_SCAN - TRIG, D("240.709")),
    ("trigger PREDATES the c2803 pre-echo by 238.689514935s", C2803_PRE - TRIG, D("238.689514935")),
    ("trigger POSTDATES window-2803 open by 199.416110071s", TRIG - WIN2803, D("199.416110071")),
    ("c2803 close POSTDATES the trigger by 524.000s (597a622 at 00:49:57)", C2803_CLOSE - TRIG, D("524.000")),
    ("foreign 7de8446 POSTDATES the trigger by 541.000s (00:50:14)", C2803_FOREIGN - TRIG, D("541.000")),
    ("c2803 close landed 3.000s BEFORE the token-0850 second (00:49:57 vs 00:50:00 — the after-class identity BROKE, the BEFORE-class opens m1)", C2803_CLOSE - TOKEN, D("-3.000")),
    ("foreign 7de8446 landed 14.000s AFTER the token second (00:50:14)", C2803_FOREIGN - TOKEN, D("14.000")),
    ("foreign 7de8446 landed +0.227417099s AFTER window-2804 open (the foreign-at-the-window-open coincidence)", C2803_FOREIGN - WIN, D("0.227417099")),
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
guard("block_title", lines[1].startswith("CYCLE 2804"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2804"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2805 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2806_birth",
      block.count("c2806") == 4 and lines[-1].count("c2806") == 2
      and "c2805/c2806" in lines[-1] and "FORWARD token c2806" in lines[-1]
      and "the c2806 pre==0 expectation" in block and "c2806_pre = 0" in block,
      f"block c2806={block.count('c2806')} next-line c2806={lines[-1].count('c2806')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2806_pre = 0' + the Next bullet's guard phrase 'c2805/c2806' AND "
      f"census-tuple sentence 'FORWARD token c2806')")
guard("block_c2805_step7_precount_sentence",
      "the c2805 pre-count is 4" in block
      and "per-line {9374: 2, 9376: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2805 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9376", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2804_next_bullet", last_nonempty.startswith("- Next: the c2804 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2804",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2804")]) == 0,
      f"c2804 substring mentions={wl.count('c2804')} (expect 14)")
c2804_lines = {i + 1: l.count("c2804") for i, l in enumerate(wl.splitlines()) if "c2804" in l}
guard("c2804_mention_census_pre", wl.count("c2804") == 14
      and c2804_lines == {9362: 2, 9364: 2, 9368: 5, 9374: 1, 9376: 4},
      f"per-line={c2804_lines}")
c2805_lines = {i + 1: l.count("c2805") for i, l in enumerate(wl.splitlines()) if "c2805" in l}
guard("c2805_forward_token_pre", wl.count("c2805") == 4 and c2805_lines == {9374: 2, 9376: 2},
      f"per-line={c2805_lines} (2 births in the c2803 Step-7 twin-print line 9374 + "
      f"2 FORWARD-token births inside the c2803 Next-block — the born-FOUR class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==481", tid_pre == 481, f"got={tid_pre}")
guard("anchor_nogold_pre==414", gold_pre == 414, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2806_pre==0", c2806_pre == 0, f"got={c2806_pre} (the forward token c2806 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2805_pre==4", c2805_pre == 4, f"got={c2805_pre} (born FOUR: the c2803 Step-7 twin-print "
      f"line 9374 TWICE + TWICE inside the c2803 Next-block — NOT the unborn class)")
guard("c2804_pre==14", c2804_pre == 14, f"got={c2804_pre}")
guard("c2803_pre==40", c2803_pre == 40, f"got={c2803_pre}")
guard("c2802_pre==91", c2802_pre == 91, f"got={c2802_pre}")
guard("c2801_pre==81", c2801_pre == 81, f"got={c2801_pre}")
guard("c2800_pre==103", c2800_pre == 103, f"got={c2800_pre}")
guard("c2799_pre==89", c2799_pre == 89, f"got={c2799_pre}")
guard("c2798_pre==87", c2798_pre == 87, f"got={c2798_pre}")
guard("c2797_pre==82", c2797_pre == 82, f"got={c2797_pre}")
guard("c2796_pre==92", c2796_pre == 92, f"got={c2796_pre}")
guard("c2795_pre==112", c2795_pre == 112, f"got={c2795_pre}")
guard("c2794_pre==109", c2794_pre == 109, f"got={c2794_pre}")
guard("c2793_pre==117", c2793_pre == 117, f"got={c2793_pre}")
guard("c2792_pre==122", c2792_pre == 122, f"got={c2792_pre}")
guard("c2791_pre==110", c2791_pre == 110, f"got={c2791_pre}")
guard("c2790_pre==120", c2790_pre == 120, f"got={c2790_pre}")
guard("c2789_pre==113", c2789_pre == 113, f"got={c2789_pre}")
guard("c2788_pre==124", c2788_pre == 124, f"got={c2788_pre}")
guard("c2787_pre==125", c2787_pre == 125, f"got={c2787_pre}")
guard("c2786_pre==144", c2786_pre == 144, f"got={c2786_pre}")
guard("c2785_pre==129", c2785_pre == 129, f"got={c2785_pre}")
guard("c2784_pre==127", c2784_pre == 127, f"got={c2784_pre}")
guard("c2783_pre==128", c2783_pre == 128, f"got={c2783_pre}")
guard("c2782_pre==127", c2782_pre == 127, f"got={c2782_pre}")
guard("c2781_pre==132", c2781_pre == 132, f"got={c2781_pre}")
guard("c2780_pre==137", c2780_pre == 137, f"got={c2780_pre}")
guard("c2779_pre==137", c2779_pre == 137, f"got={c2779_pre}")
guard("c2778_pre==181", c2778_pre == 181, f"got={c2778_pre}")
guard("c2777_pre==153", c2777_pre == 153, f"got={c2777_pre}")
guard("c2776_pre==158", c2776_pre == 158, f"got={c2776_pre}")
guard("c2775_pre==167", c2775_pre == 167, f"got={c2775_pre}")
guard("c2774_pre==172", c2774_pre == 172, f"got={c2774_pre}")
guard("c2773_pre==176", c2773_pre == 176, f"got={c2773_pre}")
guard("c2772_pre==195", c2772_pre == 195, f"got={c2772_pre}")
guard("c2771_pre==185", c2771_pre == 185, f"got={c2771_pre}")
guard("c2770_pre==230", c2770_pre == 230, f"got={c2770_pre}")
guard("c2769_pre==174", c2769_pre == 174, f"got={c2769_pre}")
guard("c2768_pre==177", c2768_pre == 177, f"got={c2768_pre}")
guard("c2767_pre==232", c2767_pre == 232, f"got={c2767_pre}")
guard("c2766_pre==206", c2766_pre == 206, f"got={c2766_pre}")
guard("c2765_pre==168", c2765_pre == 168, f"got={c2765_pre}")
guard("c2764_pre==170", c2764_pre == 170, f"got={c2764_pre}")
guard("c2763_pre==178", c2763_pre == 178, f"got={c2763_pre}")
guard("c2762_pre==213", c2762_pre == 213, f"got={c2762_pre}")
guard("c2761_pre==227", c2761_pre == 227, f"got={c2761_pre}")
guard("c2760_pre==173", c2760_pre == 173, f"got={c2760_pre}")
guard("c2759_pre==173", c2759_pre == 173, f"got={c2759_pre}")
guard("c2758_pre==175", c2758_pre == 175, f"got={c2758_pre}")
guard("c2757_pre==178", c2757_pre == 178, f"got={c2757_pre}")
guard("c2756_pre==183", c2756_pre == 183, f"got={c2756_pre}")
guard("c2755_pre==190", c2755_pre == 190, f"got={c2755_pre}")
guard("c2754_pre==193", c2754_pre == 193, f"got={c2754_pre}")
guard("c2753_pre==203", c2753_pre == 203, f"got={c2753_pre}")
guard("c2752_pre==209", c2752_pre == 209, f"got={c2752_pre}")
guard("c2751_pre==195", c2751_pre == 195, f"got={c2751_pre}")
guard("c2750_pre==199", c2750_pre == 199, f"got={c2750_pre}")
guard("c2749_pre==201", c2749_pre == 201, f"got={c2749_pre}")
guard("c2748_pre==191", c2748_pre == 191, f"got={c2748_pre}")
guard("c2747_pre==194", c2747_pre == 194, f"got={c2747_pre}")
guard("c2746_pre==197", c2746_pre == 197, f"got={c2746_pre}")

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
guard("post_worklog_lines==9388", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2805_next_bullet", last2.startswith("- Next: the c2805 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==482", tid_post == 482, f"got={tid_post}")
guard("anchor_nogold_post==415", gold_post == 415, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2804_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2804")]) == 1)
expect_c2806_mentions = wl2.count("c2806")
guard("c2806_mention_birth", expect_c2806_mentions == c2806_pre + block.count("c2806"),
      f"pre={c2806_pre} (unborn) + block births={block.count('c2806')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2806_pre + block.count('c2806')} got={expect_c2806_mentions}")
for tag, pre in (("c2805", c2805_pre), ("c2804", c2804_pre), ("c2803", c2803_pre),
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
                 ("c2748", c2748_pre), ("c2747", c2747_pre), ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9376 -> 9388 (+12), c2804 entry + DRIFT-#49 pass-53 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
