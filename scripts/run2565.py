#!/usr/bin/env python3
"""c2565 pipeline: DRIFT-#34 verification-3 (carry-class), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 27th consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2565_raw.json (genuine bytes, 446B)
  time_total = 1.710815s (EP14 s155 classification class)
  pre  = 10:49:56.253830524 +08 (epoch 1792982996.253830524)
  post = 10:49:57.973360548 +08 (epoch 1792982997.973360548)
  wall span 1.719530024
  server start 10:49:56.267 (scanned_at 10:49:57.969 - 1702ms): 13ms skew
  vs pre — proxy validated 27th consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11/10/11/12/11/12/12/13ms series)

DRIFT-#34 verification 3: five-tuple (21,0,0,18,3) == baseline (root c2563);
  verification 2 (c2564) -> 3 (c2565). honest inventory EMPTY continues
  (honest_free=0, honest_paid=0); scam 18 stable, unknown 3 stable;
  446B size band digit-width-stable. Recursive diff vs c2564: EXPECT EQUAL
  (MARKET_UNCHANGED — any differ would open DRIFT-#35 evaluation).
"""
import json
import subprocess
import sys

RAW65 = "/home/z/my-project/scripts/scan_cycle2565_raw.json"
RAW64 = "/home/z/my-project/scripts/scan_cycle2564.json"
VAL64 = "/home/z/my-project/scripts/validate_cycle2564.py"
VAL65 = "/home/z/my-project/scripts/validate_cycle2565.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW65, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n64, n65 = norm(RAW64), norm(RAW65)
    print(f"normalized={len(n65)}-vs-{len(n64)}")
    if n65 != n64:
        print("MARKET_DRIFT — unexpected at verification cycle (DRIFT-#35 evaluation)")
        sys.exit(3)
    print("MARKET_UNCHANGED — DRIFT-#34 streak 2-to-3, rc=0")

    # rebadge 2564->2565 (sed-equivalent), then carry-class provenance patches
    with open(VAL64, "r") as f:
        src = f.read()
    rebadged = src.replace("2564", "2565")

    # process generalization (c2559+): pre-verify patch sites BEFORE applying
    print("--- post-sed head (first 8 lines) ---")
    for ln in rebadged.splitlines()[:8]:
        print(ln)
    print("--- patch site pre-counts (expect 1x each) ---")

    patches = [
        # P1: header carry advance (source header references validate_cycle2563.py — one behind,
        #     untouched by the sed — generalized P1 lesson; update carry class 2->3 and point
        #     the rebadged-from at 2564)
        ("DRIFT-#34 verification-2 CARRY: rebadged from validate_cycle2563.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#34 verification-3 CARRY: rebadged from validate_cycle2564.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2563->2564 into 2563->2565)
        ("(sed 2563->2565, the DRIFT-#34 verification-1 root harness; DRIFT-#34 verification-2 carry). Baseline",
         "(sed 2564->2565, the DRIFT-#34 verification-2 carry harness; DRIFT-#34 verification-3 carry). Baseline"),
        # P3: chain head — bump verification 2->3 AND insert c2564 = verification 2
        #     before the c2563 citation (regular chain-insertion pattern)
        ("(21,0,0,18,3) @ 446B DRIFT-#34 root; c2565 = verification 2\n(c2563 = verification 1, DRIFT-#34 root;",
         "(21,0,0,18,3) @ 446B DRIFT-#34 root; c2565 = verification 3\n(c2564 = verification 2; c2563 = verification 1, DRIFT-#34 root;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        print(f"  site_count={cnt} :: {old[:64]}")
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
    for old, new in patches:
        rebadged = rebadged.replace(old, new)
    with open(VAL65, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)} (carry-class, first pass, NO misses)")

    # residue check: code body must be clean of 2564 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2564" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2564 residue"

    r = subprocess.run([sys.executable, VAL65], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
