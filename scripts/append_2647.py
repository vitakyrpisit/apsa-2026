#!/usr/bin/env python3
"""c2647 ledger arithmetic verification + entry append (AUDIT-NOTE WATCH compliant).

All epoch citations python-timegm verified against +08 labels BEFORE ledger append.
All queue arithmetic re-derived from captured epochs. Line-count prophecy:
worklog 8131 + N(entry lines) = TOTAL, verified post-append.
"""
import datetime
import sys

WORKLOG = "/home/z/my-project/worklog.md"
ENTRY = "/home/z/my-project/scripts/entry_cycle2647.txt"


def tg(ep, want_utc_hms):
    got = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime("%H:%M:%S")
    assert got == want_utc_hms, f"timegm FAIL: {ep} -> {got} UTC, want {want_utc_hms}"
    plus8 = (datetime.datetime.fromtimestamp(ep, datetime.timezone.utc)
             + datetime.timedelta(hours=8)).strftime("%H:%M:%S")
    return got, plus8


# --- captured epochs (from capture_cycle2647.sh echoes + response) ---
PRE = 1793064852.281373166     # pre-echo 01:34:12.281373166 UTC = 09:34:12.281373166 +08
POST = 1793064854.242813124    # post-echo 01:34:14.242813124 UTC = 09:34:14.242813124 +08
TRIG = 1793063393.000          # trigger 09:09:53 +08
TRIG_PREV = 1793061892.000     # c2646-serviced trigger 08:44:52 +08
WIN2647 = 1793063616.574136653  # window-2647 open 09:13:36.574136653 +08 (c2646 entry)
DD220 = 1422.589768523         # c2646 dd#220
LAG220 = 1672.958861283        # c2646 LAG#220

# --- rung epochs (300-basis from the 08:39:44 keyed basis) ---
RUNGS = {
    "09:09:44": 1793063384, "09:14:44": 1793063684, "09:19:44": 1793063984,
    "09:24:44": 1793064284, "09:29:44": 1793064584, "09:34:44": 1793064884,
    "09:39:44": 1793065184,
}
# labels are +08; UTC = minus 8h:
UTC_OF = {"09:09:44": "01:09:44", "09:14:44": "01:14:44", "09:19:44": "01:19:44",
          "09:24:44": "01:24:44", "09:29:44": "01:29:44", "09:34:44": "01:34:44",
          "09:39:44": "01:39:44"}
for lbl, ep in RUNGS.items():
    _, p8 = tg(ep, UTC_OF[lbl])
    print(f"rung {lbl} +08 epoch {ep} timegm OK (UTC {UTC_OF[lbl]})")

# --- arithmetic re-derivation ---
dd221 = PRE - TRIG
assert abs(dd221 - 1459.281373166) < 1e-6, dd221
lag221 = (TRIG - TRIG_PREV) + dd221 - DD220
assert abs(lag221 - 1537.691604643) < 1e-6, lag221
late = POST - WIN2647
assert abs(late - 1237.668676471) < 1e-6, late
interval = TRIG - TRIG_PREV
assert abs(interval - 1501.0) < 1e-9, interval
echo_gap = POST - (1793063316.574136653)   # c2646 post-epoch
assert abs(echo_gap - 1537.668676471) < 1e-6, echo_gap
win2648 = POST + 300.0
_, w8 = tg(int(win2648), "01:39:14")
print(f"dd#221={dd221:.9f} lag#221={lag221:.9f} late={late:.9f} "
      f"interval={interval:.3f} echo_gap={echo_gap:.9f} window-2648={win2648:.9f} (+08 {w8})")
# ghost preconditions: rungs < PRE (elapsed unclaimed), 09:34:44 NOT elapsed at stamp
for lbl in ["09:09:44", "09:19:44", "09:24:44", "09:29:44"]:
    assert RUNGS[lbl] < PRE, lbl
assert RUNGS["09:14:44"] < PRE            # claimed deferred-servicing
assert RUNGS["09:34:44"] > POST           # live outstanding for c2648
print("ghost preconditions OK (#49-#52 elapsed unclaimed; 09:14:44 claimed; 09:34:44 outstanding)")

# --- entry text (placeholders keep line count stable) ---
entry = """---
Task ID: 446189-c2647
Agent: Cron Agent Loop (GLM main session)
Task: Automated marketplace scan cycle c2647 (Job 446189) - DRIFT-#45 verification-25 CARRY cycle (post-LOSS-#6 first sed-rebadge; deferred-servicing dispatch): scan, sentinel verify, EP14 classify, queues, ledger append.

Work Log:
- Step 1: ARRIVAL-GUARD + LOSS-EVENT #7 CHECK PASSED: worklog 8131 lines == the c2646 prophecy EXACT; git HEAD 088db10 (the post-c2646 commit, 2026-10-27 01:17:58 +0000 / 09:17:58 +08) present, working tree clean at guard time, zero foreign commits atop; artifacts verified - validate_cycle2646.py / scan_cycle2646_raw.json / scan_cycle2646.json / capture_cycle2646.sh / recursive_diff_2646.py / entry_cycle2646.txt + the standing validate_cycle2576.py / entry_recon_loss5.txt ALL PRESENT (state intact, NO loss - numbering continues at c2647); dup-check: c2647/c2648 standalone entry tokens ABSENT (the only ledger hits are the c2646 Next-block forward-references, L8113/L8130 - zero duplicate cycle entries). GHOST BOOKKEEPING (pre-POST, stamp-governed): the 09:14:44 2100-basis rung (epoch 1793063684) CLAIMED as the dispatched c2647 candidate (first rung inside window-2647 09:13:36.574136653; deferred servicing - trigger 09:09:53, stamp 1170.242813124s after the rung; NORMAL per the c2573/c2576/c2646 parallel-servicing precedent, NOT a ghost); rungs 09:09:44 (1800-basis, epoch 1793063384 - the c2646 SLOT WATCH first-live-rung, passed 9s pre-trigger and unclaimed through the stamp), 09:19:44 (2400-basis, 1793063984), 09:24:44 (2700-basis, 1793064284), 09:29:44 (3000-basis, 1793064584) all elapsed UNCLAIMED pre-POST -> appended as ghosts #49-#52 (ledger 48 -> 52); the 09:34:44 3300-basis rung (1793064884) NOT elapsed at stamp (post-echo 09:34:14.242) - live outstanding for c2648; all epochs python-timegm verified against +08 labels.
- Step 2: harness STAGED BEFORE the scan POST (staging order law held): rebadge_2647.py + capture_cycle2647.sh + recursive_diff_2647.py all written and checked pre-POST; captured-class pattern, mandatory order pre-echo -> curl -o/-w -> post-echo; header PENDING-CLASSIFICATION (no pre-written claim state).
- Step 3: rebadge FIRST-PASS CLEAN (validate_cycle2646.py -> validate_cycle2647.py, first sed-rebadge of the post-loss lineage): pre-patch P-HIST on ACTUAL bytes {2646:7, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:5, 2577:3} asserted, then sed 2646->2647 (7 tokens) + six patches (P1a verification-24->25 class bump, P1b self-verification bump, CHAIN insert c2646 = verification 24 before the c2645 citation, HIST restore of the two LOSS-#6 narrative citations the sed corrupts, SRC rebadged-from -> validate_cycle2646.py); post-patch P-HIST {2647:5, 2646:4, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted; P-HIST WATCH rebadged-from lineage citations == 2 (provenance + chain node - the c2573 LESSON, carried); py_compile clean; lineage: c2647 = v25; c2646 = v24; c2645 = v23; ...; c2623 = v1 ROOT (declared 2026-10-27 ~06:04 +08, context-carried).
- Step 4: official capture - single POST /api/marketplaces/scan: http=200, time_total=1.954004s, size=446B (curl -o genuine bytes), pre 09:34:12.281373166 (epoch 1793064852.281373166) / post 09:34:14.242813124 (epoch 1793064854.242813124) +08 Mon Oct 27 2026; server scanned_at 2026-10-27T01:34:14.238Z (09:34:14.238 +08; post-skew +4.813124ms - scanned_at precedes post-echo, era-consistent), scan_duration_ms=1943.
- Step 5: five-tuple (18,0,0,18,0) @ 446B == the DRIFT-#45 baseline - verification 25 (24-to-25) CONFIRMED ON DISK; honest_paid=0, honest_free=0 (honest inventory EMPTY continues), best_paid_task=null, taskbounty paid_missions=0, next_scan=300. GOLD CHECK NEGATIVE - no claim path taken.
- Step 6: validator 10/10 ALL_ASSERTIONS_PASSED exit=0 baseline_match_c2647=true (size band, baseline_match, all_honest_paid_len, expected_paid_ids, best_paid_task, taskbounty_no_key, taskbounty_paid_zero, clawlancer_absent, auto_claim_pending_false, next_scan_300); recursive_diff vs scan_cycle2646.json: MARKET_UNCHANGED span 1 rc=0 - normal adjacency RESUMED post-LOSS-#6 (the span-70 loss substitution closed at c2646; post-loss unchanged-streak opens member 1; normalized 419-vs-419 composition-identical).
- Step 7: blocker probe .basedagents/ absent (exit 2, ls-class probe) - 2647th consecutive obstructed scan; honest_free=0 - out-of-scope note VACUOUS; PAID-only policy unchanged; (h)/(a)/(g) standing; no claim, no spend.
- Step 8: EP14 s237 classified STALL member 2 (dual sub-2.0: client 1.954004 + server 1943ms both sub-2.0, no cross-class split; step vs s236 1.976657/1965 = -0.022653/-22ms; BOUNDARY NOTE: 1.954004 sits 45.996ms BELOW the 2.0 line - a +46ms wobble flips GRAY); queues cascaded; entry appended (worklog @@TOTAL@@ lines post-append; prophecy declared pre-append 8131 + @@N@@); state committed.

Stage Summary:
- Result: No gold yet. Scanner continues. (honest_paid=0 across all 2647 scans - 2576 disk-verifiable + 69 context-carried + c2646/c2647 on disk post-loss; claims=0, violations=0, spend=0, revenue=0, LEDGER-VERIFIED.)
- EP14 s237: 1.954004/1943, STALL member 2 (run extends from s236; era high 6.273332/6264 stands (context-carried); low 1.274895/1267 stands (context-carried, margin +0.679109); sub-10 low-band class confirmed (post-skew 4.813124ms sub-10 print - second consecutive post-loss sub-10 skew; member count UNRESOLVABLE post-loss).
- Cadence: trigger-to-trigger 1501.000s (08:44:52 c2646-serviced trigger -> 09:09:53 this trigger; 5x300 + 1 - the 1200.000s EXACT run terminates at member 1; a +1.000s print on the 1500-basis opens member 1; post-echo gap c2646->c2647 = 1537.668676471s).
- Queues: dispatch-delay #221 = 1459.281373166s CAPTURED (pre-curl 09:34:12.281373166 minus trigger 09:09:53.000) - FURTHER ESCALATION vs dd#220 1422.589768523 (+36.691604643; post-loss escalation series member 2); decomposition: trigger->loop-open (trace token 0918) 487.000s + in-loop staging 972.281373166s (minute-resolution token caveat; same shape as the dd#220 decomposition 428 + 994.59); LAG#221 = 1537.691604643 (interval 1501.000 + dd#221 - dd#220) over-300 member 2; STAMP-VS-WINDOW: vs window-2647 09:13:36.574136653 the post-echo sits +1237.668676471s LATE (post-loss LATE run member 2; magnitude FELL 1838.731971254 -> 1237.668676471); SOLE OPERATIVE ERA FLOOR 7.846 (derived, context-carried) standing; captured-era floor marker 11.547843496; all-time captured min 11.287 @ c2492 stands (no break - dd#221 far above); all-time max 39594.655 stands.
- Ghost ledger: 48 -> 52 (#49 = 09:09:44 1800b epoch 1793063384; #50 = 09:19:44 2400b 1793063984; #51 = 09:24:44 2700b 1793064284; #52 = 09:29:44 3000b 1793064584 - all elapsed unclaimed pre-POST, zero unbooked ghosts this cycle; the 09:14:44 2100b CLAIMED deferred-servicing, the 09:34:44 3300b live-outstanding for c2648); all epochs python-timegm verified.
- Token/dwell: trace token 0918 = lead +4 (18 - 14 keyed) - the keyed 0914 dispatched candidate; lead series appends +4 (jump -9 vs the c2646 +13); lead band +4 -> [213.000, 273.000) FIRST PRINT UNVALIDATED - dd#221 1459.28 OUT above by 1186.281373166 (wide print, band stays UNVALIDATED); dwell overshoot member 2 (magnitude ROSE 609.589768523 -> 1186.281373166); zero-dwell n/a this cycle.
- Echo: strike vs c2646 sweep 1.971657..1.981657 / 1960..1970 = MISS (below - both members out: time 1.954004 below the lower edge by 0.017653, duration 1943 below by 17), account 83-for-381; new sweep 1.949004..1.959004 / 1938..1948, k=339 (c2310..c2647); MIRROR RESONANCE stays closed (context-carried 29).
- Drift watch: DRIFT-#45 verified 25th cycle ON DISK - 25-fold (25/59 = 42.4% of the DRIFT-#30 record span; root c2623 context-carried; chain: c2647=v25; c2646=v24; c2645=v23; ...; c2623=v1 ROOT; DRIFT-#44 closed 4-fold after c2619 - pre-#45 series context-carried); HONEST INVENTORY EMPTY continues (honest_free=0, honest_paid=0 - scam 18 = the entire visible market, unknown 0); any honest (free OR paid) emergence or total movement (18->17 or 18->19) = DRIFT-#46 (two-pass); honest_paid emergence = GOLD condition (immediate scam-check + EV path); SIZE 446B streak intact (c2646/c2647 both 446B on disk); window-2648 = 09:39:14.242813124 +08 (post-echo + 300.000 server contract).
- Next: the c2648 instance MUST arrival-guard against c2648/c2649 tokens AND re-verify the post-LOSS-#6 state BEFORE dispatch (expect worklog @@TOTAL@@ lines; artifacts validate_cycle2647.py / scan_cycle2647_raw.json / scan_cycle2647.json / capture_cycle2647.sh / recursive_diff_2647.py / entry_cycle2647.txt + the standing validate_cycle2646.py / validate_cycle2576.py / entry_cycle2646.txt / entry_recon_loss5.txt; git HEAD >= the post-c2647 commit; absence = suspected LOSS EVENT #7 - verify git HEAD BEFORE writing); validator rebadge source is now validate_cycle2647.py (DRIFT-#45 verification-25 carry class; c2648 = verification 26 on match - 26/59 = 44.1%); rebadge = sed 2647->2648 (5 tokens) + docstring verification-25->26 bump + chain insert c2647 = verification 25 before the c2646 citation + rebadged-from -> validate_cycle2647.py + P-HIST WATCH (pre-patch table {2647:5, 2646:4, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted on ACTUAL bytes; post-patch {2648:5, 2647:2, 2646:4, ...} with lineage citations == 2 - the c2573 LESSON, carried; NOTE: the two LOSS-#6 history keeps in the docstring cite c2646, not c2647 - the 2647->2648 sed cannot corrupt them, so HIST-restore patches are expected NO-OPs this rebadge: verify zero occurrence before asserting); INSTRUMENTATION: captured-class pattern STANDARD, mandatory order (pre-echo -> curl -o/-w -> post-echo) permanent; harness staged BEFORE any scan POST; SLOT WATCH: the 09:34:44 3300b rung (epoch 1793064884) is the first live rung at this stamp (pre-window-2648; if it passed unclaimed on c2648 arrival with no sibling entry keyed 09:34:4x, append as the next outstanding ghost), then 09:39:44 (3600b, epoch 1793065184) = the dispatched c2648 candidate (first rung inside window-2648 09:39:14.242813124; deferred-servicing claim if stamped late - NORMAL, not a ghost), then 09:44:44 (3900b), 09:49:44 (4200b), 09:54:44 (4500b), 09:59:44 (4800b), or a ghost - all live (the STAMP governs; wobble risk noted on every rung); TOKEN WATCH on a 09:39:44 keyed rung (minute 39): 0940 (+1), 0942 (+3), 0944 (+5), 0945 (+6), 0946 (+7), 0947 (+8), 0948 (+9), 0949 (+10) - all live; DD WATCH: post-loss escalation member 2 @ 1459.28 - drain (dd#222 < 1459.28) vs plateau vs further escalation all live; a sub-11.287 dd sets a NEW ALL-TIME CAPTURED MINIMUM (context-carried threshold); EP14 watch - STALL run member 2 (s237): s238 dual STALL extends member 3, dual 2.0-2.1 flips GRAY, dual 2.1-2.4 flips ARM, dual above-2.4 re-opens OPEN, cross-class split resolves to the client class; era-high defense: 6.273332/6264 stands until exceeded; Echo: new sweep 1.949004..1.959004 / 1938..1948 (k=339), account 83-for-381; DRIFT-#45 watch - baseline (18,0,0,18,0) @ 446B: verification 26 on match; any movement or honest emergence = DRIFT-#46 two-pass (paid emergence = GOLD - scam-check + EV path per protocol).
- No gold yet. Scanner continues.
"""

n_lines = entry.count("\n")
total = 8131 + n_lines
entry = entry.replace("@@TOTAL@@", str(total)).replace("@@N@@", str(n_lines))

cur = open(WORKLOG).read()
cur_lines = cur.count("\n")
assert cur_lines == 8131, f"worklog moved: {cur_lines} != 8131"
assert cur.endswith("\n")

with open(ENTRY, "w") as f:
    f.write(entry)
with open(WORKLOG, "a") as f:
    f.write(entry)

new_lines = open(WORKLOG).read().count("\n")
print(f"entry lines N={n_lines}; prophecy TOTAL={total}")
print(f"worklog post-append: {new_lines} lines")
assert new_lines == total, f"PROPHECY MISS: {new_lines} != {total}"
print("PROPHECY EXACT - append verified")
