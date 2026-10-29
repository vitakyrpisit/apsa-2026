#!/usr/bin/env python3
"""Arrival-guard for cycle 2757 (Job ID 446189) — measured, never predicted.

Spec source: the c2756 Next-block (worklog line 8812). Checks:
  worklog 8812 lines EXACT (newline count, c2756 append post-guard prophecy);
  tail = the c2757 Next bullet;
  anchors ^Task ID: 434 / ^- No gold yet 367 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2757 entries; c2757/c2758 substring accounting
  (the c2757/c2758 token-guard lives INSIDE the c2756 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2757.py, expectations below are the MEASURED values);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2756 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2756 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2756 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v56 source-intact expectations matched to the v56 pass-5 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v56 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-6 gate name is what the v57 rebadge introduces).
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
guard("worklog_lines==8812", n_nl == 8812, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2757_next_bullet", last_nonempty.startswith("- Next: the c2757 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==434", tid == 434, f"got={tid}")
guard("anchor_nogold==367", gold == 367, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2757")]
guard("dup_check_zero_serviced_c2757", len(dup) == 0, f"got={len(dup)}")
c2757_total = text.count("c2757")
c2758_total = text.count("c2758")
tok_guard = [l for l in lines if "c2757/c2758" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2757 instance")]
c2757_lines = {i + 1: l.count("c2757") for i, l in enumerate(lines) if "c2757" in l}
guard("c2757_mention_accounting_pre",
      c2757_total == 7 and c2758_total == 1 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2757_lines == {8800: 1, 8804: 2, 8812: 4},
      f"total={c2757_total} c2758={c2758_total} per-line={c2757_lines} "
      f"(expect 7 = 1 in the c2755 Next-block line 8800 [the c2756/c2757 "
      f"token-guard] + 2 in the c2756 Step-1 line 8804 [the same guard "
      f"quoted + the '+ c2757 = 1' accounting] + 4 in the c2756 Next-block "
      f"line 8812 — which is itself the c2757/c2758 token-guard)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (c2756 guard measured 29; official c2756 capture = 30th; "
          f"31 at c2756 close; the official c2757 capture is the post-guard 33rd-class render)")
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
head_is_official = head_body.startswith("c2756:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2756_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2756_commit", parent_body.startswith("c2756:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2756 commit — the 95eaed7/bbba26b precedent)")
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

C2756_SET = [
    "rebadge_cycle2756.py", "capture_cycle2756.sh", "measure_c2756_tokens.py",
    "recursive_diff_2756.py", "validate_cycle2756.py", "entry_cycle2756.txt",
    "append_cycle2756.py", "scan_cycle2756_raw.json", "scan_cycle2756.json",
]
print("c2756_instrument_set_object_presence:")
missing = []
for name in C2756_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2756 files on disk")

v56 = open("/home/z/my-project/scripts/validate_cycle2756.py", "rb").read()
guard("v56_source_intact", b"CYCLE = 2756" in v56 and b"drift49_pass5_match" in v56
      and b"drift49_pass6_match" not in v56
      and b"(18,0,0,18,0)" in v56 and b"(20,0,2,18,0)" in v56
      and b"(21,0,3,18,0)" in v56,
      f"bytes={len(v56)} (the v56 pass-5 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-6 gate name drift49_pass6_match is what the v57 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "2848a78:scripts/validate_cycle2756.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v56_commit_object_intact", len(obj.stdout) == len(v56)
          and obj.stdout == v56,
          f"object_bytes={len(obj.stdout)} == disk {len(v56)} (the 2848a78 c2756 commit)")
else:
    guard("v56_commit_object_intact", False, "2848a78 object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
