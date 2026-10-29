#!/usr/bin/env python3
"""Arrival-guard for cycle 2780 (Job ID 446189) — measured, never predicted.

Spec source: the c2779 Next-block (worklog line 9088). Checks:
  worklog 9088 lines EXACT (newline count, c2779 append post-guard prophecy);
  tail = the c2780 Next bullet;
  anchors ^Task ID: 457 / ^- No gold yet 390 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2780 entries; c2780/c2781 substring accounting
  (the c2780/c2781 token-guard lives INSIDE the c2779 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2780.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2781 = 2 born inside the c2779 Next-block guard phrase AND
  census-tuple sentence — the c2767..c2780 forward-token lessons:
  measure it, never assume it unborn);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2779 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2779 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2779 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v79 source-intact expectations matched to the v79 pass-28 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v79 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-29 gate name is what the v80 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-27 band' is present AND the evidence-paragraph lag-1 heading
  'pass-27 evidence' is present — BOTH instrument surfaces, the v80 rebadge
  P3/P8 old-string expectations, exactly as the c2779 Next-block wrote).
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
guard("worklog_lines==9088", n_nl == 9088, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2780_next_bullet", last_nonempty.startswith("- Next: the c2780 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==457", tid == 457, f"got={tid}")
guard("anchor_nogold==390", gold == 390, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2780")]
guard("dup_check_zero_serviced_c2780", len(dup) == 0, f"got={len(dup)}")
c2780_total = text.count("c2780")
c2781_total = text.count("c2781")
tok_guard = [l for l in lines if "c2780/c2781" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2780 instance")]
c2780_lines = {i + 1: l.count("c2780") for i, l in enumerate(lines) if "c2780" in l}
c2781_lines = {i + 1: l.count("c2781") for i, l in enumerate(lines) if "c2781" in l}
guard("c2780_mention_accounting_pre",
      c2780_total == 8 and c2781_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2780_lines == {9076: 2, 9080: 2, 9088: 4} and c2781_lines == {9088: 2},
      f"total={c2780_total} c2781={c2781_total} per-line={c2780_lines} "
      f"c2781_per-line={c2781_lines} "
      f"(expect 8 = 2 in the c2778 Next-block line 9076 [the c2779/c2780 "
      f"token-guard phrase + the measure_c2780/window phrasing] + 2 in the c2779 "
      f"Step-1 line 9080 [the census-tuple print '+ c2780 = 2' + the c2779/c2780 "
      f"phrase] + 4 in the c2779 Next-block line 9088 — which is itself the "
      f"c2780/c2781 token-guard: the instance + id + 'c2780/c2781' phrase + "
      f"measure_c2780_tokens.py + the pass-28-state phrasing; c2781 = 2 — the "
      f"forward token is BORN inside the c2779 Next-block guard phrase AND "
      f"the census-tuple sentence, both on line 9088 (the forward-token "
      f"lesson: measured, never assumed unborn))")

c2779_total = text.count("c2779")
c2779_lines = {i + 1: l.count("c2779") for i, l in enumerate(lines) if "c2779" in l}
guard("c2779_mention_census_pre",
      c2779_total == 33
      and c2779_lines == {9064: 2, 9068: 2, 9076: 4, 9079: 1, 9080: 4, 9081: 7,
                          9086: 4, 9088: 9},
      f"total={c2779_total} per-line={c2779_lines}")

c2778_total = text.count("c2778")
c2778_lines = {i + 1: l.count("c2778") for i, l in enumerate(lines) if "c2778" in l}
guard("c2778_mention_census_pre",
      c2778_total == 72
      and c2778_lines == {9052: 2, 9056: 3, 9064: 5, 9067: 1, 9068: 4, 9069: 7,
                          9074: 3, 9076: 9, 9078: 6, 9080: 12, 9081: 6, 9082: 4,
                          9085: 1, 9086: 6, 9088: 3},
      f"total={c2778_total} per-line={c2778_lines}")

c2777_total = text.count("c2777")
c2777_lines = {i + 1: l.count("c2777") for i, l in enumerate(lines) if "c2777" in l}
guard("c2777_mention_census_pre",
      c2777_total == 73
      and c2777_lines == {9040: 2, 9044: 3, 9052: 5, 9055: 1, 9056: 4, 9057: 7,
                          9062: 3, 9064: 9, 9066: 7, 9068: 12, 9069: 6, 9070: 2,
                          9073: 2, 9074: 1, 9076: 2, 9078: 1, 9080: 2, 9081: 2,
                          9088: 2},
      f"total={c2777_total} per-line={c2777_lines}")

c2776_total = text.count("c2776")
c2776_lines = {i + 1: l.count("c2776") for i, l in enumerate(lines) if "c2776" in l}
guard("c2776_mention_census_pre",
      c2776_total == 78
      and c2776_lines == {9028: 2, 9032: 3, 9040: 5, 9043: 1, 9044: 4, 9045: 7,
                          9050: 3, 9052: 9, 9054: 7, 9056: 13, 9057: 6, 9058: 2,
                          9061: 1, 9062: 2, 9064: 2, 9066: 1, 9068: 1, 9069: 2,
                          9076: 2, 9080: 1, 9081: 2, 9088: 2},
      f"total={c2776_total} per-line={c2776_lines}")

c2775_total = text.count("c2775")
c2775_lines = {i + 1: l.count("c2775") for i, l in enumerate(lines) if "c2775" in l}
guard("c2775_mention_census_pre",
      c2775_total == 87
      and c2775_lines == {9016: 2, 9020: 3, 9028: 5, 9031: 1, 9032: 4, 9033: 7,
                          9038: 3, 9040: 9, 9042: 8, 9044: 12, 9045: 6, 9046: 2,
                          9049: 3, 9050: 2, 9052: 2, 9054: 1, 9056: 2, 9057: 2,
                          9061: 1, 9064: 2, 9068: 1, 9069: 2, 9076: 2, 9080: 1,
                          9081: 2, 9088: 2},
      f"total={c2775_total} per-line={c2775_lines}")

c2774_total = text.count("c2774")
c2774_lines = {i + 1: l.count("c2774") for i, l in enumerate(lines) if "c2774" in l}
guard("c2774_mention_census_pre",
      c2774_total == 92
      and c2774_lines == {9004: 2, 9008: 3, 9016: 5, 9019: 1, 9020: 4, 9021: 7,
                          9026: 3, 9028: 9, 9030: 9, 9032: 12, 9033: 6, 9034: 2,
                          9037: 3, 9038: 1, 9040: 2, 9042: 1, 9044: 1, 9045: 2,
                          9049: 2, 9052: 2, 9056: 1, 9057: 2, 9064: 2, 9068: 1,
                          9069: 2, 9076: 2, 9080: 1, 9081: 2, 9088: 2},
      f"total={c2774_total} per-line={c2774_lines}")

c2773_total = text.count("c2773")
c2773_lines = {i + 1: l.count("c2773") for i, l in enumerate(lines) if "c2773" in l}
guard("c2773_mention_census_pre",
      c2773_total == 96
      and c2773_lines == {8992: 2, 8996: 3, 9004: 5, 9007: 1, 9008: 3, 9009: 7,
                          9014: 3, 9016: 9, 9018: 10, 9020: 11, 9021: 6, 9022: 2,
                          9025: 4, 9026: 1, 9028: 2, 9030: 1, 9032: 1, 9033: 2,
                          9037: 1, 9040: 2, 9044: 1, 9045: 2, 9052: 2, 9056: 1,
                          9057: 2, 9064: 2, 9068: 1, 9069: 2, 9076: 2, 9080: 1,
                          9081: 2, 9088: 2},
      f"total={c2773_total} per-line={c2773_lines}")

c2772_total = text.count("c2772")
c2772_lines = {i + 1: l.count("c2772") for i, l in enumerate(lines) if "c2772" in l}
guard("c2772_mention_census_pre",
      c2772_total == 107
      and c2772_lines == {8980: 2, 8984: 2, 8992: 4, 8995: 1, 8996: 3, 8997: 7,
                          9002: 3, 9004: 9, 9006: 7, 9008: 12, 9009: 6, 9010: 2,
                          9013: 2, 9014: 1, 9016: 3, 9018: 2, 9020: 2, 9021: 2,
                          9025: 2, 9028: 3, 9032: 1, 9033: 2, 9040: 3, 9044: 1,
                          9045: 2, 9052: 3, 9056: 1, 9057: 2, 9064: 3, 9068: 2,
                          9069: 2, 9076: 3, 9080: 2, 9081: 2, 9088: 3},
      f"total={c2772_total} per-line={c2772_lines}")

c2771_total = text.count("c2771")
c2771_lines = {i + 1: l.count("c2771") for i, l in enumerate(lines) if "c2771" in l}
guard("c2771_mention_census_pre",
      c2771_total == 105
      and c2771_lines == {8968: 2, 8972: 2, 8980: 4, 8983: 1, 8984: 3, 8985: 6,
                          8990: 3, 8992: 8, 8994: 7, 8996: 12, 8997: 5, 8998: 2,
                          9001: 1, 9002: 1, 9004: 3, 9006: 3, 9008: 3, 9009: 2,
                          9010: 1, 9013: 4, 9016: 2, 9020: 1, 9021: 2, 9028: 2,
                          9032: 1, 9033: 2, 9040: 2, 9044: 1, 9045: 2, 9052: 2,
                          9056: 1, 9057: 2, 9064: 2, 9068: 1, 9069: 2, 9076: 2,
                          9080: 1, 9081: 2, 9088: 2},
      f"total={c2771_total} per-line={c2771_lines}")

c2770_total = text.count("c2770")
c2770_lines = {i + 1: l.count("c2770") for i, l in enumerate(lines) if "c2770" in l}
guard("c2770_mention_census_pre",
      c2770_total == 126
      and c2770_lines == {8956: 2, 8960: 2, 8968: 4, 8971: 1, 8972: 3, 8973: 6,
                          8978: 2, 8980: 9, 8982: 7, 8984: 12, 8985: 5, 8986: 2,
                          8989: 2, 8990: 1, 8992: 4, 8994: 3, 8996: 3, 8997: 3,
                          9001: 3, 9004: 4, 9006: 1, 9008: 3, 9009: 3, 9013: 2,
                          9016: 3, 9020: 1, 9021: 2, 9028: 3, 9032: 1, 9033: 2,
                          9040: 3, 9044: 1, 9045: 2, 9052: 3, 9056: 1, 9057: 2,
                          9064: 3, 9068: 1, 9069: 2, 9076: 3, 9080: 1, 9081: 2,
                          9088: 3},
      f"total={c2770_total} per-line={c2770_lines}")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (93 at the c2779 guard: 91 at the "
          f"c2779 census + the in-batch loop-open echo + 1 since, foreign; then the "
          f"official c2779 capture +1 and the c2780 loop-open echo +1 and further "
          f"foreign entries since — dev.log is timestamp-less: the official/foreign "
          f"split is by latency-match, honest, no over-claim; the in-batch loop-open "
          f"echo of THIS batch adds +1 after this print)")
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
head_is_official = head_body.startswith("c2779:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2779_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2779_commit", parent_body.startswith("c2779:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2779 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb precedent)")
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

C2779_SET = [
    "census_c2779.py", "arrival_guard_c2779.py", "rebadge_cycle2779.py",
    "capture_cycle2779.sh", "measure_c2779_tokens.py", "recursive_diff_2779.py",
    "validate_cycle2779.py", "entry_cycle2779.txt", "append_cycle2779.py",
    "scan_cycle2779_raw.json", "scan_cycle2779.json",
]
print("c2779_instrument_set_object_presence:")
missing = []
for name in C2779_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2779 files on disk")

v79 = open("/home/z/my-project/scripts/validate_cycle2779.py", "rb").read()
guard("v79_source_intact", b"CYCLE = 2779" in v79 and b"drift49_pass28_match" in v79
      and b"drift49_pass29_match" not in v79
      and b"(18,0,0,18,0)" in v79 and b"(20,0,2,18,0)" in v79
      and b"(21,0,3,18,0)" in v79 and b"pass-27 band" in v79
      and b"pass-28 band" not in v79
      and b"pass-27 evidence" in v79 and b"pass-28 evidence" not in v79,
      f"bytes={len(v79)} (the v79 pass-28 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-29 gate name drift49_pass29_match is what the v80 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-27 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-27 evidence' is present — BOTH instrument surfaces, the v80 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "d5acf5e:scripts/validate_cycle2779.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v79_commit_object_intact", len(obj.stdout) == len(v79)
          and obj.stdout == v79,
          f"object_bytes={len(obj.stdout)} == disk {len(v79)} (the d5acf5e c2779 commit)")
else:
    guard("v79_commit_object_intact", False, "d5acf5e object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
