#!/usr/bin/env python3
"""c2552 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 14th consecutive):
  raw body  = curl -o scan_cycle2552_raw.json (genuine bytes, 446B)
  time_total = 2.028297s (EP14 classification class)
  pre  = 08:32:26.953063132 +08 (epoch 1792974746.953063132)
  post = 08:32:28.990802089 +08 (epoch 1792974748.990802089)
  server start 08:32:26.966 (scanned_at 08:32:28.985 - 2019ms): 13ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13ms series)
"""
import json
import subprocess
import sys

RAW52 = "/home/z/my-project/scripts/scan_cycle2552_raw.json"
RAW51 = "/home/z/my-project/scripts/scan_cycle2551_raw.json"
VAL51 = "/home/z/my-project/scripts/validate_cycle2551.py"
VAL52 = "/home/z/my-project/scripts/validate_cycle2552.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW52, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n51, n52 = norm(RAW51), norm(RAW52)
    print(f"normalized={len(n52)}-vs-{len(n51)}")
    if n52 != n51:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2551->2552 (sed-equivalent)
    with open(VAL51, "r") as f:
        src = f.read()
    rebadged = src.replace("2551", "2552")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2550.py",
         "rebadged from validate_cycle2551.py"),
        ("(sed 2550->2552, the DRIFT-#31 verification-37 harness)",
         "(sed 2551->2552, the DRIFT-#31 verification-38 harness)"),
        ("c2552 = verification 38\n(c2550 = verification 37;",
         "c2552 = verification 39\n(c2551 = verification 38; c2550 = verification 37;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL52, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2551 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2551" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2551 residue"

    r = subprocess.run([sys.executable, VAL52], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
