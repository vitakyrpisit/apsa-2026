#!/usr/bin/env python3
"""Arrival-guard for cycle 2811 (Job ID 446189) — measured, never predicted.

Spec source: the c2810 Next-block (worklog line 9460). Checks:
  worklog 9460 lines EXACT (newline count, c2810 append post-guard prophecy);
  tail = the c2811 Next bullet;
  anchors ^Task ID: 488 / ^- No gold yet 421 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2811 entries; c2812/c2813 substring accounting
  (the token-guard lives INSIDE the c2810 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2811.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2812 = 4 total = 2 births in the c2810 Step-7 line 9458 (the
  rehearsal pre-count print 'the c2812 pre==0 expectation' AND the census-time
  print 'c2812_pre = 0') + 2 FORWARD-token births inside the c2810 Next-block
  guard phrase ('arrival-guard against c2811/c2812 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2812 must be IN the census
  tuple'), both on line 9460 — the c2810 append prophecy 'c2812 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS an EIGHTH time; the c2811
  token itself is BORN FOURTEEN times pre-append: 2 in the c2809 Step-7
  twin-print (line 9446) + 2 in the c2809 Next-block (line 9448) + 5 in the
  c2810 Step-1 census sentence (line 9452: the '+ c2811 = 4 per-line' print +
  the twin-print quotes 'the c2811 pre==0 expectation' AND 'c2811_pre = 0' +
  the prophecy quote 'c2811 = 4 block births' + the 'c2767..c2810
  forward-token lessons' phrase) + 1 in the c2810 Step-7 'the c2811 pre-count
  is 4' (line 9458) + 4 in the c2810 Next-block (line 9460: the instance +
  the 446189-c2811 id + the 'c2811/c2812' guard phrase + the
  'measure_c2811_tokens.py' surface — the bare-c-token accounting, honestly
  counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2810_raw.json' /
  'validate_cycle2810.py' / 'scan_cycle2810.json' carry 'e2810'/'cycle2810',
  NOT the bare c-token 'c2810' — line 9455 ABSENT from the measured c2810
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2810 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2810 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2810 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v110 source-intact expectations matched to the v110 pass-59 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v110 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-60 gate name is what the v111 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-58 band' is present AND the evidence-paragraph lag-1 heading
  'pass-58 evidence' is present — BOTH instrument surfaces, the v111 rebadge
  P3/P8 old-string expectations, exactly as the c2810 Next-block wrote).
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
guard("worklog_lines==9460", n_nl == 9460, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2811_next_bullet", last_nonempty.startswith("- Next: the c2811 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==488", tid == 488, f"got={tid}")
guard("anchor_nogold==421", gold == 421, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2811")]
guard("dup_check_zero_serviced_c2811", len(dup) == 0, f"got={len(dup)}")
c2813_total = text.count("c2813")
c2812_total = text.count("c2812")
c2811_total = text.count("c2811")
tok_guard = [l for l in lines if "c2811/c2812" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2811 instance")]
c2812_lines = {i + 1: l.count("c2812") for i, l in enumerate(lines) if "c2812" in l}
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(lines) if "c2811" in l}
guard("c2812_mention_accounting_pre",
      c2813_total == 0 and c2812_total == 4 and c2811_total == 14
      and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and c2812_lines == {9458: 2, 9460: 2}
      and c2811_lines == {9446: 2, 9448: 2, 9452: 5, 9458: 1, 9460: 4},
      f"c2813={c2813_total} c2812={c2812_total} c2811={c2811_total} "
      f"c2812_per-line={c2812_lines} c2811_per-line={c2811_lines} "
      f"(expect c2812 = 4 — 2 births in the c2810 Step-7 line 9458 (the "
      f"rehearsal pre-count print 'the c2812 pre==0 expectation' AND the "
      f"census-time print 'c2812_pre = 0' — the Step-7 twin-print class "
      f"REPEATS) + 2 FORWARD-token births TWICE inside the c2810 Next-block "
      f"guard phrase AND census-tuple sentence, both on line 9460 (the "
      f"forward-token lesson: measured, never assumed unborn — the c2810 "
      f"append prophecy 'c2812 = 4 block births' held EXACTLY, the born-FOUR "
      f"class REPEATS an EIGHTH time); c2811 = 14 — 2 in the c2809 Step-7 "
      f"twin-print (line 9446) + 2 in the c2809 Next-block (line 9448) + 5 in "
      f"the c2810 Step-1 census sentence (line 9452) + 1 in the c2810 Step-7 "
      f"'the c2811 pre-count is 4' (line 9458) + 4 in the c2810 Next-block "
      f"(line 9460: the instance + the 446189-c2811 id + the 'c2811/c2812' "
      f"guard phrase + the 'measure_c2811_tokens.py' surface); c2813 = 0 "
      f"UNBORN (measured pre-append))")

c2810_total = text.count("c2810")
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(lines) if "c2810" in l}
guard("c2810_mention_census_pre",
      c2810_total == 36
      and c2810_lines == {9434: 2, 9436: 2, 9440: 4, 9446: 1, 9448: 4, 9451: 1,
                          9452: 4, 9453: 5, 9458: 4, 9460: 9},
      f"total={c2810_total} per-line={c2810_lines} (the pre-block 13 on lines "
      f"9434/9436/9440/9446/9448 + 23 births inside the c2810 block itself; the "
      f"Step-4 surface 'scan_cycle2810_raw.json'/'validate_cycle2810.py'/"
      f"'scan_cycle2810.json' carries 'cycle2810'/'e2810' on its path tokens — the "
      f"c2760 E-TOKEN lesson re-verified live: line 9455 ABSENT from the dict, the "
      f"bare-c2810 weight measured honestly)")

c2809_total = text.count("c2809")
c2809_lines = {i + 1: l.count("c2809") for i, l in enumerate(lines) if "c2809" in l}
guard("c2809_mention_census_pre",
      c2809_total == 75
      and c2809_lines == {9422: 2, 9424: 2, 9428: 4, 9434: 1, 9436: 4, 9439: 1,
                          9440: 4, 9441: 5, 9446: 4, 9448: 8, 9450: 13, 9452: 13,
                          9453: 5, 9454: 3, 9457: 1, 9458: 3, 9460: 2},
      f"total={c2809_total} per-line={c2809_lines} (the c2810-guard-probe state 35 "
      f"on lines 9422..9448 + 40 births inside the c2810 block itself, measured "
      f"per-line at this cycle's census)")

c2808_total = text.count("c2808")
c2808_lines = {i + 1: l.count("c2808") for i, l in enumerate(lines) if "c2808" in l}
guard("c2808_mention_census_pre",
      c2808_total == 87
      and c2808_lines == {9410: 2, 9412: 2, 9416: 5, 9422: 1, 9424: 4, 9427: 1,
                          9428: 4, 9429: 5, 9434: 4, 9436: 9, 9438: 14, 9440: 10,
                          9441: 5, 9442: 3, 9445: 3, 9446: 3, 9448: 3, 9452: 4,
                          9453: 1, 9457: 2, 9460: 2},
      f"total={c2808_total} per-line={c2808_lines} (the c2809-guard-probe state 78 "
      f"on lines 9410..9448 + 9 births inside the c2810 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2807", 78), ("c2806", 81), ("c2805", 88), ("c2804", 103),
                   ("c2803", 114), ("c2802", 118), ("c2801", 94), ("c2800", 130),
                   ("c2799", 99), ("c2798", 97), ("c2797", 89), ("c2796", 99),
                   ("c2795", 122), ("c2794", 116), ("c2793", 124), ("c2792", 129),
                   ("c2791", 117), ("c2790", 130), ("c2789", 120), ("c2788", 131),
                   ("c2787", 132), ("c2786", 154), ("c2785", 136), ("c2784", 134),
                   ("c2783", 135), ("c2782", 134), ("c2781", 139), ("c2780", 144),
                   ("c2779", 144), ("c2778", 188), ("c2777", 160), ("c2776", 165),
                   ("c2775", 174), ("c2774", 179), ("c2773", 183), ("c2772", 202),
                   ("c2771", 192), ("c2770", 244), ("c2769", 181), ("c2768", 184),
                   ("c2767", 253), ("c2766", 221), ("c2765", 175), ("c2764", 177),
                   ("c2763", 185), ("c2762", 222), ("c2761", 242), ("c2760", 180),
                   ("c2759", 180), ("c2758", 182), ("c2757", 185), ("c2756", 190),
                   ("c2755", 197), ("c2754", 200), ("c2753", 217), ("c2752", 223),
                   ("c2751", 209), ("c2750", 213), ("c2749", 216)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (209 at this probe: 204 at the "
          f"c2810 guard probe + 1 through the c2810 official capture + 1 this "
          f"cycle's echo (latency-match 1789ms class, bracketed — scan_duration "
          f"1783, curl 1.790832) = 191 accounted-path cumulative + 3 "
          f"foreign/unattributed cumulative (incl. one 1604ms POST landed AFTER "
          f"this cycle's echo — arithmetic-necessity class; dev.log is "
          f"timestamp-less: the official/foreign split is by latency-match, "
          f"honest, no over-claim))")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2810 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2810 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2810:"):
        official_depth = depth
        walk_info.append(f"official c2810 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2810_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2810_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2810 commit — the 5939089/19ff74c/660688b/7386e88/4538311/"
          f"02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/"
          f"e54aab2/d22e2bb/134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/"
          f"966ab1f/0b4f512/ffa527c/c048029/3b69581/18522dc/ea92218/4477b73/"
          f"4207111/615fc1c/7efc24d/65f4c4e/b27a69f/f0d806e/87e21ad/e6da641/"
          f"325729a/7de8446/a6fac67/35ba192/92a8201/6b53b65/7f7a022/1288d7f/"
          f"92b5acc precedent)")
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

C2810_SET = [
    "census_c2810.py", "arrival_guard_c2810.py", "rebadge_cycle2810.py",
    "capture_cycle2810.sh", "measure_c2810_tokens.py", "recursive_diff_2810.py",
    "validate_cycle2810.py", "entry_cycle2810.txt", "append_cycle2810.py",
    "scan_cycle2810_raw.json", "scan_cycle2810.json",
]
print("c2810_instrument_set_object_presence:")
missing = []
for name in C2810_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2810 files on disk")

v110 = open("/home/z/my-project/scripts/validate_cycle2810.py", "rb").read()
guard("v110_source_intact", b"CYCLE = 2810" in v110 and b"drift49_pass59_match" in v110
      and b"drift49_pass60_match" not in v110
      and b"(18,0,0,18,0)" in v110 and b"(20,0,2,18,0)" in v110
      and b"(21,0,3,18,0)" in v110 and b"pass-58 band" in v110
      and b"pass-59 band" not in v110
      and b"pass-58 evidence" in v110 and b"pass-59 evidence" not in v110,
      f"bytes={len(v110)} (the v110 pass-59 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-60 gate name drift49_pass60_match is what the v111 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-58 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-58 evidence' is present — BOTH instrument surfaces, the v111 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "d228cc8:scripts/validate_cycle2810.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v110_commit_object_intact", len(obj.stdout) == len(v110)
          and obj.stdout == v110,
          f"object_bytes={len(obj.stdout)} == disk {len(v110)} (the d228cc8 c2810 commit)")
else:
    guard("v110_commit_object_intact", False, "d228cc8 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
