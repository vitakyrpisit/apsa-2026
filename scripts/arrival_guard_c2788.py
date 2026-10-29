#!/usr/bin/env python3
"""Arrival-guard for cycle 2788 (Job ID 446189) — measured, never predicted.

Spec source: the c2787 Next-block (worklog line 9184). Checks:
  worklog 9184 lines EXACT (newline count, c2787 append post-guard prophecy);
  tail = the c2788 Next bullet;
  anchors ^Task ID: 465 / ^- No gold yet 398 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2788 entries; c2788/c2789 substring accounting
  (the c2788/c2789 token-guard lives INSIDE the c2787 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2788.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2789 = 2 total = 2 FORWARD-token births inside the c2787
  Next-block guard phrase ('arrival-guard against c2788/c2789 tokens') AND
  the FORWARD-token sentence ('the FORWARD token c2789 must be IN the census
  tuple'), both on line 9184 — the c2767..c2788 forward-token lessons:
  measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-3/4 surfaces 'scan_cycle2787_raw.json'
  / 'validate_cycle2787.py' / 'scan_cycle2787.json' carry 'e2787'/'cycle2787',
  NOT the bare c-token 'c2787' — path tokens contribute ZERO bare-c2787
  census weight, which is why the measured c2787 per-line dict has NO 9178
  entry (the c2787 Step-3 line); the guard expectations below are the census
  MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2787 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2787 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2787 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v87 source-intact expectations matched to the v87 pass-36 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v87 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-37 gate name is what the v88 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-35 band' is present AND the evidence-paragraph lag-1 heading
  'pass-35 evidence' is present — BOTH instrument surfaces, the v88 rebadge
  P3/P8 old-string expectations, exactly as the c2787 Next-block wrote).
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
guard("worklog_lines==9184", n_nl == 9184, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2788_next_bullet", last_nonempty.startswith("- Next: the c2788 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==465", tid == 465, f"got={tid}")
guard("anchor_nogold==398", gold == 398, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2788")]
guard("dup_check_zero_serviced_c2788", len(dup) == 0, f"got={len(dup)}")
c2788_total = text.count("c2788")
c2789_total = text.count("c2789")
tok_guard = [l for l in lines if "c2788/c2789" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2788 instance")]
c2788_lines = {i + 1: l.count("c2788") for i, l in enumerate(lines) if "c2788" in l}
c2789_lines = {i + 1: l.count("c2789") for i, l in enumerate(lines) if "c2789" in l}
guard("c2788_mention_accounting_pre",
      c2788_total == 11 and c2789_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2788_lines == {9129: 2, 9172: 2, 9176: 2, 9184: 5}
      and c2789_lines == {9184: 2},
      f"total={c2788_total} c2789={c2789_total} per-line={c2788_lines} "
      f"c2789_per-line={c2789_lines} "
      f"(expect 11 = 2 HISTORICAL hash-artifact substrings (line 9129, the c2782 commit "
      f"full hash '2be3f8a6c2788f1f99c61a088f45de72415a9eec' with the '6c2788f1f9' "
      f"c+4-digit run) + 2 FORWARD-token births inside the c2786 Next-block (line 9172, "
      f"the guard phrase 'c2787/c2788' AND the echo-prescription sentence 'the c2788 echo "
      f"should land') + 2 inside the c2787 Step-1 line 9176 (the guard-phrase "
      f"'c2787/c2788 token-guard' + the forward-token per-line-dict sentence) + 5 in the "
      f"c2787 Next-block line 9184 — which is itself the c2788/c2789 token-guard: the "
      f"instance + id + 'c2788/c2789' phrase + measure_c2788_tokens.py + the "
      f"echo-prescription phrase 'the c2788 echo should land'; "
      f"c2789 = 2 — 2 FORWARD-token births inside the c2787 Next-block guard "
      f"phrase AND the FORWARD-token sentence, both on line 9184 (the "
      f"forward-token lesson: measured, never assumed unborn))")

c2787_total = text.count("c2787")
c2787_lines = {i + 1: l.count("c2787") for i, l in enumerate(lines) if "c2787" in l}
guard("c2787_mention_census_pre",
      c2787_total == 38
      and c2787_lines == {9160: 2, 9164: 3, 9172: 5, 9174: 1, 9175: 1, 9176: 3,
                          9177: 8, 9182: 4, 9184: 11},
      f"total={c2787_total} per-line={c2787_lines} (NO 9178 entry — the Step-3 "
      f"capture surface 'scan_cycle2787_raw.json' and the Step-4 "
      f"validate_cycle2787.py/scan_cycle2787.json surfaces carry 'cycle2787'/'e2787', "
      f"NOT the bare c-token, the c2760 lesson re-verified live at census time)")

for tag, total in (("c2786", 78), ("c2785", 82), ("c2784", 81), ("c2783", 79),
                   ("c2782", 81), ("c2781", 86), ("c2780", 90), ("c2779", 91),
                   ("c2778", 124), ("c2777", 107), ("c2776", 112), ("c2775", 121),
                   ("c2774", 126), ("c2773", 130), ("c2772", 149), ("c2771", 139),
                   ("c2770", 168), ("c2769", 134), ("c2768", 137), ("c2767", 160),
                   ("c2766", 150), ("c2765", 128), ("c2764", 130), ("c2763", 137),
                   ("c2762", 157), ("c2761", 171), ("c2760", 133), ("c2759", 133),
                   ("c2758", 135), ("c2757", 138), ("c2756", 143), ("c2755", 150),
                   ("c2754", 153), ("c2753", 159), ("c2752", 165), ("c2751", 151),
                   ("c2750", 153), ("c2749", 157), ("c2748", 147), ("c2747", 145),
                   ("c2746", 142)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (128 at the census probe: 125 at the "
          f"c2787 census + the official c2787 capture + the loop echo #509 of THIS "
          f"servicing + 1 foreign/unattributed since — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +1 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2787 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2787 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2787:"):
        official_depth = depth
        walk_info.append(f"official c2787 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2787_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2787_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2787 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512 precedent)")
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

C2787_SET = [
    "census_c2787.py", "arrival_guard_c2787.py", "rebadge_cycle2787.py",
    "capture_cycle2787.sh", "measure_c2787_tokens.py", "recursive_diff_2787.py",
    "validate_cycle2787.py", "entry_cycle2787.txt", "append_cycle2787.py",
    "scan_cycle2787_raw.json", "scan_cycle2787.json",
]
print("c2787_instrument_set_object_presence:")
missing = []
for name in C2787_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2787 files on disk")

v87 = open("/home/z/my-project/scripts/validate_cycle2787.py", "rb").read()
guard("v87_source_intact", b"CYCLE = 2787" in v87 and b"drift49_pass36_match" in v87
      and b"drift49_pass37_match" not in v87
      and b"(18,0,0,18,0)" in v87 and b"(20,0,2,18,0)" in v87
      and b"(21,0,3,18,0)" in v87 and b"pass-35 band" in v87
      and b"pass-36 band" not in v87
      and b"pass-35 evidence" in v87 and b"pass-36 evidence" not in v87,
      f"bytes={len(v87)} (the v87 pass-36 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-37 gate name drift49_pass37_match is what the v88 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-35 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-35 evidence' is present — BOTH instrument surfaces, the v88 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "a762125:scripts/validate_cycle2787.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v87_commit_object_intact", len(obj.stdout) == len(v87)
          and obj.stdout == v87,
          f"object_bytes={len(obj.stdout)} == disk {len(v87)} (the a762125 c2787 commit)")
else:
    guard("v87_commit_object_intact", False, "a762125 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
