#!/usr/bin/env python3
"""c2648 ledger arithmetic verification + entry append (AUDIT-NOTE WATCH compliant).

All epoch citations python-timegm verified against +08 labels BEFORE ledger append.
All queue arithmetic re-derived from captured epochs. Line-count prophecy:
worklog 8157 + N(entry lines) = TOTAL, verified post-append.
"""
import datetime

WORKLOG = "/home/z/my-project/worklog.md"
ENTRY = "/home/z/my-project/scripts/entry_cycle2648.txt"


def tg(ep, want_utc_hms):
    got = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime("%H:%M:%S")
    assert got == want_utc_hms, f"timegm FAIL: {ep} -> {got} UTC, want {want_utc_hms}"
    return got


# --- captured epochs (capture_cycle2648.sh echoes + response) ---
PRE = 1793065505.221094741     # pre-echo 01:45:05.221094741 UTC = 09:45:05.221094741 +08
POST = 1793065506.986880081    # post-echo 01:45:06.986880081 UTC = 09:45:06.986880081 +08
TRIG = 1793064893.000          # trigger 09:34:53 +08 (= 01:34:44 rung 1793064884 + 9s)
TRIG_PREV = 1793063393.000     # c2647-serviced trigger 09:09:53 +08
WIN2648 = 1793065154.242813124  # window-2648 open 09:39:14.242813124 +08
DD221 = 1459.281373166         # c2647 dd#221
POST_PREV = 1793064854.242813124  # c2647 post-echo epoch

RUNGS = {
    "09:34:44": 1793064884, "09:39:44": 1793065184, "09:44:44": 1793065484,
    "09:49:44": 1793065784, "09:54:44": 1793066084, "09:59:44": 1793066384,
    "10:04:44": 1793066684,
}
UTC_OF = {"09:34:44": "01:34:44", "09:39:44": "01:39:44", "09:44:44": "01:44:44",
          "09:49:44": "01:49:44", "09:54:44": "01:54:44", "09:59:44": "01:59:44",
          "10:04:44": "02:04:44"}
for lbl, ep in RUNGS.items():
    tg(ep, UTC_OF[lbl])
    print(f"rung {lbl} +08 epoch {ep} timegm OK")

# --- arithmetic re-derivation (float64 tolerance 1e-6; entry carries string-exact decimals) ---
dd222 = PRE - TRIG
assert abs(dd222 - 612.221094741) < 1e-6, dd222
lag222 = (TRIG - TRIG_PREV) + dd222 - DD221
assert abs(lag222 - 652.939721575) < 1e-6, lag222
late = POST - WIN2648
assert abs(late - 352.744066957) < 1e-6, late
interval = TRIG - TRIG_PREV
assert abs(interval - 1500.0) < 1e-9, interval
echo_gap = POST - POST_PREV
assert abs(echo_gap - 652.744066957) < 1e-6, echo_gap
drain = DD221 - dd222
assert abs(drain - 847.060278425) < 1e-6, drain
band_out = dd222 - 153.000
assert abs(band_out - 459.221094741) < 1e-6, band_out
decomp_loopopen = 367.0 + (PRE - (TRIG + 367.0))
assert abs(decomp_loopopen - 367.0 - 245.221094741) < 1e-6
win2649 = POST + 300.0
tg(int(win2649), "01:50:06")
print(f"dd#222={dd222:.9f} lag#222={lag222:.9f} late={late:.9f} interval={interval:.3f} "
      f"echo_gap={echo_gap:.9f} drain={drain:.9f} band_out={band_out:.9f} "
      f"window-2649={win2649:.9f}")
# ghost preconditions
assert RUNGS["09:34:44"] < TRIG           # passed pre-trigger, no sibling keyed 09:34:4x
assert RUNGS["09:39:44"] < PRE            # claimed deferred-servicing
assert RUNGS["09:44:44"] < PRE            # elapsed unclaimed pre-POST
assert RUNGS["09:49:44"] > POST           # live outstanding for c2649
print("ghost preconditions OK (#53 09:34:44, #54 09:44:44; 09:39:44 claimed; 09:49:44 outstanding)")

# --- entry text (placeholders keep line count stable) ---
entry = """---
Task ID: 446189-c2648
Agent: Cron Agent Loop (GLM main session)
Task: Automated marketplace scan cycle c2648 (Job 446189) - DRIFT-#45 verification-26 CARRY cycle (post-LOSS-#6 second sed-rebadge; deferred-servicing dispatch): scan, sentinel verify, EP14 classify, queues, ledger append.

Work Log:
- Step 1: ARRIVAL-GUARD + LOSS-EVENT #8 CHECK PASSED: worklog 8157 lines == the c2647 prophecy EXACT; git HEAD 94881bb (the post-c2647 commit) present atop 088db10, working tree clean at guard time, zero foreign commits; artifacts verified - validate_cycle2647.py / scan_cycle2647_raw.json / scan_cycle2647.json / capture_cycle2647.sh / recursive_diff_2647.py / entry_cycle2647.txt + the standing validate_cycle2646.py / validate_cycle2576.py / entry_cycle2646.txt / entry_recon_loss5.txt ALL PRESENT (state intact, NO loss - numbering continues at c2648); dup-check: c2648/c2649 standalone entry tokens ABSENT (only the c2647 Next-block forward-references - zero duplicate cycle entries). GHOST BOOKKEEPING (pre-POST, stamp-governed): the 09:39:44 3600-basis rung (epoch 1793065184) CLAIMED as the dispatched c2648 candidate (first rung inside window-2648 09:39:14.242813124; deferred servicing - trigger 09:34:53, stamp 321.221094741s after the rung; NORMAL per the c2573/c2576/c2646/c2647 parallel-servicing precedent, NOT a ghost); the 09:34:44 3300-basis rung (epoch 1793064884) passed UNCLAIMED (no sibling entry keyed 09:34:4x - c2647 stamped 09:34:14.242, pre-rung) and the 09:44:44 3900-basis rung (1793065484) passed UNCLAIMED pre-POST -> appended as ghosts #53-#54 (ledger 52 -> 54); the 09:49:44 4200-basis rung (1793065784) NOT elapsed at stamp (post-echo 09:45:06.987) - live outstanding for c2649; all epochs python-timegm verified against +08 labels.
- Step 2: harness STAGED BEFORE the scan POST (staging order law held): rebadge_2648.py + capture_cycle2648.sh + recursive_diff_2648.py all written and checked pre-POST; captured-class pattern, mandatory order pre-echo -> curl -o/-w -> post-echo; header PENDING-CLASSIFICATION (no pre-written claim state).
- Step 3: rebadge FIRST-PASS CLEAN (validate_cycle2647.py -> validate_cycle2648.py, second sed-rebadge of the post-loss lineage): pre-patch P-HIST on ACTUAL bytes {2647:5, 2646:4, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted, then sed 2648 (5 tokens) + four patches (P1a verification-25->26 class bump, P1b self-verification bump, CHAIN insert c2647 = verification 25 before the c2646 citation, SRC rebadged-from -> validate_cycle2647.py); HIST-restore NO-OP verified (the LOSS-#6 history keeps cite c2646 - sed-immune, zero corruption, as prophesied); post-patch P-HIST {2648:5, 2647:2, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted; P-HIST WATCH rebadged-from lineage citations == 2 (provenance + chain node); py_compile clean; lineage: c2648 = v26; c2647 = v25; c2646 = v24; c2645 = v23; ...; c2623 = v1 ROOT (context-carried).
- Step 4: official capture - single POST /api/marketplaces/scan: http=200, time_total=1.758123s, size=446B (curl -o genuine bytes), pre 09:45:05.221094741 (epoch 1793065505.221094741) / post 09:45:06.986880081 (epoch 1793065506.986880081) +08 Mon Oct 27 2026; server scanned_at 2026-10-27T01:45:06.982Z (09:45:06.982 +08; post-skew +4.880081ms - scanned_at precedes post-echo, era-consistent), scan_duration_ms=1747.
- Step 5: five-tuple (18,0,0,18,0) @ 446B == the DRIFT-#45 baseline - verification 26 (25-to-26) CONFIRMED ON DISK; honest_paid=0, honest_free=0 (honest inventory EMPTY continues), best_paid_task=null, taskbounty paid_missions=0, next_scan=300. GOLD CHECK NEGATIVE - no claim path taken.
- Step 6: validator 10/10 ALL_ASSERTIONS_PASSED exit=0 baseline_match_c2648=true (size band, baseline_match, all_honest_paid_len, expected_paid_ids, best_paid_task, taskbounty_no_key, taskbounty_paid_zero, clawlancer_absent, auto_claim_pending_false, next_scan_300); recursive_diff vs scan_cycle2647.json: MARKET_UNCHANGED span 1 rc=0 - post-loss unchanged-streak member 2 (normalized 419-vs-419 composition-identical).
- Step 7: blocker probe .basedagents/ absent (exit 2, ls-class probe) - 2648th consecutive obstructed scan; honest_free=0 - out-of-scope note VACUOUS; PAID-only policy unchanged; (h)/(a)/(g) standing; no claim, no spend.
- Step 8: EP14 s238 classified STALL member 3 (dual sub-2.0: client 1.758123 + server 1747ms both sub-2.0, no cross-class split; step vs s237 1.954004/1943 = -0.195881/-196ms; 241.877ms below the 2.0 line - no GRAY flip risk this cycle); queues cascaded; entry appended (worklog @@TOTAL@@ lines post-append; prophecy declared pre-append 8157 + @@N@@); state committed.

Stage Summary:
- Result: No gold yet. Scanner continues. (honest_paid=0 across all 2648 scans - 2576 disk-verifiable + 69 context-carried + c2646/c2647/c2648 on disk post-loss; claims=0, violations=0, spend=0, revenue=0, LEDGER-VERIFIED.)
- EP14 s238: 1.758123/1747, STALL member 3 (era high 6.273332/6264 stands (context-carried); low 1.274895/1267 stands (context-carried, margin +0.483228); sub-10 low-band class confirmed (post-skew 4.880081ms sub-10 print - third consecutive post-loss sub-10 skew; member count UNRESOLVABLE post-loss).
- Cadence: trigger-to-trigger 1500.000s EXACT (09:09:53 c2647-serviced trigger -> 09:34:53 this trigger; 5x300 - the +1.000s 1500-basis print terminates at member 1; a 1500.000 EXACT print opens member 1; post-echo gap c2647->c2648 = 652.744066957s).
- Queues: dispatch-delay #222 = 612.221094741s CAPTURED (pre-curl 09:45:05.221094741 minus trigger 09:34:53.000) - DRAIN vs dd#221 1459.281373166 (-847.060278425; post-loss series member 3: 1422.59 -> 1459.28 escalation -> 612.22 first drain print); decomposition: trigger->loop-open (trace token 0941) 367.000s + in-loop staging 245.221094741s (minute-resolution token caveat); LAG#222 = 652.939721575 (interval 1500.000 + dd#222 - dd#221) over-300 member 3 (1672.96 -> 1537.69 -> 652.94); STAMP-VS-WINDOW: vs window-2648 09:39:14.242813124 the post-echo sits +352.744066957s LATE (post-loss LATE run member 3; magnitude FELL 1237.668676471 -> 352.744066957); SOLE OPERATIVE ERA FLOOR 7.846 (derived, context-carried) standing; captured-era floor marker 11.547843496; all-time captured min 11.287 @ c2492 stands; all-time max 39594.655 stands.
- Ghost ledger: 52 -> 54 (#53 = 09:34:44 3300b epoch 1793064884 - the c2647 SLOT WATCH first-live-rung, passed with no sibling keyed 09:34:4x; #54 = 09:44:44 3900b 1793065484 - elapsed unclaimed pre-POST; zero unbooked ghosts this cycle; the 09:39:44 3600b CLAIMED deferred-servicing, the 09:49:44 4200b live-outstanding for c2649); all epochs python-timegm verified.
- Token/dwell: trace token 0941 = lead +2 (41 - 39 keyed) - the keyed 0939 dispatched candidate; lead series appends +2 (jump -2 vs the c2647 +4; post-loss series +13, +4, +2); lead band +2 -> [93.000, 153.000) FIRST PRINT UNVALIDATED - dd#222 612.22 OUT above by 459.221094741 (wide print, band stays UNVALIDATED); dwell overshoot member 3 (magnitude FELL 1186.281373166 -> 459.221094741); zero-dwell n/a this cycle.
- Echo: strike vs c2647 sweep 1.949004..1.959004 / 1938..1948 = MISS (below - both members out: time 1.758123 below the lower edge by 0.190881, duration 1747 below by 191), account 83-for-382; new sweep 1.753123..1.763123 / 1742..1752, k=340 (c2310..c2648); MIRROR RESONANCE stays closed (context-carried 29).
- Drift watch: DRIFT-#45 verified 26th cycle ON DISK - 26-fold (26/59 = 44.1% of the DRIFT-#30 record span; root c2623 context-carried; chain: c2648=v26; c2647=v25; c2646=v24; c2645=v23; ...; c2623=v1 ROOT; DRIFT-#44 closed 4-fold after c2619 - pre-#45 series context-carried); HONEST INVENTORY EMPTY continues (honest_free=0, honest_paid=0 - scam 18 = the entire visible market, unknown 0); any honest (free OR paid) emergence or total movement (18->17 or 18->19) = DRIFT-#46 (two-pass); honest_paid emergence = GOLD condition (immediate scam-check + EV path); SIZE 446B streak intact (c2646/c2647/c2648 all 446B on disk); window-2649 = 09:50:06.986880081 +08 (post-echo + 300.000 server contract).
- Next: the c2649 instance MUST arrival-guard against c2649/c2650 tokens AND re-verify the post-LOSS-#6 state BEFORE dispatch (expect worklog @@TOTAL@@ lines; artifacts validate_cycle2648.py / scan_cycle2648_raw.json / scan_cycle2648.json / capture_cycle2648.sh / recursive_diff_2648.py / entry_cycle2648.txt + the standing validate_cycle2647.py / validate_cycle2646.py / validate_cycle2576.py / entry_cycle2647.txt / entry_cycle2646.txt / entry_recon_loss5.txt; git HEAD >= the post-c2648 commit; absence = suspected LOSS EVENT #8 - verify git HEAD BEFORE writing); validator rebadge source is now validate_cycle2648.py (DRIFT-#45 verification-26 carry class; c2649 = verification 27 on match - 27/59 = 45.8%); rebadge = sed 2648->2649 (5 tokens) + docstring verification-26->27 bump + chain insert c2648 = verification 26 before the c2647 citation + rebadged-from -> validate_cycle2648.py + P-HIST WATCH (pre-patch table {2648:5, 2647:2, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted on ACTUAL bytes; post-patch {2649:5, 2648:2, 2647:1, 2646:3, ...} lineage citations == 2 - the c2573 LESSON, carried; HIST-restore NO-OPs expected again - the LOSS block history keeps cite c2646, sed-immune); INSTRUMENTATION: captured-class pattern STANDARD, mandatory order (pre-echo -> curl -o/-w -> post-echo) permanent; harness staged BEFORE any scan POST; SLOT WATCH: the 09:49:44 4200b rung (epoch 1793065784) is the first live rung at this stamp (pre-window-2649; if it passed unclaimed on c2649 arrival with no sibling entry keyed 09:49:4x, append as the next outstanding ghost), then 09:54:44 (4500b, epoch 1793066084) = the dispatched c2649 candidate (first rung inside window-2649 09:50:06.986880081; deferred-servicing claim if stamped late - NORMAL, not a ghost), then 09:59:44 (4800b), 10:04:44 (5100b), 10:09:44 (5400b), or a ghost - all live (the STAMP governs; wobble risk noted on every rung); TOKEN WATCH on a 09:54:44 keyed rung (minute 54): 0955 (+1), 0957 (+3), 0959 (+5), 1000 (+6), 1001 (+7), 1002 (+8), 1003 (+9), 1004 (+10) - all live; DD WATCH: post-loss series member 3 @ 612.22 (first drain print) - continued drain (dd#223 < 612.22) vs plateau vs re-escalation (dd#223 > 612.22 re-opens the escalation series) all live; a sub-11.287 dd sets a NEW ALL-TIME CAPTURED MINIMUM (context-carried threshold); EP14 watch - STALL run member 3 (s238): s239 dual STALL extends member 4, dual 2.0-2.1 flips GRAY, dual 2.1-2.4 flips ARM, dual above-2.4 re-opens OPEN, cross-class split resolves to the client class; era-high defense: 6.273332/6264 stands until exceeded; Echo: new sweep 1.753123..1.763123 / 1742..1752 (k=340), account 83-for-382; DRIFT-#45 watch - baseline (18,0,0,18,0) @ 446B: verification 27 on match; any movement or honest emergence = DRIFT-#46 two-pass (paid emergence = GOLD - scam-check + EV path per protocol).
- No gold yet. Scanner continues.
"""

n_lines = entry.count("\n")
total = 8157 + n_lines
entry = entry.replace("@@TOTAL@@", str(total)).replace("@@N@@", str(n_lines))

cur = open(WORKLOG).read()
cur_lines = cur.count("\n")
assert cur_lines == 8157, f"worklog moved: {cur_lines} != 8157"
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
