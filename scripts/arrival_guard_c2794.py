#!/usr/bin/env python3
"""Arrival-guard for cycle 2794 (Job ID 446189) — measured, never predicted.

Spec source: the c2793 Next-block (worklog line 9256). Checks:
  worklog 9256 lines EXACT (newline count, c2793 append post-guard prophecy);
  tail = the c2794 Next bullet;
  anchors ^Task ID: 471 / ^- No gold yet 404 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2794 entries; c2794/c2795 substring accounting
  (the token-guard lives INSIDE the c2793 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2794.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2795 = 3 total = 1 birth in the c2793 Step-7 line 9254 (the
  rehearsal pre-count print 'the c2795 pre==0 expectation') + 2 FORWARD-token
  births inside the c2793 Next-block guard phrase ('arrival-guard against
  c2794/c2795 tokens') AND the FORWARD-token sentence ('the FORWARD token
  c2795 must be IN the census tuple'), both on line 9256 — the
  c2767..c2794 forward-token lessons: measure it, never assume it unborn;
  the c2794 token itself is BORN NINE times pre-append: 1 in the c2792
  Step-7 rehearsal print (line 9242) + 2 in the c2792 Next-block (line 9244)
  + 1 in the c2793 Step-1 census print '+ c2794 = 3' (line 9248) + 1 in the
  c2793 Step-7 'the c2794 pre-count is 3' (line 9254) + 4 in the c2793
  Next-block (line 9256: the instance + id + guard phrase 'c2794/c2795' +
  the measure_c2794_tokens.py path token — the bare-c-token path class,
  honestly accounted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2793_raw.json' /
  'validate_cycle2793.py' / 'scan_cycle2793.json' carry 'e2793'/'cycle2793',
  NOT the bare c-token 'c2793' — path tokens contribute ZERO bare-c2793
  census weight (line 9250/9251 ABSENT from the measured c2793 per-line dict);
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2793 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2793 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2793 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v93 source-intact expectations matched to the v93 pass-42 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v93 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-43 gate name is what the v94 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-41 band' is present AND the evidence-paragraph lag-1 heading
  'pass-41 evidence' is present — BOTH instrument surfaces, the v94 rebadge
  P3/P8 old-string expectations, exactly as the c2793 Next-block wrote).
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
guard("worklog_lines==9256", n_nl == 9256, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2794_next_bullet", last_nonempty.startswith("- Next: the c2794 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==471", tid == 471, f"got={tid}")
guard("anchor_nogold==404", gold == 404, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2794")]
guard("dup_check_zero_serviced_c2794", len(dup) == 0, f"got={len(dup)}")
c2794_total = text.count("c2794")
c2795_total = text.count("c2795")
tok_guard = [l for l in lines if "c2794/c2795" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2794 instance")]
c2794_lines = {i + 1: l.count("c2794") for i, l in enumerate(lines) if "c2794" in l}
c2795_lines = {i + 1: l.count("c2795") for i, l in enumerate(lines) if "c2795" in l}
guard("c2794_mention_accounting_pre",
      c2794_total == 9 and c2795_total == 3 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2794_lines == {9242: 1, 9244: 2, 9248: 1, 9254: 1, 9256: 4}
      and c2795_lines == {9254: 1, 9256: 2},
      f"total={c2794_total} c2795={c2795_total} per-line={c2794_lines} "
      f"c2795_per-line={c2795_lines} "
      f"(expect 9 = 1 in the c2792 Step-7 rehearsal print (line 9242, 'the c2794 "
      f"pre==0 expectation') + 2 in the c2792 Next-block (line 9244, the guard "
      f"phrase AND the FORWARD-token sentence) + 1 in the c2793 Step-1 census "
      f"print '+ c2794 = 3' (line 9248) + 1 in the c2793 Step-7 'the c2794 "
      f"pre-count is 3' (line 9254) + 4 in the c2793 Next-block (line 9256: "
      f"the instance + id + 'c2794/c2795' guard phrase + the "
      f"measure_c2794_tokens.py path token, the bare-c-token path class); "
      f"c2795 = 3 — 1 birth in the c2793 Step-7 rehearsal pre-count print "
      f"(line 9254, 'the c2795 pre==0 expectation') + 2 FORWARD-token births "
      f"inside the c2793 Next-block guard phrase AND the FORWARD-token "
      f"sentence, both on line 9256 (the forward-token lesson: measured, never "
      f"assumed unborn — the born-thrice class REPEATS))")

c2793_total = text.count("c2793")
c2793_lines = {i + 1: l.count("c2793") for i, l in enumerate(lines) if "c2793" in l}
guard("c2793_mention_census_pre",
      c2793_total == 36
      and c2793_lines == {9232: 2, 9236: 1, 9242: 1, 9244: 4, 9247: 1, 9248: 4,
                          9249: 8, 9254: 5, 9256: 10},
      f"total={c2793_total} per-line={c2793_lines} (the pre-block 8 on lines "
      f"9232/9236/9242/9244 + 28 births inside the c2793 block itself: 1 title "
      f"(9247) + 4 Step-1 (9248) + 8 Step-2 (9249) + 5 Step-7 (9254) + 10 "
      f"Next-block (9256); the Step-4 surfaces 'scan_cycle2793_raw.json'/"
      f"'validate_cycle2793.py'/'scan_cycle2793.json' on lines 9250/9251 carry "
      f"'cycle2793'/'e2793', NOT the bare c-token — the c2760 E-TOKEN lesson: "
      f"lines 9250/9251 ABSENT from the measured dict)")

for tag, total in (("c2792", 81), ("c2791", 87), ("c2790", 87), ("c2789", 91),
                   ("c2788", 102), ("c2787", 103), ("c2786", 112), ("c2785", 107),
                   ("c2784", 105), ("c2783", 106), ("c2782", 105), ("c2781", 110),
                   ("c2780", 114), ("c2779", 115), ("c2778", 154), ("c2777", 131),
                   ("c2776", 136), ("c2775", 145), ("c2774", 150), ("c2773", 154),
                   ("c2772", 173), ("c2771", 163), ("c2770", 198), ("c2769", 152),
                   ("c2768", 155), ("c2767", 190), ("c2766", 174), ("c2765", 146),
                   ("c2764", 148), ("c2763", 156), ("c2762", 181), ("c2761", 195),
                   ("c2760", 151), ("c2759", 151), ("c2758", 153), ("c2757", 156),
                   ("c2756", 161), ("c2755", 168), ("c2754", 171), ("c2753", 177),
                   ("c2752", 183), ("c2751", 169), ("c2750", 171), ("c2749", 175),
                   ("c2748", 165), ("c2747", 163), ("c2746", 166)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (147 at the census probe: 146 at the "
          f"c2793 post-capture note + 1 foreign/unattributed since — dev.log is "
          f"timestamp-less: the official/foreign split is by latency-match, honest, "
          f"no over-claim; the residual foreign/unattributed is arithmetic-necessity "
          f"class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2793 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2793 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2793:"):
        official_depth = depth
        walk_info.append(f"official c2793 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2793_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2793_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2793 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73 precedent)")
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

C2793_SET = [
    "census_c2793.py", "arrival_guard_c2793.py", "rebadge_cycle2793.py",
    "capture_cycle2793.sh", "measure_c2793_tokens.py", "recursive_diff_2793.py",
    "validate_cycle2793.py", "entry_cycle2793.txt", "append_cycle2793.py",
    "scan_cycle2793_raw.json", "scan_cycle2793.json",
]
print("c2793_instrument_set_object_presence:")
missing = []
for name in C2793_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2793 files on disk")

v93 = open("/home/z/my-project/scripts/validate_cycle2793.py", "rb").read()
guard("v93_source_intact", b"CYCLE = 2793" in v93 and b"drift49_pass42_match" in v93
      and b"drift49_pass43_match" not in v93
      and b"(18,0,0,18,0)" in v93 and b"(20,0,2,18,0)" in v93
      and b"(21,0,3,18,0)" in v93 and b"pass-41 band" in v93
      and b"pass-42 band" not in v93
      and b"pass-41 evidence" in v93 and b"pass-42 evidence" not in v93,
      f"bytes={len(v93)} (the v93 pass-42 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-43 gate name drift49_pass43_match is what the v94 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-41 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-41 evidence' is present — BOTH instrument surfaces, the v94 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "a27965c:scripts/validate_cycle2793.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v93_commit_object_intact", len(obj.stdout) == len(v93)
          and obj.stdout == v93,
          f"object_bytes={len(obj.stdout)} == disk {len(v93)} (the a27965c c2793 commit)")
else:
    guard("v93_commit_object_intact", False, "a27965c object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
