#!/usr/bin/env python3
"""c2540 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 2nd consecutive):
  raw body  = curl -o scan_cycle2540_raw.json (genuine bytes, 446B)
  time_total = 1.953182s (EP14 classification class)
  pre  = 07:20:16.981770088 +08 (epoch 1792970416.981033465)
  post = 07:20:18.942897507 +08 (epoch 1792970418.942897507)
  server start 07:20:16.992 (scanned_at 07:20:18.938 - 1946ms): 10ms skew vs pre — proxy validated (14/11/10ms series)
"""
import json
import subprocess
import sys

RAW40 = "/home/z/my-project/scripts/scan_cycle2540_raw.json"
RAW39 = "/home/z/my-project/scripts/scan_cycle2539_raw.json"
VAL39 = "/home/z/my-project/scripts/validate_cycle2539.py"
VAL40 = "/home/z/my-project/scripts/validate_cycle2540.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW40, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n39, n40 = norm(RAW39), norm(RAW40)
    print(f"normalized={len(n40)}-vs-{len(n39)}")
    if n40 != n39:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2539->2540 (sed-equivalent)
    with open(VAL39, "r") as f:
        src = f.read()
    rebadged = src.replace("2539", "2540")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2538.py",
         "rebadged from validate_cycle2539.py"),
        ("(sed 2538->2540, the DRIFT-#31 verification-25 harness)",
         "(sed 2539->2540, the DRIFT-#31 verification-26 harness)"),
        ("c2540 = verification 26\n(c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;",
         "c2540 = verification 27\n(c2539 = verification 26; c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL40, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2539 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2539" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2539 residue"

    r = subprocess.run([sys.executable, VAL40], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
