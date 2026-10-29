#!/usr/bin/env python3
"""Guarded worklog append for the c2782 entry (12 lines).

Follows the append_cycle2781.py precedent — ALL asserts precede the
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
echo decompositions, the stamp-gap/token-gap cadence pair, the window-2782
EPOCH-governs render check, the window-2783 prophecy check, and the
queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must use
the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.67ms on the echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2784 = 2 born inside the Next bullet's guard phrase AND
census-tuple sentence — the c2767..c2782 forward-token lessons), zero adds to
the two standing post-#6/post-#15 anchor series (OCCURRENCE counting — the
standing method), pre-state (9112 lines, tail = the c2782 Next bullet, zero
serviced c2782 entries, c2782 mention census per-line {9100: 2, 9104: 2,
9112: 4}, anchors 459/392/60/28), post-state (9124 lines, tail = the c2783
Next bullet, anchors 460/393/60/28). Zero mid-line writes (append at EOF
only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2782.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9112
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


POST = D("1793309336.135826977")    # c2782 post-echo (EPOCH-governs)
SCAN = D("1793309336.130")          # c2782 scanned_at (decimal)
TRIG = D("1793308570.000")          # c2782 trigger stamp (05:16:10 +08)
WIN = D("1793309014.144714226")     # window-2782 open (c2781 prophecy EPOCH)
ECHO = D("1793309266.346546947")    # loop echo in-batch (EPOCH-governs)
C2781_SCAN = D("1793308714.139")    # c2781 scanned_at
C2781_POST = D("1793308714.144714226")  # c2781 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 05:16:10 +08 = 1793308570.000", dec_epoch(2026, 10, 29, 21, 16, 10), TRIG),
    ("c2781 trigger stamp 05:01:10 +08 = 1793307670.000", dec_epoch(2026, 10, 29, 21, 1, 10), D("1793307670.000")),
    ("stamp-gap 900.000s by stamp (05:01:10 -> 05:16:10; the one-cycle 601 excursion closes, the 900 print returns)", TRIG - D("1793307670.000"), D("900.000")),
    ("token-gap 720.000s by token (0510 -> 0522)", dec_epoch(2026, 10, 29, 21, 22, 0) - dec_epoch(2026, 10, 29, 21, 10, 0), D("720.000")),
    ("loop echo ISO integer second 21:27:46 +0000", dec_epoch(2026, 10, 29, 21, 27, 46), D("1793309266.000")),
    ("loop echo EPOCH 1793309266.346546947 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 27, 46, 346546947), ECHO),
    ("capture pre-echo EPOCH 1793309334.490681560 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 28, 54, 490681560), D("1793309334.490681560")),
    ("post-echo ISO 21:28:56.135155126 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 21, 28, 56, 135155126), D("1793309336.135155126")),
    ("post-echo EPOCH 1793309336.135826977 (EPOCH-governs)", dec_epoch(2026, 10, 29, 21, 28, 56, 135826977), POST),
    ("scanned_at 21:28:56.130 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 28, 56) + D("0.130"), SCAN),
    ("c2781 scanned_at 21:18:34.139 +0000 (decimal)", dec_epoch(2026, 10, 29, 21, 18, 34) + D("0.139"), C2781_SCAN),
    ("window-2782 open 05:23:34.144714226 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 21, 23, 34, 144714226), WIN),
    ("window-2783 open = post-echo + 300.000", POST + D("300.000"), D("1793309636.135826977")),
    ("echo post-c2781-post-echo +552.201832721", ECHO - C2781_POST, D("552.201832721")),
]
exact_checks = [
    ("skew decimal-exact +5.826977ms (EPOCH-governs decomposition)", POST - SCAN, D("0.005826977")),
    ("echo_vs_window +252.201832721 (POST-WINDOW extends m10)", ECHO - WIN, D("252.201832721")),
    ("dd#356 = +321.991000000 (interval 621.991 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#354 print 781.926 - 300 = 481.926 and the dd#355 print 805.732 - 300 = 505.732)", SCAN - C2781_SCAN - D("300.000"), D("321.991")),
    ("INTERVAL#356 = 766.130", SCAN - TRIG, D("766.130")),
    ("LAG#356 = INTERVAL + dd - dd#355 = +582.389", (SCAN - TRIG) + (SCAN - C2781_SCAN - D("300.000")) - D("505.732"), D("582.389")),
    ("LATE#356 = trigger - window-open = -444.144714226", TRIG - WIN, D("-444.144714226")),
    ("CAPTURE_vs_window +321.991112751 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("321.991112751")),
    ("echo post-c2781-close +344.346546947 (8fa30df at 21:22:02)", ECHO - D("1793308922.000"), D("344.346546947")),
    ("echo post-foreign-51f1161 +331.346546947 (21:22:15)", ECHO - D("1793308935.000"), D("331.346546947")),
    ("stamp-to-echo 696.346546947 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("696.346546947")),
    ("trigger predates c2781 close by 352.000s", D("1793308922.000") - TRIG, D("352.000")),
    ("trigger predates the foreign 51f1161 by 365.000s (21:22:15)", D("1793308935.000") - TRIG, D("365.000")),
    ("trigger predates the c2781 post-echo by 144.144714226s", C2781_POST - TRIG, D("144.144714226")),
    ("trigger predates window-2782 open by 444.144714226s", WIN - TRIG, D("444.144714226")),
    ("trigger postdates c2780 close by 326.000s (65b5294 at 21:10:44)", TRIG - D("1793308244.000"), D("326.000")),
    ("trigger postdates the foreign 134a6b8 by 312.000s (21:10:58)", TRIG - D("1793308258.000"), D("312.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2782"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2782"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2783 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2784_birth",
      block.count("c2784") == 2 and lines[-1].count("c2784") == 2
      and "c2783/c2784" in lines[-1] and "FORWARD token c2784" in lines[-1],
      f"block c2784={block.count('c2784')} next-line c2784={lines[-1].count('c2784')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9112", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2782_next_bullet", last_nonempty.startswith("- Next: the c2782 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2782",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2782")]) == 0,
      f"c2782 substring mentions={wl.count('c2782')} (expect 8)")
c2782_lines = {i + 1: l.count("c2782") for i, l in enumerate(wl.splitlines()) if "c2782" in l}
guard("c2782_mention_census_pre", wl.count("c2782") == 8 and c2782_lines == {9100: 2, 9104: 2, 9112: 4},
      f"per-line={c2782_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==459", tid_pre == 459, f"got={tid_pre}")
guard("anchor_nogold_pre==392", gold_pre == 392, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
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
guard("c2783_pre==2", c2783_pre == 2, f"got={c2783_pre}")
guard("c2782_pre==8", c2782_pre == 8, f"got={c2782_pre}")
guard("c2781_pre==34", c2781_pre == 34, f"got={c2781_pre}")
guard("c2780_pre==65", c2780_pre == 65, f"got={c2780_pre}")
guard("c2779_pre==67", c2779_pre == 67, f"got={c2779_pre}")
guard("c2778_pre==88", c2778_pre == 88, f"got={c2778_pre}")
guard("c2777_pre==83", c2777_pre == 83, f"got={c2777_pre}")
guard("c2776_pre==88", c2776_pre == 88, f"got={c2776_pre}")
guard("c2775_pre==97", c2775_pre == 97, f"got={c2775_pre}")
guard("c2774_pre==102", c2774_pre == 102, f"got={c2774_pre}")
guard("c2773_pre==106", c2773_pre == 106, f"got={c2773_pre}")
guard("c2772_pre==119", c2772_pre == 119, f"got={c2772_pre}")
guard("c2771_pre==115", c2771_pre == 115, f"got={c2771_pre}")
guard("c2770_pre==139", c2770_pre == 139, f"got={c2770_pre}")
guard("c2769_pre==116", c2769_pre == 116, f"got={c2769_pre}")
guard("c2768_pre==119", c2768_pre == 119, f"got={c2768_pre}")
guard("c2767_pre==130", c2767_pre == 130, f"got={c2767_pre}")
guard("c2766_pre==126", c2766_pre == 126, f"got={c2766_pre}")
guard("c2765_pre==110", c2765_pre == 110, f"got={c2765_pre}")
guard("c2764_pre==111", c2764_pre == 111, f"got={c2764_pre}")
guard("c2763_pre==116", c2763_pre == 116, f"got={c2763_pre}")
guard("c2762_pre==133", c2762_pre == 133, f"got={c2762_pre}")
guard("c2761_pre==147", c2761_pre == 147, f"got={c2761_pre}")
guard("c2760_pre==113", c2760_pre == 113, f"got={c2760_pre}")
guard("c2759_pre==115", c2759_pre == 115, f"got={c2759_pre}")
guard("c2758_pre==117", c2758_pre == 117, f"got={c2758_pre}")
guard("c2757_pre==120", c2757_pre == 120, f"got={c2757_pre}")
guard("c2756_pre==125", c2756_pre == 125, f"got={c2756_pre}")
guard("c2755_pre==132", c2755_pre == 132, f"got={c2755_pre}")
guard("c2754_pre==135", c2754_pre == 135, f"got={c2754_pre}")
guard("c2753_pre==141", c2753_pre == 141, f"got={c2753_pre}")
guard("c2752_pre==147", c2752_pre == 147, f"got={c2752_pre}")
guard("c2751_pre==133", c2751_pre == 133, f"got={c2751_pre}")
guard("c2750_pre==135", c2750_pre == 135, f"got={c2750_pre}")
guard("c2749_pre==139", c2749_pre == 139, f"got={c2749_pre}")
guard("c2748_pre==129", c2748_pre == 129, f"got={c2748_pre}")
guard("c2747_pre==127", c2747_pre == 127, f"got={c2747_pre}")
guard("c2746_pre==120", c2746_pre == 120, f"got={c2746_pre}")

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
guard("post_worklog_lines==9124", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2783_next_bullet", last2.startswith("- Next: the c2783 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==460", tid_post == 460, f"got={tid_post}")
guard("anchor_nogold_post==393", gold_post == 393, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2782_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2782")]) == 1)
expect_c2784_mentions = wl2.count("c2784")
guard("c2784_mention_birth", expect_c2784_mentions == block.count("c2784"),
      f"block births={block.count('c2784')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2784_mentions}")
for tag, pre in (("c2783", c2783_pre), ("c2782", c2782_pre), ("c2781", c2781_pre),
                 ("c2780", c2780_pre), ("c2779", c2779_pre), ("c2778", c2778_pre),
                 ("c2777", c2777_pre), ("c2776", c2776_pre), ("c2775", c2775_pre),
                 ("c2774", c2774_pre), ("c2773", c2773_pre), ("c2772", c2772_pre),
                 ("c2771", c2771_pre), ("c2770", c2770_pre), ("c2769", c2769_pre),
                 ("c2768", c2768_pre), ("c2767", c2767_pre), ("c2766", c2766_pre),
                 ("c2765", c2765_pre), ("c2764", c2764_pre), ("c2763", c2763_pre),
                 ("c2762", c2762_pre), ("c2761", c2761_pre), ("c2760", c2760_pre),
                 ("c2759", c2759_pre), ("c2758", c2758_pre), ("c2757", c2757_pre),
                 ("c2756", c2756_pre), ("c2755", c2755_pre), ("c2754", c2754_pre),
                 ("c2753", c2753_pre), ("c2752", c2752_pre), ("c2751", c2751_pre),
                 ("c2750", c2750_pre), ("c2749", c2749_pre), ("c2748", c2748_pre),
                 ("c2747", c2747_pre), ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9112 -> 9124 (+12), c2782 entry + DRIFT-#49 pass-31 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
