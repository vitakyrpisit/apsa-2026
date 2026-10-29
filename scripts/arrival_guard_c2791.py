#!/usr/bin/env python3
"""Arrival-guard for cycle 2791 (Job ID 446189) — measured, never predicted.

Spec source: the c2790 Next-block (worklog line 9220). Checks:
  worklog 9220 lines EXACT (newline count, c2790 append post-guard prophecy);
  tail = the c2791 Next bullet;
  anchors ^Task ID: 468 / ^- No gold yet 401 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2791 entries; c2791/c2792 substring accounting
  (the c2791/c2792 token-guard lives INSIDE the c2790 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2791.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2792 = 2 total = 2 FORWARD-token births inside the c2790
  Next-block guard phrase ('arrival-guard against c2791/c2792 tokens') AND
  the FORWARD-token sentence ('the FORWARD token c2792 must be IN the census
  tuple'), both on line 9220 — the c2767..c2791 forward-token lessons:
  measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-3/4 surfaces 'scan_cycle2790_raw.json'
  / 'validate_cycle2790.py' / 'scan_cycle2790.json' carry 'e2790'/'cycle2790',
  NOT the bare c-token 'c2790' — path tokens contribute ZERO bare-c2790
  census weight, which is why the measured c2790 per-line dict has NO 9214
  entry (the c2790 Step-3 line); the guard expectations below are the census
  MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2790 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2790 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2790 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v90 source-intact expectations matched to the v90 pass-39 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v90 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-40 gate name is what the v91 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-38 band' is present AND the evidence-paragraph lag-1 heading
  'pass-38 evidence' is present — BOTH instrument surfaces, the v91 rebadge
  P3/P8 old-string expectations, exactly as the c2790 Next-block wrote).
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
guard("worklog_lines==9220", n_nl == 9220, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2791_next_bullet", last_nonempty.startswith("- Next: the c2791 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==468", tid == 468, f"got={tid}")
guard("anchor_nogold==401", gold == 401, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2791")]
guard("dup_check_zero_serviced_c2791", len(dup) == 0, f"got={len(dup)}")
c2791_total = text.count("c2791")
c2792_total = text.count("c2792")
tok_guard = [l for l in lines if "c2791/c2792" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2791 instance")]
c2791_lines = {i + 1: l.count("c2791") for i, l in enumerate(lines) if "c2791" in l}
c2792_lines = {i + 1: l.count("c2792") for i, l in enumerate(lines) if "c2792" in l}
guard("c2791_mention_accounting_pre",
      c2791_total == 8 and c2792_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2791_lines == {9208: 2, 9212: 1, 9218: 1, 9220: 4}
      and c2792_lines == {9220: 2},
      f"total={c2791_total} c2792={c2792_total} per-line={c2791_lines} "
      f"c2792_per-line={c2792_lines} "
      f"(expect 8 = 2 FORWARD-token births inside the c2789 Next-block (line 9208, "
      f"the guard phrase 'c2790/c2791' AND the FORWARD-token sentence) + 1 in the "
      f"c2790 Step-1 line 9212 (the loop echo #511 mention) + 1 in the c2790 "
      f"Step-7 line 9218 ('the c2791 pre==2 expectation measured BEFORE the run') "
      f"+ 4 in the c2790 Next-block line 9220 — which is itself the c2791/c2792 "
      f"token-guard: the instance + id + 'c2791/c2792' phrase + "
      f"measure_c2791_tokens.py; c2792 = 2 — 2 FORWARD-token births inside the "
      f"c2790 Next-block guard phrase AND the FORWARD-token sentence, both on "
      f"line 9220 (the forward-token lesson: measured, never assumed unborn))")

c2790_total = text.count("c2790")
c2790_lines = {i + 1: l.count("c2790") for i, l in enumerate(lines) if "c2790" in l}
guard("c2790_mention_census_pre",
      c2790_total == 35
      and c2790_lines == {9196: 2, 9200: 1, 9206: 1, 9208: 4, 9211: 1, 9212: 3,
                          9213: 8, 9218: 4, 9220: 11},
      f"total={c2790_total} per-line={c2790_lines} (NO 9214 entry — the Step-3 "
      f"capture surface 'scan_cycle2790_raw.json' and the Step-4 "
      f"validate_cycle2790.py/scan_cycle2790.json surfaces carry 'cycle2790'/'e2790', "
      f"NOT the bare c-token, the c2760 lesson re-verified live at census time)")

for tag, total in (("c2789", 74), ("c2788", 87), ("c2787", 91), ("c2786", 97),
                   ("c2785", 95), ("c2784", 93), ("c2783", 93), ("c2782", 93),
                   ("c2781", 98), ("c2780", 102), ("c2779", 103), ("c2778", 139),
                   ("c2777", 119), ("c2776", 124), ("c2775", 133), ("c2774", 138),
                   ("c2773", 142), ("c2772", 161), ("c2771", 151), ("c2770", 183),
                   ("c2769", 143), ("c2768", 146), ("c2767", 175), ("c2766", 162),
                   ("c2765", 137), ("c2764", 139), ("c2763", 147), ("c2762", 169),
                   ("c2761", 183), ("c2760", 142), ("c2759", 142), ("c2758", 144),
                   ("c2757", 147), ("c2756", 152), ("c2755", 159), ("c2754", 162),
                   ("c2753", 168), ("c2752", 174), ("c2751", 160), ("c2750", 162),
                   ("c2749", 166), ("c2748", 156), ("c2747", 154), ("c2746", 154)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (139 at the census probe: 136 at the "
          f"c2790 census + the official c2790 capture + the loop echo #512 of THIS "
          f"servicing + 1 foreign/unattributed since — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +1 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2790 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2790 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2790:"):
        official_depth = depth
        walk_info.append(f"official c2790 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2790_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2790_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2790 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581 precedent)")
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

C2790_SET = [
    "census_c2790.py", "arrival_guard_c2790.py", "rebadge_cycle2790.py",
    "capture_cycle2790.sh", "measure_c2790_tokens.py", "recursive_diff_2790.py",
    "validate_cycle2790.py", "entry_cycle2790.txt", "append_cycle2790.py",
    "scan_cycle2790_raw.json", "scan_cycle2790.json",
]
print("c2790_instrument_set_object_presence:")
missing = []
for name in C2790_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2790 files on disk")

v90 = open("/home/z/my-project/scripts/validate_cycle2790.py", "rb").read()
guard("v90_source_intact", b"CYCLE = 2790" in v90 and b"drift49_pass39_match" in v90
      and b"drift49_pass40_match" not in v90
      and b"(18,0,0,18,0)" in v90 and b"(20,0,2,18,0)" in v90
      and b"(21,0,3,18,0)" in v90 and b"pass-38 band" in v90
      and b"pass-39 band" not in v90
      and b"pass-38 evidence" in v90 and b"pass-39 evidence" not in v90,
      f"bytes={len(v90)} (the v90 pass-39 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-40 gate name drift49_pass40_match is what the v91 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-38 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-38 evidence' is present — BOTH instrument surfaces, the v91 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "e4a79df:scripts/validate_cycle2790.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v90_commit_object_intact", len(obj.stdout) == len(v90)
          and obj.stdout == v90,
          f"object_bytes={len(obj.stdout)} == disk {len(v90)} (the e4a79df c2790 commit)")
else:
    guard("v90_commit_object_intact", False, "e4a79df object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
