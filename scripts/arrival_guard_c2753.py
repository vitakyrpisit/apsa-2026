#!/usr/bin/env python3
"""Arrival-guard for cycle 2753 (Job ID 446189) — measured, never predicted.

Spec source: the c2752 Next-block (worklog line 8764). Checks:
  worklog 8764 lines EXACT (newline count, c2752 append post-guard prophecy);
  tail = the c2753 Next bullet;
  anchors ^Task ID: 430 / ^- No gold yet 363 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2753 entries; c2753/c2754 substring accounting
  (the c2753/c2754 token-guard lives INSIDE the c2752 Next-block itself —
  the c2752 attempt-1 guard-slip lesson carried: per-line census first);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752 attempt-1 lesson: the HEAD check needs the parent
  layer — HEAD may be the official c2752 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2752 instrument set object-present (the LOSS-#83 lesson: verify FIRST).
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
guard("worklog_lines==8764", n_nl == 8764, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2753_next_bullet", last_nonempty.startswith("- Next: the c2753 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==430", tid == 430, f"got={tid}")
guard("anchor_nogold==363", gold == 363, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2753")]
guard("dup_check_zero_serviced_c2753", len(dup) == 0, f"got={len(dup)}")
c2753_total = text.count("c2753")
c2754_total = text.count("c2754")
tok_guard = [l for l in lines if "c2753/c2754" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2753 instance")]
c2753_lines = {i + 1: l.count("c2753") for i, l in enumerate(lines) if "c2753" in l}
guard("c2753_mention_accounting_pre",
      c2753_total == 6 and c2754_total == 1 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2753_lines == {8752: 1, 8756: 1, 8764: 4},
      f"total={c2753_total} c2754={c2754_total} per-line={c2753_lines} "
      f"(expect 6 = 1 in the c2751 Next-block line 8752 [the c2752/c2753 "
      f"token-guard] + 1 in the c2752 Step-1 line 8756 [the same guard "
      f"quoted] + 4 in the c2752 Next-block line 8764 — which is itself "
      f"the c2753/c2754 token-guard)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (c2752 guard measured 18)")
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
head_is_official = head_body.startswith("c2752:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2752_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2752_commit", parent_body.startswith("c2752:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2752 commit — the b6a94e3/c208995 precedent)")
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

C2752_SET = [
    "rebadge_cycle2752.py", "capture_cycle2752.sh", "measure_c2752_tokens.py",
    "recursive_diff_2752.py", "validate_cycle2752.py", "entry_cycle2752.txt",
    "append_cycle2752.py", "scan_cycle2752_raw.json", "scan_cycle2752.json",
]
print("c2752_instrument_set_object_presence:")
missing = []
for name in C2752_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2752 files on disk")

v52 = open("/home/z/my-project/scripts/validate_cycle2752.py", "rb").read()
guard("v52_source_intact", b"CYCLE = 2752" in v52 and b"drift48_ver4_match" in v52
      and b"(20,0,2,18,0)" in v52 and b"(18,0,0,18,0)" not in v52,
      f"bytes={len(v52)} (the v52 verification-4 class carries ONLY the LOCKED "
      f"root (20,0,2,18,0); the pass-1 observation (18,0,0,18,0) lives in the "
      f"worklog + response bytes, NOT in the v52 source — attempt-1 RED was a "
      f"guard-spec slip on exactly this literal, zero ledger anomalies)")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
