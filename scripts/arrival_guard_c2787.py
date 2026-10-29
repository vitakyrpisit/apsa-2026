#!/usr/bin/env python3
"""Arrival-guard for cycle 2787 (Job ID 446189) — measured, never predicted.

Spec source: the c2786 Next-block (worklog line 9172). Checks:
  worklog 9172 lines EXACT (newline count, c2786 append post-guard prophecy);
  tail = the c2787 Next bullet;
  anchors ^Task ID: 464 / ^- No gold yet 397 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2787 entries; c2787/c2788 substring accounting
  (the c2787/c2788 token-guard lives INSIDE the c2786 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2787.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2788 = 4 total = 2 HISTORICAL hash-artifact substrings
  (line 9129, the c2782 commit full hash '2be3f8a6c2788f1f99c61a088f45de72415a9eec'
  with the '6c2788f1f9' c+4-digit run) + 2 FORWARD-token births inside the
  c2786 Next-block guard phrase AND FORWARD-token sentence (line 9172) —
  the c2767..c2787 forward-token lessons: measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'validate_cycle2786.py' /
  'scan_cycle2786.json' carries 'e2786', NOT 'c2786' — path tokens are
  e-tokens with ZERO c2786 census contribution, which is why the measured
  c2786 per-line dict has NO line-9167 entry; the guard expectations below
  are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2786 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2786 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2786 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v86 source-intact expectations matched to the v86 pass-35 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v86 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-36 gate name is what the v87 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-34 band' is present AND the evidence-paragraph lag-1 heading
  'pass-34 evidence' is present — BOTH instrument surfaces, the v87 rebadge
  P3/P8 old-string expectations, exactly as the c2786 Next-block wrote).
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
guard("worklog_lines==9172", n_nl == 9172, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2787_next_bullet", last_nonempty.startswith("- Next: the c2787 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==464", tid == 464, f"got={tid}")
guard("anchor_nogold==397", gold == 397, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2787")]
guard("dup_check_zero_serviced_c2787", len(dup) == 0, f"got={len(dup)}")
c2787_total = text.count("c2787")
c2788_total = text.count("c2788")
tok_guard = [l for l in lines if "c2787/c2788" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2787 instance")]
c2787_lines = {i + 1: l.count("c2787") for i, l in enumerate(lines) if "c2787" in l}
c2788_lines = {i + 1: l.count("c2788") for i, l in enumerate(lines) if "c2788" in l}
guard("c2787_mention_accounting_pre",
      c2787_total == 10 and c2788_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2787_lines == {9160: 2, 9164: 3, 9172: 5} and c2788_lines == {9129: 2, 9172: 2},
      f"total={c2787_total} c2788={c2788_total} per-line={c2787_lines} "
      f"c2788_per-line={c2788_lines} "
      f"(expect 10 = 2 in the c2785 Next-block line 9160 [the historical "
      f"c2786/c2787 token-guard phrase + FORWARD-token sentence] + 3 in the c2786 "
      f"Step-1 line 9164 [the census-tuple print '+ c2787 = 2' + the c2786/c2787 "
      f"phrase + the c2787 forward-token per-line-dict phrase] + 5 in the c2786 Next-block line 9172 "
      f"— which is itself the c2787/c2788 token-guard: the instance + id + "
      f"'c2787/c2788' phrase + measure_c2787_tokens.py + the echo-prescription phrase 'the c2787 echo should land'; "
      f"c2788 = 4 — 2 HISTORICAL hash-artifact substrings (line 9129, the c2782 commit "
      f"full hash '2be3f8a6c2788f1f99c61a088f45de72415a9eec' with the '6c2788f1f9' "
      f"c+4-digit run) + 2 FORWARD-token births inside the c2786 Next-block guard "
      f"phrase AND the FORWARD-token sentence, both on line 9172 (the "
      f"forward-token lesson: measured, never assumed unborn))")

c2786_total = text.count("c2786")
c2786_lines = {i + 1: l.count("c2786") for i, l in enumerate(lines) if "c2786" in l}
guard("c2786_mention_census_pre",
      c2786_total == 38
      and c2786_lines == {9148: 2, 9152: 3, 9160: 5, 9162: 1, 9163: 1, 9164: 4,
                          9165: 8, 9170: 4, 9172: 10},
      f"total={c2786_total} per-line={c2786_lines} (NO 9167 entry — the Step-3 "
      f"capture surface 'scan_cycle2786_raw.json' and the Step-4 "
      f"validate_cycle2786.py/scan_cycle2786.json surfaces are e-tokens, the "
      f"c2760 lesson re-verified live at census time)")

for tag, total in (("c2785", 74), ("c2784", 77), ("c2783", 75), ("c2782", 77),
                   ("c2781", 82), ("c2780", 86), ("c2779", 87), ("c2778", 118),
                   ("c2777", 103), ("c2776", 108), ("c2775", 117), ("c2774", 122),
                   ("c2773", 126), ("c2772", 145), ("c2771", 135), ("c2770", 163),
                   ("c2769", 131), ("c2768", 134), ("c2767", 155), ("c2766", 146),
                   ("c2765", 125), ("c2764", 127), ("c2763", 133), ("c2762", 153),
                   ("c2761", 167), ("c2760", 129), ("c2759", 130), ("c2758", 132),
                   ("c2757", 135), ("c2756", 140), ("c2755", 147), ("c2754", 150),
                   ("c2753", 156), ("c2752", 162), ("c2751", 148), ("c2750", 150),
                   ("c2749", 154), ("c2748", 144), ("c2747", 142), ("c2746", 138)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (125 at the census probe: 121 at the "
          f"c2786 census + the official c2786 capture + the loop echo #508 of THIS "
          f"servicing + 2 foreign/unattributed since — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +2 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2786 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2786 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2786:"):
        official_depth = depth
        walk_info.append(f"official c2786 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2786_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2786_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2786 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f precedent)")
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

C2786_SET = [
    "census_c2786.py", "arrival_guard_c2786.py", "rebadge_cycle2786.py",
    "capture_cycle2786.sh", "measure_c2786_tokens.py", "recursive_diff_2786.py",
    "validate_cycle2786.py", "entry_cycle2786.txt", "append_cycle2786.py",
    "scan_cycle2786_raw.json", "scan_cycle2786.json",
]
print("c2786_instrument_set_object_presence:")
missing = []
for name in C2786_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2786 files on disk")

v86 = open("/home/z/my-project/scripts/validate_cycle2786.py", "rb").read()
guard("v86_source_intact", b"CYCLE = 2786" in v86 and b"drift49_pass35_match" in v86
      and b"drift49_pass36_match" not in v86
      and b"(18,0,0,18,0)" in v86 and b"(20,0,2,18,0)" in v86
      and b"(21,0,3,18,0)" in v86 and b"pass-34 band" in v86
      and b"pass-35 band" not in v86
      and b"pass-34 evidence" in v86 and b"pass-35 evidence" not in v86,
      f"bytes={len(v86)} (the v86 pass-35 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-36 gate name drift49_pass36_match is what the v87 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-34 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-34 evidence' is present — BOTH instrument surfaces, the v87 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "b0c7947:scripts/validate_cycle2786.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v86_commit_object_intact", len(obj.stdout) == len(v86)
          and obj.stdout == v86,
          f"object_bytes={len(obj.stdout)} == disk {len(v86)} (the b0c7947 c2786 commit)")
else:
    guard("v86_commit_object_intact", False, "b0c7947 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
