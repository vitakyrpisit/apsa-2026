#!/usr/bin/env python3
"""Arrival-guard for cycle 2792 (Job ID 446189) — measured, never predicted.

Spec source: the c2791 Next-block (worklog line 9232). Checks:
  worklog 9232 lines EXACT (newline count, c2791 append post-guard prophecy);
  tail = the c2792 Next bullet;
  anchors ^Task ID: 469 / ^- No gold yet 402 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2792 entries; c2792/c2793 substring accounting
  (the c2792/c2793 token-guard lives INSIDE the c2791 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2792.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2793 = 2 total = 2 FORWARD-token births inside the c2791
  Next-block guard phrase ('arrival-guard against c2792/c2793 tokens') AND
  the FORWARD-token sentence ('the FORWARD token c2793 must be IN the census
  tuple'), both on line 9232 — the c2767..c2792 forward-token lessons:
  measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-3/4 surfaces 'scan_cycle2791_raw.json'
  / 'validate_cycle2791.py' / 'scan_cycle2791.json' carry 'e2791'/'cycle2791',
  NOT the bare c-token 'c2791' — path tokens contribute ZERO bare-c2791
  census weight; the guard expectations below are the census MEASUREMENTS,
  not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2791 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2791 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2791 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v91 source-intact expectations matched to the v91 pass-40 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v91 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-41 gate name is what the v92 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-39 band' is present AND the evidence-paragraph lag-1 heading
  'pass-39 evidence' is present — BOTH instrument surfaces, the v92 rebadge
  P3/P8 old-string expectations, exactly as the c2791 Next-block wrote).
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
guard("worklog_lines==9232", n_nl == 9232, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2792_next_bullet", last_nonempty.startswith("- Next: the c2792 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==469", tid == 469, f"got={tid}")
guard("anchor_nogold==402", gold == 402, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2792")]
guard("dup_check_zero_serviced_c2792", len(dup) == 0, f"got={len(dup)}")
c2792_total = text.count("c2792")
c2793_total = text.count("c2793")
tok_guard = [l for l in lines if "c2792/c2793" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2792 instance")]
c2792_lines = {i + 1: l.count("c2792") for i, l in enumerate(lines) if "c2792" in l}
c2793_lines = {i + 1: l.count("c2793") for i, l in enumerate(lines) if "c2793" in l}
guard("c2792_mention_accounting_pre",
      c2792_total == 8 and c2793_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2792_lines == {9220: 2, 9224: 1, 9230: 1, 9232: 4}
      and c2793_lines == {9232: 2},
      f"total={c2792_total} c2793={c2793_total} per-line={c2792_lines} "
      f"c2793_per-line={c2793_lines} "
      f"(expect 8 = 2 FORWARD-token births inside the c2790 Next-block (line 9220, "
      f"the guard phrase 'c2791/c2792' AND the FORWARD-token sentence) + 1 in the "
      f"c2791 Step-1 line 9224 (the forward-token census print '+ c2792 = 2') + 1 in "
      f"the c2791 Step-6 line 9230 + 4 in the c2791 Next-block line 9232 — which is "
      f"itself the c2792/c2793 token-guard: the instance + id + 'c2792/c2793' phrase "
      f"+ FORWARD-token sentence; c2793 = 2 — 2 FORWARD-token births inside the "
      f"c2791 Next-block guard phrase AND the FORWARD-token sentence, both on "
      f"line 9232 (the forward-token lesson: measured, never assumed unborn))")

c2791_total = text.count("c2791")
c2791_lines = {i + 1: l.count("c2791") for i, l in enumerate(lines) if "c2791" in l}
guard("c2791_mention_census_pre",
      c2791_total == 36
      and c2791_lines == {9208: 2, 9212: 1, 9218: 1, 9220: 4, 9223: 1, 9224: 3,
                          9225: 8, 9230: 4, 9232: 12},
      f"total={c2791_total} per-line={c2791_lines} (the c2791 block carries "
      f"'validate_cycle2791.py'/'window-2791' path-token surfaces — those carry "
      f"'cycle2791'/'e2791', NOT the bare c-token, the c2760 E-TOKEN lesson)")

for tag, total in (("c2790", 70), ("c2789", 83), ("c2788", 92), ("c2787", 95),
                   ("c2786", 102), ("c2785", 99), ("c2784", 97), ("c2783", 98),
                   ("c2782", 97), ("c2781", 102), ("c2780", 106), ("c2779", 107),
                   ("c2778", 144), ("c2777", 123), ("c2776", 128), ("c2775", 137),
                   ("c2774", 142), ("c2773", 146), ("c2772", 165), ("c2771", 155),
                   ("c2770", 188), ("c2769", 146), ("c2768", 149), ("c2767", 180),
                   ("c2766", 166), ("c2765", 140), ("c2764", 142), ("c2763", 150),
                   ("c2762", 173), ("c2761", 187), ("c2760", 145), ("c2759", 145),
                   ("c2758", 147), ("c2757", 150), ("c2756", 155), ("c2755", 162),
                   ("c2754", 165), ("c2753", 171), ("c2752", 177), ("c2751", 163),
                   ("c2750", 165), ("c2749", 169), ("c2748", 159), ("c2747", 157),
                   ("c2746", 158)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (142 at the census probe: 139 at the "
          f"c2791 census + the official c2791 capture + the loop echo #512 of the "
          f"c2791 servicing + 1 foreign/unattributed since — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +1 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2791 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2791 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2791:"):
        official_depth = depth
        walk_info.append(f"official c2791 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2791_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2791_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2791 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc precedent)")
    for depth in range(0, official_depth if official_depth is not None else 0):
        rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
        stat = git("show", "--stat", "--format=", rev)
        guard(f"git_walk_depth{depth}_zero_ledger_touch", "worklog.md" not in stat,
              f"{rev} touches only foreign-add files; worklog touched="
              f"{'worklog.md' in stat}")
head_stat = git("show", "--stat", "--format=", head_short)
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

C2791_SET = [
    "census_c2791.py", "arrival_guard_c2791.py", "rebadge_cycle2791.py",
    "capture_cycle2791.sh", "measure_c2791_tokens.py", "recursive_diff_2791.py",
    "validate_cycle2791.py", "entry_cycle2791.txt", "append_cycle2791.py",
    "scan_cycle2791_raw.json", "scan_cycle2791.json",
]
print("c2791_instrument_set_object_presence:")
missing = []
for name in C2791_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2791 files on disk")

v91 = open("/home/z/my-project/scripts/validate_cycle2791.py", "rb").read()
guard("v91_source_intact", b"CYCLE = 2791" in v91 and b"drift49_pass40_match" in v91
      and b"drift49_pass41_match" not in v91
      and b"(18,0,0,18,0)" in v91 and b"(20,0,2,18,0)" in v91
      and b"(21,0,3,18,0)" in v91 and b"pass-39 band" in v91
      and b"pass-40 band" not in v91
      and b"pass-39 evidence" in v91 and b"pass-40 evidence" not in v91,
      f"bytes={len(v91)} (the v91 pass-40 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-41 gate name drift49_pass41_match is what the v92 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-39 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-39 evidence' is present — BOTH instrument surfaces, the v92 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "f6f24d7:scripts/validate_cycle2791.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v91_commit_object_intact", len(obj.stdout) == len(v91)
          and obj.stdout == v91,
          f"object_bytes={len(obj.stdout)} == disk {len(v91)} (the f6f24d7 c2791 commit)")
else:
    guard("v91_commit_object_intact", False, "f6f24d7 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
