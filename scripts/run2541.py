#!/usr/bin/env python3
"""c2541 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 3rd consecutive):
  raw body  = curl -o scan_cycle2541_raw.json (genuine bytes, 446B)
  time_total = 2.077869s (EP14 classification class)
  pre  = 07:24:38.539842262 +08 (epoch 1792970678.539842262)
  post = 07:24:40.625866831 +08 (epoch 1792970680.625866831)
  server start 07:24:38.552 (scanned_at 07:24:40.622 - 2070ms): 12ms skew vs pre — proxy validated (14/11/10/12ms series)
"""
import json
import subprocess
import sys

RAW41 = "/home/z/my-project/scripts/scan_cycle2541_raw.json"
RAW40 = "/home/z/my-project/scripts/scan_cycle2540_raw.json"
VAL40 = "/home/z/my-project/scripts/validate_cycle2540.py"
VAL41 = "/home/z/my-project/scripts/validate_cycle2541.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW41, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n40, n41 = norm(RAW40), norm(RAW41)
    print(f"normalized={len(n41)}-vs-{len(n40)}")
    if n41 != n40:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2540->2541 (sed-equivalent)
    with open(VAL40, "r") as f:
        src = f.read()
    rebadged = src.replace("2540", "2541")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2539.py",
         "rebadged from validate_cycle2540.py"),
        ("(sed 2539->2541, the DRIFT-#31 verification-26 harness)",
         "(sed 2540->2541, the DRIFT-#31 verification-27 harness)"),
        ("c2541 = verification 27\n(c2539 = verification 26; c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;",
         "c2541 = verification 28\n(c2540 = verification 27; c2539 = verification 26; c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL41, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2540 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2540" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2540 residue"

    r = subprocess.run([sys.executable, VAL41], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
