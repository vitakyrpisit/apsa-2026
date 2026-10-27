#!/usr/bin/env python3
"""c2560 pipeline: DRIFT-#33 verification-5 (carry-class), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 22nd consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2560_raw.json (genuine bytes, 446B)
  time_total = 1.693737s (EP14 classification class)
  pre  = 09:46:27.071060623 +08 (epoch 1792979187.071060623)
  post = 09:46:28.772441648 +08 (epoch 1792979188.772441648)
  server start 09:46:27.082 (scanned_at 09:46:28.768 - 1686ms): 11ms skew
  vs pre — proxy validated 22nd consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11/10/11ms series)

DRIFT-#33 verification 5: five-tuple (20,0,0,17,3) == baseline (root c2556);
  verification 4 (c2559) -> 5 (c2560). honest inventory EMPTY continues
  (honest_free=0, honest_paid=0); scam 17 stable, unknown 3 stable;
  446B size band digit-width-stable. Recursive diff vs c2559: EXPECT EQUAL
  (MARKET_UNCHANGED — any differ would open DRIFT-#34 evaluation).
"""
import json
import subprocess
import sys

RAW60 = "/home/z/my-project/scripts/scan_cycle2560_raw.json"
RAW59 = "/home/z/my-project/scripts/scan_cycle2559.json"
VAL59 = "/home/z/my-project/scripts/validate_cycle2559.py"
VAL60 = "/home/z/my-project/scripts/validate_cycle2560.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW60, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n60, n59 = norm(RAW60), norm(RAW59)
    print(f"normalized={len(n60)}-vs-{len(n59)}")
    if n60 != n59:
        print("MARKET_DRIFT — unexpected at verification cycle (DRIFT-#34 evaluation)")
        sys.exit(3)
    print("MARKET_UNCHANGED — DRIFT-#33 streak 4-to-5, rc=0")

    # rebadge 2559->2560 (sed-equivalent), then carry-class provenance patches
    with open(VAL59, "r") as f:
        src = f.read()
    rebadged = src.replace("2559", "2560")

    patches = [
        # P1: header carry advance (source header references validate_cycle2558.py — one behind,
        #     untouched by the sed — generalized P1 lesson; update carry class 4->5 and point
        #     the rebadged-from at 2559)
        ("DRIFT-#33 verification-4 CARRY: rebadged from validate_cycle2558.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#33 verification-5 CARRY: rebadged from validate_cycle2559.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2558->2559 into 2558->2560)
        ("(sed 2558->2560, the DRIFT-#33 verification-3 harness; DRIFT-#33 verification-4 carry). Baseline",
         "(sed 2559->2560, the DRIFT-#33 verification-4 harness; DRIFT-#33 verification-5 carry). Baseline"),
        # P3: chain head — bump verification 4->5 AND insert c2559 = verification 4
        #     before the c2558 citation (regular chain-insertion pattern)
        ("c2560 = verification 4\n(c2558 = verification 3;",
         "c2560 = verification 5\n(c2559 = verification 4; c2558 = verification 3;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL60, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)} (carry-class, first pass, NO misses)")

    # residue check: code body must be clean of 2559 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2559" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2559 residue"

    r = subprocess.run([sys.executable, VAL60], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
