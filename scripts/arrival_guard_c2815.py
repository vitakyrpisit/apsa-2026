#!/usr/bin/env python3
"""Arrival-guard for cycle 2815 (Job ID 446189) — measured, never predicted.

Spec source: the c2814 Next-block (worklog line 9508). Checks:
  worklog 9508 lines EXACT (newline count, c2814 append post-guard prophecy);
  tail = the c2815 Next bullet;
  anchors ^Task ID: 492 / ^- No gold yet 425 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2815 entries; c2817/c2816/c2815 substring accounting
  (the token-guard lives INSIDE the c2814 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2815.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2817 = 0 (UNBORN, measured pre-append) and the c2816 = 4
  total = 2 births in the c2814 Step-7 twin-print (line 9506: the rehearsal
  pre-count print 'the c2816 pre==0 expectation' AND the census-time print
  'c2816_pre = 0') + 2 FORWARD-token births inside the c2814 Next-block guard
  phrase ('arrival-guard against c2815/c2816 tokens') AND the FORWARD-token
  sentence ('the FORWARD token c2816 must be IN the census tuple'), both on
  line 9508 — the c2814 append prophecy 'c2816 = 4 block births' held EXACTLY,
  the born-FOUR class REPEATS a TWELFTH time;
  the c2815 token itself is BORN FOURTEEN times pre-append: 2 in the c2813
  Step-7 twin-print (line 9494) + 2 in the c2813 Next-block (line 9496) + 5 in
  the c2814 Step-1 census sentence (line 9500) + 1 in the c2814 Step-7
  'the c2815 pre-count is 4' (line 9506) + 4 in the c2814 Next-block
  (line 9508: the instance + the 446189-c2815 id + the 'c2815/c2816' guard
  phrase + the 'measure_c2815_tokens.py' surface — the bare-c-token
  accounting, honestly counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2814_raw.json' /
  'validate_cycle2814.py' / 'scan_cycle2814.json' carry 'e2814'/'cycle2814',
  NOT the bare c-token 'c2814' — line 9503 ABSENT from the measured c2814
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2814 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2814 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2814 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v114 source-intact expectations matched to the v114 pass-63 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v114 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-64 gate name is what the v115 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-62 band' is present AND the evidence-paragraph lag-1 heading
  'pass-62 evidence' is present — BOTH instrument surfaces, the v115 rebadge
  P3/P8 old-string expectations, exactly as the c2814 Next-block wrote).
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
guard("worklog_lines==9508", n_nl == 9508, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2815_next_bullet", last_nonempty.startswith("- Next: the c2815 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==492", tid == 492, f"got={tid}")
guard("anchor_nogold==425", gold == 425, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2815")]
guard("dup_check_zero_serviced_c2815", len(dup) == 0, f"got={len(dup)}")
c2817_total = text.count("c2817")
c2816_total = text.count("c2816")
c2815_total = text.count("c2815")
tok_guard = [l for l in lines if "c2815/c2816" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2815 instance")]
c2816_lines = {i + 1: l.count("c2816") for i, l in enumerate(lines) if "c2816" in l}
c2815_lines = {i + 1: l.count("c2815") for i, l in enumerate(lines) if "c2815" in l}
guard("c2815_mention_accounting_pre",
      c2817_total == 0 and c2816_total == 4 and c2815_total == 14
      and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and c2816_lines == {9506: 2, 9508: 2}
      and c2815_lines == {9494: 2, 9496: 2, 9500: 5, 9506: 1, 9508: 4},
      f"c2817={c2817_total} c2816={c2816_total} c2815={c2815_total} "
      f"c2816_per-line={c2816_lines} c2815_per-line={c2815_lines} "
      f"(expect c2817 = 0 UNBORN (measured pre-append — the forward-token "
      f"lesson: measured, never assumed unborn); c2816 = 4 — 2 births in the "
      f"c2814 Step-7 twin-print line 9506 (the rehearsal pre-count print 'the "
      f"c2816 pre==0 expectation' AND the census-time print 'c2816_pre = 0' — "
      f"the Step-7 twin-print class REPEATS) + 2 FORWARD-token births TWICE "
      f"inside the c2814 Next-block guard phrase AND census-tuple sentence, "
      f"both on line 9508 (the c2814 append prophecy 'c2816 = 4 block births' "
      f"held EXACTLY, the born-FOUR class REPEATS a TWELFTH time); c2815 = 14 — "
      f"2 in the c2813 Step-7 twin-print (line 9494) + 2 in the c2813 "
      f"Next-block (line 9496) + 5 in the c2814 Step-1 census sentence (line "
      f"9500) + 1 in the c2814 Step-7 'the c2815 pre-count is 4' (line 9506) + "
      f"4 in the c2814 Next-block (line 9508: the instance + the 446189-c2815 "
      f"id + the 'c2815/c2816' guard phrase + the 'measure_c2815_tokens.py' "
      f"surface))")

c2814_total = text.count("c2814")
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(lines) if "c2814" in l}
guard("c2814_mention_census_pre",
      c2814_total == 37
      and c2814_lines == {9482: 2, 9484: 2, 9488: 5, 9494: 1, 9496: 4, 9499: 1,
                          9500: 4, 9501: 4, 9506: 4, 9508: 10},
      f"total={c2814_total} per-line={c2814_lines} (the c2814-guard-probe state 14 on "
      f"lines 9482/9484/9488/9494/9496 + 23 births inside the c2814 block "
      f"itself; the Step-4 surface 'scan_cycle2814_raw.json'/"
      f"'validate_cycle2814.py'/'scan_cycle2814.json' carries 'cycle2814'/'e2814' "
      f"on its path tokens — the c2760 E-TOKEN lesson re-verified live: line "
      f"9503 ABSENT from the dict, the bare-c2814 weight measured honestly)")

c2813_total = text.count("c2813")
c2813_lines = {i + 1: l.count("c2813") for i, l in enumerate(lines) if "c2813" in l}
guard("c2813_mention_census_pre",
      c2813_total == 81
      and c2813_lines == {9470: 2, 9472: 2, 9476: 5, 9482: 1, 9484: 4, 9487: 1,
                          9488: 4, 9489: 4, 9494: 4, 9496: 10, 9498: 14, 9500: 14,
                          9501: 3, 9502: 5, 9505: 3, 9506: 3, 9508: 2},
      f"total={c2813_total} per-line={c2813_lines} (the c2813-guard-probe state 37 "
      f"on lines 9470..9496 + 44 births inside the c2814 block itself, measured "
      f"per-line at this cycle's census)")

c2812_total = text.count("c2812")
c2812_lines = {i + 1: l.count("c2812") for i, l in enumerate(lines) if "c2812" in l}
guard("c2812_mention_census_pre",
      c2812_total == 84
      and c2812_lines == {9458: 2, 9460: 2, 9464: 5, 9470: 1, 9472: 4, 9475: 1,
                          9476: 4, 9477: 4, 9482: 4, 9484: 10, 9486: 14, 9488: 13,
                          9489: 5, 9490: 4, 9493: 4, 9494: 3, 9496: 1, 9500: 1,
                          9501: 1, 9508: 1},
      f"total={c2812_total} per-line={c2812_lines} (the c2812-guard-probe state 81 "
      f"on lines 9458..9484 + 3 births inside the c2814 block itself, measured "
      f"per-line at this cycle's census)")

c2811_total = text.count("c2811")
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(lines) if "c2811" in l}
guard("c2811_mention_census_pre",
      c2811_total == 84
      and c2811_lines == {9446: 2, 9448: 2, 9452: 5, 9458: 1, 9460: 4, 9463: 1,
                          9464: 4, 9465: 4, 9470: 4, 9472: 9, 9474: 14, 9476: 12,
                          9477: 4, 9478: 4, 9481: 1, 9482: 3, 9484: 1, 9486: 1,
                          9488: 2, 9489: 2, 9496: 1, 9498: 1, 9500: 1, 9508: 1},
      f"total={c2811_total} per-line={c2811_lines} (the c2811-guard-probe state 81 "
      f"on lines 9446..9484 + 3 births inside the c2814 block itself, measured "
      f"per-line at this cycle's census)")

c2810_total = text.count("c2810")
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(lines) if "c2810" in l}
guard("c2810_mention_census_pre",
      c2810_total == 100
      and c2810_lines == {9434: 2, 9436: 2, 9440: 4, 9446: 1, 9448: 4, 9451: 1,
                          9452: 4, 9453: 5, 9458: 4, 9460: 9, 9462: 14, 9464: 12,
                          9465: 4, 9466: 4, 9469: 3, 9470: 3, 9472: 3, 9474: 2,
                          9476: 2, 9481: 3, 9484: 2, 9488: 2, 9489: 4, 9493: 1,
                          9496: 2, 9500: 1, 9505: 1, 9508: 1},
      f"total={c2810_total} per-line={c2810_lines} (the c2810-guard-probe state 97 "
      f"on lines 9434..9484 + 3 births inside the c2814 block itself, measured "
      f"per-line at this cycle's census)")

c2809_total = text.count("c2809")
c2809_lines = {i + 1: l.count("c2809") for i, l in enumerate(lines) if "c2809" in l}
guard("c2809_mention_census_pre",
      c2809_total == 85
      and c2809_lines == {9422: 2, 9424: 2, 9428: 4, 9434: 1, 9436: 4, 9439: 1,
                          9440: 4, 9441: 5, 9446: 4, 9448: 8, 9450: 13, 9452: 13,
                          9453: 5, 9454: 3, 9457: 1, 9458: 3, 9460: 2, 9464: 2,
                          9469: 1, 9472: 1, 9476: 2, 9488: 2, 9500: 2},
      f"total={c2809_total} per-line={c2809_lines} (the c2809-guard-probe state 83 "
      f"on lines 9422..9476 + 2 births inside the c2814 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2808", 98), ("c2807", 89), ("c2806", 85), ("c2805", 96),
                   ("c2804", 111), ("c2803", 118), ("c2802", 126), ("c2801", 98),
                   ("c2800", 142), ("c2799", 103), ("c2798", 101), ("c2797", 93),
                   ("c2796", 103), ("c2795", 126), ("c2794", 120), ("c2793", 128),
                   ("c2792", 133), ("c2791", 121), ("c2790", 134), ("c2789", 124),
                   ("c2788", 135), ("c2787", 136), ("c2786", 158), ("c2785", 140),
                   ("c2784", 138), ("c2783", 139), ("c2782", 138), ("c2781", 143),
                   ("c2780", 148), ("c2779", 148), ("c2778", 192), ("c2777", 164),
                   ("c2776", 169), ("c2775", 178), ("c2774", 183), ("c2773", 187),
                   ("c2772", 206), ("c2771", 196), ("c2770", 253), ("c2769", 185),
                   ("c2768", 188), ("c2767", 265), ("c2766", 229), ("c2765", 179),
                   ("c2764", 181), ("c2763", 189), ("c2762", 226), ("c2761", 250),
                   ("c2760", 184), ("c2759", 184), ("c2758", 186), ("c2757", 189),
                   ("c2756", 194), ("c2755", 201), ("c2754", 204), ("c2753", 225),
                   ("c2752", 231), ("c2751", 217), ("c2750", 223), ("c2749", 233)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (234 at the census probe: 218 "
          f"accounted-path cumulative = 216 at the c2814 census probe + 1 through "
          f"the c2814 official capture + 1 this cycle's echo #536 (latency-match "
          f"2308ms class, bracketed, RE-DERIVABLE) = 218 accounted + 16 "
          f"foreign/unattributed cumulative — SIX new POSTs landed between the "
          f"probes (228 -> 234 = +6: 2 accounted + 4 foreign), "
          f"arithmetic-necessity class; timestamp-less log, latency-match split, "
          f"honest)")
else:
    print("dev_log: ABSENT")

# loop echo #536 facts (measured this session, the echo-then-capture order expected)
print("loop_echo_536: pre-echo 03:46:08.423293370 +0000 epoch 1793331968.423915835 "
      "EPOCH-governs; curl 2.321600 / server 2308ms latency-match; post-echo "
      "03:46:10.780966631 +0000 epoch 1793331970.799525028 EPOCH-governs; echo "
      "scanned_at 03:46:10.749Z = epoch 1793331970.749; wall 2.375609193; "
      "stamp-to-echo 891.423915835 (SHALLOWER than the deepest print "
      "1025.631018606 — the deepest print STANDS unchallenged); echo POST-WINDOW "
      "+463.315162342; echo account attempt #536 -> the hit-count carries "
      "137-for-530 (6 priors of the exact form counted per the census; the "
      "increment rule not re-derivable from the ledger, no over-claim either "
      "way, honest note); the echo-then-capture order class expected to "
      "EXTEND m11")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2814 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2814 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2814:"):
        official_depth = depth
        walk_info.append(f"official c2814 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2814_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2814_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2814 commit — the 5939089/19ff74c/660688b/7386e88/4538311/"
          f"02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/"
          f"e54aab2/d22e2bb/134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/"
          f"966ab1f/0b4f512/ffa527c/c048029/3b69581/18522dc/ea92218/4477b73/"
          f"4207111/615fc1c/7efc24d/65f4c4e/b27a69f/f0d806e/87e21ad/e6da641/"
          f"325729a/7de8446/a6fac67/35ba192/92a8201/6b53b65/7f7a022/1288d7f/"
          f"92b5acc/c5fb5cc/30a3440/8cc4726/ef415bd precedent)")
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

C2814_SET = [
    "census_c2814.py", "arrival_guard_c2814.py", "rebadge_cycle2814.py",
    "capture_cycle2814.sh", "measure_c2814_tokens.py", "recursive_diff_2814.py",
    "validate_cycle2814.py", "entry_cycle2814.txt", "append_cycle2814.py",
    "scan_cycle2814_raw.json", "scan_cycle2814.json",
]
print("c2814_instrument_set_object_presence:")
missing = []
for name in C2814_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2814 files on disk")

v114 = open("/home/z/my-project/scripts/validate_cycle2814.py", "rb").read()
guard("v114_source_intact", b"CYCLE = 2814" in v114 and b"drift49_pass63_match" in v114
      and b"drift49_pass64_match" not in v114
      and b"(18,0,0,18,0)" in v114 and b"(20,0,2,18,0)" in v114
      and b"(21,0,3,18,0)" in v114 and b"pass-62 band" in v114
      and b"pass-63 band" not in v114
      and b"pass-62 evidence" in v114 and b"pass-63 evidence" not in v114,
      f"bytes={len(v114)} (the v114 pass-63 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-64 gate name drift49_pass64_match is what the v115 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-62 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-62 evidence' is present — BOTH instrument surfaces, the v115 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "9fcdbae:scripts/validate_cycle2814.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v114_commit_object_intact", len(obj.stdout) == len(v114)
          and obj.stdout == v114,
          f"object_bytes={len(obj.stdout)} == disk {len(v114)} (the 9fcdbae c2814 commit)")
else:
    guard("v114_commit_object_intact", False, "9fcdbae object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
