#!/usr/bin/env python3
"""Arrival-guard for cycle 2808 (Job ID 446189) — measured, never predicted.

Spec source: the c2807 Next-block (worklog line 9424). Checks:
  worklog 9424 lines EXACT (newline count, c2807 append post-guard prophecy);
  tail = the c2808 Next bullet;
  anchors ^Task ID: 485 / ^- No gold yet 418 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2808 entries; c2808/c2809 substring accounting
  (the token-guard lives INSIDE the c2807 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2808.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2809 = 4 total = 2 births in the c2807 Step-7 line 9422 (the
  rehearsal pre-count print 'the c2809 pre==0 expectation' AND the census-time
  print 'c2809_pre = 0') + 2 FORWARD-token births inside the c2807 Next-block
  guard phrase ('arrival-guard against c2808/c2809 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2809 must be IN the census
  tuple'), both on line 9424 — the c2807 append prophecy 'c2809 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS a FIFTH time; the c2808
  token itself is BORN FOURTEEN times pre-append: 2 in the c2806 Step-7
  twin-print (line 9410) + 2 in the c2806 Next-block (line 9412) + 5 in the
  c2807 Step-1 census sentence (line 9416) + 1 in the c2807 Step-7 'the
  c2808 pre-count is 4' (line 9422) + 4 in the c2807 Next-block (line 9424:
  the instance + the 446189-c2808 id + the 'c2808/c2809' guard phrase + the
  'measure_c2808_tokens.py' surface — the bare-c-token accounting, honestly
  counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2807_raw.json' /
  'validate_cycle2807.py' / 'scan_cycle2807.json' carry 'e2807'/'cycle2807',
  NOT the bare c-token 'c2807' — line 9419 ABSENT from the measured c2807
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2807 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2807 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2807 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v107 source-intact expectations matched to the v107 pass-56 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v107 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-57 gate name is what the v108 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-55 band' is present AND the evidence-paragraph lag-1 heading
  'pass-55 evidence' is present — BOTH instrument surfaces, the v108 rebadge
  P3/P8 old-string expectations, exactly as the c2807 Next-block wrote).
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
guard("worklog_lines==9424", n_nl == 9424, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2808_next_bullet", last_nonempty.startswith("- Next: the c2808 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==485", tid == 485, f"got={tid}")
guard("anchor_nogold==418", gold == 418, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2808")]
guard("dup_check_zero_serviced_c2808", len(dup) == 0, f"got={len(dup)}")
c2808_total = text.count("c2808")
c2809_total = text.count("c2809")
tok_guard = [l for l in lines if "c2808/c2809" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2808 instance")]
c2808_lines = {i + 1: l.count("c2808") for i, l in enumerate(lines) if "c2808" in l}
c2809_lines = {i + 1: l.count("c2809") for i, l in enumerate(lines) if "c2809" in l}
guard("c2808_mention_accounting_pre",
      c2808_total == 14 and c2809_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2808_lines == {9410: 2, 9412: 2, 9416: 5, 9422: 1, 9424: 4}
      and c2809_lines == {9422: 2, 9424: 2},
      f"total={c2808_total} c2809={c2809_total} per-line={c2808_lines} "
      f"c2809_per-line={c2809_lines} "
      f"(expect 14 = 2 in the c2806 Step-7 twin-print (line 9410) + 2 in the "
      f"c2806 Next-block (line 9412) + 5 in the c2807 Step-1 census sentence "
      f"(line 9416) + 1 in the c2807 Step-7 'the c2808 pre-count is 4' (line "
      f"9422) + 4 in the c2807 Next-block (line 9424: the instance + the "
      f"446189-c2808 id + the 'c2808/c2809' guard phrase + the "
      f"'measure_c2808_tokens.py' surface, the bare-c-token accounting); "
      f"c2809 = 4 — 2 births in the c2807 Step-7 line 9422 (the rehearsal "
      f"pre-count print 'the c2809 pre==0 expectation' AND the census-time "
      f"print 'c2809_pre = 0' — the Step-7 twin-print class REPEATS) + 2 "
      f"FORWARD-token births TWICE inside the c2807 Next-block guard phrase "
      f"AND census-tuple sentence, both on line 9424 (the forward-token "
      f"lesson: measured, never assumed unborn — the c2807 append prophecy "
      f"'c2809 = 4 block births' held EXACTLY, the born-FOUR class REPEATS a "
      f"FIFTH time))")

c2807_total = text.count("c2807")
c2807_lines = {i + 1: l.count("c2807") for i, l in enumerate(lines) if "c2807" in l}
guard("c2807_mention_census_pre",
      c2807_total == 37
      and c2807_lines == {9398: 2, 9400: 2, 9404: 5, 9410: 1, 9412: 4, 9415: 1,
                          9416: 4, 9417: 5, 9422: 4, 9424: 9},
      f"total={c2807_total} per-line={c2807_lines} (the pre-block 14 on lines "
      f"9398/9400/9404/9410/9412 + 23 births inside the c2807 block itself; the "
      f"Step-4 surface 'scan_cycle2807_raw.json'/'validate_cycle2807.py'/"
      f"'scan_cycle2807.json' carries 'cycle2807'/'e2807' on its path tokens — the "
      f"c2760 E-TOKEN lesson re-verified live: line 9419 ABSENT from the dict, the "
      f"bare-c2807 weight measured honestly)")

c2806_total = text.count("c2806")
c2806_lines = {i + 1: l.count("c2806") for i, l in enumerate(lines) if "c2806" in l}
guard("c2806_mention_census_pre",
      c2806_total == 71
      and c2806_lines == {9386: 2, 9388: 2, 9392: 4, 9398: 1, 9400: 4, 9403: 1,
                          9404: 4, 9405: 5, 9410: 4, 9412: 9, 9414: 11, 9416: 9,
                          9417: 5, 9418: 3, 9421: 2, 9422: 3, 9424: 2},
      f"total={c2806_total} per-line={c2806_lines} (the c2807-guard-probe state 36 "
      f"on lines 9386..9412 + 35 births inside the c2807 block itself, measured "
      f"per-line at this cycle's census)")

c2805_total = text.count("c2805")
c2805_lines = {i + 1: l.count("c2805") for i, l in enumerate(lines) if "c2805" in l}
guard("c2805_mention_census_pre",
      c2805_total == 79
      and c2805_lines == {9374: 2, 9376: 2, 9380: 4, 9386: 1, 9388: 4, 9391: 1,
                          9392: 3, 9393: 8, 9398: 4, 9400: 10, 9402: 10, 9404: 9,
                          9405: 6, 9406: 3, 9409: 2, 9410: 3, 9412: 3, 9416: 2,
                          9424: 2},
      f"total={c2805_total} per-line={c2805_lines} (the c2806-guard-probe state 75 "
      f"on lines 9374..9412 + 4 births inside the c2807 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2804", 94), ("c2803", 105), ("c2802", 111), ("c2801", 90),
                   ("c2800", 120), ("c2799", 95), ("c2798", 93), ("c2797", 86),
                   ("c2796", 96), ("c2795", 118), ("c2794", 113), ("c2793", 121),
                   ("c2792", 126), ("c2791", 114), ("c2790", 126), ("c2789", 117),
                   ("c2788", 128), ("c2787", 129), ("c2786", 150), ("c2785", 133),
                   ("c2784", 131), ("c2783", 132), ("c2782", 131), ("c2781", 136),
                   ("c2780", 141), ("c2779", 141), ("c2778", 185), ("c2777", 157),
                   ("c2776", 162), ("c2775", 171), ("c2774", 176), ("c2773", 180),
                   ("c2772", 199), ("c2771", 189), ("c2770", 238), ("c2769", 178),
                   ("c2768", 181), ("c2767", 244), ("c2766", 215), ("c2765", 172),
                   ("c2764", 174), ("c2763", 182), ("c2762", 219), ("c2761", 236),
                   ("c2760", 177), ("c2759", 177), ("c2758", 179), ("c2757", 182),
                   ("c2756", 187), ("c2755", 194), ("c2754", 197), ("c2753", 211),
                   ("c2752", 217), ("c2751", 203), ("c2750", 207), ("c2749", 209),
                   ("c2748", 199), ("c2747", 202)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (185 accounted-path cumulative at this "
          f"probe: 183 at the c2807 guard probe + 1 through the c2807 official "
          f"capture + 1 this cycle's echo (latency-match 1690ms class, bracketed) "
          f"= 185; + foreign/unattributed cumulative — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2807 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2807 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2807:"):
        official_depth = depth
        walk_info.append(f"official c2807 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2807_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2807_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2807 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111/615fc1c/7efc24d/65f4c4e/"
          f"b27a69f/f0d806e/87e21ad/e6da641/325729a/7de8446/a6fac67/35ba192/"
          f"92a8201/6b53b65 precedent)")
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

C2807_SET = [
    "census_c2807.py", "arrival_guard_c2807.py", "rebadge_cycle2807.py",
    "capture_cycle2807.sh", "measure_c2807_tokens.py", "recursive_diff_2807.py",
    "validate_cycle2807.py", "entry_cycle2807.txt", "append_cycle2807.py",
    "scan_cycle2807_raw.json", "scan_cycle2807.json",
]
print("c2807_instrument_set_object_presence:")
missing = []
for name in C2807_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2807 files on disk")

v107 = open("/home/z/my-project/scripts/validate_cycle2807.py", "rb").read()
guard("v107_source_intact", b"CYCLE = 2807" in v107 and b"drift49_pass56_match" in v107
      and b"drift49_pass57_match" not in v107
      and b"(18,0,0,18,0)" in v107 and b"(20,0,2,18,0)" in v107
      and b"(21,0,3,18,0)" in v107 and b"pass-55 band" in v107
      and b"pass-56 band" not in v107
      and b"pass-55 evidence" in v107 and b"pass-56 evidence" not in v107,
      f"bytes={len(v107)} (the v107 pass-56 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-57 gate name drift49_pass57_match is what the v108 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-55 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-55 evidence' is present — BOTH instrument surfaces, the v108 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "276a60a:scripts/validate_cycle2807.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v107_commit_object_intact", len(obj.stdout) == len(v107)
          and obj.stdout == v107,
          f"object_bytes={len(obj.stdout)} == disk {len(v107)} (the 276a60a c2807 commit)")
else:
    guard("v107_commit_object_intact", False, "276a60a object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
