#!/usr/bin/env python3
"""Guarded worklog append for the c2777 entry (12 lines).

Follows the append_cycle2776.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge abort precedent class). The ledger arithmetic stays
in the DECIMAL class: every ns-decomposition check is Decimal-exact or
Decimal-with-1e-6-tolerance on the utc-derived values. Guards: python-timegm
epoch cross-verification (31 Decimal-class checks incl. the
dd/INTERVAL/LAG/LATE ledger arithmetic, all echo decompositions, the
stamp-gap/token-gap cadence pair, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~0.7ms on the echo),
block structure (12 lines: separator, title, standard Task ID line, Steps
1-7, no-gold, Next bullet), zero adds to the two standing post-#6/post-#15
anchor series (OCCURRENCE counting — the standing method), pre-state (9052
lines, tail = the c2777 Next bullet, zero serviced c2777 entries, c2777
mention census per-line {9040: 2, 9044: 3, 9052: 5}, anchors 454/387/60/28),
post-state (9064 lines, tail = the c2778 Next bullet, anchors 455/388/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2777.txt"
EXPECT_BEFORE = 9052
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (Decimal-class, 31 checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = D("1793305698.468039333")    # c2777 post-echo (EPOCH-governs)
SCAN = D("1793305698.461")          # c2777 scanned_at (decimal)
TRIG = D("1793304968.000")          # c2777 trigger stamp (04:16:08 +08)
WIN = D("1793305452.285338098")     # window-2777 open (c2776 prophecy)
ECHO = D("1793305577.360336468")    # loop echo in-batch (EPOCH-governs)
C2776_SCAN = D("1793305152.279")    # c2776 scanned_at
C2776_POST = D("1793305152.285338098")  # c2776 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 04:16:08 +08 = 1793304968.000", dec_epoch(2026, 10, 29, 20, 16, 8), TRIG),
    ("c2776 trigger stamp 04:06:08 +08 = 1793304368.000", dec_epoch(2026, 10, 29, 20, 6, 8), D("1793304368.000")),
    ("stamp-gap 600.000s by stamp (04:06:08 -> 04:16:08)", TRIG - D("1793304368.000"), D("600.000")),
    ("token-gap 540.000s by token (0413 -> 0422)", dec_epoch(2026, 10, 29, 20, 22, 0) - dec_epoch(2026, 10, 29, 20, 13, 0), D("540.000")),
    ("loop echo ISO integer second 20:26:17 +0000", dec_epoch(2026, 10, 29, 20, 26, 17), D("1793305577.000")),
    ("loop echo EPOCH 1793305577.360336468 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 26, 17, 360336468), ECHO),
    ("capture pre-echo EPOCH 1793305696.772258846 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 28, 16, 772258846), D("1793305696.772258846")),
    ("post-echo ISO 20:28:18.467371658 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 20, 28, 18, 467371658), D("1793305698.467371658")),
    ("post-echo EPOCH 1793305698.468039333 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 28, 18, 468039333), POST),
    ("scanned_at 20:28:18.461 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 28, 18) + D("0.461"), SCAN),
    ("c2776 scanned_at 20:19:12.279 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 19, 12) + D("0.279"), C2776_SCAN),
    ("window-2777 open 04:24:12.285338098 +08", dec_epoch(2026, 10, 29, 20, 24, 12, 285338098), WIN),
    ("window-2778 open = post-echo + 300.000", POST + D("300.000"), D("1793305998.468039333")),
    ("echo post-c2776-post-echo +425.074998370", ECHO - C2776_POST, D("425.074998370")),
]
exact_checks = [
    ("skew decimal-exact +7.039333ms (EPOCH-governs decomposition)", POST - SCAN, D("0.007039333")),
    ("echo_vs_window +125.074998370 (POST-WINDOW extends m5)", ECHO - WIN, D("125.074998370")),
    ("dd#351 = +246.182000000 (interval 546.182 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#348 print 555.221 - 300 = 255.221, the dd#349 print 583.815 - 300 = 283.815 and the dd#350 print 577.398 - 300 = 277.398)", SCAN - C2776_SCAN - D("300.000"), D("246.182")),
    ("INTERVAL#351 = 730.461", SCAN - TRIG, D("730.461")),
    ("LAG#351 = INTERVAL + dd - dd#350 = +699.245", (SCAN - TRIG) + (SCAN - C2776_SCAN - D("300.000")) - D("277.398"), D("699.245")),
    ("LATE#351 = trigger - window-open = -484.285338098", TRIG - WIN, D("-484.285338098")),
    ("CAPTURE_vs_window +246.182701235 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("246.182701235")),
    ("echo post-c2776-close +240.360336468 (1ed1bdd at 20:22:17)", ECHO - D("1793305337.000"), D("240.360336468")),
    ("echo post-foreign-2b2bd7b +225.360336468 (20:22:32)", ECHO - D("1793305352.000"), D("225.360336468")),
    ("stamp-to-echo 609.360336468 NOT deepest (821.276190288 stands)", ECHO - TRIG, D("609.360336468")),
    ("trigger predates c2776 close by 369.000s", D("1793305337.000") - TRIG, D("369.000")),
    ("trigger predates the foreign 2b2bd7b by 384.000s (20:22:32)", D("1793305352.000") - TRIG, D("384.000")),
    ("trigger predates the c2776 post-echo by 184.285338098s", C2776_POST - TRIG, D("184.285338098")),
    ("trigger predates window-2777 open by 484.285338098s", WIN - TRIG, D("484.285338098")),
    ("trigger postdates c2775 close by 196.000s (932b4cc at 20:12:52)", TRIG - D("1793304772.000"), D("196.000")),
    ("trigger postdates the foreign f9ecf31 by 181.000s (20:13:07)", TRIG - D("1793304787.000"), D("181.000")),
    ("c2776 capture pre-echo fired 182.622099681s after this stamp (the queue print)", D("1793305150.622099681") - TRIG, D("182.622099681")),
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
guard("block_title", lines[1].startswith("CYCLE 2777"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2777"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2778 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==9052", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2777_next_bullet", last_nonempty.startswith("- Next: the c2777 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2777",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2777")]) == 0,
      f"c2777 substring mentions={wl.count('c2777')} (expect 10)")
c2777_lines = {i + 1: l.count("c2777") for i, l in enumerate(wl.splitlines()) if "c2777" in l}
guard("c2777_mention_census_pre", wl.count("c2777") == 10 and c2777_lines == {9040: 2, 9044: 3, 9052: 5},
      f"per-line={c2777_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==454", tid_pre == 454, f"got={tid_pre}")
guard("anchor_nogold_pre==387", gold_pre == 387, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2778_pre = wl.count("c2778")
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
guard("c2778_pre==2", c2778_pre == 2, f"got={c2778_pre}")
guard("c2776_pre==34", c2776_pre == 34, f"got={c2776_pre}")
guard("c2775_pre==69", c2775_pre == 69, f"got={c2775_pre}")
guard("c2774_pre==77", c2774_pre == 77, f"got={c2774_pre}")
guard("c2773_pre==81", c2773_pre == 81, f"got={c2773_pre}")
guard("c2772_pre==87", c2772_pre == 87, f"got={c2772_pre}")
guard("c2771_pre==90", c2771_pre == 90, f"got={c2771_pre}")
guard("c2770_pre==108", c2770_pre == 108, f"got={c2770_pre}")
guard("c2769_pre==93", c2769_pre == 93, f"got={c2769_pre}")
guard("c2768_pre==97", c2768_pre == 97, f"got={c2768_pre}")

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
guard("post_worklog_lines==9064", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2778_next_bullet", last2.startswith("- Next: the c2778 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==455", tid_post == 455, f"got={tid_post}")
guard("anchor_nogold_post==388", gold_post == 388, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2777_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2777")]) == 1)
expect_c2779_mentions = wl2.count("c2779")
guard("c2779_mention_birth", expect_c2779_mentions == block.count("c2779"),
      f"block births={block.count('c2779')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2779_mentions}")
for tag, pre in (("c2778", c2778_pre), ("c2777", 10), ("c2776", c2776_pre),
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
print(f"WORKLOG_APPEND_GREEN: 9052 -> 9064 (+12), c2777 entry + DRIFT-#49 pass-26 block landed ({n_guards}/{n_guards} guards)")
