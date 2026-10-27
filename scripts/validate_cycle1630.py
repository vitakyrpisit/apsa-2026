#!/usr/bin/env python3
"""Validator for cycle 1630.

POST-ROLLBACK-#6 REBASE POINT (new era root; prior era root
validate_cycle1506.py and entire drift-#9 validator chain
validate_cycle1506..1562.py were ERASED by midnight rollback event #6).

Rollback event #6 (6th occurrence of item (g)): detected 2026-10-20
00:01:46 +08 on first post-outage trigger (session outage 12:25->00:00,
3RD consecutive day, item (j) manifested again after surviving past
12:25 at c1562). Filesystem rolled back to ~Oct 13 04:29 snapshot:
  - worklog.md restored to Oct 13 state (342 entries, all drift-#9 era
    entries c1495..c1562 gone; worklog mtime Oct 13 04:29)
  - scripts/: all validate_cycle*.py, scan_cycle15*.json archives,
    recursive_diff.py ERASED (only cycle-210-era files survive)
  - tool-results/: scan_c1555..c1562.json erased
  - .basedagents/ tree ENTIRELY GONE (keypair (a) absent along with dir)
Drift-#9 era record preserved ONLY in conversation context:
  1562 executions, 0 claims, 0 violations, 0 spend, 0 revenue;
  68 clean validator cycles (c1495..c1562); baseline was
  (28,5,4,16,3) @ 48344B / normalized 49257.

Drift #12 observed at c1630 (trigger 2026-10-20 00:46:46 +08): honest_free
3->2, total 27->26; paid/scam/unknown unchanged (4/17/3). Second honest_free
exit in 3 cycles (sequential aging-out pattern). Identity unobservable (no
honest_free detail payloads). Paid set unchanged: same 4 WURK IDs,
funded/open/unclaimed. GOLD STILL LIVE 4/5. Size unchanged 40360B.
REBASED baseline (26,4,2,17,3) per drift-#12; prior era root
validate_cycle1569.py (drift-#11 era, 2 obs).

Drift #11 observed at c1630 (trigger 2026-10-20 00:31:46 +08): honest_free
4->3, total 28->27; paid/scam/unknown unchanged (4/17/3). One honest_free
task left the market - identity unobservable (no honest_free detail
payloads in response). Paid set unchanged: same 4 WURK IDs, funded/open/
unclaimed. GOLD STILL LIVE 4/5. Size unchanged 40360B. REBASED baseline
(27,4,3,17,3) per drift-#11; prior era root validate_cycle1563.py.

Drift #10 observed at c1630 (trigger 2026-10-20 00:01:46 +08, scanned_at
2026-10-19T16:03:46.361Z = 00:03:46 +08, ~2 min trigger latency):
  - WURK onboarding pilot 1/5 (task_Kl7s8M1zDFwnV4u85Lr10) EXITED the
    honest_paid set during the 11.6h outage window. Exact cause
    unobservable in scan payload (task absent from response entirely;
    candidates: external claim, creator cancellation, heuristic
    reclassification - +1 scam count is consistent but not provable).
  - Delta vs drift-#9 baseline: honest_paid 5->4, scam 16->17;
    total/honest_free/unknown unchanged (28/4/3).
  - Response size 48344B -> 40360B (one ~8KB task detail payload gone).
  - Remaining 4/5 WURK slots re-verified in-response: escrow=funded,
    status=open, claimed_by=None. GOLD STILL LIVE.

Assertions encode the drift-#10 baseline (28,4,4,17,3) @ 40360B:
  - response size 40360 bytes
  - BA composition: total=28 honest_paid=4 honest_free=4 scam=17 unknown=3
  - 4 honest paid tasks, best_paid_task=task_tCnB8RqX3b3iOrNjXBHVW
  - all escrow status=funded
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1630
RAW = "/home/z/my-project/scripts/scan_cycle1630_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1630.json"
# c1630 diagnosis: raw size fluctuates 40360<->40361 purely from
# scan_duration_ms digit count (5-digit 12031ms at c1630 vs 4-digit prior);
# normalized recursive_diff proved MARKET_UNCHANGED (41087=41087).
# Baseline is therefore a BAND, not an exact value. Composition +
# normalized diff remain the authoritative drift sensors.
BASELINE_SIZE_BAND = (40360, 40361)
BASELINE_COMP = {"total": 26, "honest_paid": 4, "honest_free": 2, "scam": 17, "unknown": 3}
BEST_PAID = "task_tCnB8RqX3b3iOrNjXBHVW"
EXPECTED_PAID_IDS = [
    "task_tCnB8RqX3b3iOrNjXBHVW",
    "task_8zjlRRChZW7kWIb0Oy6Ai",
    "task_qKxsDuYZks86pyzXcpgpU",
    "task_5yzaOsv8NK1uNPtq59d2v",
]

failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"ok: {name}" + (f" ({detail})" if detail else ""))
    else:
        failures.append(f"{name} ({detail})")
        print(f"FAIL: {name} ({detail})")


with open(RAW, "rb") as f:
    raw_bytes = f.read()
print(f"clean_body_bytes={len(raw_bytes)}")
check("size_matches_baseline_band", len(raw_bytes) in BASELINE_SIZE_BAND,
      f"{len(raw_bytes)}B vs band {BASELINE_SIZE_BAND}")

d = json.loads(raw_bytes)
ba = d.get("basedagents", {})
hp = ba.get("all_honest_paid", []) or []
tb = d.get("taskbounty", {})

comp = {
    "total": ba.get("total_tasks"),
    "honest_paid": ba.get("honest_paid"),
    "honest_free": ba.get("honest_free"),
    "scam": ba.get("scam_pattern"),
    "unknown": ba.get("unknown"),
}
print(f"scanned_at={d.get('scanned_at')}")
print(f"scan_duration_ms={d.get('scan_duration_ms')}")
print(f"BA composition: total={comp['total']} honest_paid={comp['honest_paid']} "
      f"honest_free={comp['honest_free']} scam={comp['scam']} unknown={comp['unknown']}")
check("baseline_match", comp == BASELINE_COMP, str(comp))
check("all_honest_paid_len", len(hp) == BASELINE_COMP["honest_paid"], f"len={len(hp)}")

for t in hp:
    tid = t.get("task_id")
    esc = (t.get("escrow") or {}).get("status")
    print(f"  paid_task={tid} bounty={t.get('bounty', {}).get('amount_atomic')} "
          f"{t.get('bounty', {}).get('token')} escrow={esc} status={t.get('status')} "
          f"claimed_by={t.get('claimed_by')}")
    check(f"escrow_funded:{tid}", esc == "funded", str(esc))
    check(f"status_open:{tid}", t.get("status") == "open", str(t.get("status")))
    check(f"unclaimed:{tid}", t.get("claimed_by") is None, str(t.get("claimed_by")))

ids = [t.get("task_id") for t in hp]
check("expected_paid_ids", sorted(ids) == sorted(EXPECTED_PAID_IDS), str(ids))

bpt = ba.get("best_paid_task") or {}
check("best_paid_task", bpt.get("task_id") == BEST_PAID, str(bpt.get("task_id")))

print(f"taskbounty: api_key={tb.get('api_key_configured')} bounties={tb.get('total_bounties')} "
      f"paid_missions={tb.get('paid_missions')}")
check("taskbounty_no_key", tb.get("api_key_configured") is False)
check("taskbounty_paid_zero", (tb.get("paid_missions") or 0) == 0)
check("clawlancer_absent", "clawlancer" not in json.dumps(d).lower())
check("auto_claim_pending_false", d.get("auto_claim_pending") is False)
check("next_scan_300", d.get("next_scan_in_seconds") == 300, str(d.get("next_scan_in_seconds")))

if failures:
    print(f"ASSERTION_FAILURES: {len(failures)}")
    for f_ in failures:
        print(f"  - {f_}")
    sys.exit(1)

with open(PRETTY, "w") as f:
    f.write(json.dumps(d, indent=2, sort_keys=False) + "\n")
print(f"archive_written={PRETTY}")
print("ALL_ASSERTIONS_PASSED")
print(f"baseline_match_c{CYCLE}=true")
