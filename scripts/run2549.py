#!/usr/bin/env python3
"""c2549 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 11th consecutive):
  raw body  = curl -o scan_cycle2549_raw.json (genuine bytes, 446B)
  time_total = 1.774493s (EP14 classification class)
  pre  = 08:11:40.368207676 +08 (epoch 1792973500.368207676)
  post = 08:11:42.150520545 +08 (epoch 1792973502.150520545)
  server start 08:11:40.379 (scanned_at 08:11:42.146 - 1767ms): 11ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11/10/11/11ms series)
"""
import json
import subprocess
import sys

RAW49 = "/home/z/my-project/scripts/scan_cycle2549_raw.json"
RAW48 = "/home/z/my-project/scripts/scan_cycle2548_raw.json"
VAL48 = "/home/z/my-project/scripts/validate_cycle2548.py"
VAL49 = "/home/z/my-project/scripts/validate_cycle2549.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW49, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n48, n49 = norm(RAW48), norm(RAW49)
    print(f"normalized={len(n49)}-vs-{len(n48)}")
    if n49 != n48:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2548->2549 (sed-equivalent)
    with open(VAL48, "r") as f:
        src = f.read()
    rebadged = src.replace("2548", "2549")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2547.py",
         "rebadged from validate_cycle2548.py"),
        ("(sed 2547->2549, the DRIFT-#31 verification-34 harness)",
         "(sed 2548->2549, the DRIFT-#31 verification-35 harness)"),
        ("c2549 = verification 35\n(c2547 = verification 34;",
         "c2549 = verification 36\n(c2548 = verification 35; c2547 = verification 34;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL49, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2548 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2548" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2548 residue"

    r = subprocess.run([sys.executable, VAL49], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
