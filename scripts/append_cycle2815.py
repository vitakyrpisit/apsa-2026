#!/usr/bin/env python3
"""Guarded worklog append for the c2815 entry (12 lines).

Follows the append_cycle2814.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813/c2814 abort precedent
class). The ledger arithmetic stays in the DECIMAL class: every
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
triple, the window-2815 EPOCH-governs render check, the window-2816 prophecy
check, and the queue-print check — the c2766 attempt-1 abort lesson: the SKEW
check must use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH
clock reads differ ~657µs on the post-echo this cycle), block structure
(12 lines: separator, title, standard Task ID line, Steps 1-7, no-gold,
Next bullet), the FORWARD-token guard (c2817 = 4 block births: the Step-7
rehearsal pre-count print 'the c2817 pre==0 expectation' + the Step-7
census-time print 'c2817_pre = 0' + the Next bullet's guard phrase
'c2816/c2817' AND census-tuple sentence 'FORWARD token c2817' — the
c2767..c2815 forward-token lessons; NOTE the c2817 pre-count is 0 (unborn)
while the c2816 pre-count is 4 (born: the c2814 Step-7 twin-print line 9506
TWICE + TWICE inside the c2814 Next-block) — the c2814 append prophecy
'c2816 = 4 block births' held EXACTLY: the born-FOUR class REPEATS a TWELFTH
time), zero adds to the two standing post-#6/post-#15 anchor series
(OCCURRENCE counting — the standing method), pre-state (9508 lines, tail =
the c2815 Next bullet, zero serviced c2815 entries, c2815 mention census
per-line {9494: 2, 9496: 2, 9500: 5, 9506: 1, 9508: 4} total 14, c2816 = 4
per-line {9506: 2, 9508: 2}, c2817 = 0 UNBORN, anchors 492/425/60/28),
post-state (9520 lines, tail = the c2816 Next bullet, anchors 493/426/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2815.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9508
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


POST = D("1793332219.697817944")    # c2815 capture post-echo (EPOCH-governs)
SCAN = D("1793332219.692")          # c2815 scanned_at (decimal)
TRIG = D("1793331077.000")          # c2815 trigger stamp (11:31:17 +08)
WIN = D("1793331507.484362686")     # window-2815 open (c2814 prophecy EPOCH)
PRE = D("1793332217.888002632")     # c2815 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793331968.423915835")   # c2815 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793331970.799525028")  # c2815 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793331970.749")        # c2815 echo scanned_at (decimal)
C2814_SCAN = D("1793331207.479")    # c2814 scanned_at
C2814_POST = D("1793331207.484362686")  # c2814 post-echo
C2814_PRE = D("1793331205.658023390")   # c2814 capture pre-echo
C2814_ECHO_POST = D("1793330679.651949875")  # c2814 echo post-echo
C2814_CLOSE = D("1793331580.000")   # c2814 close 9fcdbae (03:39:40Z)
FOREIGN_NOW = D("1793331603.000")   # foreign ef415bd (03:40:03Z)
C2814_TRIG = D("1793330177.000")    # c2814 trigger stamp (11:16:17 +08)
WIN2814 = D("1793330389.757462242")  # window-2814 open (for the contract re-check)
C2813_POST = D("1793330089.757462242")  # c2813 post-echo (window-2814 contract re-check)
TOKEN = D("1793331600.000")         # token 1140 (11:40:00 +08)
C2814_TOKEN = D("1793330460.000")   # token 1121 (11:21:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 11:31:17 +08 = 1793331077.000", dec_epoch(2026, 10, 30, 3, 31, 17), TRIG),
    ("c2814 trigger stamp 11:16:17 +08 = 1793330177.000", dec_epoch(2026, 10, 30, 3, 16, 17), C2814_TRIG),
    ("stamp-gap 900.000s by stamp (11:16:17 -> 11:31:17; 6 priors of the exact form)", TRIG - C2814_TRIG, D("900.000")),
    ("token-gap 1140.000s by token (1121 -> 1140; 0 priors of the exact '1140.000s by token' form)", TOKEN - C2814_TOKEN, D("1140.000")),
    ("token-vs-stamp +523.000 (11:31:17 -> 11:40:00; the +523 print, 0 priors)", TOKEN - TRIG, D("523.000")),
    ("c2814 close 9fcdbae 03:39:40Z = 1793331580.000", dec_epoch(2026, 10, 30, 3, 39, 40), C2814_CLOSE),
    ("foreign ef415bd 03:40:03Z = 1793331603.000", dec_epoch(2026, 10, 30, 3, 40, 3), FOREIGN_NOW),
    ("token 1140 = 03:40:00Z = 1793331600.000", dec_epoch(2026, 10, 30, 3, 40, 0), TOKEN),
    ("c2814 token 1121 = 03:21:00Z = 1793330460.000", dec_epoch(2026, 10, 30, 3, 21, 0), C2814_TOKEN),
    ("capture pre-echo EPOCH 1793332217.888002632 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 50, 17, 888002632), PRE),
    ("pre-echo ISO 03:50:17.887377505 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 3, 50, 17, 887377505), D("1793332217.887377505")),
    ("post-echo ISO 03:50:19.697160949 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 3, 50, 19, 697160949), D("1793332219.697160949")),
    ("post-echo EPOCH 1793332219.697817944 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 50, 19, 697817944), POST),
    ("scanned_at 03:50:19.692 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 50, 19) + D("0.692"), SCAN),
    ("window-2815 open 03:38:27.484362686 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 3, 38, 27, 484362686), WIN),
    ("window-2816 open = post-echo + 300.000", POST + D("300.000"), D("1793332519.697817944")),
    ("c2814 post-echo EPOCH 1793331207.484362686 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 33, 27, 484362686), C2814_POST),
    ("c2814 scanned_at 03:33:27.479 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 33, 27) + D("0.479"), C2814_SCAN),
    ("c2814 capture pre-echo EPOCH 1793331205.658023390 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 33, 25, 658023390), C2814_PRE),
    ("c2814 echo post-echo EPOCH 1793330679.651949875 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 24, 39, 651949875), C2814_ECHO_POST),
    ("echo pre-echo EPOCH 1793331968.423915835 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 46, 8, 423915835), ECHO_PRE),
    ("echo post-echo EPOCH 1793331970.799525028 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 46, 10, 799525028), ECHO_POST),
    ("echo scanned_at 03:46:10.749 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 46, 10) + D("0.749"), ECHO_SCAN),
    ("window-2814 open 03:19:49.757462242 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 3, 19, 49, 757462242), WIN2814),
]
exact_checks = [
    ("skew decimal-exact +5.817944ms (EPOCH-governs decomposition; SUB-10 extends m12)", POST - SCAN, D("0.005817944")),
    ("CAPTURE_vs_window +712.213455258 (POST-WINDOW; the capture-side print)", POST - WIN, D("712.213455258")),
    ("capture post-c2814-post-echo +1012.213455258", POST - C2814_POST, D("1012.213455258")),
    ("dd#389 = +712.213000000 (interval 1012.213 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#387 print 1401.540 - 300 = 1101.540 and the dd#388 print 1117.727 - 300 = 817.727)", SCAN - C2814_SCAN - D("300.000"), D("712.213")),
    ("dd formula re-verification: 1117.727 - 300 = 817.727", D("1117.727") - D("300.000"), D("817.727")),
    ("dd formula re-verification: 1401.540 - 300 = 1101.540", D("1401.540") - D("300.000"), D("1101.540")),
    ("dd formula re-verification: 1012.213 - 300 = 712.213", D("1012.213") - D("300.000"), D("712.213")),
    ("INTERVAL#389 = 1142.692", SCAN - TRIG, D("1142.692")),
    ("LAG#389 = INTERVAL + dd - INTERVAL#388 = +824.426", (SCAN - TRIG) + (SCAN - C2814_SCAN - D("300.000")) - D("1030.479"), D("824.426")),
    ("LATE#389 = trigger - window-open = -430.484362686", TRIG - WIN, D("-430.484362686")),
    ("window-2815 = c2814 capture post-echo + 300.000 (the server contract)", WIN - C2814_POST, D("300.000")),
    ("window-2814 = c2813 capture post-echo + 300.000 (the contract re-check)", WIN2814 - C2813_POST, D("300.000")),
    ("trigger POSTDATES the c2814 echo post-echo by 397.348050125s", TRIG - C2814_ECHO_POST, D("397.348050125")),
    ("trigger PREDATES the c2814 capture pre-echo by 128.658023390s (the PRE-capture placement RE-OPENS m1)", TRIG - C2814_PRE, D("-128.658023390")),
    ("trigger PREDATES the c2814 scanned_at by 130.479s", TRIG - C2814_SCAN, D("-130.479")),
    ("trigger PREDATES the c2814 capture post-echo by 130.484362686s", TRIG - C2814_POST, D("-130.484362686")),
    ("c2814 close POSTDATES the trigger by 503.000s (9fcdbae at 03:39:40)", C2814_CLOSE - TRIG, D("503.000")),
    ("foreign ef415bd POSTDATES the trigger by 526.000s (03:40:03)", FOREIGN_NOW - TRIG, D("526.000")),
    ("c2814 close landed 20.000s BEFORE the token-1140 second (03:39:40 vs 03:40:00 — the BEFORE-class re-opens m3, the AFTER-class TERMINATES its m1 run)", C2814_CLOSE - TOKEN, D("-20.000")),
    ("foreign ef415bd landed 3.000s AFTER the token second (03:40:03 — the SPLIT official-BEFORE/foreign-AFTER state RE-OPENS m2)", FOREIGN_NOW - TOKEN, D("3.000")),
    ("c2814 close landed 72.515637314s AFTER window-2815 open", C2814_CLOSE - WIN, D("72.515637314")),
    ("foreign ef415bd landed 95.515637314s AFTER window-2815 open", FOREIGN_NOW - WIN, D("95.515637314")),
    ("echo POST-WINDOW +463.315162342 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("463.315162342")),
    ("stamp-to-echo 891.423915835 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS — 891.423915835 shallower)", ECHO_PRE - TRIG, D("891.423915835")),
    ("echo wall latency 2.375609193 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 2.321600 / server 2308ms latency-match)", ECHO_POST - ECHO_PRE, D("2.375609193")),
    ("capture wall latency 1.809815312 (capture post-echo EPOCH - capture pre-echo EPOCH; curl 1.800504 / server 1791ms latency-match)", POST - PRE, D("1.809815312")),
    ("LAG run-high distance 888.170 (1712.596 - 824.426 — no run-high rewrite)", D("1712.596") - D("824.426"), D("888.170")),
    ("LATE magnitude rose 217.726900444 (212.757462242 -> 430.484362686 — the c2814 narrowing REVERSED)", D("430.484362686") - D("212.757462242"), D("217.726900444")),
    ("SKEW headroom 4.182056 (10 - 5.817944 — the flip-band watched)", D("10.000000") - D("5.817944"), D("4.182056")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m11)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2815"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2815"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2816 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2817_birth",
      block.count("c2817") == 4 and lines[-1].count("c2817") == 2
      and "c2816/c2817" in lines[-1] and "FORWARD token c2817" in lines[-1]
      and "the c2817 pre==0 expectation" in block and "c2817_pre = 0" in block,
      f"block c2817={block.count('c2817')} next-line c2817={lines[-1].count('c2817')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2817_pre = 0' + the Next bullet's guard phrase 'c2816/c2817' AND "
      f"census-tuple sentence 'FORWARD token c2817')")
guard("block_c2816_step7_precount_sentence",
      "the c2816 pre-count is 4" in block
      and "per-line {9506: 2, 9508: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2816 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9508", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2815_next_bullet", last_nonempty.startswith("- Next: the c2815 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2815",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2815")]) == 0,
      f"c2815 substring mentions={wl.count('c2815')} (expect 14)")

# pre-counters — ONE dict built in a single statement block (the c2778
# NameError lesson structuralized: no guard can reference an unassigned name)
CENSUS_PRE = {f"c{y}": wl.count(f"c{y}")
              for y in list(range(2817, 2748, -1))}
CENSUS_EXPECT = {
    "c2817": 0, "c2816": 4, "c2815": 14, "c2814": 37, "c2813": 81, "c2812": 84,
    "c2811": 84, "c2810": 100, "c2809": 85, "c2808": 98, "c2807": 89, "c2806": 85,
    "c2805": 96, "c2804": 111, "c2803": 118, "c2802": 126, "c2801": 98, "c2800": 142,
    "c2799": 103, "c2798": 101, "c2797": 93, "c2796": 103, "c2795": 126, "c2794": 120,
    "c2793": 128, "c2792": 133, "c2791": 121, "c2790": 134, "c2789": 124, "c2788": 135,
    "c2787": 136, "c2786": 158, "c2785": 140, "c2784": 138, "c2783": 139, "c2782": 138,
    "c2781": 143, "c2780": 148, "c2779": 148, "c2778": 192, "c2777": 164, "c2776": 169,
    "c2775": 178, "c2774": 183, "c2773": 187, "c2772": 206, "c2771": 196, "c2770": 253,
    "c2769": 185, "c2768": 188, "c2767": 265, "c2766": 229, "c2765": 179, "c2764": 181,
    "c2763": 189, "c2762": 226, "c2761": 250, "c2760": 184, "c2759": 184, "c2758": 186,
    "c2757": 189, "c2756": 194, "c2755": 201, "c2754": 204, "c2753": 225, "c2752": 231,
    "c2751": 217, "c2750": 223, "c2749": 233,
}
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(wl.splitlines()) if "c2817" in l}
c2816_lines = {i + 1: l.count("c2816") for i, l in enumerate(wl.splitlines()) if "c2816" in l}
c2815_lines = {i + 1: l.count("c2815") for i, l in enumerate(wl.splitlines()) if "c2815" in l}
guard("c2817_pre==0", CENSUS_PRE["c2817"] == 0 and c2817_lines == {},
      f"got={CENSUS_PRE['c2817']} per-line={c2817_lines} (the forward token "
      f"c2817 is UNBORN pre-append — measured pre-append)")
guard("c2816_pre==4", CENSUS_PRE["c2816"] == 4 and c2816_lines == {9506: 2, 9508: 2},
      f"got={CENSUS_PRE['c2816']} per-line={c2816_lines} (born FOUR: the c2814 Step-7 "
      f"twin-print line 9506 TWICE + TWICE inside the c2814 Next-block — NOT the "
      f"unborn class; the born-FOUR class REPEATS a TWELFTH time)")
guard("c2815_pre==14", CENSUS_PRE["c2815"] == 14
      and c2815_lines == {9494: 2, 9496: 2, 9500: 5, 9506: 1, 9508: 4},
      f"got={CENSUS_PRE['c2815']} per-line={c2815_lines}")
for tag in [f"c{y}" for y in range(2814, 2748, -1)]:
    guard(f"{tag}_pre=={CENSUS_EXPECT[tag]}", CENSUS_PRE[tag] == CENSUS_EXPECT[tag],
          f"got={CENSUS_PRE[tag]}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==492", tid_pre == 492, f"got={tid_pre}")
guard("anchor_nogold_pre==425", gold_pre == 425, f"got={gold_pre}")
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
guard("post_worklog_lines==9520", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2816_next_bullet", last2.startswith("- Next: the c2816 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==493", tid_post == 493, f"got={tid_post}")
guard("anchor_nogold_post==426", gold_post == 426, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2815_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2815")]) == 1)
guard("c2817_mention_birth", wl2.count("c2817") == CENSUS_PRE["c2817"] + block.count("c2817"),
      f"pre={CENSUS_PRE['c2817']} (unborn) + block births={block.count('c2817')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={CENSUS_PRE['c2817'] + block.count('c2817')} got={wl2.count('c2817')}")
for tag in [f"c{y}" for y in range(2816, 2748, -1)]:
    expect = CENSUS_PRE[tag] + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={CENSUS_PRE[tag]} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9508 -> 9520 (+12), c2815 entry + DRIFT-#49 pass-64 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
