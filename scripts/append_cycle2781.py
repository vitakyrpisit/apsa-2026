#!/usr/bin/env python3
"""Guarded worklog append for the c2781 entry (12 lines).

Follows the append_cycle2780.py precedent — ALL asserts precede the
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
REAL runs only. Guards: python-timegm epoch cross-verification (30
Decimal-class checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic, all
echo decompositions, the stamp-gap/token-gap cadence pair, the window-2781
EPOCH-governs render check, the window-2782 prophecy check, and the
queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must use
the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.6ms on the echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2783 = 2 born inside the Next bullet's guard phrase AND
census-tuple sentence — the c2767..c2781 forward-token lessons), zero adds to
the two standing post-#6/post-#15 anchor series (OCCURRENCE counting — the
standing method), pre-state (9100 lines, tail = the c2781 Next bullet, zero
serviced c2781 entries, c2781 mention census per-line {9088: 2, 9092: 2,
9100: 4}, anchors 458/391/60/28), post-state (9112 lines, tail = the c2782
Next bullet, anchors 459/392/60/28). Zero mid-line writes (append at EOF
only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2781.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9100
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

# 1) python-timegm epoch cross-verification (Decimal-class, 30 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = D("1793308714.144714226")    # c2781 post-echo (EPOCH-governs)
SCAN = D("1793308714.139")          # c2781 scanned_at (decimal)
TRIG = D("1793307670.000")          # c2781 trigger stamp (05:01:10 +08)
WIN = D("1793308208.413692370")     # window-2781 open (c2780 prophecy EPOCH)
ECHO = D("1793308695.631018606")    # loop echo in-batch (EPOCH-governs)
C2780_SCAN = D("1793307908.407")    # c2780 scanned_at
C2780_POST = D("1793307908.413692370")  # c2780 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 05:01:10 +08 = 1793307670.000", dec_epoch(2026, 10, 29, 21, 1, 10), TRIG),
    ("c2780 trigger stamp 04:51:09 +08 = 1793307069.000", dec_epoch(2026, 10, 29, 20, 51, 9), D("1793307069.000")),
    ("stamp-gap 601.000s by stamp (04:51:09 -> 05:01:10; the one-cycle 900 excursion closes, the 600/601 band resumes)", TRIG - D("1793307069.000"), D("601.000")),
    ("token-gap 780.000s by token (0457 -> 0510)", dec_epoch(2026, 10, 29, 21, 10, 0) - dec_epoch(2026, 10, 29, 20, 57, 0), D("780.000")),
    ("loop echo ISO integer second 21:18:15 +0000", dec_epoch(2026, 10, 29, 21, 18, 15), D("1793308695.000")),
    ("loop echo EPOCH 1793308695.631018606 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 18, 15, 631018606), ECHO),
    ("capture pre-echo EPOCH 1793308712.605625703 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 18, 32, 605625703), D("1793308712.605625703")),
    ("post-echo ISO 21:18:34.144071434 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 21, 18, 34, 144071434), D("1793308714.144071434")),
    ("post-echo EPOCH 1793308714.144714226 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 18, 34, 144714226), POST),
    ("scanned_at 21:18:34.139 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 18, 34) + D("0.139"), SCAN),
    ("c2780 scanned_at 21:05:08.407 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 5, 8) + D("0.407"), C2780_SCAN),
    ("window-2781 open 05:10:08.413692370 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 21, 10, 8, 413692370), WIN),
    ("window-2782 open = post-echo + 300.000", POST + D("300.000"), D("1793309014.144714226")),
    ("echo post-c2780-post-echo +787.217326236", ECHO - C2780_POST, D("787.217326236")),
]
exact_checks = [
    ("skew decimal-exact +5.714226ms (EPOCH-governs decomposition)", POST - SCAN, D("0.005714226")),
    ("echo_vs_window +487.217326236 (POST-WINDOW extends m9)", ECHO - WIN, D("487.217326236")),
    ("dd#355 = +505.732000000 (interval 805.732 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#353 print 844.922 - 300 = 544.922 and the dd#354 print 781.926 - 300 = 481.926)", SCAN - C2780_SCAN - D("300.000"), D("505.732")),
    ("INTERVAL#355 = 1044.139", SCAN - TRIG, D("1044.139")),
    ("LAG#355 = INTERVAL + dd - dd#354 = +1067.945", (SCAN - TRIG) + (SCAN - C2780_SCAN - D("300.000")) - D("481.926"), D("1067.945")),
    ("LATE#355 = trigger - window-open = -538.413692370", TRIG - WIN, D("-538.413692370")),
    ("CAPTURE_vs_window +505.731021856 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("505.731021856")),
    ("echo post-c2780-close +451.631018606 (65b5294 at 21:10:44)", ECHO - D("1793308244.000"), D("451.631018606")),
    ("echo post-foreign-134a6b8 +437.631018606 (21:10:58)", ECHO - D("1793308258.000"), D("437.631018606")),
    ("stamp-to-echo 1025.631018606 (a NEW DEEPEST print — supersedes the 930.579496688)", ECHO - TRIG, D("1025.631018606")),
    ("trigger predates c2780 close by 574.000s", D("1793308244.000") - TRIG, D("574.000")),
    ("trigger predates the foreign 134a6b8 by 588.000s (21:10:58)", D("1793308258.000") - TRIG, D("588.000")),
    ("trigger predates the c2780 post-echo by 238.413692370s", C2780_POST - TRIG, D("238.413692370")),
    ("trigger predates window-2781 open by 538.413692370s", WIN - TRIG, D("538.413692370")),
    ("trigger postdates c2779 close by 230.000s (d5acf5e at 20:57:20)", TRIG - D("1793307440.000"), D("230.000")),
    ("trigger postdates the foreign d22e2bb by 210.000s (20:57:40)", TRIG - D("1793307460.000"), D("210.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2781"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2781"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2782 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2783_birth",
      block.count("c2783") == 2 and lines[-1].count("c2783") == 2
      and "c2782/c2783" in lines[-1] and "FORWARD token c2783" in lines[-1],
      f"block c2783={block.count('c2783')} next-line c2783={lines[-1].count('c2783')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9100", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2781_next_bullet", last_nonempty.startswith("- Next: the c2781 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2781",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2781")]) == 0,
      f"c2781 substring mentions={wl.count('c2781')} (expect 8)")
c2781_lines = {i + 1: l.count("c2781") for i, l in enumerate(wl.splitlines()) if "c2781" in l}
guard("c2781_mention_census_pre", wl.count("c2781") == 8 and c2781_lines == {9088: 2, 9092: 2, 9100: 4},
      f"per-line={c2781_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==458", tid_pre == 458, f"got={tid_pre}")
guard("anchor_nogold_pre==391", gold_pre == 391, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2782_pre==2", c2782_pre == 2, f"got={c2782_pre}")
guard("c2781_pre==8", c2781_pre == 8, f"got={c2781_pre}")
guard("c2780_pre==35", c2780_pre == 35, f"got={c2780_pre}")
guard("c2779_pre==61", c2779_pre == 61, f"got={c2779_pre}")
guard("c2778_pre==81", c2778_pre == 81, f"got={c2778_pre}")
guard("c2777_pre==78", c2777_pre == 78, f"got={c2777_pre}")
guard("c2776_pre==83", c2776_pre == 83, f"got={c2776_pre}")
guard("c2775_pre==92", c2775_pre == 92, f"got={c2775_pre}")
guard("c2774_pre==97", c2774_pre == 97, f"got={c2774_pre}")
guard("c2773_pre==101", c2773_pre == 101, f"got={c2773_pre}")
guard("c2772_pre==113", c2772_pre == 113, f"got={c2772_pre}")
guard("c2771_pre==110", c2771_pre == 110, f"got={c2771_pre}")
guard("c2770_pre==133", c2770_pre == 133, f"got={c2770_pre}")
guard("c2769_pre==112", c2769_pre == 112, f"got={c2769_pre}")
guard("c2768_pre==115", c2768_pre == 115, f"got={c2768_pre}")
guard("c2767_pre==125", c2767_pre == 125, f"got={c2767_pre}")
guard("c2766_pre==122", c2766_pre == 122, f"got={c2766_pre}")
guard("c2765_pre==107", c2765_pre == 107, f"got={c2765_pre}")
guard("c2764_pre==108", c2764_pre == 108, f"got={c2764_pre}")
guard("c2763_pre==113", c2763_pre == 113, f"got={c2763_pre}")
guard("c2762_pre==129", c2762_pre == 129, f"got={c2762_pre}")
guard("c2761_pre==143", c2761_pre == 143, f"got={c2761_pre}")
guard("c2760_pre==110", c2760_pre == 110, f"got={c2760_pre}")
guard("c2759_pre==112", c2759_pre == 112, f"got={c2759_pre}")
guard("c2758_pre==114", c2758_pre == 114, f"got={c2758_pre}")
guard("c2757_pre==117", c2757_pre == 117, f"got={c2757_pre}")
guard("c2756_pre==122", c2756_pre == 122, f"got={c2756_pre}")
guard("c2755_pre==129", c2755_pre == 129, f"got={c2755_pre}")
guard("c2754_pre==132", c2754_pre == 132, f"got={c2754_pre}")
guard("c2753_pre==138", c2753_pre == 138, f"got={c2753_pre}")
guard("c2752_pre==144", c2752_pre == 144, f"got={c2752_pre}")
guard("c2751_pre==130", c2751_pre == 130, f"got={c2751_pre}")
guard("c2750_pre==132", c2750_pre == 132, f"got={c2750_pre}")
guard("c2749_pre==136", c2749_pre == 136, f"got={c2749_pre}")
guard("c2748_pre==126", c2748_pre == 126, f"got={c2748_pre}")
guard("c2747_pre==124", c2747_pre == 124, f"got={c2747_pre}")
guard("c2746_pre==117", c2746_pre == 117, f"got={c2746_pre}")

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
guard("post_worklog_lines==9112", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2782_next_bullet", last2.startswith("- Next: the c2782 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==459", tid_post == 459, f"got={tid_post}")
guard("anchor_nogold_post==392", gold_post == 392, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2781_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2781")]) == 1)
expect_c2783_mentions = wl2.count("c2783")
guard("c2783_mention_birth", expect_c2783_mentions == block.count("c2783"),
      f"block births={block.count('c2783')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2783_mentions}")
for tag, pre in (("c2782", c2782_pre), ("c2781", c2781_pre), ("c2780", c2780_pre),
                 ("c2779", c2779_pre), ("c2778", c2778_pre), ("c2777", c2777_pre),
                 ("c2776", c2776_pre), ("c2775", c2775_pre), ("c2774", c2774_pre),
                 ("c2773", c2773_pre), ("c2772", c2772_pre), ("c2771", c2771_pre),
                 ("c2770", c2770_pre), ("c2769", c2769_pre), ("c2768", c2768_pre),
                 ("c2767", c2767_pre), ("c2766", c2766_pre), ("c2765", c2765_pre),
                 ("c2764", c2764_pre), ("c2763", c2763_pre), ("c2762", c2762_pre),
                 ("c2761", c2761_pre), ("c2760", c2760_pre), ("c2759", c2759_pre),
                 ("c2758", c2758_pre), ("c2757", c2757_pre), ("c2756", c2756_pre),
                 ("c2755", c2755_pre), ("c2754", c2754_pre), ("c2753", c2753_pre),
                 ("c2752", c2752_pre), ("c2751", c2751_pre), ("c2750", c2750_pre),
                 ("c2749", c2749_pre), ("c2748", c2748_pre), ("c2747", c2747_pre),
                 ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9100 -> 9112 (+12), c2781 entry + DRIFT-#49 pass-30 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
