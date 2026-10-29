#!/usr/bin/env python3
"""Arrival-guard for cycle 2752 (Job ID 446189) — measured, never predicted.

Spec source: the c2751 Next-block (worklog line 8752). Checks:
  worklog 8752 lines EXACT (newline count, c2751 append post-guard prophecy);
  tail = the c2752 Next bullet;
  anchors ^Task ID: 429 / ^- No gold yet 362 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2752 entries; c2752 substring accounting;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification (body prefix 'c2751:') + foreign-commit census;
  c2751 instrument set object-present (the LOSS-#83 lesson: object-verify FIRST).
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
guard("worklog_lines==8752", n_nl == 8752, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2752_next_bullet", last_nonempty.startswith("- Next: the c2752 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==429", tid == 429, f"got={tid}")
guard("anchor_nogold==362", gold == 362, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2752")]
guard("dup_check_zero_serviced_c2752", len(dup) == 0, f"got={len(dup)}")
c2752_total = text.count("c2752")
tok_guard = [l for l in lines if "c2752/c2753" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2752 instance")]
c2752_lines = {i + 1: l.count("c2752") for i, l in enumerate(lines) if "c2752" in l}
guard("c2752_mention_accounting_pre",
      c2752_total == 5 and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and next_block[0].count("c2752") == 4
      and c2752_lines == {8740: 1, 8752: 4},
      f"total={c2752_total} per-line={c2752_lines} (expect 5 = 4 in the c2751 "
      f"Next-block line 8752 — which is itself the c2752/c2753 token-guard — "
      f"+ 1 'c2751/c2752' token-guard in the c2750 Next-block line 8740)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (c2751 guard measured 14)")
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
head_is_foreign = head_subj.endswith("-cron") and not head_body.startswith("c2751:")
guard("git_parent_is_c2751_commit", parent_body.startswith("c2751:"),
      f"parent={parent_short} body[:40]={parent_body[:40]!r}")
guard("git_head_foreign_class", head_is_foreign,
      f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add class atop the c2751 commit — the dd1ae9d/113dbc1 precedent)")
head_stat = git("show", "--stat", "--format=", head_short)
n_files = len([l for l in head_stat.splitlines() if l.strip()])
touched = [l for l in head_stat.splitlines() if "worklog" in l or "scripts/" in l and "pyc" not in l]
guard("git_head_zero_ledger_touch", "worklog.md" not in head_stat,
      f"foreign commit touches {n_files} file entries; worklog touched={'worklog.md' in head_stat}")
print(f"foreign_commit_stat_tail: {head_stat.splitlines()[-1] if head_stat else '(empty)'}")
recent = git("log", "-3", "--format=%h %s")
print("recent_commits:")
for ln in recent.splitlines():
    print(f"  {ln[:120]}")
status = git("status", "--short")
print(f"working_tree_entries={len(status.splitlines()) if status else 0}")

C2751_SET = [
    "rebadge_cycle2751.py", "capture_cycle2751.sh", "measure_c2751_tokens.py",
    "recursive_diff_2751.py", "validate_cycle2751.py", "entry_cycle2751.txt",
    "append_cycle2751.py", "scan_cycle2751_raw.json", "scan_cycle2751.json",
]
print("c2751_instrument_set_object_presence:")
missing = []
for name in C2751_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2751 files on disk")

v51 = open("/home/z/my-project/scripts/validate_cycle2751.py", "rb").read()
guard("v51_source_intact", b"CYCLE = 2751" in v51 and b"drift48_ver3_match" in v51
      and b"(20,0,2,18,0)" in v51,
      f"bytes={len(v51)}")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
