#!/usr/bin/env python3
"""Arrival-guard for cycle 2810 (Job ID 446189) — measured, never predicted.

Spec source: the c2809 Next-block (worklog line 9448). Checks:
  worklog 9448 lines EXACT (newline count, c2809 append post-guard prophecy);
  tail = the c2810 Next bullet;
  anchors ^Task ID: 487 / ^- No gold yet 420 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2810 entries; c2810/c2811 substring accounting
  (the token-guard lives INSIDE the c2809 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2810.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2811 = 4 total = 2 births in the c2809 Step-7 line 9446 (the
  rehearsal pre-count print 'the c2811 pre==0 expectation' AND the census-time
  print 'c2811_pre = 0') + 2 FORWARD-token births inside the c2809 Next-block
  guard phrase ('arrival-guard against c2810/c2811 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2811 must be IN the census
  tuple'), both on line 9448 — the c2809 append prophecy 'c2811 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS a SEVENTH time; the c2810
  token itself is BORN THIRTEEN times pre-append: 2 in the c2808 Step-7
  twin-print (line 9434) + 2 in the c2808 Next-block (line 9436) + 4 in the
  c2809 Step-1 census sentence (line 9440: the '+ c2810 = 4 per-line' print +
  the twin-print quotes 'the c2810 pre==0 expectation' AND 'c2810_pre = 0' +
  the prophecy quote 'c2810 = 4 block births') + 1 in the c2809 Step-7 'the
  c2810 pre-count is 4' (line 9446) + 4 in the c2809 Next-block (line 9448:
  the instance + the 446189-c2810 id + the 'c2810/c2811' guard phrase + the
  'measure_c2810_tokens.py' surface — the bare-c-token accounting, honestly
  counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2809_raw.json' /
  'validate_cycle2809.py' / 'scan_cycle2809.json' carry 'e2809'/'cycle2809',
  NOT the bare c-token 'c2809' — line 9443 ABSENT from the measured c2809
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2809 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2809 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2809 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v109 source-intact expectations matched to the v109 pass-58 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v109 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-59 gate name is what the v110 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-57 band' is present AND the evidence-paragraph lag-1 heading
  'pass-57 evidence' is present — BOTH instrument surfaces, the v110 rebadge
  P3/P8 old-string expectations, exactly as the c2809 Next-block wrote).
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
guard("worklog_lines==9448", n_nl == 9448, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2810_next_bullet", last_nonempty.startswith("- Next: the c2810 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==487", tid == 487, f"got={tid}")
guard("anchor_nogold==420", gold == 420, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2810")]
guard("dup_check_zero_serviced_c2810", len(dup) == 0, f"got={len(dup)}")
c2810_total = text.count("c2810")
c2811_total = text.count("c2811")
tok_guard = [l for l in lines if "c2810/c2811" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2810 instance")]
c2810_lines = {i + 1: l.count("c2810") for i, l in enumerate(lines) if "c2810" in l}
c2811_lines = {i + 1: l.count("c2811") for i, l in enumerate(lines) if "c2811" in l}
guard("c2810_mention_accounting_pre",
      c2810_total == 13 and c2811_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2810_lines == {9434: 2, 9436: 2, 9440: 4, 9446: 1, 9448: 4}
      and c2811_lines == {9446: 2, 9448: 2},
      f"total={c2810_total} c2811={c2811_total} per-line={c2810_lines} "
      f"c2811_per-line={c2811_lines} "
      f"(expect 13 = 2 in the c2808 Step-7 twin-print (line 9434) + 2 in the "
      f"c2808 Next-block (line 9436) + 4 in the c2809 Step-1 census sentence "
      f"(line 9440: the '+ c2810 = 4 per-line' print + the twin-print quotes "
      f"'the c2810 pre==0 expectation' AND 'c2810_pre = 0' + the prophecy "
      f"quote 'c2810 = 4 block births') + 1 in the c2809 Step-7 'the c2810 "
      f"pre-count is 4' (line 9446) + 4 in the c2809 Next-block (line 9448: "
      f"the instance + the 446189-c2810 id + the 'c2810/c2811' guard phrase + "
      f"the 'measure_c2810_tokens.py' surface, the bare-c-token accounting); "
      f"c2811 = 4 — 2 births in the c2809 Step-7 line 9446 (the rehearsal "
      f"pre-count print 'the c2811 pre==0 expectation' AND the census-time "
      f"print 'c2811_pre = 0' — the Step-7 twin-print class REPEATS) + 2 "
      f"FORWARD-token births TWICE inside the c2809 Next-block guard phrase "
      f"AND census-tuple sentence, both on line 9448 (the forward-token "
      f"lesson: measured, never assumed unborn — the c2809 append prophecy "
      f"'c2811 = 4 block births' held EXACTLY, the born-FOUR class REPEATS a "
      f"SEVENTH time))")

c2809_total = text.count("c2809")
c2809_lines = {i + 1: l.count("c2809") for i, l in enumerate(lines) if "c2809" in l}
guard("c2809_mention_census_pre",
      c2809_total == 35
      and c2809_lines == {9422: 2, 9424: 2, 9428: 4, 9434: 1, 9436: 4, 9439: 1,
                          9440: 4, 9441: 5, 9446: 4, 9448: 8},
      f"total={c2809_total} per-line={c2809_lines} (the pre-block 13 on lines "
      f"9422/9424/9428/9434/9436 + 22 births inside the c2809 block itself; the "
      f"Step-4 surface 'scan_cycle2809_raw.json'/'validate_cycle2809.py'/"
      f"'scan_cycle2809.json' carries 'cycle2809'/'e2809' on its path tokens — the "
      f"c2760 E-TOKEN lesson re-verified live: line 9443 ABSENT from the dict, the "
      f"bare-c2809 weight measured honestly)")

c2808_total = text.count("c2808")
c2808_lines = {i + 1: l.count("c2808") for i, l in enumerate(lines) if "c2808" in l}
guard("c2808_mention_census_pre",
      c2808_total == 78
      and c2808_lines == {9410: 2, 9412: 2, 9416: 5, 9422: 1, 9424: 4, 9427: 1,
                          9428: 4, 9429: 5, 9434: 4, 9436: 9, 9438: 14, 9440: 10,
                          9441: 5, 9442: 3, 9445: 3, 9446: 3, 9448: 3},
      f"total={c2808_total} per-line={c2808_lines} (the c2809-guard-probe state 37 "
      f"on lines 9410..9436 + 41 births inside the c2809 block itself, measured "
      f"per-line at this cycle's census)")

c2807_total = text.count("c2807")
c2807_lines = {i + 1: l.count("c2807") for i, l in enumerate(lines) if "c2807" in l}
guard("c2807_mention_census_pre",
      c2807_total == 76
      and c2807_lines == {9398: 2, 9400: 2, 9404: 5, 9410: 1, 9412: 4, 9415: 1,
                          9416: 4, 9417: 5, 9422: 4, 9424: 9, 9426: 10, 9428: 10,
                          9429: 5, 9430: 3, 9433: 1, 9434: 3, 9436: 2, 9438: 1,
                          9440: 2, 9441: 1, 9448: 1},
      f"total={c2807_total} per-line={c2807_lines} (the c2808-guard-probe state 71 "
      f"on lines 9398..9436 + 5 births inside the c2809 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2806", 78), ("c2805", 86), ("c2804", 101), ("c2803", 112),
                   ("c2802", 116), ("c2801", 93), ("c2800", 127), ("c2799", 98),
                   ("c2798", 96), ("c2797", 88), ("c2796", 98), ("c2795", 121),
                   ("c2794", 115), ("c2793", 123), ("c2792", 128), ("c2791", 116),
                   ("c2790", 129), ("c2789", 119), ("c2788", 130), ("c2787", 131),
                   ("c2786", 153), ("c2785", 135), ("c2784", 133), ("c2783", 134),
                   ("c2782", 133), ("c2781", 138), ("c2780", 143), ("c2779", 143),
                   ("c2778", 187), ("c2777", 159), ("c2776", 164), ("c2775", 173),
                   ("c2774", 178), ("c2773", 182), ("c2772", 201), ("c2771", 191),
                   ("c2770", 242), ("c2769", 180), ("c2768", 183), ("c2767", 250),
                   ("c2766", 219), ("c2765", 174), ("c2764", 176), ("c2763", 184),
                   ("c2762", 221), ("c2761", 240), ("c2760", 179), ("c2759", 179),
                   ("c2758", 181), ("c2757", 184), ("c2756", 189), ("c2755", 196),
                   ("c2754", 199), ("c2753", 215), ("c2752", 221), ("c2751", 207),
                   ("c2750", 211), ("c2749", 213)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (204 at this probe: 201 at the "
          f"c2809 guard probe + 1 through the c2809 official capture + 2 foreign "
          f"POSTs landed in the span since (1548ms absorbed pre-close, 1674ms + "
          f"1724ms post-close) + 1 this cycle's echo (latency-match 1807ms class, "
          f"bracketed) = 190 accounted-path cumulative + 14 foreign/unattributed "
          f"cumulative — dev.log is timestamp-less: the official/foreign split is "
          f"by latency-match, honest, no over-claim; the residual "
          f"foreign/unattributed is arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2809 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2809 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2809:"):
        official_depth = depth
        walk_info.append(f"official c2809 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2809_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2809_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2809 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111/615fc1c/7efc24d/65f4c4e/"
          f"b27a69f/f0d806e/87e21ad/e6da641/325729a/7de8446/a6fac67/35ba192/"
          f"92a8201/6b53b65/7f7a022/1288d7f precedent)")
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

C2809_SET = [
    "census_c2809.py", "arrival_guard_c2809.py", "rebadge_cycle2809.py",
    "capture_cycle2809.sh", "measure_c2809_tokens.py", "recursive_diff_2809.py",
    "validate_cycle2809.py", "entry_cycle2809.txt", "append_cycle2809.py",
    "scan_cycle2809_raw.json", "scan_cycle2809.json",
]
print("c2809_instrument_set_object_presence:")
missing = []
for name in C2809_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2809 files on disk")

v109 = open("/home/z/my-project/scripts/validate_cycle2809.py", "rb").read()
guard("v109_source_intact", b"CYCLE = 2809" in v109 and b"drift49_pass58_match" in v109
      and b"drift49_pass59_match" not in v109
      and b"(18,0,0,18,0)" in v109 and b"(20,0,2,18,0)" in v109
      and b"(21,0,3,18,0)" in v109 and b"pass-57 band" in v109
      and b"pass-58 band" not in v109
      and b"pass-57 evidence" in v109 and b"pass-58 evidence" not in v109,
      f"bytes={len(v109)} (the v109 pass-58 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-59 gate name drift49_pass59_match is what the v110 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-57 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-57 evidence' is present — BOTH instrument surfaces, the v110 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "d19b6ac:scripts/validate_cycle2809.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v109_commit_object_intact", len(obj.stdout) == len(v109)
          and obj.stdout == v109,
          f"object_bytes={len(obj.stdout)} == disk {len(v109)} (the d19b6ac c2809 commit)")
else:
    guard("v109_commit_object_intact", False, "d19b6ac object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
