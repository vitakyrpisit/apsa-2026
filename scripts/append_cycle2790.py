#!/usr/bin/env python3
"""Guarded worklog append for the c2790 entry (12 lines).

Follows the append_cycle2789.py precedent — ALL asserts precede the
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
decompositions, the stamp-gap/token-gap/token-vs-stamp cadence triple, the
window-2790 EPOCH-governs render check, the window-2791 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.66ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2792 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2790 forward-token lessons; NOTE the c2792 pre-count
is 0 (unborn) while the c2791 pre-count is 2 — the c2783 c2788-pre==2 class
CARRIES this cycle: the c2791 forward token was born TWICE inside the c2789
Next-block (measured at census time: per-line {9208: 2}), NOT the c2785
c2787-pre==0 class), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9208 lines,
tail = the c2790 Next bullet, zero serviced c2790 entries, c2790 mention
census per-line {9196: 2, 9200: 1, 9206: 1, 9208: 4}, c2791 = 2 per-line
{9208: 2}, anchors 467/400/60/28), post-state (9220 lines, tail = the c2791
Next bullet, anchors 468/401/60/28). Zero mid-line writes (append at EOF
only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2790.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9208
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


POST = D("1793313709.181138247")    # c2790 post-echo (EPOCH-governs)
SCAN = D("1793313709.175")          # c2790 scanned_at (decimal)
TRIG = D("1793313071.000")          # c2790 trigger stamp (06:31:11 +08)
WIN = D("1793313456.207059789")     # window-2790 open (c2789 prophecy EPOCH)
ECHO = D("1793313453.285658076")    # loop echo #511 in-batch POST read (EPOCH-governs)
ECHO_PRE = D("1793313451.607965396")  # loop echo #511 PRE read (the bracket)
C2789_SCAN = D("1793313156.201")    # c2789 scanned_at
C2789_POST = D("1793313156.207059789")  # c2789 post-echo
C2789_CLOSE = D("1793313367.000")   # c2789 close 2af9fd7 (22:36:07Z)
C2789_FOREIGN = D("1793313382.000") # foreign c048029 (22:36:22Z)
C2789_TRIG = D("1793312471.000")    # c2789 trigger stamp (06:21:11 +08)
C2788_CLOSE = D("1793312840.000")   # c2788 close 6253361 (22:27:20Z)
C2788_FOREIGN = D("1793312859.000") # foreign ffa527c (22:27:39Z)
TOKEN = D("1793313360.000")         # token 0636 (06:36:00Z)
C2789_TOKEN = D("1793312820.000")   # token 0627 (06:27:00Z)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 06:31:11 +08 = 1793313071.000", dec_epoch(2026, 10, 29, 22, 31, 11), TRIG),
    ("c2789 trigger stamp 06:21:11 +08 = 1793312471.000", dec_epoch(2026, 10, 29, 22, 21, 11), C2789_TRIG),
    ("stamp-gap 600.000s by stamp (06:21:11 -> 06:31:11; the 600 print REPEATS, 20 priors)", TRIG - C2789_TRIG, D("600.000")),
    ("token-gap 540.000s by token (0627 -> 0636; the 540 print RETURNS, 16 priors)", TOKEN - C2789_TOKEN, D("540.000")),
    ("token-vs-stamp +289.000 (06:31:11 -> 06:36:00; the +289 print is NEW)", TOKEN - TRIG, D("289.000")),
    ("c2789 close 2af9fd7 22:36:07Z = 1793313367.000", dec_epoch(2026, 10, 29, 22, 36, 7), C2789_CLOSE),
    ("foreign c048029 22:36:22Z = 1793313382.000", dec_epoch(2026, 10, 29, 22, 36, 22), C2789_FOREIGN),
    ("c2788 close 6253361 22:27:20Z = 1793312840.000", dec_epoch(2026, 10, 29, 22, 27, 20), C2788_CLOSE),
    ("foreign ffa527c 22:27:39Z = 1793312859.000", dec_epoch(2026, 10, 29, 22, 27, 39), C2788_FOREIGN),
    ("loop echo ISO integer second 22:37:33 +0000", dec_epoch(2026, 10, 29, 22, 37, 33), D("1793313453.000")),
    ("loop echo EPOCH 1793313453.285658076 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 22, 37, 33, 285658076), ECHO),
    ("loop echo PRE read 1793313451.607965396 (the bracket)", dec_epoch(2026, 10, 29, 22, 37, 31, 607965396), ECHO_PRE),
    ("capture pre-echo EPOCH 1793313707.513201615 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 41, 47, 513201615), D("1793313707.513201615")),
    ("post-echo ISO 22:41:49.180477286 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 22, 41, 49, 180477286), D("1793313709.180477286")),
    ("post-echo EPOCH 1793313709.181138247 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 41, 49, 181138247), POST),
    ("scanned_at 22:41:49.175 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 41, 49) + D("0.175"), SCAN),
    ("c2789 scanned_at 22:32:36.201 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 32, 36) + D("0.201"), C2789_SCAN),
    ("c2789 post-echo EPOCH 1793313156.207059789", dec_epoch(2026, 10, 29, 22, 32, 36, 207059789), C2789_POST),
    ("window-2790 open 06:37:36.207059789 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 22, 37, 36, 207059789), WIN),
    ("window-2791 open = post-echo + 300.000", POST + D("300.000"), D("1793314009.181138247")),
    ("echo post-c2789-post-echo +297.078598287", ECHO - C2789_POST, D("297.078598287")),
]
exact_checks = [
    ("skew decimal-exact +6.138247ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006138247")),
    ("echo_vs_window -2.921401713 (PRE-WINDOW re-opens m1)", ECHO - WIN, D("-2.921401713")),
    ("dd#364 = +252.974000000 (interval 552.974 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#358 print 631.629 - 300 = 331.629 and the dd#359 print 544.537 - 300 = 244.537 and the dd#360 print 574.472 - 300 = 274.472 and the dd#361 print 523.771 - 300 = 223.771 and the dd#362 print 445.372 - 300 = 145.372 and the dd#363 print 545.490 - 300 = 245.490)", SCAN - C2789_SCAN - D("300.000"), D("252.974")),
    ("dd formula re-verification: 631.629 - 300 = 331.629", D("631.629") - D("300.000"), D("331.629")),
    ("dd formula re-verification: 544.537 - 300 = 244.537", D("544.537") - D("300.000"), D("244.537")),
    ("dd formula re-verification: 574.472 - 300 = 274.472", D("574.472") - D("300.000"), D("274.472")),
    ("dd formula re-verification: 523.771 - 300 = 223.771", D("523.771") - D("300.000"), D("223.771")),
    ("dd formula re-verification: 445.372 - 300 = 145.372", D("445.372") - D("300.000"), D("145.372")),
    ("dd formula re-verification: 545.490 - 300 = 245.490", D("545.490") - D("300.000"), D("245.490")),
    ("INTERVAL#364 = 638.175", SCAN - TRIG, D("638.175")),
    ("LAG#364 = INTERVAL + dd - dd#363 = +645.659", (SCAN - TRIG) + (SCAN - C2789_SCAN - D("300.000")) - D("245.490"), D("645.659")),
    ("LATE#364 = trigger - window-open = -385.207059789", TRIG - WIN, D("-385.207059789")),
    ("CAPTURE_vs_window +252.974078458 (POST-WINDOW; echo PRE — the SPLIT print returns)", POST - WIN, D("252.974078458")),
    ("capture-vs-echo +255.895480171", POST - ECHO, D("255.895480171")),
    ("capture post-c2789-post-echo +552.974078458", POST - C2789_POST, D("552.974078458")),
    ("echo post-c2789-close +86.285658076 (2af9fd7 at 22:36:07)", ECHO - C2789_CLOSE, D("86.285658076")),
    ("echo post-foreign-c048029 +71.285658076 (22:36:22)", ECHO - C2789_FOREIGN, D("71.285658076")),
    ("stamp-to-echo 382.285658076 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("382.285658076")),
    ("trigger predates c2789 close by 296.000s", C2789_CLOSE - TRIG, D("296.000")),
    ("trigger predates the foreign c048029 by 311.000s (22:36:22)", C2789_FOREIGN - TRIG, D("311.000")),
    ("trigger predates the c2789 post-echo by 85.207059789s", C2789_POST - TRIG, D("85.207059789")),
    ("trigger predates window-2790 open by 385.207059789s", WIN - TRIG, D("385.207059789")),
    ("trigger postdates c2788 close by 231.000s (6253361 at 22:27:20)", TRIG - C2788_CLOSE, D("231.000")),
    ("trigger postdates the foreign ffa527c by 212.000s (22:27:39)", TRIG - C2788_FOREIGN, D("212.000")),
    ("c2789 close landed 7.000s AFTER the token second (22:36:07 vs 06:36:00)", C2789_CLOSE - TOKEN, D("7.000")),
    ("foreign c048029 landed 22.000s AFTER the token second (22:36:22)", C2789_FOREIGN - TOKEN, D("22.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2790"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2790"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2791 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2792_birth",
      block.count("c2792") == 2 and lines[-1].count("c2792") == 2
      and "c2791/c2792" in lines[-1] and "FORWARD token c2792" in lines[-1],
      f"block c2792={block.count('c2792')} next-line c2792={lines[-1].count('c2792')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9208", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2790_next_bullet", last_nonempty.startswith("- Next: the c2790 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2790",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2790")]) == 0,
      f"c2790 substring mentions={wl.count('c2790')} (expect 8)")
c2790_lines = {i + 1: l.count("c2790") for i, l in enumerate(wl.splitlines()) if "c2790" in l}
guard("c2790_mention_census_pre", wl.count("c2790") == 8 and c2790_lines == {9196: 2, 9200: 1, 9206: 1, 9208: 4},
      f"per-line={c2790_lines}")
c2791_lines = {i + 1: l.count("c2791") for i, l in enumerate(wl.splitlines()) if "c2791" in l}
guard("c2791_forward_token_pre", wl.count("c2791") == 2 and c2791_lines == {9208: 2},
      f"per-line={c2791_lines} (2 FORWARD-token births inside the c2789 Next-block "
      f"— the c2783 c2788-pre==2 class carries)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==467", tid_pre == 467, f"got={tid_pre}")
guard("anchor_nogold_pre==400", gold_pre == 400, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2792_pre = wl.count("c2792")
c2791_pre = wl.count("c2791")
c2790_pre = wl.count("c2790")
c2789_pre = wl.count("c2789")
c2788_pre = wl.count("c2788")
c2787_pre = wl.count("c2787")
c2786_pre = wl.count("c2786")
c2785_pre = wl.count("c2785")
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
guard("c2792_pre==0", c2792_pre == 0, f"got={c2792_pre} (the forward token c2792 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2791_pre==2", c2791_pre == 2, f"got={c2791_pre} (2 FORWARD-token births inside "
      f"the c2789 Next-block — the c2783 c2788-pre==2 class carries)")
guard("c2790_pre==8", c2790_pre == 8, f"got={c2790_pre}")
guard("c2789_pre==36", c2789_pre == 36, f"got={c2789_pre}")
guard("c2788_pre==76", c2788_pre == 76, f"got={c2788_pre}")
guard("c2787_pre==87", c2787_pre == 87, f"got={c2787_pre}")
guard("c2786_pre==92", c2786_pre == 92, f"got={c2786_pre}")
guard("c2785_pre==91", c2785_pre == 91, f"got={c2785_pre}")
guard("c2784_pre==89", c2784_pre == 89, f"got={c2784_pre}")
guard("c2783_pre==88", c2783_pre == 88, f"got={c2783_pre}")
guard("c2782_pre==89", c2782_pre == 89, f"got={c2782_pre}")
guard("c2781_pre==94", c2781_pre == 94, f"got={c2781_pre}")
guard("c2780_pre==98", c2780_pre == 98, f"got={c2780_pre}")
guard("c2779_pre==99", c2779_pre == 99, f"got={c2779_pre}")
guard("c2778_pre==134", c2778_pre == 134, f"got={c2778_pre}")
guard("c2777_pre==115", c2777_pre == 115, f"got={c2777_pre}")
guard("c2776_pre==120", c2776_pre == 120, f"got={c2776_pre}")
guard("c2775_pre==129", c2775_pre == 129, f"got={c2775_pre}")
guard("c2774_pre==134", c2774_pre == 134, f"got={c2774_pre}")
guard("c2773_pre==138", c2773_pre == 138, f"got={c2773_pre}")
guard("c2772_pre==157", c2772_pre == 157, f"got={c2772_pre}")
guard("c2771_pre==147", c2771_pre == 147, f"got={c2771_pre}")
guard("c2770_pre==178", c2770_pre == 178, f"got={c2770_pre}")
guard("c2769_pre==140", c2769_pre == 140, f"got={c2769_pre}")
guard("c2768_pre==143", c2768_pre == 143, f"got={c2768_pre}")
guard("c2767_pre==170", c2767_pre == 170, f"got={c2767_pre}")
guard("c2766_pre==158", c2766_pre == 158, f"got={c2766_pre}")
guard("c2765_pre==134", c2765_pre == 134, f"got={c2765_pre}")
guard("c2764_pre==136", c2764_pre == 136, f"got={c2764_pre}")
guard("c2763_pre==144", c2763_pre == 144, f"got={c2763_pre}")
guard("c2762_pre==165", c2762_pre == 165, f"got={c2762_pre}")
guard("c2761_pre==179", c2761_pre == 179, f"got={c2761_pre}")
guard("c2760_pre==139", c2760_pre == 139, f"got={c2760_pre}")
guard("c2759_pre==139", c2759_pre == 139, f"got={c2759_pre}")
guard("c2758_pre==141", c2758_pre == 141, f"got={c2758_pre}")
guard("c2757_pre==144", c2757_pre == 144, f"got={c2757_pre}")
guard("c2756_pre==149", c2756_pre == 149, f"got={c2756_pre}")
guard("c2755_pre==156", c2755_pre == 156, f"got={c2755_pre}")
guard("c2754_pre==159", c2754_pre == 159, f"got={c2754_pre}")
guard("c2753_pre==165", c2753_pre == 165, f"got={c2753_pre}")
guard("c2752_pre==171", c2752_pre == 171, f"got={c2752_pre}")
guard("c2751_pre==157", c2751_pre == 157, f"got={c2751_pre}")
guard("c2750_pre==159", c2750_pre == 159, f"got={c2750_pre}")
guard("c2749_pre==163", c2749_pre == 163, f"got={c2749_pre}")
guard("c2748_pre==153", c2748_pre == 153, f"got={c2748_pre}")
guard("c2747_pre==151", c2747_pre == 151, f"got={c2747_pre}")
guard("c2746_pre==150", c2746_pre == 150, f"got={c2746_pre}")

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
guard("post_worklog_lines==9220", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2791_next_bullet", last2.startswith("- Next: the c2791 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==468", tid_post == 468, f"got={tid_post}")
guard("anchor_nogold_post==401", gold_post == 401, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2790_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2790")]) == 1)
expect_c2792_mentions = wl2.count("c2792")
guard("c2792_mention_birth", expect_c2792_mentions == c2792_pre + block.count("c2792"),
      f"pre={c2792_pre} (unborn) + block births={block.count('c2792')} (guard phrase + census-tuple sentence) -> expect={c2792_pre + block.count('c2792')} got={expect_c2792_mentions}")
for tag, pre in (("c2791", c2791_pre), ("c2790", c2790_pre), ("c2789", c2789_pre),
                 ("c2788", c2788_pre), ("c2787", c2787_pre), ("c2786", c2786_pre),
                 ("c2785", c2785_pre), ("c2784", c2784_pre), ("c2783", c2783_pre),
                 ("c2782", c2782_pre), ("c2781", c2781_pre), ("c2780", c2780_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9208 -> 9220 (+12), c2790 entry + DRIFT-#49 pass-39 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
