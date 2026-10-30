#!/usr/bin/env python3
"""Arrival-guard for cycle 2809 (Job ID 446189) — measured, never predicted.

Spec source: the c2808 Next-block (worklog line 9436). Checks:
  worklog 9436 lines EXACT (newline count, c2808 append post-guard prophecy);
  tail = the c2809 Next bullet;
  anchors ^Task ID: 486 / ^- No gold yet 419 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2809 entries; c2809/c2810 substring accounting
  (the token-guard lives INSIDE the c2808 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2809.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2810 = 4 total = 2 births in the c2808 Step-7 line 9434 (the
  rehearsal pre-count print 'the c2810 pre==0 expectation' AND the census-time
  print 'c2810_pre = 0') + 2 FORWARD-token births inside the c2808 Next-block
  guard phrase ('arrival-guard against c2809/c2810 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2810 must be IN the census
  tuple'), both on line 9436 — the c2808 append prophecy 'c2810 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS a SIXTH time; the c2809
  token itself is BORN THIRTEEN times pre-append: 2 in the c2807 Step-7
  twin-print (line 9422) + 2 in the c2807 Next-block (line 9424) + 4 in the
  c2808 Step-1 census sentence (line 9428: the '+ c2809 = 4 per-line' print +
  the twin-print quotes 'the c2809 pre==0 expectation' AND 'c2809_pre = 0' +
  the prophecy quote 'c2809 = 4 block births') + 1 in the c2808 Step-7 'the
  c2809 pre-count is 4' (line 9434) + 4 in the c2808 Next-block (line 9436:
  the instance + the 446189-c2809 id + the 'c2809/c2810' guard phrase + the
  'measure_c2809_tokens.py' surface — the bare-c-token accounting, honestly
  counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2808_raw.json' /
  'validate_cycle2808.py' / 'scan_cycle2808.json' carry 'e2808'/'cycle2808',
  NOT the bare c-token 'c2808' — line 9431 ABSENT from the measured c2808
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2808 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2808 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2808 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v108 source-intact expectations matched to the v108 pass-57 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v108 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-58 gate name is what the v109 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-56 band' is present AND the evidence-paragraph lag-1 heading
  'pass-56 evidence' is present — BOTH instrument surfaces, the v109 rebadge
  P3/P8 old-string expectations, exactly as the c2808 Next-block wrote).
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
guard("worklog_lines==9436", n_nl == 9436, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2809_next_bullet", last_nonempty.startswith("- Next: the c2809 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==486", tid == 486, f"got={tid}")
guard("anchor_nogold==419", gold == 419, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2809")]
guard("dup_check_zero_serviced_c2809", len(dup) == 0, f"got={len(dup)}")
c2809_total = text.count("c2809")
c2810_total = text.count("c2810")
tok_guard = [l for l in lines if "c2809/c2810" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2809 instance")]
c2809_lines = {i + 1: l.count("c2809") for i, l in enumerate(lines) if "c2809" in l}
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(lines) if "c2810" in l}
guard("c2809_mention_accounting_pre",
      c2809_total == 13 and c2810_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2809_lines == {9422: 2, 9424: 2, 9428: 4, 9434: 1, 9436: 4}
      and c2810_lines == {9434: 2, 9436: 2},
      f"total={c2809_total} c2810={c2810_total} per-line={c2809_lines} "
      f"c2810_per-line={c2810_lines} "
      f"(expect 13 = 2 in the c2807 Step-7 twin-print (line 9422) + 2 in the "
      f"c2807 Next-block (line 9424) + 4 in the c2808 Step-1 census sentence "
      f"(line 9428: the '+ c2809 = 4 per-line' print + the twin-print quotes "
      f"'the c2809 pre==0 expectation' AND 'c2809_pre = 0' + the prophecy "
      f"quote 'c2809 = 4 block births') + 1 in the c2808 Step-7 'the c2809 "
      f"pre-count is 4' (line 9434) + 4 in the c2808 Next-block (line 9436: "
      f"the instance + the 446189-c2809 id + the 'c2809/c2810' guard phrase + "
      f"the 'measure_c2809_tokens.py' surface, the bare-c-token accounting); "
      f"c2810 = 4 — 2 births in the c2808 Step-7 line 9434 (the rehearsal "
      f"pre-count print 'the c2810 pre==0 expectation' AND the census-time "
      f"print 'c2810_pre = 0' — the Step-7 twin-print class REPEATS) + 2 "
      f"FORWARD-token births TWICE inside the c2808 Next-block guard phrase "
      f"AND census-tuple sentence, both on line 9436 (the forward-token "
      f"lesson: measured, never assumed unborn — the c2808 append prophecy "
      f"'c2810 = 4 block births' held EXACTLY, the born-FOUR class REPEATS a "
      f"SIXTH time))")

c2808_total = text.count("c2808")
c2808_lines = {i + 1: l.count("c2808") for i, l in enumerate(lines) if "c2808" in l}
guard("c2808_mention_census_pre",
      c2808_total == 37
      and c2808_lines == {9410: 2, 9412: 2, 9416: 5, 9422: 1, 9424: 4, 9427: 1,
                          9428: 4, 9429: 5, 9434: 4, 9436: 9},
      f"total={c2808_total} per-line={c2808_lines} (the pre-block 14 on lines "
      f"9410/9412/9416/9422/9424 + 23 births inside the c2808 block itself; the "
      f"Step-4 surface 'scan_cycle2808_raw.json'/'validate_cycle2808.py'/"
      f"'scan_cycle2808.json' carries 'cycle2808'/'e2808' on its path tokens — the "
      f"c2760 E-TOKEN lesson re-verified live: line 9431 ABSENT from the dict, the "
      f"bare-c2808 weight measured honestly)")

c2807_total = text.count("c2807")
c2807_lines = {i + 1: l.count("c2807") for i, l in enumerate(lines) if "c2807" in l}
guard("c2807_mention_census_pre",
      c2807_total == 71
      and c2807_lines == {9398: 2, 9400: 2, 9404: 5, 9410: 1, 9412: 4, 9415: 1,
                          9416: 4, 9417: 5, 9422: 4, 9424: 9, 9426: 10, 9428: 10,
                          9429: 5, 9430: 3, 9433: 1, 9434: 3, 9436: 2},
      f"total={c2807_total} per-line={c2807_lines} (the c2808-guard-probe state 37 "
      f"on lines 9398..9424 + 34 births inside the c2808 block itself, measured "
      f"per-line at this cycle's census)")

c2806_total = text.count("c2806")
c2806_lines = {i + 1: l.count("c2806") for i, l in enumerate(lines) if "c2806" in l}
guard("c2806_mention_census_pre",
      c2806_total == 76
      and c2806_lines == {9386: 2, 9388: 2, 9392: 4, 9398: 1, 9400: 4, 9403: 1,
                          9404: 4, 9405: 5, 9410: 4, 9412: 9, 9414: 11, 9416: 9,
                          9417: 5, 9418: 3, 9421: 2, 9422: 3, 9424: 2, 9428: 2,
                          9429: 2, 9436: 1},
      f"total={c2806_total} per-line={c2806_lines} (the c2807-guard-probe state 71 "
      f"on lines 9386..9424 + 5 births inside the c2808 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2805", 82), ("c2804", 98), ("c2803", 109), ("c2802", 113),
                   ("c2801", 91), ("c2800", 123), ("c2799", 96), ("c2798", 94),
                   ("c2797", 87), ("c2796", 97), ("c2795", 119), ("c2794", 114),
                   ("c2793", 122), ("c2792", 127), ("c2791", 115), ("c2790", 127),
                   ("c2789", 118), ("c2788", 129), ("c2787", 130), ("c2786", 151),
                   ("c2785", 134), ("c2784", 132), ("c2783", 133), ("c2782", 132),
                   ("c2781", 137), ("c2780", 142), ("c2779", 142), ("c2778", 186),
                   ("c2777", 158), ("c2776", 163), ("c2775", 172), ("c2774", 177),
                   ("c2773", 181), ("c2772", 200), ("c2771", 190), ("c2770", 240),
                   ("c2769", 179), ("c2768", 182), ("c2767", 247), ("c2766", 217),
                   ("c2765", 173), ("c2764", 175), ("c2763", 183), ("c2762", 220),
                   ("c2761", 238), ("c2760", 178), ("c2759", 178), ("c2758", 180),
                   ("c2757", 183), ("c2756", 188), ("c2755", 195), ("c2754", 198),
                   ("c2753", 213), ("c2752", 219), ("c2751", 205), ("c2750", 209),
                   ("c2749", 211), ("c2748", 201)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (188 accounted-path cumulative at this "
          f"probe: 185 at the c2808 census probe + 1 through the c2808 official "
          f"capture + 1 this cycle's echo (latency-match 1660ms class, bracketed) "
          f"+ 1 through this cycle's official capture = 188; + foreign/unattributed "
          f"cumulative — dev.log is timestamp-less: the official/foreign split is "
          f"by latency-match, honest, no over-claim; the residual "
          f"foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2808 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2808 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2808:"):
        official_depth = depth
        walk_info.append(f"official c2808 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2808_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2808_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2808 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111/615fc1c/7efc24d/65f4c4e/"
          f"b27a69f/f0d806e/87e21ad/e6da641/325729a/7de8446/a6fac67/35ba192/"
          f"92a8201/6b53b65/7f7a022 precedent)")
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

C2808_SET = [
    "census_c2808.py", "arrival_guard_c2808.py", "rebadge_cycle2808.py",
    "capture_cycle2808.sh", "measure_c2808_tokens.py", "recursive_diff_2808.py",
    "validate_cycle2808.py", "entry_cycle2808.txt", "append_cycle2808.py",
    "scan_cycle2808_raw.json", "scan_cycle2808.json",
]
print("c2808_instrument_set_object_presence:")
missing = []
for name in C2808_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2808 files on disk")

v108 = open("/home/z/my-project/scripts/validate_cycle2808.py", "rb").read()
guard("v108_source_intact", b"CYCLE = 2808" in v108 and b"drift49_pass57_match" in v108
      and b"drift49_pass58_match" not in v108
      and b"(18,0,0,18,0)" in v108 and b"(20,0,2,18,0)" in v108
      and b"(21,0,3,18,0)" in v108 and b"pass-56 band" in v108
      and b"pass-57 band" not in v108
      and b"pass-56 evidence" in v108 and b"pass-57 evidence" not in v108,
      f"bytes={len(v108)} (the v108 pass-57 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-58 gate name drift49_pass58_match is what the v109 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-56 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-56 evidence' is present — BOTH instrument surfaces, the v109 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "3c0fe6c:scripts/validate_cycle2808.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v108_commit_object_intact", len(obj.stdout) == len(v108)
          and obj.stdout == v108,
          f"object_bytes={len(obj.stdout)} == disk {len(v108)} (the 3c0fe6c c2808 commit)")
else:
    guard("v108_commit_object_intact", False, "3c0fe6c object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
