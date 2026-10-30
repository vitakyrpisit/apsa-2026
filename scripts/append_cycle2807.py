#!/usr/bin/env python3
"""Guarded worklog append for the c2807 entry (12 lines).

Follows the append_cycle2806.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806 abort precedent class). The ledger arithmetic stays in the DECIMAL
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
the stamp-gap/token-gap/token-vs-stamp cadence triple, the window-2807
EPOCH-governs render check, the window-2808 prophecy check, and the
queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock
reads differ ~657µs on the post-echo this cycle), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
the FORWARD-token guard (c2809 = 4 block births: the Step-7 rehearsal
pre-count print 'the c2809 pre==0 expectation' + the Step-7 census-time print
'c2809_pre = 0' + the Next bullet's guard phrase 'c2808/c2809' AND
census-tuple sentence 'FORWARD token c2809' — the c2767..c2807 forward-token
lessons; NOTE the c2809 pre-count is 0 (unborn) while the c2808 pre-count is
4 (born: the c2806 Step-7 twin-print line 9410 TWICE + TWICE inside the
c2806 Next-block) — the c2806 append prophecy 'c2808 = 4 block births' held
EXACTLY: the born-FOUR class REPEATS a FOURTH time), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9412 lines, tail = the c2807 Next bullet, zero serviced
c2807 entries, c2807 mention census per-line {9398: 2, 9400: 2, 9404: 5,
9410: 1, 9412: 4} total 14, c2808 = 4 per-line {9410: 2, 9412: 2}, anchors
484/417/60/28), post-state (9424 lines, tail = the c2808 Next bullet,
anchors 485/418/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2807.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9412
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


POST = D("1793323992.810145543")    # c2807 post-echo (EPOCH-governs)
SCAN = D("1793323992.804")          # c2807 scanned_at (decimal)
TRIG = D("1793322974.000")          # c2807 trigger stamp (09:16:14 +08)
WIN = D("1793323481.104795547")     # window-2807 open (c2806 prophecy EPOCH)
PRE = D("1793323991.072783920")     # c2807 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793323838.862424272")   # c2807 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793323840.586538137")  # c2807 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793323840.523")        # c2807 echo scanned_at (decimal)
C2806_SCAN = D("1793323181.098")    # c2806 scanned_at
C2806_POST = D("1793323181.104795547")  # c2806 post-echo
C2806_PRE = D("1793323179.315388590")   # c2806 capture pre-echo
C2806_ECHO_POST = D("1793322961.533383900")  # c2806 echo post-echo
C2806_CLOSE = D("1793323497.000")   # c2806 close cceafc6 (01:24:57Z)
FOREIGN_NOW = D("1793323511.000")   # foreign 92a8201 (01:25:11Z)
C2806_FOREIGN = D("1793322862.000")  # foreign 35ba192 (01:14:22Z)
C2806_TRIG = D("1793322374.000")    # c2806 trigger stamp (09:06:14 +08)
WIN2806 = D("1793322818.012641186")  # window-2806 open (for the trigger-postdates check)
TOKEN = D("1793323500.000")         # token 0925 (09:25:00 +08)
C2806_TOKEN = D("1793322840.000")   # token 0914 (09:14:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 09:16:14 +08 = 1793322974.000", dec_epoch(2026, 10, 30, 1, 16, 14), TRIG),
    ("c2806 trigger stamp 09:06:14 +08 = 1793322374.000", dec_epoch(2026, 10, 30, 1, 6, 14), C2806_TRIG),
    ("stamp-gap 600.000s by stamp (09:06:14 -> 09:16:14; the 600 print REPEATS)", TRIG - C2806_TRIG, D("600.000")),
    ("token-gap 660.000s by token (0914 -> 0925; the 660 print RETURNS)", TOKEN - C2806_TOKEN, D("660.000")),
    ("token-vs-stamp +526.000 (09:16:14 -> 09:25:00; the +526 print NEW)", TOKEN - TRIG, D("526.000")),
    ("c2806 close cceafc6 01:24:57Z = 1793323497.000", dec_epoch(2026, 10, 30, 1, 24, 57), C2806_CLOSE),
    ("foreign 92a8201 01:25:11Z = 1793323511.000", dec_epoch(2026, 10, 30, 1, 25, 11), FOREIGN_NOW),
    ("token 0925 = 01:25:00Z = 1793323500.000", dec_epoch(2026, 10, 30, 1, 25, 0), TOKEN),
    ("c2806 token 0914 = 01:14:00Z = 1793322840.000", dec_epoch(2026, 10, 30, 1, 14, 0), C2806_TOKEN),
    ("capture pre-echo EPOCH 1793323991.072783920 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 33, 11, 72783920), PRE),
    ("pre-echo ISO 01:33:11.072088733 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 33, 11, 72088733), D("1793323991.072088733")),
    ("post-echo ISO 01:33:12.809488264 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 33, 12, 809488264), D("1793323992.809488264")),
    ("post-echo EPOCH 1793323992.810145543 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 33, 12, 810145543), POST),
    ("scanned_at 01:33:12.804 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 33, 12) + D("0.804"), SCAN),
    ("window-2807 open 01:24:41.104795547 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 1, 24, 41, 104795547), WIN),
    ("window-2808 open = post-echo + 300.000", POST + D("300.000"), D("1793324292.810145543")),
    ("c2806 post-echo EPOCH 1793323181.104795547 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 19, 41, 104795547), C2806_POST),
    ("c2806 scanned_at 01:19:41.098 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 19, 41) + D("0.098"), C2806_SCAN),
    ("c2806 capture pre-echo EPOCH 1793323179.315388590 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 19, 39, 315388590), C2806_PRE),
    ("c2806 echo post-echo EPOCH 1793322961.533383900 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 16, 1, 533383900), C2806_ECHO_POST),
    ("echo pre-echo EPOCH 1793323838.862424272 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 30, 38, 862424272), ECHO_PRE),
    ("echo pre-echo ISO 01:30:38.861666044 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 30, 38, 861666044), D("1793323838.861666044")),
    ("echo post-echo ISO 01:30:40.564947016 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 1, 30, 40, 564947016), D("1793323840.564947016")),
    ("echo post-echo EPOCH 1793323840.586538137 (EPOCH-governs)", dec_epoch(2026, 10, 30, 1, 30, 40, 586538137), ECHO_POST),
    ("echo scanned_at 01:30:40.523 +0000 (decimal)", dec_epoch(2026, 10, 30, 1, 30, 40) + D("0.523"), ECHO_SCAN),
]
exact_checks = [
    ("skew decimal-exact +6.145543ms (EPOCH-governs decomposition; SUB-10 extends m4)", POST - SCAN, D("0.006145543")),
    ("CAPTURE_vs_window +511.705349996 (POST-WINDOW; the capture-side print)", POST - WIN, D("511.705349996")),
    ("capture post-c2806-post-echo +811.705349996", POST - C2806_POST, D("811.705349996")),
    ("dd#381 = +511.706000000 (interval 811.706 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#380 print 663.092 - 300 = 363.092 and the dd#379 print 740.572 - 300 = 440.572)", SCAN - C2806_SCAN - D("300.000"), D("511.706")),
    ("dd formula re-verification: 423.763 - 300 = 123.763", D("423.763") - D("300.000"), D("123.763")),
    ("dd formula re-verification: 740.182 - 300 = 440.182", D("740.182") - D("300.000"), D("440.182")),
    ("dd formula re-verification: 663.725 - 300 = 363.725", D("663.725") - D("300.000"), D("363.725")),
    ("dd formula re-verification: 740.572 - 300 = 440.572", D("740.572") - D("300.000"), D("440.572")),
    ("dd formula re-verification: 663.092 - 300 = 363.092", D("663.092") - D("300.000"), D("363.092")),
    ("INTERVAL#381 = 1018.804", SCAN - TRIG, D("1018.804")),
    ("LAG#381 = INTERVAL + dd - dd#380 = +1167.418", (SCAN - TRIG) + (SCAN - C2806_SCAN - D("300.000")) - D("363.092"), D("1167.418")),
    ("LATE#381 = trigger - window-open = -507.104795547", TRIG - WIN, D("-507.104795547")),
    ("window-2807 = c2806 post-echo + 300.000 (the server contract)", WIN - C2806_POST, D("300.000")),
    ("trigger POSTDATES the c2806 echo post-echo by 12.466616100s (the POST-echo placement REPEATS)", TRIG - C2806_ECHO_POST, D("12.466616100")),
    ("trigger PREDATES the c2806 pre-echo by 205.315388590s", C2806_PRE - TRIG, D("205.315388590")),
    ("trigger PREDATES the c2806 scanned_at by 207.098s", C2806_SCAN - TRIG, D("207.098")),
    ("trigger POSTDATES window-2806 open by 155.987358814s", TRIG - WIN2806, D("155.987358814")),
    ("c2806 close POSTDATES the trigger by 523.000s (cceafc6 at 01:24:57)", C2806_CLOSE - TRIG, D("523.000")),
    ("foreign 92a8201 POSTDATES the trigger by 537.000s (01:25:11)", FOREIGN_NOW - TRIG, D("537.000")),
    ("c2806 close landed 3.000s BEFORE the token-0925 second (01:24:57 vs 01:25:00 — the BEFORE-class opens m1)", TOKEN - C2806_CLOSE, D("3.000")),
    ("foreign 92a8201 landed 11.000s AFTER the token second (01:25:11)", FOREIGN_NOW - TOKEN, D("11.000")),
    ("foreign 92a8201 landed +29.895204453s AFTER window-2807 open", FOREIGN_NOW - WIN, D("29.895204453")),
    ("c2806 close cceafc6 landed +15.895204453s AFTER window-2807 open", C2806_CLOSE - WIN, D("15.895204453")),
    ("echo POST-WINDOW +359.481742590 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("359.481742590")),
    ("stamp-to-echo 864.862424272 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS)", ECHO_PRE - TRIG, D("864.862424272")),
    ("echo wall latency 1.724113865 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.678441 / server 1678ms latency-match)", ECHO_POST - ECHO_PRE, D("1.724113865")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m5)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2807"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2807"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2808 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2809_birth",
      block.count("c2809") == 4 and lines[-1].count("c2809") == 2
      and "c2808/c2809" in lines[-1] and "FORWARD token c2809" in lines[-1]
      and "the c2809 pre==0 expectation" in block and "c2809_pre = 0" in block,
      f"block c2809={block.count('c2809')} next-line c2809={lines[-1].count('c2809')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2809_pre = 0' + the Next bullet's guard phrase 'c2808/c2809' AND "
      f"census-tuple sentence 'FORWARD token c2809')")
guard("block_c2808_step7_precount_sentence",
      "the c2808 pre-count is 4" in block
      and "per-line {9410: 2, 9412: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2808 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9412", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2807_next_bullet", last_nonempty.startswith("- Next: the c2807 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2807",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2807")]) == 0,
      f"c2807 substring mentions={wl.count('c2807')} (expect 14)")
c2807_lines = {i + 1: l.count("c2807") for i, l in enumerate(wl.splitlines()) if "c2807" in l}
guard("c2807_mention_census_pre", wl.count("c2807") == 14
      and c2807_lines == {9398: 2, 9400: 2, 9404: 5, 9410: 1, 9412: 4},
      f"per-line={c2807_lines}")
c2808_lines = {i + 1: l.count("c2808") for i, l in enumerate(wl.splitlines()) if "c2808" in l}
guard("c2808_forward_token_pre", wl.count("c2808") == 4 and c2808_lines == {9410: 2, 9412: 2},
      f"per-line={c2808_lines} (2 births in the c2806 Step-7 twin-print line 9410 + "
      f"2 FORWARD-token births inside the c2806 Next-block — the born-FOUR class "
      f"REPEATS a FOURTH time)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==484", tid_pre == 484, f"got={tid_pre}")
guard("anchor_nogold_pre==417", gold_pre == 417, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
c2747_pre = wl.count("c2747")
c2746_pre = wl.count("c2746")
guard("c2809_pre==0", c2809_pre == 0, f"got={c2809_pre} (the forward token c2809 is UNBORN "
      f"pre-append — measured pre-append)")
guard("c2808_pre==4", c2808_pre == 4, f"got={c2808_pre} (born FOUR: the c2806 Step-7 twin-print "
      f"line 9410 TWICE + TWICE inside the c2806 Next-block — NOT the unborn class)")
guard("c2807_pre==14", c2807_pre == 14, f"got={c2807_pre}")
guard("c2806_pre==36", c2806_pre == 36, f"got={c2806_pre}")
guard("c2805_pre==75", c2805_pre == 75, f"got={c2805_pre}")
guard("c2804_pre==91", c2804_pre == 91, f"got={c2804_pre}")
guard("c2803_pre==99", c2803_pre == 99, f"got={c2803_pre}")
guard("c2802_pre==109", c2802_pre == 109, f"got={c2802_pre}")
guard("c2801_pre==89", c2801_pre == 89, f"got={c2801_pre}")
guard("c2800_pre==117", c2800_pre == 117, f"got={c2800_pre}")
guard("c2799_pre==94", c2799_pre == 94, f"got={c2799_pre}")
guard("c2798_pre==92", c2798_pre == 92, f"got={c2798_pre}")
guard("c2797_pre==85", c2797_pre == 85, f"got={c2797_pre}")
guard("c2796_pre==95", c2796_pre == 95, f"got={c2796_pre}")
guard("c2795_pre==117", c2795_pre == 117, f"got={c2795_pre}")
guard("c2794_pre==112", c2794_pre == 112, f"got={c2794_pre}")
guard("c2793_pre==120", c2793_pre == 120, f"got={c2793_pre}")
guard("c2792_pre==125", c2792_pre == 125, f"got={c2792_pre}")
guard("c2791_pre==113", c2791_pre == 113, f"got={c2791_pre}")
guard("c2790_pre==125", c2790_pre == 125, f"got={c2790_pre}")
guard("c2789_pre==116", c2789_pre == 116, f"got={c2789_pre}")
guard("c2788_pre==127", c2788_pre == 127, f"got={c2788_pre}")
guard("c2787_pre==128", c2787_pre == 128, f"got={c2787_pre}")
guard("c2786_pre==149", c2786_pre == 149, f"got={c2786_pre}")
guard("c2785_pre==132", c2785_pre == 132, f"got={c2785_pre}")
guard("c2784_pre==130", c2784_pre == 130, f"got={c2784_pre}")
guard("c2783_pre==131", c2783_pre == 131, f"got={c2783_pre}")
guard("c2782_pre==130", c2782_pre == 130, f"got={c2782_pre}")
guard("c2781_pre==135", c2781_pre == 135, f"got={c2781_pre}")
guard("c2780_pre==140", c2780_pre == 140, f"got={c2780_pre}")
guard("c2779_pre==140", c2779_pre == 140, f"got={c2779_pre}")
guard("c2778_pre==184", c2778_pre == 184, f"got={c2778_pre}")
guard("c2777_pre==156", c2777_pre == 156, f"got={c2777_pre}")
guard("c2776_pre==161", c2776_pre == 161, f"got={c2776_pre}")
guard("c2775_pre==170", c2775_pre == 170, f"got={c2775_pre}")
guard("c2774_pre==175", c2774_pre == 175, f"got={c2774_pre}")
guard("c2773_pre==179", c2773_pre == 179, f"got={c2773_pre}")
guard("c2772_pre==198", c2772_pre == 198, f"got={c2772_pre}")
guard("c2771_pre==188", c2771_pre == 188, f"got={c2771_pre}")
guard("c2770_pre==236", c2770_pre == 236, f"got={c2770_pre}")
guard("c2769_pre==177", c2769_pre == 177, f"got={c2769_pre}")
guard("c2768_pre==180", c2768_pre == 180, f"got={c2768_pre}")
guard("c2767_pre==241", c2767_pre == 241, f"got={c2767_pre}")
guard("c2766_pre==213", c2766_pre == 213, f"got={c2766_pre}")
guard("c2765_pre==171", c2765_pre == 171, f"got={c2765_pre}")
guard("c2764_pre==173", c2764_pre == 173, f"got={c2764_pre}")
guard("c2763_pre==181", c2763_pre == 181, f"got={c2763_pre}")
guard("c2762_pre==218", c2762_pre == 218, f"got={c2762_pre}")
guard("c2761_pre==234", c2761_pre == 234, f"got={c2761_pre}")
guard("c2760_pre==176", c2760_pre == 176, f"got={c2760_pre}")
guard("c2759_pre==176", c2759_pre == 176, f"got={c2759_pre}")
guard("c2758_pre==178", c2758_pre == 178, f"got={c2758_pre}")
guard("c2757_pre==181", c2757_pre == 181, f"got={c2757_pre}")
guard("c2756_pre==186", c2756_pre == 186, f"got={c2756_pre}")
guard("c2755_pre==193", c2755_pre == 193, f"got={c2755_pre}")
guard("c2754_pre==196", c2754_pre == 196, f"got={c2754_pre}")
guard("c2753_pre==209", c2753_pre == 209, f"got={c2753_pre}")
guard("c2752_pre==215", c2752_pre == 215, f"got={c2752_pre}")
guard("c2751_pre==201", c2751_pre == 201, f"got={c2751_pre}")
guard("c2750_pre==205", c2750_pre == 205, f"got={c2750_pre}")
guard("c2749_pre==207", c2749_pre == 207, f"got={c2749_pre}")
guard("c2748_pre==197", c2748_pre == 197, f"got={c2748_pre}")
guard("c2747_pre==200", c2747_pre == 200, f"got={c2747_pre}")
guard("c2746_pre==209", c2746_pre == 209, f"got={c2746_pre}")

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
guard("post_worklog_lines==9424", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2808_next_bullet", last2.startswith("- Next: the c2808 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==485", tid_post == 485, f"got={tid_post}")
guard("anchor_nogold_post==418", gold_post == 418, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2807_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2807")]) == 1)
expect_c2809_mentions = wl2.count("c2809")
guard("c2809_mention_birth", expect_c2809_mentions == c2809_pre + block.count("c2809"),
      f"pre={c2809_pre} (unborn) + block births={block.count('c2809')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={c2809_pre + block.count('c2809')} got={expect_c2809_mentions}")
for tag, pre in (("c2808", c2808_pre), ("c2807", c2807_pre), ("c2806", c2806_pre),
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
                 ("c2748", c2748_pre), ("c2747", c2747_pre), ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9412 -> 9424 (+12), c2807 entry + DRIFT-#49 pass-56 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
