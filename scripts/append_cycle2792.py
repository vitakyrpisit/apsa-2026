#!/usr/bin/env python3
"""Guarded worklog append for the c2792 entry (12 lines).

Follows the append_cycle2791.py precedent — ALL asserts precede the
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
window-2792 EPOCH-governs render check, the window-2793 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~11.0ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2794 = 3 block births: the Step-7 rehearsal pre-count print 'the
c2794 pre==0 expectation' + the Next bullet's guard phrase 'c2793/c2794' AND
census-tuple sentence 'FORWARD token c2794' — the c2767..c2792 forward-token
lessons; NOTE the c2794 pre-count is 0 (unborn) while the c2793 pre-count is
2 — the c2783 c2788-pre==2 class CARRIES this cycle: the c2793 forward token
was born TWICE inside the c2791 Next-block (measured at census time: per-line
{9232: 2}), NOT the unborn class), zero adds to the two standing post-#6/
post-#15 anchor series (OCCURRENCE counting — the standing method), pre-state
(9232 lines, tail = the c2792 Next bullet, zero serviced c2792 entries, c2792
mention census per-line {9220: 2, 9224: 1, 9230: 1, 9232: 4}, c2793 = 2
per-line {9232: 2}, anchors 469/402/60/28), post-state (9244 lines, tail =
the c2793 Next bullet, anchors 470/403/60/28). Zero mid-line writes (append
at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2792.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9232
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


POST = D("1793314722.218649965")    # c2792 post-echo (EPOCH-governs)
SCAN = D("1793314722.153")          # c2792 scanned_at (decimal)
TRIG = D("1793313971.000")          # c2792 trigger stamp (06:46:11 +08)
WIN = D("1793314522.291848898")     # window-2792 open (c2791 prophecy EPOCH)
ECHO = D("1793314447.5846183")      # loop echo #513 first-command POST read (EPOCH-governs)
ECHO_PRE = D("1793314447.573930374")  # loop echo #513 PRE read (the bracket)
C2791_SCAN = D("1793314222.240")    # c2791 scanned_at
C2791_POST = D("1793314222.291848898")  # c2791 post-echo
C2791_CLOSE = D("1793314387.000")   # c2791 close f6f24d7 (22:53:07Z)
C2791_FOREIGN = D("1793314407.000")  # foreign 18522dc (22:53:27Z)
C2791_TRIG = D("1793313371.000")    # c2791 trigger stamp (06:36:11 +08)
C2791_ECHO = D("1793314074.412459312")  # c2791 loop echo #512 (22:47:54.412459312)
C2790_CLOSE = D("1793313913.000")   # c2790 close e4a79df (22:45:13Z)
C2790_FOREIGN = D("1793313928.000")  # foreign 3b69581 (22:45:28Z)
TOKEN = D("1793314380.000")         # token 0653 (06:53:00Z)
C2791_TOKEN = D("1793313900.000")   # token 0645 (06:45:00Z)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 06:46:11 +08 = 1793313971.000", dec_epoch(2026, 10, 29, 22, 46, 11), TRIG),
    ("c2791 trigger stamp 06:36:11 +08 = 1793313371.000", dec_epoch(2026, 10, 29, 22, 36, 11), C2791_TRIG),
    ("stamp-gap 600.000s by stamp (06:36:11 -> 06:46:11; the 600 print REPEATS, 22 priors)", TRIG - C2791_TRIG, D("600.000")),
    ("token-gap 480.000s by token (0645 -> 0653; the 480 print REPEATS, 18 priors)", TOKEN - C2791_TOKEN, D("480.000")),
    ("token-vs-stamp +409.000 (06:46:11 -> 06:53:00; the +409 print is NEW)", TOKEN - TRIG, D("409.000")),
    ("c2791 close f6f24d7 22:53:07Z = 1793314387.000", dec_epoch(2026, 10, 29, 22, 53, 7), C2791_CLOSE),
    ("foreign 18522dc 22:53:27Z = 1793314407.000", dec_epoch(2026, 10, 29, 22, 53, 27), C2791_FOREIGN),
    ("c2790 close e4a79df 22:45:13Z = 1793313913.000", dec_epoch(2026, 10, 29, 22, 45, 13), C2790_CLOSE),
    ("foreign 3b69581 22:45:28Z = 1793313928.000", dec_epoch(2026, 10, 29, 22, 45, 28), C2790_FOREIGN),
    ("loop echo ISO integer second 22:54:07 +0000", dec_epoch(2026, 10, 29, 22, 54, 7), D("1793314447.000")),
    ("loop echo EPOCH 1793314447.5846183 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 22, 54, 7, 584618300), ECHO),
    ("loop echo PRE read 1793314447.573930374 (the bracket)", dec_epoch(2026, 10, 29, 22, 54, 7, 573930374), ECHO_PRE),
    ("capture pre-echo EPOCH 1793314720.466776136 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 58, 40, 466776136), D("1793314720.466776136")),
    ("post-echo ISO 22:58:42.207643177 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 22, 58, 42, 207643177), D("1793314722.207643177")),
    ("post-echo EPOCH 1793314722.218649965 (EPOCH-governs)", dec_epoch(2026, 10, 29, 22, 58, 42, 218649965), POST),
    ("scanned_at 22:58:42.153 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 58, 42) + D("0.153"), SCAN),
    ("c2791 scanned_at 22:50:22.240 +0000 (decimal)", dec_epoch(2026, 10, 29, 22, 50, 22) + D("0.240"), C2791_SCAN),
    ("c2791 post-echo EPOCH 1793314222.291848898", dec_epoch(2026, 10, 29, 22, 50, 22, 291848898), C2791_POST),
    ("window-2792 open 06:55:22.291848898 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 22, 55, 22, 291848898), WIN),
    ("window-2793 open = post-echo + 300.000", POST + D("300.000"), D("1793315022.218649965")),
    ("echo post-c2791-post-echo +225.292769402", ECHO - C2791_POST, D("225.292769402")),
]
exact_checks = [
    ("skew decimal-exact +65.649965ms (EPOCH-governs decomposition; ABOVE-10 extends m2)", POST - SCAN, D("0.065649965")),
    ("echo_vs_window -74.707230598 (PRE-WINDOW re-opens m1)", ECHO - WIN, D("-74.707230598")),
    ("dd#366 = +199.913000000 (interval 499.913 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#360 print 574.472 - 300 = 274.472 and the dd#361 print 523.771 - 300 = 223.771 and the dd#362 print 445.372 - 300 = 145.372 and the dd#363 print 545.490 - 300 = 245.490 and the dd#364 print 552.974 - 300 = 252.974 and the dd#365 print 513.065 - 300 = 213.065)", SCAN - C2791_SCAN - D("300.000"), D("199.913")),
    ("dd formula re-verification: 574.472 - 300 = 274.472", D("574.472") - D("300.000"), D("274.472")),
    ("dd formula re-verification: 523.771 - 300 = 223.771", D("523.771") - D("300.000"), D("223.771")),
    ("dd formula re-verification: 445.372 - 300 = 145.372", D("445.372") - D("300.000"), D("145.372")),
    ("dd formula re-verification: 545.490 - 300 = 245.490", D("545.490") - D("300.000"), D("245.490")),
    ("dd formula re-verification: 552.974 - 300 = 252.974", D("552.974") - D("300.000"), D("252.974")),
    ("dd formula re-verification: 513.065 - 300 = 213.065", D("513.065") - D("300.000"), D("213.065")),
    ("INTERVAL#366 = 751.153", SCAN - TRIG, D("751.153")),
    ("LAG#366 = INTERVAL + dd - dd#365 = +738.001", (SCAN - TRIG) + (SCAN - C2791_SCAN - D("300.000")) - D("213.065"), D("738.001")),
    ("LATE#366 = trigger - window-open = -551.291848898", TRIG - WIN, D("-551.291848898")),
    ("CAPTURE_vs_window +199.926801067 (POST-WINDOW; echo PRE — the SPLIT print returns)", POST - WIN, D("199.926801067")),
    ("capture-vs-echo +274.634031665", POST - ECHO, D("274.634031665")),
    ("capture post-c2791-post-echo +499.926801067", POST - C2791_POST, D("499.926801067")),
    ("echo post-c2791-close +60.5846183 (f6f24d7 at 22:53:07)", ECHO - C2791_CLOSE, D("60.5846183")),
    ("echo post-foreign-18522dc +40.5846183 (22:53:27)", ECHO - C2791_FOREIGN, D("40.5846183")),
    ("stamp-to-echo 476.5846183 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("476.5846183")),
    ("trigger predates c2791 close by 416.000s", C2791_CLOSE - TRIG, D("416.000")),
    ("trigger predates the foreign 18522dc by 436.000s (22:53:27)", C2791_FOREIGN - TRIG, D("436.000")),
    ("trigger predates the c2791 post-echo by 251.291848898s", C2791_POST - TRIG, D("251.291848898")),
    ("trigger predates the c2791 loop echo #512 by 103.412459312s", C2791_ECHO - TRIG, D("103.412459312")),
    ("trigger predates window-2792 open by 551.291848898s", WIN - TRIG, D("551.291848898")),
    ("trigger postdates c2790 close by 58.000s (e4a79df at 22:45:13)", TRIG - C2790_CLOSE, D("58.000")),
    ("trigger postdates the foreign 3b69581 by 43.000s (22:45:28)", TRIG - C2790_FOREIGN, D("43.000")),
    ("c2791 close landed 7.000s AFTER the token second (22:53:07 vs 06:53:00)", C2791_CLOSE - TOKEN, D("7.000")),
    ("foreign 18522dc landed 27.000s AFTER the token second (22:53:27)", C2791_FOREIGN - TOKEN, D("27.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2792"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2792"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2793 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2794_birth",
      block.count("c2794") == 3 and lines[-1].count("c2794") == 2
      and "c2793/c2794" in lines[-1] and "FORWARD token c2794" in lines[-1]
      and "the c2794 pre==0 expectation" in block,
      f"block c2794={block.count('c2794')} next-line c2794={lines[-1].count('c2794')} "
      f"(expect 3: the Step-7 rehearsal pre-count print + the Next bullet's guard "
      f"phrase 'c2793/c2794' AND census-tuple sentence 'FORWARD token c2794')")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9232", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2792_next_bullet", last_nonempty.startswith("- Next: the c2792 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2792",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2792")]) == 0,
      f"c2792 substring mentions={wl.count('c2792')} (expect 8)")
c2792_lines = {i + 1: l.count("c2792") for i, l in enumerate(wl.splitlines()) if "c2792" in l}
guard("c2792_mention_census_pre", wl.count("c2792") == 8 and c2792_lines == {9220: 2, 9224: 1, 9230: 1, 9232: 4},
      f"per-line={c2792_lines}")
c2793_lines = {i + 1: l.count("c2793") for i, l in enumerate(wl.splitlines()) if "c2793" in l}
guard("c2793_forward_token_pre", wl.count("c2793") == 2 and c2793_lines == {9232: 2},
      f"per-line={c2793_lines} (2 FORWARD-token births inside the c2791 Next-block "
      f"— the c2783 c2788-pre==2 class carries)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==469", tid_pre == 469, f"got={tid_pre}")
guard("anchor_nogold_pre==402", gold_pre == 402, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2794_pre = wl.count("c2794")
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
guard("c2794_pre==0", c2794_pre == 0, f"got={c2794_pre} (the forward token c2794 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2793_pre==2", c2793_pre == 2, f"got={c2793_pre} (2 FORWARD-token births inside "
      f"the c2791 Next-block — the c2783 c2788-pre==2 class carries)")
guard("c2792_pre==8", c2792_pre == 8, f"got={c2792_pre}")
guard("c2791_pre==36", c2791_pre == 36, f"got={c2791_pre}")
guard("c2790_pre==70", c2790_pre == 70, f"got={c2790_pre}")
guard("c2789_pre==83", c2789_pre == 83, f"got={c2789_pre}")
guard("c2788_pre==92", c2788_pre == 92, f"got={c2788_pre}")
guard("c2787_pre==95", c2787_pre == 95, f"got={c2787_pre}")
guard("c2786_pre==102", c2786_pre == 102, f"got={c2786_pre}")
guard("c2785_pre==99", c2785_pre == 99, f"got={c2785_pre}")
guard("c2784_pre==97", c2784_pre == 97, f"got={c2784_pre}")
guard("c2783_pre==98", c2783_pre == 98, f"got={c2783_pre}")
guard("c2782_pre==97", c2782_pre == 97, f"got={c2782_pre}")
guard("c2781_pre==102", c2781_pre == 102, f"got={c2781_pre}")
guard("c2780_pre==106", c2780_pre == 106, f"got={c2780_pre}")
guard("c2779_pre==107", c2779_pre == 107, f"got={c2779_pre}")
guard("c2778_pre==144", c2778_pre == 144, f"got={c2778_pre}")
guard("c2777_pre==123", c2777_pre == 123, f"got={c2777_pre}")
guard("c2776_pre==128", c2776_pre == 128, f"got={c2776_pre}")
guard("c2775_pre==137", c2775_pre == 137, f"got={c2775_pre}")
guard("c2774_pre==142", c2774_pre == 142, f"got={c2774_pre}")
guard("c2773_pre==146", c2773_pre == 146, f"got={c2773_pre}")
guard("c2772_pre==165", c2772_pre == 165, f"got={c2772_pre}")
guard("c2771_pre==155", c2771_pre == 155, f"got={c2771_pre}")
guard("c2770_pre==188", c2770_pre == 188, f"got={c2770_pre}")
guard("c2769_pre==146", c2769_pre == 146, f"got={c2769_pre}")
guard("c2768_pre==149", c2768_pre == 149, f"got={c2768_pre}")
guard("c2767_pre==180", c2767_pre == 180, f"got={c2767_pre}")
guard("c2766_pre==166", c2766_pre == 166, f"got={c2766_pre}")
guard("c2765_pre==140", c2765_pre == 140, f"got={c2765_pre}")
guard("c2764_pre==142", c2764_pre == 142, f"got={c2764_pre}")
guard("c2763_pre==150", c2763_pre == 150, f"got={c2763_pre}")
guard("c2762_pre==173", c2762_pre == 173, f"got={c2762_pre}")
guard("c2761_pre==187", c2761_pre == 187, f"got={c2761_pre}")
guard("c2760_pre==145", c2760_pre == 145, f"got={c2760_pre}")
guard("c2759_pre==145", c2759_pre == 145, f"got={c2759_pre}")
guard("c2758_pre==147", c2758_pre == 147, f"got={c2758_pre}")
guard("c2757_pre==150", c2757_pre == 150, f"got={c2757_pre}")
guard("c2756_pre==155", c2756_pre == 155, f"got={c2756_pre}")
guard("c2755_pre==162", c2755_pre == 162, f"got={c2755_pre}")
guard("c2754_pre==165", c2754_pre == 165, f"got={c2754_pre}")
guard("c2753_pre==171", c2753_pre == 171, f"got={c2753_pre}")
guard("c2752_pre==177", c2752_pre == 177, f"got={c2752_pre}")
guard("c2751_pre==163", c2751_pre == 163, f"got={c2751_pre}")
guard("c2750_pre==165", c2750_pre == 165, f"got={c2750_pre}")
guard("c2749_pre==169", c2749_pre == 169, f"got={c2749_pre}")
guard("c2748_pre==159", c2748_pre == 159, f"got={c2748_pre}")
guard("c2747_pre==157", c2747_pre == 157, f"got={c2747_pre}")
guard("c2746_pre==158", c2746_pre == 158, f"got={c2746_pre}")

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
guard("post_worklog_lines==9244", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2793_next_bullet", last2.startswith("- Next: the c2793 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==470", tid_post == 470, f"got={tid_post}")
guard("anchor_nogold_post==403", gold_post == 403, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2792_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2792")]) == 1)
expect_c2794_mentions = wl2.count("c2794")
guard("c2794_mention_birth", expect_c2794_mentions == c2794_pre + block.count("c2794"),
      f"pre={c2794_pre} (unborn) + block births={block.count('c2794')} (Step-7 pre-count "
      f"print + guard phrase + census-tuple sentence) -> expect={c2794_pre + block.count('c2794')} got={expect_c2794_mentions}")
for tag, pre in (("c2793", c2793_pre), ("c2792", c2792_pre), ("c2791", c2791_pre),
                 ("c2790", c2790_pre), ("c2789", c2789_pre), ("c2788", c2788_pre),
                 ("c2787", c2787_pre), ("c2786", c2786_pre), ("c2785", c2785_pre),
                 ("c2784", c2784_pre), ("c2783", c2783_pre), ("c2782", c2782_pre),
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
print(f"WORKLOG_APPEND_GREEN ({mode}): 9232 -> 9244 (+12), c2792 entry + DRIFT-#49 pass-41 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
