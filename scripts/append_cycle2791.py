#!/usr/bin/env python3
"""Guarded worklog append for the c2791 entry (12 lines).

Follows the append_cycle2790.py precedent — ALL asserts precede the
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
window-2791 EPOCH-governs render check, the window-2792 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~2.16ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2793 = 2 born inside the Next bullet's guard phrase AND census-tuple
sentence — the c2767..c2791 forward-token lessons; NOTE the c2793 pre-count
is 0 (unborn) while the c2792 pre-count is 2 — the c2783 c2788-pre==2 class
CARRIES this cycle: the c2792 forward token was born TWICE inside the c2790
Next-block (measured at census time: per-line {9220: 2}), NOT the c2785
c2787-pre==0 class), zero adds to the two standing post-#6/post-#15 anchor
series (OCCURRENCE counting — the standing method), pre-state (9220 lines,
tail = the c2791 Next bullet, zero serviced c2791 entries, c2791 mention
census per-line {9208: 2, 9212: 1, 9218: 1, 9220: 4}, c2792 = 2 per-line
{9220: 2}, anchors 468/401/60/28), post-state (9232 lines, tail = the c2792
Next bullet, anchors 469/402/60/28). Zero mid-line writes (append at EOF
only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2791.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9220
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


POST = D("1793314222.291848898")    # c2791 post-echo (EPOCH-governs)
SCAN = D("1793314222.240")          # c2791 scanned_at (decimal)
TRIG = D("1793313371.000")          # c2791 trigger stamp (06:36:11 +08)
WIN = D("1793314009.181138247")     # window-2791 open (c2790 prophecy EPOCH)
ECHO = D("1793314074.412459312")    # loop echo #512 mid-session POST read (EPOCH-governs)
ECHO_PRE = D("1793314074.411053642")  # loop echo #512 PRE read (the bracket)
C2790_SCAN = D("1793313709.175")    # c2790 scanned_at
C2790_POST = D("1793313709.181138247")  # c2790 post-echo
C2790_CLOSE = D("1793313913.000")   # c2790 close e4a79df (22:45:13Z)
C2790_FOREIGN = D("1793313928.000") # foreign 3b69581 (22:45:28Z)
C2790_TRIG = D("1793313071.000")    # c2790 trigger stamp (06:31:11 +08)
C2789_CLOSE = D("1793313367.000")   # c2789 close 2af9fd7 (22:36:07Z)
C2789_FOREIGN = D("1793313382.000") # foreign c048029 (22:36:22Z)
TOKEN = D("1793313900.000")         # token 0645 (06:45:00Z)
C2790_TOKEN = D("1793313360.000")   # token 0636 (06:36:00Z)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 06:36:11 +08 = 1793313371.000", dec_epoch(2026, 10, 29, 22, 36, 11), TRIG),
    ("c2790 trigger stamp 06:31:11 +08 = 1793313071.000", dec_epoch(2026, 10, 29, 22, 31, 11), C2790_TRIG),
    ("stamp-gap 300.000s by stamp (06:31:11 -> 06:36:11; the 300 print REPEATS, 8 priors)", TRIG - C2790_TRIG, D("300.000")),
    ("token-gap 540.000s by token (0636 -> 0645; the 540 print REPEATS, 18 priors)", TOKEN - C2790_TOKEN, D("540.000")),
    ("token-vs-stamp +529.000 (06:36:11 -> 06:45:00; the +529 print is NEW)", TOKEN - TRIG, D("529.000")),
    ("c2790 close e4a79df 22:45:13Z = 1793313913.000", dec_epoch(2026, 10, 29, 22, 45, 13), C2790_CLOSE),
    ("foreign 3b69581 22:45:28Z = 1793313928.000", dec_epoch(2026, 10, 29, 22, 45, 28), C2790_FOREIGN),
    ("c2789 close 2af9fd7 22:36:07Z = 1793313367.000", dec_epoch(2026, 10, 29, 22, 36, 7), C2789_CLOSE),
    ("foreign c048029 22:36:22Z = 1793313382.000", dec_epoch(2026, 10, 29, 22, 36, 22), C2789_FOREIGN),
    ("loop echo ISO integer second 22:47:54 +0000", dec_epoch(2026, 10, 29, 22, 47, 54), D("1793314074.000")),
    ("loop echo EPOCH 1793314074.412459312 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 22, 47, 54, 412459312), ECHO),
    ("loop echo PRE read 1793314074.411053642 (the bracket)", dec_epoch(2026, 10, 29, 22, 47, 54, 411053642), ECHO_PRE),
    ("capture pre-echo EPOCH 1793314220.549403216 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 50, 20, 549403216), D("1793314220.549403216")),
    ("post-echo ISO 22:50:22.289692475 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 22, 50, 22, 289692475), D("1793314222.289692475")),
    ("post-echo EPOCH 1793314222.291848898 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 50, 22, 291848898), POST),
    ("scanned_at 22:50:22.240 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 50, 22) + D("0.240"), SCAN),
    ("c2790 scanned_at 22:41:49.175 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 41, 49) + D("0.175"), C2790_SCAN),
    ("c2790 post-echo EPOCH 1793313709.181138247", dec_epoch(2026, 10, 29, 22, 41, 49, 181138247), C2790_POST),
    ("window-2791 open 06:46:49.181138247 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 22, 46, 49, 181138247), WIN),
    ("window-2792 open = post-echo + 300.000", POST + D("300.000"), D("1793314522.291848898")),
    ("echo post-c2790-post-echo +365.231321065", ECHO - C2790_POST, D("365.231321065")),
]
exact_checks = [
    ("skew decimal-exact +51.848898ms (EPOCH-governs decomposition; ABOVE-10 FLIP)", POST - SCAN, D("0.051848898")),
    ("echo_vs_window +65.231321065 (POST-WINDOW re-opens m1)", ECHO - WIN, D("65.231321065")),
    ("dd#365 = +213.065000000 (interval 513.065 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#359 print 544.537 - 300 = 244.537 and the dd#360 print 574.472 - 300 = 274.472 and the dd#361 print 523.771 - 300 = 223.771 and the dd#362 print 445.372 - 300 = 145.372 and the dd#363 print 545.490 - 300 = 245.490 and the dd#364 print 552.974 - 300 = 252.974)", SCAN - C2790_SCAN - D("300.000"), D("213.065")),
    ("dd formula re-verification: 544.537 - 300 = 244.537", D("544.537") - D("300.000"), D("244.537")),
    ("dd formula re-verification: 574.472 - 300 = 274.472", D("574.472") - D("300.000"), D("274.472")),
    ("dd formula re-verification: 523.771 - 300 = 223.771", D("523.771") - D("300.000"), D("223.771")),
    ("dd formula re-verification: 445.372 - 300 = 145.372", D("445.372") - D("300.000"), D("145.372")),
    ("dd formula re-verification: 545.490 - 300 = 245.490", D("545.490") - D("300.000"), D("245.490")),
    ("dd formula re-verification: 552.974 - 300 = 252.974", D("552.974") - D("300.000"), D("252.974")),
    ("INTERVAL#365 = 851.240", SCAN - TRIG, D("851.240")),
    ("LAG#365 = INTERVAL + dd - dd#364 = +811.331", (SCAN - TRIG) + (SCAN - C2790_SCAN - D("300.000")) - D("252.974"), D("811.331")),
    ("LATE#365 = trigger - window-open = -638.181138247", TRIG - WIN, D("-638.181138247")),
    ("CAPTURE_vs_window +213.110710651 (POST-WINDOW; echo POST — the BOTH-POST print returns)", POST - WIN, D("213.110710651")),
    ("capture-vs-echo +147.879389586", POST - ECHO, D("147.879389586")),
    ("capture post-c2790-post-echo +513.110710651", POST - C2790_POST, D("513.110710651")),
    ("echo post-c2790-close +161.412459312 (e4a79df at 22:45:13)", ECHO - C2790_CLOSE, D("161.412459312")),
    ("echo post-foreign-3b69581 +146.412459312 (22:45:28)", ECHO - C2790_FOREIGN, D("146.412459312")),
    ("stamp-to-echo 703.412459312 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("703.412459312")),
    ("trigger predates c2790 close by 542.000s", C2790_CLOSE - TRIG, D("542.000")),
    ("trigger predates the foreign 3b69581 by 557.000s (22:45:28)", C2790_FOREIGN - TRIG, D("557.000")),
    ("trigger predates the c2790 post-echo by 338.181138247s", C2790_POST - TRIG, D("338.181138247")),
    ("trigger predates window-2791 open by 638.181138247s", WIN - TRIG, D("638.181138247")),
    ("trigger postdates c2789 close by 4.000s (2af9fd7 at 22:36:07)", TRIG - C2789_CLOSE, D("4.000")),
    ("trigger predates the foreign c048029 by 11.000s (22:36:22)", C2789_FOREIGN - TRIG, D("11.000")),
    ("c2790 close landed 13.000s AFTER the token second (22:45:13 vs 06:45:00)", C2790_CLOSE - TOKEN, D("13.000")),
    ("foreign 3b69581 landed 28.000s AFTER the token second (22:45:28)", C2790_FOREIGN - TOKEN, D("28.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2791"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2791"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2792 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2793_birth",
      block.count("c2793") == 2 and lines[-1].count("c2793") == 2
      and "c2792/c2793" in lines[-1] and "FORWARD token c2793" in lines[-1],
      f"block c2793={block.count('c2793')} next-line c2793={lines[-1].count('c2793')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9220", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2791_next_bullet", last_nonempty.startswith("- Next: the c2791 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2791",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2791")]) == 0,
      f"c2791 substring mentions={wl.count('c2791')} (expect 8)")
c2791_lines = {i + 1: l.count("c2791") for i, l in enumerate(wl.splitlines()) if "c2791" in l}
guard("c2791_mention_census_pre", wl.count("c2791") == 8 and c2791_lines == {9208: 2, 9212: 1, 9218: 1, 9220: 4},
      f"per-line={c2791_lines}")
c2792_lines = {i + 1: l.count("c2792") for i, l in enumerate(wl.splitlines()) if "c2792" in l}
guard("c2792_forward_token_pre", wl.count("c2792") == 2 and c2792_lines == {9220: 2},
      f"per-line={c2792_lines} (2 FORWARD-token births inside the c2790 Next-block "
      f"— the c2783 c2788-pre==2 class carries)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==468", tid_pre == 468, f"got={tid_pre}")
guard("anchor_nogold_pre==401", gold_pre == 401, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2793_pre = wl.count("c2793")
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
guard("c2793_pre==0", c2793_pre == 0, f"got={c2793_pre} (the forward token c2793 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2792_pre==2", c2792_pre == 2, f"got={c2792_pre} (2 FORWARD-token births inside "
      f"the c2790 Next-block — the c2783 c2788-pre==2 class carries)")
guard("c2791_pre==8", c2791_pre == 8, f"got={c2791_pre}")
guard("c2790_pre==35", c2790_pre == 35, f"got={c2790_pre}")
guard("c2789_pre==74", c2789_pre == 74, f"got={c2789_pre}")
guard("c2788_pre==87", c2788_pre == 87, f"got={c2788_pre}")
guard("c2787_pre==91", c2787_pre == 91, f"got={c2787_pre}")
guard("c2786_pre==97", c2786_pre == 97, f"got={c2786_pre}")
guard("c2785_pre==95", c2785_pre == 95, f"got={c2785_pre}")
guard("c2784_pre==93", c2784_pre == 93, f"got={c2784_pre}")
guard("c2783_pre==93", c2783_pre == 93, f"got={c2783_pre}")
guard("c2782_pre==93", c2782_pre == 93, f"got={c2782_pre}")
guard("c2781_pre==98", c2781_pre == 98, f"got={c2781_pre}")
guard("c2780_pre==102", c2780_pre == 102, f"got={c2780_pre}")
guard("c2779_pre==103", c2779_pre == 103, f"got={c2779_pre}")
guard("c2778_pre==139", c2778_pre == 139, f"got={c2778_pre}")
guard("c2777_pre==119", c2777_pre == 119, f"got={c2777_pre}")
guard("c2776_pre==124", c2776_pre == 124, f"got={c2776_pre}")
guard("c2775_pre==133", c2775_pre == 133, f"got={c2775_pre}")
guard("c2774_pre==138", c2774_pre == 138, f"got={c2774_pre}")
guard("c2773_pre==142", c2773_pre == 142, f"got={c2773_pre}")
guard("c2772_pre==161", c2772_pre == 161, f"got={c2772_pre}")
guard("c2771_pre==151", c2771_pre == 151, f"got={c2771_pre}")
guard("c2770_pre==183", c2770_pre == 183, f"got={c2770_pre}")
guard("c2769_pre==143", c2769_pre == 143, f"got={c2769_pre}")
guard("c2768_pre==146", c2768_pre == 146, f"got={c2768_pre}")
guard("c2767_pre==175", c2767_pre == 175, f"got={c2767_pre}")
guard("c2766_pre==162", c2766_pre == 162, f"got={c2766_pre}")
guard("c2765_pre==137", c2765_pre == 137, f"got={c2765_pre}")
guard("c2764_pre==139", c2764_pre == 139, f"got={c2764_pre}")
guard("c2763_pre==147", c2763_pre == 147, f"got={c2763_pre}")
guard("c2762_pre==169", c2762_pre == 169, f"got={c2762_pre}")
guard("c2761_pre==183", c2761_pre == 183, f"got={c2761_pre}")
guard("c2760_pre==142", c2760_pre == 142, f"got={c2760_pre}")
guard("c2759_pre==142", c2759_pre == 142, f"got={c2759_pre}")
guard("c2758_pre==144", c2758_pre == 144, f"got={c2758_pre}")
guard("c2757_pre==147", c2757_pre == 147, f"got={c2757_pre}")
guard("c2756_pre==152", c2756_pre == 152, f"got={c2756_pre}")
guard("c2755_pre==159", c2755_pre == 159, f"got={c2755_pre}")
guard("c2754_pre==162", c2754_pre == 162, f"got={c2754_pre}")
guard("c2753_pre==168", c2753_pre == 168, f"got={c2753_pre}")
guard("c2752_pre==174", c2752_pre == 174, f"got={c2752_pre}")
guard("c2751_pre==160", c2751_pre == 160, f"got={c2751_pre}")
guard("c2750_pre==162", c2750_pre == 162, f"got={c2750_pre}")
guard("c2749_pre==166", c2749_pre == 166, f"got={c2749_pre}")
guard("c2748_pre==156", c2748_pre == 156, f"got={c2748_pre}")
guard("c2747_pre==154", c2747_pre == 154, f"got={c2747_pre}")
guard("c2746_pre==154", c2746_pre == 154, f"got={c2746_pre}")

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
guard("post_worklog_lines==9232", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2792_next_bullet", last2.startswith("- Next: the c2792 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==469", tid_post == 469, f"got={tid_post}")
guard("anchor_nogold_post==402", gold_post == 402, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2791_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2791")]) == 1)
expect_c2793_mentions = wl2.count("c2793")
guard("c2793_mention_birth", expect_c2793_mentions == c2793_pre + block.count("c2793"),
      f"pre={c2793_pre} (unborn) + block births={block.count('c2793')} (guard phrase + census-tuple sentence) -> expect={c2793_pre + block.count('c2793')} got={expect_c2793_mentions}")
for tag, pre in (("c2792", c2792_pre), ("c2791", c2791_pre), ("c2790", c2790_pre),
                 ("c2789", c2789_pre), ("c2788", c2788_pre), ("c2787", c2787_pre),
                 ("c2786", c2786_pre), ("c2785", c2785_pre), ("c2784", c2784_pre),
                 ("c2783", c2783_pre), ("c2782", c2782_pre), ("c2781", c2781_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9220 -> 9232 (+12), c2791 entry + DRIFT-#49 pass-40 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
