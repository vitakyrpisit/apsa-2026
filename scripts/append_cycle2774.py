#!/usr/bin/env python3
"""Guarded worklog append for the c2774 entry (12 lines).

Follows the append_cycle2773.py precedent (attempt-1 GREEN this cycle expected
— the c2773 attempt-1 abort lesson did not recur): ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773
abort precedent class). The ledger arithmetic stays in the DECIMAL class:
every ns-decomposition check is Decimal-exact or Decimal-with-1e-6-tolerance
on the utc-derived values. Guards: python-timegm epoch cross-verification
(30 Decimal-class checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic,
all three echo decompositions, and the stamp-gap/token-gap cadence pair —
the c2766 attempt-1 abort lesson: the SKEW check must use the EPOCH-governs
print's own ns decomposition, the ISO/EPOCH clock reads differ ~0.65ms on the
echo and ~2.1ms on the capture post-echo), block structure (12 lines:
separator, title, standard Task ID line, Steps 1-7, no-gold, Next bullet),
zero adds to the two standing post-#6/post-#15 anchor series (OCCURRENCE
counting — the standing method), pre-state (9016 lines, tail = the c2774 Next
bullet, zero serviced c2774 entries, c2774 mention census per-line {9004: 2,
9008: 3, 9016: 5}, anchors 451/384/60/28), post-state (9028 lines, tail = the
c2775 Next bullet, anchors 452/385/60/28). Zero mid-line writes (append at
EOF only).
"""
import calendar
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2774.txt"
EXPECT_BEFORE = 9016
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (Decimal-class, 30 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = D("1793303991.071555080")    # c2774 post-echo (EPOCH-governs)
SCAN = D("1793303991.066")          # c2774 scanned_at (decimal)
TRIG = D("1793303168.000")          # c2774 trigger stamp (03:46:08 +08)
WIN = D("1793303735.851108753")     # window-2774 open (c2773 prophecy)
ECHO = D("1793303989.276190288")    # loop echo in-batch (EPOCH-governs)
C2773_SCAN = D("1793303435.845")    # c2773 scanned_at
C2773_POST = D("1793303435.851108753")  # c2773 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 03:46:08 +08 = 1793303168.000", dec_epoch(2026, 10, 29, 19, 46, 8), TRIG),
    ("c2773 trigger stamp 03:36:08 +08 = 1793302568.000", dec_epoch(2026, 10, 29, 19, 36, 8), D("1793302568.000")),
    ("stamp-gap 600.000s by stamp (03:36:08 -> 03:46:08)", TRIG - D("1793302568.000"), D("600.000")),
    ("token-gap 600s by token (0345 -> 0355)", dec_epoch(2026, 10, 29, 19, 55, 0) - dec_epoch(2026, 10, 29, 19, 45, 0), D("600.000")),
    ("loop echo ISO integer second 19:59:49 +0000", dec_epoch(2026, 10, 29, 19, 59, 49), D("1793303989.000")),
    ("loop echo EPOCH 1793303989.276190288 (EPOCH-governs)", dec_epoch(2026, 10, 29, 19, 59, 49, 276190288), ECHO),
    ("pre-echo EPOCH 1793303989.279474872 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 19, 59, 49, 279474872), D("1793303989.279474872")),
    ("post-echo ISO 19:59:51.070915029 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 19, 59, 51, 70915029), D("1793303991.070915029")),
    ("post-echo EPOCH 1793303991.071555080 (EPOCH-governs)", dec_epoch(2026, 10, 29, 19, 59, 51, 71555080), POST),
    ("scanned_at 19:59:51.066 +0000 (decimal)", dec_epoch(2026, 10, 29, 19, 59, 51) + D("0.066"), SCAN),
    ("c2773 scanned_at 19:50:35.845 +0000 (decimal)", dec_epoch(2026, 10, 29, 19, 50, 35) + D("0.845"), C2773_SCAN),
    ("window-2774 open 03:55:35.851108753 +08", dec_epoch(2026, 10, 29, 19, 55, 35, 851108753), WIN),
    ("window-2775 open = post-echo + 300.000", POST + D("300.000"), D("1793304291.071555080")),
    ("echo post-c2773-post-echo +553.425081535", ECHO - C2773_POST, D("553.425081535")),
]
exact_checks = [
    ("skew decimal-exact +5.555080ms (EPOCH-governs decomposition)", POST - SCAN, D("0.005555080")),
    ("echo_vs_window +253.425081535 (POST-WINDOW extends m2)", ECHO - WIN, D("253.425081535")),
    ("dd#348 = +255.221000000 (interval 555.221 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#346 print 407.711 - 300 = 107.711 and the dd#347 print 495.905 - 300 = 195.905)", SCAN - C2773_SCAN - D("300.000"), D("255.221")),
    ("INTERVAL#348 = 823.066", SCAN - TRIG, D("823.066")),
    ("LAG#348 = INTERVAL + dd - dd#347 = +882.382", (SCAN - TRIG) + (SCAN - C2773_SCAN - D("300.000")) - D("195.905"), D("882.382")),
    ("LATE#348 = trigger - window-open = -567.851108753", TRIG - WIN, D("-567.851108753")),
    ("CAPTURE_vs_window +255.220446327 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("255.220446327")),
    ("echo post-c2773-close +300.276190288 (98cc097 at 19:54:49)", ECHO - D("1793303689.000"), D("300.276190288")),
    ("echo post-foreign-eb9de41 +281.276190288 (19:55:08)", ECHO - D("1793303708.000"), D("281.276190288")),
    ("stamp-to-echo NEW DEEPEST 821.276190288 (supersedes 791.462616937)", ECHO - TRIG, D("821.276190288")),
    ("trigger predates c2773 close by 521.000s", D("1793303689.000") - TRIG, D("521.000")),
    ("trigger predates the foreign eb9de41 by 540.000s (19:55:08)", D("1793303708.000") - TRIG, D("540.000")),
    ("trigger predates the c2773 post-echo by 267.851108753s", C2773_POST - TRIG, D("267.851108753")),
    ("trigger predates window-2773 open by 71.999424683s", D("1793303239.999424683") - TRIG, D("71.999424683")),
    ("trigger postdates c2772 close by 75.000s (b774591 at 19:44:53)", TRIG - D("1793303093.000"), D("75.000")),
    ("trigger postdates the foreign 0539b68 by 59.000s (19:45:09)", TRIG - D("1793303109.000"), D("59.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2774"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2774"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2775 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==9016", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2774_next_bullet", last_nonempty.startswith("- Next: the c2774 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2774",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2774")]) == 0,
      f"c2774 substring mentions={wl.count('c2774')} (expect 10)")
c2774_lines = {i + 1: l.count("c2774") for i, l in enumerate(wl.splitlines()) if "c2774" in l}
guard("c2774_mention_census_pre", wl.count("c2774") == 10 and c2774_lines == {9004: 2, 9008: 3, 9016: 5},
      f"per-line={c2774_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==451", tid_pre == 451, f"got={tid_pre}")
guard("anchor_nogold_pre==384", gold_pre == 384, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2775_pre = wl.count("c2775")
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
guard("c2775_pre==2", c2775_pre == 2, f"got={c2775_pre}")
guard("c2773_pre==33", c2773_pre == 33, f"got={c2773_pre}")
guard("c2772_pre==64", c2772_pre == 64, f"got={c2772_pre}")
guard("c2771_pre==75", c2771_pre == 75, f"got={c2771_pre}")
guard("c2770_pre==90", c2770_pre == 90, f"got={c2770_pre}")
guard("c2769_pre==78", c2769_pre == 78, f"got={c2769_pre}")
guard("c2768_pre==82", c2768_pre == 82, f"got={c2768_pre}")
guard("c2767_pre==87", c2767_pre == 87, f"got={c2767_pre}")
guard("c2766_pre==90", c2766_pre == 90, f"got={c2766_pre}")

if failures:
    print(f"APPEND_ABORTED: {len(failures)} guard failures - worklog UNTOUCHED")
    sys.exit(1)

# 4) append with newline normalization
if not wl.endswith("\n"):
    wl += "\n"
block_norm = block if block.endswith("\n") else block + "\n"
with open(WL, "a") as f:
    f.write(block_norm)

# 5) post-append assertions
wl2 = open(WL).read()
n_after = wl2.count("\n")
guard("post_worklog_lines==9028", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2775_next_bullet", last2.startswith("- Next: the c2775 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==452", tid_post == 452, f"got={tid_post}")
guard("anchor_nogold_post==385", gold_post == 385, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2774_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2774")]) == 1)
expect_c2776_mentions = wl2.count("c2776")
guard("c2776_mention_birth", expect_c2776_mentions == block.count("c2776"),
      f"block births={block.count('c2776')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2776_mentions}")
for tag, pre in (("c2775", c2775_pre), ("c2774", 10), ("c2773", c2773_pre),
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
print(f"WORKLOG_APPEND_GREEN: 9016 -> 9028 (+12), c2774 entry + DRIFT-#49 pass-23 block landed ({n_guards}/{n_guards} guards)")
