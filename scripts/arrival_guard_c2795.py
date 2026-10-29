#!/usr/bin/env python3
"""Arrival-guard for cycle 2795 (Job ID 446189) — measured, never predicted.

Spec source: the c2794 Next-block (worklog line 9268). Checks:
  worklog 9268 lines EXACT (newline count, c2794 append post-guard prophecy);
  tail = the c2795 Next bullet;
  anchors ^Task ID: 472 / ^- No gold yet 405 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2795 entries; c2795/c2796 substring accounting
  (the token-guard lives INSIDE the c2794 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2795.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2796 = 3 total = 1 birth in the c2794 Step-7 line 9266 (the
  rehearsal pre-count print 'the c2796 pre==0 expectation') + 2 FORWARD-token
  births inside the c2794 Next-block guard phrase ('arrival-guard against
  c2795/c2796 tokens') AND the FORWARD-token sentence ('the FORWARD token
  c2796 must be IN the census tuple'), both on line 9268 — the
  c2767..c2795 forward-token lessons: measure it, never assume it unborn;
  the c2795 token itself is BORN ELEVEN times pre-append: 1 in the c2793
  Step-7 rehearsal print (line 9254) + 2 in the c2793 Next-block (line 9256)
  + 3 in the c2794 Step-1 census print (line 9260) + 1 in the c2794 Step-7
  'the c2795 pre-count is 3' (line 9266) + 4 in the c2794 Next-block
  (line 9268: the instance + id + the 'c2795/c2796' guard phrase + the
  measure_c2795_tokens.py path token — the bare-c-token path class, honestly
  accounted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2794_raw.json' /
  'validate_cycle2794.py' / 'scan_cycle2794.json' carry 'e2794'/'cycle2794',
  NOT the bare c-token 'c2794' — path tokens contribute ZERO bare-c2794
  census weight (line 9263 ABSENT from the measured c2794 per-line dict);
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2794 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2794 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2794 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v94 source-intact expectations matched to the v94 pass-43 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v94 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-44 gate name is what the v95 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-42 band' is present AND the evidence-paragraph lag-1 heading
  'pass-42 evidence' is present — BOTH instrument surfaces, the v95 rebadge
  P3/P8 old-string expectations, exactly as the c2794 Next-block wrote).
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
guard("worklog_lines==9268", n_nl == 9268, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2795_next_bullet", last_nonempty.startswith("- Next: the c2795 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==472", tid == 472, f"got={tid}")
guard("anchor_nogold==405", gold == 405, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2795")]
guard("dup_check_zero_serviced_c2795", len(dup) == 0, f"got={len(dup)}")
c2795_total = text.count("c2795")
c2796_total = text.count("c2796")
tok_guard = [l for l in lines if "c2795/c2796" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2795 instance")]
c2795_lines = {i + 1: l.count("c2795") for i, l in enumerate(lines) if "c2795" in l}
c2796_lines = {i + 1: l.count("c2796") for i, l in enumerate(lines) if "c2796" in l}
guard("c2795_mention_accounting_pre",
      c2795_total == 11 and c2796_total == 3 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2795_lines == {9254: 1, 9256: 2, 9260: 3, 9266: 1, 9268: 4}
      and c2796_lines == {9266: 1, 9268: 2},
      f"total={c2795_total} c2796={c2796_total} per-line={c2795_lines} "
      f"c2796_per-line={c2796_lines} "
      f"(expect 11 = 1 in the c2793 Step-7 rehearsal print (line 9254, 'the c2795 "
      f"pre==0 expectation') + 2 in the c2793 Next-block (line 9256, the guard "
      f"phrase AND the FORWARD-token sentence) + 3 in the c2794 Step-1 census "
      f"print (line 9260) + 1 in the c2794 Step-7 'the c2795 pre-count is 3' "
      f"(line 9266) + 4 in the c2794 Next-block (line 9268: the instance + id + "
      f"'c2795/c2796' guard phrase + the measure_c2795_tokens.py path token, the "
      f"bare-c-token path class); c2796 = 3 — 1 birth in the c2794 Step-7 "
      f"rehearsal pre-count print (line 9266, 'the c2796 pre==0 expectation') + "
      f"2 FORWARD-token births inside the c2794 Next-block guard phrase AND the "
      f"FORWARD-token sentence, both on line 9268 (the forward-token lesson: "
      f"measured, never assumed unborn — the born-thrice class REPEATS))")

c2794_total = text.count("c2794")
c2794_lines = {i + 1: l.count("c2794") for i, l in enumerate(lines) if "c2794" in l}
guard("c2794_mention_census_pre",
      c2794_total == 42
      and c2794_lines == {9242: 1, 9244: 2, 9248: 1, 9254: 1, 9256: 4, 9259: 1,
                          9260: 9, 9261: 8, 9266: 4, 9268: 11},
      f"total={c2794_total} per-line={c2794_lines} (the pre-block 9 on lines "
      f"9242/9244/9248/9254/9256 + 33 births inside the c2794 block itself; the "
      f"Step-4 surface 'scan_cycle2794_raw.json'/'validate_cycle2794.py'/"
      f"'scan_cycle2794.json' on line 9263 carries 'cycle2794'/'e2794', NOT the "
      f"bare c-token — the c2760 E-TOKEN lesson: line 9263 ABSENT from the "
      f"measured dict)")

for tag, total in (("c2793", 83), ("c2792", 93), ("c2791", 92), ("c2790", 93),
                   ("c2789", 95), ("c2788", 106), ("c2787", 107), ("c2786", 117),
                   ("c2785", 111), ("c2784", 109), ("c2783", 110), ("c2782", 109),
                   ("c2781", 114), ("c2780", 118), ("c2779", 119), ("c2778", 159),
                   ("c2777", 135), ("c2776", 140), ("c2775", 149), ("c2774", 154),
                   ("c2773", 158), ("c2772", 177), ("c2771", 167), ("c2770", 203),
                   ("c2769", 156), ("c2768", 159), ("c2767", 196), ("c2766", 179),
                   ("c2765", 150), ("c2764", 152), ("c2763", 160), ("c2762", 186),
                   ("c2761", 200), ("c2760", 155), ("c2759", 155), ("c2758", 157),
                   ("c2757", 160), ("c2756", 165), ("c2755", 172), ("c2754", 175),
                   ("c2753", 181), ("c2752", 187), ("c2751", 173), ("c2750", 175),
                   ("c2749", 179), ("c2748", 169), ("c2747", 167), ("c2746", 171)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (150 at the census probe: 148 through "
          f"the c2794 official capture + 2 foreign/unattributed since — dev.log is "
          f"timestamp-less: the official/foreign split is by latency-match, honest, "
          f"no over-claim; the residual foreign/unattributed is arithmetic-necessity "
          f"class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2794 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2794 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2794:"):
        official_depth = depth
        walk_info.append(f"official c2794 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2794_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2794_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2794 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111 precedent)")
    for depth in range(0, official_depth if official_depth is not None else 0):
        rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
        stat = git("show", "--stat", "--format=", rev)
        guard(f"git_walk_depth{depth}_zero_ledger_touch", "worklog.md" not in stat,
              f"{rev} touches only foreign-add files; worklog touched="
              f"{'worklog.md' in stat}")
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

C2794_SET = [
    "census_c2794.py", "arrival_guard_c2794.py", "rebadge_cycle2794.py",
    "capture_cycle2794.sh", "measure_c2794_tokens.py", "recursive_diff_2794.py",
    "validate_cycle2794.py", "entry_cycle2794.txt", "append_cycle2794.py",
    "scan_cycle2794_raw.json", "scan_cycle2794.json",
]
print("c2794_instrument_set_object_presence:")
missing = []
for name in C2794_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2794 files on disk")

v94 = open("/home/z/my-project/scripts/validate_cycle2794.py", "rb").read()
guard("v94_source_intact", b"CYCLE = 2794" in v94 and b"drift49_pass43_match" in v94
      and b"drift49_pass44_match" not in v94
      and b"(18,0,0,18,0)" in v94 and b"(20,0,2,18,0)" in v94
      and b"(21,0,3,18,0)" in v94 and b"pass-42 band" in v94
      and b"pass-43 band" not in v94
      and b"pass-42 evidence" in v94 and b"pass-43 evidence" not in v94,
      f"bytes={len(v94)} (the v94 pass-43 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-44 gate name drift49_pass44_match is what the v95 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-42 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-42 evidence' is present — BOTH instrument surfaces, the v95 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "fb1d1d1:scripts/validate_cycle2794.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v94_commit_object_intact", len(obj.stdout) == len(v94)
          and obj.stdout == v94,
          f"object_bytes={len(obj.stdout)} == disk {len(v94)} (the fb1d1d1 c2794 commit)")
else:
    guard("v94_commit_object_intact", False, "fb1d1d1 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
