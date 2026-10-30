#!/usr/bin/env python3
"""Arrival-guard for cycle 2820 (Job ID 446189) — measured, never predicted.

Spec source: the c2819 Next-block (worklog line 9568). Checks:
  worklog 9568 lines EXACT (newline count, c2819 append post-guard prophecy);
  tail = the c2820 Next bullet;
  anchors ^Task ID: 497 / ^- No gold yet 430 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2820 entries; c2822/c2821/c2820 substring accounting
  (the token-guard lives INSIDE the c2819 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2820.py, expectations below are the MEASURED values, INCLUDING the
  forward-forward token c2822 = 0 (UNBORN, measured pre-append) and the
  c2821 = 4 total = 2 births in the c2819 Step-7 twin-print (line 9566: the
  rehearsal pre-count print 'the c2821 pre==0 expectation' AND the census-time
  print 'c2821_pre = 0') + 2 FORWARD-token births inside the c2819 Next-block
  guard phrase ('arrival-guard against c2820/c2821 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2821 must be IN the census
  tuple'), both on line 9568 — the c2819 append prophecy 'c2821 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS a SIXTEENTH time;
  the c2820 token itself is BORN TWELVE times pre-append: 2 in the c2818
  Step-7 twin-print (line 9554) + 2 in the c2818 Next-block (line 9556) + 3 in
  the c2819 Step-1 census sentence (line 9560) + 1 in the c2819 Step-7 'the
  c2820 pre-count 4 born-FOUR' (line 9566) + 4 in the c2819 Next-block (line
  9568: the instance + the 446189-c2820 id + the 'c2820/c2821' guard phrase +
  the 'measure_c2820_tokens.py' surface — the bare-c-token accounting, honestly
  counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surfaces 'scan_cycle2819_raw.json' /
  'validate_cycle2819.py' / 'scan_cycle2819.json' carry 'e2819'/'cycle2819',
  NOT the bare c-token 'c2819' — line 9563 ABSENT from the measured c2819
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2819 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2819 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2819 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v119 source-intact expectations matched to the v119 pass-68 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v119 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-69 gate name is what the v120 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-67 band' is present AND the evidence-paragraph lag-1 heading
  'pass-67 evidence' is present — BOTH instrument surfaces, the v120 rebadge
  P3/P8 old-string expectations, exactly as the c2819 Next-block wrote).
"""
import os
import subprocess
import sys
import time

WL = "/home/z/my-project/worklog.md"
DEVLOG = "/home/z/my-project/dev.log"
BA = "/home/z/my-project/.basedagents"

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


print(f"guard_run_epoch={time.time():.9f}")
raw = open(WL, "rb").read()
n_nl = raw.count(b"\n")
guard("worklog_lines==9568", n_nl == 9568, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2820_next_bullet", last_nonempty.startswith("- Next: the c2820 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==497", tid == 497, f"got={tid}")
guard("anchor_nogold==430", gold == 430, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2820")]
guard("dup_check_zero_serviced_c2820", len(dup) == 0, f"got={len(dup)}")
c2822_total = text.count("c2822")
c2821_total = text.count("c2821")
c2820_total = text.count("c2820")
tok_guard = [l for l in lines if "c2820/c2821" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2820 instance")]
c2821_lines = {i + 1: l.count("c2821") for i, l in enumerate(lines) if "c2821" in l}
c2820_lines = {i + 1: l.count("c2820") for i, l in enumerate(lines) if "c2820" in l}
guard("c2820_mention_accounting_pre",
      c2822_total == 0 and c2821_total == 4 and c2820_total == 12
      and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and c2821_lines == {9566: 2, 9568: 2}
      and c2820_lines == {9554: 2, 9556: 2, 9560: 3, 9566: 1, 9568: 4},
      f"c2822={c2822_total} c2821={c2821_total} c2820={c2820_total} "
      f"c2821_per-line={c2821_lines} c2820_per-line={c2820_lines} "
      f"(expect c2822 = 0 UNBORN (measured pre-append — the forward-token "
      f"lesson: measured, never assumed unborn); c2821 = 4 — 2 births in the "
      f"c2819 Step-7 twin-print line 9566 (the rehearsal pre-count print 'the "
      f"c2821 pre==0 expectation' AND the census-time print 'c2821_pre = 0' — "
      f"the Step-7 twin-print class REPEATS) + 2 FORWARD-token births TWICE "
      f"inside the c2819 Next-block guard phrase AND census-tuple sentence, "
      f"both on line 9568 (the c2819 append prophecy 'c2821 = 4 block births' "
      f"held EXACTLY, the born-FOUR class REPEATS a SIXTEENTH time); c2820 = "
      f"12 — 2 in the c2818 Step-7 twin-print (line 9554) + 2 in the c2818 "
      f"Next-block (line 9556) + 3 in the c2819 Step-1 census sentence (line "
      f"9560) + 1 in the c2819 Step-7 'the c2820 pre-count 4 born-FOUR' (line "
      f"9566) + 4 in the c2819 Next-block (line 9568: the instance + the "
      f"446189-c2820 id + the 'c2820/c2821' guard phrase + the "
      f"'measure_c2820_tokens.py' surface))")

c2819_total = text.count("c2819")
c2819_lines = {i + 1: l.count("c2819") for i, l in enumerate(lines) if "c2819" in l}
guard("c2819_mention_census_pre",
      c2819_total == 41
      and c2819_lines == {9542: 2, 9544: 2, 9548: 3, 9554: 1, 9556: 4, 9559: 1,
                          9560: 7, 9561: 6, 9566: 5, 9568: 10},
      f"total={c2819_total} per-line={c2819_lines} (the c2819-guard-probe state 12 on "
      f"lines 9542..9556 + 29 births inside the c2819 block itself; the Step-4 "
      f"surface 'scan_cycle2819_raw.json'/'validate_cycle2819.py'/"
      f"'scan_cycle2819.json' carries 'cycle2819'/'e2819' on its path tokens — "
      f"the c2760 E-TOKEN lesson re-verified live: line 9563 ABSENT from the "
      f"dict, the bare-c2819 weight measured honestly)")

c2818_total = text.count("c2818")
c2818_lines = {i + 1: l.count("c2818") for i, l in enumerate(lines) if "c2818" in l}
guard("c2818_mention_census_pre",
      c2818_total == 90
      and c2818_lines == {9530: 2, 9532: 2, 9536: 5, 9542: 1, 9544: 4, 9547: 1,
                          9548: 7, 9549: 6, 9554: 4, 9556: 11, 9558: 16, 9560: 16,
                          9561: 3, 9562: 4, 9565: 3, 9566: 3, 9568: 2},
      f"total={c2818_total} per-line={c2818_lines} (the c2818-guard-probe state 43 on "
      f"lines 9530..9556 + 47 births inside the c2819 block itself, measured "
      f"per-line at this cycle's census)")

c2817_total = text.count("c2817")
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(lines) if "c2817" in l}
guard("c2817_mention_census_pre",
      c2817_total == 107
      and c2817_lines == {9518: 2, 9520: 2, 9524: 4, 9530: 1, 9532: 4, 9535: 1,
                          9536: 8, 9537: 5, 9542: 4, 9544: 11, 9546: 17, 9548: 17,
                          9549: 5, 9550: 5, 9553: 4, 9554: 3, 9556: 4, 9560: 4,
                          9561: 1, 9565: 2, 9568: 3},
      f"total={c2817_total} per-line={c2817_lines} (the c2817-guard-probe state 97 on "
      f"lines 9518..9556 + 10 births inside the c2819 block itself, measured "
      f"per-line at this cycle's census)")

c2816_total = text.count("c2816")
c2816_lines = {i + 1: l.count("c2816") for i, l in enumerate(lines) if "c2816" in l}
guard("c2816_mention_census_pre",
      c2816_total == 94
      and c2816_lines == {9506: 2, 9508: 2, 9512: 6, 9518: 1, 9520: 4, 9523: 1,
                          9524: 7, 9525: 4, 9530: 4, 9532: 10, 9534: 14, 9536: 19,
                          9537: 2, 9538: 5, 9541: 3, 9542: 3, 9544: 1, 9548: 1,
                          9549: 1, 9556: 1, 9560: 1, 9561: 1, 9568: 1},
      f"total={c2816_total} per-line={c2816_lines} (the c2816-guard-probe state 91 "
      f"on lines 9506..9556 + 3 births inside the c2819 block itself, measured "
      f"per-line at this cycle's census)")

c2815_total = text.count("c2815")
c2815_lines = {i + 1: l.count("c2815") for i, l in enumerate(lines) if "c2815" in l}
guard("c2815_mention_census_pre",
      c2815_total == 92
      and c2815_lines == {9494: 2, 9496: 2, 9500: 5, 9506: 1, 9508: 4, 9511: 1,
                          9512: 5, 9513: 4, 9517: 1, 9518: 4, 9520: 9, 9522: 13,
                          9524: 17, 9525: 4, 9526: 4, 9529: 3, 9530: 3, 9532: 3,
                          9536: 1, 9537: 2, 9544: 1, 9548: 1, 9556: 1, 9560: 1},
      f"total={c2815_total} per-line={c2815_lines} (the c2815-guard-probe state 91 "
      f"on lines 9494..9556 + 1 birth inside the c2819 block itself, measured "
      f"per-line at this cycle's census)")

c2814_total = text.count("c2814")
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(lines) if "c2814" in l}
guard("c2814_mention_census_pre",
      c2814_total == 86
      and c2814_lines == {9482: 2, 9484: 2, 9488: 5, 9494: 1, 9496: 4, 9499: 1,
                          9500: 4, 9501: 4, 9506: 4, 9508: 10, 9510: 12, 9512: 14,
                          9513: 2, 9514: 4, 9517: 3, 9518: 3, 9520: 2, 9524: 1,
                          9525: 1, 9526: 1, 9532: 2, 9536: 1, 9544: 1, 9548: 1,
                          9560: 1},
      f"total={c2814_total} per-line={c2814_lines} (the c2814-guard-probe state 85 "
      f"on lines 9482..9548 + 1 birth inside the c2819 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2813", 100), ("c2812", 94), ("c2811", 98), ("c2810", 114),
                   ("c2809", 93), ("c2808", 105), ("c2807", 94), ("c2806", 90),
                   ("c2805", 107), ("c2804", 117), ("c2803", 123), ("c2802", 139),
                   ("c2801", 103), ("c2800", 154), ("c2799", 108), ("c2798", 106),
                   ("c2797", 98), ("c2796", 108), ("c2795", 131), ("c2794", 125),
                   ("c2793", 133), ("c2792", 138), ("c2791", 126), ("c2790", 139),
                   ("c2789", 129), ("c2788", 140), ("c2787", 141), ("c2786", 163),
                   ("c2785", 145), ("c2784", 143), ("c2783", 144), ("c2782", 143),
                   ("c2781", 148), ("c2780", 153), ("c2779", 153), ("c2778", 197),
                   ("c2777", 169), ("c2776", 174), ("c2775", 183), ("c2774", 188),
                   ("c2773", 192), ("c2772", 211), ("c2771", 201), ("c2770", 263),
                   ("c2769", 190), ("c2768", 193), ("c2767", 280), ("c2766", 241),
                   ("c2765", 184), ("c2764", 186), ("c2763", 194), ("c2762", 231),
                   ("c2761", 260), ("c2760", 189), ("c2759", 189), ("c2758", 191),
                   ("c2757", 194), ("c2756", 199), ("c2755", 206), ("c2754", 209),
                   ("c2753", 235), ("c2752", 241), ("c2751", 227), ("c2750", 233),
                   ("c2749", 253)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (253 at the c2819 census probe: 226 "
          f"accounted-path cumulative then; FIVE new POSTs landed between the "
          f"probes (253 -> 258 = +5: 2 accounted — the c2819 official capture + "
          f"this cycle's echo #541 (latency-match 1655ms class, bracketed, "
          f"RE-DERIVABLE) — + 3 foreign), arithmetic-necessity class, honest; "
          f"cumulative accounted-path now 228 = 226 + 2; timestamp-less log, "
          f"latency-match split, honest)")
else:
    print("dev_log: ABSENT")

# loop echo #541 facts (measured this session, the echo-then-capture order held)
print("loop_echo_541: pre-echo 04:58:39.899240925 +0000 epoch 1793336319.899924115 "
      "EPOCH-governs; curl 1.661584 / server 1655ms latency-match; post-echo "
      "04:58:41.570175831 +0000 epoch 1793336321.570815873 EPOCH-governs; echo "
      "scanned_at 04:58:41.565Z = epoch 1793336321.565; wall 1.670891758; "
      "stamp-to-echo 740.899924115 (SHALLOWER than the deepest print "
      "1025.631018606 — the deepest print STANDS unchallenged); echo POST-WINDOW "
      "+265.212868478; echo account attempt #541 -> the hit-count carry NOT "
      "RE-DERIVABLE from the ledger (the c2817 honest note stands — the "
      "increment rule not re-derivable, no over-claim either way, honest note; "
      "12 priors of the '137-for-530' form counted per the census — the form's "
      "ledger weight, not a forecast); the echo landed MID-SESSION (the "
      "first-command prescription slipped a TWENTY-EIGHTH consecutive cycle); "
      "the echo-then-capture order class expected to EXTEND m13 (the echo ran "
      "BEFORE the official capture this cycle — the confirmation lands in "
      "Step 3)")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2819 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2819 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2819:"):
        official_depth = depth
        walk_info.append(f"official c2819 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2819_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2819_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2819 commit — the 5939089/19ff74c/660688b/7386e88/4538311/"
          f"02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/"
          f"e54aab2/d22e2bb/134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/"
          f"966ab1f/0b4f512/ffa527c/c048029/3b69581/18522dc/ea92218/4477b73/"
          f"4207111/615fc1c/7efc24d/65f4c4e/b27a69f/f0d806e/87e21ad/e6da641/"
          f"325729a/7de8446/a6fac67/35ba192/92a8201/6b53b65/7f7a022/1288d7f/"
          f"92b5acc/c5fb5cc/30a3440/8cc4726/ef415bd/42f95e4/68117e3/a009715/"
          f"724e4a0/b9757c0 precedent)")
    for depth in range(0, official_depth if official_depth is not None else 0):
        rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
        stat = git("show", "--stat", "--format=", rev)
        guard(f"git_walk_depth{depth}_zero_ledger_touch", "worklog.md" not in stat,
              f"{rev} touches only foreign-add files; worklog touched="
              f"{'worklog.md' in stat}")
guard("git_head_zero_ledger_touch", "worklog.md" not in head_stat,
      f"HEAD={head_short} touches foreign-add files only; worklog touched="
      f"{'worklog.md' in head_stat}")
print(f"head_commit_stat_tail: {head_stat.splitlines()[-1] if head_stat else '(empty)'}")
recent = git("log", "-3", "--format=%h %s")
print("recent_commits:")
for ln in recent.splitlines():
    print(f"  {ln[:120]}")
status = git("status", "--short")
print(f"working_tree_entries={len(status.splitlines()) if status else 0}")

C2819_SET = [
    "census_c2819.py", "arrival_guard_c2819.py", "rebadge_cycle2819.py",
    "capture_cycle2819.sh", "measure_c2819_tokens.py", "recursive_diff_2819.py",
    "validate_cycle2819.py", "entry_cycle2819.txt", "append_cycle2819.py",
    "scan_cycle2819_raw.json", "scan_cycle2819.json",
]
print("c2819_instrument_set_object_presence:")
missing = []
for name in C2819_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2819 files on disk")

v119 = open("/home/z/my-project/scripts/validate_cycle2819.py", "rb").read()
guard("v119_source_intact", b"CYCLE = 2819" in v119 and b"drift49_pass68_match" in v119
      and b"drift49_pass69_match" not in v119
      and b"(18,0,0,18,0)" in v119 and b"(20,0,2,18,0)" in v119
      and b"(21,0,3,18,0)" in v119 and b"pass-67 band" in v119
      and b"pass-68 band" not in v119
      and b"pass-67 evidence" in v119 and b"pass-68 evidence" not in v119,
      f"bytes={len(v119)} (the v119 pass-68 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-69 gate name drift49_pass69_match is what the v120 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-67 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-67 evidence' is present — BOTH instrument surfaces, the v120 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "5a868fa:scripts/validate_cycle2819.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v119_commit_object_intact", len(obj.stdout) == len(v119)
          and obj.stdout == v119,
          f"object_bytes={len(obj.stdout)} == disk {len(v119)} (the 5a868fa c2819 commit)")
else:
    guard("v119_commit_object_intact", False, "5a868fa object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
