#!/usr/bin/env python3
"""c2553 pipeline: drift-root RE-ANCHOR (DRIFT-#32), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 15th consecutive):
  raw body  = curl -o scan_cycle2553_raw.json (genuine bytes, 446B)
  time_total = 1.878420s (EP14 classification class)
  pre  = 08:42:25.984376688 +08 (epoch 1792975345.984376688)
  post = 08:42:27.870518876 +08 (epoch 1792975347.870518876)
  server start 08:42:25.995 (scanned_at 08:42:27.866 - 1871ms): 11ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11ms series)

DRIFT ROOT: five-tuple (21,0,1,17,3) != DRIFT-#31 baseline (22,0,2,17,3)
  -> DRIFT-#31 closes at 39-fold (root c2514); DRIFT-#32 root c2553.
  Delta: total 22->21, honest_free 2->1, honest_paid 0 throughout,
  scam 17 stable, unknown 3 stable; 446B size band digit-width-stable.
  Payload is aggregate-only: departed-task identity not exposed.
"""
import json
import subprocess
import sys

RAW53 = "/home/z/my-project/scripts/scan_cycle2553_raw.json"
RAW52 = "/home/z/my-project/scripts/scan_cycle2552_raw.json"
VAL52 = "/home/z/my-project/scripts/validate_cycle2552.py"
VAL53 = "/home/z/my-project/scripts/validate_cycle2553.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW53, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n52, n53 = norm(RAW52), norm(RAW53)
    print(f"normalized={len(n53)}-vs-{len(n52)}")
    if n53 == n52:
        print("MARKET_UNCHANGED — unexpected at claimed drift root")
        sys.exit(3)
    print("MARKET_DRIFT_CONFIRMED — DRIFT-#31 closes at 39-fold; DRIFT-#32 root c2553")

    # rebadge 2552->2553 (sed-equivalent), then drift-root RE-ANCHOR patches
    with open(VAL52, "r") as f:
        src = f.read()
    rebadged = src.replace("2552", "2553")

    patches = [
        # P1: header carry -> re-anchor
        ("DRIFT-#31 BASELINE CARRY: rebadged from validate_cycle2551.py",
         "DRIFT-#32 RE-ANCHOR: rebadged from validate_cycle2552.py (drift-root precedent c2454/c2514)"),
        # P2: sed-line lineage fix (global sed had corrupted 2551->2553)
        ("(sed 2551->2553, the DRIFT-#31 verification-38 harness). Baseline",
         "(sed 2552->2553, the DRIFT-#31 verification-39 harness; DRIFT-#32 root re-anchor). Baseline"),
        # P3: chain head — c2553 = verification 1 with c2552 final-39 inserted
        ("(22,0,2,17,3) @ 446B carried unchanged; c2553 = verification 39\n(c2551 = verification 38;",
         "(21,0,1,17,3) @ 446B DRIFT-#32 root; c2553 = verification 1\n(c2552 = verification 39, DRIFT-#31 final; c2551 = verification 38;"),
        # P4: baseline constants 22/2 -> 21/1
        ('BASELINE_COMP = {"total": 22, "honest_paid": 0, "honest_free": 2, "scam": 17, "unknown": 3}',
         'BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 1, "scam": 17, "unknown": 3}'),
        # P5: DRIFT-#32 delta paragraph inserted ahead of the DRIFT-#31 history
        ("DRIFT-#31 delta vs DRIFT-#30: total 23->22, honest_free 3->2 (one",
         "DRIFT-#32 delta vs DRIFT-#31: total 22->21, honest_free 2->1 (a second honest_free task departed the market; honest_paid 0 throughout — no paid movement), scam 17 stable, unknown 3 stable. All other sentinels held: 446B size band (digit-width-stable change), all_honest_paid empty, best_paid_task None, taskbounty zeros, next_scan=300.\n\nDRIFT-#31 delta vs DRIFT-#30: total 23->22, honest_free 3->2 (one"),
        # P6: assertions-encode line
        ("Assertions encode the DRIFT-#31 baseline (22,0,2,17,3) @ 446B:",
         "Assertions encode the DRIFT-#32 baseline (21,0,1,17,3) @ 446B:"),
        # P7: composition bullet
        ("  - BA composition: total=22 honest_paid=0 honest_free=2 scam=17 unknown=3",
         "  - BA composition: total=21 honest_paid=0 honest_free=1 scam=17 unknown=3"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL53, "w") as f:
        f.write(rebadged)
    print(f"reanchor_patches_applied={len(patches)} (drift-root class)")

    # residue check: code body must be clean of 2552 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2552" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2552 residue"

    r = subprocess.run([sys.executable, VAL53], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
