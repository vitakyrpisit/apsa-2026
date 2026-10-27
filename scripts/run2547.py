#!/usr/bin/env python3
"""c2547 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 9th consecutive):
  raw body  = curl -o scan_cycle2547_raw.json (genuine bytes, 446B)
  time_total = 1.699192s (EP14 classification class)
  pre  = 07:56:19.291536669 +08 (epoch 1792972579.291536669)
  post = 07:56:20.998273225 +08 (epoch 1792972580.998273225)
  server start 07:56:19.302 (scanned_at 07:56:20.994 - 1692ms): 10ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11/10ms series)
"""
import json
import subprocess
import sys

RAW47 = "/home/z/my-project/scripts/scan_cycle2547_raw.json"
RAW46 = "/home/z/my-project/scripts/scan_cycle2546_raw.json"
VAL46 = "/home/z/my-project/scripts/validate_cycle2546.py"
VAL47 = "/home/z/my-project/scripts/validate_cycle2547.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW47, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n46, n47 = norm(RAW46), norm(RAW47)
    print(f"normalized={len(n47)}-vs-{len(n46)}")
    if n47 != n46:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2546->2547 (sed-equivalent)
    with open(VAL46, "r") as f:
        src = f.read()
    rebadged = src.replace("2546", "2547")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2545.py",
         "rebadged from validate_cycle2546.py"),
        ("(sed 2545->2547, the DRIFT-#31 verification-32 harness)",
         "(sed 2546->2547, the DRIFT-#31 verification-33 harness)"),
        ("c2547 = verification 33\n(c2545 = verification 32;",
         "c2547 = verification 34\n(c2546 = verification 33; c2545 = verification 32;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL47, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2546 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2546" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2546 residue"

    r = subprocess.run([sys.executable, VAL47], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
