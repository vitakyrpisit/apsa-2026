#!/usr/bin/env python3
"""Validator for cycle 2747.

DRIFT-#47 verification-9 CLASS (record extends on tuple match) — REBUILT-FROM-CONTEXT
post-LOSS-#83: the v46 source (validate_cycle2746.py) and the entire c2736..c2746
corpus were WIPED by the LOSS EVENT #83 snapshot rollback (environment re-provisioned
2026-10-29 ~16:01 UTC to the post-LOSS-#79-recon state). This validator is a FRESH
reconstruction implementing the context-carried DRIFT-#47 verification-9 gate; it is
NOT a byte-exact rebadge (the rebadge source does not exist on disk). Structural
conventions inherited from the disk-surviving validate_cycle2735.py (v113-class,
DRIFT-#45 verification-113 carry). Gate count is computed PROGRAMMATICALLY (the
v45 76/76 off-by-one class is retired).

DRIFT-#47 root (CONTEXT-CARRIED): five-tuple (21,0,3,18,0) @ 446B LOCKED at
c2738 pass-1 / c2739 pass-2; verifications 1-8 = c2738..c2746, all honest_paid=0
(context-carried; disk record lost). Tuple components:
(total_tasks, honest_paid, honest_free, scam_pattern, unknown).

Contract: STRUCTURAL gates are HARD (failures -> exit non-zero, no archive write).
Baseline gates are CLASSIFICATION gates (match -> DRIFT-#47 verification-9 record
extends; any other composition/size -> DRIFT-#48 pass-1 opened, movement evidence
recorded, archive still written — pass-1 never rewrites the root).

Exits non-zero on any structural assertion failure (before archive write).
"""
import json
import sys

CYCLE = 2747
RAW = "/home/z/my-project/scripts/scan_cycle2747_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2747.json"
SIZE_BAND = (446, 447)  # context-carried DRIFT-#47 band @ 446B
BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 3,
                 "scam": 18, "unknown": 0}

failures = []       # HARD structural failures
soft_notes = []     # classification observations
gate_count = 0      # programmatic counter (off-by-one class retired)


def check(name, cond, detail="", hard=True):
    global gate_count
    gate_count += 1
    if cond:
        print(f"ok: {name}" + (f" ({detail})" if detail else ""))
    else:
        line = f"{name} ({detail})"
        if hard:
            failures.append(line)
            print(f"FAIL: {line}")
        else:
            soft_notes.append(line)
            print(f"SOFT: {line}")


with open(RAW, "rb") as f:
    raw_bytes = f.read()
print(f"clean_body_bytes={len(raw_bytes)}")

# --- structural gates (HARD) ---
try:
    json.loads(raw_bytes)
    _parses = True
except Exception as _e:
    _parses = False
    _parse_err = str(_e)
check("json_parse", _parses, _parse_err if not _parses else f"{len(raw_bytes)}B")
d = json.loads(raw_bytes)

check("scanned_at_str", isinstance(d.get("scanned_at"), str), repr(d.get("scanned_at")))
check("scan_duration_ms_int", isinstance(d.get("scan_duration_ms"), int),
      repr(d.get("scan_duration_ms")))
ba = d.get("basedagents")
check("basedagents_obj", isinstance(ba, dict), type(ba).__name__)
tb = d.get("taskbounty")
check("taskbounty_obj", isinstance(tb, dict), type(tb).__name__)
for k in ("total_tasks", "honest_paid", "honest_free", "scam_pattern", "unknown",
          "best_paid_task", "all_honest_paid"):
    check(f"ba_key:{k}", k in ba, repr(ba.get(k, "<absent>")))
for k in ("api_key_configured", "total_bounties", "paid_missions", "best_bounty",
          "all_bounties"):
    check(f"tb_key:{k}", k in tb, repr(tb.get(k, "<absent>")))
check("auto_claim_pending_false", d.get("auto_claim_pending") is False,
      repr(d.get("auto_claim_pending")))
check("next_scan_int", isinstance(d.get("next_scan_in_seconds"), int),
      repr(d.get("next_scan_in_seconds")))
check("clawlancer_absent", "clawlancer" not in json.dumps(d).lower())

comp = {
    "total": ba.get("total_tasks"),
    "honest_paid": ba.get("honest_paid"),
    "honest_free": ba.get("honest_free"),
    "scam": ba.get("scam_pattern"),
    "unknown": ba.get("unknown"),
}
hp = ba.get("all_honest_paid", []) or []
print(f"scanned_at={d.get('scanned_at')}")
print(f"scan_duration_ms={d.get('scan_duration_ms')}")
print(f"BA composition: total={comp['total']} honest_paid={comp['honest_paid']} "
      f"honest_free={comp['honest_free']} scam={comp['scam']} unknown={comp['unknown']}")
check("hp_len_consistent", len(hp) == (comp["honest_paid"] or 0),
      f"len={len(hp)} vs honest_paid={comp['honest_paid']}")

# per-task paid assertions (self-skip when empty) — escrow/status/unclaimed
for t in hp:
    tid = t.get("task_id")
    esc = (t.get("escrow") or {}).get("status")
    print(f"  paid_task={tid} bounty={t.get('bounty', {}).get('amount_atomic')} "
          f"{t.get('bounty', {}).get('token')} escrow={esc} status={t.get('status')} "
          f"claimed_by={t.get('claimed_by')}")
    check(f"escrow_funded:{tid}", esc == "funded", str(esc))
    check(f"status_open:{tid}", t.get("status") == "open", str(t.get("status")))
    check(f"unclaimed:{tid}", t.get("claimed_by") is None, str(t.get("claimed_by")))

bpt = ba.get("best_paid_task")
check("best_paid_task_null_or_obj", bpt is None or isinstance(bpt, dict), repr(bpt))
check("taskbounty_no_key", tb.get("api_key_configured") is False,
      repr(tb.get("api_key_configured")))

# --- GOLD CHECK (absent-key class per the context-carried c2746 gold account) ---
derived_gold = (comp["honest_paid"] or 0) > 0 or (tb.get("paid_missions") or 0) > 0 \
    or bpt is not None
check("has_gold_key_absent", "has_gold" not in d, "<absent-key class>")
print(f"GOLD_CHECK: has_gold(derived)={derived_gold} honest_paid={comp['honest_paid']} "
      f"best_paid_task={'None' if bpt is None else bpt.get('task_id')} "
      f"paid_missions={tb.get('paid_missions')} total_bounties={tb.get('total_bounties')}")

# --- classification gates (SOFT — DRIFT-#47 verification-9 vs DRIFT-#48 pass-1) ---
size_ok = len(raw_bytes) in SIZE_BAND
check("size_band_446_447", size_ok, f"{len(raw_bytes)}B vs band {SIZE_BAND}", hard=False)
comp_ok = comp == BASELINE_COMP
check("drift47_tuple_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (21,0,3,18,0)", hard=False)
if comp_ok and size_ok:
    classification = "DRIFT-#47 verification-9 (record extends, eighth post-root carry; baseline CARRY UNCHANGED)"
elif comp_ok:
    classification = "DRIFT-#47 verification-9 (tuple match, size drifted) - size movement noted"
else:
    classification = "DRIFT-#48 PASS-1 (movement evidence recorded; root NOT rewritten)"
print(f"CLASSIFICATION: {classification}")

if failures:
    print(f"ASSERTION_FAILURES: {len(failures)}")
    for f_ in failures:
        print(f"  - {f_}")
    print(f"gate_count={gate_count} hard_failures={len(failures)} soft_notes={len(soft_notes)}")
    sys.exit(1)

with open(PRETTY, "w") as f:
    f.write(json.dumps(d, indent=2, sort_keys=False) + "\n")
print(f"archive_written={PRETTY}")
print(f"gate_count={gate_count} hard_failures=0 soft_notes={len(soft_notes)}")
print("ALL_STRUCTURAL_ASSERTIONS_PASSED")
print(f"classification_c{CYCLE}={classification}")
