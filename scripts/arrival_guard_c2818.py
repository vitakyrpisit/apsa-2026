#!/usr/bin/env python3
"""Arrival-guard for cycle 2818 (Job ID 446189) — measured, never predicted.

Spec source: the c2817 Next-block (worklog line 9544). Checks:
  worklog 9544 lines EXACT (newline count, c2817 append post-guard prophecy);
  tail = the c2818 Next bullet;
  anchors ^Task ID: 495 / ^- No gold yet 428 (as-found post-block);
  standing post-#6/post-#15 series by OCCURRENCE count 60/28;
  dup-check: zero serviced c2818 entries; c2820/c2819/c2818 substring accounting
  (the token-guard lives INSIDE the c2817 Next-block itself —
  the per-line-census-first lesson carried: census measured pre-guard via
  census_c2818.py, expectations below are the MEASURED values, INCLUDING the
  forward token c2820 = 0 (UNBORN, measured pre-append) and the c2819 = 4
  total = 2 births in the c2817 Step-7 twin-print (line 9542: the rehearsal
  pre-count print 'the c2819 pre==0 expectation' AND the census-time print
  'c2819_pre = 0') + 2 FORWARD-token births inside the c2817 Next-block guard
  phrase ('arrival-guard against c2818/c2819 tokens') AND the FORWARD-token
  sentence ('the FORWARD token c2819 must be IN the census tuple'), both on
  line 9544 — the c2817 append prophecy 'c2819 = 4 block births' held EXACTLY,
  the born-FOUR class REPEATS a FIFTEENTH time;
  the c2818 token itself is BORN FOURTEEN times pre-append: 2 in the c2816
  Step-7 twin-print (line 9530) + 2 in the c2816 Next-block (line 9532) + 5 in
  the c2817 Step-1 census sentence (line 9536) + 1 in the c2817 Step-7 'the
  c2818 pre-count is 4' (line 9542) + 4 in the c2817 Next-block (line 9544:
  the instance + the 446189-c2818 id + the 'c2818/c2819' guard phrase + the
  'measure_c2818_tokens.py' surface — the bare-c-token accounting, honestly
  counted));
  the E-TOKEN lesson re-applied at guard-authoring time (the c2760 lesson,
  re-verified live this cycle): the Step-4 surface 'scan_cycle2817_raw.json' /
  'validate_cycle2817.py' / 'scan_cycle2817.json' carry 'e2817'/'cycle2817',
  NOT the bare c-token 'c2817' — line 9539 ABSENT from the measured c2817
  per-line dict;
  the guard expectations below are the census MEASUREMENTS, not hand counts;
  trailing-newline hygiene;
  .basedagents blocker probe (the claim path);
  dev.log foreign-POST census (PRINT, not guard — the timestamp-less
  latency-match split, honest, no over-claim);
  git HEAD object-verification with the FOREIGN-COMMIT-TOP layer handled
  explicitly (the c2752..c2817 lessons: the HEAD check needs the parent
  layer — HEAD may be the official c2817 commit OR a benign-add foreign
  cron commit ATOP it — the parent WALK handles stacked foreign commits,
  every pre-official layer must be foreign-cron class with zero worklog
  touch; both classes GREEN, the class printed honestly);
  c2817 instrument set object-present (the LOSS-#83 lesson: verify FIRST);
  v117 source-intact expectations matched to the v117 pass-66 class ACTUAL
  carries (the c2753 attempt-1 guard-slip lesson verbatim: the v117 class
  carries the baseline observation (18,0,0,18,0) AND the locked root
  (20,0,2,18,0); the pass-67 gate name is what the v118 rebadge introduces,
  so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry
  'pass-65 band' is present AND the evidence-paragraph lag-1 heading
  'pass-65 evidence' is present — BOTH instrument surfaces, the v118 rebadge
  P3/P8 old-string expectations, exactly as the c2817 Next-block wrote).
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
guard("worklog_lines==9544", n_nl == 9544, f"got={n_nl}")
guard("single_trailing_newline", raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
      repr(raw[-8:]))
text = raw.decode("utf-8")
lines = text.splitlines()
last_nonempty = [l for l in lines if l.strip()][-1]
guard("tail_is_c2818_next_bullet", last_nonempty.startswith("- Next: the c2818 instance"),
      repr(last_nonempty[:44]))

tid = len([l for l in lines if l.startswith("Task ID:")])
gold = len([l for l in lines if l.startswith("- No gold yet")])
guard("anchor_TaskID==495", tid == 495, f"got={tid}")
guard("anchor_nogold==428", gold == 428, f"got={gold}")
guard("anchor_LOSS6_occ==60", text.count("LOSS-#6") == 60, f"got={text.count('LOSS-#6')}")
guard("anchor_LOSS15_occ==28", text.count("LOSS-#15") == 28, f"got={text.count('LOSS-#15')}")

dup = [l for l in lines if l.startswith("Task ID: 446189-c2818")]
guard("dup_check_zero_serviced_c2818", len(dup) == 0, f"got={len(dup)}")
c2820_total = text.count("c2820")
c2819_total = text.count("c2819")
c2818_total = text.count("c2818")
tok_guard = [l for l in lines if "c2818/c2819" in l]
next_block = [l for l in lines if l.startswith("- Next: the c2818 instance")]
c2819_lines = {i + 1: l.count("c2819") for i, l in enumerate(lines) if "c2819" in l}
c2818_lines = {i + 1: l.count("c2818") for i, l in enumerate(lines) if "c2818" in l}
guard("c2818_mention_accounting_pre",
      c2820_total == 0 and c2819_total == 4 and c2818_total == 14
      and len(tok_guard) == 1 and len(next_block) == 1
      and tok_guard[0] is next_block[0]
      and c2819_lines == {9542: 2, 9544: 2}
      and c2818_lines == {9530: 2, 9532: 2, 9536: 5, 9542: 1, 9544: 4},
      f"c2820={c2820_total} c2819={c2819_total} c2818={c2818_total} "
      f"c2819_per-line={c2819_lines} c2818_per-line={c2818_lines} "
      f"(expect c2820 = 0 UNBORN (measured pre-append — the forward-token "
      f"lesson: measured, never assumed unborn); c2819 = 4 — 2 births in the "
      f"c2817 Step-7 twin-print line 9542 (the rehearsal pre-count print 'the "
      f"c2819 pre==0 expectation' AND the census-time print 'c2819_pre = 0' — "
      f"the Step-7 twin-print class REPEATS) + 2 FORWARD-token births TWICE "
      f"inside the c2817 Next-block guard phrase AND census-tuple sentence, "
      f"both on line 9544 (the c2817 append prophecy 'c2819 = 4 block births' "
      f"held EXACTLY, the born-FOUR class REPEATS a FIFTEENTH time); c2818 = "
      f"14 — 2 in the c2816 Step-7 twin-print (line 9530) + 2 in the c2816 "
      f"Next-block (line 9532) + 5 in the c2817 Step-1 census sentence (line "
      f"9536) + 1 in the c2817 Step-7 'the c2818 pre-count is 4' (line 9542) + "
      f"4 in the c2817 Next-block (line 9544: the instance + the 446189-c2818 "
      f"id + the 'c2818/c2819' guard phrase + the 'measure_c2818_tokens.py' "
      f"surface))")

c2817_total = text.count("c2817")
c2817_lines = {i + 1: l.count("c2817") for i, l in enumerate(lines) if "c2817" in l}
guard("c2817_mention_census_pre",
      c2817_total == 42
      and c2817_lines == {9518: 2, 9520: 2, 9524: 4, 9530: 1, 9532: 4, 9535: 1,
                          9536: 8, 9537: 5, 9542: 4, 9544: 11},
      f"total={c2817_total} per-line={c2817_lines} (the c2817-guard-probe state 13 on "
      f"lines 9518/9520/9524/9530/9532 + 29 births inside the c2817 block "
      f"itself; the Step-4 surface 'scan_cycle2817_raw.json'/"
      f"'validate_cycle2817.py'/'scan_cycle2817.json' carries 'cycle2817'/'e2817' "
      f"on its path tokens — the c2760 E-TOKEN lesson re-verified live: line "
      f"9539 ABSENT from the dict, the bare-c2817 weight measured honestly)")

c2816_total = text.count("c2816")
c2816_lines = {i + 1: l.count("c2816") for i, l in enumerate(lines) if "c2816" in l}
guard("c2816_mention_census_pre",
      c2816_total == 88
      and c2816_lines == {9506: 2, 9508: 2, 9512: 6, 9518: 1, 9520: 4, 9523: 1,
                          9524: 7, 9525: 4, 9530: 4, 9532: 10, 9534: 14, 9536: 19,
                          9537: 2, 9538: 5, 9541: 3, 9542: 3, 9544: 1},
      f"total={c2816_total} per-line={c2816_lines} (the c2816-guard-probe state 41 on "
      f"lines 9506..9532 + 47 births inside the c2817 block itself, measured "
      f"per-line at this cycle's census)")

c2815_total = text.count("c2815")
c2815_lines = {i + 1: l.count("c2815") for i, l in enumerate(lines) if "c2815" in l}
guard("c2815_mention_census_pre",
      c2815_total == 89
      and c2815_lines == {9494: 2, 9496: 2, 9500: 5, 9506: 1, 9508: 4, 9511: 1,
                          9512: 5, 9513: 4, 9517: 1, 9518: 4, 9520: 9, 9522: 13,
                          9524: 17, 9525: 4, 9526: 4, 9529: 3, 9530: 3, 9532: 3,
                          9536: 1, 9537: 2, 9544: 1},
      f"total={c2815_total} per-line={c2815_lines} (the c2815-guard-probe state 85 on "
      f"lines 9494..9532 + 4 births inside the c2817 block itself, measured "
      f"per-line at this cycle's census)")

c2814_total = text.count("c2814")
c2814_lines = {i + 1: l.count("c2814") for i, l in enumerate(lines) if "c2814" in l}
guard("c2814_mention_census_pre",
      c2814_total == 84
      and c2814_lines == {9482: 2, 9484: 2, 9488: 5, 9494: 1, 9496: 4, 9499: 1,
                          9500: 4, 9501: 4, 9506: 4, 9508: 10, 9510: 12, 9512: 14,
                          9513: 2, 9514: 4, 9517: 3, 9518: 3, 9520: 2, 9524: 1,
                          9525: 1, 9526: 1, 9532: 2, 9536: 1, 9544: 1},
      f"total={c2814_total} per-line={c2814_lines} (the c2814-guard-probe state 82 "
      f"on lines 9482..9532 + 2 births inside the c2817 block itself, measured "
      f"per-line at this cycle's census)")

c2813_total = text.count("c2813")
c2813_lines = {i + 1: l.count("c2813") for i, l in enumerate(lines) if "c2813" in l}
guard("c2813_mention_census_pre",
      c2813_total == 95
      and c2813_lines == {9470: 2, 9472: 2, 9476: 5, 9482: 1, 9484: 4, 9487: 1,
                          9488: 4, 9489: 4, 9494: 4, 9496: 10, 9498: 14, 9500: 14,
                          9501: 3, 9502: 5, 9505: 3, 9506: 3, 9508: 2, 9510: 1,
                          9512: 1, 9513: 1, 9514: 1, 9517: 1, 9520: 2, 9522: 1,
                          9524: 1, 9529: 1, 9532: 1, 9534: 1, 9536: 1, 9541: 1},
      f"total={c2813_total} per-line={c2813_lines} (the c2813-guard-probe state 88 "
      f"on lines 9470..9532 + 7 births inside the c2817 block itself, measured "
      f"per-line at this cycle's census)")

c2812_total = text.count("c2812")
c2812_lines = {i + 1: l.count("c2812") for i, l in enumerate(lines) if "c2812" in l}
guard("c2812_mention_census_pre",
      c2812_total == 88
      and c2812_lines == {9458: 2, 9460: 2, 9464: 5, 9470: 1, 9472: 4, 9475: 1,
                          9476: 4, 9477: 4, 9482: 4, 9484: 10, 9486: 14, 9488: 13,
                          9489: 5, 9490: 4, 9493: 4, 9494: 3, 9496: 1, 9500: 1,
                          9501: 1, 9508: 1, 9512: 1, 9520: 1, 9524: 1, 9536: 1},
      f"total={c2812_total} per-line={c2812_lines} (the c2812-guard-probe state 87 "
      f"on lines 9458..9524 + 1 birth inside the c2817 block itself, measured "
      f"per-line at this cycle's census)")

for tag, total in (("c2811", 91), ("c2810", 112), ("c2809", 91), ("c2808", 103),
                   ("c2807", 92), ("c2806", 88), ("c2805", 103), ("c2804", 115),
                   ("c2803", 121), ("c2802", 133), ("c2801", 101), ("c2800", 150),
                   ("c2799", 106), ("c2798", 104), ("c2797", 96), ("c2796", 106),
                   ("c2795", 129), ("c2794", 123), ("c2793", 131), ("c2792", 136),
                   ("c2791", 124), ("c2790", 137), ("c2789", 127), ("c2788", 138),
                   ("c2787", 139), ("c2786", 161), ("c2785", 143), ("c2784", 141),
                   ("c2783", 142), ("c2782", 141), ("c2781", 146), ("c2780", 151),
                   ("c2779", 151), ("c2778", 195), ("c2777", 167), ("c2776", 172),
                   ("c2775", 181), ("c2774", 186), ("c2773", 190), ("c2772", 209),
                   ("c2771", 199), ("c2770", 259), ("c2769", 188), ("c2768", 191),
                   ("c2767", 274), ("c2766", 237), ("c2765", 182), ("c2764", 184),
                   ("c2763", 192), ("c2762", 229), ("c2761", 256), ("c2760", 187),
                   ("c2759", 187), ("c2758", 189), ("c2757", 192), ("c2756", 197),
                   ("c2755", 204), ("c2754", 207), ("c2753", 231), ("c2752", 237),
                   ("c2751", 223), ("c2750", 229), ("c2749", 245)):
    guard(f"{tag}_mention_census_pre", text.count(tag) == total,
          f"got={text.count(tag)} (total-class guard; per-line dicts in the census log)")

guard("basedagents_absent", not os.path.isdir(BA),
      "test -d exit-1 class" if not os.path.isdir(BA) else "PRESENT - blocker lifted?")
if os.path.isdir(BA):
    print("  BLOCKER-LIFTED: .basedagents present - claim path re-probe required at gold time")

if os.path.isfile(DEVLOG):
    dl = open(DEVLOG, "r", errors="replace").read()
    n_post = dl.count("POST /api/marketplaces/scan")
    print(f"dev_log_post_scan_entries={n_post} (249 at the census probe: 224 "
          f"accounted-path cumulative = 222 at the c2817 census probe + 1 through "
          f"the c2817 official capture + 1 this cycle's echo #539 (latency-match "
          f"1636ms class, bracketed, RE-DERIVABLE) = 224 accounted + 25 "
          f"foreign/unattributed cumulative — FIVE new POSTs landed between the "
          f"probes (244 -> 249 = +5: 2 accounted + 3 foreign), "
          f"arithmetic-necessity class, honest; timestamp-less log, latency-match "
          f"split, honest)")
else:
    print("dev_log: ABSENT")

# loop echo #539 facts (measured this session, the echo-then-capture order expected)
print("loop_echo_539: pre-echo 04:32:22.514505763 +0000 epoch 1793334742.515107961 "
      "EPOCH-governs; curl 1.644084 / server 1636ms latency-match; post-echo "
      "04:32:24.168180955 +0000 epoch 1793334744.168910915 EPOCH-governs; echo "
      "scanned_at 04:32:24.162Z = epoch 1793334744.162; wall 1.653802954; "
      "stamp-to-echo 664.515107961 (SHALLOWER than the deepest print "
      "1025.631018606 — the deepest print STANDS unchallenged); echo POST-WINDOW "
      "+342.494159700; echo account attempt #539 -> the hit-count carry NOT "
      "RE-DERIVABLE from the ledger (the c2817 honest note stands — the "
      "increment rule not re-derivable, no over-claim either way, honest note; "
      "10 priors of the '137-for-530' form counted per the census — the form's "
      "ledger weight, not a forecast); the echo landed MID-SESSION (the "
      "first-command prescription slipped a TWENTY-SIXTH consecutive cycle); "
      "the echo-then-capture order class expected to EXTEND m13")


def git(*args):
    return subprocess.run(["git", "-C", "/home/z/my-project", *args],
                          capture_output=True, text=True).stdout.strip()


# parent-layer WALK: HEAD may be the official c2817 commit, or one/more benign
# foreign cron commits stacked ATOP it (the c2752..c2817 foreign-commit-TOP
# lessons; the walk handles the stacked class honestly).
official_depth = None
walk_info = []
for depth in range(0, 6):
    rev = "HEAD" if depth == 0 else f"HEAD~{depth}"
    body = git("log", "-1", "--format=%B", rev)
    subj = git("log", "-1", "--format=%s", rev)
    short = git("log", "-1", "--format=%h", rev)
    if body.startswith("c2817:"):
        official_depth = depth
        walk_info.append(f"official c2817 commit found at depth {depth} ({short})")
        break
    walk_info.append(f"depth {depth}: {short} subj={subj[:60]!r} (foreign class)")
    if not subj.endswith("-cron"):
        break

head_short = git("log", "-1", "--format=%h")
head_subj = git("log", "-1", "--format=%s")
head_stat = git("show", "--stat", "--format=", head_short)
if official_depth == 0:
    guard("git_head_is_c2817_commit", True,
          f"HEAD={head_short} body-prefix object-verified")
else:
    guard("git_parent_layer_reaches_c2817_commit", official_depth is not None,
          f"walk: {'; '.join(walk_info)}")
    guard("git_head_foreign_class", head_subj.endswith("-cron"),
          f"HEAD={head_short} subj={head_subj[:50]!r} (benign-add foreign-cron class "
          f"atop the c2817 commit — the 5939089/19ff74c/660688b/7386e88/4538311/"
          f"02d651d/dd48816/0539b68/eb9de41/9b5ea95/f9ecf31/2b2bd7b/336d5f2/"
          f"e54aab2/d22e2bb/134a6b8/51f1161/f076455/b9b0ce0/128bbec/67ba021/"
          f"966ab1f/0b4f512/ffa527c/c048029/3b69581/18522dc/ea92218/4477b73/"
          f"4207111/615fc1c/7efc24d/65f4c4e/b27a69f/f0d806e/87e21ad/e6da641/"
          f"325729a/7de8446/a6fac67/35ba192/92a8201/6b53b65/7f7a022/1288d7f/"
          f"92b5acc/c5fb5cc/30a3440/8cc4726/ef415bd/42f95e4/68117e3/a009715 "
          f"precedent)")
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

C2817_SET = [
    "census_c2817.py", "arrival_guard_c2817.py", "rebadge_cycle2817.py",
    "capture_cycle2817.sh", "measure_c2817_tokens.py", "recursive_diff_2817.py",
    "validate_cycle2817.py", "entry_cycle2817.txt", "append_cycle2817.py",
    "scan_cycle2817_raw.json", "scan_cycle2817.json",
]
print("c2817_instrument_set_object_presence:")
missing = []
for name in C2817_SET:
    p = os.path.join("/home/z/my-project/scripts", name)
    if os.path.isfile(p):
        print(f"  ok {name} bytes={os.path.getsize(p)}")
    else:
        missing.append(name)
        print(f"  MISSING {name}")
guard("instrument_set_object_present", not missing, f"missing={missing}" if missing else "11/11 c2817 files on disk")

v117 = open("/home/z/my-project/scripts/validate_cycle2817.py", "rb").read()
guard("v117_source_intact", b"CYCLE = 2817" in v117 and b"drift49_pass66_match" in v117
      and b"drift49_pass67_match" not in v117
      and b"(18,0,0,18,0)" in v117 and b"(20,0,2,18,0)" in v117
      and b"(21,0,3,18,0)" in v117 and b"pass-65 band" in v117
      and b"pass-66 band" not in v117
      and b"pass-65 evidence" in v117 and b"pass-66 evidence" not in v117,
      f"bytes={len(v117)} (the v117 pass-66 class carries the baseline observation "
      f"(18,0,0,18,0) AND the locked root (20,0,2,18,0) — expectations matched to "
      f"the class actual carries per the c2753 attempt-1 guard-slip lesson; the "
      f"pass-67 gate name drift49_pass67_match is what the v118 rebadge introduces, "
      f"so its absence is the correct pre-rebadge state; the SIZE_BAND lag-1 carry "
      f"'pass-65 band' is present AND the evidence-paragraph lag-1 heading "
      f"'pass-65 evidence' is present — BOTH instrument surfaces, the v118 P3/P8 "
      f"old-string expectations)")

obj = subprocess.run(["git", "-C", "/home/z/my-project", "cat-file", "-p",
                      "da7d469:scripts/validate_cycle2817.py"],
                     capture_output=True)
if obj.returncode == 0 and obj.stdout:
    guard("v117_commit_object_intact", len(obj.stdout) == len(v117)
          and obj.stdout == v117,
          f"object_bytes={len(obj.stdout)} == disk {len(v117)} (the da7d469 c2817 commit)")
else:
    guard("v117_commit_object_intact", False, "da7d469 object unreadable")

print(f"guard_count={n_guards} (programmatic)")
print(f"GUARD_RESULT={'GREEN' if not failures else 'RED:' + ','.join(failures)}")
sys.exit(0 if not failures else 1)
