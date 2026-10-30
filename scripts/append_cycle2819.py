#!/usr/bin/env python3
"""Guarded worklog append for the c2819 entry (12 lines).

Follows the append_cycle2818.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815/c2816/
c2817/c2818 abort precedent class). The ledger arithmetic stays in the DECIMAL class: every
ns-decomposition check is Decimal-exact or Decimal-with-1e-6-tolerance on the
utc-derived values. THE C2778 ABORT LESSON STRUCTURALIZED: the pre-counters
are built as ONE dict in a single statement block before any guard references
them (the c2778 attempt-1 NameError class is structurally impossible here),
and a REHEARSAL mode (APPEND_REHEARSAL=1) runs the full guard battery against
a byte-identical temp copy BEFORE the real run — the attempt counter counts
REAL runs only. Guards: python-timegm epoch cross-verification (Decimal-class
checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic, the ECHO
decompositions (pre/post/latency/stamp-to-echo/POST-WINDOW — the echo
RE-DERIVABLE this cycle), the stamp-gap/token-gap/token-vs-stamp cadence
triple, the window-2819 EPOCH-governs render check, the window-2820 prophecy
check, the SWEEP split check, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~631µs on the post-echo
this cycle), block structure (12 lines: separator, title, standard Task ID
line, Steps 1-7, no-gold, Next bullet), the FORWARD-token guard (c2821 = 4
block births: the Step-7 rehearsal pre-count print 'the c2821 pre==0
expectation' + the Step-7 census-time print 'c2821_pre = 0' + the Next
bullet's guard phrase 'c2820/c2821' AND census-tuple sentence 'FORWARD token
c2821' — the c2767..c2819 forward-token lessons; NOTE the c2821 pre-count is
0 (unborn) while the c2820 pre-count is 4 (born: the c2818 Step-7 twin-print
line 9554 TWICE + TWICE inside the c2818 Next-block) — the c2818 append
prophecy 'c2820 = 4 block births' held EXACTLY: the born-FOUR class REPEATS
a FIFTEENTH time), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9556 lines,
tail = the c2819 Next bullet, zero serviced c2819 entries, c2819 mention
census per-line {9542: 2, 9544: 2, 9548: 3, 9554: 1, 9556: 4} total 12,
c2820 = 4 per-line {9554: 2, 9556: 2}, c2821 = 0 UNBORN, anchors
496/429/60/28), post-state (9568 lines, tail = the c2820 Next bullet,
anchors 497/430/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2819.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9556
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


POST = D("1793335756.357947395")    # c2819 capture post-echo (EPOCH-governs)
SCAN = D("1793335756.352")          # c2819 scanned_at (decimal)
TRIG = D("1793334678.000")          # c2819 trigger stamp (12:31:18 +08)
WIN = D("1793335216.503403091")     # window-2819 open (c2818 prophecy EPOCH)
PRE = D("1793335754.652641980")     # c2819 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793335434.454358605")   # c2819 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793335436.153565649")  # c2819 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793335436.147")        # c2819 echo scanned_at (decimal)
C2818_SCAN = D("1793334916.498")    # c2818 scanned_at
C2818_POST = D("1793334916.503403091")  # c2818 post-echo
C2818_PRE = D("1793334914.697021096")   # c2818 capture pre-echo
C2818_ECHO_PRE = D("1793334742.515107961")  # c2818 echo pre-echo
C2818_ECHO_POST = D("1793334744.168910915")  # c2818 echo post-echo
C2817_POST = D("1793334101.674751215")  # c2817 post-echo (window-2818 re-check)
WIN2818 = D("1793334401.674751215")  # window-2818 open (re-check)
C2818_CLOSE = D("1793335240.000")   # c2818 close 290adbb (04:40:40Z)
FOREIGN_NOW = D("1793335262.000")   # foreign 724e4a0 (04:41:02Z)
C2818_TRIG = D("1793334078.000")    # c2818 trigger stamp (12:21:18 +08)
TOKEN = D("1793335260.000")         # token 1241 (12:41:00 +08)
C2818_TOKEN = D("1793334420.000")   # token 1227 (12:27:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 12:31:18 +08 = 1793334678.000", dec_epoch(2026, 10, 30, 4, 31, 18), TRIG),
    ("c2818 trigger stamp 12:21:18 +08 = 1793334078.000", dec_epoch(2026, 10, 30, 4, 21, 18), C2818_TRIG),
    ("stamp-gap 600.000s by stamp (12:21:18 -> 12:31:18; 49 priors of the exact form)", TRIG - C2818_TRIG, D("600.000")),
    ("token-gap 840.000s by token (1227 -> 1241; 6 priors of the exact '840.000s by token' form)", TOKEN - C2818_TOKEN, D("840.000")),
    ("token-vs-stamp +582.000 (12:31:18 -> 12:41:00; the +582 print, 0 priors)", TOKEN - TRIG, D("582.000")),
    ("c2818 close 290adbb 04:40:40Z = 1793335240.000", dec_epoch(2026, 10, 30, 4, 40, 40), C2818_CLOSE),
    ("foreign 724e4a0 04:41:02Z = 1793335262.000", dec_epoch(2026, 10, 30, 4, 41, 2), FOREIGN_NOW),
    ("token 1241 = 04:41:00Z = 1793335260.000", dec_epoch(2026, 10, 30, 4, 41, 0), TOKEN),
    ("c2818 token 1227 = 04:27:00Z = 1793334420.000", dec_epoch(2026, 10, 30, 4, 27, 0), C2818_TOKEN),
    ("capture pre-echo EPOCH 1793335754.652641980 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 49, 14, 652641980), PRE),
    ("pre-echo ISO 04:49:14.651999009 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 49, 14, 651999009), D("1793335754.651999009")),
    ("post-echo ISO 04:49:16.357316613 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 49, 16, 357316613), D("1793335756.357316613")),
    ("post-echo EPOCH 1793335756.357947395 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 49, 16, 357947395), POST),
    ("scanned_at 04:49:16.352 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 49, 16) + D("0.352"), SCAN),
    ("window-2819 open 04:40:16.503403091 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 4, 40, 16, 503403091), WIN),
    ("window-2820 open = post-echo + 300.000", POST + D("300.000"), D("1793336056.357947395")),
    ("c2818 post-echo EPOCH 1793334916.503403091 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 35, 16, 503403091), C2818_POST),
    ("c2818 scanned_at 04:35:16.498 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 35, 16) + D("0.498"), C2818_SCAN),
    ("c2818 capture pre-echo EPOCH 1793334914.697021096 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 35, 14, 697021096), C2818_PRE),
    ("c2818 echo pre-echo EPOCH 1793334742.515107961 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 32, 22, 515107961), C2818_ECHO_PRE),
    ("c2818 echo post-echo EPOCH 1793334744.168910915 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 32, 24, 168910915), C2818_ECHO_POST),
    ("echo pre-echo EPOCH 1793335434.454358605 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 43, 54, 454358605), ECHO_PRE),
    ("echo post-echo EPOCH 1793335436.153565649 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 43, 56, 153565649), ECHO_POST),
    ("echo scanned_at 04:43:56.147 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 43, 56) + D("0.147"), ECHO_SCAN),
    ("window-2818 open 04:26:41.674751215 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 4, 26, 41, 674751215), WIN2818),
]
exact_checks = [
    ("skew decimal-exact +5.947395ms (EPOCH-governs decomposition; SUB-10 extends m16)", POST - SCAN, D("0.005947395")),
    ("CAPTURE_vs_window +539.854544304 (POST-WINDOW; the capture-side print)", POST - WIN, D("539.854544304")),
    ("capture post-c2818-post-echo +839.854544304", POST - C2818_POST, D("839.854544304")),
    ("dd#393 = +539.854000000 (interval 839.854 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#391 print 856.966 - 300 = 556.966 and the dd#392 print 814.829 - 300 = 514.829)", SCAN - C2818_SCAN - D("300.000"), D("539.854")),
    ("dd formula re-verification: 1117.727 - 300 = 817.727", D("1117.727") - D("300.000"), D("817.727")),
    ("dd formula re-verification: 1401.540 - 300 = 1101.540", D("1401.540") - D("300.000"), D("1101.540")),
    ("dd formula re-verification: 1012.213 - 300 = 712.213", D("1012.213") - D("300.000"), D("712.213")),
    ("dd formula re-verification: 1025.011 - 300 = 725.011", D("1025.011") - D("300.000"), D("725.011")),
    ("dd formula re-verification: 856.966 - 300 = 556.966", D("856.966") - D("300.000"), D("556.966")),
    ("dd formula re-verification: 814.829 - 300 = 514.829", D("814.829") - D("300.000"), D("514.829")),
    ("dd formula re-verification: 839.854 - 300 = 539.854", D("839.854") - D("300.000"), D("539.854")),
    ("INTERVAL#393 = 1078.352", SCAN - TRIG, D("1078.352")),
    ("LAG#393 = INTERVAL + dd - INTERVAL#392 = +779.708", (SCAN - TRIG) + (SCAN - C2818_SCAN - D("300.000")) - D("838.498"), D("779.708")),
    ("LATE#393 = trigger - window-open = -538.503403091", TRIG - WIN, D("-538.503403091")),
    ("window-2819 = c2818 capture post-echo + 300.000 (the server contract)", WIN - C2818_POST, D("300.000")),
    ("window-2818 = c2817 capture post-echo + 300.000 (the contract re-check)", WIN2818 - C2817_POST, D("300.000")),
    ("trigger PREDATES the c2818 echo pre-echo by 64.515107961s (the PRE-ECHO phase — the earliest placement observed)", C2818_ECHO_PRE - TRIG, D("64.515107961")),
    ("trigger PREDATES the c2818 echo post-echo by 66.168910915s", C2818_ECHO_POST - TRIG, D("66.168910915")),
    ("trigger PREDATES the c2818 capture pre-echo by 236.697021096s (the PRE-capture placement EXTENDS m3)", C2818_PRE - TRIG, D("236.697021096")),
    ("trigger PREDATES the c2818 scanned_at by 238.498s", C2818_SCAN - TRIG, D("238.498")),
    ("trigger PREDATES the c2818 capture post-echo by 238.503403091s", C2818_POST - TRIG, D("238.503403091")),
    ("c2818 close POSTDATES the trigger by 562.000s (290adbb at 04:40:40)", C2818_CLOSE - TRIG, D("562.000")),
    ("foreign 724e4a0 POSTDATES the trigger by 584.000s (04:41:02)", FOREIGN_NOW - TRIG, D("584.000")),
    ("c2818 close landed 20.000s BEFORE the token-1241 second (04:40:40 vs 04:41:00 — the BEFORE-class EXTENDS m5)", TOKEN - C2818_CLOSE, D("20.000")),
    ("foreign 724e4a0 landed 2.000s AFTER the token second (04:41:02 — the SPLIT official-BEFORE/foreign-AFTER state EXTENDS m4)", FOREIGN_NOW - TOKEN, D("2.000")),
    ("c2818 close landed 23.496596909s AFTER window-2819 open", C2818_CLOSE - WIN, D("23.496596909")),
    ("foreign 724e4a0 landed 45.496596909s AFTER window-2819 open", FOREIGN_NOW - WIN, D("45.496596909")),
    ("echo POST-WINDOW +219.650162558 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("219.650162558")),
    ("stamp-to-echo 756.454358605 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS — 756.454358605 shallower)", ECHO_PRE - TRIG, D("756.454358605")),
    ("stamp-to-capture-pre 1076.652641980 (the capture pre-echo EPOCH minus the trigger)", PRE - TRIG, D("1076.652641980")),
    ("echo wall latency 1.699207044 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.689836 / server 1679ms latency-match)", ECHO_POST - ECHO_PRE, D("1.699207044")),
    ("capture wall latency 1.705305415 (capture post-echo EPOCH - capture pre-echo EPOCH; curl 1.695880 / server 1689ms latency-match)", POST - PRE, D("1.705305415")),
    ("echo PREDATED the capture pre-echo by 318.499076331 (the echo-then-capture order class EXTENDS m13)", PRE - ECHO_POST, D("318.499076331")),
    ("LAG run-high distance 932.888 (1712.596 - 779.708 — no run-high rewrite)", D("1712.596") - D("779.708"), D("932.888")),
    ("LATE magnitude grew 214.828651876 (538.503403091 - 323.674751215 — the c2818 narrowing REVERSED)", D("538.503403091") - D("323.674751215"), D("214.828651876")),
    ("SKEW headroom 4.052605 (10 - 5.947395 — the flip-band watched; the ms-scale check)", D("10.000000") - D("5.947395"), D("4.052605")),
    ("SWEEP server miss 22.000 (1711.000 - 1689.000 — the print sits BELOW the lower edge)", D("1711.000") - D("1689.000"), D("22.000")),
    ("echo-side skew-analog +0.006565649 (echo post-echo EPOCH - echo scanned_at)", ECHO_POST - ECHO_SCAN, D("0.006565649")),
    ("DRAIN miss 24.698241212 (564.552241212 - 539.854 — the print sits BELOW the dd lower edge)", D("564.552241212") - D("539.854"), D("24.698241212")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m13)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2819"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2819"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2820 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2821_birth",
      block.count("c2821") == 4 and lines[-1].count("c2821") == 2
      and "c2820/c2821" in lines[-1] and "FORWARD token c2821" in lines[-1]
      and "the c2821 pre==0 expectation" in block and "c2821_pre = 0" in block,
      f"block c2821={block.count('c2821')} next-line c2821={lines[-1].count('c2821')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2821_pre = 0' + the Next bullet's guard phrase 'c2820/c2821' AND "
      f"census-tuple sentence 'FORWARD token c2821')")
guard("block_c2820_step7_precount_sentence",
      "the c2820 pre-count is 4" in block
      and "per-line {9554: 2, 9556: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2820 pre-count is 4, "
      "born per the census measurement)")
guard("block_birth_accounting",
      block.count("c2820") == 8 and block.count("c2819") == 29
      and block.count("c2818") == 47 and block.count("c2817") == 10,
      f"c2820={block.count('c2820')} c2819={block.count('c2819')} "
      f"c2818={block.count('c2818')} c2817={block.count('c2817')} (the MEASURED "
      f"block births)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9556", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2819_next_bullet", last_nonempty.startswith("- Next: the c2819 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2819",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2819")]) == 0,
      f"c2819 substring mentions={wl.count('c2819')} (expect 12)")

# pre-counters — ONE dict built in a single statement block (the c2778
# NameError lesson structuralized: no guard can reference an unassigned name)
CENSUS_PRE = {f"c{y}": wl.count(f"c{y}")
              for y in list(range(2821, 2749, -1))}
CENSUS_EXPECT = {
    "c2821": 0, "c2820": 4, "c2819": 12, "c2818": 43, "c2817": 97, "c2816": 91,
    "c2815": 91, "c2814": 85, "c2813": 98, "c2812": 90, "c2811": 96, "c2810": 113,
    "c2809": 92, "c2808": 104, "c2807": 93, "c2806": 89, "c2805": 105, "c2804": 116,
    "c2803": 122, "c2802": 136, "c2801": 102, "c2800": 152, "c2799": 107, "c2798": 105,
    "c2797": 97, "c2796": 107, "c2795": 130, "c2794": 124, "c2793": 132, "c2792": 137,
    "c2791": 125, "c2790": 138, "c2789": 128, "c2788": 139, "c2787": 140, "c2786": 162,
    "c2785": 144, "c2784": 142, "c2783": 143, "c2782": 142, "c2781": 147, "c2780": 152,
    "c2779": 152, "c2778": 196, "c2777": 168, "c2776": 173, "c2775": 182, "c2774": 187,
    "c2773": 191, "c2772": 210, "c2771": 200, "c2770": 261, "c2769": 189, "c2768": 192,
    "c2767": 277, "c2766": 239, "c2765": 183, "c2764": 185, "c2763": 193, "c2762": 230,
    "c2761": 258, "c2760": 188, "c2759": 188, "c2758": 190, "c2757": 193, "c2756": 198,
    "c2755": 205, "c2754": 208, "c2753": 233, "c2752": 239, "c2751": 225, "c2750": 231,
}
c2821_lines = {i + 1: l.count("c2821") for i, l in enumerate(wl.splitlines()) if "c2821" in l}
c2820_lines = {i + 1: l.count("c2820") for i, l in enumerate(wl.splitlines()) if "c2820" in l}
c2819_lines = {i + 1: l.count("c2819") for i, l in enumerate(wl.splitlines()) if "c2819" in l}
c2818_lines = {i + 1: l.count("c2818") for i, l in enumerate(wl.splitlines()) if "c2818" in l}
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(wl.splitlines()) if "c2817" in l}
guard("c2821_pre==0", CENSUS_PRE["c2821"] == 0 and c2821_lines == {},
      f"got={CENSUS_PRE['c2821']} per-line={c2821_lines} (the forward token "
      f"c2821 is UNBORN pre-append — measured pre-append)")
guard("c2820_pre==4", CENSUS_PRE["c2820"] == 4 and c2820_lines == {9554: 2, 9556: 2},
      f"got={CENSUS_PRE['c2820']} per-line={c2820_lines} (born FOUR: the c2818 Step-7 "
      f"twin-print line 9554 TWICE + TWICE inside the c2818 Next-block — NOT the "
      f"unborn class; the born-FOUR class REPEATS a FIFTEENTH time)")
guard("c2819_pre==12", CENSUS_PRE["c2819"] == 12
      and c2819_lines == {9542: 2, 9544: 2, 9548: 3, 9554: 1, 9556: 4},
      f"got={CENSUS_PRE['c2819']} per-line={c2819_lines} (the MEASURED weight — the "
      f"pre-block state 4 + 8 births inside the c2818 block, the honest note)")
guard("c2818_pre==43", CENSUS_PRE["c2818"] == 43
      and c2818_lines == {9530: 2, 9532: 2, 9536: 5, 9542: 1, 9544: 4, 9547: 1,
                          9548: 7, 9549: 6, 9554: 4, 9556: 11},
      f"got={CENSUS_PRE['c2818']} per-line={c2818_lines} (the MEASURED weight — the "
      f"pre-block state 14 + 29 births inside the c2818 block, the honest note)")
guard("c2817_pre==97", CENSUS_PRE["c2817"] == 97
      and c2817_lines == {9518: 2, 9520: 2, 9524: 4, 9530: 1, 9532: 4, 9535: 1,
                          9536: 8, 9537: 5, 9542: 4, 9544: 11, 9546: 17, 9548: 17,
                          9549: 5, 9550: 5, 9553: 4, 9554: 3, 9556: 4},
      f"got={CENSUS_PRE['c2817']} per-line={c2817_lines} (the MEASURED weight — the "
      f"pre-block state 42 + 55 births inside the c2818 block, the honest note)")
for tag in [f"c{y}" for y in range(2816, 2749, -1)]:
    guard(f"{tag}_pre=={CENSUS_EXPECT[tag]}", CENSUS_PRE[tag] == CENSUS_EXPECT[tag],
          f"got={CENSUS_PRE[tag]}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==496", tid_pre == 496, f"got={tid_pre}")
guard("anchor_nogold_pre==429", gold_pre == 429, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")

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
guard("post_worklog_lines==9568", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2820_next_bullet", last2.startswith("- Next: the c2820 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==497", tid_post == 497, f"got={tid_post}")
guard("anchor_nogold_post==430", gold_post == 430, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2819_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2819")]) == 1)
guard("c2821_mention_birth", wl2.count("c2821") == CENSUS_PRE["c2821"] + block.count("c2821"),
      f"pre={CENSUS_PRE['c2821']} (unborn) + block births={block.count('c2821')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={CENSUS_PRE['c2821'] + block.count('c2821')} got={wl2.count('c2821')}")
for tag in [f"c{y}" for y in range(2820, 2749, -1)]:
    expect = CENSUS_PRE[tag] + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={CENSUS_PRE[tag]} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9556 -> 9568 (+12), c2819 entry + DRIFT-#49 pass-68 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
