#!/usr/bin/env python3
"""c2546 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 8th consecutive):
  raw body  = curl -o scan_cycle2546_raw.json (genuine bytes, 446B)
  time_total = 1.817384s (EP14 classification class)
  pre  = 07:53:00.073505747 +08 (epoch 1792972380.073505747)
  post = 07:53:01.898423622 +08 (epoch 1792972381.898423622)
  server start 07:53:00.085 (scanned_at 07:53:01.894 - 1809ms): 11ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11ms series)
"""
import json
import subprocess
import sys

RAW46 = "/home/z/my-project/scripts/scan_cycle2546_raw.json"
RAW45 = "/home/z/my-project/scripts/scan_cycle2545_raw.json"
VAL45 = "/home/z/my-project/scripts/validate_cycle2545.py"
VAL46 = "/home/z/my-project/scripts/validate_cycle2546.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW46, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n45, n46 = norm(RAW45), norm(RAW46)
    print(f"normalized={len(n46)}-vs-{len(n45)}")
    if n46 != n45:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2545->2546 (sed-equivalent)
    with open(VAL45, "r") as f:
        src = f.read()
    rebadged = src.replace("2545", "2546")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2544.py",
         "rebadged from validate_cycle2545.py"),
        ("(sed 2544->2546, the DRIFT-#31 verification-31 harness)",
         "(sed 2545->2546, the DRIFT-#31 verification-32 harness)"),
        ("c2546 = verification 32\n(c2544 = verification 31;",
         "c2546 = verification 33\n(c2545 = verification 32; c2544 = verification 31;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL46, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2545 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2545" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2545 residue"

    r = subprocess.run([sys.executable, VAL46], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
