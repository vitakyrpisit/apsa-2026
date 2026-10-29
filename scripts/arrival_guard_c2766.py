#!/usr/bin/env python3
"""Arrival-guard for cycle 2766 (Job ID 446189) — measured, never predicted.

Spec source: the c2765 Next-block (worklog line 8920). Checks:
  worklog 8920 lines EXACT (newline count, c2765 append post-guard prophecy);
  tail = the c2766 Next bullet;
  anchors ^Task ID: 443 / ^- No gold yet 376 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2766 entries; c2766/c2767 substring accounting
  (the c2766/c2767 token-guard lives INSIDE the c2765 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2766.py, expectations below are the MEASURED values);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2765 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2765 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2765 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v65 source-intact expectations matched to the v65 pass-14 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v65 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-15 gate name is what the v66 rebadge introduces).
"""
import os
import subprocess
import sys
import time

WL = "/home/z/my-project/worklog.md"
DEVLOG = "/home/z/my-project/dev.log"
BA = "/home/z/my-project/.basedagents"

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


print(f"guard_run_epoch={time.time():.9f}")
raw = open(WL, "rb").read()
n_nl = raw.count(b"\n")
guard("worklog_lines==8920", n_nl == 8920, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2766_next_bullet", last_nonempty.startswith("- Next: the c2766 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==443", tid == 443, f"got={tid}")
guard("anchor_nogold==376", gold == 376, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2766")]
guard("dup_check_zero_serviced_c2766", len(dup) == 0, f"got={len(dup)}")
c2766_total = text.count("c2766")
c2767_total = text.count("c2767")
tok_guard = [l for l in lines if "c2766/c2767" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2766 instance")]
c2766_lines = {i + 1: l.count("c2766") for i, l in enumerate(lines) if "c2766" in l}
guard("c2766_mention_accounting_pre",
      c2766_total == 7 and c2767_total == 1 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2766_lines == {8908: 1, 8912: 2, 8920: 4},
      f"total={c2766_total} c2767={c2767_total} per-line={c2766_lines} "
      f"(expect 7 = 1 in the c2764 Next-block line 8908 [the "
      f"'c2765/c2766' token-guard phrase] + 2 in the c2765 Step-1 line 8912 [the "
      f"c2765-guard output quote '+ c2766 = 1' + the 'c2765/c2766 token-guard' "
      f"phrase] + 4 in the c2765 Next-block line 8920 — which is itself the "
      f"c2766/c2767 token-guard: instance + Task ID + the guard phrase + "
      f"measure_c2766_tokens.py)")

c2765_total = text.count("c2765")
c2765_lines = {i + 1: l.count("c2765") for i, l in enumerate(lines) if "c2765" in l}
guard("c2765_mention_census_pre",
      c2765_total == 26
      and c2765_lines == {8896: 1, 8900: 2, 8908: 4, 8911: 1, 8912: 4, 8913: 6,
                          8918: 1, 8920: 7},
      f"total={c2765_total} per-line={c2765_lines}")

c2764_total = text.count("c2764")
c2764_lines = {i + 1: l.count("c2764") for i, l in enumerate(lines) if "c2764" in l}
guard("c2764_mention_census_pre",
      c2764_total == 54
      and c2764_lines == {8884: 1, 8888: 2, 8896: 4, 8899: 1, 8900: 5, 8901: 6,
                          8906: 1, 8908: 7, 8910: 6, 8912: 9, 8913: 7, 8914: 2,
                          8918: 1, 8920: 2},
      f"total={c2764_total} per-line={c2764_lines}")

c2763_total = text.count("c2763")
c2763_lines = {i + 1: l.count("c2763") for i, l in enumerate(lines) if "c2763" in l}
guard("c2763_mention_census_pre",
      c2763_total == 63
      and c2763_lines == {8872: 1, 8876: 2, 8884: 4, 8887: 1, 8888: 5, 8889: 6,
                          8894: 1, 8896: 6, 8898: 6, 8900: 9, 8901: 7, 8902: 1,
                          8906: 1, 8908: 2, 8910: 5, 8912: 1, 8913: 2, 8914: 1,
                          8920: 2},
      f"total={c2763_total} per-line={c2763_lines}")

c2762_total = text.count("c2762")
c2762_lines = {i + 1: l.count("c2762") for i, l in enumerate(lines) if "c2762" in l}
guard("c2762_mention_census_pre",
      c2762_total == 65
      and c2762_lines == {8860: 1, 8864: 2, 8872: 4, 8875: 1, 8876: 5, 8877: 6,
                          8882: 1, 8884: 6, 8886: 6, 8888: 8, 8889: 7, 8890: 1,
                          8894: 1, 8896: 2, 8898: 1, 8900: 1, 8901: 2, 8908: 2,
                          8910: 2, 8912: 1, 8913: 2, 8917: 1, 8920: 2},
      f"total={c2762_total} per-line={c2762_lines}")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (53 at echo time: 51 at the c2765 "
          f"guard + the official c2765 capture (the latency-matched 1730ms render) "
          f"+ 1 since, foreign/unattributed — dev.log is timestamp-less: the "
          f"official/foreign split is by latency-match, honest, no over-claim)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


head_body = git("log", "-1", "--format=%B")
head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
parent_body = git("log", "-1", "--format=%B", "HEAD~1")
parent_short = git("log", "-1", "--format=%h", "HEAD~1")
head_is_official = head_body.startswith("c2765:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2765_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2765_commit", parent_body.startswith("c2765:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2765 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/7b9e5f3/519471c/b28848d/5939089 precedent)")
head_stat = git("show", "--stat", "--format=", head_short)
n_files = len([l for l in head_stat.splitlines() if l.strip()])
guard("git_head_zero_ledger_touch", "worklog.md" not in head_stat,
      f"HEAD touches {n_files} file entries; worklog touched={'worklog.md' in head_stat}")
print(f"head_commit_stat_tail: {head_stat.splitlines()[-1] if head_stat else '(empty)'}")
recent = git("log", "-3", "--format=%h %s")
print("recent_commits:")
for ln in recent.splitlines():
    print(f"  {ln[:120]}")
status = git("status", "--short")
print(f"working_tree_entries={len(status.splitlines()) if status else 0}")

C2765_SET = [
    "rebadge_cycle2765.py", "capture_cycle2765.sh", "measure_c2765_tokens.py",
    "recursive_diff_2765.py", "validate_cycle2765.py", "entry_cycle2765.txt",
    "append_cycle2765.py", "scan_cycle2765_raw.json", "scan_cycle2765.json",
]
print("c2765_instrument_set_object_presence:")
missing = []
for name in C2765_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2765 files on disk")

v65 = open("/home/z/my-project/scripts/validate_cycle2765.py", "rb").read()
guard("v65_source_intact", b"CYCLE = 2765" in v65 and b"drift49_pass14_match" in v65
      and b"drift49_pass15_match" not in v65
      and b"(18,0,0,18,0)" in v65 and b"(20,0,2,18,0)" in v65
      and b"(21,0,3,18,0)" in v65,
      f"bytes={len(v65)} (the v65 pass-14 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-15 gate name drift49_pass15_match is what the v66 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "5409e39:scripts/validate_cycle2765.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v65_commit_object_intact", len(obj.stdout) == len(v65)
          and obj.stdout == v65,
          f"object_bytes={len(obj.stdout)} == disk {len(v65)} (the 5409e39 c2765 commit)")
else:
    guard("v65_commit_object_intact", False, "5409e39 object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
