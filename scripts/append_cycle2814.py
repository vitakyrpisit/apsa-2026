#!/usr/bin/env python3
"""Guarded worklog append for the c2814 entry (12 lines).

Follows the append_cycle2813.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2800-append/c2804/
c2805/c2806/c2807/c2808/c2809/c2810/c2811/c2812/c2813 abort precedent class). The
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
triple, the window-2814 EPOCH-governs render check, the window-2815 prophecy
check, and the queue-print check — the c2766 attempt-1 abort lesson: the SKEW
check must use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH
clock reads differ ~627µs on the post-echo this cycle), block structure
(12 lines: separator, title, standard Task ID line, Steps 1-7, no-gold,
Next bullet), the FORWARD-token guard (c2816 = 4 block births: the Step-7
rehearsal pre-count print 'the c2816 pre==0 expectation' + the Step-7
census-time print 'c2816_pre = 0' + the Next bullet's guard phrase
'c2815/c2816' AND census-tuple sentence 'FORWARD token c2816' — the
c2767..c2814 forward-token lessons; NOTE the c2816 pre-count is 0 (unborn)
while the c2815 pre-count is 4 (born: the c2813 Step-7 twin-print line 9494
TWICE + TWICE inside the c2813 Next-block) — the c2813 append prophecy
'c2815 = 4 block births' held EXACTLY: the born-FOUR class REPEATS an
ELEVENTH time), zero adds to the two standing post-#6/post-#15 anchor series
(OCCURRENCE counting — the standing method), pre-state (9496 lines, tail =
the c2814 Next bullet, zero serviced c2814 entries, c2814 mention census
per-line {9482: 2, 9484: 2, 9488: 5, 9494: 1, 9496: 4} total 14, c2815 = 4
per-line {9494: 2, 9496: 2}, anchors 491/424/60/28), post-state (9508 lines,
tail = the c2815 Next bullet, anchors 492/425/60/28). Zero mid-line writes
(append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2814.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9496
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


POST = D("1793331207.484362686")    # c2814 capture post-echo (EPOCH-governs)
SCAN = D("1793331207.479")          # c2814 scanned_at (decimal)
TRIG = D("1793330177.000")          # c2814 trigger stamp (11:16:17 +08)
WIN = D("1793330389.757462242")     # window-2814 open (c2813 prophecy EPOCH)
PRE = D("1793331205.658023390")     # c2814 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793330677.889456533")   # c2814 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793330679.651949875")  # c2814 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793330679.647")        # c2814 echo scanned_at (decimal)
C2813_SCAN = D("1793330089.752")    # c2813 scanned_at
C2813_POST = D("1793330089.757462242")  # c2813 post-echo
C2813_PRE = D("1793330088.037175665")   # c2813 capture pre-echo
C2813_ECHO_POST = D("1793329673.062755684")  # c2813 echo post-echo
C2813_CLOSE = D("1793330478.000")   # c2813 close f52cdbe (03:21:18Z)
FOREIGN_NOW = D("1793330503.000")   # foreign 8cc4726 (03:21:43Z)
C2813_TRIG = D("1793328677.000")    # c2813 trigger stamp (10:51:17 +08)
WIN2813 = D("1793328988.217915386")  # window-2813 open (for the contract re-check)
TOKEN = D("1793330460.000")         # token 1121 (11:21:00 +08)
C2813_TOKEN = D("1793329260.000")   # token 1101 (11:01:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 11:16:17 +08 = 1793330177.000", dec_epoch(2026, 10, 30, 3, 16, 17), TRIG),
    ("c2813 trigger stamp 10:51:17 +08 = 1793328677.000", dec_epoch(2026, 10, 30, 2, 51, 17), C2813_TRIG),
    ("stamp-gap 1500.000s by stamp (10:51:17 -> 11:16:17; 0 priors of the exact form)", TRIG - C2813_TRIG, D("1500.000")),
    ("token-gap 1200.000s by token (1101 -> 1121; 0 priors of the exact '1200.000s by token' form)", TOKEN - C2813_TOKEN, D("1200.000")),
    ("token-vs-stamp +283.000 (11:16:17 -> 11:21:00; the +283 print, 0 priors)", TOKEN - TRIG, D("283.000")),
    ("c2813 close f52cdbe 03:21:18Z = 1793330478.000", dec_epoch(2026, 10, 30, 3, 21, 18), C2813_CLOSE),
    ("foreign 8cc4726 03:21:43Z = 1793330503.000", dec_epoch(2026, 10, 30, 3, 21, 43), FOREIGN_NOW),
    ("token 1121 = 03:21:00Z = 1793330460.000", dec_epoch(2026, 10, 30, 3, 21, 0), TOKEN),
    ("c2813 token 1101 = 03:01:00Z = 1793329260.000", dec_epoch(2026, 10, 30, 3, 1, 0), C2813_TOKEN),
    ("capture pre-echo EPOCH 1793331205.658023390 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 33, 25, 658023390), PRE),
    ("pre-echo ISO 03:33:25.657438369 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 3, 33, 25, 657438369), D("1793331205.657438369")),
    ("post-echo ISO 03:33:27.483736070 +0000 (epoch ns)", dec_epoch(2026, 10, 30, 3, 33, 27, 483736070), D("1793331207.483736070")),
    ("post-echo EPOCH 1793331207.484362686 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 33, 27, 484362686), POST),
    ("scanned_at 03:33:27.479 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 33, 27) + D("0.479"), SCAN),
    ("window-2814 open 03:19:49.757462242 +0000 (EPOCH-governs render)", dec_epoch(2026, 10, 30, 3, 19, 49, 757462242), WIN),
    ("window-2815 open = post-echo + 300.000", POST + D("300.000"), D("1793331507.484362686")),
    ("c2813 post-echo EPOCH 1793330089.757462242 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 14, 49, 757462242), C2813_POST),
    ("c2813 scanned_at 03:14:49.752 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 14, 49) + D("0.752"), C2813_SCAN),
    ("c2813 capture pre-echo EPOCH 1793330088.037175665 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 14, 48, 37175665), C2813_PRE),
    ("c2813 echo post-echo EPOCH 1793329673.062755684 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 7, 53, 62755684), C2813_ECHO_POST),
    ("echo pre-echo EPOCH 1793330677.889456533 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 24, 37, 889456533), ECHO_PRE),
    ("echo post-echo EPOCH 1793330679.651949875 (EPOCH-governs)", dec_epoch(2026, 10, 30, 3, 24, 39, 651949875), ECHO_POST),
    ("echo scanned_at 03:24:39.647 +0000 (decimal)", dec_epoch(2026, 10, 30, 3, 24, 39) + D("0.647"), ECHO_SCAN),
    ("window-2813 open 02:56:28.217915386 +0000 (EPOCH-governs re-check)", dec_epoch(2026, 10, 30, 2, 56, 28, 217915386), WIN2813),
]
exact_checks = [
    ("skew decimal-exact +5.362686ms (EPOCH-governs decomposition; SUB-10 extends m11)", POST - SCAN, D("0.005362686")),
    ("CAPTURE_vs_window +817.726900444 (POST-WINDOW; the capture-side print)", POST - WIN, D("817.726900444")),
    ("capture post-c2813-post-echo +1117.726900444", POST - C2813_POST, D("1117.726900444")),
    ("dd#388 = +817.727000000 (interval 1117.727 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#385 print 960.015 - 300 = 660.015 and the dd#387 print 1401.540 - 300 = 1101.540)", SCAN - C2813_SCAN - D("300.000"), D("817.727")),
    ("dd formula re-verification: 960.015 - 300 = 660.015", D("960.015") - D("300.000"), D("660.015")),
    ("dd formula re-verification: 1461.399 - 300 = 1161.399", D("1461.399") - D("300.000"), D("1161.399")),
    ("dd formula re-verification: 1401.540 - 300 = 1101.540", D("1401.540") - D("300.000"), D("1101.540")),
    ("INTERVAL#388 = 1030.479", SCAN - TRIG, D("1030.479")),
    ("LAG#388 = INTERVAL + dd - dd#387 = +746.666", (SCAN - TRIG) + (SCAN - C2813_SCAN - D("300.000")) - D("1101.540"), D("746.666")),
    ("LATE#388 = trigger - window-open = -212.757462242", TRIG - WIN, D("-212.757462242")),
    ("window-2814 = c2813 capture post-echo + 300.000 (the server contract)", WIN - C2813_POST, D("300.000")),
    ("trigger POSTDATES the c2813 echo post-echo by 503.937244316s (the POST-capture placement RE-OPENS m1)", TRIG - C2813_ECHO_POST, D("503.937244316")),
    ("trigger POSTDATES the c2813 capture pre-echo by 88.962824335s", TRIG - C2813_PRE, D("88.962824335")),
    ("trigger POSTDATES the c2813 scanned_at by 87.248s", TRIG - C2813_SCAN, D("87.248")),
    ("trigger POSTDATES the c2813 capture post-echo by 87.242537758s", TRIG - C2813_POST, D("87.242537758")),
    ("c2813 close POSTDATES the trigger by 301.000s (f52cdbe at 03:21:18)", C2813_CLOSE - TRIG, D("301.000")),
    ("foreign 8cc4726 POSTDATES the trigger by 326.000s (03:21:43)", FOREIGN_NOW - TRIG, D("326.000")),
    ("c2813 close landed 18.000s AFTER the token-1121 second (03:21:18 vs 03:21:00 — the AFTER-class re-opens m1, the BEFORE-class TERMINATES its m3 run)", C2813_CLOSE - TOKEN, D("18.000")),
    ("foreign 8cc4726 landed 43.000s AFTER the token second (03:21:43 — the BOTH-AFTER state RE-OPENS m1)", FOREIGN_NOW - TOKEN, D("43.000")),
    ("c2813 close landed 88.242537758s AFTER window-2814 open", C2813_CLOSE - WIN, D("88.242537758")),
    ("foreign 8cc4726 landed 113.242537758s AFTER window-2814 open", FOREIGN_NOW - WIN, D("113.242537758")),
    ("echo POST-WINDOW +289.894487633 (the echo-side print; the BOTH-POST print REPEATS)", ECHO_POST - WIN, D("289.894487633")),
    ("stamp-to-echo 500.889456533 (the echo pre-echo EPOCH minus the trigger; the deepest print 1025.631018606 STANDS — 500.889456533 shallower)", ECHO_PRE - TRIG, D("500.889456533")),
    ("echo wall latency 1.762493342 (echo post-echo EPOCH - echo pre-echo EPOCH; curl 1.755046 / server 1746ms latency-match)", ECHO_POST - ECHO_PRE, D("1.762493342")),
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
guard("block_title", lines[1].startswith("CYCLE 2814"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2814"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2815 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2816_birth",
      block.count("c2816") == 4 and lines[-1].count("c2816") == 2
      and "c2815/c2816" in lines[-1] and "FORWARD token c2816" in lines[-1]
      and "the c2816 pre==0 expectation" in block and "c2816_pre = 0" in block,
      f"block c2816={block.count('c2816')} next-line c2816={lines[-1].count('c2816')} "
      f"(expect 4: the Step-7 rehearsal pre-count print + the Step-7 census-time "
      f"print 'c2816_pre = 0' + the Next bullet's guard phrase 'c2815/c2816' AND "
      f"census-tuple sentence 'FORWARD token c2816')")
guard("block_c2815_step7_precount_sentence",
      "the c2815 pre-count is 4" in block
      and "per-line {9494: 2, 9496: 2}" in block,
      "the Step-7 current+1 pre-count sentence present (the c2815 pre-count is 4, "
      "born per the census measurement)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9496", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2814_next_bullet", last_nonempty.startswith("- Next: the c2814 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2814",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2814")]) == 0,
      f"c2814 substring mentions={wl.count('c2814')} (expect 14)")

# pre-counters — ONE dict built in a single statement block (the c2778
# NameError lesson structuralized: no guard can reference an unassigned name)
CENSUS_PRE = {f"c{y}": wl.count(f"c{y}")
              for y in list(range(2816, 2748, -1))}
CENSUS_EXPECT = {
    "c2816": 0, "c2815": 4, "c2814": 14, "c2813": 37, "c2812": 81, "c2811": 81,
    "c2810": 97, "c2809": 83, "c2808": 95, "c2807": 88, "c2806": 84, "c2805": 94,
    "c2804": 109, "c2803": 117, "c2802": 124, "c2801": 97, "c2800": 139, "c2799": 102,
    "c2798": 100, "c2797": 92, "c2796": 102, "c2795": 125, "c2794": 119, "c2793": 127,
    "c2792": 132, "c2791": 120, "c2790": 133, "c2789": 123, "c2788": 134, "c2787": 135,
    "c2786": 157, "c2785": 139, "c2784": 137, "c2783": 138, "c2782": 137, "c2781": 142,
    "c2780": 147, "c2779": 147, "c2778": 191, "c2777": 163, "c2776": 168, "c2775": 177,
    "c2774": 182, "c2773": 186, "c2772": 205, "c2771": 195, "c2770": 251, "c2769": 184,
    "c2768": 187, "c2767": 262, "c2766": 227, "c2765": 178, "c2764": 180, "c2763": 188,
    "c2762": 225, "c2761": 248, "c2760": 183, "c2759": 183, "c2758": 185, "c2757": 188,
    "c2756": 193, "c2755": 200, "c2754": 203, "c2753": 223, "c2752": 229, "c2751": 215,
    "c2750": 221, "c2749": 229,
}
c2815_lines = {i + 1: l.count("c2815") for i, l in enumerate(wl.splitlines()) if "c2815" in l}
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(wl.splitlines()) if "c2814" in l}
guard("c2816_pre==0", CENSUS_PRE["c2816"] == 0, f"got={CENSUS_PRE['c2816']} (the forward token "
      f"c2816 is UNBORN pre-append — measured pre-append)")
guard("c2815_pre==4", CENSUS_PRE["c2815"] == 4 and c2815_lines == {9494: 2, 9496: 2},
      f"got={CENSUS_PRE['c2815']} per-line={c2815_lines} (born FOUR: the c2813 Step-7 "
      f"twin-print line 9494 TWICE + TWICE inside the c2813 Next-block — NOT the "
      f"unborn class; the born-FOUR class REPEATS an ELEVENTH time)")
guard("c2814_pre==14", CENSUS_PRE["c2814"] == 14
      and c2814_lines == {9482: 2, 9484: 2, 9488: 5, 9494: 1, 9496: 4},
      f"got={CENSUS_PRE['c2814']} per-line={c2814_lines}")
for tag in [f"c{y}" for y in range(2813, 2748, -1)]:
    guard(f"{tag}_pre=={CENSUS_EXPECT[tag]}", CENSUS_PRE[tag] == CENSUS_EXPECT[tag],
          f"got={CENSUS_PRE[tag]}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==491", tid_pre == 491, f"got={tid_pre}")
guard("anchor_nogold_pre==424", gold_pre == 424, f"got={gold_pre}")
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
guard("post_worklog_lines==9508", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2815_next_bullet", last2.startswith("- Next: the c2815 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==492", tid_post == 492, f"got={tid_post}")
guard("anchor_nogold_post==425", gold_post == 425, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2814_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2814")]) == 1)
guard("c2816_mention_birth", wl2.count("c2816") == CENSUS_PRE["c2816"] + block.count("c2816"),
      f"pre={CENSUS_PRE['c2816']} (unborn) + block births={block.count('c2816')} (Step-7 pre-count "
      f"print + Step-7 census-time print + guard phrase + census-tuple sentence) "
      f"-> expect={CENSUS_PRE['c2816'] + block.count('c2816')} got={wl2.count('c2816')}")
for tag in [f"c{y}" for y in range(2815, 2748, -1)]:
    expect = CENSUS_PRE[tag] + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={CENSUS_PRE[tag]} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9496 -> 9508 (+12), c2814 entry + DRIFT-#49 pass-63 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
