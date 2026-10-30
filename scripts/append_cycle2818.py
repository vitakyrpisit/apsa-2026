#!/usr/bin/env python3
"""Guarded worklog append for the c2818 entry (12 lines).

Follows the append_cycle2817.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815/c2816/
c2817 abort precedent class). The ledger arithmetic stays in the DECIMAL class: every
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
triple, the window-2818 EPOCH-governs render check, the window-2819 prophecy
check, the SWEEP double-miss check, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~625µs on the post-echo
this cycle), block structure (12 lines: separator, title, standard Task ID
line, Steps 1-7, no-gold, Next bullet), the FORWARD-token guard (c2820 = 4
block births: the Step-7 rehearsal pre-count print 'the c2820 pre==0
expectation' + the Step-7 census-time print 'c2820_pre = 0' + the Next
bullet's guard phrase 'c2819/c2820' AND census-tuple sentence 'FORWARD token
c2820' — the c2767..c2818 forward-token lessons; NOTE the c2820 pre-count is
0 (unborn) while the c2819 pre-count is 4 (born: the c2817 Step-7 twin-print
line 9542 TWICE + TWICE inside the c2817 Next-block) — the c2817 append
prophecy 'c2819 = 4 block births' held EXACTLY: the born-FOUR class REPEATS
a FIFTEENTH time), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9544 lines,
tail = the c2818 Next bullet, zero serviced c2818 entries, c2818 mention
census per-line {9530: 2, 9532: 2, 9536: 5, 9542: 1, 9544: 4} total 14,
c2819 = 4 per-line {9542: 2, 9544: 2}, c2820 = 0 UNBORN, anchors
495/428/60/28), post-state (9556 lines, tail = the c2819 Next bullet,
anchors 496/429/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2818.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9544
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


POST = D("1793334916.503403091")    # c2818 capture post-echo (EPOCH-governs)
SCAN = D("1793334916.498")          # c2818 scanned_at (decimal)
TRIG = D("1793334078.000")          # c2818 trigger stamp (12:21:18 +08)
WIN = D("1793334401.674751215")     # window-2818 open (c2817 prophecy EPOCH)
PRE = D("1793334914.697021096")     # c2818 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793334742.515107961")   # c2818 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793334744.168910915")  # c2818 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793334744.162")        # c2818 echo scanned_at (decimal)
C2817_SCAN = D("1793334101.669")    # c2817 scanned_at
C2817_POST = D("1793334101.674751215")  # c2817 post-echo
C2817_PRE = D("1793334100.184672197")   # c2817 capture pre-echo
C2817_ECHO_POST = D("1793333828.255033591")  # c2817 echo post-echo
C2816_POST = D("1793333244.708518331")  # c2816 post-echo (window-2817 re-check)
WIN2817 = D("1793333544.708518331")  # window-2817 open (re-check)
C2817_CLOSE = D("1793334414.000")   # c2817 close da7d469 (04:26:54Z)
FOREIGN_NOW = D("1793334429.000")   # foreign a009715 (04:27:09Z)
C2817_TRIG = D("1793333178.000")    # c2817 trigger stamp (12:06:18 +08)
TOKEN = D("1793334420.000")         # token 1227 (12:27:00 +08)
C2817_TOKEN = D("1793333580.000")   # token 1213 (12:13:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 12:21:18 +08 = 1793334078.000", dec_epoch(2026, 10, 30, 4, 21, 18), TRIG),
    ("c2817 trigger stamp 12:06:18 +08 = 1793333178.000", dec_epoch(2026, 10, 30, 4, 6, 18), C2817_TRIG),
    ("stamp-gap 900.000s by stamp (12:06:18 -> 12:21:18; 12 priors of the exact form)", TRIG - C2817_TRIG, D("900.000")),
    ("token-gap 840.000s by token (1213 -> 1227; 0 priors of the exact '840.000s by token' form — the hand-slip CAUGHT class)", TOKEN - C2817_TOKEN, D("840.000")),
    ("token-vs-stamp +342.000 (12:21:18 -> 12:27:00; the +342 print, 0 priors)", TOKEN - TRIG, D("342.000")),
    ("c2817 close da7d469 04:26:54Z = 1793334414.000", dec_epoch(2026, 10, 30, 4, 26, 54), C2817_CLOSE),
    ("foreign a009715 04:27:09Z = 1793334429.000", dec_epoch(2026, 10, 30, 4, 27, 9), FOREIGN_NOW),
    ("token 1227 = 04:27:00Z = 1793334420.000", dec_epoch(2026, 10, 30, 4, 27, 0), TOKEN),
    ("c2817 token 1213 = 04:13:00Z = 1793333580.000", dec_epoch(2026, 10, 30, 4, 13, 0), C2817_TOKEN),
    ("capture pre-echo EPOCH 1793334914.697021096 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 35, 14, 697021096), PRE),
    ("pre-echo ISO 04:35:14.696389132 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 35, 14, 696389132), D("1793334914.696389132")),
    ("post-echo ISO 04:35:16.502777923 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 35, 16, 502777923), D("1793334916.502777923")),
    ("post-echo EPOCH 1793334916.503403091 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 35, 16, 503403091), POST),
    ("scanned_at 04:35:16.498 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 35, 16) + D("0.498"), SCAN),
    ("window-2818 open 04:26:41.674751215 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 4, 26, 41, 674751215), WIN),
    ("window-2819 open = post-echo + 300.000", POST + D("300.000"), D("1793335216.503403091")),
    ("c2817 post-echo EPOCH 1793334101.674751215 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 21, 41, 674751215), C2817_POST),
    ("c2817 scanned_at 04:21:41.669 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 21, 41) + D("0.669"), C2817_SCAN),
    ("c2817 capture pre-echo EPOCH 1793334100.184672197 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 21, 40, 184672197), C2817_PRE),
    ("c2817 echo post-echo EPOCH 1793333828.255033591 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 17, 8, 255033591), C2817_ECHO_POST),
    ("echo pre-echo EPOCH 1793334742.515107961 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 32, 22, 515107961), ECHO_PRE),
    ("echo post-echo EPOCH 1793334744.168910915 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 32, 24, 168910915), ECHO_POST),
    ("echo scanned_at 04:32:24.162 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 32, 24) + D("0.162"), ECHO_SCAN),
    ("window-2817 open 04:12:24.708518331 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 4, 12, 24, 708518331), WIN2817),
]
exact_checks = [
    ("skew decimal-exact +5.403091ms (EPOCH-governs decomposition; SUB-10 extends m15)", POST - SCAN, D("0.005403091")),
    ("CAPTURE_vs_window +514.828651876 (POST-WINDOW; the capture-side print)", POST - WIN, D("514.828651876")),
    ("capture post-c2817-post-echo +814.828651876", POST - C2817_POST, D("814.828651876")),
    ("dd#392 = +514.829000000 (interval 814.829 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#390 print 1025.011 - 300 = 725.011 and the dd#391 print 856.966 - 300 = 556.966)", SCAN - C2817_SCAN - D("300.000"), D("514.829")),
    ("dd formula re-verification: 1117.727 - 300 = 817.727", D("1117.727") - D("300.000"), D("817.727")),
    ("dd formula re-verification: 1401.540 - 300 = 1101.540", D("1401.540") - D("300.000"), D("1101.540")),
    ("dd formula re-verification: 1012.213 - 300 = 712.213", D("1012.213") - D("300.000"), D("712.213")),
    ("dd formula re-verification: 1025.011 - 300 = 725.011", D("1025.011") - D("300.000"), D("725.011")),
    ("dd formula re-verification: 856.966 - 300 = 556.966", D("856.966") - D("300.000"), D("556.966")),
    ("dd formula re-verification: 814.829 - 300 = 514.829", D("814.829") - D("300.000"), D("514.829")),
    ("INTERVAL#392 = 838.498", SCAN - TRIG, D("838.498")),
    ("LAG#392 = INTERVAL + dd - INTERVAL#391 = +429.658", (SCAN - TRIG) + (SCAN - C2817_SCAN - D("300.000")) - D("923.669"), D("429.658")),
    ("LATE#392 = trigger - window-open = -323.674751215", TRIG - WIN, D("-323.674751215")),
    ("window-2818 = c2817 capture post-echo + 300.000 (the server contract)", WIN - C2817_POST, D("300.000")),
    ("window-2817 = c2816 capture post-echo + 300.000 (the contract re-check)", WIN2817 - C2816_POST, D("300.000")),
    ("trigger POSTDATES the c2817 echo post-echo by 249.744966409s", TRIG - C2817_ECHO_POST, D("249.744966409")),
    ("trigger PREDATES the c2817 capture pre-echo by 22.184672197s (the PRE-capture placement EXTENDS m2)", C2817_PRE - TRIG, D("22.184672197")),
    ("trigger PREDATES the c2817 scanned_at by 23.669s", C2817_SCAN - TRIG, D("23.669")),
    ("trigger PREDATES the c2817 capture post-echo by 23.674751215s", C2817_POST - TRIG, D("23.674751215")),
    ("c2817 close POSTDATES the trigger by 336.000s (da7d469 at 04:26:54)", C2817_CLOSE - TRIG, D("336.000")),
    ("foreign a009715 POSTDATES the trigger by 351.000s (04:27:09)", FOREIGN_NOW - TRIG, D("351.000")),
    ("c2817 close landed 6.000s BEFORE the token-1227 second (04:26:54 vs 04:27:00 — the BEFORE-class EXTENDS m4, the AFTER-class TERMINATED its m1 run at c2817)", TOKEN - C2817_CLOSE, D("6.000")),
    ("foreign a009715 landed 9.000s AFTER the token second (04:27:09 — the SPLIT official-BEFORE/foreign-AFTER state EXTENDS m3)", FOREIGN_NOW - TOKEN, D("9.000")),
    ("c2817 close landed 12.325248785s AFTER window-2818 open", C2817_CLOSE - WIN, D("12.325248785")),
    ("foreign a009715 landed 27.325248785s AFTER window-2818 open", FOREIGN_NOW - WIN, D("27.325248785")),
    ("echo POST-WINDOW +342.494159700 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("342.494159700")),
    ("stamp-to-echo 664.515107961 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS — 664.515107961 shallower)", ECHO_PRE - TRIG, D("664.515107961")),
    ("stamp-to-capture-pre 836.697021096 (the capture pre-echo EPOCH minus the trigger)", PRE - TRIG, D("836.697021096")),
    ("echo wall latency 1.653802954 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.644084 / server 1636ms latency-match)", ECHO_POST - ECHO_PRE, D("1.653802954")),
    ("capture wall latency 1.806381995 (capture post-echo EPOCH - capture pre-echo EPOCH; curl 1.797099 / server 1791ms latency-match)", POST - PRE, D("1.806381995")),
    ("LAG run-high distance 1282.938 (1712.596 - 429.658 — no run-high rewrite)", D("1712.596") - D("429.658"), D("1282.938")),
    ("LATE magnitude shrank 43.033767116 (366.708518331 -> 323.674751215 — the c2817 widening REVERSED)", D("366.708518331") - D("323.674751215"), D("43.033767116")),
    ("SKEW headroom 4.596909 (10 - 5.403091 — the flip-band watched)", D("10.000000") - D("5.403091"), D("4.596909")),
    ("SWEEP client miss 0.197329 (1.797099 - 1.599770 — the print sits ABOVE the upper edge)", D("1.797099") - D("1.599770"), D("0.197329")),
    ("SWEEP server miss 239.000 (1791.000 - 1552.000 — the print sits ABOVE the upper edge)", D("1791.000") - D("1552.000"), D("239.000")),
    ("echo-side skew-analog +0.006910915 (echo post-echo EPOCH - echo scanned_at)", ECHO_POST - ECHO_SCAN, D("0.006910915")),
    ("DRAIN miss 49.723241212 (564.552241212 - 514.829 — the print sits BELOW the dd lower edge)", D("564.552241212") - D("514.829"), D("49.723241212")),
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
guard("block_title", lines[1].startswith("CYCLE 2818"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2818"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2819 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2820_birth",
      block.count("c2820") == 4 and lines[-1].count("c2820") == 2
      and "c2819/c2820" in lines[-1] and "FORWARD token c2820" in lines[-1]
      and "the c2820 pre==0 expectation" in block and "c2820_pre = 0" in block,
      f"block c2820={block.count('c2820')} next-line c2820={lines[-1].count('c2820')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2820_pre = 0' + the Next bullet's guard phrase 'c2819/c2820' AND "
      f"census-tuple sentence 'FORWARD token c2820')")
guard("block_c2819_step7_precount_sentence",
      "the c2819 pre-count is 4" in block
      and "per-line {9542: 2, 9544: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2819 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9544", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2818_next_bullet", last_nonempty.startswith("- Next: the c2818 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2818",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2818")]) == 0,
      f"c2818 substring mentions={wl.count('c2818')} (expect 14)")

# pre-counters — ONE dict built in a single statement block (the c2778
# NameError lesson structuralized: no guard can reference an unassigned name)
CENSUS_PRE = {f"c{y}": wl.count(f"c{y}")
              for y in list(range(2820, 2749, -1))}
CENSUS_EXPECT = {
    "c2820": 0, "c2819": 4, "c2818": 14, "c2817": 42, "c2816": 88, "c2815": 89,
    "c2814": 84, "c2813": 95, "c2812": 88, "c2811": 91, "c2810": 112, "c2809": 91,
    "c2808": 103, "c2807": 92, "c2806": 88, "c2805": 103, "c2804": 115, "c2803": 121,
    "c2802": 133, "c2801": 101, "c2800": 150, "c2799": 106, "c2798": 104, "c2797": 96,
    "c2796": 106, "c2795": 129, "c2794": 123, "c2793": 131, "c2792": 136, "c2791": 124,
    "c2790": 137, "c2789": 127, "c2788": 138, "c2787": 139, "c2786": 161, "c2785": 143,
    "c2784": 141, "c2783": 142, "c2782": 141, "c2781": 146, "c2780": 151, "c2779": 151,
    "c2778": 195, "c2777": 167, "c2776": 172, "c2775": 181, "c2774": 186, "c2773": 190,
    "c2772": 209, "c2771": 199, "c2770": 259, "c2769": 188, "c2768": 191, "c2767": 274,
    "c2766": 237, "c2765": 182, "c2764": 184, "c2763": 192, "c2762": 229, "c2761": 256,
    "c2760": 187, "c2759": 187, "c2758": 189, "c2757": 192, "c2756": 197, "c2755": 204,
    "c2754": 207, "c2753": 231, "c2752": 237, "c2751": 223, "c2750": 229,
}
c2820_lines = {i + 1: l.count("c2820") for i, l in enumerate(wl.splitlines()) if "c2820" in l}
c2819_lines = {i + 1: l.count("c2819") for i, l in enumerate(wl.splitlines()) if "c2819" in l}
c2818_lines = {i + 1: l.count("c2818") for i, l in enumerate(wl.splitlines()) if "c2818" in l}
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(wl.splitlines()) if "c2817" in l}
guard("c2820_pre==0", CENSUS_PRE["c2820"] == 0 and c2820_lines == {},
      f"got={CENSUS_PRE['c2820']} per-line={c2820_lines} (the forward token "
      f"c2820 is UNBORN pre-append — measured pre-append)")
guard("c2819_pre==4", CENSUS_PRE["c2819"] == 4 and c2819_lines == {9542: 2, 9544: 2},
      f"got={CENSUS_PRE['c2819']} per-line={c2819_lines} (born FOUR: the c2817 Step-7 "
      f"twin-print line 9542 TWICE + TWICE inside the c2817 Next-block — NOT the "
      f"unborn class; the born-FOUR class REPEATS a FIFTEENTH time)")
guard("c2818_pre==14", CENSUS_PRE["c2818"] == 14
      and c2818_lines == {9530: 2, 9532: 2, 9536: 5, 9542: 1, 9544: 4},
      f"got={CENSUS_PRE['c2818']} per-line={c2818_lines} (the MEASURED weight — the "
      f"pre-block state 4 + 10 births inside the c2817 block, the honest note)")
guard("c2817_pre==42", CENSUS_PRE["c2817"] == 42
      and c2817_lines == {9518: 2, 9520: 2, 9524: 4, 9530: 1, 9532: 4, 9535: 1,
                          9536: 8, 9537: 5, 9542: 4, 9544: 11},
      f"got={CENSUS_PRE['c2817']} per-line={c2817_lines} (the MEASURED weight — the "
      f"pre-block state 13 + 29 births inside the c2817 block, the honest note)")
for tag in [f"c{y}" for y in range(2816, 2749, -1)]:
    guard(f"{tag}_pre=={CENSUS_EXPECT[tag]}", CENSUS_PRE[tag] == CENSUS_EXPECT[tag],
          f"got={CENSUS_PRE[tag]}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==495", tid_pre == 495, f"got={tid_pre}")
guard("anchor_nogold_pre==428", gold_pre == 428, f"got={gold_pre}")
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
guard("post_worklog_lines==9556", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2819_next_bullet", last2.startswith("- Next: the c2819 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==496", tid_post == 496, f"got={tid_post}")
guard("anchor_nogold_post==429", gold_post == 429, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2818_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2818")]) == 1)
guard("c2820_mention_birth", wl2.count("c2820") == CENSUS_PRE["c2820"] + block.count("c2820"),
      f"pre={CENSUS_PRE['c2820']} (unborn) + block births={block.count('c2820')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={CENSUS_PRE['c2820'] + block.count('c2820')} got={wl2.count('c2820')}")
for tag in [f"c{y}" for y in range(2819, 2749, -1)]:
    expect = CENSUS_PRE[tag] + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={CENSUS_PRE[tag]} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9544 -> 9556 (+12), c2818 entry + DRIFT-#49 pass-67 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
