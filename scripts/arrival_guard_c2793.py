#!/usr/bin/env python3
"""Arrival-guard for cycle 2793 (Job ID 446189) — measured, never predicted.

Spec source: the c2792 Next-block (worklog line 9244). Checks:
  worklog 9244 lines EXACT (newline count, c2792 append post-guard prophecy);
  tail = the c2793 Next bullet;
  anchors ^Task ID: 470 / ^- No gold yet 403 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2793 entries; c2793/c2794 substring accounting
  (the c2793/c2794 token-guard lives INSIDE the c2792 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2793.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2794 = 3 total = 1 birth in the c2792 Step-7 line 9242 (the
  rehearsal pre-count print 'the c2794 pre==0 expectation') + 2 FORWARD-token
  births inside the c2792 Next-block guard phrase ('arrival-guard against
  c2793/c2794 tokens') AND the FORWARD-token sentence ('the FORWARD token
  c2794 must be IN the census tuple'), both on line 9244 — the
  c2767..c2793 forward-token lessons: measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2792_raw.json' /
  'validate_cycle2792.py' / 'scan_cycle2792.json' carry 'e2792'/'cycle2792',
  NOT the bare c-token 'c2792' — path tokens contribute ZERO bare-c2792
  census weight (line 9239 ABSENT from the measured c2792 per-line dict);
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2792 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2792 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2792 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v92 source-intact expectations matched to the v92 pass-41 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v92 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-42 gate name is what the v93 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-40 band' is present AND the evidence-paragraph lag-1 heading
  'pass-40 evidence' is present — BOTH instrument surfaces, the v93 rebadge
  P3/P8 old-string expectations, exactly as the c2792 Next-block wrote).
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
guard("worklog_lines==9244", n_nl == 9244, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2793_next_bullet", last_nonempty.startswith("- Next: the c2793 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==470", tid == 470, f"got={tid}")
guard("anchor_nogold==403", gold == 403, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2793")]
guard("dup_check_zero_serviced_c2793", len(dup) == 0, f"got={len(dup)}")
c2793_total = text.count("c2793")
c2794_total = text.count("c2794")
tok_guard = [l for l in lines if "c2793/c2794" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2793 instance")]
c2793_lines = {i + 1: l.count("c2793") for i, l in enumerate(lines) if "c2793" in l}
c2794_lines = {i + 1: l.count("c2794") for i, l in enumerate(lines) if "c2794" in l}
guard("c2793_mention_accounting_pre",
      c2793_total == 8 and c2794_total == 3 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2793_lines == {9232: 2, 9236: 1, 9242: 1, 9244: 4}
      and c2794_lines == {9242: 1, 9244: 2},
      f"total={c2793_total} c2794={c2794_total} per-line={c2793_lines} "
      f"c2794_per-line={c2794_lines} "
      f"(expect 8 = 2 FORWARD-token births inside the c2791 Next-block (line 9232, "
      f"the guard phrase 'c2792/c2793' AND the FORWARD-token sentence) + 1 in the "
      f"c2792 Step-1 line 9236 (the forward-token census print '+ c2793 = 2') + 1 in "
      f"the c2792 Step-7 line 9242 + 4 in the c2792 Next-block line 9244 — which is "
      f"itself the c2793/c2794 token-guard: the instance + id + 'c2793/c2794' phrase "
      f"+ FORWARD-token sentence; c2794 = 3 — 1 birth in the c2792 Step-7 rehearsal "
      f"pre-count print (line 9242, 'the c2794 pre==0 expectation') + 2 FORWARD-token "
      f"births inside the c2792 Next-block guard phrase AND the FORWARD-token "
      f"sentence, both on line 9244 (the forward-token lesson: measured, never "
      f"assumed unborn))")

c2792_total = text.count("c2792")
c2792_lines = {i + 1: l.count("c2792") for i, l in enumerate(lines) if "c2792" in l}
guard("c2792_mention_census_pre",
      c2792_total == 35
      and c2792_lines == {9220: 2, 9224: 1, 9230: 1, 9232: 4, 9235: 1, 9236: 3,
                          9237: 8, 9242: 4, 9244: 11},
      f"total={c2792_total} per-line={c2792_lines} (the c2792 block carries "
      f"'scan_cycle2792_raw.json'/'validate_cycle2792.py'/'scan_cycle2792.json' "
      f"path-token surfaces on line 9238 — those carry 'cycle2792'/'e2792', NOT "
      f"the bare c-token, the c2760 E-TOKEN lesson: line 9238 ABSENT from the "
      f"measured dict)")

for tag, total in (("c2791", 78), ("c2790", 81), ("c2789", 87), ("c2788", 97),
                   ("c2787", 99), ("c2786", 107), ("c2785", 103), ("c2784", 101),
                   ("c2783", 102), ("c2782", 101), ("c2781", 106), ("c2780", 110),
                   ("c2779", 111), ("c2778", 149), ("c2777", 127), ("c2776", 132),
                   ("c2775", 141), ("c2774", 146), ("c2773", 150), ("c2772", 169),
                   ("c2771", 159), ("c2770", 193), ("c2769", 149), ("c2768", 152),
                   ("c2767", 185), ("c2766", 170), ("c2765", 143), ("c2764", 145),
                   ("c2763", 153), ("c2762", 177), ("c2761", 191), ("c2760", 148),
                   ("c2759", 148), ("c2758", 150), ("c2757", 153), ("c2756", 158),
                   ("c2755", 165), ("c2754", 168), ("c2753", 174), ("c2752", 180),
                   ("c2751", 166), ("c2750", 168), ("c2749", 172), ("c2748", 162),
                   ("c2747", 160), ("c2746", 162)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (144 at the census probe: 139 at the "
          f"c2791 census + the official c2791 capture + the loop echo #512 of the "
          f"c2791 servicing + 1 foreign/unattributed + the official c2792 capture + "
          f"the loop echo #513 of the c2792 servicing — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +1 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2792 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2792 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2792:"):
        official_depth = depth
        walk_info.append(f"official c2792 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2792_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2792_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2792 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218 precedent)")
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

C2792_SET = [
    "census_c2792.py", "arrival_guard_c2792.py", "rebadge_cycle2792.py",
    "capture_cycle2792.sh", "measure_c2792_tokens.py", "recursive_diff_2792.py",
    "validate_cycle2792.py", "entry_cycle2792.txt", "append_cycle2792.py",
    "scan_cycle2792_raw.json", "scan_cycle2792.json",
]
print("c2792_instrument_set_object_presence:")
missing = []
for name in C2792_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2792 files on disk")

v92 = open("/home/z/my-project/scripts/validate_cycle2792.py", "rb").read()
guard("v92_source_intact", b"CYCLE = 2792" in v92 and b"drift49_pass41_match" in v92
      and b"drift49_pass42_match" not in v92
      and b"(18,0,0,18,0)" in v92 and b"(20,0,2,18,0)" in v92
      and b"(21,0,3,18,0)" in v92 and b"pass-40 band" in v92
      and b"pass-41 band" not in v92
      and b"pass-40 evidence" in v92 and b"pass-41 evidence" not in v92,
      f"bytes={len(v92)} (the v92 pass-41 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-42 gate name drift49_pass42_match is what the v93 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-40 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-40 evidence' is present — BOTH instrument surfaces, the v93 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "99f6ee6:scripts/validate_cycle2792.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v92_commit_object_intact", len(obj.stdout) == len(v92)
          and obj.stdout == v92,
          f"object_bytes={len(obj.stdout)} == disk {len(v92)} (the 99f6ee6 c2792 commit)")
else:
    guard("v92_commit_object_intact", False, "99f6ee6 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
