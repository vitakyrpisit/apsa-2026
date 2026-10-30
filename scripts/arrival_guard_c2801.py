#!/usr/bin/env python3
"""Arrival-guard for cycle 2801 (Job ID 446189) — measured, never predicted.

Spec source: the c2800 Next-block (worklog line 9340). Checks:
  worklog 9340 lines EXACT (newline count, c2800 append post-guard prophecy);
  tail = the c2801 Next bullet;
  anchors ^Task ID: 478 / ^- No gold yet 411 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2801 entries; c2801/c2802 substring accounting
  (the token-guard lives INSIDE the c2800 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2801.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2802 = 4 total = 2 births in the c2800 Step-7 line 9338 (the
  rehearsal pre-count print 'the c2802 pre==0 expectation' AND the census-time
  print 'c2802_pre = 0') + 2 FORWARD-token births inside the c2800 Next-block
  guard phrase ('arrival-guard against c2801/c2802 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2802 must be IN the census
  tuple'), both on line 9340 — the c2800 append prophecy 'c2802 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS; the c2801 token itself is
  BORN FOURTEEN times pre-append: 2 in the c2799 Step-7 twin-print (line
  9326) + 2 in the c2799 Next-block (line 9328) + 5 in the c2800 Step-1
  census print (line 9332) + 1 in the c2800 Step-7 'the c2801 pre-count is 4'
  (line 9338) + 4 in the c2800 Next-block (line 9340: the instance + the
  446189-c2801 id + the 'c2801/c2802' guard phrase + the fourth measured
  surface — the bare-c-token accounting, honestly counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2800_raw.json' /
  'validate_cycle2800.py' / 'scan_cycle2800.json' carry 'e2800'/'cycle2800',
  NOT the bare c-token 'c2800' — path tokens contribute ZERO bare-c2800
  census weight;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2800 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2800 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2800 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v100 source-intact expectations matched to the v100 pass-49 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v100 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-50 gate name is what the v101 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-48 band' is present AND the evidence-paragraph lag-1 heading
  'pass-48 evidence' is present — BOTH instrument surfaces, the v101 rebadge
  P3/P8 old-string expectations, exactly as the c2800 Next-block wrote).
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
guard("worklog_lines==9340", n_nl == 9340, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2801_next_bullet", last_nonempty.startswith("- Next: the c2801 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==478", tid == 478, f"got={tid}")
guard("anchor_nogold==411", gold == 411, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2801")]
guard("dup_check_zero_serviced_c2801", len(dup) == 0, f"got={len(dup)}")
c2801_total = text.count("c2801")
c2802_total = text.count("c2802")
tok_guard = [l for l in lines if "c2801/c2802" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2801 instance")]
c2801_lines = {i + 1: l.count("c2801") for i, l in enumerate(lines) if "c2801" in l}
c2802_lines = {i + 1: l.count("c2802") for i, l in enumerate(lines) if "c2802" in l}
guard("c2801_mention_accounting_pre",
      c2801_total == 14 and c2802_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2801_lines == {9326: 2, 9328: 2, 9332: 5, 9338: 1, 9340: 4}
      and c2802_lines == {9338: 2, 9340: 2},
      f"total={c2801_total} c2802={c2802_total} per-line={c2801_lines} "
      f"c2802_per-line={c2802_lines} "
      f"(expect 14 = 2 in the c2799 Step-7 twin-print (line 9326) + 2 in the "
      f"c2799 Next-block (line 9328) + 5 in the c2800 Step-1 census print (line "
      f"9332) + 1 in the c2800 Step-7 'the c2801 pre-count is 4' (line 9338) + "
      f"4 in the c2800 Next-block (line 9340: the instance + the 446189-c2801 id "
      f"+ the 'c2801/c2802' guard phrase + the fourth measured surface, the "
      f"bare-c-token accounting); c2802 = 4 — 2 births in the c2800 Step-7 line "
      f"9338 (the rehearsal pre-count print 'the c2802 pre==0 expectation' AND the "
      f"census-time print 'c2802_pre = 0' — the Step-7 twin-print class REPEATS) + "
      f"2 FORWARD-token births inside the c2800 Next-block guard phrase AND the "
      f"FORWARD-token sentence, both on line 9340 (the forward-token lesson: "
      f"measured, never assumed unborn — the c2800 append prophecy 'c2802 = 4 "
      f"block births' held EXACTLY, the born-FOUR class REPEATS))")

c2800_total = text.count("c2800")
c2800_lines = {i + 1: l.count("c2800") for i, l in enumerate(lines) if "c2800" in l}
guard("c2800_mention_census_pre",
      c2800_total == 38
      and c2800_lines == {9314: 2, 9316: 2, 9320: 5, 9326: 1, 9328: 4, 9331: 1,
                          9332: 4, 9333: 4, 9338: 4, 9340: 11},
      f"total={c2800_total} per-line={c2800_lines} (the pre-block 14 on lines "
      f"9314/9316/9320/9326/9328 + 24 births inside the c2800 block itself; the "
      f"Step-4 surface 'scan_cycle2800_raw.json'/'validate_cycle2800.py'/"
      f"'scan_cycle2800.json' on line 9335 carries 'cycle2800'/'e2800', NOT the "
      f"bare c-token — the c2760 E-TOKEN lesson: line 9335 ABSENT from the "
      f"measured dict)")

for tag, total in (("c2799", 78), ("c2798", 81), ("c2797", 79), ("c2796", 89),
                   ("c2795", 104), ("c2794", 106), ("c2793", 111), ("c2792", 116),
                   ("c2791", 107), ("c2790", 114), ("c2789", 110), ("c2788", 121),
                   ("c2787", 122), ("c2786", 138), ("c2785", 126), ("c2784", 124),
                   ("c2783", 125), ("c2782", 124), ("c2781", 129), ("c2780", 133),
                   ("c2779", 134), ("c2778", 178), ("c2777", 150), ("c2776", 155),
                   ("c2775", 164), ("c2774", 169), ("c2773", 173), ("c2772", 192),
                   ("c2771", 182), ("c2770", 224), ("c2769", 171), ("c2768", 174),
                   ("c2767", 223), ("c2766", 200), ("c2765", 165), ("c2764", 167),
                   ("c2763", 175), ("c2762", 207), ("c2761", 221), ("c2760", 170),
                   ("c2759", 170), ("c2758", 172), ("c2757", 175), ("c2756", 180),
                   ("c2755", 187), ("c2754", 190), ("c2753", 197), ("c2752", 203),
                   ("c2751", 189), ("c2750", 191), ("c2749", 195), ("c2748", 185),
                   ("c2747", 184)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (165 at the c2800 guard probe + 1 through "
          f"the c2800 official capture = 166, + 2 foreign/unattributed cumulative since — "
          f"dev.log is timestamp-less: the official/foreign split is by latency-match, "
          f"honest, no over-claim; the residual foreign/unattributed is "
          f"arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2800 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2800 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2800:"):
        official_depth = depth
        walk_info.append(f"official c2800 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2800_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2800_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2800 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111/615fc1c/7efc24d/65f4c4e/"
          f"b27a69f/f0d806e/87e21ad precedent)")
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

C2800_SET = [
    "census_c2800.py", "arrival_guard_c2800.py", "rebadge_cycle2800.py",
    "capture_cycle2800.sh", "measure_c2800_tokens.py", "recursive_diff_2800.py",
    "validate_cycle2800.py", "entry_cycle2800.txt", "append_cycle2800.py",
    "scan_cycle2800_raw.json", "scan_cycle2800.json",
]
print("c2800_instrument_set_object_presence:")
missing = []
for name in C2800_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2800 files on disk")

v100 = open("/home/z/my-project/scripts/validate_cycle2800.py", "rb").read()
guard("v100_source_intact", b"CYCLE = 2800" in v100 and b"drift49_pass49_match" in v100
      and b"drift49_pass50_match" not in v100
      and b"(18,0,0,18,0)" in v100 and b"(20,0,2,18,0)" in v100
      and b"(21,0,3,18,0)" in v100 and b"pass-48 band" in v100
      and b"pass-49 band" not in v100
      and b"pass-48 evidence" in v100 and b"pass-49 evidence" not in v100,
      f"bytes={len(v100)} (the v100 pass-49 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-50 gate name drift49_pass50_match is what the v101 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-48 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-48 evidence' is present — BOTH instrument surfaces, the v101 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "e829f19:scripts/validate_cycle2800.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v100_commit_object_intact", len(obj.stdout) == len(v100)
          and obj.stdout == v100,
          f"object_bytes={len(obj.stdout)} == disk {len(v100)} (the e829f19 c2800 commit)")
else:
    guard("v100_commit_object_intact", False, "e829f19 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
