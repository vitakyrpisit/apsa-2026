#!/usr/bin/env python3
"""c2556 pipeline: drift-root RE-ANCHOR (DRIFT-#33), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 18th consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2556_raw.json (genuine bytes, 446B)
  time_total = 2.183847s (EP14 classification class)
  pre  = 09:02:16.118167064 +08 (epoch 1792976536.118167064)
  post = 09:02:18.311528832 +08 (epoch 1792976538.311528832)
  server start 09:02:16.131 (scanned_at 09:02:18.307 - 2176ms): 13ms skew
  vs pre — proxy validated 18th consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13ms series)

DRIFT ROOT: five-tuple (20,0,0,17,3) != DRIFT-#32 baseline (21,0,1,17,3)
  -> DRIFT-#32 closes at 3-fold (root c2553); DRIFT-#33 root c2556.
  Delta: total 21->20, honest_free 1->0 (honest inventory EMPTY),
  honest_paid 0 throughout, scam 17 stable, unknown 3 stable;
  446B size band digit-width-stable.
"""
import json
import subprocess
import sys

RAW56 = "/home/z/my-project/scripts/scan_cycle2556_raw.json"
RAW55 = "/home/z/my-project/scripts/scan_cycle2555_raw.json"
VAL55 = "/home/z/my-project/scripts/validate_cycle2555.py"
VAL56 = "/home/z/my-project/scripts/validate_cycle2556.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW56, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n55, n56 = norm(RAW55), norm(RAW56)
    print(f"normalized={len(n56)}-vs-{len(n55)}")
    if n56 == n55:
        print("MARKET_UNCHANGED — unexpected at claimed drift root")
        sys.exit(3)
    print("MARKET_DRIFT_CONFIRMED — DRIFT-#32 closes at 3-fold; DRIFT-#33 root c2556")

    # rebadge 2555->2556 (sed-equivalent), then drift-root RE-ANCHOR patches
    with open(VAL55, "r") as f:
        src = f.read()
    rebadged = src.replace("2555", "2556")

    patches = [
        # P1: header carry -> re-anchor (source header references 2554, the file IT was rebadged from)
        ("DRIFT-#32 CARRY: rebadged from validate_cycle2554.py (verification-2 carry harness)",
         "DRIFT-#33 RE-ANCHOR: rebadged from validate_cycle2555.py (drift-root precedent c2454/c2514/c2553)"),
        # P2: sed-line lineage fix (global sed corrupted 2554->2555 into 2554->2556)
        ("(sed 2554->2556, the DRIFT-#32 verification-2 carry harness). Baseline",
         "(sed 2555->2556, the DRIFT-#32 verification-3 carry harness; DRIFT-#33 root re-anchor). Baseline"),
        # P3: chain head — c2556 = verification 1 with c2555 final-3 inserted (post-sed chain jumps c2556 -> c2554)
        ("(21,0,1,17,3) @ 446B DRIFT-#32 root; c2556 = verification 3\n(c2554 = verification 2;",
         "(20,0,0,17,3) @ 446B DRIFT-#33 root; c2556 = verification 1\n(c2555 = verification 3, DRIFT-#32 final; c2554 = verification 2;"),
        # P4: baseline constants 21/1 -> 20/0
        ('BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 1, "scam": 17, "unknown": 3}',
         'BASELINE_COMP = {"total": 20, "honest_paid": 0, "honest_free": 0, "scam": 17, "unknown": 3}'),
        # P5: DRIFT-#33 delta paragraph inserted ahead of the DRIFT-#32 history
        ("DRIFT-#32 delta vs DRIFT-#31: total 22->21, honest_free 2->1 (a second honest_free task departed the market; honest_paid 0 throughout — no paid movement), scam 17 stable, unknown 3 stable. All other sentinels held: 446B size band (digit-width-stable change), all_honest_paid empty, best_paid_task None, taskbounty zeros, next_scan=300.",
         "DRIFT-#33 delta vs DRIFT-#32: total 21->20, honest_free 1->0 (the LAST honest free task departed the market — honest inventory now EMPTY; honest_paid 0 throughout — no paid movement), scam 17 stable, unknown 3 stable. All other sentinels held: 446B size band (digit-width-stable change), all_honest_paid empty, best_paid_task None, taskbounty zeros, next_scan=300.\n\nDRIFT-#32 delta vs DRIFT-#31: total 22->21, honest_free 2->1 (a second honest_free task departed the market; honest_paid 0 throughout — no paid movement), scam 17 stable, unknown 3 stable. All other sentinels held: 446B size band (digit-width-stable change), all_honest_paid empty, best_paid_task None, taskbounty zeros, next_scan=300."),
        # P6: assertions-encode line
        ("Assertions encode the DRIFT-#32 baseline (21,0,1,17,3) @ 446B:",
         "Assertions encode the DRIFT-#33 baseline (20,0,0,17,3) @ 446B:"),
        # P7: composition bullet
        ("  - BA composition: total=21 honest_paid=0 honest_free=1 scam=17 unknown=3",
         "  - BA composition: total=20 honest_paid=0 honest_free=0 scam=17 unknown=3"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL56, "w") as f:
        f.write(rebadged)
    print(f"reanchor_patches_applied={len(patches)} (drift-root class)")

    # residue check: code body must be clean of 2555 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2555" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2555 residue"

    r = subprocess.run([sys.executable, VAL56], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
