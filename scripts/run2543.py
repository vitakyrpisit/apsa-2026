#!/usr/bin/env python3
"""c2543 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 5th consecutive):
  raw body  = curl -o scan_cycle2543_raw.json (genuine bytes, 446B)
  time_total = 1.748671s (EP14 classification class)
  pre  = 07:34:37.547843496 +08 (epoch 1792971277.547843496)
  post = 07:34:39.305062444 +08 (epoch 1792971279.305062444)
  server start 07:34:37.559 (scanned_at 07:34:39.300 - 1741ms): 11ms skew vs pre — proxy validated (14/11/10/12/12/11ms series)
"""
import json
import subprocess
import sys

RAW43 = "/home/z/my-project/scripts/scan_cycle2543_raw.json"
RAW42 = "/home/z/my-project/scripts/scan_cycle2542_raw.json"
VAL42 = "/home/z/my-project/scripts/validate_cycle2542.py"
VAL43 = "/home/z/my-project/scripts/validate_cycle2543.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW43, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n42, n43 = norm(RAW42), norm(RAW43)
    print(f"normalized={len(n43)}-vs-{len(n42)}")
    if n43 != n42:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2542->2543 (sed-equivalent)
    with open(VAL42, "r") as f:
        src = f.read()
    rebadged = src.replace("2542", "2543")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2541.py",
         "rebadged from validate_cycle2542.py"),
        ("(sed 2541->2543, the DRIFT-#31 verification-28 harness)",
         "(sed 2542->2543, the DRIFT-#31 verification-29 harness)"),
        ("c2543 = verification 29\n(c2541 = verification 28; c2540 = verification 27; c2539 = verification 26; c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;",
         "c2543 = verification 30\n(c2542 = verification 29; c2541 = verification 28; c2540 = verification 27; c2539 = verification 26; c2538 = verification 25; c2537 = verification 24; c2536 = verification 23;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL43, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2542 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2542" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2542 residue"

    r = subprocess.run([sys.executable, VAL43], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
