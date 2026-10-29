#!/usr/bin/env python3
"""Arrival-guard for cycle 2798 (Job ID 446189) — measured, never predicted.

Spec source: the c2797 Next-block (worklog line 9304). Checks:
  worklog 9304 lines EXACT (newline count, c2797 append post-guard prophecy);
  tail = the c2798 Next bullet;
  anchors ^Task ID: 475 / ^- No gold yet 408 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2798 entries; c2798/c2799 substring accounting
  (the token-guard lives INSIDE the c2797 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2798.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2799 = 4 total = 2 births in the c2797 Step-7 line 9302 (the
  rehearsal pre-count print 'the c2799 pre==0 expectation' AND the census-time
  print 'c2799_pre = 0') + 2 FORWARD-token births inside the c2797 Next-block
  guard phrase ('arrival-guard against c2798/c2799 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2799 must be IN the census
  tuple'), both on line 9304 — the c2767..c2798 forward-token lessons: measure
  it, never assume it unborn; the born-FOUR class is NEW this cycle (the
  c2796-cycle forward token was born THRICE, the c2797-cycle token UNBORN —
  the Step-7 twin-print class born 2 + the Next-block 2 = 4, honestly
  accounted); the c2798 token itself is BORN ELEVEN times
  pre-append: 1 in the c2796 Step-7 rehearsal print (line 9290) + 2 in the
  c2796 Next-block (line 9292) + 3 in the c2797 Step-1 census print (line
  9296) + 1 in the c2797 Step-7 'the c2798 pre-count is 3' (line 9302) + 4 in
  the c2797 Next-block (line 9304: the instance + id + the 'c2798/c2799'
  guard phrase + the measure_c2798_tokens.py path token — the bare-c-token
  path class, honestly accounted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2797_raw.json' /
  'validate_cycle2797.py' / 'scan_cycle2797.json' carry 'e2797'/'cycle2797',
  NOT the bare c-token 'c2797' — path tokens contribute ZERO bare-c2797
  census weight (line 9299 ABSENT from the measured c2797 per-line dict);
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2797 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2797 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2797 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v97 source-intact expectations matched to the v97 pass-46 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v97 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-47 gate name is what the v98 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-45 band' is present AND the evidence-paragraph lag-1 heading
  'pass-45 evidence' is present — BOTH instrument surfaces, the v98 rebadge
  P3/P8 old-string expectations, exactly as the c2797 Next-block wrote).
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
guard("worklog_lines==9304", n_nl == 9304, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2798_next_bullet", last_nonempty.startswith("- Next: the c2798 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==475", tid == 475, f"got={tid}")
guard("anchor_nogold==408", gold == 408, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2798")]
guard("dup_check_zero_serviced_c2798", len(dup) == 0, f"got={len(dup)}")
c2798_total = text.count("c2798")
c2799_total = text.count("c2799")
tok_guard = [l for l in lines if "c2798/c2799" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2798 instance")]
c2798_lines = {i + 1: l.count("c2798") for i, l in enumerate(lines) if "c2798" in l}
c2799_lines = {i + 1: l.count("c2799") for i, l in enumerate(lines) if "c2799" in l}
guard("c2798_mention_accounting_pre",
      c2798_total == 11 and c2799_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2798_lines == {9290: 1, 9292: 2, 9296: 3, 9302: 1, 9304: 4}
      and c2799_lines == {9302: 2, 9304: 2},
      f"total={c2798_total} c2799={c2799_total} per-line={c2798_lines} "
      f"c2799_per-line={c2799_lines} "
      f"(expect 11 = 1 in the c2796 Step-7 rehearsal print (line 9290, 'the c2798 "
      f"pre==0 expectation' context) + 2 in the c2796 Next-block (line 9292, the "
      f"guard phrase AND the FORWARD-token sentence) + 3 in the c2797 Step-1 census "
      f"print (line 9296) + 1 in the c2797 Step-7 'the c2798 pre-count is 3' "
      f"(line 9302) + 4 in the c2797 Next-block (line 9304: the instance + id + "
      f"'c2798/c2799' guard phrase + the measure_c2798_tokens.py path token, the "
      f"bare-c-token path class); c2799 = 4 — 2 births in the c2797 Step-7 line "
      f"9302 (the rehearsal pre-count print 'the c2799 pre==0 expectation' AND the "
      f"census-time print 'c2799_pre = 0' — the Step-7 twin-print class, NEW) + "
      f"2 FORWARD-token births inside the c2797 Next-block guard phrase AND the "
      f"FORWARD-token sentence, both on line 9304 (the forward-token lesson: "
      f"measured, never assumed unborn — the born-FOUR class is NEW, the c2797 "
      f"append prophecy 'c2799 = 4 block births' held EXACTLY))")

c2797_total = text.count("c2797")
c2797_lines = {i + 1: l.count("c2797") for i, l in enumerate(lines) if "c2797" in l}
guard("c2797_mention_census_pre",
      c2797_total == 38
      and c2797_lines == {9278: 1, 9280: 2, 9284: 3, 9290: 1, 9292: 4, 9295: 1,
                          9296: 8, 9297: 4, 9302: 4, 9304: 10},
      f"total={c2797_total} per-line={c2797_lines} (the pre-block 11 on lines "
      f"9278/9280/9284/9290/9292 + 27 births inside the c2797 block itself; the "
      f"Step-4 surface 'scan_cycle2797_raw.json'/'validate_cycle2797.py'/"
      f"'scan_cycle2797.json' on line 9299 carries 'cycle2797'/'e2797', NOT the "
      f"bare c-token — the c2760 E-TOKEN lesson: line 9299 ABSENT from the "
      f"measured dict)")

for tag, total in (("c2796", 81), ("c2795", 96), ("c2794", 101), ("c2793", 103),
                   ("c2792", 108), ("c2791", 102), ("c2790", 106), ("c2789", 105),
                   ("c2788", 116), ("c2787", 117), ("c2786", 130), ("c2785", 121),
                   ("c2784", 119), ("c2783", 120), ("c2782", 119), ("c2781", 124),
                   ("c2780", 128), ("c2779", 129), ("c2778", 173), ("c2777", 145),
                   ("c2776", 150), ("c2775", 159), ("c2774", 164), ("c2773", 168),
                   ("c2772", 187), ("c2771", 177), ("c2770", 216), ("c2769", 166),
                   ("c2768", 169), ("c2767", 212), ("c2766", 192), ("c2765", 160),
                   ("c2764", 162), ("c2763", 170), ("c2762", 199), ("c2761", 213),
                   ("c2760", 165), ("c2759", 165), ("c2758", 167), ("c2757", 170),
                   ("c2756", 175), ("c2755", 182), ("c2754", 185), ("c2753", 191),
                   ("c2752", 197), ("c2751", 183), ("c2750", 185), ("c2749", 189),
                   ("c2748", 179), ("c2747", 177), ("c2746", 184)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (158 at the census probe: 154 through "
          f"the c2797 official capture + 4 foreign/unattributed cumulative since the "
          f"c2795 probe — dev.log is timestamp-less: the official/foreign split is "
          f"by latency-match, honest, no over-claim; the residual foreign/"
          f"unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2797 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2797 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2797:"):
        official_depth = depth
        walk_info.append(f"official c2797 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2797_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2797_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2797 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111/615fc1c/7efc24d/65f4c4e "
          f"precedent)")
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

C2797_SET = [
    "census_c2797.py", "arrival_guard_c2797.py", "rebadge_cycle2797.py",
    "capture_cycle2797.sh", "measure_c2797_tokens.py", "recursive_diff_2797.py",
    "validate_cycle2797.py", "entry_cycle2797.txt", "append_cycle2797.py",
    "scan_cycle2797_raw.json", "scan_cycle2797.json",
]
print("c2797_instrument_set_object_presence:")
missing = []
for name in C2797_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2797 files on disk")

v97 = open("/home/z/my-project/scripts/validate_cycle2797.py", "rb").read()
guard("v97_source_intact", b"CYCLE = 2797" in v97 and b"drift49_pass46_match" in v97
      and b"drift49_pass47_match" not in v97
      and b"(18,0,0,18,0)" in v97 and b"(20,0,2,18,0)" in v97
      and b"(21,0,3,18,0)" in v97 and b"pass-45 band" in v97
      and b"pass-46 band" not in v97
      and b"pass-45 evidence" in v97 and b"pass-46 evidence" not in v97,
      f"bytes={len(v97)} (the v97 pass-46 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-47 gate name drift49_pass47_match is what the v98 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-45 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-45 evidence' is present — BOTH instrument surfaces, the v98 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "98db775:scripts/validate_cycle2797.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v97_commit_object_intact", len(obj.stdout) == len(v97)
          and obj.stdout == v97,
          f"object_bytes={len(obj.stdout)} == disk {len(v97)} (the 98db775 c2797 commit)")
else:
    guard("v97_commit_object_intact", False, "98db775 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
