#!/usr/bin/env python3
"""c2561 pipeline: DRIFT-#33 verification-6 (carry-class), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 23rd consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2561_raw.json (genuine bytes, 446B)
  time_total = 2.320963s (EP14 classification class)
  pre  = 09:50:57.443313095 +08 (epoch 1792979457.443313095)
  post = 09:50:59.778914514 +08 (epoch 1792979459.778914514)
  server start 09:50:57.455 (scanned_at 09:50:59.744 - 2289ms): 12ms skew
  vs pre — proxy validated 23rd consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11/10/11/12ms series)

DRIFT-#33 verification 6: five-tuple (20,0,0,17,3) == baseline (root c2556);
  verification 5 (c2560) -> 6 (c2561). honest inventory EMPTY continues
  (honest_free=0, honest_paid=0); scam 17 stable, unknown 3 stable;
  446B size band digit-width-stable. Recursive diff vs c2560: EXPECT EQUAL
  (MARKET_UNCHANGED — any differ would open DRIFT-#34 evaluation).
"""
import json
import subprocess
import sys

RAW61 = "/home/z/my-project/scripts/scan_cycle2561_raw.json"
RAW60 = "/home/z/my-project/scripts/scan_cycle2560.json"
VAL60 = "/home/z/my-project/scripts/validate_cycle2560.py"
VAL61 = "/home/z/my-project/scripts/validate_cycle2561.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW61, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n61, n60 = norm(RAW61), norm(RAW60)
    print(f"normalized={len(n61)}-vs-{len(n60)}")
    if n61 != n60:
        print("MARKET_DRIFT — unexpected at verification cycle (DRIFT-#34 evaluation)")
        sys.exit(3)
    print("MARKET_UNCHANGED — DRIFT-#33 streak 5-to-6, rc=0")

    # rebadge 2560->2561 (sed-equivalent), then carry-class provenance patches
    with open(VAL60, "r") as f:
        src = f.read()
    rebadged = src.replace("2560", "2561")

    patches = [
        # P1: header carry advance (source header references validate_cycle2559.py — one behind,
        #     untouched by the sed — generalized P1 lesson; update carry class 5->6 and point
        #     the rebadged-from at 2560)
        ("DRIFT-#33 verification-5 CARRY: rebadged from validate_cycle2559.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#33 verification-6 CARRY: rebadged from validate_cycle2560.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2559->2560 into 2559->2561)
        ("(sed 2559->2561, the DRIFT-#33 verification-4 harness; DRIFT-#33 verification-5 carry). Baseline",
         "(sed 2560->2561, the DRIFT-#33 verification-5 harness; DRIFT-#33 verification-6 carry). Baseline"),
        # P3: chain head — bump verification 5->6 AND insert c2560 = verification 5
        #     before the c2559 citation (regular chain-insertion pattern)
        ("c2561 = verification 5\n(c2559 = verification 4;",
         "c2561 = verification 6\n(c2560 = verification 5; c2559 = verification 4;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL61, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)} (carry-class, first pass, NO misses)")

    # residue check: code body must be clean of 2560 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2560" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2560 residue"

    r = subprocess.run([sys.executable, VAL61], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
