#!/usr/bin/env python3
"""Guarded worklog append for the c2813 entry (12 lines).

Follows the append_cycle2812.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812 abort precedent class). The
ledger arithmetic stays in the DECIMAL class: every ns-decomposition check is
Decimal-exact or Decimal-with-1e-6-tolerance on the utc-derived values. THE
C2778 ABORT LESSON STRUCTURALIZED: the pre-counters are built as ONE dict in
a single statement block before any guard references them (the c2778
attempt-1 NameError class is structurally impossible here), and a REHEARSAL
mode (APPEND_REHEARSAL=1) runs the full guard battery against a
byte-identical temp copy BEFORE the real run — the attempt counter counts
REAL runs only. Guards: python-timegm epoch cross-verification (Decimal-class
checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic, the ECHO
decompositions (pre/post/latency/stamp-to-echo/POST-WINDOW — the echo
RE-DERIVABLE this cycle), the stamp-gap/token-gap/token-vs-stamp cadence
triple, the window-2813 EPOCH-governs render check, the window-2814 prophecy
check, and the queue-print check — the c2766 attempt-1 abort lesson: the SKEW
check must use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH
clock reads differ ~697µs on the post-echo this cycle), block structure
(12 lines: separator, title, standard Task ID line, Steps 1-7, no-gold,
Next bullet), the FORWARD-token guard (c2815 = 4 block births: the Step-7
rehearsal pre-count print 'the c2815 pre==0 expectation' + the Step-7
census-time print 'c2815_pre = 0' + the Next bullet's guard phrase
'c2814/c2815' AND census-tuple sentence 'FORWARD token c2815' — the
c2767..c2813 forward-token lessons; NOTE the c2815 pre-count is 0 (unborn)
while the c2814 pre-count is 4 (born: the c2812 Step-7 twin-print line 9482
TWICE + TWICE inside the c2812 Next-block) — the c2812 append prophecy
'c2814 = 4 block births' held EXACTLY: the born-FOUR class REPEATS a TENTH
time), zero adds to the two standing post-#6/post-#15 anchor series
(OCCURRENCE counting — the standing method), pre-state (9484 lines, tail =
the c2813 Next bullet, zero serviced c2813 entries, c2813 mention census
per-line {9470: 2, 9472: 2, 9476: 5, 9482: 1, 9484: 4} total 14, c2814 = 4
per-line {9482: 2, 9484: 2}, anchors 490/423/60/28), post-state (9496 lines,
tail = the c2814 Next bullet, anchors 491/424/60/28). Zero mid-line writes
(append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2813.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9484
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


POST = D("1793330089.757462242")    # c2813 capture post-echo (EPOCH-governs)
SCAN = D("1793330089.752")          # c2813 scanned_at (decimal)
TRIG = D("1793328677.000")          # c2813 trigger stamp (10:51:17 +08)
WIN = D("1793328988.217915386")     # window-2813 open (c2812 prophecy EPOCH)
PRE = D("1793330088.037175665")     # c2813 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793329671.491053914")   # c2813 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793329673.062755684")  # c2813 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793329673.057")        # c2813 echo scanned_at (decimal)
C2812_SCAN = D("1793328688.212")    # c2812 scanned_at
C2812_POST = D("1793328688.217915386")  # c2812 post-echo
C2812_PRE = D("1793328686.469282375")   # c2812 capture pre-echo
C2812_ECHO_POST = D("1793328410.534691612")  # c2812 echo post-echo
C2812_CLOSE = D("1793329236.000")   # c2812 close fcd7b1c (03:00:36Z)
FOREIGN_NOW = D("1793329264.000")   # foreign 30a3440 (03:01:04Z)
C2812_TRIG = D("1793327477.000")    # c2812 trigger stamp (10:31:17 +08)
WIN2812 = D("1793327526.818599805")  # window-2812 open (for the contract re-check)
TOKEN = D("1793329260.000")         # token 1101 (11:01:00 +08)
C2812_TOKEN = D("1793327940.000")   # token 1039 (10:39:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 10:51:17 +08 = 1793328677.000", dec_epoch(2026, 10, 30, 2, 51, 17), TRIG),
    ("c2812 trigger stamp 10:31:17 +08 = 1793327477.000", dec_epoch(2026, 10, 30, 2, 31, 17), C2812_TRIG),
    ("stamp-gap 1200.000s by stamp (10:31:17 -> 10:51:17; 2 priors of the exact form)", TRIG - C2812_TRIG, D("1200.000")),
    ("token-gap 1320.000s by token (1039 -> 1101; 1 prior of the exact '1320.000s by token' form)", TOKEN - C2812_TOKEN, D("1320.000")),
    ("token-vs-stamp +583.000 (10:51:17 -> 11:01:00; the +583 print, 0 priors)", TOKEN - TRIG, D("583.000")),
    ("c2812 close fcd7b1c 03:00:36Z = 1793329236.000", dec_epoch(2026, 10, 30, 3, 0, 36), C2812_CLOSE),
    ("foreign 30a3440 03:01:04Z = 1793329264.000", dec_epoch(2026, 10, 30, 3, 1, 4), FOREIGN_NOW),
    ("token 1101 = 03:01:00Z = 1793329260.000", dec_epoch(2026, 10, 30, 3, 1, 0), TOKEN),
    ("c2812 token 1039 = 02:39:00Z = 1793327940.000", dec_epoch(2026, 10, 30, 2, 39, 0), C2812_TOKEN),
    ("capture pre-echo EPOCH 1793330088.037175665 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 14, 48, 37175665), PRE),
    ("pre-echo ISO 03:14:48.036435212 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 3, 14, 48, 36435212), D("1793330088.036435212")),
    ("post-echo ISO 03:14:49.756765295 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 3, 14, 49, 756765295), D("1793330089.756765295")),
    ("post-echo EPOCH 1793330089.757462242 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 14, 49, 757462242), POST),
    ("scanned_at 03:14:49.752 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 14, 49) + D("0.752"), SCAN),
    ("window-2813 open 02:56:28.217915386 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 2, 56, 28, 217915386), WIN),
    ("window-2814 open = post-echo + 300.000", POST + D("300.000"), D("1793330389.757462242")),
    ("c2812 post-echo EPOCH 1793328688.217915386 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 51, 28, 217915386), C2812_POST),
    ("c2812 scanned_at 02:51:28.212 +0000 (decimal)", dec_epoch(2026, 10, 30, 2, 51, 28) + D("0.212"), C2812_SCAN),
    ("c2812 capture pre-echo EPOCH 1793328686.469282375 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 51, 26, 469282375), C2812_PRE),
    ("c2812 echo post-echo EPOCH 1793328410.534691612 (EPOCH-governs)", dec_epoch(2026, 10, 30, 2, 46, 50, 534691612), C2812_ECHO_POST),
    ("echo pre-echo EPOCH 1793329671.491053914 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 7, 51, 491053914), ECHO_PRE),
    ("echo post-echo EPOCH 1793329673.062755684 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 7, 53, 62755684), ECHO_POST),
    ("echo scanned_at 03:07:53.057 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 7, 53) + D("0.057"), ECHO_SCAN),
    ("window-2812 open 02:32:06.818599805 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 2, 32, 6, 818599805), WIN2812),
]
exact_checks = [
    ("skew decimal-exact +5.462242ms (EPOCH-governs decomposition; SUB-10 extends m10)", POST - SCAN, D("0.005462242")),
    ("CAPTURE_vs_window +1101.539546856 (POST-WINDOW; the capture-side print)", POST - WIN, D("1101.539546856")),
    ("capture post-c2812-post-echo +1401.539546856", POST - C2812_POST, D("1401.539546856")),
    ("dd#387 = +1101.540000000 (interval 1401.540 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#385 print 960.015 - 300 = 660.015 and the dd#386 print 1461.399 - 300 = 1161.399)", SCAN - C2812_SCAN - D("300.000"), D("1101.540")),
    ("dd formula re-verification: 960.015 - 300 = 660.015", D("960.015") - D("300.000"), D("660.015")),
    ("dd formula re-verification: 1461.399 - 300 = 1161.399", D("1461.399") - D("300.000"), D("1161.399")),
    ("dd formula re-verification: 878.961 - 300 = 578.961", D("878.961") - D("300.000"), D("578.961")),
    ("INTERVAL#387 = 1412.752", SCAN - TRIG, D("1412.752")),
    ("LAG#387 = INTERVAL + dd - dd#386 = +1352.893", (SCAN - TRIG) + (SCAN - C2812_SCAN - D("300.000")) - D("1161.399"), D("1352.893")),
    ("LATE#387 = trigger - window-open = -311.217915386", TRIG - WIN, D("-311.217915386")),
    ("window-2813 = c2812 capture post-echo + 300.000 (the server contract)", WIN - C2812_POST, D("300.000")),
    ("trigger POSTDATES the c2812 echo post-echo by 266.465308388s (the PRE-capture placement NEW)", TRIG - C2812_ECHO_POST, D("266.465308388")),
    ("trigger PREDATES the c2812 capture pre-echo by 9.469282375s", TRIG - C2812_PRE, D("-9.469282375")),
    ("trigger PREDATES the c2812 scanned_at by 11.212s", TRIG - C2812_SCAN, D("-11.212")),
    ("trigger PREDATES the c2812 capture post-echo by 11.217915386s", TRIG - C2812_POST, D("-11.217915386")),
    ("c2812 close POSTDATES the trigger by 559.000s (fcd7b1c at 03:00:36)", C2812_CLOSE - TRIG, D("559.000")),
    ("foreign 30a3440 POSTDATES the trigger by 587.000s (03:01:04)", FOREIGN_NOW - TRIG, D("587.000")),
    ("c2812 close landed 24.000s BEFORE the token-1101 second (03:00:36 vs 03:01:00 — the before-class REPEATS m2)", C2812_CLOSE - TOKEN, D("-24.000")),
    ("foreign 30a3440 landed 4.000s AFTER the token second (03:01:04 — the after-class REPEATS)", FOREIGN_NOW - TOKEN, D("4.000")),
    ("c2812 close landed 247.782084614s AFTER window-2813 open", C2812_CLOSE - WIN, D("247.782084614")),
    ("foreign 30a3440 landed 275.782084614s AFTER window-2813 open", FOREIGN_NOW - WIN, D("275.782084614")),
    ("echo POST-WINDOW +684.844840298 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("684.844840298")),
    ("stamp-to-echo 994.491053914 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS — 994.491053914 shallower)", ECHO_PRE - TRIG, D("994.491053914")),
    ("echo wall latency 1.571701770 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.562345 / server 1556ms latency-match)", ECHO_POST - ECHO_PRE, D("1.571701770")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
guard("echo PREDATED the capture pre-echo (the echo-then-capture order class EXTENDS m10)",
      ECHO_POST < PRE, f"echo_post={ECHO_POST} capture_pre={PRE}")

# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2813"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2813"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2814 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2815_birth",
      block.count("c2815") == 4 and lines[-1].count("c2815") == 2
      and "c2814/c2815" in lines[-1] and "FORWARD token c2815" in lines[-1]
      and "the c2815 pre==0 expectation" in block and "c2815_pre = 0" in block,
      f"block c2815={block.count('c2815')} next-line c2815={lines[-1].count('c2815')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2815_pre = 0' + the Next bullet's guard phrase 'c2814/c2815' AND "
      f"census-tuple sentence 'FORWARD token c2815')")
guard("block_c2814_step7_precount_sentence",
      "the c2814 pre-count is 4" in block
      and "per-line {9482: 2, 9484: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2814 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9484", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2813_next_bullet", last_nonempty.startswith("- Next: the c2813 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2813",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2813")]) == 0,
      f"c2813 substring mentions={wl.count('c2813')} (expect 14)")

# pre-counters — ONE dict built in a single statement block (the c2778
# NameError lesson structuralized: no guard can reference an unassigned name)
CENSUS_PRE = {f"c{y}": wl.count(f"c{y}")
              for y in list(range(2815, 2748, -1))}
CENSUS_EXPECT = {
    "c2815": 0, "c2814": 4, "c2813": 14, "c2812": 37, "c2811": 75, "c2810": 88,
    "c2809": 81, "c2808": 90, "c2807": 87, "c2806": 83, "c2805": 92, "c2804": 107,
    "c2803": 116, "c2802": 122, "c2801": 96, "c2800": 136, "c2799": 101, "c2798": 99,
    "c2797": 91, "c2796": 101, "c2795": 124, "c2794": 118, "c2793": 126, "c2792": 131,
    "c2791": 119, "c2790": 132, "c2789": 122, "c2788": 133, "c2787": 134, "c2786": 156,
    "c2785": 138, "c2784": 136, "c2783": 137, "c2782": 136, "c2781": 141, "c2780": 146,
    "c2779": 146, "c2778": 190, "c2777": 162, "c2776": 167, "c2775": 176, "c2774": 181,
    "c2773": 185, "c2772": 204, "c2771": 194, "c2770": 248, "c2769": 183, "c2768": 186,
    "c2767": 259, "c2766": 225, "c2765": 177, "c2764": 179, "c2763": 187, "c2762": 224,
    "c2761": 246, "c2760": 182, "c2759": 182, "c2758": 184, "c2757": 187, "c2756": 192,
    "c2755": 199, "c2754": 202, "c2753": 221, "c2752": 227, "c2751": 213, "c2750": 219,
    "c2749": 224,
}
c2813_lines = {i + 1: l.count("c2813") for i, l in enumerate(wl.splitlines()) if "c2813" in l}
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(wl.splitlines()) if "c2814" in l}
guard("c2815_pre==0", CENSUS_PRE["c2815"] == 0, f"got={CENSUS_PRE['c2815']} (the forward token "
      f"c2815 is UNBORN pre-append — measured pre-append)")
guard("c2814_pre==4", CENSUS_PRE["c2814"] == 4 and c2814_lines == {9482: 2, 9484: 2},
      f"got={CENSUS_PRE['c2814']} per-line={c2814_lines} (born FOUR: the c2812 Step-7 "
      f"twin-print line 9482 TWICE + TWICE inside the c2812 Next-block — NOT the "
      f"unborn class; the born-FOUR class REPEATS a TENTH time)")
guard("c2813_pre==14", CENSUS_PRE["c2813"] == 14
      and c2813_lines == {9470: 2, 9472: 2, 9476: 5, 9482: 1, 9484: 4},
      f"got={CENSUS_PRE['c2813']} per-line={c2813_lines}")
for tag in [f"c{y}" for y in range(2812, 2748, -1)]:
    guard(f"{tag}_pre=={CENSUS_EXPECT[tag]}", CENSUS_PRE[tag] == CENSUS_EXPECT[tag],
          f"got={CENSUS_PRE[tag]}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==490", tid_pre == 490, f"got={tid_pre}")
guard("anchor_nogold_pre==423", gold_pre == 423, f"got={gold_pre}")
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
guard("post_worklog_lines==9496", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2814_next_bullet", last2.startswith("- Next: the c2814 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==491", tid_post == 491, f"got={tid_post}")
guard("anchor_nogold_post==424", gold_post == 424, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2813_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2813")]) == 1)
guard("c2815_mention_birth", wl2.count("c2815") == CENSUS_PRE["c2815"] + block.count("c2815"),
      f"pre={CENSUS_PRE['c2815']} (unborn) + block births={block.count('c2815')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={CENSUS_PRE['c2815'] + block.count('c2815')} got={wl2.count('c2815')}")
for tag in [f"c{y}" for y in range(2814, 2748, -1)]:
    expect = CENSUS_PRE[tag] + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={CENSUS_PRE[tag]} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9484 -> 9496 (+12), c2813 entry + DRIFT-#49 pass-62 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
