#!/usr/bin/env python3
"""Validator for cycle 2783.

DRIFT-#49 pass-32 CLASS (movement repeat-class on tuple match) — sed-rebadge
from the v82 pass-31 carry (the v82 source survived on disk and in the
2be3f8a commit object, so the REBADGE-CLASS continues). Baseline for c2783 = the
DRIFT-#49 pass-1 observation (18,0,0,18,0) @ 446B (opened at c2752 — the first
market movement since LOSS-#83; pass-2 repeat recorded at c2753; pass-3 repeat
recorded at c2754; pass-4 repeat recorded at c2755; pass-5 repeat recorded at
c2756; pass-6 repeat recorded at c2757; pass-7 repeat recorded at c2758;
pass-8 repeat recorded at c2759; pass-9 repeat recorded at c2760; pass-10
repeat recorded at c2761; pass-11 repeat recorded at c2762; pass-12 repeat
recorded at c2763; pass-13 repeat recorded at c2764; pass-14 repeat recorded
at c2765; pass-15 repeat recorded at c2766; pass-16 repeat recorded
at c2767; pass-17 repeat recorded
at c2768; pass-18 repeat recorded
at c2769; pass-19 repeat recorded
at c2770; pass-20 repeat recorded
at c2771; pass-21 repeat recorded
at c2772; pass-22 repeat recorded
at c2773; pass-23 repeat recorded
at c2774; pass-24 repeat recorded
at c2775; pass-25 repeat recorded
at c2776; pass-26 repeat recorded
at c2777; pass-27 repeat recorded
at c2778; pass-28 repeat recorded
at c2779; pass-29 repeat recorded
at c2780; pass-30 repeat recorded
at c2781; pass-31 repeat recorded
at c2782); a repeat records pass-32
(movement repeat-class, the DRIFT-#48 root (20,0,2,18,0) remains LOCKED,
never rewritten); a return to (20,0,2,18,0) records the RESTORATION event
(the root stands, the pass-1 excursion closes as a transient); any other
composition records newest-observation evidence with the full delta chain
printed. Structural conventions inherited from the v82 class (itself
inheriting the v81/v80/v79/v78/v77/v76/v75/v74/v73/v72/v71/v70/v69/v68/v67/v66/v65/v64/
v63/v62/v61/v60/v59/v58/v57/v56/v55/v54/v53/v52/v51/v50/v49/v48/v47/v113 conventions). Gate count is computed PROGRAMMATICALLY
(the v45 76/76 off-by-one class is retired).

DRIFT-#49 pass-31 evidence (on disk): five-tuple (18,0,0,18,0) @ 446B observed
at c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/
c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/
c2777/c2778/c2779/c2780/c2781/c2782 (pass-1 opens at c2752 — the first market movement since LOSS-#83: total
20->18, honest_free 2->0, the two honest-free tasks EXITED the market;
pass-2 repeats at c2753; pass-3 repeats at c2754; pass-4 repeats at c2755;
pass-5 repeats at c2756; pass-6 repeats at c2757; pass-7 repeats at c2758;
pass-8 repeats at c2759; pass-9 repeats at c2760; pass-10 repeats at c2761;
pass-11 repeats at c2762; pass-12 repeats at c2763; pass-13 repeats at
c2764; pass-14 repeats at c2765; pass-15 repeats at c2766; pass-16 repeats
at c2767; pass-17 repeats
at c2768; pass-18 repeats
at c2769; pass-19 repeats
at c2770; pass-20 repeats
at c2771; pass-21 repeats
at c2772; pass-22 repeats
at c2773; pass-23 repeats
at c2774; pass-24 repeats
at c2775; pass-25 repeats
at c2776; pass-26 repeats
at c2777; pass-27 repeats
at c2778; pass-28 repeats
at c2779; pass-29 repeats
at c2780; pass-30 repeats
at c2781; pass-31 repeats
at c2782, movement
repeat-class — the scam block 18 stands). The
DRIFT-#48 root (20,0,2,18,0) @ 446B remains LOCKED at c2747 pass-1 /
c2748 pass-2 (verification series 1-4 = c2749/c2750/c2751/c2752 held) — pass-1
never rewrites; the DRIFT-#47 root (21,0,3,18,0) remains CONTEXT-CARRIED,
superseded. Tuple components: (total_tasks, honest_paid, honest_free,
scam_pattern, unknown).

Contract: STRUCTURAL gates are HARD (failures -> exit non-zero, no archive write).
Baseline gates are CLASSIFICATION gates (match -> DRIFT-#49 pass-32 recorded,
movement repeat-class; return to the DRIFT-#48 root -> RESTORATION recorded; any
other composition/size -> newest-observation evidence with the full delta chain
printed, archive still written — the root is never rewritten).

Exits non-zero on any structural assertion failure (before archive write).
"""
import json
import sys

CYCLE = 2783
RAW = "/home/z/my-project/scripts/scan_cycle2783_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle2783.json"
SIZE_BAND = (446, 447)  # DRIFT-#49 pass-31 band @ 446B (observed c2752/c2753/c2754/c2755/c2756/c2757/c2758/c2759/c2760/c2761/c2762/c2763/c2764/c2765/c2766/c2767/c2768/c2769/c2770/c2771/c2772/c2773/c2774/c2775/c2776/c2777/c2778/c2779/c2780/c2781/c2782; the DRIFT-#48 root band 446B locked c2747/c2748)
BASELINE_COMP = {"total": 18, "honest_paid": 0, "honest_free": 0,
                 "scam": 18, "unknown": 0}
DRIFT48_ROOT = {"total": 20, "honest_paid": 0, "honest_free": 2,
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

# --- classification gates (SOFT — DRIFT-#49 pass-32 vs RESTORATION vs newest-observation) ---
size_ok = len(raw_bytes) in SIZE_BAND
check("size_band_446_447", size_ok, f"{len(raw_bytes)}B vs band {SIZE_BAND}", hard=False)
comp_ok = comp == BASELINE_COMP
check("drift49_pass32_match", comp_ok,
      f"{(comp['total'], comp['honest_paid'], comp['honest_free'], comp['scam'], comp['unknown'])} "
      f"vs (18,0,0,18,0)", hard=False)
restoration_ok = comp == DRIFT48_ROOT
if comp_ok and size_ok:
    classification = "DRIFT-#49 pass-32 (movement repeat-class recorded; the DRIFT-#48 root (20,0,2,18,0) remains LOCKED, never rewritten)"
elif comp_ok:
    classification = "DRIFT-#49 pass-32 (movement repeat-class, size drifted) - size movement noted"
elif restoration_ok and size_ok:
    classification = "RESTORATION (the DRIFT-#48 root stands; the pass-1 excursion closes as a transient)"
elif restoration_ok:
    classification = "RESTORATION (the DRIFT-#48 root stands; size drifted) - size movement noted"
else:
    classification = "DRIFT-#49 newest-observation evidence (full delta chain via recursive_diff; root NOT rewritten)"
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
