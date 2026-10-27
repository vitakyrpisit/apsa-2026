#!/usr/bin/env python3
"""c2555 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 17th consecutive —
MANDATORY ORDER RESTORED: pre-epoch echo captured BEFORE curl):
  raw body  = curl -o scan_cycle2555_raw.json (genuine bytes, 446B)
  time_total = 2.119091s (EP14 classification class)
  pre  = 08:58:05.959860801 +08 (epoch 1792976285.959860801)
  post = 08:58:08.086474051 +08 (epoch 1792976288.086474051)
  server start 08:58:05.971 (scanned_at 08:58:08.082 - 2111ms): 11ms skew
  vs pre — proxy validated 17th consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11ms series)
"""
import json
import subprocess
import sys

RAW55 = "/home/z/my-project/scripts/scan_cycle2555_raw.json"
RAW54 = "/home/z/my-project/scripts/scan_cycle2554_raw.json"
VAL54 = "/home/z/my-project/scripts/validate_cycle2554.py"
VAL55 = "/home/z/my-project/scripts/validate_cycle2555.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW55, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n54, n55 = norm(RAW54), norm(RAW55)
    print(f"normalized={len(n55)}-vs-{len(n54)}")
    if n55 != n54:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2554->2555 (sed-equivalent), then carry-class patches
    with open(VAL54, "r") as f:
        src = f.read()
    rebadged = src.replace("2554", "2555")

    patches = [
        # P1: header carry lineage advance
        ("DRIFT-#32 CARRY: rebadged from validate_cycle2553.py (verification-1 root harness)",
         "DRIFT-#32 CARRY: rebadged from validate_cycle2554.py (verification-2 carry harness)"),
        # P2: sed-line lineage fix (global sed corrupted 2553->2554 into 2553->2555)
        ("(sed 2553->2555, the DRIFT-#32 verification-1 root harness). Baseline",
         "(sed 2554->2555, the DRIFT-#32 verification-2 carry harness). Baseline"),
        # P3: chain head — c2555 = verification 3 with c2554 = verification 2 inserted
        ("(21,0,1,17,3) @ 446B DRIFT-#32 root; c2555 = verification 2\n(c2553 = verification 1, DRIFT-#32 root; c2552 = verification 39, DRIFT-#31 final; c2551 = verification 38;",
         "(21,0,1,17,3) @ 446B DRIFT-#32 root; c2555 = verification 3\n(c2554 = verification 2; c2553 = verification 1, DRIFT-#32 root; c2552 = verification 39, DRIFT-#31 final; c2551 = verification 38;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL55, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2554 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2554" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2554 residue"

    r = subprocess.run([sys.executable, VAL55], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
