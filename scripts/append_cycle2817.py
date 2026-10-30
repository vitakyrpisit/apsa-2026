#!/usr/bin/env python3
"""Guarded worklog append for the c2817 entry (12 lines).

Follows the append_cycle2816.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815/c2816
abort precedent class). The ledger arithmetic stays in the DECIMAL class: every
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
triple, the window-2817 EPOCH-governs render check, the window-2818 prophecy
check, the SWEEP double-miss check, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~656µs on the post-echo
this cycle), block structure (12 lines: separator, title, standard Task ID
line, Steps 1-7, no-gold, Next bullet), the FORWARD-token guard (c2819 = 4
block births: the Step-7 rehearsal pre-count print 'the c2819 pre==0
expectation' + the Step-7 census-time print 'c2819_pre = 0' + the Next
bullet's guard phrase 'c2818/c2819' AND census-tuple sentence 'FORWARD token
c2819' — the c2767..c2817 forward-token lessons; NOTE the c2819 pre-count is
0 (unborn) while the c2818 pre-count is 4 (born: the c2816 Step-7 twin-print
line 9530 TWICE + TWICE inside the c2816 Next-block) — the c2816 append
prophecy 'c2818 = 4 block births' held EXACTLY: the born-FOUR class REPEATS
a FOURTEENTH time), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9532 lines,
tail = the c2817 Next bullet, zero serviced c2817 entries, c2817 mention
census per-line {9518: 2, 9520: 2, 9524: 4, 9530: 1, 9532: 4} total 13,
c2818 = 4 per-line {9530: 2, 9532: 2}, c2819 = 0 UNBORN, anchors
494/427/60/28), post-state (9544 lines, tail = the c2818 Next bullet,
anchors 495/428/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2817.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9532
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


POST = D("1793334101.674751215")    # c2817 capture post-echo (EPOCH-governs)
SCAN = D("1793334101.669")          # c2817 scanned_at (decimal)
TRIG = D("1793333178.000")          # c2817 trigger stamp (12:06:18 +08)
WIN = D("1793333544.708518331")     # window-2817 open (c2816 prophecy EPOCH)
PRE = D("1793334100.184672197")     # c2817 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793333826.556031485")   # c2817 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793333828.255033591")  # c2817 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793333828.249")        # c2817 echo scanned_at (decimal)
C2816_SCAN = D("1793333244.703")    # c2816 scanned_at
C2816_POST = D("1793333244.708518331")  # c2816 post-echo
C2816_PRE = D("1793333242.986737497")   # c2816 capture pre-echo
C2816_ECHO_POST = D("1793332819.527632488")  # c2816 echo post-echo
C2815_POST = D("1793332219.697817944")  # c2815 post-echo (window-2816 re-check)
WIN2816 = D("1793332519.697817944")  # window-2816 open (re-check)
C2816_CLOSE = D("1793333577.000")   # c2816 close f3695b7 (04:12:57Z)
FOREIGN_NOW = D("1793333595.000")   # foreign 68117e3 (04:13:15Z)
C2816_TRIG = D("1793332278.000")    # c2816 trigger stamp (11:51:18 +08)
TOKEN = D("1793333580.000")         # token 1213 (12:13:00 +08)
C2816_TOKEN = D("1793332680.000")   # token 1158 (11:58:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 12:06:18 +08 = 1793333178.000", dec_epoch(2026, 10, 30, 4, 6, 18), TRIG),
    ("c2816 trigger stamp 11:51:18 +08 = 1793332278.000", dec_epoch(2026, 10, 30, 3, 51, 18), C2816_TRIG),
    ("stamp-gap 900.000s by stamp (11:51:18 -> 12:06:18; 9 priors of the exact form)", TRIG - C2816_TRIG, D("900.000")),
    ("token-gap 900.000s by token (1158 -> 1213; 2 priors of the exact '900.000s by token' form)", TOKEN - C2816_TOKEN, D("900.000")),
    ("token-vs-stamp +402.000 (12:06:18 -> 12:13:00; the +402 print, 1 prior)", TOKEN - TRIG, D("402.000")),
    ("c2816 close f3695b7 04:12:57Z = 1793333577.000", dec_epoch(2026, 10, 30, 4, 12, 57), C2816_CLOSE),
    ("foreign 68117e3 04:13:15Z = 1793333595.000", dec_epoch(2026, 10, 30, 4, 13, 15), FOREIGN_NOW),
    ("token 1213 = 04:13:00Z = 1793333580.000", dec_epoch(2026, 10, 30, 4, 13, 0), TOKEN),
    ("c2816 token 1158 = 03:58:00Z = 1793332680.000", dec_epoch(2026, 10, 30, 3, 58, 0), C2816_TOKEN),
    ("capture pre-echo EPOCH 1793334100.184672197 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 21, 40, 184672197), PRE),
    ("pre-echo ISO 04:21:40.183933200 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 21, 40, 183933200), D("1793334100.183933200")),
    ("post-echo ISO 04:21:41.674095031 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 21, 41, 674095031), D("1793334101.674095031")),
    ("post-echo EPOCH 1793334101.674751215 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 21, 41, 674751215), POST),
    ("scanned_at 04:21:41.669 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 21, 41) + D("0.669"), SCAN),
    ("window-2817 open 04:12:24.708518331 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 4, 12, 24, 708518331), WIN),
    ("window-2818 open = post-echo + 300.000", POST + D("300.000"), D("1793334401.674751215")),
    ("c2816 post-echo EPOCH 1793333244.708518331 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 7, 24, 708518331), C2816_POST),
    ("c2816 scanned_at 04:07:24.703 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 7, 24) + D("0.703"), C2816_SCAN),
    ("c2816 capture pre-echo EPOCH 1793333242.986737497 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 7, 22, 986737497), C2816_PRE),
    ("c2816 echo post-echo EPOCH 1793332819.527632488 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 0, 19, 527632488), C2816_ECHO_POST),
    ("echo pre-echo EPOCH 1793333826.556031485 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 17, 6, 556031485), ECHO_PRE),
    ("echo post-echo EPOCH 1793333828.255033591 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 17, 8, 255033591), ECHO_POST),
    ("echo scanned_at 04:17:08.249 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 17, 8) + D("0.249"), ECHO_SCAN),
    ("window-2816 open 03:55:19.697817944 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 3, 55, 19, 697817944), WIN2816),
]
exact_checks = [
    ("skew decimal-exact +5.751215ms (EPOCH-governs decomposition; SUB-10 extends m14)", POST - SCAN, D("0.005751215")),
    ("CAPTURE_vs_window +556.966232884 (POST-WINDOW; the capture-side print)", POST - WIN, D("556.966232884")),
    ("capture post-c2816-post-echo +856.966232884", POST - C2816_POST, D("856.966232884")),
    ("dd#391 = +556.966000000 (interval 856.966 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#389 print 1012.213 - 300 = 712.213 and the dd#390 print 1025.011 - 300 = 725.011)", SCAN - C2816_SCAN - D("300.000"), D("556.966")),
    ("dd formula re-verification: 1117.727 - 300 = 817.727", D("1117.727") - D("300.000"), D("817.727")),
    ("dd formula re-verification: 1401.540 - 300 = 1101.540", D("1401.540") - D("300.000"), D("1101.540")),
    ("dd formula re-verification: 1012.213 - 300 = 712.213", D("1012.213") - D("300.000"), D("712.213")),
    ("dd formula re-verification: 1025.011 - 300 = 725.011", D("1025.011") - D("300.000"), D("725.011")),
    ("dd formula re-verification: 856.966 - 300 = 556.966", D("856.966") - D("300.000"), D("556.966")),
    ("INTERVAL#391 = 923.669", SCAN - TRIG, D("923.669")),
    ("LAG#391 = INTERVAL + dd - INTERVAL#390 = +513.932", (SCAN - TRIG) + (SCAN - C2816_SCAN - D("300.000")) - D("966.703"), D("513.932")),
    ("LATE#391 = trigger - window-open = -366.708518331", TRIG - WIN, D("-366.708518331")),
    ("window-2817 = c2816 capture post-echo + 300.000 (the server contract)", WIN - C2816_POST, D("300.000")),
    ("window-2816 = c2815 capture post-echo + 300.000 (the contract re-check)", WIN2816 - C2815_POST, D("300.000")),
    ("trigger POSTDATES the c2816 echo post-echo by 358.472367512s", TRIG - C2816_ECHO_POST, D("358.472367512")),
    ("trigger PREDATES the c2816 capture pre-echo by 64.986737497s (the PRE-capture placement RE-OPENS m1)", C2816_PRE - TRIG, D("64.986737497")),
    ("trigger PREDATES the c2816 scanned_at by 66.703s", C2816_SCAN - TRIG, D("66.703")),
    ("trigger PREDATES the c2816 capture post-echo by 66.708518331s", C2816_POST - TRIG, D("66.708518331")),
    ("c2816 close POSTDATES the trigger by 399.000s (f3695b7 at 04:12:57)", C2816_CLOSE - TRIG, D("399.000")),
    ("foreign 68117e3 POSTDATES the trigger by 417.000s (04:13:15)", FOREIGN_NOW - TRIG, D("417.000")),
    ("c2816 close landed 3.000s BEFORE the token-1213 second (04:12:57 vs 04:13:00 — the BEFORE-class re-opens m3, the AFTER-class TERMINATES its m1 run)", TOKEN - C2816_CLOSE, D("3.000")),
    ("foreign 68117e3 landed 15.000s AFTER the token second (04:13:15 — the SPLIT official-BEFORE/foreign-AFTER state RE-OPENS m2)", FOREIGN_NOW - TOKEN, D("15.000")),
    ("c2816 close landed 32.291481669s AFTER window-2817 open", C2816_CLOSE - WIN, D("32.291481669")),
    ("foreign 68117e3 landed 50.291481669s AFTER window-2817 open", FOREIGN_NOW - WIN, D("50.291481669")),
    ("echo POST-WINDOW +283.546515260 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("283.546515260")),
    ("stamp-to-echo 648.556031485 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS — 648.556031485 shallower)", ECHO_PRE - TRIG, D("648.556031485")),
    ("stamp-to-capture-pre 922.184672197 (the capture pre-echo EPOCH minus the trigger)", PRE - TRIG, D("922.184672197")),
    ("echo wall latency 1.699002106 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.690023 / server 1683ms latency-match)", ECHO_POST - ECHO_PRE, D("1.699002106")),
    ("capture wall latency 1.490079018 (capture post-echo EPOCH - capture pre-echo EPOCH; curl 1.479770 / server 1472ms latency-match)", POST - PRE, D("1.490079018")),
    ("LAG run-high distance 1198.664 (1712.596 - 513.932 — no run-high rewrite)", D("1712.596") - D("513.932"), D("1198.664")),
    ("LATE magnitude grew 125.010700387 (241.697817944 -> 366.708518331 — the c2816 narrowing REVERSED)", D("366.708518331") - D("241.697817944"), D("125.010700387")),
    ("SKEW headroom 4.248785 (10 - 5.751215 — the flip-band watched)", D("10.000000") - D("5.751215"), D("4.248785")),
    ("SWEEP client miss 0.112728 (1.592498 - 1.479770 — the print sits BELOW the lower edge)", D("1.592498") - D("1.479770"), D("0.112728")),
    ("SWEEP server miss 152.000 (1624.000 - 1472.000 — the print sits BELOW the lower edge)", D("1624.000") - D("1472.000"), D("152.000")),
    ("echo-side skew-analog +0.006033591 (echo post-echo EPOCH - echo scanned_at)", ECHO_POST - ECHO_SCAN, D("0.006033591")),
    ("DRAIN miss 7.586241212 (564.552241212 - 556.966 — the print sits BELOW the dd lower edge)", D("564.552241212") - D("556.966"), D("7.586241212")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m12)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2817"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2817"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2818 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2819_birth",
      block.count("c2819") == 4 and lines[-1].count("c2819") == 2
      and "c2818/c2819" in lines[-1] and "FORWARD token c2819" in lines[-1]
      and "the c2819 pre==0 expectation" in block and "c2819_pre = 0" in block,
      f"block c2819={block.count('c2819')} next-line c2819={lines[-1].count('c2819')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2819_pre = 0' + the Next bullet's guard phrase 'c2818/c2819' AND "
      f"census-tuple sentence 'FORWARD token c2819')")
guard("block_c2818_step7_precount_sentence",
      "the c2818 pre-count is 4" in block
      and "per-line {9530: 2, 9532: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2818 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9532", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2817_next_bullet", last_nonempty.startswith("- Next: the c2817 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2817",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2817")]) == 0,
      f"c2817 substring mentions={wl.count('c2817')} (expect 13)")

# pre-counters — ONE dict built in a single statement block (the c2778
# NameError lesson structuralized: no guard can reference an unassigned name)
CENSUS_PRE = {f"c{y}": wl.count(f"c{y}")
              for y in list(range(2819, 2748, -1))}
CENSUS_EXPECT = {
    "c2819": 0, "c2818": 4, "c2817": 13, "c2816": 41, "c2815": 85, "c2814": 82,
    "c2813": 92, "c2812": 87, "c2811": 88, "c2810": 107, "c2809": 90, "c2808": 102,
    "c2807": 91, "c2806": 87, "c2805": 101, "c2804": 114, "c2803": 120, "c2802": 130,
    "c2801": 100, "c2800": 148, "c2799": 105, "c2798": 103, "c2797": 95, "c2796": 105,
    "c2795": 128, "c2794": 122, "c2793": 130, "c2792": 135, "c2791": 123, "c2790": 136,
    "c2789": 126, "c2788": 137, "c2787": 138, "c2786": 160, "c2785": 142, "c2784": 140,
    "c2783": 141, "c2782": 140, "c2781": 145, "c2780": 150, "c2779": 150, "c2778": 194,
    "c2777": 166, "c2776": 171, "c2775": 180, "c2774": 185, "c2773": 189, "c2772": 208,
    "c2771": 198, "c2770": 257, "c2769": 187, "c2768": 190, "c2767": 271, "c2766": 235,
    "c2765": 181, "c2764": 183, "c2763": 191, "c2762": 228, "c2761": 254, "c2760": 186,
    "c2759": 186, "c2758": 188, "c2757": 191, "c2756": 196, "c2755": 203, "c2754": 206,
    "c2753": 229, "c2752": 235, "c2751": 221, "c2750": 227, "c2749": 241,
}
c2819_lines = {i + 1: l.count("c2819") for i, l in enumerate(wl.splitlines()) if "c2819" in l}
c2818_lines = {i + 1: l.count("c2818") for i, l in enumerate(wl.splitlines()) if "c2818" in l}
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(wl.splitlines()) if "c2817" in l}
c2816_lines = {i + 1: l.count("c2816") for i, l in enumerate(wl.splitlines()) if "c2816" in l}
guard("c2819_pre==0", CENSUS_PRE["c2819"] == 0 and c2819_lines == {},
      f"got={CENSUS_PRE['c2819']} per-line={c2819_lines} (the forward token "
      f"c2819 is UNBORN pre-append — measured pre-append)")
guard("c2818_pre==4", CENSUS_PRE["c2818"] == 4 and c2818_lines == {9530: 2, 9532: 2},
      f"got={CENSUS_PRE['c2818']} per-line={c2818_lines} (born FOUR: the c2816 Step-7 "
      f"twin-print line 9530 TWICE + TWICE inside the c2816 Next-block — NOT the "
      f"unborn class; the born-FOUR class REPEATS a FOURTEENTH time)")
guard("c2817_pre==13", CENSUS_PRE["c2817"] == 13
      and c2817_lines == {9518: 2, 9520: 2, 9524: 4, 9530: 1, 9532: 4},
      f"got={CENSUS_PRE['c2817']} per-line={c2817_lines} (the MEASURED weight — the "
      f"pre-block state 4 + 9 births inside the c2816 block, the honest note)")
guard("c2816_pre==41", CENSUS_PRE["c2816"] == 41
      and c2816_lines == {9506: 2, 9508: 2, 9512: 6, 9518: 1, 9520: 4, 9523: 1,
                          9524: 7, 9525: 4, 9530: 4, 9532: 10},
      f"got={CENSUS_PRE['c2816']} per-line={c2816_lines} (the MEASURED weight — the "
      f"pre-block state 15 + 26 births inside the c2816 block, the honest note)")
for tag in [f"c{y}" for y in range(2815, 2748, -1)]:
    guard(f"{tag}_pre=={CENSUS_EXPECT[tag]}", CENSUS_PRE[tag] == CENSUS_EXPECT[tag],
          f"got={CENSUS_PRE[tag]}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==494", tid_pre == 494, f"got={tid_pre}")
guard("anchor_nogold_pre==427", gold_pre == 427, f"got={gold_pre}")
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
guard("post_worklog_lines==9544", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2818_next_bullet", last2.startswith("- Next: the c2818 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==495", tid_post == 495, f"got={tid_post}")
guard("anchor_nogold_post==428", gold_post == 428, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2817_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2817")]) == 1)
guard("c2819_mention_birth", wl2.count("c2819") == CENSUS_PRE["c2819"] + block.count("c2819"),
      f"pre={CENSUS_PRE['c2819']} (unborn) + block births={block.count('c2819')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={CENSUS_PRE['c2819'] + block.count('c2819')} got={wl2.count('c2819')}")
for tag in [f"c{y}" for y in range(2818, 2748, -1)]:
    expect = CENSUS_PRE[tag] + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={CENSUS_PRE[tag]} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9532 -> 9544 (+12), c2817 entry + DRIFT-#49 pass-66 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
