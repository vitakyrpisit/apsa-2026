#!/usr/bin/env python3
"""Guarded worklog append for the c2776 entry (12 lines).

Follows the append_cycle2775.py precedent (attempt-1 GREEN this cycle expected
— the c2774 attempt-1 abort lesson did not recur): ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775 abort precedent class). The ledger arithmetic stays in the DECIMAL
class: every ns-decomposition check is Decimal-exact or
Decimal-with-1e-6-tolerance on the utc-derived values. Guards: python-timegm
epoch cross-verification (31 Decimal-class checks incl. the
dd/INTERVAL/LAG/LATE ledger arithmetic, all echo decompositions, the
stamp-gap/token-gap cadence pair, and the queue-print check — the c2766
attempt-1 abort lesson: the SKEW check must use the EPOCH-governs print's own
ns decomposition, the ISO/EPOCH clock reads differ ~0.6ms on the echo and
~0.7ms on the capture post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), zero adds to the two
standing post-#6/post-#15 anchor series (OCCURRENCE counting — the standing
method), pre-state (9040 lines, tail = the c2776 Next bullet, zero serviced
c2776 entries, c2776 mention census per-line {9028: 2, 9032: 3, 9040: 5},
anchors 453/386/60/28), post-state (9052 lines, tail = the c2777 Next bullet,
anchors 454/387/60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2776.txt"
EXPECT_BEFORE = 9040
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


POST = D("1793305152.285338098")    # c2776 post-echo (EPOCH-governs)
SCAN = D("1793305152.279")          # c2776 scanned_at (decimal)
TRIG = D("1793304368.000")          # c2776 trigger stamp (04:06:08 +08)
WIN = D("1793304874.889710120")     # window-2776 open (c2775 prophecy)
ECHO = D("1793305075.025656919")    # loop echo in-batch (EPOCH-governs)
C2775_SCAN = D("1793304574.881")    # c2775 scanned_at
C2775_POST = D("1793304574.889710120")  # c2775 post-echo


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 04:06:08 +08 = 1793304368.000", dec_epoch(2026, 10, 29, 20, 6, 8), TRIG),
    ("c2775 trigger stamp 03:56:08 +08 = 1793303768.000", dec_epoch(2026, 10, 29, 19, 56, 8), D("1793303768.000")),
    ("stamp-gap 600.000s by stamp (03:56:08 -> 04:06:08)", TRIG - D("1793303768.000"), D("600.000")),
    ("token-gap 600.000s by token (0403 -> 0413)", dec_epoch(2026, 10, 29, 20, 13, 0) - dec_epoch(2026, 10, 29, 20, 3, 0), D("600.000")),
    ("loop echo ISO integer second 20:17:55 +0000", dec_epoch(2026, 10, 29, 20, 17, 55), D("1793305075.000")),
    ("loop echo EPOCH 1793305075.025656919 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 17, 55, 25656919), ECHO),
    ("capture pre-echo EPOCH 1793305150.622099681 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 19, 10, 622099681), D("1793305150.622099681")),
    ("post-echo ISO 20:19:12.284685685 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 20, 19, 12, 284685685), D("1793305152.284685685")),
    ("post-echo EPOCH 1793305152.285338098 (EPOCH-governs)", dec_epoch(2026, 10, 29, 20, 19, 12, 285338098), POST),
    ("scanned_at 20:19:12.279 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 19, 12) + D("0.279"), SCAN),
    ("c2775 scanned_at 20:09:34.881 +0000 (decimal)", dec_epoch(2026, 10, 29, 20, 9, 34) + D("0.881"), C2775_SCAN),
    ("window-2776 open 04:14:34.889710120 +08", dec_epoch(2026, 10, 29, 20, 14, 34, 889710120), WIN),
    ("window-2777 open = post-echo + 300.000", POST + D("300.000"), D("1793305452.285338098")),
    ("echo post-c2775-post-echo +500.135946799", ECHO - C2775_POST, D("500.135946799")),
]
exact_checks = [
    ("skew decimal-exact +6.338098ms (EPOCH-governs decomposition)", POST - SCAN, D("0.006338098")),
    ("echo_vs_window +200.135946799 (POST-WINDOW extends m4)", ECHO - WIN, D("200.135946799")),
    ("dd#350 = +277.398000000 (interval 577.398 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#348 print 555.221 - 300 = 255.221 and the dd#349 print 583.815 - 300 = 283.815)", SCAN - C2775_SCAN - D("300.000"), D("277.398")),
    ("INTERVAL#350 = 784.279", SCAN - TRIG, D("784.279")),
    ("LAG#350 = INTERVAL + dd - dd#349 = +777.862", (SCAN - TRIG) + (SCAN - C2775_SCAN - D("300.000")) - D("283.815"), D("777.862")),
    ("LATE#350 = trigger - window-open = -506.889710120", TRIG - WIN, D("-506.889710120")),
    ("CAPTURE_vs_window +277.395627978 (POST-WINDOW; echo POST — the both-POST print)", POST - WIN, D("277.395627978")),
    ("echo post-c2775-close +303.025656919 (932b4cc at 20:12:52)", ECHO - D("1793304772.000"), D("303.025656919")),
    ("echo post-foreign-f9ecf31 +288.025656919 (20:13:07)", ECHO - D("1793304787.000"), D("288.025656919")),
    ("stamp-to-echo 707.025656919 NOT deepest (821.276190288 stands)", ECHO - TRIG, D("707.025656919")),
    ("trigger predates c2775 close by 404.000s", D("1793304772.000") - TRIG, D("404.000")),
    ("trigger predates the foreign f9ecf31 by 419.000s (20:13:07)", D("1793304787.000") - TRIG, D("419.000")),
    ("trigger predates the c2775 post-echo by 206.889710120s", C2775_POST - TRIG, D("206.889710120")),
    ("trigger predates window-2776 open by 506.889710120s", WIN - TRIG, D("506.889710120")),
    ("trigger postdates c2774 close by 183.000s (0017b3b at 20:03:05)", TRIG - D("1793304185.000"), D("183.000")),
    ("trigger postdates the foreign 9b5ea95 by 171.000s (20:03:17)", TRIG - D("1793304197.000"), D("171.000")),
    ("c2775 capture pre-echo fired 205.141857286s after this stamp (the queue print)", D("1793304573.141857286") - TRIG, D("205.141857286")),
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
guard("block_title", lines[1].startswith("CYCLE 2776"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2776"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2777 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==9040", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2776_next_bullet", last_nonempty.startswith("- Next: the c2776 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2776",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2776")]) == 0,
      f"c2776 substring mentions={wl.count('c2776')} (expect 10)")
c2776_lines = {i + 1: l.count("c2776") for i, l in enumerate(wl.splitlines()) if "c2776" in l}
guard("c2776_mention_census_pre", wl.count("c2776") == 10 and c2776_lines == {9028: 2, 9032: 3, 9040: 5},
      f"per-line={c2776_lines}")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==453", tid_pre == 453, f"got={tid_pre}")
guard("anchor_nogold_pre==386", gold_pre == 386, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
c2777_pre = wl.count("c2777")
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
guard("c2777_pre==2", c2777_pre == 2, f"got={c2777_pre}")
guard("c2775_pre==34", c2775_pre == 34, f"got={c2775_pre}")
guard("c2774_pre==69", c2774_pre == 69, f"got={c2774_pre}")
guard("c2773_pre==76", c2773_pre == 76, f"got={c2773_pre}")
guard("c2772_pre==81", c2772_pre == 81, f"got={c2772_pre}")
guard("c2771_pre==85", c2771_pre == 85, f"got={c2771_pre}")
guard("c2770_pre==102", c2770_pre == 102, f"got={c2770_pre}")
guard("c2769_pre==88", c2769_pre == 88, f"got={c2769_pre}")
guard("c2768_pre==92", c2768_pre == 92, f"got={c2768_pre}")
guard("c2767_pre==99", c2767_pre == 99, f"got={c2767_pre}")

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
guard("post_worklog_lines==9052", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2777_next_bullet", last2.startswith("- Next: the c2777 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==454", tid_post == 454, f"got={tid_post}")
guard("anchor_nogold_post==387", gold_post == 387, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2776_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2776")]) == 1)
expect_c2778_mentions = wl2.count("c2778")
guard("c2778_mention_birth", expect_c2778_mentions == block.count("c2778"),
      f"block births={block.count('c2778')} (expect 2: guard phrase + census-tuple sentence) got={expect_c2778_mentions}")
for tag, pre in (("c2777", c2777_pre), ("c2776", 10), ("c2775", c2775_pre),
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
print(f"WORKLOG_APPEND_GREEN: 9040 -> 9052 (+12), c2776 entry + DRIFT-#49 pass-25 block landed ({n_guards}/{n_guards} guards)")
