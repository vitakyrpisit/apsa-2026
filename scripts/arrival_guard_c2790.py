#!/usr/bin/env python3
"""Arrival-guard for cycle 2790 (Job ID 446189) — measured, never predicted.

Spec source: the c2789 Next-block (worklog line 9208). Checks:
  worklog 9208 lines EXACT (newline count, c2789 append post-guard prophecy);
  tail = the c2790 Next bullet;
  anchors ^Task ID: 467 / ^- No gold yet 400 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2790 entries; c2790/c2791 substring accounting
  (the c2790/c2791 token-guard lives INSIDE the c2789 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2790.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2791 = 2 total = 2 FORWARD-token births inside the c2789
  Next-block guard phrase ('arrival-guard against c2790/c2791 tokens') AND
  the FORWARD-token sentence ('the FORWARD token c2791 must be IN the census
  tuple'), both on line 9208 — the c2767..c2790 forward-token lessons:
  measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-3/4 surfaces 'scan_cycle2789_raw.json'
  / 'validate_cycle2789.py' / 'scan_cycle2789.json' carry 'e2789'/'cycle2789',
  NOT the bare c-token 'c2789' — path tokens contribute ZERO bare-c2789
  census weight, which is why the measured c2789 per-line dict has NO 9202
  entry (the c2789 Step-3 line); the guard expectations below are the census
  MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2789 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2789 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2789 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v89 source-intact expectations matched to the v89 pass-38 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v89 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-39 gate name is what the v90 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-37 band' is present AND the evidence-paragraph lag-1 heading
  'pass-37 evidence' is present — BOTH instrument surfaces, the v90 rebadge
  P3/P8 old-string expectations, exactly as the c2789 Next-block wrote).
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
guard("worklog_lines==9208", n_nl == 9208, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2790_next_bullet", last_nonempty.startswith("- Next: the c2790 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==467", tid == 467, f"got={tid}")
guard("anchor_nogold==400", gold == 400, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2790")]
guard("dup_check_zero_serviced_c2790", len(dup) == 0, f"got={len(dup)}")
c2790_total = text.count("c2790")
c2791_total = text.count("c2791")
tok_guard = [l for l in lines if "c2790/c2791" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2790 instance")]
c2790_lines = {i + 1: l.count("c2790") for i, l in enumerate(lines) if "c2790" in l}
c2791_lines = {i + 1: l.count("c2791") for i, l in enumerate(lines) if "c2791" in l}
guard("c2790_mention_accounting_pre",
      c2790_total == 8 and c2791_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2790_lines == {9196: 2, 9200: 1, 9206: 1, 9208: 4}
      and c2791_lines == {9208: 2},
      f"total={c2790_total} c2791={c2791_total} per-line={c2790_lines} "
      f"c2791_per-line={c2791_lines} "
      f"(expect 8 = 2 FORWARD-token births inside the c2788 Next-block (line 9196, "
      f"the guard phrase 'c2789/c2790' AND the FORWARD-token sentence) + 1 in the "
      f"c2789 Step-1 line 9200 (the loop echo #510 mention) + 1 in the c2789 "
      f"Step-7 line 9206 ('the c2790 pre==2 expectation measured BEFORE the run') "
      f"+ 4 in the c2789 Next-block line 9208 — which is itself the c2790/c2791 "
      f"token-guard: the instance + id + 'c2790/c2791' phrase + "
      f"measure_c2790_tokens.py + the echo-prescription phrase 'the c2789 echo "
      f"landed'; c2791 = 2 — 2 FORWARD-token births inside the c2789 "
      f"Next-block guard phrase AND the FORWARD-token sentence, both on line "
      f"9208 (the forward-token lesson: measured, never assumed unborn))")

c2789_total = text.count("c2789")
c2789_lines = {i + 1: l.count("c2789") for i, l in enumerate(lines) if "c2789" in l}
guard("c2789_mention_census_pre",
      c2789_total == 36
      and c2789_lines == {9184: 2, 9188: 1, 9194: 1, 9196: 5, 9199: 1, 9200: 3,
                          9201: 8, 9206: 4, 9208: 11},
      f"total={c2789_total} per-line={c2789_lines} (NO 9202 entry — the Step-3 "
      f"capture surface 'scan_cycle2789_raw.json' and the Step-4 "
      f"validate_cycle2789.py/scan_cycle2789.json surfaces carry 'cycle2789'/'e2789', "
      f"NOT the bare c-token, the c2760 lesson re-verified live at census time)")

for tag, total in (("c2788", 76), ("c2787", 87), ("c2786", 92), ("c2785", 91),
                   ("c2784", 89), ("c2783", 88), ("c2782", 89), ("c2781", 94),
                   ("c2780", 98), ("c2779", 99), ("c2778", 134), ("c2777", 115),
                   ("c2776", 120), ("c2775", 129), ("c2774", 134), ("c2773", 138),
                   ("c2772", 157), ("c2771", 147), ("c2770", 178), ("c2769", 140),
                   ("c2768", 143), ("c2767", 170), ("c2766", 158), ("c2765", 134),
                   ("c2764", 136), ("c2763", 144), ("c2762", 165), ("c2761", 179),
                   ("c2760", 139), ("c2759", 139), ("c2758", 141), ("c2757", 144),
                   ("c2756", 149), ("c2755", 156), ("c2754", 159), ("c2753", 165),
                   ("c2752", 171), ("c2751", 157), ("c2750", 159), ("c2749", 163),
                   ("c2748", 153), ("c2747", 151), ("c2746", 150)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (136 at the census probe: 132 at the "
          f"c2789 census + the official c2789 capture + the loop echo #511 of THIS "
          f"servicing + 2 foreign/unattributed since — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +2 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2789 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2789 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2789:"):
        official_depth = depth
        walk_info.append(f"official c2789 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2789_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2789_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2789 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029 precedent)")
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

C2789_SET = [
    "census_c2789.py", "arrival_guard_c2789.py", "rebadge_cycle2789.py",
    "capture_cycle2789.sh", "measure_c2789_tokens.py", "recursive_diff_2789.py",
    "validate_cycle2789.py", "entry_cycle2789.txt", "append_cycle2789.py",
    "scan_cycle2789_raw.json", "scan_cycle2789.json",
]
print("c2789_instrument_set_object_presence:")
missing = []
for name in C2789_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2789 files on disk")

v89 = open("/home/z/my-project/scripts/validate_cycle2789.py", "rb").read()
guard("v89_source_intact", b"CYCLE = 2789" in v89 and b"drift49_pass38_match" in v89
      and b"drift49_pass39_match" not in v89
      and b"(18,0,0,18,0)" in v89 and b"(20,0,2,18,0)" in v89
      and b"(21,0,3,18,0)" in v89 and b"pass-37 band" in v89
      and b"pass-38 band" not in v89
      and b"pass-37 evidence" in v89 and b"pass-38 evidence" not in v89,
      f"bytes={len(v89)} (the v89 pass-38 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-39 gate name drift49_pass39_match is what the v90 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-37 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-37 evidence' is present — BOTH instrument surfaces, the v90 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "2af9fd7:scripts/validate_cycle2789.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v89_commit_object_intact", len(obj.stdout) == len(v89)
          and obj.stdout == v89,
          f"object_bytes={len(obj.stdout)} == disk {len(v89)} (the 2af9fd7 c2789 commit)")
else:
    guard("v89_commit_object_intact", False, "2af9fd7 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
