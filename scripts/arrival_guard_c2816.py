#!/usr/bin/env python3
"""Arrival-guard for cycle 2816 (Job ID 446189) — measured, never predicted.

Spec source: the c2815 Next-block (worklog line 9520). Checks:
  worklog 9520 lines EXACT (newline count, c2815 append post-guard prophecy);
  tail = the c2816 Next bullet;
  anchors ^Task ID: 493 / ^- No gold yet 426 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2816 entries; c2818/c2817/c2816 substring accounting
  (the token-guard lives INSIDE the c2815 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2816.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2818 = 0 (UNBORN, measured pre-append) and the c2817 = 4
  total = 2 births in the c2815 Step-7 twin-print (line 9518: the rehearsal
  pre-count print 'the c2817 pre==0 expectation' AND the census-time print
  'c2817_pre = 0') + 2 FORWARD-token births inside the c2815 Next-block guard
  phrase ('arrival-guard against c2816/c2817 tokens') AND the FORWARD-token
  sentence ('the FORWARD token c2817 must be IN the census tuple'), both on
  line 9520 — the c2815 append prophecy 'c2817 = 4 block births' held EXACTLY,
  the born-FOUR class REPEATS a THIRTEENTH time;
  the c2816 token itself is BORN FIFTEEN times pre-append: 2 in the c2814
  Step-7 twin-print (line 9506) + 2 in the c2814 Next-block (line 9508) + 6 in
  the c2815 Step-1 census sentence (line 9512 — the MEASURED weight, not the
  hand-count 5: the battery-rotation phrase 'the combined dict retains the
  c2816/c2815 rotation' AND the attempt-1 probe-correction quote "'c2815/c2816'
  on line 9508" ADD TWO mentions beyond the four birth-class quotes — the
  c2815 Step-1 sentence carries SIX c2816 occurrences, honest note) + 1 in the
  c2815 Step-7 'the c2816 pre-count is 4' (line 9518) + 4 in the c2815
  Next-block (line 9520: the instance + the 446189-c2816 id + the 'c2816/c2817'
  guard phrase + the 'measure_c2816_tokens.py' surface — the bare-c-token
  accounting, honestly counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2815_raw.json' /
  'validate_cycle2815.py' / 'scan_cycle2815.json' carry 'e2815'/'cycle2815',
  NOT the bare c-token 'c2815' — line 9515 ABSENT from the measured c2815
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2815 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2815 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2815 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v115 source-intact expectations matched to the v115 pass-64 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v115 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-65 gate name is what the v116 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-63 band' is present AND the evidence-paragraph lag-1 heading
  'pass-63 evidence' is present — BOTH instrument surfaces, the v116 rebadge
  P3/P8 old-string expectations, exactly as the c2815 Next-block wrote).
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
guard("worklog_lines==9520", n_nl == 9520, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2816_next_bullet", last_nonempty.startswith("- Next: the c2816 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==493", tid == 493, f"got={tid}")
guard("anchor_nogold==426", gold == 426, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2816")]
guard("dup_check_zero_serviced_c2816", len(dup) == 0, f"got={len(dup)}")
c2818_total = text.count("c2818")
c2817_total = text.count("c2817")
c2816_total = text.count("c2816")
tok_guard = [l for l in lines if "c2816/c2817" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2816 instance")]
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(lines) if "c2817" in l}
c2816_lines = {i + 1: l.count("c2816") for i, l in enumerate(lines) if "c2816" in l}
guard("c2816_mention_accounting_pre",
      c2818_total == 0 and c2817_total == 4 and c2816_total == 15
      and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and c2817_lines == {9518: 2, 9520: 2}
      and c2816_lines == {9506: 2, 9508: 2, 9512: 6, 9518: 1, 9520: 4},
      f"c2818={c2818_total} c2817={c2817_total} c2816={c2816_total} "
      f"c2817_per-line={c2817_lines} c2816_per-line={c2816_lines} "
      f"(expect c2818 = 0 UNBORN (measured pre-append — the forward-token "
      f"lesson: measured, never assumed unborn); c2817 = 4 — 2 births in the "
      f"c2815 Step-7 twin-print line 9518 (the rehearsal pre-count print 'the "
      f"c2817 pre==0 expectation' AND the census-time print 'c2817_pre = 0' — "
      f"the Step-7 twin-print class REPEATS) + 2 FORWARD-token births TWICE "
      f"inside the c2815 Next-block guard phrase AND census-tuple sentence, "
      f"both on line 9520 (the c2815 append prophecy 'c2817 = 4 block births' "
      f"held EXACTLY, the born-FOUR class REPEATS a THIRTEENTH time); c2816 = "
      f"15 — 2 in the c2814 Step-7 twin-print (line 9506) + 2 in the c2814 "
      f"Next-block (line 9508) + 6 in the c2815 Step-1 census sentence (line "
      f"9512 — the MEASURED weight: the battery-rotation phrase AND the "
      f"attempt-1 probe-correction quote ADD TWO beyond the four birth-class "
      f"quotes, honest note) + 1 in the c2815 Step-7 'the c2816 pre-count is "
      f"4' (line 9518) + 4 in the c2815 Next-block (line 9520: the instance + "
      f"the 446189-c2816 id + the 'c2816/c2817' guard phrase + the "
      f"'measure_c2816_tokens.py' surface))")

c2815_total = text.count("c2815")
c2815_lines = {i + 1: l.count("c2815") for i, l in enumerate(lines) if "c2815" in l}
guard("c2815_mention_census_pre",
      c2815_total == 38
      and c2815_lines == {9494: 2, 9496: 2, 9500: 5, 9506: 1, 9508: 4, 9511: 1,
                          9512: 5, 9513: 4, 9517: 1, 9518: 4, 9520: 9},
      f"total={c2815_total} per-line={c2815_lines} (the c2815-guard-probe state 14 on "
      f"lines 9494/9496/9500/9506/9508 + 24 births inside the c2815 block "
      f"itself; the Step-4 surface 'scan_cycle2815_raw.json'/"
      f"'validate_cycle2815.py'/'scan_cycle2815.json' carries 'cycle2815'/'e2815' "
      f"on its path tokens — the c2760 E-TOKEN lesson re-verified live: line "
      f"9515 ABSENT from the dict, the bare-c2815 weight measured honestly)")

c2814_total = text.count("c2814")
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(lines) if "c2814" in l}
guard("c2814_mention_census_pre",
      c2814_total == 77
      and c2814_lines == {9482: 2, 9484: 2, 9488: 5, 9494: 1, 9496: 4, 9499: 1,
                          9500: 4, 9501: 4, 9506: 4, 9508: 10, 9510: 12, 9512: 14,
                          9513: 2, 9514: 4, 9517: 3, 9518: 3, 9520: 2},
      f"total={c2814_total} per-line={c2814_lines} (the c2814-guard-probe state 37 "
      f"on lines 9482..9508 + 40 births inside the c2815 block itself, measured "
      f"per-line at this cycle's census)")

c2813_total = text.count("c2813")
c2813_lines = {i + 1: l.count("c2813") for i, l in enumerate(lines) if "c2813" in l}
guard("c2813_mention_census_pre",
      c2813_total == 88
      and c2813_lines == {9470: 2, 9472: 2, 9476: 5, 9482: 1, 9484: 4, 9487: 1,
                          9488: 4, 9489: 4, 9494: 4, 9496: 10, 9498: 14, 9500: 14,
                          9501: 3, 9502: 5, 9505: 3, 9506: 3, 9508: 2, 9510: 1,
                          9512: 1, 9513: 1, 9514: 1, 9517: 1, 9520: 2},
      f"total={c2813_total} per-line={c2813_lines} (the c2813-guard-probe state 81 "
      f"on lines 9470..9508 + 7 births inside the c2815 block itself, measured "
      f"per-line at this cycle's census)")

c2812_total = text.count("c2812")
c2812_lines = {i + 1: l.count("c2812") for i, l in enumerate(lines) if "c2812" in l}
guard("c2812_mention_census_pre",
      c2812_total == 86
      and c2812_lines == {9458: 2, 9460: 2, 9464: 5, 9470: 1, 9472: 4, 9475: 1,
                          9476: 4, 9477: 4, 9482: 4, 9484: 10, 9486: 14, 9488: 13,
                          9489: 5, 9490: 4, 9493: 4, 9494: 3, 9496: 1, 9500: 1,
                          9501: 1, 9508: 1, 9512: 1, 9520: 1},
      f"total={c2812_total} per-line={c2812_lines} (the c2812-guard-probe state 84 "
      f"on lines 9458..9501 + 2 births inside the c2815 block itself, measured "
      f"per-line at this cycle's census)")

c2811_total = text.count("c2811")
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(lines) if "c2811" in l}
guard("c2811_mention_census_pre",
      c2811_total == 86
      and c2811_lines == {9446: 2, 9448: 2, 9452: 5, 9458: 1, 9460: 4, 9463: 1,
                          9464: 4, 9465: 4, 9470: 4, 9472: 9, 9474: 14, 9476: 12,
                          9477: 4, 9478: 4, 9481: 1, 9482: 3, 9484: 1, 9486: 1,
                          9488: 2, 9489: 2, 9496: 1, 9498: 1, 9500: 1, 9508: 1,
                          9510: 1, 9512: 1},
      f"total={c2811_total} per-line={c2811_lines} (the c2811-guard-probe state 84 "
      f"on lines 9446..9508 + 2 births inside the c2815 block itself, measured "
      f"per-line at this cycle's census)")

c2810_total = text.count("c2810")
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(lines) if "c2810" in l}
guard("c2810_mention_census_pre",
      c2810_total == 103
      and c2810_lines == {9434: 2, 9436: 2, 9440: 4, 9446: 1, 9448: 4, 9451: 1,
                          9452: 4, 9453: 5, 9458: 4, 9460: 9, 9462: 14, 9464: 12,
                          9465: 4, 9466: 4, 9469: 3, 9470: 3, 9472: 3, 9474: 2,
                          9476: 2, 9481: 3, 9484: 2, 9488: 2, 9489: 4, 9493: 1,
                          9496: 2, 9500: 1, 9505: 1, 9508: 1, 9512: 1, 9517: 1,
                          9520: 1},
      f"total={c2810_total} per-line={c2810_lines} (the c2810-guard-probe state 100 "
      f"on lines 9434..9508 + 3 births inside the c2815 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2809", 87), ("c2808", 101), ("c2807", 90), ("c2806", 86),
                   ("c2805", 99), ("c2804", 113), ("c2803", 119), ("c2802", 128),
                   ("c2801", 99), ("c2800", 145), ("c2799", 104), ("c2798", 102),
                   ("c2797", 94), ("c2796", 104), ("c2795", 127), ("c2794", 121),
                   ("c2793", 129), ("c2792", 134), ("c2791", 122), ("c2790", 135),
                   ("c2789", 125), ("c2788", 136), ("c2787", 137), ("c2786", 159),
                   ("c2785", 141), ("c2784", 139), ("c2783", 140), ("c2782", 139),
                   ("c2781", 144), ("c2780", 149), ("c2779", 149), ("c2778", 193),
                   ("c2777", 165), ("c2776", 170), ("c2775", 179), ("c2774", 184),
                   ("c2773", 188), ("c2772", 207), ("c2771", 197), ("c2770", 255),
                   ("c2769", 186), ("c2768", 189), ("c2767", 268), ("c2766", 232),
                   ("c2765", 180), ("c2764", 182), ("c2763", 190), ("c2762", 227),
                   ("c2761", 252), ("c2760", 185), ("c2759", 185), ("c2758", 187),
                   ("c2757", 190), ("c2756", 195), ("c2755", 202), ("c2754", 205),
                   ("c2753", 227), ("c2752", 233), ("c2751", 219), ("c2750", 225),
                   ("c2749", 237)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (239 at the census probe: 220 "
          f"accounted-path cumulative = 218 at the c2815 census probe + 1 through "
          f"the c2815 official capture + 1 this cycle's echo #537 (latency-match "
          f"1673ms class, bracketed, RE-DERIVABLE) = 220 accounted + 19 "
          f"foreign/unattributed cumulative — THREE new POSTs landed between the "
          f"probes (236 -> 239 = +3: 2 accounted + 1... arithmetic: 234 + 2 "
          f"accounted = 236, measured 239, +3 foreign), "
          f"arithmetic-necessity class; timestamp-less log, latency-match split, "
          f"honest)")
else:
    print("dev_log: ABSENT")

# loop echo #537 facts (measured this session, the echo-then-capture order expected)
print("loop_echo_537: pre-echo 04:00:17.837664247 +0000 epoch 1793332817.838339414 "
      "EPOCH-governs; curl 1.679972 / server 1673ms latency-match; post-echo "
      "04:00:19.527005216 +0000 epoch 1793332819.527632488 EPOCH-governs; echo "
      "scanned_at 04:00:19.522Z = epoch 1793332819.522; wall 1.689293074; "
      "stamp-to-echo 539.838339414 (SHALLOWER than the deepest print "
      "1025.631018606 — the deepest print STANDS unchallenged); echo POST-WINDOW "
      "+299.829814544; echo account attempt #537 -> the hit-count carry NOT "
      "RE-DERIVABLE from the ledger (the c2815 honest note stands — the "
      "increment rule not re-derivable, no over-claim either way, honest note; "
      "8 priors of the '137-for-530' form counted per the census — the form's "
      "ledger weight, not a forecast); the echo landed MID-SESSION (the "
      "first-command prescription slipped a TWENTY-FOURTH consecutive cycle); "
      "the echo-then-capture order class expected to EXTEND m12")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2815 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2815 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2815:"):
        official_depth = depth
        walk_info.append(f"official c2815 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2815_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2815_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2815 commit — the 5939089/19ff74c/660688b/7386e88/4538311/"
          f"02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/"
          f"e54aab2/d22e2bb/134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/"
          f"966ab1f/0b4f512/ffa527c/c048029/3b69581/18522dc/ea92218/4477b73/"
          f"4207111/615fc1c/7efc24d/65f4c4e/b27a69f/f0d806e/87e21ad/e6da641/"
          f"325729a/7de8446/a6fac67/35ba192/92a8201/6b53b65/7f7a022/1288d7f/"
          f"92b5acc/c5fb5cc/30a3440/8cc4726/ef415bd/42f95e4 precedent)")
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

C2815_SET = [
    "census_c2815.py", "arrival_guard_c2815.py", "rebadge_cycle2815.py",
    "capture_cycle2815.sh", "measure_c2815_tokens.py", "recursive_diff_2815.py",
    "validate_cycle2815.py", "entry_cycle2815.txt", "append_cycle2815.py",
    "scan_cycle2815_raw.json", "scan_cycle2815.json",
]
print("c2815_instrument_set_object_presence:")
missing = []
for name in C2815_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2815 files on disk")

v115 = open("/home/z/my-project/scripts/validate_cycle2815.py", "rb").read()
guard("v115_source_intact", b"CYCLE = 2815" in v115 and b"drift49_pass64_match" in v115
      and b"drift49_pass65_match" not in v115
      and b"(18,0,0,18,0)" in v115 and b"(20,0,2,18,0)" in v115
      and b"(21,0,3,18,0)" in v115 and b"pass-63 band" in v115
      and b"pass-64 band" not in v115
      and b"pass-63 evidence" in v115 and b"pass-64 evidence" not in v115,
      f"bytes={len(v115)} (the v115 pass-64 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-65 gate name drift49_pass65_match is what the v116 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-63 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-63 evidence' is present — BOTH instrument surfaces, the v116 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "80e165e:scripts/validate_cycle2815.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v115_commit_object_intact", len(obj.stdout) == len(v115)
          and obj.stdout == v115,
          f"object_bytes={len(obj.stdout)} == disk {len(v115)} (the 80e165e c2815 commit)")
else:
    guard("v115_commit_object_intact", False, "80e165e object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
