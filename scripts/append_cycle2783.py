#!/usr/bin/env python3
"""Guarded worklog append for the c2783 entry (12 lines).

Follows the append_cycle2782.py precedent — ALL asserts precede the
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
REAL runs only. Guards: python-timegm epoch cross-verification (Decimal-class
checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic, all echo
decompositions, the stamp-gap/token-gap cadence pair, the window-2783
EPOCH-governs render check, the window-2784 prophecy check, the
close-at-the-token-second identity, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~0.7ms on the echo), block
structure (12 lines: separator, title, standard Task ID line, Steps 1-7,
no-gold, Next bullet), the FORWARD-token guard (c2785 = 2 born inside the Next
bullet's guard phrase AND census-tuple sentence — the c2767..c2783
forward-token lessons), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9124 lines,
tail = the c2783 Next bullet, zero serviced c2783 entries, c2783 mention
census per-line {9112: 2, 9116: 2, 9124: 4}, c2784 = 2 per-line {9124: 2},
anchors 460/393/60/28), post-state (9136 lines, tail = the c2784 Next bullet,
anchors 461/394/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2783.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9124
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


POST = D("1793309890.936509291")    # c2783 post-echo (EPOCH-governs)
SCAN = D("1793309890.930")          # c2783 scanned_at (decimal)
TRIG = D("1793309169.000")          # c2783 trigger stamp (05:26:09 +08)
WIN = D("1793309636.135826977")     # window-2783 open (c2782 prophecy EPOCH)
ECHO = D("1793309870.502864009")    # loop echo in-batch (EPOCH-governs)
C2782_SCAN = D("1793309336.130")    # c2782 scanned_at
C2782_POST = D("1793309336.135826977")  # c2782 post-echo
CLOSE = D("1793309520.000")         # c2782 close 2be3f8a (21:32:00Z)
FOREIGN = D("1793309532.000")       # foreign f076455 (21:32:12Z)
C2781_CLOSE = D("1793308922.000")   # c2781 close 8fa30df (21:22:02Z)
C2781_FOREIGN = D("1793308935.000") # foreign 51f1161 (21:22:15Z)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 05:26:09 +08 = 1793309169.000", dec_epoch(2026, 10, 29, 21, 26, 9), TRIG),
    ("c2782 trigger stamp 05:16:10 +08 = 1793308570.000", dec_epoch(2026, 10, 29, 21, 16, 10), D("1793308570.000")),
    ("c2781 trigger stamp 05:01:10 +08 = 1793307670.000", dec_epoch(2026, 10, 29, 21, 1, 10), D("1793307670.000")),
    ("stamp-gap 599.000s by stamp (05:16:10 -> 05:26:09; the 599 print returns)", TRIG - D("1793308570.000"), D("599.000")),
    ("token-gap 600.000s by token (0522 -> 0532; the 600 print returns)", dec_epoch(2026, 10, 29, 21, 32, 0) - dec_epoch(2026, 10, 29, 21, 22, 0), D("600.000")),
    ("c2782 close 2be3f8a 21:32:00Z = 1793309520.000", dec_epoch(2026, 10, 29, 21, 32, 0), CLOSE),
    ("close-at-the-token-second identity (close 1793309520.000 == token 0532 epoch)", CLOSE, dec_epoch(2026, 10, 29, 21, 32, 0)),
    ("foreign f076455 21:32:12Z = 1793309532.000", dec_epoch(2026, 10, 29, 21, 32, 12), FOREIGN),
    ("c2781 close 8fa30df 21:22:02Z = 1793308922.000", dec_epoch(2026, 10, 29, 21, 22, 2), C2781_CLOSE),
    ("foreign 51f1161 21:22:15Z = 1793308935.000", dec_epoch(2026, 10, 29, 21, 22, 15), C2781_FOREIGN),
    ("loop echo ISO integer second 21:37:50 +0000", dec_epoch(2026, 10, 29, 21, 37, 50), D("1793309870.000")),
    ("loop echo EPOCH 1793309870.502864009 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 37, 50, 502864009), ECHO),
    ("capture pre-echo EPOCH 1793309889.279138432 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 38, 9, 279138432), D("1793309889.279138432")),
    ("post-echo ISO 21:38:10.935833505 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 21, 38, 10, 935833505), D("1793309890.935833505")),
    ("post-echo EPOCH 1793309890.936509291 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 38, 10, 936509291), POST),
    ("scanned_at 21:38:10.930 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 38, 10) + D("0.930"), SCAN),
    ("c2782 scanned_at 21:28:56.130 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 28, 56) + D("0.130"), C2782_SCAN),
    ("c2782 post-echo EPOCH 1793309336.135826977", dec_epoch(2026, 10, 29, 21, 28, 56, 135826977), C2782_POST),
    ("window-2783 open 05:33:56.135826977 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 21, 33, 56, 135826977), WIN),
    ("window-2784 open = post-echo + 300.000", POST + D("300.000"), D("1793310190.936509291")),
    ("echo post-c2782-post-echo +534.367037032", ECHO - C2782_POST, D("534.367037032")),
]
exact_checks = [
    ("skew decimal-exact +6.509291ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006509291")),
    ("echo_vs_window +234.367037032 (POST-WINDOW extends m11)", ECHO - WIN, D("234.367037032")),
    ("dd#357 = +254.800000000 (interval 554.800 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#355 print 805.732 - 300 = 505.732 and the dd#356 print 621.991 - 300 = 321.991)", SCAN - C2782_SCAN - D("300.000"), D("254.800")),
    ("INTERVAL#357 = 721.930", SCAN - TRIG, D("721.930")),
    ("LAG#357 = INTERVAL + dd - dd#356 = +654.739", (SCAN - TRIG) + (SCAN - C2782_SCAN - D("300.000")) - D("321.991"), D("654.739")),
    ("LATE#357 = trigger - window-open = -467.135826977", TRIG - WIN, D("-467.135826977")),
    ("CAPTURE_vs_window +254.800682314 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("254.800682314")),
    ("echo post-c2782-close +350.502864009 (2be3f8a at 21:32:00)", ECHO - CLOSE, D("350.502864009")),
    ("echo post-foreign-f076455 +338.502864009 (21:32:12)", ECHO - FOREIGN, D("338.502864009")),
    ("stamp-to-echo 701.502864009 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("701.502864009")),
    ("trigger predates c2782 close by 351.000s", CLOSE - TRIG, D("351.000")),
    ("trigger predates the foreign f076455 by 363.000s (21:32:12)", FOREIGN - TRIG, D("363.000")),
    ("trigger predates the c2782 post-echo by 167.135826977s", C2782_POST - TRIG, D("167.135826977")),
    ("trigger predates window-2783 open by 467.135826977s", WIN - TRIG, D("467.135826977")),
    ("trigger postdates c2781 close by 247.000s (8fa30df at 21:22:02)", TRIG - C2781_CLOSE, D("247.000")),
    ("trigger postdates the foreign 51f1161 by 234.000s (21:22:15)", TRIG - C2781_FOREIGN, D("234.000")),
    ("capture post-c2782-post-echo +554.800682314", POST - C2782_POST, D("554.800682314")),
    ("capture-vs-echo +20.433645282", POST - ECHO, D("20.433645282")),
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
guard("block_title", lines[1].startswith("CYCLE 2783"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2783"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2784 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2785_birth",
      block.count("c2785") == 2 and lines[-1].count("c2785") == 2
      and "c2784/c2785" in lines[-1] and "FORWARD token c2785" in lines[-1],
      f"block c2785={block.count('c2785')} next-line c2785={lines[-1].count('c2785')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9124", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2783_next_bullet", last_nonempty.startswith("- Next: the c2783 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2783",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2783")]) == 0,
      f"c2783 substring mentions={wl.count('c2783')} (expect 8)")
c2783_lines = {i + 1: l.count("c2783") for i, l in enumerate(wl.splitlines()) if "c2783" in l}
guard("c2783_mention_census_pre", wl.count("c2783") == 8 and c2783_lines == {9112: 2, 9116: 2, 9124: 4},
      f"per-line={c2783_lines}")
c2784_lines = {i + 1: l.count("c2784") for i, l in enumerate(wl.splitlines()) if "c2784" in l}
guard("c2784_forward_token_pre", wl.count("c2784") == 2 and c2784_lines == {9124: 2},
      f"per-line={c2784_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==460", tid_pre == 460, f"got={tid_pre}")
guard("anchor_nogold_pre==393", gold_pre == 393, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2784_pre==2", c2784_pre == 2, f"got={c2784_pre}")
guard("c2783_pre==8", c2783_pre == 8, f"got={c2783_pre}")
guard("c2782_pre==35", c2782_pre == 35, f"got={c2782_pre}")
guard("c2781_pre==65", c2781_pre == 65, f"got={c2781_pre}")
guard("c2780_pre==70", c2780_pre == 70, f"got={c2780_pre}")
guard("c2779_pre==71", c2779_pre == 71, f"got={c2779_pre}")
guard("c2778_pre==94", c2778_pre == 94, f"got={c2778_pre}")
guard("c2777_pre==87", c2777_pre == 87, f"got={c2777_pre}")
guard("c2776_pre==92", c2776_pre == 92, f"got={c2776_pre}")
guard("c2775_pre==101", c2775_pre == 101, f"got={c2775_pre}")
guard("c2774_pre==106", c2774_pre == 106, f"got={c2774_pre}")
guard("c2773_pre==110", c2773_pre == 110, f"got={c2773_pre}")
guard("c2772_pre==124", c2772_pre == 124, f"got={c2772_pre}")
guard("c2771_pre==119", c2771_pre == 119, f"got={c2771_pre}")
guard("c2770_pre==144", c2770_pre == 144, f"got={c2770_pre}")
guard("c2769_pre==119", c2769_pre == 119, f"got={c2769_pre}")
guard("c2768_pre==122", c2768_pre == 122, f"got={c2768_pre}")
guard("c2767_pre==135", c2767_pre == 135, f"got={c2767_pre}")
guard("c2766_pre==130", c2766_pre == 130, f"got={c2766_pre}")
guard("c2765_pre==113", c2765_pre == 113, f"got={c2765_pre}")
guard("c2764_pre==114", c2764_pre == 114, f"got={c2764_pre}")
guard("c2763_pre==119", c2763_pre == 119, f"got={c2763_pre}")
guard("c2762_pre==137", c2762_pre == 137, f"got={c2762_pre}")
guard("c2761_pre==151", c2761_pre == 151, f"got={c2761_pre}")
guard("c2760_pre==116", c2760_pre == 116, f"got={c2760_pre}")
guard("c2759_pre==118", c2759_pre == 118, f"got={c2759_pre}")
guard("c2758_pre==120", c2758_pre == 120, f"got={c2758_pre}")
guard("c2757_pre==123", c2757_pre == 123, f"got={c2757_pre}")
guard("c2756_pre==128", c2756_pre == 128, f"got={c2756_pre}")
guard("c2755_pre==135", c2755_pre == 135, f"got={c2755_pre}")
guard("c2754_pre==138", c2754_pre == 138, f"got={c2754_pre}")
guard("c2753_pre==144", c2753_pre == 144, f"got={c2753_pre}")
guard("c2752_pre==150", c2752_pre == 150, f"got={c2752_pre}")
guard("c2751_pre==136", c2751_pre == 136, f"got={c2751_pre}")
guard("c2750_pre==138", c2750_pre == 138, f"got={c2750_pre}")
guard("c2749_pre==142", c2749_pre == 142, f"got={c2749_pre}")
guard("c2748_pre==132", c2748_pre == 132, f"got={c2748_pre}")
guard("c2747_pre==130", c2747_pre == 130, f"got={c2747_pre}")
guard("c2746_pre==123", c2746_pre == 123, f"got={c2746_pre}")

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
guard("post_worklog_lines==9136", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2784_next_bullet", last2.startswith("- Next: the c2784 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==461", tid_post == 461, f"got={tid_post}")
guard("anchor_nogold_post==394", gold_post == 394, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2783_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2783")]) == 1)
expect_c2785_mentions = wl2.count("c2785")
guard("c2785_mention_birth", expect_c2785_mentions == block.count("c2785"),
      f"block births={block.count('c2785')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2785_mentions}")
for tag, pre in (("c2784", c2784_pre), ("c2783", c2783_pre), ("c2782", c2782_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9124 -> 9136 (+12), c2783 entry + DRIFT-#49 pass-32 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
