#!/usr/bin/env python3
"""c2548 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 10th consecutive):
  raw body  = curl -o scan_cycle2548_raw.json (genuine bytes, 446B)
  time_total = 1.876524s (EP14 classification class)
  pre  = 07:59:44.859214642 +08 (epoch 1792972784.859214642)
  post = 07:59:46.743346514 +08 (epoch 1792972786.743346514)
  server start 07:59:44.870 (scanned_at 07:59:46.739 - 1869ms): 11ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11/10/11ms series)
"""
import json
import subprocess
import sys

RAW48 = "/home/z/my-project/scripts/scan_cycle2548_raw.json"
RAW47 = "/home/z/my-project/scripts/scan_cycle2547_raw.json"
VAL47 = "/home/z/my-project/scripts/validate_cycle2547.py"
VAL48 = "/home/z/my-project/scripts/validate_cycle2548.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW48, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n47, n48 = norm(RAW47), norm(RAW48)
    print(f"normalized={len(n48)}-vs-{len(n47)}")
    if n48 != n47:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2547->2548 (sed-equivalent)
    with open(VAL47, "r") as f:
        src = f.read()
    rebadged = src.replace("2547", "2548")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2546.py",
         "rebadged from validate_cycle2547.py"),
        ("(sed 2546->2548, the DRIFT-#31 verification-33 harness)",
         "(sed 2547->2548, the DRIFT-#31 verification-34 harness)"),
        ("c2548 = verification 34\n(c2546 = verification 33;",
         "c2548 = verification 35\n(c2547 = verification 34; c2546 = verification 33;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL48, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2547 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2547" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2547 residue"

    r = subprocess.run([sys.executable, VAL48], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
