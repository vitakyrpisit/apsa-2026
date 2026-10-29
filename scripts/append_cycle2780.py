#!/usr/bin/env python3
"""Guarded worklog append for the c2780 entry (12 lines).

Follows the append_cycle2779.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append abort precedent class).
The ledger arithmetic stays in the DECIMAL class: every ns-decomposition
check is Decimal-exact or Decimal-with-1e-6-tolerance on the utc-derived
values. THE C2778 ABORT LESSON STRUCTURALIZED: every pre-counter variable is
assigned in the SAME statement block before any guard references it (the
c2778 attempt-1 NameError class is impossible here), and a REHEARSAL mode
(APPEND_REHEARSAL=1) runs the full guard battery against a byte-identical
temp copy BEFORE the real run — the attempt counter counts REAL runs only.
Guards: python-timegm epoch cross-verification (30 Decimal-class checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic, all echo decompositions, the
stamp-gap/token-gap cadence pair, the window-2780 EPOCH-governs render check,
and the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check
must use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock
reads differ ~0.7ms on the echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2782 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2780 forward-token lessons), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9088 lines, tail = the c2780 Next bullet, zero serviced
c2780 entries, c2780 mention census per-line {9076: 2, 9080: 2, 9088: 4},
anchors 457/390/60/28), post-state (9100 lines, tail = the c2781 Next
bullet, anchors 458/391/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2780.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9088
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


POST = D("1793307908.413692370")    # c2780 post-echo (EPOCH-governs)
SCAN = D("1793307908.407")          # c2780 scanned_at (decimal)
TRIG = D("1793307069.000")          # c2780 trigger stamp (04:51:09 +08)
WIN = D("1793307426.486281620")     # window-2780 open (c2779 prophecy EPOCH)
ECHO = D("1793307625.932544410")    # loop echo in-batch (EPOCH-governs)
C2779_SCAN = D("1793307126.481")    # c2779 scanned_at
C2779_POST = D("1793307126.486281620")  # c2779 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 04:51:09 +08 = 1793307069.000", dec_epoch(2026, 10, 29, 20, 51, 9), TRIG),
    ("c2779 trigger stamp 04:36:09 +08 = 1793306169.000", dec_epoch(2026, 10, 29, 20, 36, 9), D("1793306169.000")),
    ("stamp-gap 900.000s by stamp (04:36:09 -> 04:51:09; the attempt-1 harness constant carried 600.000 — the Decimal-exact guard caught the hand-derivation error, worklog UNTOUCHED)", TRIG - D("1793306169.000"), D("900.000")),
    ("token-gap 960.000s by token (0441 -> 0457)", dec_epoch(2026, 10, 29, 20, 57, 0) - dec_epoch(2026, 10, 29, 20, 41, 0), D("960.000")),
    ("loop echo ISO integer second 21:00:25 +0000", dec_epoch(2026, 10, 29, 21, 0, 25), D("1793307625.000")),
    ("loop echo EPOCH 1793307625.932544410 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 0, 25, 932544410), ECHO),
    ("capture pre-echo EPOCH 1793307906.807028387 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 5, 6, 807028387), D("1793307906.807028387")),
    ("post-echo ISO 21:05:08.412985022 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 21, 5, 8, 412985022), D("1793307908.412985022")),
    ("post-echo EPOCH 1793307908.413692370 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 5, 8, 413692370), POST),
    ("scanned_at 21:05:08.407 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 5, 8) + D("0.407"), SCAN),
    ("c2779 scanned_at 20:52:06.481 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 52, 6) + D("0.481"), C2779_SCAN),
    ("window-2780 open 04:57:06.486281620 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 20, 57, 6, 486281620), WIN),
    ("window-2781 open = post-echo + 300.000", POST + D("300.000"), D("1793308208.413692370")),
    ("echo post-c2779-post-echo +499.446262790", ECHO - C2779_POST, D("499.446262790")),
]
exact_checks = [
    ("skew decimal-exact +6.692370ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006692370")),
    ("echo_vs_window +199.446262790 (POST-WINDOW extends m8)", ECHO - WIN, D("199.446262790")),
    ("dd#354 = +481.926000000 (interval 781.926 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#352 print 583.098 - 300 = 283.098 and the dd#353 print 844.922 - 300 = 544.922)", SCAN - C2779_SCAN - D("300.000"), D("481.926")),
    ("INTERVAL#354 = 839.407", SCAN - TRIG, D("839.407")),
    ("LAG#354 = INTERVAL + dd - dd#353 = +776.411", (SCAN - TRIG) + (SCAN - C2779_SCAN - D("300.000")) - D("544.922"), D("776.411")),
    ("LATE#354 = trigger - window-open = -357.486281620", TRIG - WIN, D("-357.486281620")),
    ("CAPTURE_vs_window +481.927410750 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("481.927410750")),
    ("echo post-c2779-close +185.932544410 (d5acf5e at 20:57:20)", ECHO - D("1793307440.000"), D("185.932544410")),
    ("echo post-foreign-d22e2bb +165.932544410 (20:57:40)", ECHO - D("1793307460.000"), D("165.932544410")),
    ("stamp-to-echo 556.932544410 (the deepest 930.579496688 STANDS)", ECHO - TRIG, D("556.932544410")),
    ("trigger predates c2779 close by 371.000s", D("1793307440.000") - TRIG, D("371.000")),
    ("trigger predates the foreign d22e2bb by 391.000s (20:57:40)", D("1793307460.000") - TRIG, D("391.000")),
    ("trigger predates the c2779 post-echo by 57.486281620s", C2779_POST - TRIG, D("57.486281620")),
    ("trigger predates window-2780 open by 357.486281620s", WIN - TRIG, D("357.486281620")),
    ("trigger postdates c2778 close by 585.000s (486f086 at 20:41:24)", TRIG - D("1793306484.000"), D("585.000")),
    ("trigger postdates the foreign e54aab2 by 569.000s (20:41:40)", TRIG - D("1793306500.000"), D("569.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2780"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2780"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2781 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2782_birth",
      block.count("c2782") == 2 and lines[-1].count("c2782") == 2
      and "c2781/c2782" in lines[-1] and "FORWARD token c2782" in lines[-1],
      f"block c2782={block.count('c2782')} next-line c2782={lines[-1].count('c2782')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9088", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2780_next_bullet", last_nonempty.startswith("- Next: the c2780 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2780",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2780")]) == 0,
      f"c2780 substring mentions={wl.count('c2780')} (expect 8)")
c2780_lines = {i + 1: l.count("c2780") for i, l in enumerate(wl.splitlines()) if "c2780" in l}
guard("c2780_mention_census_pre", wl.count("c2780") == 8 and c2780_lines == {9076: 2, 9080: 2, 9088: 4},
      f"per-line={c2780_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==457", tid_pre == 457, f"got={tid_pre}")
guard("anchor_nogold_pre==390", gold_pre == 390, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2781_pre==2", c2781_pre == 2, f"got={c2781_pre}")
guard("c2780_pre==8", c2780_pre == 8, f"got={c2780_pre}")
guard("c2779_pre==33", c2779_pre == 33, f"got={c2779_pre}")
guard("c2778_pre==72", c2778_pre == 72, f"got={c2778_pre}")
guard("c2777_pre==73", c2777_pre == 73, f"got={c2777_pre}")
guard("c2776_pre==78", c2776_pre == 78, f"got={c2776_pre}")
guard("c2775_pre==87", c2775_pre == 87, f"got={c2775_pre}")
guard("c2774_pre==92", c2774_pre == 92, f"got={c2774_pre}")
guard("c2773_pre==96", c2773_pre == 96, f"got={c2773_pre}")
guard("c2772_pre==107", c2772_pre == 107, f"got={c2772_pre}")
guard("c2771_pre==105", c2771_pre == 105, f"got={c2771_pre}")
guard("c2770_pre==126", c2770_pre == 126, f"got={c2770_pre}")
guard("c2769_pre==108", c2769_pre == 108, f"got={c2769_pre}")
guard("c2768_pre==111", c2768_pre == 111, f"got={c2768_pre}")
guard("c2767_pre==120", c2767_pre == 120, f"got={c2767_pre}")
guard("c2766_pre==117", c2766_pre == 117, f"got={c2766_pre}")
guard("c2765_pre==104", c2765_pre == 104, f"got={c2765_pre}")
guard("c2764_pre==105", c2764_pre == 105, f"got={c2764_pre}")
guard("c2763_pre==110", c2763_pre == 110, f"got={c2763_pre}")
guard("c2762_pre==125", c2762_pre == 125, f"got={c2762_pre}")
guard("c2761_pre==139", c2761_pre == 139, f"got={c2761_pre}")
guard("c2760_pre==107", c2760_pre == 107, f"got={c2760_pre}")
guard("c2759_pre==109", c2759_pre == 109, f"got={c2759_pre}")
guard("c2758_pre==111", c2758_pre == 111, f"got={c2758_pre}")
guard("c2757_pre==114", c2757_pre == 114, f"got={c2757_pre}")
guard("c2756_pre==119", c2756_pre == 119, f"got={c2756_pre}")
guard("c2755_pre==126", c2755_pre == 126, f"got={c2755_pre}")
guard("c2754_pre==129", c2754_pre == 129, f"got={c2754_pre}")
guard("c2753_pre==135", c2753_pre == 135, f"got={c2753_pre}")
guard("c2752_pre==141", c2752_pre == 141, f"got={c2752_pre}")
guard("c2751_pre==127", c2751_pre == 127, f"got={c2751_pre}")
guard("c2750_pre==129", c2750_pre == 129, f"got={c2750_pre}")
guard("c2749_pre==133", c2749_pre == 133, f"got={c2749_pre}")
guard("c2748_pre==123", c2748_pre == 123, f"got={c2748_pre}")
guard("c2747_pre==121", c2747_pre == 121, f"got={c2747_pre}")
guard("c2746_pre==114", c2746_pre == 114, f"got={c2746_pre}")

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
guard("post_worklog_lines==9100", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2781_next_bullet", last2.startswith("- Next: the c2781 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==458", tid_post == 458, f"got={tid_post}")
guard("anchor_nogold_post==391", gold_post == 391, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2780_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2780")]) == 1)
expect_c2782_mentions = wl2.count("c2782")
guard("c2782_mention_birth", expect_c2782_mentions == block.count("c2782"),
      f"block births={block.count('c2782')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2782_mentions}")
for tag, pre in (("c2781", c2781_pre), ("c2780", c2780_pre), ("c2779", c2779_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9088 -> 9100 (+12), c2780 entry + DRIFT-#49 pass-29 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
