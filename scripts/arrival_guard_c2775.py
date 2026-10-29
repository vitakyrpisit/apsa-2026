#!/usr/bin/env python3
"""Arrival-guard for cycle 2775 (Job ID 446189) — measured, never predicted.

Spec source: the c2774 Next-block (worklog line 9028). Checks:
  worklog 9028 lines EXACT (newline count, c2774 append post-guard prophecy);
  tail = the c2775 Next bullet;
  anchors ^Task ID: 452 / ^- No gold yet 385 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2775 entries; c2775/c2776 substring accounting
  (the c2775/c2776 token-guard lives INSIDE the c2774 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2775.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2776 = 2 born inside the c2774 Next-block guard phrase AND
  census-tuple sentence — the c2767..c2775 forward-token lessons:
  measure it, never assume it unborn);
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2774 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2774 commit OR a benign-add foreign
  cron commit ATOP it; both classes GREEN, the class printed honestly);
  c2774 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v74 source-intact expectations matched to the v74 pass-23 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v74 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-24 gate name is what the v75 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-22 band' is present AND the evidence-paragraph lag-1 heading
  'pass-22 evidence' is present — BOTH instrument surfaces, the v75 rebadge
  P3/P8 old-string expectations, exactly as the c2774 Next-block wrote).
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
guard("worklog_lines==9028", n_nl == 9028, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2775_next_bullet", last_nonempty.startswith("- Next: the c2775 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==452", tid == 452, f"got={tid}")
guard("anchor_nogold==385", gold == 385, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2775")]
guard("dup_check_zero_serviced_c2775", len(dup) == 0, f"got={len(dup)}")
c2775_total = text.count("c2775")
c2776_total = text.count("c2776")
tok_guard = [l for l in lines if "c2775/c2776" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2775 instance")]
c2775_lines = {i + 1: l.count("c2775") for i, l in enumerate(lines) if "c2775" in l}
c2776_lines = {i + 1: l.count("c2776") for i, l in enumerate(lines) if "c2776" in l}
guard("c2775_mention_accounting_pre",
      c2775_total == 10 and c2776_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2775_lines == {9016: 2, 9020: 3, 9028: 5} and c2776_lines == {9028: 2},
      f"total={c2775_total} c2776={c2776_total} per-line={c2775_lines} "
      f"c2776_per-line={c2776_lines} "
      f"(expect 10 = 2 in the c2773 Next-block line 9016 [the c2774/c2775 "
      f"token-guard phrase + the FORWARD-token sentence] + 3 in the c2774 "
      f"Step-1 line 9020 [the census-tuple print + the c2774/c2775 phrase + "
      f"the RE-AFFIRMED prescription] + 5 in the c2774 Next-block line 9028 — "
      f"which is itself the c2775/c2776 token-guard: the instance + id + "
      f"'c2775/c2776' phrase + measure_c2775_tokens.py + window-2775; c2776 = 2 "
      f"— the forward token is BORN inside the c2774 Next-block guard phrase "
      f"AND the census-tuple sentence, both on line 9028 (the forward-token "
      f"lesson: measured, never assumed unborn))")

c2774_total = text.count("c2774")
c2774_lines = {i + 1: l.count("c2774") for i, l in enumerate(lines) if "c2774" in l}
guard("c2774_mention_census_pre",
      c2774_total == 34
      and c2774_lines == {9004: 2, 9008: 3, 9016: 5, 9019: 1, 9020: 4, 9021: 7,
                          9026: 3, 9028: 9},
      f"total={c2774_total} per-line={c2774_lines}")

c2773_total = text.count("c2773")
c2773_lines = {i + 1: l.count("c2773") for i, l in enumerate(lines) if "c2773" in l}
guard("c2773_mention_census_pre",
      c2773_total == 69
      and c2773_lines == {8992: 2, 8996: 3, 9004: 5, 9007: 1, 9008: 3, 9009: 7,
                          9014: 3, 9016: 9, 9018: 10, 9020: 11, 9021: 6, 9022: 2,
                          9025: 4, 9026: 1, 9028: 2},
      f"total={c2773_total} per-line={c2773_lines}")

c2772_total = text.count("c2772")
c2772_lines = {i + 1: l.count("c2772") for i, l in enumerate(lines) if "c2772" in l}
guard("c2772_mention_census_pre",
      c2772_total == 75
      and c2772_lines == {8980: 2, 8984: 2, 8992: 4, 8995: 1, 8996: 3, 8997: 7,
                          9002: 3, 9004: 9, 9006: 7, 9008: 12, 9009: 6, 9010: 2,
                          9013: 2, 9014: 1, 9016: 3, 9018: 2, 9020: 2, 9021: 2,
                          9025: 2, 9028: 3},
      f"total={c2772_total} per-line={c2772_lines}")

c2771_total = text.count("c2771")
c2771_lines = {i + 1: l.count("c2771") for i, l in enumerate(lines) if "c2771" in l}
guard("c2771_mention_census_pre",
      c2771_total == 80
      and c2771_lines == {8968: 2, 8972: 2, 8980: 4, 8983: 1, 8984: 3, 8985: 6,
                          8990: 3, 8992: 8, 8994: 7, 8996: 12, 8997: 5, 8998: 2,
                          9001: 1, 9002: 1, 9004: 3, 9006: 3, 9008: 3, 9009: 2,
                          9010: 1, 9013: 4, 9016: 2, 9020: 1, 9021: 2, 9028: 2},
      f"total={c2771_total} per-line={c2771_lines}")

c2770_total = text.count("c2770")
c2770_lines = {i + 1: l.count("c2770") for i, l in enumerate(lines) if "c2770" in l}
guard("c2770_mention_census_pre",
      c2770_total == 96
      and c2770_lines == {8956: 2, 8960: 2, 8968: 4, 8971: 1, 8972: 3, 8973: 6,
                          8978: 2, 8980: 9, 8982: 7, 8984: 12, 8985: 5, 8986: 2,
                          8989: 2, 8990: 1, 8992: 4, 8994: 3, 8996: 3, 8997: 3,
                          9001: 3, 9004: 4, 9006: 1, 9008: 3, 9009: 3, 9013: 2,
                          9016: 3, 9020: 1, 9021: 2, 9028: 3},
      f"total={c2770_total} per-line={c2770_lines}")

c2769_total = text.count("c2769")
c2769_lines = {i + 1: l.count("c2769") for i, l in enumerate(lines) if "c2769" in l}
guard("c2769_mention_census_pre",
      c2769_total == 83
      and c2769_lines == {8944: 2, 8948: 2, 8956: 4, 8959: 1, 8960: 3, 8961: 6,
                          8966: 2, 8968: 8, 8970: 5, 8972: 11, 8973: 5, 8974: 1,
                          8978: 1, 8980: 2, 8982: 2, 8984: 2, 8985: 2, 8989: 1,
                          8992: 3, 8996: 3, 8997: 2, 9001: 1, 9004: 2, 9008: 2,
                          9009: 2, 9013: 1, 9016: 2, 9020: 1, 9021: 2, 9028: 2},
      f"total={c2769_total} per-line={c2769_lines}")

c2768_total = text.count("c2768")
c2768_lines = {i + 1: l.count("c2768") for i, l in enumerate(lines) if "c2768" in l}
guard("c2768_mention_census_pre",
      c2768_total == 87
      and c2768_lines == {8932: 1, 8936: 6, 8944: 4, 8947: 1, 8948: 3, 8949: 6,
                          8954: 2, 8956: 8, 8958: 5, 8960: 12, 8961: 4, 8962: 1,
                          8966: 1, 8968: 2, 8970: 1, 8972: 2, 8973: 2, 8980: 2,
                          8982: 1, 8984: 2, 8985: 2, 8992: 2, 8996: 2, 8997: 2,
                          9004: 2, 9008: 2, 9009: 2, 9016: 2, 9020: 1, 9021: 2,
                          9028: 2},
      f"total={c2768_total} per-line={c2768_lines}")

c2767_total = text.count("c2767")
c2767_lines = {i + 1: l.count("c2767") for i, l in enumerate(lines) if "c2767" in l}
guard("c2767_mention_census_pre",
      c2767_total == 93
      and c2767_lines == {8920: 1, 8924: 2, 8932: 4, 8935: 1, 8936: 4, 8937: 6,
                          8942: 1, 8944: 8, 8946: 6, 8948: 11, 8949: 4, 8950: 1,
                          8953: 1, 8954: 1, 8956: 2, 8958: 2, 8960: 2, 8961: 2,
                          8965: 1, 8968: 2, 8972: 2, 8973: 3, 8980: 2, 8984: 2,
                          8985: 2, 8992: 2, 8996: 2, 8997: 2, 9004: 2, 9008: 2,
                          9009: 2, 9016: 2, 9020: 2, 9021: 2, 9028: 2},
      f"total={c2767_total} per-line={c2767_lines}")

c2766_total = text.count("c2766")
c2766_lines = {i + 1: l.count("c2766") for i, l in enumerate(lines) if "c2766" in l}
guard("c2766_mention_census_pre",
      c2766_total == 95
      and c2766_lines == {8908: 1, 8912: 2, 8920: 4, 8923: 1, 8924: 4, 8925: 6,
                          8930: 1, 8932: 7, 8934: 4, 8936: 10, 8937: 4, 8938: 1,
                          8941: 1, 8942: 2, 8944: 1, 8946: 1, 8948: 1, 8949: 2,
                          8953: 1, 8954: 1, 8956: 1, 8960: 1, 8961: 2, 8965: 2,
                          8966: 1, 8968: 1, 8970: 1, 8972: 1, 8973: 3, 8977: 2,
                          8980: 1, 8982: 1, 8984: 1, 8985: 2, 8989: 2, 8992: 1,
                          8994: 1, 8996: 1, 8997: 2, 9001: 2, 9004: 1, 9008: 1,
                          9009: 2, 9013: 1, 9016: 1, 9020: 1, 9021: 2, 9025: 1,
                          9028: 1},
      f"total={c2766_total} per-line={c2766_lines}")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (78 at guard time: 75 at the c2774 "
          f"guard + the official c2774 capture (the latency-matched 1778ms render) "
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
head_is_official = head_body.startswith("c2774:")
head_is_foreign = head_subj.endswith("-cron") and not head_is_official
if head_is_official:
    guard("git_head_is_c2774_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_is_c2774_commit", parent_body.startswith("c2774:"),
          f"parent={parent_short} body[:40]={parent_body[:40]!r}")
    guard("git_head_foreign_class", head_is_foreign,
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class atop the c2774 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/dd48816/0539b68/eb9de41/9b5ea95 precedent)")
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

C2774_SET = [
    "census_c2774.py", "arrival_guard_c2774.py", "rebadge_cycle2774.py",
    "capture_cycle2774.sh", "measure_c2774_tokens.py", "recursive_diff_2774.py",
    "validate_cycle2774.py", "entry_cycle2774.txt", "append_cycle2774.py",
    "scan_cycle2774_raw.json", "scan_cycle2774.json",
]
print("c2774_instrument_set_object_presence:")
missing = []
for name in C2774_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2774 files on disk")

v74 = open("/home/z/my-project/scripts/validate_cycle2774.py", "rb").read()
guard("v74_source_intact", b"CYCLE = 2774" in v74 and b"drift49_pass23_match" in v74
      and b"drift49_pass24_match" not in v74
      and b"(18,0,0,18,0)" in v74 and b"(20,0,2,18,0)" in v74
      and b"(21,0,3,18,0)" in v74 and b"pass-22 band" in v74
      and b"pass-23 band" not in v74
      and b"pass-22 evidence" in v74 and b"pass-23 evidence" not in v74,
      f"bytes={len(v74)} (the v74 pass-23 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-24 gate name drift49_pass24_match is what the v75 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-22 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-22 evidence' is present — BOTH instrument surfaces, the v75 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "0017b3b:scripts/validate_cycle2774.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v74_commit_object_intact", len(obj.stdout) == len(v74)
          and obj.stdout == v74,
          f"object_bytes={len(obj.stdout)} == disk {len(v74)} (the 0017b3b c2774 commit)")
else:
    guard("v74_commit_object_intact", False, "0017b3b object unreadable")

print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
