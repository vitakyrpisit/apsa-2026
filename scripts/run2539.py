#!/usr/bin/env python3
"""c2539 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (client instrumentation restored per c2538 priority):
  raw body  = curl -o scan_cycle2539_raw.json (genuine bytes, 446B)
  time_total = 2.018130s (EP14 classification class)
  pre  = 07:17:21.714802991 +08 (epoch 1792970241.714802991)
  post = 07:17:23.741312332 +08 (epoch 1792970243.741312332)
  server start 07:17:21.726 (scanned_at 07:17:23.736 - 2010ms): 11ms skew vs pre — proxy validated
"""
import json
import subprocess
import sys

RAW39 = "/home/z/my-project/scripts/scan_cycle2539_raw.json"
RAW38 = "/home/z/my-project/scripts/scan_cycle2538_raw.json"
VAL38 = "/home/z/my-project/scripts/validate_cycle2538.py"
VAL39 = "/home/z/my-project/scripts/validate_cycle2539.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW39, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n38, n39 = norm(RAW38), norm(RAW39)
    print(f"normalized={len(n39)}-vs-{len(n38)}")
    if n39 != n38:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2538->2539 (sed-equivalent)
    with open(VAL38, "r") as f:
        src = f.read()
    rebadged = src.replace("2538", "2539")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2537.py",
         "rebadged from validate_cycle2538.py"),
        ("(sed 2537->2539, the DRIFT-#31 verification-24 harness)",
         "(sed 2538->2539, the DRIFT-#31 verification-25 harness)"),
        ("c2539 = verification 25\n(c2537 = verification 24; c2536 = verification 23;",
         "c2539 = verification 26\n(c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL39, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2538 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2538" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2538 residue"

    r = subprocess.run([sys.executable, VAL39], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
