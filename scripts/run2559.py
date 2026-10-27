#!/usr/bin/env python3
"""c2559 pipeline: DRIFT-#33 verification-4 (carry-class), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 21st consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2559_raw.json (genuine bytes, 446B)
  time_total = 1.917850s (EP14 classification class)
  pre  = 09:41:18.418794284 +08 (epoch 1792978878.418794284)
  post = 09:41:20.344230151 +08 (epoch 1792978880.344230151)
  server start 09:41:18.429 (scanned_at 09:41:20.339 - 1910ms): 10ms skew
  vs pre — proxy validated 21st consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11/10ms series)

DRIFT-#33 verification 4: five-tuple (20,0,0,17,3) == baseline (root c2556);
  verification 3 (c2558) -> 4 (c2559). honest inventory EMPTY continues
  (honest_free=0, honest_paid=0); scam 17 stable, unknown 3 stable;
  446B size band digit-width-stable. Recursive diff vs c2558: EXPECT EQUAL
  (MARKET_UNCHANGED — any differ would open DRIFT-#34 evaluation).
"""
import json
import subprocess
import sys

RAW59 = "/home/z/my-project/scripts/scan_cycle2559_raw.json"
RAW58 = "/home/z/my-project/scripts/scan_cycle2558.json"
VAL58 = "/home/z/my-project/scripts/validate_cycle2558.py"
VAL59 = "/home/z/my-project/scripts/validate_cycle2559.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW59, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n59, n58 = norm(RAW59), norm(RAW58)
    print(f"normalized={len(n59)}-vs-{len(n58)}")
    if n59 != n58:
        print("MARKET_DRIFT — unexpected at verification cycle (DRIFT-#34 evaluation)")
        sys.exit(3)
    print("MARKET_UNCHANGED — DRIFT-#33 streak 3-to-4, rc=0")

    # rebadge 2558->2559 (sed-equivalent), then carry-class provenance patches
    with open(VAL58, "r") as f:
        src = f.read()
    rebadged = src.replace("2558", "2559")

    patches = [
        # P1: header carry advance (source header references validate_cycle2557.py — the file IT
        #     was rebadged from, which the sed does NOT touch — the c2558 P1 lesson; update carry
        #     class 3->4 and point the rebadged-from at 2558)
        ("DRIFT-#33 verification-3 CARRY: rebadged from validate_cycle2557.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#33 verification-4 CARRY: rebadged from validate_cycle2558.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2557->2558 into 2557->2559)
        ("(sed 2557->2559, the DRIFT-#33 verification-2 harness; DRIFT-#33 verification-3 carry). Baseline",
         "(sed 2558->2559, the DRIFT-#33 verification-3 harness; DRIFT-#33 verification-4 carry). Baseline"),
        # P3: chain head — bump verification 3->4 AND insert c2558 = verification 3
        #     before the c2557 citation (regular chain-insertion pattern per the c2558 forecast note)
        ("c2559 = verification 3\n(c2557 = verification 2;",
         "c2559 = verification 4\n(c2558 = verification 3; c2557 = verification 2;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL59, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)} (carry-class, first pass, NO misses)")

    # residue check: code body must be clean of 2558 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2558" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2558 residue"

    r = subprocess.run([sys.executable, VAL59], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
