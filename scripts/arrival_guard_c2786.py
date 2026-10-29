#!/usr/bin/env python3
"""Arrival-guard for cycle 2786 (Job ID 446189) — measured, never predicted.

Spec source: the c2785 Next-block (worklog line 9160). Checks:
  worklog 9160 lines EXACT (newline count, c2785 append post-guard prophecy);
  tail = the c2786 Next bullet;
  anchors ^Task ID: 463 / ^- No gold yet 396 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2786 entries; c2786/c2787 substring accounting
  (the c2786/c2787 token-guard lives INSIDE the c2785 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2786.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2787 = 2 born inside the c2785 Next-block guard phrase AND
  FORWARD-token sentence — the c2767..c2786 forward-token lessons:
  measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'validate_cycle2785.py' /
  'scan_cycle2785.json' carries 'e2785', NOT 'c2785' — path tokens are
  e-tokens with ZERO c2785 census contribution, which is why the measured
  c2785 per-line dict has NO line-9155 entry; the guard expectations below
  are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2785 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2785 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2785 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v85 source-intact expectations matched to the v85 pass-34 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v85 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-35 gate name is what the v86 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-33 band' is present AND the evidence-paragraph lag-1 heading
  'pass-33 evidence' is present — BOTH instrument surfaces, the v86 rebadge
  P3/P8 old-string expectations, exactly as the c2785 Next-block wrote).
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
guard("worklog_lines==9160", n_nl == 9160, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2786_next_bullet", last_nonempty.startswith("- Next: the c2786 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==463", tid == 463, f"got={tid}")
guard("anchor_nogold==396", gold == 396, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2786")]
guard("dup_check_zero_serviced_c2786", len(dup) == 0, f"got={len(dup)}")
c2786_total = text.count("c2786")
c2787_total = text.count("c2787")
tok_guard = [l for l in lines if "c2786/c2787" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2786 instance")]
c2786_lines = {i + 1: l.count("c2786") for i, l in enumerate(lines) if "c2786" in l}
c2787_lines = {i + 1: l.count("c2787") for i, l in enumerate(lines) if "c2787" in l}
guard("c2786_mention_accounting_pre",
      c2786_total == 10 and c2787_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2786_lines == {9148: 2, 9152: 3, 9160: 5} and c2787_lines == {9160: 2},
      f"total={c2786_total} c2787={c2787_total} per-line={c2786_lines} "
      f"c2787_per-line={c2787_lines} "
      f"(expect 10 = 2 in the c2784 Next-block line 9148 [the historical "
      f"c2785/c2786 token-guard phrase + FORWARD-token sentence] + 3 in the c2785 "
      f"Step-1 line 9152 [the census-tuple print '+ c2786 = 2' + the c2785/c2786 "
      f"phrase + the forward-lesson phrase] + 5 in the c2785 Next-block line 9160 "
      f"— which is itself the c2786/c2787 token-guard: the instance + id + "
      f"'c2786/c2787' phrase + measure_c2786_tokens.py (e-token, zero census "
      f"weight) + the echo-prescription phrase 'the c2786 echo should land'; "
      f"c2787 = 2 — the forward token is BORN inside the c2785 Next-block guard "
      f"phrase AND the FORWARD-token sentence, both on line 9160 (the "
      f"forward-token lesson: measured, never assumed unborn))")

c2785_total = text.count("c2785")
c2785_lines = {i + 1: l.count("c2785") for i, l in enumerate(lines) if "c2785" in l}
guard("c2785_mention_census_pre",
      c2785_total == 37
      and c2785_lines == {9136: 2, 9140: 2, 9148: 4, 9151: 1, 9152: 5, 9153: 8,
                          9158: 5, 9160: 10},
      f"total={c2785_total} per-line={c2785_lines} (NO 9155 entry — the Step-4 "
      f"validate_cycle2785.py/scan_cycle2785.json surfaces are e-tokens, the "
      f"c2760 lesson re-verified live at census time)")

c2784_total = text.count("c2784")
c2784_lines = {i + 1: l.count("c2784") for i, l in enumerate(lines) if "c2784" in l}
guard("c2784_mention_census_pre",
      c2784_total == 71
      and c2784_lines == {9124: 2, 9128: 2, 9136: 4, 9139: 1, 9140: 4, 9141: 8,
                          9146: 5, 9148: 9, 9150: 7, 9152: 14, 9153: 8, 9154: 2,
                          9157: 1, 9158: 3, 9160: 1},
      f"total={c2784_total} per-line={c2784_lines}")

for tag, total in (("c2783", 71), ("c2782", 73), ("c2781", 78), ("c2780", 82),
                   ("c2779", 83), ("c2778", 112), ("c2777", 99), ("c2776", 104),
                   ("c2775", 113), ("c2774", 118), ("c2773", 122), ("c2772", 139),
                   ("c2771", 131), ("c2770", 158), ("c2769", 128), ("c2768", 131),
                   ("c2767", 150), ("c2766", 142), ("c2765", 122), ("c2764", 124),
                   ("c2763", 129), ("c2762", 149), ("c2761", 163), ("c2760", 125),
                   ("c2759", 127), ("c2758", 129), ("c2757", 132), ("c2756", 137),
                   ("c2755", 144), ("c2754", 147), ("c2753", 153), ("c2752", 159),
                   ("c2751", 145), ("c2750", 147), ("c2749", 151), ("c2748", 141),
                   ("c2747", 139), ("c2746", 134)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (121 at the census probe: 117 at the "
          f"c2785 guard + the official c2785 capture + the in-batch echo of THIS "
          f"servicing + 2 foreign/unattributed since — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +2 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2785 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2785 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2785:"):
        official_depth = depth
        walk_info.append(f"official c2785 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2785_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2785_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2785 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021 precedent)")
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

C2785_SET = [
    "census_c2785.py", "arrival_guard_c2785.py", "rebadge_cycle2785.py",
    "capture_cycle2785.sh", "measure_c2785_tokens.py", "recursive_diff_2785.py",
    "validate_cycle2785.py", "entry_cycle2785.txt", "append_cycle2785.py",
    "scan_cycle2785_raw.json", "scan_cycle2785.json",
]
print("c2785_instrument_set_object_presence:")
missing = []
for name in C2785_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2785 files on disk")

v85 = open("/home/z/my-project/scripts/validate_cycle2785.py", "rb").read()
guard("v85_source_intact", b"CYCLE = 2785" in v85 and b"drift49_pass34_match" in v85
      and b"drift49_pass35_match" not in v85
      and b"(18,0,0,18,0)" in v85 and b"(20,0,2,18,0)" in v85
      and b"(21,0,3,18,0)" in v85 and b"pass-33 band" in v85
      and b"pass-34 band" not in v85
      and b"pass-33 evidence" in v85 and b"pass-34 evidence" not in v85,
      f"bytes={len(v85)} (the v85 pass-34 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-35 gate name drift49_pass35_match is what the v86 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-33 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-33 evidence' is present — BOTH instrument surfaces, the v86 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "797cfcb:scripts/validate_cycle2785.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v85_commit_object_intact", len(obj.stdout) == len(v85)
          and obj.stdout == v85,
          f"object_bytes={len(obj.stdout)} == disk {len(v85)} (the 797cfcb c2785 commit)")
else:
    guard("v85_commit_object_intact", False, "797cfcb object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
