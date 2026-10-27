#!/usr/bin/env python3
"""c2554 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 16th consecutive — WITH
INSTRUMENTATION SLIP: pre-curl epoch NOT captured (echo ordering error);
partial recovery: derived pre = POST(1792976011.608021767) - time_total
(2.018518) = 1792976009.589503767, cross-validated by server-start
00:53:29.563 and by LAG identity exec-to-exec 663.605127079 — DERIVED
class, flagged per the c2538 INSTRUMENTATION PRIORITY precedent):
  raw body  = curl -o scan_cycle2554_raw.json (genuine bytes, 446B)
  time_total = 2.018518s (EP14 classification class)
  pre  = DERIVED 1792976009.589503767 (~08:53:29.589 +08)
  post = 1792976011.608021767 (~08:53:31.608 +08)
  server start 08:53:29.563 (scanned_at 08:53:31.574 - 2011ms) — skew
  cross-check UNRESOLVABLE this cycle (no captured pre)
"""
import json
import subprocess
import sys

RAW54 = "/home/z/my-project/scripts/scan_cycle2554_raw.json"
RAW53 = "/home/z/my-project/scripts/scan_cycle2553_raw.json"
VAL53 = "/home/z/my-project/scripts/validate_cycle2553.py"
VAL54 = "/home/z/my-project/scripts/validate_cycle2554.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW54, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n53, n54 = norm(RAW53), norm(RAW54)
    print(f"normalized={len(n54)}-vs-{len(n53)}")
    if n54 != n53:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2553->2554 (sed-equivalent), then carry-class patches
    with open(VAL53, "r") as f:
        src = f.read()
    rebadged = src.replace("2553", "2554")

    patches = [
        # P1: header re-anchor -> carry
        ("DRIFT-#32 RE-ANCHOR: rebadged from validate_cycle2552.py (drift-root precedent c2454/c2514)",
         "DRIFT-#32 CARRY: rebadged from validate_cycle2553.py (verification-1 root harness)"),
        # P2: sed-line lineage fix (global sed corrupted 2552->2553 into 2552->2554)
        ("(sed 2552->2554, the DRIFT-#31 verification-39 harness; DRIFT-#32 root re-anchor). Baseline",
         "(sed 2553->2554, the DRIFT-#32 verification-1 root harness). Baseline"),
        # P3: chain head — c2554 = verification 2 with c2553 = verification 1 inserted
        ("(21,0,1,17,3) @ 446B DRIFT-#32 root; c2554 = verification 1\n(c2552 = verification 39, DRIFT-#31 final; c2551 = verification 38;",
         "(21,0,1,17,3) @ 446B DRIFT-#32 root; c2554 = verification 2\n(c2553 = verification 1, DRIFT-#32 root; c2552 = verification 39, DRIFT-#31 final; c2551 = verification 38;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL54, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2553 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2553" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2553 residue"

    r = subprocess.run([sys.executable, VAL54], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
