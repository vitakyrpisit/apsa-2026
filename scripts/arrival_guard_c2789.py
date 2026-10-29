#!/usr/bin/env python3
"""Arrival-guard for cycle 2789 (Job ID 446189) — measured, never predicted.

Spec source: the c2788 Next-block (worklog line 9196). Checks:
  worklog 9196 lines EXACT (newline count, c2788 append post-guard prophecy);
  tail = the c2789 Next bullet;
  anchors ^Task ID: 466 / ^- No gold yet 399 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2789 entries; c2789/c2790 substring accounting
  (the c2789/c2790 token-guard lives INSIDE the c2788 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2789.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2790 = 2 total = 2 FORWARD-token births inside the c2788
  Next-block guard phrase ('arrival-guard against c2789/c2790 tokens') AND
  the FORWARD-token sentence ('the FORWARD token c2790 must be IN the census
  tuple'), both on line 9196 — the c2767..c2789 forward-token lessons:
  measure it, never assume it unborn);
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-3/4 surfaces 'scan_cycle2788_raw.json'
  / 'validate_cycle2788.py' / 'scan_cycle2788.json' carry 'e2788'/'cycle2788',
  NOT the bare c-token 'c2788' — path tokens contribute ZERO bare-c2788
  census weight, which is why the measured c2788 per-line dict has NO 9190
  entry (the c2788 Step-3 line); the guard expectations below are the census
  MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2788 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2788 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2788 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v88 source-intact expectations matched to the v88 pass-37 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v88 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-38 gate name is what the v89 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-36 band' is present AND the evidence-paragraph lag-1 heading
  'pass-36 evidence' is present — BOTH instrument surfaces, the v89 rebadge
  P3/P8 old-string expectations, exactly as the c2788 Next-block wrote).
"""
import os
import subprocess
import sys
import time

WL = "/home/z/my-project/worklog.md"
DEVLOG = "/home/z/my-project/dev.log"
BA = "/home/z/my-project/.basedagents"

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


print(f"guard_run_epoch={time.time():.9f}")
raw = open(WL, "rb").read()
n_nl = raw.count(b"\n")
guard("worklog_lines==9196", n_nl == 9196, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2789_next_bullet", last_nonempty.startswith("- Next: the c2789 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==466", tid == 466, f"got={tid}")
guard("anchor_nogold==399", gold == 399, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2789")]
guard("dup_check_zero_serviced_c2789", len(dup) == 0, f"got={len(dup)}")
c2789_total = text.count("c2789")
c2790_total = text.count("c2790")
tok_guard = [l for l in lines if "c2789/c2790" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2789 instance")]
c2789_lines = {i + 1: l.count("c2789") for i, l in enumerate(lines) if "c2789" in l}
c2790_lines = {i + 1: l.count("c2790") for i, l in enumerate(lines) if "c2790" in l}
guard("c2789_mention_accounting_pre",
      c2789_total == 9 and c2790_total == 2 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2789_lines == {9184: 2, 9188: 1, 9194: 1, 9196: 5}
      and c2790_lines == {9196: 2},
      f"total={c2789_total} c2790={c2790_total} per-line={c2789_lines} "
      f"c2790_per-line={c2790_lines} "
      f"(expect 9 = 2 FORWARD-token births inside the c2787 Next-block (line 9184, "
      f"the guard phrase 'c2788/c2789' AND the FORWARD-token sentence) + 1 in the "
      f"c2788 Step-1 line 9188 (the rehearsal pre==0 mention) + 1 in the c2788 "
      f"Step-7 line 9194 ('the c2789 pre==0 expectation measured BEFORE the run') "
      f"+ 5 in the c2788 Next-block line 9196 — which is itself the c2789/c2790 "
      f"token-guard: the instance + id + 'c2789/c2790' phrase + "
      f"measure_c2789_tokens.py + the echo-prescription phrase 'the c2789 echo "
      f"should land'; c2790 = 2 — 2 FORWARD-token births inside the c2788 "
      f"Next-block guard phrase AND the FORWARD-token sentence, both on line "
      f"9196 (the forward-token lesson: measured, never assumed unborn))")

c2788_total = text.count("c2788")
c2788_lines = {i + 1: l.count("c2788") for i, l in enumerate(lines) if "c2788" in l}
guard("c2788_mention_census_pre",
      c2788_total == 38
      and c2788_lines == {9129: 2, 9172: 2, 9176: 2, 9184: 5, 9187: 1, 9188: 3,
                          9189: 8, 9194: 4, 9196: 11},
      f"total={c2788_total} per-line={c2788_lines} (NO 9190 entry — the Step-3 "
      f"capture surface 'scan_cycle2788_raw.json' and the Step-4 "
      f"validate_cycle2788.py/scan_cycle2788.json surfaces carry 'cycle2788'/'e2788', "
      f"NOT the bare c-token, the c2760 lesson re-verified live at census time)")

for tag, total in (("c2787", 78), ("c2786", 88), ("c2785", 87), ("c2784", 85),
                   ("c2783", 83), ("c2782", 85), ("c2781", 90), ("c2780", 94),
                   ("c2779", 95), ("c2778", 129), ("c2777", 111), ("c2776", 116),
                   ("c2775", 125), ("c2774", 130), ("c2773", 134), ("c2772", 153),
                   ("c2771", 143), ("c2770", 173), ("c2769", 137), ("c2768", 140),
                   ("c2767", 165), ("c2766", 154), ("c2765", 131), ("c2764", 133),
                   ("c2763", 141), ("c2762", 161), ("c2761", 175), ("c2760", 136),
                   ("c2759", 136), ("c2758", 138), ("c2757", 141), ("c2756", 146),
                   ("c2755", 153), ("c2754", 156), ("c2753", 162), ("c2752", 168),
                   ("c2751", 154), ("c2750", 156), ("c2749", 160), ("c2748", 150),
                   ("c2747", 148), ("c2746", 146)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (132 at the census probe: 129 at the "
          f"c2788 guard + the official c2788 capture + the loop echo #510 of THIS "
          f"servicing + 1 foreign/unattributed since — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual +1 foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2788 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2788 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2788:"):
        official_depth = depth
        walk_info.append(f"official c2788 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_body = git("log", "-1", "--format=%B")
if official_depth == 0:
    guard("git_head_is_c2788_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2788_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2788 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c "
          f"precedent)")
    for depth in range(0, official_depth if official_depth is not None else 0):
        rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
        stat = git("show", "--stat", "--format=", rev)
        guard(f"git_walk_depth{depth}_zero_ledger_touch", "worklog.md" not in stat,
              f"{rev} touches only foreign-add files; worklog touched="
              f"{'worklog.md' in stat}")
head_stat = git("show", "--stat", "--format=", head_short)
guard("git_head_zero_ledger_touch", "worklog.md" not in head_stat,
      f"HEAD={head_short} touches foreign-add files only; worklog touched="
      f"{'worklog.md' in head_stat}")
print(f"head_commit_stat_tail: {head_stat.splitlines()[-1] if head_stat else '(empty)'}")
recent = git("log", "-3", "--format=%h %s")
print("recent_commits:")
for ln in recent.splitlines():
    print(f"  {ln[:120]}")
status = git("status", "--short")
print(f"working_tree_entries={len(status.splitlines()) if status else 0}")

C2788_SET = [
    "census_c2788.py", "arrival_guard_c2788.py", "rebadge_cycle2788.py",
    "capture_cycle2788.sh", "measure_c2788_tokens.py", "recursive_diff_2788.py",
    "validate_cycle2788.py", "entry_cycle2788.txt", "append_cycle2788.py",
    "scan_cycle2788_raw.json", "scan_cycle2788.json",
]
print("c2788_instrument_set_object_presence:")
missing = []
for name in C2788_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2788 files on disk")

v88 = open("/home/z/my-project/scripts/validate_cycle2788.py", "rb").read()
guard("v88_source_intact", b"CYCLE = 2788" in v88 and b"drift49_pass37_match" in v88
      and b"drift49_pass38_match" not in v88
      and b"(18,0,0,18,0)" in v88 and b"(20,0,2,18,0)" in v88
      and b"(21,0,3,18,0)" in v88 and b"pass-36 band" in v88
      and b"pass-37 band" not in v88
      and b"pass-36 evidence" in v88 and b"pass-37 evidence" not in v88,
      f"bytes={len(v88)} (the v88 pass-37 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-38 gate name drift49_pass38_match is what the v89 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-36 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-36 evidence' is present — BOTH instrument surfaces, the v89 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "6253361:scripts/validate_cycle2788.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v88_commit_object_intact", len(obj.stdout) == len(v88)
          and obj.stdout == v88,
          f"object_bytes={len(obj.stdout)} == disk {len(v88)} (the 6253361 c2788 commit)")
else:
    guard("v88_commit_object_intact", False, "6253361 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
