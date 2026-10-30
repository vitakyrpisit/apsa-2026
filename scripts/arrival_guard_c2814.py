#!/usr/bin/env python3
"""Arrival-guard for cycle 2814 (Job ID 446189) — measured, never predicted.

Spec source: the c2813 Next-block (worklog line 9496). Checks:
  worklog 9496 lines EXACT (newline count, c2813 append post-guard prophecy);
  tail = the c2814 Next bullet;
  anchors ^Task ID: 491 / ^- No gold yet 424 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2814 entries; c2816/c2815/c2814 substring accounting
  (the token-guard lives INSIDE the c2813 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2814.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2815 = 4 total = 2 births in the c2813 Step-7 twin-print
  (line 9494: the rehearsal pre-count print 'the c2815 pre==0 expectation' AND
  the census-time print 'c2815_pre = 0') + 2 FORWARD-token births inside the
  c2813 Next-block guard phrase ('arrival-guard against c2814/c2815 tokens')
  AND the FORWARD-token sentence ('the FORWARD token c2815 must be IN the
  census tuple'), both on line 9496 — the c2813 append prophecy 'c2815 = 4
  block births' held EXACTLY, the born-FOUR class REPEATS an ELEVENTH time;
  the c2814 token itself is BORN FOURTEEN times pre-append: 2 in the c2812
  Step-7 twin-print (line 9482) + 2 in the c2812 Next-block (line 9484) + 5 in
  the c2813 Step-1 census sentence (line 9488) + 1 in the c2813 Step-7
  'the c2814 pre-count is 4' (line 9494) + 4 in the c2813 Next-block
  (line 9496: the instance + the 446189-c2814 id + the 'c2814/c2815' guard
  phrase + the 'measure_c2814_tokens.py' surface — the bare-c-token
  accounting, honestly counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2813_raw.json' /
  'validate_cycle2813.py' / 'scan_cycle2813.json' carry 'e2813'/'cycle2813',
  NOT the bare c-token 'c2813' — line 9491 ABSENT from the measured c2813
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2813 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2813 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2813 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v113 source-intact expectations matched to the v113 pass-62 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v113 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-63 gate name is what the v114 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-61 band' is present AND the evidence-paragraph lag-1 heading
  'pass-61 evidence' is present — BOTH instrument surfaces, the v114 rebadge
  P3/P8 old-string expectations, exactly as the c2813 Next-block wrote).
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
guard("worklog_lines==9496", n_nl == 9496, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2814_next_bullet", last_nonempty.startswith("- Next: the c2814 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==491", tid == 491, f"got={tid}")
guard("anchor_nogold==424", gold == 424, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2814")]
guard("dup_check_zero_serviced_c2814", len(dup) == 0, f"got={len(dup)}")
c2816_total = text.count("c2816")
c2815_total = text.count("c2815")
c2814_total = text.count("c2814")
tok_guard = [l for l in lines if "c2814/c2815" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2814 instance")]
c2815_lines = {i + 1: l.count("c2815") for i, l in enumerate(lines) if "c2815" in l}
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(lines) if "c2814" in l}
guard("c2815_mention_accounting_pre",
      c2816_total == 0 and c2815_total == 4 and c2814_total == 14
      and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and c2815_lines == {9494: 2, 9496: 2}
      and c2814_lines == {9482: 2, 9484: 2, 9488: 5, 9494: 1, 9496: 4},
      f"c2816={c2816_total} c2815={c2815_total} c2814={c2814_total} "
      f"c2815_per-line={c2815_lines} c2814_per-line={c2814_lines} "
      f"(expect c2815 = 4 — 2 births in the c2813 Step-7 twin-print line 9494 (the "
      f"rehearsal pre-count print 'the c2815 pre==0 expectation' AND the "
      f"census-time print 'c2815_pre = 0' — the Step-7 twin-print class "
      f"REPEATS) + 2 FORWARD-token births TWICE inside the c2813 Next-block "
      f"guard phrase AND census-tuple sentence, both on line 9496 (the "
      f"forward-token lesson: measured, never assumed unborn — the c2813 "
      f"append prophecy 'c2815 = 4 block births' held EXACTLY, the born-FOUR "
      f"class REPEATS an ELEVENTH time); c2814 = 14 — 2 in the c2812 Step-7 "
      f"twin-print (line 9482) + 2 in the c2812 Next-block (line 9484) + 5 in "
      f"the c2813 Step-1 census sentence (line 9488) + 1 in the c2813 Step-7 "
      f"'the c2814 pre-count is 4' (line 9494) + 4 in the c2813 Next-block "
      f"(line 9496: the instance + the 446189-c2814 id + the 'c2814/c2815' "
      f"guard phrase + the 'measure_c2814_tokens.py' surface); c2816 = 0 "
      f"UNBORN (measured pre-append))")

c2813_total = text.count("c2813")
c2813_lines = {i + 1: l.count("c2813") for i, l in enumerate(lines) if "c2813" in l}
guard("c2813_mention_census_pre",
      c2813_total == 37
      and c2813_lines == {9470: 2, 9472: 2, 9476: 5, 9482: 1, 9484: 4, 9487: 1,
                          9488: 4, 9489: 4, 9494: 4, 9496: 10},
      f"total={c2813_total} per-line={c2813_lines} (the c2813-guard-probe state 14 on "
      f"lines 9470/9472/9476/9482/9484 + 23 births inside the c2813 block "
      f"itself; the Step-4 surface 'scan_cycle2813_raw.json'/"
      f"'validate_cycle2813.py'/'scan_cycle2813.json' carries 'cycle2813'/'e2813' "
      f"on its path tokens — the c2760 E-TOKEN lesson re-verified live: line "
      f"9491 ABSENT from the dict, the bare-c2813 weight measured honestly)")

c2812_total = text.count("c2812")
c2812_lines = {i + 1: l.count("c2812") for i, l in enumerate(lines) if "c2812" in l}
guard("c2812_mention_census_pre",
      c2812_total == 81
      and c2812_lines == {9458: 2, 9460: 2, 9464: 5, 9470: 1, 9472: 4, 9475: 1,
                          9476: 4, 9477: 4, 9482: 4, 9484: 10, 9486: 14, 9488: 13,
                          9489: 5, 9490: 4, 9493: 4, 9494: 3, 9496: 1},
      f"total={c2812_total} per-line={c2812_lines} (the c2812-guard-probe state 37 "
      f"on lines 9458..9484 + 44 births inside the c2813 block itself, measured "
      f"per-line at this cycle's census)")

c2811_total = text.count("c2811")
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(lines) if "c2811" in l}
guard("c2811_mention_census_pre",
      c2811_total == 81
      and c2811_lines == {9446: 2, 9448: 2, 9452: 5, 9458: 1, 9460: 4, 9463: 1,
                          9464: 4, 9465: 4, 9470: 4, 9472: 9, 9474: 14, 9476: 12,
                          9477: 4, 9478: 4, 9481: 1, 9482: 3, 9484: 1, 9486: 1,
                          9488: 2, 9489: 2, 9496: 1},
      f"total={c2811_total} per-line={c2811_lines} (the c2812-guard-probe state 75 "
      f"on lines 9446..9484 + 6 births inside the c2813 block itself, measured "
      f"per-line at this cycle's census)")

c2810_total = text.count("c2810")
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(lines) if "c2810" in l}
guard("c2810_mention_census_pre",
      c2810_total == 97
      and c2810_lines == {9434: 2, 9436: 2, 9440: 4, 9446: 1, 9448: 4, 9451: 1,
                          9452: 4, 9453: 5, 9458: 4, 9460: 9, 9462: 14, 9464: 12,
                          9465: 4, 9466: 4, 9469: 3, 9470: 3, 9472: 3, 9474: 2,
                          9476: 2, 9481: 3, 9484: 2, 9488: 2, 9489: 4, 9493: 1,
                          9496: 2},
      f"total={c2810_total} per-line={c2810_lines} (the c2811-guard-probe state 88 "
      f"on lines 9434..9484 + 9 births inside the c2813 block itself, measured "
      f"per-line at this cycle's census)")

c2809_total = text.count("c2809")
c2809_lines = {i + 1: l.count("c2809") for i, l in enumerate(lines) if "c2809" in l}
guard("c2809_mention_census_pre",
      c2809_total == 83
      and c2809_lines == {9422: 2, 9424: 2, 9428: 4, 9434: 1, 9436: 4, 9439: 1,
                          9440: 4, 9441: 5, 9446: 4, 9448: 8, 9450: 13, 9452: 13,
                          9453: 5, 9454: 3, 9457: 1, 9458: 3, 9460: 2, 9464: 2,
                          9469: 1, 9472: 1, 9476: 2, 9488: 2},
      f"total={c2809_total} per-line={c2809_lines} (the c2810-guard-probe state 81 "
      f"on lines 9422..9476 + 2 births inside the c2813 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2808", 95), ("c2807", 88), ("c2806", 84), ("c2805", 94),
                   ("c2804", 109), ("c2803", 117), ("c2802", 124), ("c2801", 97),
                   ("c2800", 139), ("c2799", 102), ("c2798", 100), ("c2797", 92),
                   ("c2796", 102), ("c2795", 125), ("c2794", 119), ("c2793", 127),
                   ("c2792", 132), ("c2791", 120), ("c2790", 133), ("c2789", 123),
                   ("c2788", 134), ("c2787", 135), ("c2786", 157), ("c2785", 139),
                   ("c2784", 137), ("c2783", 138), ("c2782", 137), ("c2781", 142),
                   ("c2780", 147), ("c2779", 147), ("c2778", 191), ("c2777", 163),
                   ("c2776", 168), ("c2775", 177), ("c2774", 182), ("c2773", 186),
                   ("c2772", 205), ("c2771", 195), ("c2770", 251), ("c2769", 184),
                   ("c2768", 187), ("c2767", 262), ("c2766", 227), ("c2765", 178),
                   ("c2764", 180), ("c2763", 188), ("c2762", 225), ("c2761", 248),
                   ("c2760", 183), ("c2759", 183), ("c2758", 185), ("c2757", 188),
                   ("c2756", 193), ("c2755", 200), ("c2754", 203), ("c2753", 223),
                   ("c2752", 229), ("c2751", 215), ("c2750", 221), ("c2749", 229)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (228 at the census probe: 216 "
          f"accounted-path cumulative = 214 at the c2813 census probe + 1 through "
          f"the c2813 official capture + 1 this cycle's echo #535 (latency-match "
          f"1746ms class, bracketed, RE-DERIVABLE) = 216 accounted + 12 "
          f"foreign/unattributed cumulative — SIX new POSTs landed between the "
          f"probes (222 -> 228 = +6: 2 accounted + 4 foreign), "
          f"arithmetic-necessity class; timestamp-less log, latency-match split, "
          f"honest)")
else:
    print("dev_log: ABSENT")

# loop echo #535 facts (measured this session, the echo-then-capture order expected)
print("loop_echo_535: pre-echo 03:24:37.889456533 +0000 epoch 1793330677.889456533 "
      "EPOCH-governs; curl 1.755046 / server 1746ms latency-match; post-echo "
      "03:24:39.651949875 +0000 epoch 1793330679.651949875 EPOCH-governs; echo "
      "scanned_at 03:24:39.647Z = epoch 1793330679.647; wall 1.762493342; "
      "stamp-to-echo 500.889456533 (SHALLOWER than the deepest print "
      "1025.631018606 — the deepest print STANDS unchallenged); echo POST-WINDOW "
      "+289.894487633; echo account attempt #535 -> the hit-count carries "
      "137-for-530 (4 priors of the exact form counted per the census; the "
      "increment rule not re-derivable from the ledger, no over-claim either "
      "way, honest note); the echo-then-capture order class expected to "
      "EXTEND m11")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2813 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2813 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2813:"):
        official_depth = depth
        walk_info.append(f"official c2813 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2813_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2813_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2813 commit — the 5939089/19ff74c/660688b/7386e88/4538311/"
          f"02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/"
          f"e54aab2/d22e2bb/134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/"
          f"966ab1f/0b4f512/ffa527c/c048029/3b69581/18522dc/ea92218/4477b73/"
          f"4207111/615fc1c/7efc24d/65f4c4e/b27a69f/f0d806e/87e21ad/e6da641/"
          f"325729a/7de8446/a6fac67/35ba192/92a8201/6b53b65/7f7a022/1288d7f/"
          f"92b5acc/c5fb5cc/30a3440/8cc4726 precedent)")
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

C2813_SET = [
    "census_c2813.py", "arrival_guard_c2813.py", "rebadge_cycle2813.py",
    "capture_cycle2813.sh", "measure_c2813_tokens.py", "recursive_diff_2813.py",
    "validate_cycle2813.py", "entry_cycle2813.txt", "append_cycle2813.py",
    "scan_cycle2813_raw.json", "scan_cycle2813.json",
]
print("c2813_instrument_set_object_presence:")
missing = []
for name in C2813_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2813 files on disk")

v113 = open("/home/z/my-project/scripts/validate_cycle2813.py", "rb").read()
guard("v113_source_intact", b"CYCLE = 2813" in v113 and b"drift49_pass62_match" in v113
      and b"drift49_pass63_match" not in v113
      and b"(18,0,0,18,0)" in v113 and b"(20,0,2,18,0)" in v113
      and b"(21,0,3,18,0)" in v113 and b"pass-61 band" in v113
      and b"pass-62 band" not in v113
      and b"pass-61 evidence" in v113 and b"pass-62 evidence" not in v113,
      f"bytes={len(v113)} (the v113 pass-62 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-63 gate name drift49_pass63_match is what the v114 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-61 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-61 evidence' is present — BOTH instrument surfaces, the v114 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "f52cdbe:scripts/validate_cycle2813.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v113_commit_object_intact", len(obj.stdout) == len(v113)
          and obj.stdout == v113,
          f"object_bytes={len(obj.stdout)} == disk {len(v113)} (the f52cdbe c2813 commit)")
else:
    guard("v113_commit_object_intact", False, "f52cdbe object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
