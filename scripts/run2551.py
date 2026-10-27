#!/usr/bin/env python3
"""c2551 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 13th consecutive):
  raw body  = curl -o scan_cycle2551_raw.json (genuine bytes, 446B)
  time_total = 1.709915s (EP14 classification class)
  pre  = 08:24:01.109448637 +08 (epoch 1792974241.109448637)
  post = 08:24:02.851933505 +08 (epoch 1792974242.851933505)
  server start 08:24:01.121 (scanned_at 08:24:02.820 - 1699ms): 12ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11/10/11/11/10/12ms series)
"""
import json
import subprocess
import sys

RAW51 = "/home/z/my-project/scripts/scan_cycle2551_raw.json"
RAW50 = "/home/z/my-project/scripts/scan_cycle2550_raw.json"
VAL50 = "/home/z/my-project/scripts/validate_cycle2550.py"
VAL51 = "/home/z/my-project/scripts/validate_cycle2551.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW51, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n50, n51 = norm(RAW50), norm(RAW51)
    print(f"normalized={len(n51)}-vs-{len(n50)}")
    if n51 != n50:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2550->2551 (sed-equivalent)
    with open(VAL50, "r") as f:
        src = f.read()
    rebadged = src.replace("2550", "2551")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2549.py",
         "rebadged from validate_cycle2550.py"),
        ("(sed 2549->2551, the DRIFT-#31 verification-36 harness)",
         "(sed 2550->2551, the DRIFT-#31 verification-37 harness)"),
        ("c2551 = verification 37\n(c2549 = verification 36;",
         "c2551 = verification 38\n(c2550 = verification 37; c2549 = verification 36;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL51, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2550 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2550" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2550 residue"

    r = subprocess.run([sys.executable, VAL51], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
