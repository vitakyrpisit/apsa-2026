#!/usr/bin/env python3
"""Validator for cycle 1414.

Rebuilt from scratch after ROLLBACK EVENT #5 (2026-10-19 ~00:00 +08:00) which
restored the 2026-10-13T12:29 snapshot and destroyed the validator chain
(validate_cycle665..1413.py all lost).

Assertions encode the drift-#8 rebased baseline (established at c1448,
first cycle after ROLLBACK #5; prior drift-#7 baseline (25,0,6,16,3)
drifted to (23,0,4,16,3) — honest_free 6->4, total 25->23, scam/unknown/paid unchanged):
  - response size 446 bytes
  - BA composition: total=23 honest_paid=0 honest_free=4 scam=16 unknown=3
  - no honest paid task (all_honest_paid_len=0, best_paid_task=null)
  - taskbounty: no api_key, paid_missions=0
  - clawlancer absent, auto_claim_pending=false

Exits non-zero on any assertion failure.
"""
import json
import sys

CYCLE = 1448
RAW = "/home/z/my-project/scripts/scan_cycle1448_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1448.json"
BASELINE_SIZE = 446
BASELINE_COMP = {"total": 23, "honest_paid": 0, "honest_free": 4, "scam": 16, "unknown": 3}

def fail(msg):
    print(f"ASSERT_FAIL: {msg}")
    sys.exit(1)

raw = open(RAW, "rb").read()
clean = raw.strip()
print(f"clean_body_bytes={len(clean)}")

if len(clean) != BASELINE_SIZE:
    fail(f"size {len(clean)} != baseline {BASELINE_SIZE}")
print(f"size_matches_baseline=true ({len(clean)}B vs {BASELINE_SIZE}B)")

try:
    d = json.loads(clean)
except Exception as e:
    fail(f"json invalid: {e}")
print("json_valid=true")
print(f"scanned_at={d.get('scanned_at')}")
print(f"scan_duration_ms={d.get('scan_duration_ms')}")

ba = d.get("basedagents", {})
# Actual key names verified from raw response at c1448:
# total_tasks / honest_paid / honest_free / scam_pattern / unknown / best_paid_task / all_honest_paid
comp = {
    "total": int(ba.get("total_tasks", 0) or 0),
    "honest_paid": int(ba.get("honest_paid", 0) or 0),
    "honest_free": int(ba.get("honest_free", 0) or 0),
    "scam": int(ba.get("scam_pattern", 0) or 0),
    "unknown": int(ba.get("unknown", 0) or 0),
}

print(f"BA composition: total={comp['total']} honest_paid={comp['honest_paid']} honest_free={comp['honest_free']} scam={comp['scam']} unknown={comp['unknown']}")

if comp != BASELINE_COMP:
    fail(f"composition {comp} != drift-#8 baseline {BASELINE_COMP}")
print(f"baseline_match_c{CYCLE}=true")

honest_paid = ba.get("all_honest_paid") or []
honest_paid_len = len(honest_paid) if isinstance(honest_paid, (list, dict)) else int(honest_paid or 0)
print(f"all_honest_paid_len={honest_paid_len}")
if honest_paid_len != 0:
    fail(f"honest_paid_len {honest_paid_len} != 0")

bpt = d.get("best_paid_task")
print(f"best_paid_task={bpt if bpt is None else 'NONNULL:' + str(bpt)[:80]}")
if bpt is not None:
    fail(f"best_paid_task non-null: {bpt}")

tb = d.get("taskbounty", {})
print(f"taskbounty: api_key={bool(tb.get('api_key'))} bounties={len(tb.get('bounties', []) or [])} paid_missions={len(tb.get('paid_missions', []) or [])}")
if tb.get("api_key"):
    fail("taskbounty api_key present (unexpected)")
if len(tb.get("paid_missions", []) or []) != 0:
    fail("taskbounty paid_missions > 0")

cl = d.get("clawlancer", {})
clawlancer_present = bool(cl) or (d.get("clawlancer_present") is True)
print(f"clawlancer_present={clawlancer_present}")
if clawlancer_present:
    fail("clawlancer present (unexpected)")

acp = d.get("auto_claim_pending", False)
print(f"auto_claim_pending={acp}")
if acp:
    fail("auto_claim_pending=true (unexpected)")

print(f"next_scan_in_seconds={d.get('next_scan_in_seconds')}")

with open(PRETTY, "w") as f:
    json.dump(d, f, indent=2, sort_keys=True)
print(f"archive_written={PRETTY}")
print("ALL_ASSERTIONS_PASSED")
