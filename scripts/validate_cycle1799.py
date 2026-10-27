#!/usr/bin/env python3
"""Validator for cycle 1799.

DRIFT-#17 REBASE POINT (new era root; prior drift-#16 validator chain
validate_cycle1715..1797.py encoded the (27,1,5,18,3) @ 16408B baseline
and is retired by this drift event).

Drift event #17: detected at c1797 (scanned_at 2026-10-20T23:02:35.950Z
= 2026-10-21 07:02:35 +08, scan_duration_ms=2080 fast band, raw 16408B,
+0B vs drift-#16 band). Changes vs drift-#16 baseline (27,1,5,18,3):
  - total_tasks 27->29 (+2); scam_pattern 18->20 (+2)
  - honest_paid 1->1, honest_free 5->5, unknown 3->3 all unchanged
  - raw payload +0B: the 2 new scam tasks are aggregate-counter-only
    entries; the API does not itemize scam tasks (no IDs/titles
    exposed), so their content is not determinable from the response
  - honest_paid list unchanged: sole slot task_qKxsDuYZks86pyzXcpgpU
    (pilot 3/5) bounty=100000 raw (0.10 USDC), escrow=funded, open,
    unclaimed; best_paid_task unchanged
  - all other facets unchanged: taskbounty api_key=False
    paid_missions=0, clawlancer absent, auto_claim_pending=False,
    next_scan=300

recursive_diff c1796 vs c1797 (correct arg order <new> <old>):
MARKET_CHANGED (stripped canonical 16693 -> 16693, same-length
different-bytes — exact signature of 2-digit counter substitution
27->29 / 18->20 with zero structural payload change).

drift-#16 era MARKET_UNCHANGED streak: ENDED at 81 (c1715..c1796).
drift-#17 era streak restarts at 0 from c1797.

Assertions encode the drift-#17 baseline (29,1,5,20,3) @ 16408B:
  - response size 16408 bytes (band 16408-16409)
  - BA composition: total=29 honest_paid=1 honest_free=5 scam=20 unknown=3
  - 1 honest paid task, best_paid_task=task_qKxsDuYZks86pyzXcpgpU
  - escrow status=funded, status=open, unclaimed
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false, next_scan=300

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1799
RAW = "/home/z/my-project/scripts/scan_cycle1799_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1799.json"
BASELINE_SIZE_BAND = (16408, 16409)
BASELINE_COMP = {"total": 29, "honest_paid": 1, "honest_free": 5, "scam": 20, "unknown": 3}
BEST_PAID = "task_qKxsDuYZks86pyzXcpgpU"
EXPECTED_PAID_IDS = [
    "task_qKxsDuYZks86pyzXcpgpU",
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
