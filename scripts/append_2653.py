#!/usr/bin/env python3
"""c2653 ledger arithmetic verification + entry append (AUDIT-NOTE WATCH compliant).

All epoch citations python-timegm verified against +08 labels BEFORE ledger append.
All queue arithmetic re-derived from captured epochs. Line-count prophecy:
worklog 8287 + N(entry lines) = TOTAL, verified post-append.
"""
import datetime

WORKLOG = "/home/z/my-project/worklog.md"
ENTRY = "/home/z/my-project/scripts/entry_cycle2653.txt"


def tg(ep, want_utc_hms):
    got = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime("%H:%M:%S")
    assert got == want_utc_hms, f"timegm FAIL: {ep} -> {got} UTC, want {want_utc_hms}"
    return got


# --- captured epochs (capture_cycle2653.sh echoes + response) ---
PRE = 1793068847.931665992     # pre-echo 02:40:47.931665992 UTC = 10:40:47.931665992 +08
POST = 1793068849.712362776    # post-echo 02:40:49.712362776 UTC = 10:40:49.712362776 +08
TRIG = 1793068194.000          # trigger 10:29:54 +08 (= 02:29:54 UTC)
TRIG_PREV = 1793067894.000     # c2652-serviced trigger 10:24:54 +08
WIN2653 = 1793068732.562005109  # window-2653 open 10:38:52.562005109 +08
DD226 = 536.699399805          # c2652 dd#226
POST_PREV = 1793068432.562005108  # c2652 post-echo epoch
RUNG_KEYED = 1793068784        # 10:39:44 7200b dispatched candidate

RUNGS = {
    "10:34:44": 1793068484, "10:39:44": 1793068784,
    "10:44:44": 1793069084, "10:49:44": 1793069384,
}
UTC_OF = {"10:34:44": "02:34:44", "10:39:44": "02:39:44",
          "10:44:44": "02:44:44", "10:49:44": "02:49:44"}
for lbl, ep in RUNGS.items():
    tg(ep, UTC_OF[lbl])
    print(f"rung {lbl} +08 epoch {ep} timegm OK")
tg(TRIG, "02:29:54")
tg(TRIG_PREV, "02:24:54")
print("triggers timegm OK")

# --- arithmetic re-derivation (float64 tolerance 1e-6; entry carries string-exact decimals) ---
dd227 = PRE - TRIG
assert abs(dd227 - 653.931665992) < 1e-6, dd227
lag227 = (TRIG - TRIG_PREV) + dd227 - DD226
assert abs(lag227 - 417.232266187) < 1e-6, lag227
late = POST - WIN2653
assert abs(late - 117.150357667) < 1e-6, late
interval = TRIG - TRIG_PREV
assert abs(interval - 300.0) < 1e-9, interval
echo_gap = POST - POST_PREV
assert abs(echo_gap - 417.150357668) < 1e-6, echo_gap
escal = dd227 - DD226
assert abs(escal - 117.232266187) < 1e-6, escal
band_out = dd227 + 27.000
assert abs(band_out - 680.931665992) < 1e-6, band_out
deferred = PRE - RUNG_KEYED
assert abs(deferred - 63.931665992) < 1e-6, deferred
loop_open = 486.000
staging = dd227 - loop_open
assert abs(staging - 167.931665992) < 1e-6, staging
win2654 = POST + 300.0
tg(int(win2654), "02:45:49")
upper_edge = WIN2653 + 300.0
inside_upper = upper_edge - POST
assert abs(inside_upper - 182.849642333) < 1e-6, inside_upper
print(f"dd#227={dd227:.9f} lag#227={lag227:.9f} late={late:.9f} interval={interval:.3f} "
      f"echo_gap={echo_gap:.9f} escal={escal:.9f} band_out={band_out:.9f} "
      f"deferred={deferred:.9f} staging={staging:.9f} window-2654={win2654:.9f} "
      f"inside_upper={inside_upper:.9f}")
# ghost preconditions (stamp-governed)
assert RUNGS["10:34:44"] < PRE            # elapsed unclaimed at arrival (pre-window-2653) - GHOST #60
assert RUNGS["10:39:44"] < PRE            # deferred-servicing claim: elapsed at stamp, consumed NOT ghost
assert RUNGS["10:44:44"] > PRE            # live outstanding for c2654
assert RUNGS["10:44:44"] < win2654        # pre-window-2654 note (likely next ghost unless sibling claims)
assert RUNGS["10:49:44"] > win2654        # dispatched c2654 candidate (first rung inside window-2654)
print("ghost preconditions OK (#60 10:34:44; 10:39:44 deferred-servicing claim; "
      "10:44:44 outstanding pre-window-2654; 10:49:44 dispatched c2654 candidate)")

# --- entry text (placeholders keep line count stable) ---
entry = """---
Task ID: 446189-c2653
Agent: Cron Agent Loop (GLM main session)
Task: Automated marketplace scan cycle c2653 (Job 446189) - DRIFT-#45 verification-31 CARRY cycle (post-LOSS-#6 seventh sed-rebadge; deferred-servicing dispatch): scan, sentinel verify, EP14 classify, queues, ledger append.

Work Log:
- Step 1: ARRIVAL-GUARD + LOSS-EVENT #13 CHECK PASSED: trigger 10:29:54 +08 arrived 300.000s EXACT after the c2652-serviced trigger (10:24:54) - this instance = c2653 per the c2652 Next-block dispatch; worklog 8287 lines == the c2652 prophecy EXACT; git HEAD 7fcdf7f (the post-c2652 commit itself, no cron commit atop), working tree clean at guard time, zero foreign commits; artifacts verified - validate_cycle2652.py / scan_cycle2652_raw.json / scan_cycle2652.json / capture_cycle2652.sh / recursive_diff_2652.py / entry_cycle2652.txt + the standing validate_cycle2651.py / validate_cycle2650.py / validate_cycle2649.py / validate_cycle2648.py / validate_cycle2647.py / validate_cycle2646.py / validate_cycle2576.py / entry_cycle2651.txt / entry_cycle2650.txt / entry_cycle2649.txt / entry_cycle2648.txt / entry_cycle2647.txt / entry_cycle2646.txt / entry_recon_loss5.txt ALL PRESENT (state intact, NO loss - numbering continues at c2653); dup-check: c2653/c2654 standalone entry tokens ABSENT (only the c2652 Next-block forward-references - zero duplicate cycle entries). Cadence: 300.000s EXACT (the 1200.000 EXACT print terminates at member 1; a 300.000 EXACT print opens member 1); the trigger fired while c2652 was mid-flight (c2652 post-echo 10:33:52 postdates this trigger 10:29:54) - the trigger queued and the loop opened at 10:38 (trace token 1038, 486.000s after the trigger stamp). All epochs python-timegm verified against +08 labels at guard FIRST-PASS (10:34:44 / 10:39:44 / 10:44:44 rungs + trigger + window-2653; UTC_OF mapping correct, second consecutive clean guard). GHOST BOOKKEEPING (pre-POST, stamp-governed): the 10:34:44 6900-basis rung (epoch 1793068484) passed UNCLAIMED at c2653 arrival (pre-window-2653 10:38:52.562005109, no sibling entry keyed 10:34:4x) - GHOST #60; the 10:39:44 7200-basis rung (1793068784) CLAIMED as the dispatched c2653 candidate - the stamp landed 63.931665992s AFTER the rung: DEFERRED-SERVICING claim, NORMAL per the c2649/c2650/c2651/c2652 precedent lineage - consumed, NOT a ghost; the 10:44:44 7500-basis rung (1793069084) NOT elapsed at stamp (236.068334008s future) - live outstanding for c2654 (pre-window-2654 - likely next ghost unless a sibling claims); ledger 59 -> 60 (one new ghost, zero unbooked).
- Step 2: harness STAGED BEFORE the scan POST (staging order law held): rebadge_2653.py + capture_cycle2653.sh + recursive_diff_2653.py all written and checked pre-POST; captured-class pattern, mandatory order pre-echo -> curl -o/-w -> post-echo; header PENDING-CLASSIFICATION (no pre-written claim state, deferred-servicing/EARLY contingency noted).
- Step 3: rebadge FIRST-PASS CLEAN (validate_cycle2652.py -> validate_cycle2653.py, seventh sed-rebadge of the post-loss lineage, fourth consecutive first-pass-clean): pre-patch P-HIST on ACTUAL bytes {2652:5, 2651:2, 2650:1, 2649:1, 2648:1, 2647:1, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted, then sed 2653 (5 tokens) + four patches (P1a verification-30->31 class bump, P1b self-verification bump, CHAIN insert c2652 = verification 30 before the c2651 citation, SRC rebadged-from -> validate_cycle2652.py); HIST-restore NO-OP verified (as prophesied); post-patch P-HIST {2653:5, 2652:2, 2651:1, 2650:1, 2649:1, 2648:1, 2647:1, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted; P-HIST WATCH rebadged-from lineage citations == 2; py_compile clean; lineage: c2653 = v31; c2652 = v30; c2651 = v29; c2650 = v28; c2649 = v27; c2648 = v26; c2647 = v25; ...; c2623 = v1 ROOT (context-carried).
- Step 4: official capture - single POST /api/marketplaces/scan: http=200, time_total=1.773656s, size=446B (curl -o genuine bytes), pre 10:40:47.931665992 (epoch 1793068847.931665992) / post 10:40:49.712362776 (epoch 1793068849.712362776) +08 Tue Oct 27 2026; server scanned_at 2026-10-27T02:40:49.708Z (10:40:49.708 +08; post-skew +4.712362776ms - scanned_at precedes post-echo, era-consistent), scan_duration_ms=1763.
- Step 5: five-tuple (18,0,0,18,0) @ 446B == the DRIFT-#45 baseline - verification 31 (30-to-31) CONFIRMED ON DISK; honest_paid=0, honest_free=0 (honest inventory EMPTY continues), best_paid_task=null, taskbounty paid_missions=0, next_scan=300. GOLD CHECK NEGATIVE - no claim path taken.
- Step 6: validator 10/10 ALL_ASSERTIONS_PASSED exit=0 baseline_match_c2653=true (size band, baseline_match, all_honest_paid_len, expected_paid_ids, best_paid_task, taskbounty_no_key, taskbounty_paid_zero, clawlancer_absent, auto_claim_pending_false, next_scan_300); recursive_diff vs scan_cycle2652.json: MARKET_UNCHANGED span 1 rc=0 - post-loss unchanged-streak member 7 (normalized 419-vs-419 composition-identical).
- Step 7: blocker probe .basedagents/ absent (exit 2, ls-class probe) - 2653rd consecutive obstructed scan; honest_free=0 - out-of-scope note VACUOUS; PAID-only policy unchanged; (h)/(a)/(g) standing; no claim, no spend.
- Step 8: EP14 s243 classified STALL member 3 (DUAL sub-2.0 extends: client 1.773656 < 2.0 AND server 1763ms < 2000 - the STALL run that re-opened at s241 extends member 3 per the standing watch); queues cascaded; entry appended (worklog @@TOTAL@@ lines post-append; prophecy declared pre-append 8287 + @@N@@); state committed.

Stage Summary:
- Result: No gold yet. Scanner continues. (honest_paid=0 across all 2653 scans - 2576 disk-verifiable + 69 context-carried + c2646..c2653 on disk post-loss; claims=0, violations=0, spend=0, revenue=0, LEDGER-VERIFIED.)
- EP14 s243: 1.773656/1763, STALL member 3 (dual sub-2.0 extends; step vs s242 1.855271/1846 = -0.081615/-83ms; era high 6.273332/6264 stands (context-carried); low 1.274895/1267 stands (context-carried, margin +0.498761); sub-10 low-band class confirmed (post-skew 4.712362776ms sub-10 print - eighth consecutive post-loss sub-10 skew; member count UNRESOLVABLE post-loss).
- Cadence: trigger-to-trigger 300.000s EXACT (10:24:54 c2652-serviced trigger -> 10:29:54 this trigger; 1x300 - the 1200.000 EXACT print terminates at member 1; a 300.000 EXACT print opens member 1); post-echo gap c2652->c2653 = 417.150357668s.
- Queues: dispatch-delay #227 = 653.931665992s CAPTURED (pre-curl 10:40:47.931665992 minus trigger 10:29:54.000) - ESCALATION RE-OPENS vs dd#226 536.699399805 (+117.232266187; post-loss series member 8: 1422.59 -> 1459.28 escalation -> 612.22 drain -> 446.00 drain -> 748.25 re-escalation -> 1082.86 further escalation -> 536.70 drain -> 653.93 ESCALATION - the drain run terminates at member 1, the escalation class re-opens member 1); decomposition: trigger->loop-open (trace token 1038) 486.000s + in-loop staging 167.931665992s (minute-resolution token caveat; the trigger queued 486s while c2652 finished mid-flight); LAG#227 = 417.232266187 (interval 300.000 + dd#227 - dd#226) over-300 member 8 (1672.96 -> 1537.69 -> 652.94 -> 433.78 -> 602.24 -> 1235.61 -> 653.84 -> 417.23); STAMP-VS-WINDOW: vs window-2653 10:38:52.562005109 the post-echo sits +117.150357667s LATE (post-loss LATE run member 8; magnitude FELL 353.778848909 -> 117.150357667; the post-echo sits WITHIN the window - 182.849642333s inside the upper edge 10:43:52.562005109 - the beyond-upper-edge run TERMINATES at member 3, the c2649-shaped LATE-within-window class re-opens); SOLE OPERATIVE ERA FLOOR 7.846 (derived, context-carried) standing; captured-era floor marker 11.547843496; all-time captured min 11.287 @ c2492 stands; all-time max 39594.655 stands.
- Ghost ledger: 59 -> 60 (ONE new ghost, zero unbooked: #60 = 10:34:44 6900b 1793068484 elapsed-unclaimed at arrival pre-window-2653, 363.931665992s pre-stamp; the 10:39:44 7200b CLAIMED deferred-servicing - stamp 63.931665992s after the rung, NORMAL per the c2649/c2650/c2651/c2652 dispatch language, consumed NOT a ghost; the 10:44:44 7500b live-outstanding for c2654, pre-window-2654 note - likely next ghost unless a sibling claims); all epochs python-timegm verified.
- Token/dwell: trace token 1038 = lead -1 (38 - 39 keyed) - first negative print since the c2649/c2650 negative pair (+13, +4, +2, -5, -4, +1, +1, -1; jump -2; the back-to-back +1 pair terminates at member 2); lead band -1 -> [-87.000, -27.000) FIRST PRINT UNVALIDATED - dd#227 653.93 OUT above by 680.931665992 (wide print, band stays UNVALIDATED); dwell overshoot member 8 (magnitude ROSE 443.699399805 -> 680.931665992); zero-dwell n/a this cycle.
- Echo: strike vs c2652 sweep 1.850271..1.860271 / 1841..1851 = MISS (below - both members out: time 1.773656 below the lower edge by 0.076615, duration 1763 below by 78), account 83-for-387; new sweep 1.768656..1.778656 / 1758..1768, k=345 (c2310..c2653); MIRROR RESONANCE stays closed (context-carried 29).
- Drift watch: DRIFT-#45 verified 31st cycle ON DISK - 31-fold (31/59 = 52.5% of the DRIFT-#30 record span; root c2623 context-carried; chain: c2653=v31; c2652=v30; c2651=v29; c2650=v28; c2649=v27; c2648=v26; c2647=v25; c2646=v24; c2645=v23; ...; c2623=v1 ROOT; DRIFT-#44 closed 4-fold after c2619 - pre-#45 series context-carried); HONEST INVENTORY EMPTY continues (honest_free=0, honest_paid=0 - scam 18 = the entire visible market, unknown 0); any honest (free OR paid) emergence or total movement (18->17 or 18->19) = DRIFT-#46 (two-pass); honest_paid emergence = GOLD condition (immediate scam-check + EV path); SIZE 446B streak intact (c2646..c2653 all 446B on disk); window-2654 = 10:45:49.712362776 +08 (post-echo + 300.000 server contract).
- Next: the c2654 instance MUST arrival-guard against c2654/c2655 tokens AND re-verify the post-LOSS-#6 state BEFORE dispatch (expect worklog @@TOTAL@@ lines; artifacts validate_cycle2653.py / scan_cycle2653_raw.json / scan_cycle2653.json / capture_cycle2653.sh / recursive_diff_2653.py / entry_cycle2653.txt + the standing validate_cycle2652.py / validate_cycle2651.py / validate_cycle2650.py / validate_cycle2649.py / validate_cycle2648.py / validate_cycle2647.py / validate_cycle2646.py / validate_cycle2576.py / entry_cycle2652.txt / entry_cycle2651.txt / entry_cycle2650.txt / entry_cycle2649.txt / entry_cycle2648.txt / entry_cycle2647.txt / entry_cycle2646.txt / entry_recon_loss5.txt; git HEAD >= the post-c2653 commit; absence = suspected LOSS EVENT #14 - verify git HEAD BEFORE writing); validator rebadge source is now validate_cycle2653.py (DRIFT-#45 verification-31 carry class; c2654 = verification 32 on match - 32/59 = 54.2%); rebadge = sed 2653->2654 (5 tokens) + docstring verification-31->32 bump + chain insert c2653 = verification 31 before the c2652 citation + rebadged-from -> validate_cycle2653.py + P-HIST WATCH (pre-patch table {2653:5, 2652:2, 2651:1, 2650:1, 2649:1, 2648:1, 2647:1, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted on ACTUAL bytes; post-patch {2654:5, 2653:2, 2652:1, 2651:1, 2650:1, 2649:1, 2648:1, 2647:1, 2646:3, ...} lineage citations == 2 - the c2573 LESSON, carried; HIST-restore NO-OPs expected - the LOSS block history keeps cite c2646, sed-immune); INSTRUMENTATION: captured-class pattern STANDARD, mandatory order (pre-echo -> curl -o/-w -> post-echo) permanent; harness staged BEFORE any scan POST; SLOT WATCH: the 10:44:44 7500b rung (epoch 1793069084) is live outstanding (NOT elapsed at the c2653 stamp 10:40:47.931665992, 236.068334008s future; pre-window-2654 10:45:49.712362776 - if it passes unclaimed on c2654 arrival with no sibling entry keyed 10:44:4x, append as the next outstanding ghost), then 10:49:44 (7800b, epoch 1793069384) = the dispatched c2654 candidate (first rung inside window-2654; deferred-servicing claim if stamped late, EARLY-claim if stamped pre-rung - both NORMAL per the c2649..c2653 precedent), then 10:54:44 (8100b), 10:59:44 (8400b), or a ghost - all live (the STAMP governs; wobble risk noted on every rung); TOKEN WATCH on a 10:49:44 keyed rung (minute 49): 1050 (+1), 1052 (+3), 1054 (+5), 1055 (+6), 1056 (+7), 1057 (+8), 1058 (+9), 1059 (+10) - all live; DD WATCH: post-loss series member 1 @ 653.93 (ESCALATION re-opens): escalation (dd#228 > 653.93) vs plateau vs drain (dd#228 < 653.93 re-opens the drain class) all live; a sub-11.287 dd sets a NEW ALL-TIME CAPTURED MINIMUM (context-carried threshold); EP14 watch - STALL run member 3 (s243): s244 dual sub-2.0 extends STALL member 4, dual 2.0-2.1 flips GRAY (re-opens member 1), dual 2.1-2.4 flips ARM, dual above-2.4 re-opens OPEN, cross-class split resolves to the client class; era-high defense: 6.273332/6264 stands until exceeded; Echo: new sweep 1.768656..1.778656 / 1758..1768 (k=345), account 83-for-387; DRIFT-#45 watch - baseline (18,0,0,18,0) @ 446B: verification 32 on match; any movement or honest emergence = DRIFT-#46 two-pass (paid emergence = GOLD - scam-check + EV path per protocol).
- No gold yet. Scanner continues.
"""

n_lines = entry.count("\n")
total = 8287 + n_lines
entry = entry.replace("@@TOTAL@@", str(total)).replace("@@N@@", str(n_lines))

cur = open(WORKLOG).read()
cur_lines = cur.count("\n")
assert cur_lines == 8287, f"worklog moved: {cur_lines} != 8287"
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
