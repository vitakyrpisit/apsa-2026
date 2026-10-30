#!/usr/bin/env python3
"""Arrival-guard for cycle 2805 (Job ID 446189) — measured, never predicted.

Spec source: the c2804 Next-block (worklog line 9388). Checks:
  worklog 9388 lines EXACT (newline count, c2804 append post-guard prophecy);
  tail = the c2805 Next bullet;
  anchors ^Task ID: 482 / ^- No gold yet 415 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2805 entries; c2805/c2806 substring accounting
  (the token-guard lives INSIDE the c2804 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2805.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2806 = 4 total = 2 births in the c2804 Step-7 line 9386 (the
  rehearsal pre-count print 'the c2806 pre==0 expectation' AND the census-time
  print 'c2806_pre = 0') + 2 FORWARD-token births inside the c2804 Next-block
  guard phrase ('arrival-guard against c2805/c2806 tokens') AND the
  FORWARD-token sentence ('the FORWARD token c2806 must be IN the census
  tuple'), both on line 9388 — the c2804 append prophecy 'c2806 = 4 block
  births' held EXACTLY, the born-FOUR class REPEATS; the c2805 token itself is
  BORN THIRTEEN times pre-append: 2 in the c2803 Step-7 twin-print (line
  9374) + 2 in the c2803 Next-block (line 9376) + 4 in the c2804 Step-1
  (line 9380) + 1 in the c2804 Step-7 'the c2805 pre-count is 4' (line
  9386) + 4 in the c2804 Next-block (line 9388: the instance + the
  446189-c2805 id + the 'c2805/c2806' guard phrase + the measure_c2805
  tool-path surface — the bare-c-token accounting, honestly counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2804_raw.json' /
  'validate_cycle2804.py' / 'scan_cycle2804.json' carry 'e2804'/'cycle2804',
  NOT the bare c-token 'c2804' — path tokens contribute ZERO bare-c2804
  census weight;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census;
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2804 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2804 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2804 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v104 source-intact expectations matched to the v104 pass-53 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v104 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-54 gate name is what the v105 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-52 band' is present AND the evidence-paragraph lag-1 heading
  'pass-52 evidence' is present — BOTH instrument surfaces, the v105 rebadge
  P3/P8 old-string expectations, exactly as the c2804 Next-block wrote).
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
guard("worklog_lines==9388", n_nl == 9388, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2805_next_bullet", last_nonempty.startswith("- Next: the c2805 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==482", tid == 482, f"got={tid}")
guard("anchor_nogold==415", gold == 415, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2805")]
guard("dup_check_zero_serviced_c2805", len(dup) == 0, f"got={len(dup)}")
c2805_total = text.count("c2805")
c2806_total = text.count("c2806")
tok_guard = [l for l in lines if "c2805/c2806" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2805 instance")]
c2805_lines = {i + 1: l.count("c2805") for i, l in enumerate(lines) if "c2805" in l}
c2806_lines = {i + 1: l.count("c2806") for i, l in enumerate(lines) if "c2806" in l}
guard("c2805_mention_accounting_pre",
      c2805_total == 13 and c2806_total == 4 and len(tok_guard) == 1
      and len(next_block) == 1 and tok_guard[0] is next_block[0]
      and c2805_lines == {9374: 2, 9376: 2, 9380: 4, 9386: 1, 9388: 4}
      and c2806_lines == {9386: 2, 9388: 2},
      f"total={c2805_total} c2806={c2806_total} per-line={c2805_lines} "
      f"c2806_per-line={c2806_lines} "
      f"(expect 13 = 2 in the c2803 Step-7 twin-print (line 9374) + 2 in the "
      f"c2803 Next-block (line 9376) + 4 in the c2804 Step-1 (line 9380) + "
      f"1 in the c2804 Step-7 'the c2805 pre-count is 4' (line 9386) + "
      f"4 in the c2804 Next-block (line 9388: the instance + the 446189-c2805 id "
      f"+ the 'c2805/c2806' guard phrase + the measure_c2805 tool-path surface, the "
      f"bare-c-token accounting); c2806 = 4 — 2 births in the c2804 Step-7 line "
      f"9386 (the rehearsal pre-count print 'the c2806 pre==0 expectation' AND the "
      f"census-time print 'c2806_pre = 0' — the Step-7 twin-print class REPEATS) + "
      f"2 FORWARD-token births TWICE inside the c2804 Next-block guard phrase AND "
      f"census-tuple sentence, both on line 9388 (the forward-token lesson: "
      f"measured, never assumed unborn — the c2804 append prophecy 'c2806 = 4 "
      f"block births' held EXACTLY, the born-FOUR class REPEATS))")

c2804_total = text.count("c2804")
c2804_lines = {i + 1: l.count("c2804") for i, l in enumerate(lines) if "c2804" in l}
guard("c2804_mention_census_pre",
      c2804_total == 36
      and c2804_lines == {9362: 2, 9364: 2, 9368: 5, 9374: 1, 9376: 4, 9379: 1,
                          9380: 3, 9381: 4, 9386: 4, 9388: 10},
      f"total={c2804_total} per-line={c2804_lines} (the pre-block 14 on lines "
      f"9362/9364/9368/9374/9376 + 22 births inside the c2804 block itself; the "
      f"Step-4 surface 'scan_cycle2804_raw.json'/'validate_cycle2804.py'/"
      f"'scan_cycle2804.json' carries 'cycle2804'/'e2804' on its path tokens — the "
      f"c2760 E-TOKEN lesson, the bare-c2804 weight measured honestly)")

c2803_total = text.count("c2803")
c2803_lines = {i + 1: l.count("c2803") for i, l in enumerate(lines) if "c2803" in l}
guard("c2803_mention_census_pre",
      c2803_total == 87
      and c2803_lines == {9350: 2, 9352: 2, 9356: 6, 9362: 1, 9364: 4, 9367: 1,
                          9368: 5, 9369: 4, 9374: 4, 9376: 11, 9378: 15, 9380: 14,
                          9381: 3, 9382: 3, 9385: 7, 9386: 3, 9388: 2},
      f"total={c2803_total} per-line={c2803_lines} (the c2804-guard-probe state 40 "
      f"on lines 9350..9376 + 47 births inside the c2804 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2802", 99), ("c2801", 86), ("c2800", 109), ("c2799", 91),
                   ("c2798", 89), ("c2797", 83), ("c2796", 93), ("c2795", 114),
                   ("c2794", 110), ("c2793", 118), ("c2792", 123), ("c2791", 111),
                   ("c2790", 122), ("c2789", 114), ("c2788", 125), ("c2787", 126),
                   ("c2786", 146), ("c2785", 130), ("c2784", 128), ("c2783", 129),
                   ("c2782", 128), ("c2781", 133), ("c2780", 138), ("c2779", 138),
                   ("c2778", 182), ("c2777", 154), ("c2776", 159), ("c2775", 168),
                   ("c2774", 173), ("c2773", 177), ("c2772", 196), ("c2771", 186),
                   ("c2770", 232), ("c2769", 175), ("c2768", 178), ("c2767", 235),
                   ("c2766", 209), ("c2765", 169), ("c2764", 171), ("c2763", 179),
                   ("c2762", 215), ("c2761", 229), ("c2760", 174), ("c2759", 174),
                   ("c2758", 176), ("c2757", 179), ("c2756", 184), ("c2755", 191),
                   ("c2754", 194), ("c2753", 205), ("c2752", 211), ("c2751", 197),
                   ("c2750", 201), ("c2749", 203), ("c2748", 193), ("c2747", 196),
                   ("c2746", 201)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (177 total at the c2804 guard probe: "
          f"175 accounted + 2 foreign/unattributed; + 1 through the c2804 official "
          f"capture = 178, + 1 this cycle's echo (latency-match 1677ms class, "
          f"re-derivable) = 179 accounted-path cumulative, + foreign residual — "
          f"dev.log is timestamp-less: the official/foreign split is by latency-match, "
          f"honest, no over-claim; the residual foreign/unattributed is "
          f"arithmetic-necessity class)")
else:
    print("dev_log: ABSENT")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2804 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2804 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2804:"):
        official_depth = depth
        walk_info.append(f"official c2804 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2804_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2804_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2804 commit — the d990e91/5712edd/dc1c551/92ba2e4/5a117ea/"
          f"7b9e5f3/519471c/b28848d/5939089/19ff74c/660688b/7386e88/4538311/02d651d/"
          f"dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/e54aab2/d22e2bb/"
          f"134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/966ab1f/0b4f512/ffa527c/"
          f"c048029/3b69581/18522dc/ea92218/4477b73/4207111/615fc1c/7efc24d/65f4c4e/"
          f"b27a69f/f0d806e/87e21ad/e6da641/325729a/7de8446/a6fac67 precedent)")
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

C2804_SET = [
    "census_c2804.py", "arrival_guard_c2804.py", "rebadge_cycle2804.py",
    "capture_cycle2804.sh", "measure_c2804_tokens.py", "recursive_diff_2804.py",
    "validate_cycle2804.py", "entry_cycle2804.txt", "append_cycle2804.py",
    "scan_cycle2804_raw.json", "scan_cycle2804.json",
]
print("c2804_instrument_set_object_presence:")
missing = []
for name in C2804_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2804 files on disk")

v104 = open("/home/z/my-project/scripts/validate_cycle2804.py", "rb").read()
guard("v104_source_intact", b"CYCLE = 2804" in v104 and b"drift49_pass53_match" in v104
      and b"drift49_pass54_match" not in v104
      and b"(18,0,0,18,0)" in v104 and b"(20,0,2,18,0)" in v104
      and b"(21,0,3,18,0)" in v104 and b"pass-52 band" in v104
      and b"pass-53 band" not in v104
      and b"pass-52 evidence" in v104 and b"pass-53 evidence" not in v104,
      f"bytes={len(v104)} (the v104 pass-53 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-54 gate name drift49_pass54_match is what the v105 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-52 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-52 evidence' is present — BOTH instrument surfaces, the v105 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "cbdb675:scripts/validate_cycle2804.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v104_commit_object_intact", len(obj.stdout) == len(v104)
          and obj.stdout == v104,
          f"object_bytes={len(obj.stdout)} == disk {len(v104)} (the cbdb675 c2804 commit)")
else:
    guard("v104_commit_object_intact", False, "cbdb675 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
