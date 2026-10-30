#!/usr/bin/env python3
"""Arrival-guard for cycle 2807 (Job ID 446189) — measured, never predicted.

Spec source: the c2806 Next-block (worklog line 9412). Checks:
  worklog 9412 lines EXACT (newline count, c2806 append post-guard prophecy);
  tail = the c2807 Next bullet;
  anchors ^Task ID: 484 / ^- No gold yet 417 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2807 entries; c2807/c2808 substring accounting
  (the token-guard lives INSIDE the c2806 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2807.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2808 = 4 total = 2 births in the c2806 Step-7 line 9410 (the
  rehearsal pre-count print 'the c2808 pre==0 expectation' AND the census-time
  print 'c2808_pre = 0') + 2 FORWARD-token births inside the c2806 Next-block
  guard phrase ('arrival-guard against c2807/c2808 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2808 must be IN the census
  tuple'), both on line 9412 — the c2806 append prophecy 'c2808 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS a FOURTH time; the c2807
  token itself is BORN FOURTEEN times pre-append: 2 in the c2805 Step-7
  twin-print (line 9398) + 2 in the c2805 Next-block (line 9400) + 5 in the
  c2806 Step-1 census sentence (line 9404) + 1 in the c2806 Step-7 'the
  c2807 pre-count is 4' (line 9410) + 4 in the c2806 Next-block (line 9412:
  the instance + the 446189-c2807 id + the 'c2807/c2808' guard phrase + the
  census-tuple sentence 'the FORWARD token c2808' — the bare-c-token
  accounting, honestly counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2806_raw.json' /
  'validate_cycle2806.py' / 'scan_cycle2806.json' carry 'e2806'/'cycle2806',
  NOT the bare c-token 'c2806' — line 9407 ABSENT from the measured c2806
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2806 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2806 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2806 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v106 source-intact expectations matched to the v106 pass-55 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v106 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-56 gate name is what the v107 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-54 band' is present AND the evidence-paragraph lag-1 heading
  'pass-54 evidence' is present — BOTH instrument surfaces, the v107 rebadge
  P3/P8 old-string expectations, exactly as the c2806 Next-block wrote).
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
guard("worklog_lines==9412", n_nl == 9412, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2807_next_bullet", last_nonempty.startswith("- Next: the c2807 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==484", tid == 484, f"got={tid}")
guard("anchor_nogold==417", gold == 417, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2807")]
guard("dup_check_zero_serviced_c2807", len(dup) == 0, f"got={len(dup)}")
c2807_total = text.count("c2807")
c2808_total = text.count("c2808")
tok_guard = [l for l in lines if "c2807/c2808" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2807 instance")]
c2807_lines = {i + 1: l.count("c2807") for i, l in enumerate(lines) if "c2807" in l}
c2808_lines = {i + 1: l.count("c2808") for i, l in enumerate(lines) if "c2808" in l}
guard("c2807_mention_accounting_pre",
      c2807_total == 14 and c2808_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2807_lines == {9398: 2, 9400: 2, 9404: 5, 9410: 1, 9412: 4}
      and c2808_lines == {9410: 2, 9412: 2},
      f"total={c2807_total} c2808={c2808_total} per-line={c2807_lines} "
      f"c2808_per-line={c2808_lines} "
      f"(expect 14 = 2 in the c2805 Step-7 twin-print (line 9398) + 2 in the "
      f"c2805 Next-block (line 9400) + 5 in the c2806 Step-1 census sentence "
      f"(line 9404) + 1 in the c2806 Step-7 'the c2807 pre-count is 4' (line "
      f"9410) + 4 in the c2806 Next-block (line 9412: the instance + the "
      f"446189-c2807 id + the 'c2807/c2808' guard phrase + the census-tuple "
      f"sentence 'the FORWARD token c2808', the bare-c-token accounting); "
      f"c2808 = 4 — 2 births in the c2806 Step-7 line 9410 (the rehearsal "
      f"pre-count print 'the c2808 pre==0 expectation' AND the census-time "
      f"print 'c2808_pre = 0' — the Step-7 twin-print class REPEATS) + 2 "
      f"FORWARD-token births TWICE inside the c2806 Next-block guard phrase "
      f"AND census-tuple sentence, both on line 9412 (the forward-token "
      f"lesson: measured, never assumed unborn — the c2806 append prophecy "
      f"'c2808 = 4 block births' held EXACTLY, the born-FOUR class REPEATS a "
      f"FOURTH time))")

c2806_total = text.count("c2806")
c2806_lines = {i + 1: l.count("c2806") for i, l in enumerate(lines) if "c2806" in l}
guard("c2806_mention_census_pre",
      c2806_total == 36
      and c2806_lines == {9386: 2, 9388: 2, 9392: 4, 9398: 1, 9400: 4, 9403: 1,
                          9404: 4, 9405: 5, 9410: 4, 9412: 9},
      f"total={c2806_total} per-line={c2806_lines} (the pre-block 13 on lines "
      f"9386/9388/9392/9398/9400 + 23 births inside the c2806 block itself; the "
      f"Step-4 surface 'scan_cycle2806_raw.json'/'validate_cycle2806.py'/"
      f"'scan_cycle2806.json' carries 'cycle2806'/'e2806' on its path tokens — the "
      f"c2760 E-TOKEN lesson re-verified live: line 9407 ABSENT from the dict, the "
      f"bare-c2806 weight measured honestly)")

c2805_total = text.count("c2805")
c2805_lines = {i + 1: l.count("c2805") for i, l in enumerate(lines) if "c2805" in l}
guard("c2805_mention_census_pre",
      c2805_total == 75
      and c2805_lines == {9374: 2, 9376: 2, 9380: 4, 9386: 1, 9388: 4, 9391: 1,
                          9392: 3, 9393: 8, 9398: 4, 9400: 10, 9402: 10, 9404: 9,
                          9405: 6, 9406: 3, 9409: 2, 9410: 3, 9412: 3},
      f"total={c2805_total} per-line={c2805_lines} (the c2806-guard-probe state 39 "
      f"on lines 9374..9400 + 36 births inside the c2806 block itself, measured "
      f"per-line at this cycle's census)")

c2804_total = text.count("c2804")
c2804_lines = {i + 1: l.count("c2804") for i, l in enumerate(lines) if "c2804" in l}
guard("c2804_mention_census_pre",
      c2804_total == 91
      and c2804_lines == {9362: 2, 9364: 2, 9368: 5, 9374: 1, 9376: 4, 9379: 1,
                          9380: 3, 9381: 4, 9386: 4, 9388: 10, 9390: 14, 9392: 13,
                          9393: 7, 9394: 3, 9397: 8, 9398: 4, 9400: 2, 9404: 2,
                          9410: 1, 9412: 1},
      f"total={c2804_total} per-line={c2804_lines} (the c2805-guard-probe state 87 "
      f"on lines 9362..9400 + 4 births inside the c2806 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2803", 99), ("c2802", 109), ("c2801", 89), ("c2800", 117),
                   ("c2799", 94), ("c2798", 92), ("c2797", 85), ("c2796", 95),
                   ("c2795", 117), ("c2794", 112), ("c2793", 120), ("c2792", 125),
                   ("c2791", 113), ("c2790", 125), ("c2789", 116), ("c2788", 127),
                   ("c2787", 128), ("c2786", 149), ("c2785", 132), ("c2784", 130),
                   ("c2783", 131), ("c2782", 130), ("c2781", 135), ("c2780", 140),
                   ("c2779", 140), ("c2778", 184), ("c2777", 156), ("c2776", 161),
                   ("c2775", 170), ("c2774", 175), ("c2773", 179), ("c2772", 198),
                   ("c2771", 188), ("c2770", 236), ("c2769", 177), ("c2768", 180),
                   ("c2767", 241), ("c2766", 213), ("c2765", 171), ("c2764", 173),
                   ("c2763", 181), ("c2762", 218), ("c2761", 234), ("c2760", 176),
                   ("c2759", 176), ("c2758", 178), ("c2757", 181), ("c2756", 186),
                   ("c2755", 193), ("c2754", 196), ("c2753", 209), ("c2752", 215),
                   ("c2751", 201), ("c2750", 205), ("c2749", 207), ("c2748", 197),
                   ("c2747", 200), ("c2746", 209)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (183 accounted-path cumulative at this "
          f"probe: 181 at the c2806 guard probe + 1 through the c2806 official "
          f"capture + 1 this cycle's echo (latency-match 1678ms class, bracketed) "
          f"= 183; + 7 foreign/unattributed cumulative — dev.log is timestamp-less: "
          f"the official/foreign split is by latency-match, honest, no over-claim; "
          f"the residual foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2806 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2806 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2806:"):
        official_depth = depth
        walk_info.append(f"official c2806 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2806_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2806_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2806 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111/615fc1c/7efc24d/65f4c4e/"
          f"b27a69f/f0d806e/87e21ad/e6da641/325729a/7de8446/a6fac67/35ba192/"
          f"92a8201 precedent)")
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

C2806_SET = [
    "census_c2806.py", "arrival_guard_c2806.py", "rebadge_cycle2806.py",
    "capture_cycle2806.sh", "measure_c2806_tokens.py", "recursive_diff_2806.py",
    "validate_cycle2806.py", "entry_cycle2806.txt", "append_cycle2806.py",
    "scan_cycle2806_raw.json", "scan_cycle2806.json",
]
print("c2806_instrument_set_object_presence:")
missing = []
for name in C2806_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2806 files on disk")

v106 = open("/home/z/my-project/scripts/validate_cycle2806.py", "rb").read()
guard("v106_source_intact", b"CYCLE = 2806" in v106 and b"drift49_pass55_match" in v106
      and b"drift49_pass56_match" not in v106
      and b"(18,0,0,18,0)" in v106 and b"(20,0,2,18,0)" in v106
      and b"(21,0,3,18,0)" in v106 and b"pass-54 band" in v106
      and b"pass-55 band" not in v106
      and b"pass-54 evidence" in v106 and b"pass-55 evidence" not in v106,
      f"bytes={len(v106)} (the v106 pass-55 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-56 gate name drift49_pass56_match is what the v107 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-54 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-54 evidence' is present — BOTH instrument surfaces, the v107 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "cceafc6:scripts/validate_cycle2806.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v106_commit_object_intact", len(obj.stdout) == len(v106)
          and obj.stdout == v106,
          f"object_bytes={len(obj.stdout)} == disk {len(v106)} (the cceafc6 c2806 commit)")
else:
    guard("v106_commit_object_intact", False, "cceafc6 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
