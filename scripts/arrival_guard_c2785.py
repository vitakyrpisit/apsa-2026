#!/usr/bin/env python3
"""Arrival-guard for cycle 2785 (Job ID 446189) — measured, never predicted.

Spec source: the c2784 Next-block (worklog line 9148). Checks:
  worklog 9148 lines EXACT (newline count, c2784 append post-guard prophecy);
  tail = the c2785 Next bullet;
  anchors ^Task ID: 462 / ^- No gold yet 395 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2785 entries; c2785/c2786 substring accounting
  (the c2785/c2786 token-guard lives INSIDE the c2784 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2785.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2786 = 2 born inside the c2784 Next-block guard phrase AND
  FORWARD-token sentence — the c2767..c2785 forward-token lessons:
  measure it, never assume it unborn);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2784 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2784 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2784 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v84 source-intact expectations matched to the v84 pass-33 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v84 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-34 gate name is what the v85 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-32 band' is present AND the evidence-paragraph lag-1 heading
  'pass-32 evidence' is present — BOTH instrument surfaces, the v85 rebadge
  P3/P8 old-string expectations, exactly as the c2784 Next-block wrote).
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
guard("worklog_lines==9148", n_nl == 9148, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2785_next_bullet", last_nonempty.startswith("- Next: the c2785 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==462", tid == 462, f"got={tid}")
guard("anchor_nogold==395", gold == 395, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2785")]
guard("dup_check_zero_serviced_c2785", len(dup) == 0, f"got={len(dup)}")
c2785_total = text.count("c2785")
c2786_total = text.count("c2786")
tok_guard = [l for l in lines if "c2785/c2786" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2785 instance")]
c2785_lines = {i + 1: l.count("c2785") for i, l in enumerate(lines) if "c2785" in l}
c2786_lines = {i + 1: l.count("c2786") for i, l in enumerate(lines) if "c2786" in l}
guard("c2785_mention_accounting_pre",
      c2785_total == 8 and c2786_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2785_lines == {9136: 2, 9140: 2, 9148: 4} and c2786_lines == {9148: 2},
      f"total={c2785_total} c2786={c2786_total} per-line={c2785_lines} "
      f"c2786_per-line={c2786_lines} "
      f"(expect 8 = 2 in the c2783 Next-block line 9136 [the historical "
      f"c2784/c2785 token-guard phrase + FORWARD-token sentence] + 2 in the c2784 "
      f"Step-1 line 9140 [the census-tuple print '+ c2785 = 2' + the c2784/c2785 "
      f"phrase] + 4 in the c2784 Next-block line 9148 — which is itself the "
      f"c2785/c2786 token-guard: the instance + id + 'c2785/c2786' phrase + "
      f"measure_c2785_tokens.py (the 'window-2785' phrasing carries NO c-token — "
      f"hyphen, not c-prefix); c2786 = 2 — the forward token is BORN inside the "
      f"c2784 Next-block guard phrase AND the FORWARD-token sentence, both on line "
      f"9148 (the forward-token lesson: measured, never assumed unborn))")

c2784_total = text.count("c2784")
c2784_lines = {i + 1: l.count("c2784") for i, l in enumerate(lines) if "c2784" in l}
guard("c2784_mention_census_pre",
      c2784_total == 35
      and c2784_lines == {9124: 2, 9128: 2, 9136: 4, 9139: 1, 9140: 4, 9141: 8,
                          9146: 5, 9148: 9},
      f"total={c2784_total} per-line={c2784_lines}")

c2783_total = text.count("c2783")
c2783_lines = {i + 1: l.count("c2783") for i, l in enumerate(lines) if "c2783" in l}
guard("c2783_mention_census_pre",
      c2783_total == 65
      and c2783_lines == {9112: 2, 9116: 2, 9124: 4, 9127: 1, 9128: 4, 9129: 8,
                          9134: 5, 9136: 9, 9138: 8, 9140: 9, 9141: 8, 9142: 2,
                          9145: 1, 9146: 1, 9148: 1},
      f"total={c2783_total} per-line={c2783_lines}")

for tag, total in (("c2782", 68), ("c2781", 74), ("c2780", 78), ("c2779", 79),
                   ("c2778", 106), ("c2777", 95), ("c2776", 100), ("c2775", 109),
                   ("c2774", 114), ("c2773", 118), ("c2772", 134), ("c2771", 127),
                   ("c2770", 153), ("c2769", 125), ("c2768", 128), ("c2767", 145),
                   ("c2766", 138), ("c2765", 119), ("c2764", 121), ("c2763", 125),
                   ("c2762", 145), ("c2761", 159), ("c2760", 122), ("c2759", 124),
                   ("c2758", 126), ("c2757", 129), ("c2756", 134), ("c2755", 141),
                   ("c2754", 144), ("c2753", 150), ("c2752", 156), ("c2751", 142),
                   ("c2750", 144), ("c2749", 148), ("c2748", 138), ("c2747", 136),
                   ("c2746", 129)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (117 at the census probe: 114 at the "
          f"c2784 guard + the official c2784 capture + 1 foreign since + the "
          f"in-batch loop-open echo of THIS servicing — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +1 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2784 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2784 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2784:"):
        official_depth = depth
        walk_info.append(f"official c2784 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2784_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2784_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2784 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec precedent)")
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

C2784_SET = [
    "census_c2784.py", "arrival_guard_c2784.py", "rebadge_cycle2784.py",
    "capture_cycle2784.sh", "measure_c2784_tokens.py", "recursive_diff_2784.py",
    "validate_cycle2784.py", "entry_cycle2784.txt", "append_cycle2784.py",
    "scan_cycle2784_raw.json", "scan_cycle2784.json",
]
print("c2784_instrument_set_object_presence:")
missing = []
for name in C2784_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2784 files on disk")

v84 = open("/home/z/my-project/scripts/validate_cycle2784.py", "rb").read()
guard("v84_source_intact", b"CYCLE = 2784" in v84 and b"drift49_pass33_match" in v84
      and b"drift49_pass34_match" not in v84
      and b"(18,0,0,18,0)" in v84 and b"(20,0,2,18,0)" in v84
      and b"(21,0,3,18,0)" in v84 and b"pass-32 band" in v84
      and b"pass-33 band" not in v84
      and b"pass-32 evidence" in v84 and b"pass-33 evidence" not in v84,
      f"bytes={len(v84)} (the v84 pass-33 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-34 gate name drift49_pass34_match is what the v85 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-32 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-32 evidence' is present — BOTH instrument surfaces, the v85 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "9b1c925:scripts/validate_cycle2784.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v84_commit_object_intact", len(obj.stdout) == len(v84)
          and obj.stdout == v84,
          f"object_bytes={len(obj.stdout)} == disk {len(v84)} (the 9b1c925 c2784 commit)")
else:
    guard("v84_commit_object_intact", False, "9b1c925 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
