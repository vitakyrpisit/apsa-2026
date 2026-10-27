#!/usr/bin/env python3
"""c2542 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 4th consecutive):
  raw body  = curl -o scan_cycle2542_raw.json (genuine bytes, 446B)
  time_total = 1.700382s (EP14 classification class)
  pre  = 07:29:38.115729532 +08 (epoch 1792970978.115729532)
  post = 07:29:39.824354353 +08 (epoch 1792970979.824354353)
  server start 07:29:38.128 (scanned_at 07:29:39.820 - 1692ms): 12ms skew vs pre — proxy validated (14/11/10/12/12ms series)
"""
import json
import subprocess
import sys

RAW42 = "/home/z/my-project/scripts/scan_cycle2542_raw.json"
RAW41 = "/home/z/my-project/scripts/scan_cycle2541_raw.json"
VAL41 = "/home/z/my-project/scripts/validate_cycle2541.py"
VAL42 = "/home/z/my-project/scripts/validate_cycle2542.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW42, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n41, n42 = norm(RAW41), norm(RAW42)
    print(f"normalized={len(n42)}-vs-{len(n41)}")
    if n42 != n41:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2541->2542 (sed-equivalent)
    with open(VAL41, "r") as f:
        src = f.read()
    rebadged = src.replace("2541", "2542")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2540.py",
         "rebadged from validate_cycle2541.py"),
        ("(sed 2540->2542, the DRIFT-#31 verification-27 harness)",
         "(sed 2541->2542, the DRIFT-#31 verification-28 harness)"),
        ("c2542 = verification 28\n(c2540 = verification 27; c2539 = verification 26; c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;",
         "c2542 = verification 29\n(c2541 = verification 28; c2540 = verification 27; c2539 = verification 26; c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL42, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2541 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2541" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2541 residue"

    r = subprocess.run([sys.executable, VAL42], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
