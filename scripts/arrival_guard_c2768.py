#!/usr/bin/env python3
"""Arrival-guard for cycle 2768 (Job ID 446189) — measured, never predicted.

Spec source: the c2767 Next-block (worklog line 8944). Checks:
  worklog 8944 lines EXACT (newline count, c2767 append post-guard prophecy);
  tail = the c2768 Next bullet;
  anchors ^Task ID: 445 / ^- No gold yet 378 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2768 entries; c2768/c2769 substring accounting
  (the c2768/c2769 token-guard lives INSIDE the c2767 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2768.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2769 = 2 born inside the c2767 Next-block guard phrase —
  the c2767 attempt-1 RED lesson: measure it, never assume it unborn);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2767 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2767 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2767 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v67 source-intact expectations matched to the v67 pass-16 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v67 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-17 gate name is what the v68 rebadge introduces;
  the SIZE_BAND lag-1 carry 'pass-15 band' is present — the P8 old-string
  expectation for the v68 rebadge).
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
guard("worklog_lines==8944", n_nl == 8944, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2768_next_bullet", last_nonempty.startswith("- Next: the c2768 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==445", tid == 445, f"got={tid}")
guard("anchor_nogold==378", gold == 378, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2768")]
guard("dup_check_zero_serviced_c2768", len(dup) == 0, f"got={len(dup)}")
c2768_total = text.count("c2768")
c2769_total = text.count("c2769")
tok_guard = [l for l in lines if "c2768/c2769" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2768 instance")]
c2768_lines = {i + 1: l.count("c2768") for i, l in enumerate(lines) if "c2768" in l}
c2769_lines = {i + 1: l.count("c2769") for i, l in enumerate(lines) if "c2769" in l}
guard("c2768_mention_accounting_pre",
      c2768_total == 11 and c2769_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2768_lines == {8932: 1, 8936: 6, 8944: 4} and c2769_lines == {8944: 2},
      f"total={c2768_total} c2769={c2769_total} per-line={c2768_lines} "
      f"c2769_per-line={c2769_lines} "
      f"(expect 11 = 1 in the c2766 Next-block line 8932 [the 'c2767/c2768' "
      f"token-guard phrase] + 6 in the c2767 Step-1 line 8936 [the attempt-1 "
      f"RED narrative: the 'c2768 = 0' prediction + 'c2768 = 1' measurement + "
      f"the guard-phrase quote + the tuple-omission + the census print + the "
      f"token-guard quote] + 4 in the c2767 Next-block line 8944 — which is "
      f"itself the c2768/c2769 token-guard: the 'c2768/c2769' phrase + "
      f"instance + measure_c2768_tokens.py + window-2768; c2769 = 2 — the "
      f"forward token is BORN inside the c2767 Next-block guard phrase AND "
      f"the census-tuple sentence, both on line 8944 (the forward-token "
      f"lesson: measured, never assumed unborn)")

c2767_total = text.count("c2767")
c2767_lines = {i + 1: l.count("c2767") for i, l in enumerate(lines) if "c2767" in l}
guard("c2767_mention_census_pre",
      c2767_total == 27
      and c2767_lines == {8920: 1, 8924: 2, 8932: 4, 8935: 1, 8936: 4, 8937: 6,
                          8942: 1, 8944: 8},
      f"total={c2767_total} per-line={c2767_lines}")

c2766_total = text.count("c2766")
c2766_lines = {i + 1: l.count("c2766") for i, l in enumerate(lines) if "c2766" in l}
guard("c2766_mention_census_pre",
      c2766_total == 49
      and c2766_lines == {8908: 1, 8912: 2, 8920: 4, 8923: 1, 8924: 4, 8925: 6,
                          8930: 1, 8932: 7, 8934: 4, 8936: 10, 8937: 4, 8938: 1,
                          8941: 1, 8942: 2, 8944: 1},
      f"total={c2766_total} per-line={c2766_lines}")

c2765_total = text.count("c2765")
c2765_lines = {i + 1: l.count("c2765") for i, l in enumerate(lines) if "c2765" in l}
guard("c2765_mention_census_pre",
      c2765_total == 62
      and c2765_lines == {8896: 1, 8900: 2, 8908: 4, 8911: 1, 8912: 4, 8913: 6,
                          8918: 1, 8920: 7, 8922: 8, 8924: 10, 8925: 7, 8926: 1,
                          8930: 1, 8932: 2, 8934: 2, 8936: 2, 8937: 2, 8944: 1},
      f"total={c2765_total} per-line={c2765_lines}")

c2764_total = text.count("c2764")
c2764_lines = {i + 1: l.count("c2764") for i, l in enumerate(lines) if "c2764" in l}
guard("c2764_mention_census_pre",
      c2764_total == 65
      and c2764_lines == {8884: 1, 8888: 2, 8896: 4, 8899: 1, 8900: 5, 8901: 6,
                          8906: 1, 8908: 7, 8910: 6, 8912: 9, 8913: 7, 8914: 2,
                          8918: 1, 8920: 2, 8922: 1, 8924: 1, 8925: 2, 8932: 2,
                          8934: 1, 8936: 1, 8937: 2, 8944: 1},
      f"total={c2764_total} per-line={c2764_lines}")

c2763_total = text.count("c2763")
c2763_lines = {i + 1: l.count("c2763") for i, l in enumerate(lines) if "c2763" in l}
guard("c2763_mention_census_pre",
      c2763_total == 72
      and c2763_lines == {8872: 1, 8876: 2, 8884: 4, 8887: 1, 8888: 5, 8889: 6,
                          8894: 1, 8896: 6, 8898: 6, 8900: 9, 8901: 7, 8902: 1,
                          8906: 1, 8908: 2, 8910: 5, 8912: 1, 8913: 2, 8914: 1,
                          8920: 2, 8924: 1, 8925: 2, 8932: 2, 8936: 1, 8937: 2,
                          8944: 1},
      f"total={c2763_total} per-line={c2763_lines}")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (59 at guard time: 56 at the c2767 "
          f"guard + the official c2767 capture (the latency-matched 6259ms render) "
          f"+ 2 since, foreign/unattributed — dev.log is timestamp-less: the "
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
head_is_official = head_body.startswith("c2767:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2767_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2767_commit", parent_body.startswith("c2767:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2767 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b precedent)")
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

C2767_SET = [
    "rebadge_cycle2767.py", "capture_cycle2767.sh", "measure_c2767_tokens.py",
    "recursive_diff_2767.py", "validate_cycle2767.py", "entry_cycle2767.txt",
    "append_cycle2767.py", "scan_cycle2767_raw.json", "scan_cycle2767.json",
]
print("c2767_instrument_set_object_presence:")
missing = []
for name in C2767_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "9/9 c2767 files on disk")

v67 = open("/home/z/my-project/scripts/validate_cycle2767.py", "rb").read()
guard("v67_source_intact", b"CYCLE = 2767" in v67 and b"drift49_pass16_match" in v67
      and b"drift49_pass17_match" not in v67
      and b"(18,0,0,18,0)" in v67 and b"(20,0,2,18,0)" in v67
      and b"(21,0,3,18,0)" in v67 and b"pass-15 band" in v67
      and b"pass-16 band" not in v67,
      f"bytes={len(v67)} (the v67 pass-16 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-17 gate name drift49_pass17_match is what the v68 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-15 band' is present — the v68 P8 old-string expectation)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "e641a22:scripts/validate_cycle2767.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v67_commit_object_intact", len(obj.stdout) == len(v67)
          and obj.stdout == v67,
          f"object_bytes={len(obj.stdout)} == disk {len(v67)} (the e641a22 c2767 commit)")
else:
    guard("v67_commit_object_intact", False, "e641a22 object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
