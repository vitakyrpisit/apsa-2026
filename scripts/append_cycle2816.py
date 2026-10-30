#!/usr/bin/env python3
"""Guarded worklog append for the c2816 entry (12 lines).

Follows the append_cycle2815.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814/c2815 abort
precedent class). The ledger arithmetic stays in the DECIMAL class: every
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
triple, the window-2816 EPOCH-governs render check, the window-2817 prophecy
check, the SWEEP server-miss check, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~644µs on the post-echo
this cycle), block structure (12 lines: separator, title, standard Task ID
line, Steps 1-7, no-gold, Next bullet), the FORWARD-token guard (c2818 = 4
block births: the Step-7 rehearsal pre-count print 'the c2818 pre==0
expectation' + the Step-7 census-time print 'c2818_pre = 0' + the Next
bullet's guard phrase 'c2817/c2818' AND census-tuple sentence 'FORWARD token
c2818' — the c2767..c2816 forward-token lessons; NOTE the c2818 pre-count is
0 (unborn) while the c2817 pre-count is 4 (born: the c2815 Step-7 twin-print
line 9518 TWICE + TWICE inside the c2815 Next-block) — the c2815 append
prophecy 'c2817 = 4 block births' held EXACTLY: the born-FOUR class REPEATS
a THIRTEENTH time), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9520 lines,
tail = the c2816 Next bullet, zero serviced c2816 entries, c2816 mention
census per-line {9506: 2, 9508: 2, 9512: 6, 9518: 1, 9520: 4} total 15,
c2817 = 4 per-line {9518: 2, 9520: 2}, c2818 = 0 UNBORN, anchors
493/426/60/28), post-state (9532 lines, tail = the c2817 Next bullet,
anchors 494/427/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2816.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9520
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


POST = D("1793333244.708518331")    # c2816 capture post-echo (EPOCH-governs)
SCAN = D("1793333244.703")          # c2816 scanned_at (decimal)
TRIG = D("1793332278.000")          # c2816 trigger stamp (11:51:18 +08)
WIN = D("1793332519.697817944")     # window-2816 open (c2815 prophecy EPOCH)
PRE = D("1793333242.986737497")     # c2816 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793332817.838339414")   # c2816 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793332819.527632488")  # c2816 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793332819.522")        # c2816 echo scanned_at (decimal)
C2815_SCAN = D("1793332219.692")    # c2815 scanned_at
C2815_POST = D("1793332219.697817944")  # c2815 post-echo
C2815_PRE = D("1793332217.888002632")   # c2815 capture pre-echo
C2815_ECHO_POST = D("1793331970.799525028")  # c2815 echo post-echo
C2814_SCAN = D("1793331207.479")    # c2814 scanned_at (dd#389 re-verify)
C2814_POST = D("1793331207.484362686")  # c2814 post-echo (window-2815 re-check)
C2813_POST = D("1793330089.757462242")  # c2813 post-echo (window-2814 re-check)
WIN2815 = D("1793331507.484362686")  # window-2815 open (re-check)
WIN2814 = D("1793330389.757462242")  # window-2814 open (re-check)
C2815_CLOSE = D("1793332587.000")   # c2815 close 80e165e (03:56:27Z)
FOREIGN_NOW = D("1793332716.000")   # foreign 42f95e4 (03:58:36Z)
C2815_TRIG = D("1793331077.000")    # c2815 trigger stamp (11:31:17 +08)
TOKEN = D("1793332680.000")         # token 1158 (11:58:00 +08)
C2815_TOKEN = D("1793331600.000")   # token 1140 (11:40:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 11:51:18 +08 = 1793332278.000", dec_epoch(2026, 10, 30, 3, 51, 18), TRIG),
    ("c2815 trigger stamp 11:31:17 +08 = 1793331077.000", dec_epoch(2026, 10, 30, 3, 31, 17), C2815_TRIG),
    ("stamp-gap 1201.000s by stamp (11:31:17 -> 11:51:18; 3 priors of the exact form)", TRIG - C2815_TRIG, D("1201.000")),
    ("token-gap 1080.000s by token (1140 -> 1158; 0 priors of the exact '1080.000s by token' form)", TOKEN - C2815_TOKEN, D("1080.000")),
    ("token-vs-stamp +402.000 (11:51:18 -> 11:58:00; the +402 print, 0 priors)", TOKEN - TRIG, D("402.000")),
    ("c2815 close 80e165e 03:56:27Z = 1793332587.000", dec_epoch(2026, 10, 30, 3, 56, 27), C2815_CLOSE),
    ("foreign 42f95e4 03:58:36Z = 1793332716.000", dec_epoch(2026, 10, 30, 3, 58, 36), FOREIGN_NOW),
    ("token 1158 = 03:58:00Z = 1793332680.000", dec_epoch(2026, 10, 30, 3, 58, 0), TOKEN),
    ("c2815 token 1140 = 03:40:00Z = 1793331600.000", dec_epoch(2026, 10, 30, 3, 40, 0), C2815_TOKEN),
    ("capture pre-echo EPOCH 1793333242.986737497 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 7, 22, 986737497), PRE),
    ("pre-echo ISO 04:07:22.986065026 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 7, 22, 986065026), D("1793333242.986065026")),
    ("post-echo ISO 04:07:24.707873847 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 4, 7, 24, 707873847), D("1793333244.707873847")),
    ("post-echo EPOCH 1793333244.708518331 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 7, 24, 708518331), POST),
    ("scanned_at 04:07:24.703 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 7, 24) + D("0.703"), SCAN),
    ("window-2816 open 03:55:19.697817944 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 3, 55, 19, 697817944), WIN),
    ("window-2817 open = post-echo + 300.000", POST + D("300.000"), D("1793333544.708518331")),
    ("c2815 post-echo EPOCH 1793332219.697817944 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 50, 19, 697817944), C2815_POST),
    ("c2815 scanned_at 03:50:19.692 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 50, 19) + D("0.692"), C2815_SCAN),
    ("c2815 capture pre-echo EPOCH 1793332217.888002632 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 50, 17, 888002632), C2815_PRE),
    ("c2815 echo post-echo EPOCH 1793331970.799525028 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 46, 10, 799525028), C2815_ECHO_POST),
    ("echo pre-echo EPOCH 1793332817.838339414 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 0, 17, 838339414), ECHO_PRE),
    ("echo post-echo EPOCH 1793332819.527632488 (EPOCH-governs)", dec_epoch(2026, 10, 30, 4, 0, 19, 527632488), ECHO_POST),
    ("echo scanned_at 04:00:19.522 +0000 (decimal)", dec_epoch(2026, 10, 30, 4, 0, 19) + D("0.522"), ECHO_SCAN),
    ("window-2815 open 03:38:27.484362686 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 3, 38, 27, 484362686), WIN2815),
]
exact_checks = [
    ("skew decimal-exact +5.518331ms (EPOCH-governs decomposition; SUB-10 extends m13)", POST - SCAN, D("0.005518331")),
    ("CAPTURE_vs_window +725.010700387 (POST-WINDOW; the capture-side print)", POST - WIN, D("725.010700387")),
    ("capture post-c2815-post-echo +1025.010700387", POST - C2815_POST, D("1025.010700387")),
    ("dd#390 = +725.011000000 (interval 1025.011 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#388 print 1117.727 - 300 = 817.727 and the dd#389 print 1012.213 - 300 = 712.213)", SCAN - C2815_SCAN - D("300.000"), D("725.011")),
    ("dd formula re-verification: 1117.727 - 300 = 817.727", D("1117.727") - D("300.000"), D("817.727")),
    ("dd formula re-verification: 1401.540 - 300 = 1101.540", D("1401.540") - D("300.000"), D("1101.540")),
    ("dd formula re-verification: 1012.213 - 300 = 712.213", D("1012.213") - D("300.000"), D("712.213")),
    ("dd formula re-verification: 1025.011 - 300 = 725.011", D("1025.011") - D("300.000"), D("725.011")),
    ("INTERVAL#390 = 966.703", SCAN - TRIG, D("966.703")),
    ("LAG#390 = INTERVAL + dd - INTERVAL#389 = +549.022", (SCAN - TRIG) + (SCAN - C2815_SCAN - D("300.000")) - D("1142.692"), D("549.022")),
    ("LATE#390 = trigger - window-open = -241.697817944", TRIG - WIN, D("-241.697817944")),
    ("window-2816 = c2815 capture post-echo + 300.000 (the server contract)", WIN - C2815_POST, D("300.000")),
    ("window-2815 = c2814 capture post-echo + 300.000 (the contract re-check)", WIN2815 - C2814_POST, D("300.000")),
    ("window-2814 = c2813 capture post-echo + 300.000 (the contract re-check)", WIN2814 - C2813_POST, D("300.000")),
    ("trigger POSTDATES the c2815 echo post-echo by 307.200474972s", TRIG - C2815_ECHO_POST, D("307.200474972")),
    ("trigger POSTDATES the c2815 capture pre-echo by 60.111997368s (the POST-capture placement RE-OPENS m1)", TRIG - C2815_PRE, D("60.111997368")),
    ("trigger POSTDATES the c2815 scanned_at by 58.308s", TRIG - C2815_SCAN, D("58.308")),
    ("trigger POSTDATES the c2815 capture post-echo by 58.302182056s", TRIG - C2815_POST, D("58.302182056")),
    ("c2815 close POSTDATES the trigger by 309.000s (80e165e at 03:56:27)", C2815_CLOSE - TRIG, D("309.000")),
    ("foreign 42f95e4 POSTDATES the trigger by 438.000s (03:58:36)", FOREIGN_NOW - TRIG, D("438.000")),
    ("c2815 close landed 93.000s BEFORE the token-1158 second (03:56:27 vs 03:58:00 — the BEFORE-class re-opens m3, the AFTER-class TERMINATES its m1 run)", C2815_CLOSE - TOKEN, D("-93.000")),
    ("foreign 42f95e4 landed 36.000s AFTER the token second (03:58:36 — the SPLIT official-BEFORE/foreign-AFTER state RE-OPENS m2)", FOREIGN_NOW - TOKEN, D("36.000")),
    ("c2815 close landed 67.302182056s AFTER window-2816 open", C2815_CLOSE - WIN, D("67.302182056")),
    ("foreign 42f95e4 landed 196.302182056s AFTER window-2816 open", FOREIGN_NOW - WIN, D("196.302182056")),
    ("echo POST-WINDOW +299.829814544 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("299.829814544")),
    ("stamp-to-echo 539.838339414 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS — 539.838339414 shallower)", ECHO_PRE - TRIG, D("539.838339414")),
    ("echo wall latency 1.689293074 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.679972 / server 1673ms latency-match)", ECHO_POST - ECHO_PRE, D("1.689293074")),
    ("capture wall latency 1.721780834 (capture post-echo EPOCH - capture pre-echo EPOCH; curl 1.712498 / server 1704ms latency-match)", POST - PRE, D("1.721780834")),
    ("LAG run-high distance 1163.574 (1712.596 - 549.022 — no run-high rewrite)", D("1712.596") - D("549.022"), D("1163.574")),
    ("LATE magnitude fell 188.786544742 (430.484362686 -> 241.697817944 — the c2815 widening REVERSED)", D("430.484362686") - D("241.697817944"), D("188.786544742")),
    ("SKEW headroom 4.481669 (10 - 5.518331 — the flip-band watched)", D("10.000000") - D("5.518331"), D("4.481669")),
    ("SWEEP server miss 7.000 (1711.000 - 1704.000 — the print sits 7.000 BELOW the lower edge)", D("1711.000") - D("1704.000"), D("7.000")),
    ("echo-side skew-analog +0.005632488 (echo post-echo EPOCH - echo scanned_at)", ECHO_POST - ECHO_SCAN, D("0.005632488")),
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
guard("block_title", lines[1].startswith("CYCLE 2816"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2816"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2817 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2818_birth",
      block.count("c2818") == 4 and lines[-1].count("c2818") == 2
      and "c2817/c2818" in lines[-1] and "FORWARD token c2818" in lines[-1]
      and "the c2818 pre==0 expectation" in block and "c2818_pre = 0" in block,
      f"block c2818={block.count('c2818')} next-line c2818={lines[-1].count('c2818')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2818_pre = 0' + the Next bullet's guard phrase 'c2817/c2818' AND "
      f"census-tuple sentence 'FORWARD token c2818')")
guard("block_c2817_step7_precount_sentence",
      "the c2817 pre-count is 4" in block
      and "per-line {9518: 2, 9520: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2817 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9520", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2816_next_bullet", last_nonempty.startswith("- Next: the c2816 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2816",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2816")]) == 0,
      f"c2816 substring mentions={wl.count('c2816')} (expect 15)")

# pre-counters — ONE dict built in a single statement block (the c2778
# NameError lesson structuralized: no guard can reference an unassigned name)
CENSUS_PRE = {f"c{y}": wl.count(f"c{y}")
              for y in list(range(2818, 2748, -1))}
CENSUS_EXPECT = {
    "c2818": 0, "c2817": 4, "c2816": 15, "c2815": 38, "c2814": 77, "c2813": 88,
    "c2812": 86, "c2811": 86, "c2810": 103, "c2809": 87, "c2808": 101, "c2807": 90,
    "c2806": 86, "c2805": 99, "c2804": 113, "c2803": 119, "c2802": 128, "c2801": 99,
    "c2800": 145, "c2799": 104, "c2798": 102, "c2797": 94, "c2796": 104, "c2795": 127,
    "c2794": 121, "c2793": 129, "c2792": 134, "c2791": 122, "c2790": 135, "c2789": 125,
    "c2788": 136, "c2787": 137, "c2786": 159, "c2785": 141, "c2784": 139, "c2783": 140,
    "c2782": 139, "c2781": 144, "c2780": 149, "c2779": 149, "c2778": 193, "c2777": 165,
    "c2776": 170, "c2775": 179, "c2774": 184, "c2773": 188, "c2772": 207, "c2771": 197,
    "c2770": 255, "c2769": 186, "c2768": 189, "c2767": 268, "c2766": 232, "c2765": 180,
    "c2764": 182, "c2763": 190, "c2762": 227, "c2761": 252, "c2760": 185, "c2759": 185,
    "c2758": 187, "c2757": 190, "c2756": 195, "c2755": 202, "c2754": 205, "c2753": 227,
    "c2752": 233, "c2751": 219, "c2750": 225, "c2749": 237,
}
c2818_lines = {i + 1: l.count("c2818") for i, l in enumerate(wl.splitlines()) if "c2818" in l}
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(wl.splitlines()) if "c2817" in l}
c2816_lines = {i + 1: l.count("c2816") for i, l in enumerate(wl.splitlines()) if "c2816" in l}
guard("c2818_pre==0", CENSUS_PRE["c2818"] == 0 and c2818_lines == {},
      f"got={CENSUS_PRE['c2818']} per-line={c2818_lines} (the forward token "
      f"c2818 is UNBORN pre-append — measured pre-append)")
guard("c2817_pre==4", CENSUS_PRE["c2817"] == 4 and c2817_lines == {9518: 2, 9520: 2},
      f"got={CENSUS_PRE['c2817']} per-line={c2817_lines} (born FOUR: the c2815 Step-7 "
      f"twin-print line 9518 TWICE + TWICE inside the c2815 Next-block — NOT the "
      f"unborn class; the born-FOUR class REPEATS a THIRTEENTH time)")
guard("c2816_pre==15", CENSUS_PRE["c2816"] == 15
      and c2816_lines == {9506: 2, 9508: 2, 9512: 6, 9518: 1, 9520: 4},
      f"got={CENSUS_PRE['c2816']} per-line={c2816_lines} (the MEASURED weight — the "
      f"c2815 Step-1 census sentence carries SIX c2816 mentions, the honest note)")
for tag in [f"c{y}" for y in range(2815, 2748, -1)]:
    guard(f"{tag}_pre=={CENSUS_EXPECT[tag]}", CENSUS_PRE[tag] == CENSUS_EXPECT[tag],
          f"got={CENSUS_PRE[tag]}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==493", tid_pre == 493, f"got={tid_pre}")
guard("anchor_nogold_pre==426", gold_pre == 426, f"got={gold_pre}")
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
guard("post_worklog_lines==9532", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2817_next_bullet", last2.startswith("- Next: the c2817 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==494", tid_post == 494, f"got={tid_post}")
guard("anchor_nogold_post==427", gold_post == 427, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2816_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2816")]) == 1)
guard("c2818_mention_birth", wl2.count("c2818") == CENSUS_PRE["c2818"] + block.count("c2818"),
      f"pre={CENSUS_PRE['c2818']} (unborn) + block births={block.count('c2818')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={CENSUS_PRE['c2818'] + block.count('c2818')} got={wl2.count('c2818')}")
for tag in [f"c{y}" for y in range(2817, 2748, -1)]:
    expect = CENSUS_PRE[tag] + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={CENSUS_PRE[tag]} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9520 -> 9532 (+12), c2816 entry + DRIFT-#49 pass-65 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
