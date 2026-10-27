#!/usr/bin/env python3
"""Validator for cycle 1714.

DRIFT-#15 REBASE POINT (new era root; prior drift-#14 validator chain
validate_cycle1711..1712.py encoded the (24,3,1,17,3) @ 32376B baseline
and is retired by this drift event).

Context: trigger outage 2026-10-20 12:36:50 -> 2026-10-21 00:01:50 +08
(~142 scheduled triggers undelivered, ~11.5h gap). NO filesystem
rollback occurred (worklog 607606B continuous, mtime = c1712 closure;
all c1711/c1712 artifacts intact) — outage-only event, unlike rollback
#7. Cycle numbering continued at c1713; the gap is unscannable
(retrospective market states unrecoverable) and recorded honestly.

Drift event #15: detected at c1713 (scanned_at 2026-10-20T16:03:07.962Z
= 2026-10-21 00:03:07 +08, scan_duration_ms=2636 fast band, raw 24392B,
-7984B vs drift-#14 band). Changes vs drift-#14 baseline (24,3,1,17,3):
  - task_8zjlRRChZW7kWIb0Oy6Ai (WURK onboarding pilot 4/5, 0.10 USDC,
    the drift-#14 best_paid_task) DISAPPEARED (cause not determinable:
    API returns only open tasks; claimed-vs-delisted indistinguishable)
  - honest_paid 3->2; surviving slots: qKxsDuYZ (pilot 3/5, now best),
    5yzaOsv8 (pilot 2/5) — both bounty=100000 raw (0.10 USDC),
    escrow=funded, open, unclaimed
  - honest_free 1->5 (+4 new free tasks; payload carries counts only,
    no free-task detail field — recorded as count-only fact)
  - scam 17->18 (+1); unknown 3 unchanged; total 24->28
  - all other facets unchanged: taskbounty api_key=False
    paid_missions=0, clawlancer absent, auto_claim_pending=False,
    next_scan=300

Old-baseline probe evidence (validate_cycle1712.py logic against c1713
payload, scratch run, artifacts cleaned): ASSERTION_FAILURES: 5 —
  size_matches_baseline_band (24392B vs band (32376, 32377)),
  baseline_match ((28,2,5,18,3) vs (24,3,1,17,3)),
  all_honest_paid_len (2 vs 3),
  expected_paid_ids (8zjlRRCh missing),
  best_paid_task (qKxsDuYZ != 8zjlRRCh).
All per-task assertions for surviving slots passed.

recursive_diff c1712 vs c1713 (correct arg order <new> <old>):
MARKET_CHANGED (stripped canonical 32975 -> 24834). Drift-#15 era
stripped-canonical constant: 24834 bytes.

Assertions encode the drift-#15 baseline (28,2,5,18,3) @ 24392B:
  - response size 24392 bytes (band 24392-24393)
  - BA composition: total=28 honest_paid=2 honest_free=5 scam=18 unknown=3
  - 2 honest paid tasks, best_paid_task=task_qKxsDuYZks86pyzXcpgpU
  - all escrow status=funded, status=open, unclaimed
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1714
RAW = "/home/z/my-project/scripts/scan_cycle1714_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1714.json"
BASELINE_SIZE_BAND = (24392, 24393)
BASELINE_COMP = {"total": 28, "honest_paid": 2, "honest_free": 5, "scam": 18, "unknown": 3}
BEST_PAID = "task_qKxsDuYZks86pyzXcpgpU"
EXPECTED_PAID_IDS = [
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
