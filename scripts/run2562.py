#!/usr/bin/env python3
"""c2562 pipeline: DRIFT-#33 verification-7 (carry-class), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 24th consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2562_raw.json (genuine bytes, 446B)
  time_total = 1.706945s (EP14 classification class)
  pre  = 10:05:31.503659941 +08 (epoch 1792980331.503659941)
  post = 10:05:33.220949036 +08 (epoch 1792980333.220949036)
  server start 10:05:31.515 (scanned_at 10:05:33.215 - 1700ms): 11ms skew
  vs pre — proxy validated 24th consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11/10/11/12/11ms series)

DRIFT-#33 verification 7: five-tuple (20,0,0,17,3) == baseline (root c2556);
  verification 6 (c2561) -> 7 (c2562). honest inventory EMPTY continues
  (honest_free=0, honest_paid=0); scam 17 stable, unknown 3 stable;
  446B size band digit-width-stable. Recursive diff vs c2561: EXPECT EQUAL
  (MARKET_UNCHANGED — any differ would open DRIFT-#34 evaluation).
"""
import json
import subprocess
import sys

RAW62 = "/home/z/my-project/scripts/scan_cycle2562_raw.json"
RAW61 = "/home/z/my-project/scripts/scan_cycle2561.json"
VAL61 = "/home/z/my-project/scripts/validate_cycle2561.py"
VAL62 = "/home/z/my-project/scripts/validate_cycle2562.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW62, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n62, n61 = norm(RAW62), norm(RAW61)
    print(f"normalized={len(n62)}-vs-{len(n61)}")
    if n62 != n61:
        print("MARKET_DRIFT — unexpected at verification cycle (DRIFT-#34 evaluation)")
        sys.exit(3)
    print("MARKET_UNCHANGED — DRIFT-#33 streak 6-to-7, rc=0")

    # rebadge 2561->2562 (sed-equivalent), then carry-class provenance patches
    with open(VAL61, "r") as f:
        src = f.read()
    rebadged = src.replace("2561", "2562")

    patches = [
        # P1: header carry advance (source header references validate_cycle2560.py — one behind,
        #     untouched by the sed — generalized P1 lesson; update carry class 6->7 and point
        #     the rebadged-from at 2561)
        ("DRIFT-#33 verification-6 CARRY: rebadged from validate_cycle2560.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#33 verification-7 CARRY: rebadged from validate_cycle2561.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2560->2561 into 2560->2562)
        ("(sed 2560->2562, the DRIFT-#33 verification-5 harness; DRIFT-#33 verification-6 carry). Baseline",
         "(sed 2561->2562, the DRIFT-#33 verification-6 harness; DRIFT-#33 verification-7 carry). Baseline"),
        # P3: chain head — bump verification 6->7 AND insert c2561 = verification 6
        #     before the c2560 citation (regular chain-insertion pattern)
        ("c2562 = verification 6\n(c2560 = verification 5;",
         "c2562 = verification 7\n(c2561 = verification 6; c2560 = verification 5;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL62, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)} (carry-class, first pass, NO misses)")

    # residue check: code body must be clean of 2561 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2561" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2561 residue"

    r = subprocess.run([sys.executable, VAL62], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
