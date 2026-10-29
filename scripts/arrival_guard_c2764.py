#!/usr/bin/env python3
"""Arrival-guard for cycle 2764 (Job ID 446189) — measured, never predicted.

Spec source: the c2763 Next-block (worklog line 8896). Checks:
  worklog 8896 lines EXACT (newline count, c2763 append post-guard prophecy);
  tail = the c2764 Next bullet;
  anchors ^Task ID: 441 / ^- No gold yet 374 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2764 entries; c2764/c2765 substring accounting
  (the c2764/c2765 token-guard lives INSIDE the c2763 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2764.py, expectations below are the MEASURED values);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2763 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2763 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2763 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v63 source-intact expectations matched to the v63 pass-12 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v63 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-13 gate name is what the v64 rebadge introduces).
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
guard("worklog_lines==8896", n_nl == 8896, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2764_next_bullet", last_nonempty.startswith("- Next: the c2764 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==441", tid == 441, f"got={tid}")
guard("anchor_nogold==374", gold == 374, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2764")]
guard("dup_check_zero_serviced_c2764", len(dup) == 0, f"got={len(dup)}")
c2764_total = text.count("c2764")
c2765_total = text.count("c2765")
tok_guard = [l for l in lines if "c2764/c2765" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2764 instance")]
c2764_lines = {i + 1: l.count("c2764") for i, l in enumerate(lines) if "c2764" in l}
guard("c2764_mention_accounting_pre",
      c2764_total == 7 and c2765_total == 1 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2764_lines == {8884: 1, 8888: 2, 8896: 4},
      f"total={c2764_total} c2765={c2765_total} per-line={c2764_lines} "
      f"(expect 7 = 1 in the c2762 Next-block line 8884 [the "
      f"'c2763/c2764' token-guard phrase] + 2 in the c2763 Step-1 line 8888 [the "
      f"c2763-guard output quote '+ c2764 = 1' + the 'c2763/c2764 token-guard' "
      f"phrase] + 4 in the c2763 Next-block line 8896 — which is itself the "
      f"c2764/c2765 token-guard)")

c2763_total = text.count("c2763")
c2763_lines = {i + 1: l.count("c2763") for i, l in enumerate(lines) if "c2763" in l}
guard("c2763_mention_census_pre",
      c2763_total == 26
      and c2763_lines == {8872: 1, 8876: 2, 8884: 4, 8887: 1, 8888: 5, 8889: 6,
                          8894: 1, 8896: 6},
      f"total={c2763_total} per-line={c2763_lines}")

c2762_total = text.count("c2762")
c2762_lines = {i + 1: l.count("c2762") for i, l in enumerate(lines) if "c2762" in l}
guard("c2762_mention_census_pre",
      c2762_total == 51
      and c2762_lines == {8860: 1, 8864: 2, 8872: 4, 8875: 1, 8876: 5, 8877: 6,
                          8882: 1, 8884: 6, 8886: 6, 8888: 8, 8889: 7, 8890: 1,
                          8894: 1, 8896: 2},
      f"total={c2762_total} per-line={c2762_lines}")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (48 at guard time: 46 at the c2763 "
          f"guard + 2 during the c2763 window; the official c2763 capture was the "
          f"latency-matched 1704ms render)")
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
head_is_official = head_body.startswith("c2763:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2763_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2763_commit", parent_body.startswith("c2763:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2763 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/7b9e5f3/519471c precedent)")
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

C2763_SET = [
    "rebadge_cycle2763.py", "capture_cycle2763.sh", "measure_c2763_tokens.py",
    "recursive_diff_2763.py", "validate_cycle2763.py", "entry_cycle2763.txt",
    "append_cycle2763.py", "scan_cycle2763_raw.json", "scan_cycle2763.json",
]
print("c2763_instrument_set_object_presence:")
missing = []
for name in C2763_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2763 files on disk")

v63 = open("/home/z/my-project/scripts/validate_cycle2763.py", "rb").read()
guard("v63_source_intact", b"CYCLE = 2763" in v63 and b"drift49_pass12_match" in v63
      and b"drift49_pass13_match" not in v63
      and b"(18,0,0,18,0)" in v63 and b"(20,0,2,18,0)" in v63
      and b"(21,0,3,18,0)" in v63,
      f"bytes={len(v63)} (the v63 pass-12 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-13 gate name drift49_pass13_match is what the v64 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "47d8243:scripts/validate_cycle2763.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v63_commit_object_intact", len(obj.stdout) == len(v63)
          and obj.stdout == v63,
          f"object_bytes={len(obj.stdout)} == disk {len(v63)} (the 47d8243 c2763 commit)")
else:
    guard("v63_commit_object_intact", False, "47d8243 object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
