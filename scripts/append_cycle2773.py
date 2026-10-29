#!/usr/bin/env python3
"""Guarded worklog append for the c2773 entry (12 lines).

Follows the append_cycle2772.py precedent (attempt-1 GREEN, zero aborts three
cycles running after the c2766/c2769 abort lessons): ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. THIS RUN IS
ATTEMPT-2 for c2773: attempt-1 aborted PRE-MUTATION — two harness constants
hand-transposed +20s each (the c2770-close epoch 1793302244.000 written for
the correct 1793302224.000 and the 02d651d epoch 1793302254.000 for the
correct 1793302234.000), BOTH caught by the Decimal-exact timegm guards,
worklog UNTOUCHED (the c2769 TRIG stale-epoch typo precedent class; the
decimal-exact guard design is the last line of defense). The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770-abort
precedent class). THIS CYCLE the ledger arithmetic migrates from float to
DECIMAL: the float pre-verification printed 6.108760834ms against the
Decimal-exact 6.108753ms decomposition (a ~7.8e-6 noise the old 1e-6
tolerance class would have tripped) — every ns-decomposition check below is
Decimal-exact or Decimal-with-1e-6-tolerance on the utc-derived values.
Guards: python-timegm epoch cross-verification (30 Decimal-class checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic, all three echo decompositions,
and the stamp-gap/token-gap cadence pair — the c2766 attempt-1 abort lesson:
the SKEW check must use the EPOCH-governs print's own ns decomposition, the
ISO/EPOCH clock reads differ ~0.67ms on the pre-echo and ~5.4ms on the
capture post-echo), block structure (12 lines: separator, title, standard
Task ID line, Steps 1-7, no-gold, Next bullet), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9004 lines, tail = the c2773 Next bullet, zero serviced c2773
entries, c2773 mention census per-line {8992: 2, 8996: 3, 9004: 5}, anchors
450/383/60/28), post-state (9016 lines, tail = the c2774 Next bullet,
anchors 451/384/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2773.txt"
EXPECT_BEFORE = 9004
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


POST = D("1793303435.851108753")    # c2773 post-echo (EPOCH-governs)
SCAN = D("1793303435.845")          # c2773 scanned_at (decimal)
TRIG = D("1793302568.000")          # c2773 trigger stamp (03:36:08 +08)
WIN = D("1793303239.999424683")     # window-2773 open (c2772 prophecy)
ECHO = D("1793303302.549820439")    # loop echo post-read-phase (EPOCH-governs)
C2772_SCAN = D("1793302939.940")    # c2772 scanned_at
C2772_POST = D("1793302939.999424683")  # c2772 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 03:36:08 +08 = 1793302568.000", dec_epoch(2026, 10, 29, 19, 36, 8), TRIG),
    ("c2772 trigger stamp 03:31:07 +08 = 1793302267.000", dec_epoch(2026, 10, 29, 19, 31, 7), D("1793302267.000")),
    ("stamp-gap 301s by stamp (03:31:07 -> 03:36:08)", TRIG - D("1793302267.000"), D("301.000")),
    ("token-gap 420s by token (0338 -> 0345)", dec_epoch(2026, 10, 29, 19, 45, 0) - dec_epoch(2026, 10, 29, 19, 38, 0), D("420.000")),
    ("loop echo ISO integer second 19:48:22 +0000", dec_epoch(2026, 10, 29, 19, 48, 22), D("1793303302.000")),
    ("loop echo EPOCH 1793303302.549820439 (EPOCH-governs)", dec_epoch(2026, 10, 29, 19, 48, 22, 549820439), ECHO),
    ("pre-echo EPOCH 1793303433.808400498 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 19, 50, 33, 808400498), D("1793303433.808400498")),
    ("post-echo ISO 19:50:35.850464462 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 19, 50, 35, 850464462), D("1793303435.850464462")),
    ("post-echo EPOCH 1793303435.851108753 (EPOCH-governs)", dec_epoch(2026, 10, 29, 19, 50, 35, 851108753), POST),
    ("scanned_at 19:50:35.845 +0000 (decimal)", dec_epoch(2026, 10, 29, 19, 50, 35) + D("0.845"), SCAN),
    ("c2772 scanned_at 19:42:19.940 +0000 (decimal)", dec_epoch(2026, 10, 29, 19, 42, 19) + D("0.940"), C2772_SCAN),
    ("window-2773 open 03:47:19.999424683 +08", dec_epoch(2026, 10, 29, 19, 47, 19, 999424683), WIN),
    ("window-2774 open = post-echo + 300.000", POST + D("300.000"), D("1793303735.851108753")),
    ("echo post-c2772-post-echo +362.550395756", ECHO - C2772_POST, D("362.550395756")),
]
exact_checks = [
    ("skew decimal-exact +6.108753ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006108753")),
    ("echo_vs_window +62.550395756 (POST-WINDOW flip re-opens m1)", ECHO - WIN, D("62.550395756")),
    ("dd#347 = +195.905000000 (interval 495.905 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#345 print 482.587 - 300 = 182.587 and the dd#346 print 407.711 - 300 = 107.711)", SCAN - C2772_SCAN - D("300.000"), D("195.905")),
    ("INTERVAL#347 = 867.845", SCAN - TRIG, D("867.845")),
    ("LAG#347 = INTERVAL + dd - dd#346 = +956.039", (SCAN - TRIG) + (SCAN - C2772_SCAN - D("300.000")) - D("107.711"), D("956.039")),
    ("LATE#347 = trigger - window-open = -671.999424683", TRIG - WIN, D("-671.999424683")),
    ("CAPTURE_vs_window +195.851684070 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("195.851684070")),
    ("echo post-c2772-close +209.549820439 (b774591 at 19:44:53)", ECHO - D("1793303093.000"), D("209.549820439")),
    ("echo post-foreign-0539b68 +193.549820439 (19:45:09)", ECHO - D("1793303109.000"), D("193.549820439")),
    ("trigger predates c2772 close by 525.000s", D("1793303093.000") - TRIG, D("525.000")),
    ("trigger predates the foreign 0539b68 by 541.000s (19:45:09)", D("1793303109.000") - TRIG, D("541.000")),
    ("trigger predates the c2772 post-echo by 371.999424683s", C2772_POST - TRIG, D("371.999424683")),
    ("trigger predates c2771 close by 133.000s (71880e8 at 19:38:21)", D("1793302701.000") - TRIG, D("133.000")),
    ("trigger predates the foreign dd48816 by 146.000s (19:38:34)", D("1793302714.000") - TRIG, D("146.000")),
    ("trigger postdates c2770 close by 344.000s (5622953 at 19:30:24)", TRIG - D("1793302224.000"), D("344.000")),
    ("trigger postdates the foreign 02d651d by 334.000s (19:30:34)", TRIG - D("1793302234.000"), D("334.000")),
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
guard("block_title", lines[1].startswith("CYCLE 2773"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2773"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2774 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==9004", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2773_next_bullet", last_nonempty.startswith("- Next: the c2773 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2773",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2773")]) == 0,
      f"c2773 substring mentions={wl.count('c2773')} (expect 10)")
c2773_lines = {i + 1: l.count("c2773") for i, l in enumerate(wl.splitlines()) if "c2773" in l}
guard("c2773_mention_census_pre", wl.count("c2773") == 10 and c2773_lines == {8992: 2, 8996: 3, 9004: 5},
      f"per-line={c2773_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==450", tid_pre == 450, f"got={tid_pre}")
guard("anchor_nogold_pre==383", gold_pre == 383, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2774_pre = wl.count("c2774")
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
guard("c2774_pre==2", c2774_pre == 2, f"got={c2774_pre}")
guard("c2772_pre==31", c2772_pre == 31, f"got={c2772_pre}")
guard("c2771_pre==60", c2771_pre == 60, f"got={c2771_pre}")
guard("c2770_pre==78", c2770_pre == 78, f"got={c2770_pre}")
guard("c2769_pre==71", c2769_pre == 71, f"got={c2769_pre}")

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
guard("post_worklog_lines==9016", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2774_next_bullet", last2.startswith("- Next: the c2774 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==451", tid_post == 451, f"got={tid_post}")
guard("anchor_nogold_post==384", gold_post == 384, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2773_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2773")]) == 1)
expect_c2775_mentions = wl2.count("c2775")
guard("c2775_mention_birth", expect_c2775_mentions == block.count("c2775"),
      f"block births={block.count('c2775')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2775_mentions}")
for tag, pre in (("c2774", c2774_pre), ("c2773", 10), ("c2772", c2772_pre),
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
print(f"WORKLOG_APPEND_GREEN: 9004 -> 9016 (+12), c2773 entry + DRIFT-#49 pass-22 block landed ({n_guards}/{n_guards} guards)")
