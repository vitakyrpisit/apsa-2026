#!/usr/bin/env python3
"""Guarded worklog append for the c2778 entry (12 lines).

Follows the append_cycle2777.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append abort precedent class). The ledger
arithmetic stays in the DECIMAL class: every ns-decomposition check is
Decimal-exact or Decimal-with-1e-6-tolerance on the utc-derived values.
Guards: python-timegm epoch cross-verification (31 Decimal-class checks incl.
the dd/INTERVAL/LAG/LATE ledger arithmetic, all echo decompositions, the
stamp-gap/token-gap cadence pair, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~0.7ms on the echo),
block structure (12 lines: separator, title, standard Task ID line, Steps
1-7, no-gold, Next bullet), the FORWARD-token guard (c2780 = 2 born inside
the Next bullet's guard phrase AND census-tuple sentence — the c2767..c2778
forward-token lessons), zero adds to the two standing post-#6/post-#15
anchor series (OCCURRENCE counting — the standing method), pre-state (9064
lines, tail = the c2778 Next bullet, zero serviced c2778 entries, c2778
mention census per-line {9052: 2, 9056: 3, 9064: 5}, anchors 455/388/60/28),
post-state (9076 lines, tail = the c2779 Next bullet, anchors 456/389/60/28).
Zero mid-line writes (append at EOF only).
"""
import calendar
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2778.txt"
EXPECT_BEFORE = 9064
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


POST = D("1793306281.565781844")    # c2778 post-echo (EPOCH-governs)
SCAN = D("1793306281.559")          # c2778 scanned_at (decimal)
TRIG = D("1793305568.000")          # c2778 trigger stamp (04:26:08 +08)
WIN = D("1793305998.468039333")     # window-2778 open (c2777 prophecy)
ECHO = D("1793306253.192795887")    # loop echo in-batch (EPOCH-governs)
C2777_SCAN = D("1793305698.461")    # c2777 scanned_at
C2777_POST = D("1793305698.468039333")  # c2777 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 04:26:08 +08 = 1793305568.000", dec_epoch(2026, 10, 29, 20, 26, 8), TRIG),
    ("c2777 trigger stamp 04:16:08 +08 = 1793304968.000", dec_epoch(2026, 10, 29, 20, 16, 8), D("1793304968.000")),
    ("stamp-gap 600.000s by stamp (04:16:08 -> 04:26:08)", TRIG - D("1793304968.000"), D("600.000")),
    ("token-gap 540.000s by token (0422 -> 0431)", dec_epoch(2026, 10, 29, 20, 31, 0) - dec_epoch(2026, 10, 29, 20, 22, 0), D("540.000")),
    ("loop echo ISO integer second 20:37:33 +0000", dec_epoch(2026, 10, 29, 20, 37, 33), D("1793306253.000")),
    ("loop echo EPOCH 1793306253.192795887 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 37, 33, 192795887), ECHO),
    ("capture pre-echo EPOCH 1793306279.970542211 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 37, 59, 970542211), D("1793306279.970542211")),
    ("post-echo ISO 20:38:01.565087927 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 20, 38, 1, 565087927), D("1793306281.565087927")),
    ("post-echo EPOCH 1793306281.565781844 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 38, 1, 565781844), POST),
    ("scanned_at 20:38:01.559 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 38, 1) + D("0.559"), SCAN),
    ("c2777 scanned_at 20:28:18.461 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 28, 18) + D("0.461"), C2777_SCAN),
    ("window-2778 open 04:33:18.468039333 +08", dec_epoch(2026, 10, 29, 20, 33, 18, 468039333), WIN),
    ("window-2779 open = post-echo + 300.000", POST + D("300.000"), D("1793306581.565781844")),
    ("echo post-c2777-post-echo +554.724756554", ECHO - C2777_POST, D("554.724756554")),
]
exact_checks = [
    ("skew decimal-exact +6.781844ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006781844")),
    ("echo_vs_window +254.724756554 (POST-WINDOW extends m6)", ECHO - WIN, D("254.724756554")),
    ("dd#352 = +283.098000000 (interval 583.098 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#350 print 577.398 - 300 = 277.398 and the dd#351 print 546.182 - 300 = 246.182)", SCAN - C2777_SCAN - D("300.000"), D("283.098")),
    ("INTERVAL#352 = 713.559", SCAN - TRIG, D("713.559")),
    ("LAG#352 = INTERVAL + dd - dd#351 = +750.475", (SCAN - TRIG) + (SCAN - C2777_SCAN - D("300.000")) - D("246.182"), D("750.475")),
    ("LATE#352 = trigger - window-open = -430.468039333", TRIG - WIN, D("-430.468039333")),
    ("CAPTURE_vs_window +283.097742511 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("283.097742511")),
    ("echo post-c2777-close +349.192795887 (e961185 at 20:31:44)", ECHO - D("1793305904.000"), D("349.192795887")),
    ("echo post-foreign-336d5f2 +337.192795887 (20:31:56)", ECHO - D("1793305916.000"), D("337.192795887")),
    ("stamp-to-echo 685.192795887 NOT deepest (821.276190288 stands)", ECHO - TRIG, D("685.192795887")),
    ("trigger predates c2777 close by 336.000s", D("1793305904.000") - TRIG, D("336.000")),
    ("trigger predates the foreign 336d5f2 by 348.000s (20:31:56)", D("1793305916.000") - TRIG, D("348.000")),
    ("trigger predates the c2777 post-echo by 130.468039333s", C2777_POST - TRIG, D("130.468039333")),
    ("trigger predates window-2778 open by 430.468039333s", WIN - TRIG, D("430.468039333")),
    ("trigger postdates c2776 close by 231.000s (1ed1bdd at 20:22:17)", TRIG - D("1793305337.000"), D("231.000")),
    ("trigger postdates the foreign 2b2bd7b by 216.000s (20:22:32)", TRIG - D("1793305352.000"), D("216.000")),
    ("c2777 capture pre-echo fired 128.772258846s after this stamp (the queue print)", D("1793305696.772258846") - TRIG, D("128.772258846")),
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
guard("block_title", lines[1].startswith("CYCLE 2778"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2778"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2779 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2780_birth",
      block.count("c2780") == 2 and lines[-1].count("c2780") == 2
      and "c2779/c2780" in lines[-1] and "FORWARD token c2780" in lines[-1],
      f"block c2780={block.count('c2780')} next-line c2780={lines[-1].count('c2780')} "
      f"(expect 2: guard phrase + census-tuple sentence, both inside the Next bullet)")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==9064", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2778_next_bullet", last_nonempty.startswith("- Next: the c2778 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2778",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2778")]) == 0,
      f"c2778 substring mentions={wl.count('c2778')} (expect 10)")
c2778_lines = {i + 1: l.count("c2778") for i, l in enumerate(wl.splitlines()) if "c2778" in l}
guard("c2778_mention_census_pre", wl.count("c2778") == 10 and c2778_lines == {9052: 2, 9056: 3, 9064: 5},
      f"per-line={c2778_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==455", tid_pre == 455, f"got={tid_pre}")
guard("anchor_nogold_pre==388", gold_pre == 388, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
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
guard("c2779_pre==2", c2779_pre == 2, f"got={c2779_pre}")
guard("c2778_pre==10", c2778_pre == 10, f"got={c2778_pre}")
guard("c2777_pre==34", c2777_pre == 34, f"got={c2777_pre}")
guard("c2776_pre==67", c2776_pre == 67, f"got={c2776_pre}")
guard("c2775_pre==77", c2775_pre == 77, f"got={c2775_pre}")
guard("c2774_pre==82", c2774_pre == 82, f"got={c2774_pre}")
guard("c2773_pre==86", c2773_pre == 86, f"got={c2773_pre}")
guard("c2772_pre==93", c2772_pre == 93, f"got={c2772_pre}")
guard("c2771_pre==95", c2771_pre == 95, f"got={c2771_pre}")
guard("c2770_pre==114", c2770_pre == 114, f"got={c2770_pre}")
guard("c2769_pre==98", c2769_pre == 98, f"got={c2769_pre}")
guard("c2768_pre==102", c2768_pre == 102, f"got={c2768_pre}")

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
guard("post_worklog_lines==9076", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2779_next_bullet", last2.startswith("- Next: the c2779 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==456", tid_post == 456, f"got={tid_post}")
guard("anchor_nogold_post==389", gold_post == 389, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2778_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2778")]) == 1)
expect_c2780_mentions = wl2.count("c2780")
guard("c2780_mention_birth", expect_c2780_mentions == block.count("c2780"),
      f"block births={block.count('c2780')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2780_mentions}")
for tag, pre in (("c2779", c2779_pre), ("c2778", c2778_pre), ("c2777", c2777_pre),
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
print(f"WORKLOG_APPEND_GREEN: 9064 -> 9076 (+12), c2778 entry + DRIFT-#49 pass-27 block landed ({n_guards}/{n_guards} guards)")
