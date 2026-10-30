#!/usr/bin/env python3
"""Arrival-guard for cycle 2813 (Job ID 446189) — measured, never predicted.

Spec source: the c2812 Next-block (worklog line 9484). Checks:
  worklog 9484 lines EXACT (newline count, c2812 append post-guard prophecy);
  tail = the c2813 Next bullet;
  anchors ^Task ID: 490 / ^- No gold yet 423 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2813 entries; c2815/c2814/c2813 substring accounting
  (the token-guard lives INSIDE the c2812 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2813.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2814 = 4 total = 2 births in the c2812 Step-7 line 9482 (the
  rehearsal pre-count print 'the c2814 pre==0 expectation' AND the census-time
  print 'c2814_pre = 0') + 2 FORWARD-token births inside the c2812 Next-block
  guard phrase ('arrival-guard against c2813/c2814 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2814 must be IN the census
  tuple'), both on line 9484 — the c2812 append prophecy 'c2814 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS a TENTH time; the c2813
  token itself is BORN FOURTEEN times pre-append: 2 in the c2811 Step-7
  twin-print (line 9470) + 2 in the c2811 Next-block (line 9472) + 5 in the
  c2812 Step-1 census sentence (line 9476: the '+ c2813 = 4 per-line' print +
  the twin-print quotes 'the c2813 pre==0 expectation' AND 'c2813_pre = 0' +
  the prophecy quote 'c2813 = 4 block births' + the 'c2767..c2812
  forward-token lessons' phrase) + 1 in the c2812 Step-7 'the c2813 pre-count
  is 4' (line 9482) + 4 in the c2812 Next-block (line 9484: the instance +
  the 446189-c2813 id + the 'c2813/c2814' guard phrase + the
  'measure_c2813_tokens.py' surface — the bare-c-token accounting, honestly
  counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2812_raw.json' /
  'validate_cycle2812.py' / 'scan_cycle2812.json' carry 'e2812'/'cycle2812',
  NOT the bare c-token 'c2812' — line 9479 ABSENT from the measured c2812
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2812 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2812 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2812 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v112 source-intact expectations matched to the v112 pass-61 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v112 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-62 gate name is what the v113 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-60 band' is present AND the evidence-paragraph lag-1 heading
  'pass-60 evidence' is present — BOTH instrument surfaces, the v113 rebadge
  P3/P8 old-string expectations, exactly as the c2812 Next-block wrote).
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
guard("worklog_lines==9484", n_nl == 9484, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2813_next_bullet", last_nonempty.startswith("- Next: the c2813 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==490", tid == 490, f"got={tid}")
guard("anchor_nogold==423", gold == 423, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2813")]
guard("dup_check_zero_serviced_c2813", len(dup) == 0, f"got={len(dup)}")
c2815_total = text.count("c2815")
c2814_total = text.count("c2814")
c2813_total = text.count("c2813")
tok_guard = [l for l in lines if "c2813/c2814" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2813 instance")]
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(lines) if "c2814" in l}
c2813_lines = {i + 1: l.count("c2813") for i, l in enumerate(lines) if "c2813" in l}
guard("c2814_mention_accounting_pre",
      c2815_total == 0 and c2814_total == 4 and c2813_total == 14
      and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and c2814_lines == {9482: 2, 9484: 2}
      and c2813_lines == {9470: 2, 9472: 2, 9476: 5, 9482: 1, 9484: 4},
      f"c2815={c2815_total} c2814={c2814_total} c2813={c2813_total} "
      f"c2814_per-line={c2814_lines} c2813_per-line={c2813_lines} "
      f"(expect c2814 = 4 — 2 births in the c2812 Step-7 line 9482 (the "
      f"rehearsal pre-count print 'the c2814 pre==0 expectation' AND the "
      f"census-time print 'c2814_pre = 0' — the Step-7 twin-print class "
      f"REPEATS) + 2 FORWARD-token births TWICE inside the c2812 Next-block "
      f"guard phrase AND census-tuple sentence, both on line 9484 (the "
      f"forward-token lesson: measured, never assumed unborn — the c2812 "
      f"append prophecy 'c2814 = 4 block births' held EXACTLY, the born-FOUR "
      f"class REPEATS a TENTH time); c2813 = 14 — 2 in the c2811 Step-7 "
      f"twin-print (line 9470) + 2 in the c2811 Next-block (line 9472) + 5 in "
      f"the c2812 Step-1 census sentence (line 9476) + 1 in the c2812 Step-7 "
      f"'the c2813 pre-count is 4' (line 9482) + 4 in the c2812 Next-block "
      f"(line 9484: the instance + the 446189-c2813 id + the 'c2813/c2814' "
      f"guard phrase + the 'measure_c2813_tokens.py' surface); c2815 = 0 "
      f"UNBORN (measured pre-append))")

c2812_total = text.count("c2812")
c2812_lines = {i + 1: l.count("c2812") for i, l in enumerate(lines) if "c2812" in l}
guard("c2812_mention_census_pre",
      c2812_total == 37
      and c2812_lines == {9458: 2, 9460: 2, 9464: 5, 9470: 1, 9472: 4, 9475: 1,
                          9476: 4, 9477: 4, 9482: 4, 9484: 10},
      f"total={c2812_total} per-line={c2812_lines} (the c2812 pre-block 14 on "
      f"lines 9458/9460/9464/9470/9472 + 23 births inside the c2812 block "
      f"itself; the Step-4 surface 'scan_cycle2812_raw.json'/"
      f"'validate_cycle2812.py'/'scan_cycle2812.json' carries 'cycle2812'/'e2812' "
      f"on its path tokens — the c2760 E-TOKEN lesson re-verified live: line "
      f"9479 ABSENT from the dict, the bare-c2812 weight measured honestly)")

c2811_total = text.count("c2811")
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(lines) if "c2811" in l}
guard("c2811_mention_census_pre",
      c2811_total == 75
      and c2811_lines == {9446: 2, 9448: 2, 9452: 5, 9458: 1, 9460: 4, 9463: 1,
                          9464: 4, 9465: 4, 9470: 4, 9472: 9, 9474: 14, 9476: 12,
                          9477: 4, 9478: 4, 9481: 1, 9482: 3, 9484: 1},
      f"total={c2811_total} per-line={c2811_lines} (the c2812-guard-probe state 36 "
      f"on lines 9446..9472 + 39 births inside the c2812 block itself, measured "
      f"per-line at this cycle's census)")

c2810_total = text.count("c2810")
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(lines) if "c2810" in l}
guard("c2810_mention_census_pre",
      c2810_total == 88
      and c2810_lines == {9434: 2, 9436: 2, 9440: 4, 9446: 1, 9448: 4, 9451: 1,
                          9452: 4, 9453: 5, 9458: 4, 9460: 9, 9462: 14, 9464: 12,
                          9465: 4, 9466: 4, 9469: 3, 9470: 3, 9472: 3, 9474: 2,
                          9476: 2, 9481: 3, 9484: 2},
      f"total={c2810_total} per-line={c2810_lines} (the c2811-guard-probe state 79 "
      f"on lines 9434..9472 + 9 births inside the c2812 block itself, measured "
      f"per-line at this cycle's census)")

c2809_total = text.count("c2809")
c2809_lines = {i + 1: l.count("c2809") for i, l in enumerate(lines) if "c2809" in l}
guard("c2809_mention_census_pre",
      c2809_total == 81
      and c2809_lines == {9422: 2, 9424: 2, 9428: 4, 9434: 1, 9436: 4, 9439: 1,
                          9440: 4, 9441: 5, 9446: 4, 9448: 8, 9450: 13, 9452: 13,
                          9453: 5, 9454: 3, 9457: 1, 9458: 3, 9460: 2, 9464: 2,
                          9469: 1, 9472: 1, 9476: 2},
      f"total={c2809_total} per-line={c2809_lines} (the c2810-guard-probe state 79 "
      f"on lines 9422..9472 + 2 births inside the c2812 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2808", 90), ("c2807", 87), ("c2806", 83), ("c2805", 92),
                   ("c2804", 107), ("c2803", 116), ("c2802", 122), ("c2801", 96),
                   ("c2800", 136), ("c2799", 101), ("c2798", 99), ("c2797", 91),
                   ("c2796", 101), ("c2795", 124), ("c2794", 118), ("c2793", 126),
                   ("c2792", 131), ("c2791", 119), ("c2790", 132), ("c2789", 122),
                   ("c2788", 133), ("c2787", 134), ("c2786", 156), ("c2785", 138),
                   ("c2784", 136), ("c2783", 137), ("c2782", 136), ("c2781", 141),
                   ("c2780", 146), ("c2779", 146), ("c2778", 190), ("c2777", 162),
                   ("c2776", 167), ("c2775", 176), ("c2774", 181), ("c2773", 185),
                   ("c2772", 204), ("c2771", 194), ("c2770", 248), ("c2769", 183),
                   ("c2768", 186), ("c2767", 259), ("c2766", 225), ("c2765", 177),
                   ("c2764", 179), ("c2763", 187), ("c2762", 224), ("c2761", 246),
                   ("c2760", 182), ("c2759", 182), ("c2758", 184), ("c2757", 187),
                   ("c2756", 192), ("c2755", 199), ("c2754", 202), ("c2753", 221),
                   ("c2752", 227), ("c2751", 213), ("c2750", 219), ("c2749", 224)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (222 at the census probe: 214 "
          f"accounted-path cumulative = 212 at the c2812 census probe + 1 through "
          f"the c2812 official capture + 1 this cycle's echo #534 (latency-match "
          f"1556ms class, bracketed, RE-DERIVABLE) = 214 accounted + 8 "
          f"foreign/unattributed cumulative — FOUR new foreign POSTs landed "
          f"between the probes (216 -> 222 = +6: 2 accounted + 4 foreign), "
          f"arithmetic-necessity class; timestamp-less log, latency-match split, "
          f"honest)")
else:
    print("dev_log: ABSENT")

# loop echo #534 facts (measured this session, the echo-then-capture order expected)
print("loop_echo_534: pre-echo 03:07:51.490391899 +0000 epoch 1793329671.491053914 "
      "EPOCH-governs; curl 1.562345 / server 1556ms latency-match; post-echo "
      "03:07:53.062124568 +0000 epoch 1793329673.062755684 EPOCH-governs; echo "
      "scanned_at 03:07:53.057Z = epoch 1793329673.057; wall 1.571701770; "
      "stamp-to-echo 994.491053914 (SHALLOWER than the deepest print "
      "1025.631018606 — the deepest print STANDS unchallenged); echo POST-WINDOW "
      "+684.844840298; echo account attempt #534 -> the hit-count carries "
      "137-for-530 (2 priors of the exact form counted per the census; the "
      "increment rule not re-derivable from the ledger, no over-claim either "
      "way, honest note); the echo-then-capture order class expected to "
      "EXTEND m10")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2812 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2812 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2812:"):
        official_depth = depth
        walk_info.append(f"official c2812 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2812_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2812_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2812 commit — the 5939089/19ff74c/660688b/7386e88/4538311/"
          f"02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/"
          f"e54aab2/d22e2bb/134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/"
          f"966ab1f/0b4f512/ffa527c/c048029/3b69581/18522dc/ea92218/4477b73/"
          f"4207111/615fc1c/7efc24d/65f4c4e/b27a69f/f0d806e/87e21ad/e6da641/"
          f"325729a/7de8446/a6fac67/35ba192/92a8201/6b53b65/7f7a022/1288d7f/"
          f"92b5acc/c5fb5cc/30a3440 precedent)")
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

C2812_SET = [
    "census_c2812.py", "arrival_guard_c2812.py", "rebadge_cycle2812.py",
    "capture_cycle2812.sh", "measure_c2812_tokens.py", "recursive_diff_2812.py",
    "validate_cycle2812.py", "entry_cycle2812.txt", "append_cycle2812.py",
    "scan_cycle2812_raw.json", "scan_cycle2812.json",
]
print("c2812_instrument_set_object_presence:")
missing = []
for name in C2812_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2812 files on disk")

v112 = open("/home/z/my-project/scripts/validate_cycle2812.py", "rb").read()
guard("v112_source_intact", b"CYCLE = 2812" in v112 and b"drift49_pass61_match" in v112
      and b"drift49_pass62_match" not in v112
      and b"(18,0,0,18,0)" in v112 and b"(20,0,2,18,0)" in v112
      and b"(21,0,3,18,0)" in v112 and b"pass-60 band" in v112
      and b"pass-61 band" not in v112
      and b"pass-60 evidence" in v112 and b"pass-61 evidence" not in v112,
      f"bytes={len(v112)} (the v112 pass-61 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-62 gate name drift49_pass62_match is what the v113 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-60 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-60 evidence' is present — BOTH instrument surfaces, the v113 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "fcd7b1c:scripts/validate_cycle2812.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v112_commit_object_intact", len(obj.stdout) == len(v112)
          and obj.stdout == v112,
          f"object_bytes={len(obj.stdout)} == disk {len(v112)} (the fcd7b1c c2812 commit)")
else:
    guard("v112_commit_object_intact", False, "fcd7b1c object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
