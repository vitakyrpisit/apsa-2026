#!/usr/bin/env python3
"""c2544 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 6th consecutive):
  raw body  = curl -o scan_cycle2544_raw.json (genuine bytes, 446B)
  time_total = 1.779044s (EP14 classification class)
  pre  = 07:40:58.845566420 +08 (epoch 1792971658.845566420)
  post = 07:41:00.632504776 +08 (epoch 1792971660.632504776)
  server start 07:40:58.856 (scanned_at 07:41:00.628 - 1772ms): 10ms skew vs pre — proxy validated (14/11/10/12/12/11/10ms series)
"""
import json
import subprocess
import sys

RAW44 = "/home/z/my-project/scripts/scan_cycle2544_raw.json"
RAW43 = "/home/z/my-project/scripts/scan_cycle2543_raw.json"
VAL43 = "/home/z/my-project/scripts/validate_cycle2543.py"
VAL44 = "/home/z/my-project/scripts/validate_cycle2544.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW44, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n43, n44 = norm(RAW43), norm(RAW44)
    print(f"normalized={len(n44)}-vs-{len(n43)}")
    if n44 != n43:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2543->2544 (sed-equivalent)
    with open(VAL43, "r") as f:
        src = f.read()
    rebadged = src.replace("2543", "2544")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2542.py",
         "rebadged from validate_cycle2543.py"),
        ("(sed 2542->2544, the DRIFT-#31 verification-29 harness)",
         "(sed 2543->2544, the DRIFT-#31 verification-30 harness)"),
        ("c2544 = verification 30\n(c2542 = verification 29;",
         "c2544 = verification 31\n(c2543 = verification 30; c2542 = verification 29;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL44, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2543 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2543" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2543 residue"

    r = subprocess.run([sys.executable, VAL44], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
