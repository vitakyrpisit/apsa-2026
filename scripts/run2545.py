#!/usr/bin/env python3
"""c2545 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 7th consecutive):
  raw body  = curl -o scan_cycle2545_raw.json (genuine bytes, 446B)
  time_total = 1.926542s (EP14 classification class)
  pre  = 07:49:13.461884685 +08 (epoch 1792972153.461884685)
  post = 07:49:15.395689221 +08 (epoch 1792972155.395689221)
  server start 07:49:13.472 (scanned_at 07:49:15.392 - 1920ms): 10ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10ms series)
"""
import json
import subprocess
import sys

RAW45 = "/home/z/my-project/scripts/scan_cycle2545_raw.json"
RAW44 = "/home/z/my-project/scripts/scan_cycle2544_raw.json"
VAL44 = "/home/z/my-project/scripts/validate_cycle2544.py"
VAL45 = "/home/z/my-project/scripts/validate_cycle2545.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW45, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n44, n45 = norm(RAW44), norm(RAW45)
    print(f"normalized={len(n45)}-vs-{len(n44)}")
    if n45 != n44:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2544->2545 (sed-equivalent)
    with open(VAL44, "r") as f:
        src = f.read()
    rebadged = src.replace("2544", "2545")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2543.py",
         "rebadged from validate_cycle2544.py"),
        ("(sed 2543->2545, the DRIFT-#31 verification-30 harness)",
         "(sed 2544->2545, the DRIFT-#31 verification-31 harness)"),
        ("c2545 = verification 31\n(c2543 = verification 30;",
         "c2545 = verification 32\n(c2544 = verification 31; c2543 = verification 30;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL45, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2544 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2544" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2544 residue"

    r = subprocess.run([sys.executable, VAL45], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
