#!/usr/bin/env python3
"""Arrival-guard for cycle 2760 (Job ID 446189) — measured, never predicted.

Spec source: the c2759 Next-block (worklog line 8848). Checks:
  worklog 8848 lines EXACT (newline count, c2759 append post-guard prophecy);
  tail = the c2760 Next bullet;
  anchors ^Task ID: 437 / ^- No gold yet 370 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2760 entries; c2760/c2761 substring accounting
  (the c2760/c2761 token-guard lives INSIDE the c2759 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2760.py, expectations below are the MEASURED values);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2759 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2759 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2759 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v59 source-intact expectations matched to the v59 pass-8 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v59 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-9 gate name is what the v60 rebadge introduces).
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
guard("worklog_lines==8848", n_nl == 8848, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2760_next_bullet", last_nonempty.startswith("- Next: the c2760 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==437", tid == 437, f"got={tid}")
guard("anchor_nogold==370", gold == 370, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2760")]
guard("dup_check_zero_serviced_c2760", len(dup) == 0, f"got={len(dup)}")
c2760_total = text.count("c2760")
c2761_total = text.count("c2761")
tok_guard = [l for l in lines if "c2760/c2761" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2760 instance")]
c2760_lines = {i + 1: l.count("c2760") for i, l in enumerate(lines) if "c2760" in l}
guard("c2760_mention_accounting_pre",
      c2760_total == 7 and c2761_total == 1 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2760_lines == {8836: 1, 8840: 2, 8848: 4},
      f"total={c2760_total} c2761={c2761_total} per-line={c2760_lines} "
      f"(expect 7 = 1 in the c2758 Next-block line 8836 [the c2759/c2760 "
      f"token-guard] + 2 in the c2759 Step-1 line 8840 [the same guard "
      f"quoted + the '+ c2760 = 1' accounting] + 4 in the c2759 Next-block "
      f"line 8848 — which is itself the c2760/c2761 token-guard)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (37 at the c2759 close; 1 MORE foreign since "
          f"[the 1769ms render class]; the official c2760 capture is the post-guard "
          f"39th-class render)")
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
head_is_official = head_body.startswith("c2759:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2759_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2759_commit", parent_body.startswith("c2759:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2759 commit — the d990e91/5712edd/dc1c551 precedent)")
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

C2759_SET = [
    "rebadge_cycle2759.py", "capture_cycle2759.sh", "measure_c2759_tokens.py",
    "recursive_diff_2759.py", "validate_cycle2759.py", "entry_cycle2759.txt",
    "append_cycle2759.py", "scan_cycle2759_raw.json", "scan_cycle2759.json",
]
print("c2759_instrument_set_object_presence:")
missing = []
for name in C2759_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2759 files on disk")

v59 = open("/home/z/my-project/scripts/validate_cycle2759.py", "rb").read()
guard("v59_source_intact", b"CYCLE = 2759" in v59 and b"drift49_pass8_match" in v59
      and b"drift49_pass9_match" not in v59
      and b"(18,0,0,18,0)" in v59 and b"(20,0,2,18,0)" in v59
      and b"(21,0,3,18,0)" in v59,
      f"bytes={len(v59)} (the v59 pass-8 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-9 gate name drift49_pass9_match is what the v60 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "b867cb7:scripts/validate_cycle2759.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v59_commit_object_intact", len(obj.stdout) == len(v59)
          and obj.stdout == v59,
          f"object_bytes={len(obj.stdout)} == disk {len(v59)} (the b867cb7 c2759 commit)")
else:
    guard("v59_commit_object_intact", False, "b867cb7 object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
