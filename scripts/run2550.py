#!/usr/bin/env python3
"""c2550 pipeline: normalized recursive diff, validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 12th consecutive):
  raw body  = curl -o scan_cycle2550_raw.json (genuine bytes, 446B)
  time_total = 1.725336s (EP14 classification class)
  pre  = 08:19:43.296056867 +08 (epoch 1792973983.296056867)
  post = 08:19:45.029961982 +08 (epoch 1792973985.029961982)
  server start 08:19:43.306 (scanned_at 08:19:45.024 - 1718ms): 10ms skew vs pre — proxy validated (14/11/10/12/12/11/10/10/11/10/11/11/10ms series)
"""
import json
import subprocess
import sys

RAW50 = "/home/z/my-project/scripts/scan_cycle2550_raw.json"
RAW49 = "/home/z/my-project/scripts/scan_cycle2549_raw.json"
VAL49 = "/home/z/my-project/scripts/validate_cycle2549.py"
VAL50 = "/home/z/my-project/scripts/validate_cycle2550.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW50, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n49, n50 = norm(RAW49), norm(RAW50)
    print(f"normalized={len(n50)}-vs-{len(n49)}")
    if n50 != n49:
        print("MARKET_DRIFT")
        sys.exit(2)
    print("MARKET_UNCHANGED")

    # rebadge 2549->2550 (sed-equivalent)
    with open(VAL49, "r") as f:
        src = f.read()
    rebadged = src.replace("2549", "2550")

    # lineage-aware provenance patch (3 explicit sites + sed title site = x4)
    patches = [
        ("rebadged from validate_cycle2548.py",
         "rebadged from validate_cycle2549.py"),
        ("(sed 2548->2550, the DRIFT-#31 verification-35 harness)",
         "(sed 2549->2550, the DRIFT-#31 verification-36 harness)"),
        ("c2550 = verification 36\n(c2548 = verification 35;",
         "c2550 = verification 37\n(c2549 = verification 36; c2548 = verification 35;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL50, "w") as f:
        f.write(rebadged)
    print(f"provenance_patches_applied={len(patches)}+title")

    # residue check: code body must be clean of 2549 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2549" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2549 residue"

    r = subprocess.run([sys.executable, VAL50], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
