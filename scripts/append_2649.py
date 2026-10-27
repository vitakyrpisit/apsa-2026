#!/usr/bin/env python3
"""c2649 ledger arithmetic verification + entry append (AUDIT-NOTE WATCH compliant).

All epoch citations python-timegm verified against +08 labels BEFORE ledger append.
All queue arithmetic re-derived from captured epochs. Line-count prophecy:
worklog 8183 + N(entry lines) = TOTAL, verified post-append.
"""
import datetime

WORKLOG = "/home/z/my-project/worklog.md"
ENTRY = "/home/z/my-project/scripts/entry_cycle2649.txt"


def tg(ep, want_utc_hms):
    got = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime("%H:%M:%S")
    assert got == want_utc_hms, f"timegm FAIL: {ep} -> {got} UTC, want {want_utc_hms}"
    return got


# --- captured epochs (capture_cycle2649.sh echoes + response) ---
PRE = 1793065939.001367207     # pre-echo 01:52:19.001367207 UTC = 09:52:19.001367207 +08
POST = 1793065941.184685968    # post-echo 01:52:21.184685968 UTC = 09:52:21.184685968 +08
TRIG = 1793065493.000          # trigger 09:44:53 +08 (= 01:44:44 rung 1793065484 + 9s)
TRIG_PREV = 1793064893.000     # c2648-serviced trigger 09:34:53 +08
WIN2649 = 1793065806.986880081  # window-2649 open 09:50:06.986880081 +08
DD222 = 612.221094741          # c2648 dd#222
POST_PREV = 1793065506.986880081  # c2648 post-echo epoch
RUNG_KEYED = 1793066084        # 09:54:44 4500b dispatched candidate

RUNGS = {
    "09:49:44": 1793065784, "09:54:44": 1793066084, "09:59:44": 1793066384,
    "10:04:44": 1793066684, "10:09:44": 1793066984,
}
UTC_OF = {"09:49:44": "01:49:44", "09:54:44": "01:54:44", "09:59:44": "01:59:44",
          "10:04:44": "02:04:44", "10:09:44": "02:09:44"}
for lbl, ep in RUNGS.items():
    tg(ep, UTC_OF[lbl])
    print(f"rung {lbl} +08 epoch {ep} timegm OK")

# --- arithmetic re-derivation (float64 tolerance 1e-6; entry carries string-exact decimals) ---
dd223 = PRE - TRIG
assert abs(dd223 - 446.001367207) < 1e-6, dd223
lag223 = (TRIG - TRIG_PREV) + dd223 - DD222
assert abs(lag223 - 433.780272466) < 1e-6, lag223
late = POST - WIN2649
assert abs(late - 134.197805887) < 1e-6, late
interval = TRIG - TRIG_PREV
assert abs(interval - 600.0) < 1e-9, interval
echo_gap = POST - POST_PREV
assert abs(echo_gap - 434.197805887) < 1e-6, echo_gap
drain = DD222 - dd223
assert abs(drain - 166.219727534) < 1e-6, drain
band_out = dd223 + 267.000
assert abs(band_out - 713.001367207) < 1e-6, band_out
early = RUNG_KEYED - POST
assert abs(early - 142.815314032) < 1e-6, early
win2650 = POST + 300.0
tg(int(win2650), "01:57:21")
print(f"dd#223={dd223:.9f} lag#223={lag223:.9f} late={late:.9f} interval={interval:.3f} "
      f"echo_gap={echo_gap:.9f} drain={drain:.9f} band_out={band_out:.9f} "
      f"EARLY={early:.9f} window-2650={win2650:.9f}")
# ghost preconditions
assert RUNGS["09:49:44"] < PRE            # passed post-trigger pre-POST (loop-open wait), no sibling keyed 09:49:4x
assert RUNGS["09:54:44"] > POST           # EARLY claim: rung still future at stamp
assert RUNGS["09:59:44"] > POST           # live outstanding for c2650
print("ghost preconditions OK (#55 09:49:44; 09:54:44 EARLY-claimed; 09:59:44 outstanding)")

# --- entry text (placeholders keep line count stable) ---
entry = """---
Task ID: 446189-c2649
Agent: Cron Agent Loop (GLM main session)
Task: Automated marketplace scan cycle c2649 (Job 446189) - DRIFT-#45 verification-27 CARRY cycle (post-LOSS-#6 third sed-rebadge; EARLY-claim dispatch): scan, sentinel verify, EP14 classify, queues, ledger append.

Work Log:
- Step 1: ARRIVAL-GUARD + LOSS-EVENT #9 CHECK PASSED: worklog 8183 lines == the c2648 prophecy EXACT; git HEAD 4e24d85 (the post-c2648 commit) present atop 94881bb, working tree clean at guard time, zero foreign commits; artifacts verified - validate_cycle2648.py / scan_cycle2648_raw.json / scan_cycle2648.json / capture_cycle2648.sh / recursive_diff_2648.py / entry_cycle2648.txt + the standing validate_cycle2647.py / validate_cycle2646.py / validate_cycle2576.py / entry_cycle2647.txt / entry_cycle2646.txt / entry_recon_loss5.txt ALL PRESENT (state intact, NO loss - numbering continues at c2649); dup-check: c2649/c2650 standalone entry tokens ABSENT (only the c2648 Next-block forward-references - zero duplicate cycle entries). GHOST BOOKKEEPING (pre-POST, stamp-governed): the 09:49:44 4200-basis rung (epoch 1793065784) passed UNCLAIMED (no sibling entry keyed 09:49:4x - c2648 stamped 09:45:06.987, pre-rung) -> appended as ghost #55 (ledger 54 -> 55); the 09:54:44 4500-basis rung (1793066084) CLAIMED EARLY as the dispatched c2649 candidate (first rung inside window-2649 09:50:06.986880081; the stamp PRECEDES the rung - post-echo 142.815314032s EARLY; FIRST EARLY CLAIM of the post-loss lineage after four deferred-servicing LATE claims; the STAMP governs - consumed, NOT a ghost; NORMAL dispatch accounting, shape-change recorded); the 09:59:44 4800-basis rung (1793066384) NOT elapsed at stamp - live outstanding for c2650; all epochs python-timegm verified against +08 labels.
- Step 2: harness STAGED BEFORE the scan POST (staging order law held): rebadge_2649.py + capture_cycle2649.sh + recursive_diff_2649.py all written and checked pre-POST; captured-class pattern, mandatory order pre-echo -> curl -o/-w -> post-echo; header PENDING-CLASSIFICATION (no pre-written claim state, EARLY-claim contingency noted).
- Step 3: rebadge FIRST-PASS CLEAN (validate_cycle2648.py -> validate_cycle2649.py, third sed-rebadge of the post-loss lineage): pre-patch P-HIST on ACTUAL bytes {2648:5, 2647:2, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted, then sed 2649 (5 tokens) + four patches (P1a verification-26->27 class bump, P1b self-verification bump, CHAIN insert c2648 = verification 26 before the c2647 citation, SRC rebadged-from -> validate_cycle2648.py); HIST-restore NO-OP verified (as prophesied); post-patch P-HIST {2649:5, 2648:2, 2647:1, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted; P-HIST WATCH rebadged-from lineage citations == 2; py_compile clean; lineage: c2649 = v27; c2648 = v26; c2647 = v25; c2646 = v24; c2645 = v23; ...; c2623 = v1 ROOT (context-carried).
- Step 4: official capture - single POST /api/marketplaces/scan: http=200, time_total=2.176020s, size=446B (curl -o genuine bytes), pre 09:52:19.001367207 (epoch 1793065939.001367207) / post 09:52:21.184685968 (epoch 1793065941.184685968) +08 Mon Oct 27 2026; server scanned_at 2026-10-27T01:52:21.180Z (09:52:21.180 +08; post-skew +4.685968ms - scanned_at precedes post-echo, era-consistent), scan_duration_ms=2165.
- Step 5: five-tuple (18,0,0,18,0) @ 446B == the DRIFT-#45 baseline - verification 27 (26-to-27) CONFIRMED ON DISK; honest_paid=0, honest_free=0 (honest inventory EMPTY continues), best_paid_task=null, taskbounty paid_missions=0, next_scan=300. GOLD CHECK NEGATIVE - no claim path taken.
- Step 6: validator 10/10 ALL_ASSERTIONS_PASSED exit=0 baseline_match_c2649=true (size band, baseline_match, all_honest_paid_len, expected_paid_ids, best_paid_task, taskbounty_no_key, taskbounty_paid_zero, clawlancer_absent, auto_claim_pending_false, next_scan_300); recursive_diff vs scan_cycle2648.json: MARKET_UNCHANGED span 1 rc=0 - post-loss unchanged-streak member 3 (normalized 419-vs-419 composition-identical).
- Step 7: blocker probe .basedagents/ absent (exit 2, ls-class probe) - 2649th consecutive obstructed scan; honest_free=0 - out-of-scope note VACUOUS; PAID-only policy unchanged; (h)/(a)/(g) standing; no claim, no spend.
- Step 8: EP14 s239 classified ARM member 1 (DUAL 2.1-2.4: client 2.176020 in [2.1, 2.4) AND server 2165ms in [2100, 2400) - the STALL run terminates at member 3 (s236/s237/s238); FIRST ARM print of the post-loss era; re-opens member 1 per the standing watch); queues cascaded; entry appended (worklog @@TOTAL@@ lines post-append; prophecy declared pre-append 8183 + @@N@@); state committed.

Stage Summary:
- Result: No gold yet. Scanner continues. (honest_paid=0 across all 2649 scans - 2576 disk-verifiable + 69 context-carried + c2646..c2649 on disk post-loss; claims=0, violations=0, spend=0, revenue=0, LEDGER-VERIFIED.)
- EP14 s239: 2.176020/2165, ARM member 1 (dual 2.1-2.4 flip; step vs s238 1.758123/1747 = +0.417897/+418ms; era high 6.273332/6264 stands (context-carried); low 1.274895/1267 stands (context-carried, margin +0.901125); sub-10 low-band class confirmed (post-skew 4.685968ms sub-10 print - fourth consecutive post-loss sub-10 skew; member count UNRESOLVABLE post-loss).
- Cadence: trigger-to-trigger 600.000s EXACT (09:34:53 c2648-serviced trigger -> 09:44:53 this trigger; 2x300 - the 1500.000 EXACT print terminates at member 1; a 600.000 EXACT print opens member 1; post-echo gap c2648->c2649 = 434.197805887s).
- Queues: dispatch-delay #223 = 446.001367207s CAPTURED (pre-curl 09:52:19.001367207 minus trigger 09:44:53.000) - CONTINUED DRAIN vs dd#222 612.221094741 (-166.219727534; post-loss series member 4: 1422.59 -> 1459.28 escalation -> 612.22 drain -> 446.00 drain); decomposition: trigger->loop-open (trace token 0949) 247.000s + in-loop staging 199.001367207s (minute-resolution token caveat); LAG#223 = 433.780272466 (interval 600.000 + dd#223 - dd#222) over-300 member 4 (1672.96 -> 1537.69 -> 652.94 -> 433.78); STAMP-VS-WINDOW: vs window-2649 09:50:06.986880081 the post-echo sits +134.197805887s LATE (post-loss LATE run member 4; magnitude FELL 352.744066957 -> 134.197805887 - converging toward EARLY flip); SOLE OPERATIVE ERA FLOOR 7.846 (derived, context-carried) standing; captured-era floor marker 11.547843496; all-time captured min 11.287 @ c2492 stands; all-time max 39594.655 stands.
- Ghost ledger: 54 -> 55 (#55 = 09:49:44 4200b epoch 1793065784 - the c2648 SLOT WATCH first-live-rung, passed with no sibling keyed 09:49:4x; zero unbooked ghosts this cycle; the 09:54:44 4500b CLAIMED EARLY (pre-rung consumption, first of the post-loss era), the 09:59:44 4800b live-outstanding for c2650); all epochs python-timegm verified.
- Token/dwell: trace token 0949 = lead -5 (49 - 54 keyed) - FIRST NEGATIVE LEAD PRINT of the post-loss series (+13, +4, +2, -5; jump -7; the loop-open precedes the keyed rung - the EARLY-claim shape in token space); lead band -5 -> [-327.000, -267.000) FIRST PRINT UNVALIDATED - dd#223 446.00 OUT above by 713.001367207 (wide print, band stays UNVALIDATED); dwell overshoot member 4 (magnitude ROSE 459.221094741 -> 713.001367207); zero-dwell n/a this cycle.
- Echo: strike vs c2648 sweep 1.753123..1.763123 / 1742..1752 = MISS (above - both members out: time 2.176020 above the upper edge by 0.412897, duration 2165 above by 413), account 83-for-383; new sweep 2.171020..2.181020 / 2160..2170, k=341 (c2310..c2649); MIRROR RESONANCE stays closed (context-carried 29).
- Drift watch: DRIFT-#45 verified 27th cycle ON DISK - 27-fold (27/59 = 45.8% of the DRIFT-#30 record span; root c2623 context-carried; chain: c2649=v27; c2648=v26; c2647=v25; c2646=v24; c2645=v23; ...; c2623=v1 ROOT; DRIFT-#44 closed 4-fold after c2619 - pre-#45 series context-carried); HONEST INVENTORY EMPTY continues (honest_free=0, honest_paid=0 - scam 18 = the entire visible market, unknown 0); any honest (free OR paid) emergence or total movement (18->17 or 18->19) = DRIFT-#46 (two-pass); honest_paid emergence = GOLD condition (immediate scam-check + EV path); SIZE 446B streak intact (c2646..c2649 all 446B on disk); window-2650 = 09:57:21.184685968 +08 (post-echo + 300.000 server contract).
- Next: the c2650 instance MUST arrival-guard against c2650/c2651 tokens AND re-verify the post-LOSS-#6 state BEFORE dispatch (expect worklog @@TOTAL@@ lines; artifacts validate_cycle2649.py / scan_cycle2649_raw.json / scan_cycle2649.json / capture_cycle2649.sh / recursive_diff_2649.py / entry_cycle2649.txt + the standing validate_cycle2648.py / validate_cycle2647.py / validate_cycle2646.py / validate_cycle2576.py / entry_cycle2648.txt / entry_cycle2647.txt / entry_cycle2646.txt / entry_recon_loss5.txt; git HEAD >= the post-c2649 commit; absence = suspected LOSS EVENT #9 - verify git HEAD BEFORE writing); validator rebadge source is now validate_cycle2649.py (DRIFT-#45 verification-27 carry class; c2650 = verification 28 on match - 28/59 = 47.5%); rebadge = sed 2649->2650 (5 tokens) + docstring verification-27->28 bump + chain insert c2649 = verification 27 before the c2648 citation + rebadged-from -> validate_cycle2649.py + P-HIST WATCH (pre-patch table {2649:5, 2648:2, 2647:1, 2646:3, 2645:7, 2644:1, 2643:1, 2624:1, 2623:2, 2576:4, 2577:3} asserted on ACTUAL bytes; post-patch {2650:5, 2649:2, 2648:1, 2647:1, 2646:3, ...} lineage citations == 2 - the c2573 LESSON, carried; HIST-restore NO-OPs expected - the LOSS block history keeps cite c2646, sed-immune); INSTRUMENTATION: captured-class pattern STANDARD, mandatory order (pre-echo -> curl -o/-w -> post-echo) permanent; harness staged BEFORE any scan POST; SLOT WATCH: NO outstanding pre-window rung this time (the 09:54:44 4500b was consumed EARLY by c2649) - the dispatched c2650 candidate is 09:59:44 (4800b, epoch 1793066384, first rung inside window-2650 09:57:21.184685968; deferred-servicing claim if stamped late, EARLY-claim if stamped pre-rung - both NORMAL per the c2649 precedent), then 10:04:44 (5100b), 10:09:44 (5400b), 10:14:44 (5700b), or a ghost - all live (the STAMP governs; wobble risk noted on every rung); TOKEN WATCH on a 09:59:44 keyed rung (minute 59): 1000 (+1), 1002 (+3), 1004 (+5), 1005 (+6), 1006 (+7), 1007 (+8), 1008 (+9), 1009 (+10) - all live (hour-rollover on the 1000-class tokens); DD WATCH: post-loss series member 4 @ 446.00 (drain) - continued drain (dd#224 < 446.00) vs plateau vs re-escalation (dd#224 > 446.00 re-opens escalation) all live; a sub-11.287 dd sets a NEW ALL-TIME CAPTURED MINIMUM (context-carried threshold); EP14 watch - ARM run member 1 (s239): s240 dual 2.1-2.4 extends ARM member 2, dual 2.0-2.1 flips GRAY, dual sub-2.0 flips STALL (re-opens member 1), dual above-2.4 re-opens OPEN, cross-class split resolves to the client class; era-high defense: 6.273332/6264 stands until exceeded; Echo: new sweep 2.171020..2.181020 / 2160..2170 (k=341), account 83-for-383; DRIFT-#45 watch - baseline (18,0,0,18,0) @ 446B: verification 28 on match; any movement or honest emergence = DRIFT-#46 two-pass (paid emergence = GOLD - scam-check + EV path per protocol).
- No gold yet. Scanner continues.
"""

n_lines = entry.count("\n")
total = 8183 + n_lines
entry = entry.replace("@@TOTAL@@", str(total)).replace("@@N@@", str(n_lines))

cur = open(WORKLOG).read()
cur_lines = cur.count("\n")
assert cur_lines == 8183, f"worklog moved: {cur_lines} != 8183"
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
