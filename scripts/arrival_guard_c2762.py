#!/usr/bin/env python3
"""Arrival-guard for cycle 2762 (Job ID 446189) — measured, never predicted.

Spec source: the c2761 Next-block (worklog line 8872). Checks:
  worklog 8872 lines EXACT (newline count, c2761 append post-guard prophecy);
  tail = the c2762 Next bullet;
  anchors ^Task ID: 439 / ^- No gold yet 372 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2762 entries; c2762/c2763 substring accounting
  (the c2762/c2763 token-guard lives INSIDE the c2761 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2762.py, expectations below are the MEASURED values);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2761 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2761 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2761 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v61 source-intact expectations matched to the v61 pass-10 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v61 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-11 gate name is what the v62 rebadge introduces).
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
guard("worklog_lines==8872", n_nl == 8872, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2762_next_bullet", last_nonempty.startswith("- Next: the c2762 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==439", tid == 439, f"got={tid}")
guard("anchor_nogold==372", gold == 372, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2762")]
guard("dup_check_zero_serviced_c2762", len(dup) == 0, f"got={len(dup)}")
c2762_total = text.count("c2762")
c2763_total = text.count("c2763")
tok_guard = [l for l in lines if "c2762/c2763" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2762 instance")]
c2762_lines = {i + 1: l.count("c2762") for i, l in enumerate(lines) if "c2762" in l}
guard("c2762_mention_accounting_pre",
      c2762_total == 7 and c2763_total == 1 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2762_lines == {8860: 1, 8864: 2, 8872: 4},
      f"total={c2762_total} c2763={c2763_total} per-line={c2762_lines} "
      f"(expect 7 = 1 in the c2760 Next-block line 8860 [the "
      f"measure_c2762_tokens.py birth] + 2 in the c2761 Step-1 line 8864 [the "
      f"c2761-guard output quote '+ c2762 = 1' + the 'c2761/c2762 token-guard' "
      f"phrase] + 4 in the c2761 Next-block line 8872 — which is itself the "
      f"c2762/c2763 token-guard)")

c2761_total = text.count("c2761")
c2761_lines = {i + 1: l.count("c2761") for i, l in enumerate(lines) if "c2761" in l}
guard("c2761_mention_census_pre",
      c2761_total == 30
      and c2761_lines == {8848: 1, 8852: 2, 8860: 4, 8863: 1, 8864: 5, 8865: 8,
                          8870: 1, 8872: 8},
      f"total={c2761_total} per-line={c2761_lines}")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (43 at the c2761 close; the official "
          f"c2761 capture was the latency-matched 2140ms render)")
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
head_is_official = head_body.startswith("c2761:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2761_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2761_commit", parent_body.startswith("c2761:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2761 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea precedent)")
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

C2761_SET = [
    "rebadge_cycle2761.py", "capture_cycle2761.sh", "measure_c2761_tokens.py",
    "recursive_diff_2761.py", "validate_cycle2761.py", "entry_cycle2761.txt",
    "append_cycle2761.py", "scan_cycle2761_raw.json", "scan_cycle2761.json",
]
print("c2761_instrument_set_object_presence:")
missing = []
for name in C2761_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2761 files on disk")

v61 = open("/home/z/my-project/scripts/validate_cycle2761.py", "rb").read()
guard("v61_source_intact", b"CYCLE = 2761" in v61 and b"drift49_pass10_match" in v61
      and b"drift49_pass11_match" not in v61
      and b"(18,0,0,18,0)" in v61 and b"(20,0,2,18,0)" in v61
      and b"(21,0,3,18,0)" in v61,
      f"bytes={len(v61)} (the v61 pass-10 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-11 gate name drift49_pass11_match is what the v62 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "d3b1054:scripts/validate_cycle2761.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v61_commit_object_intact", len(obj.stdout) == len(v61)
          and obj.stdout == v61,
          f"object_bytes={len(obj.stdout)} == disk {len(v61)} (the d3b1054 c2761 commit)")
else:
    guard("v61_commit_object_intact", False, "d3b1054 object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
