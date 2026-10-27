#!/usr/bin/env python3
"""c2558 pipeline: DRIFT-#33 verification-3 (carry-class), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 20th consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2558_raw.json (genuine bytes, 446B)
  time_total = 1.728745s (EP14 classification class)
  pre  = 09:27:31.202242751 +08 (epoch 1792978051.202242751)
  post = 09:27:32.938678222 +08 (epoch 1792978052.938678222)
  server start 09:27:31.213 (scanned_at 09:27:32.935 - 1722ms): 11ms skew
  vs pre — proxy validated 20th consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11ms series)

DRIFT-#33 verification 3: five-tuple (20,0,0,17,3) == baseline (root c2556);
  verification 2 (c2557) -> 3 (c2558). honest inventory EMPTY continues
  (honest_free=0, honest_paid=0); scam 17 stable, unknown 3 stable;
  446B size band digit-width-stable. Recursive diff vs c2557: EXPECT EQUAL
  (MARKET_UNCHANGED — any differ would open DRIFT-#34 evaluation).
"""
import json
import subprocess
import sys

RAW58 = "/home/z/my-project/scripts/scan_cycle2558_raw.json"
RAW57 = "/home/z/my-project/scripts/scan_cycle2557.json"
VAL57 = "/home/z/my-project/scripts/validate_cycle2557.py"
VAL58 = "/home/z/my-project/scripts/validate_cycle2558.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW58, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n58, n57 = norm(RAW58), norm(RAW57)
    print(f"normalized={len(n58)}-vs-{len(n57)}")
    if n58 != n57:
        print("MARKET_DRIFT — unexpected at verification cycle (DRIFT-#34 evaluation)")
        sys.exit(3)
    print("MARKET_UNCHANGED — DRIFT-#33 streak 2-to-3, rc=0")

    # rebadge 2557->2558 (sed-equivalent), then carry-class provenance patches
    with open(VAL57, "r") as f:
        src = f.read()
    rebadged = src.replace("2557", "2558")

    patches = [
        # P1: header carry advance (source header references validate_cycle2556.py — the file IT
        #     was rebadged from, which the sed does NOT touch; update carry class 2->3 and
        #     point the rebadged-from at 2557, the harness this rebadge actually derives from)
        ("DRIFT-#33 verification-2 CARRY: rebadged from validate_cycle2556.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#33 verification-3 CARRY: rebadged from validate_cycle2557.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2556->2557 into 2556->2558)
        ("(sed 2556->2558, the DRIFT-#33 verification-1 root harness; DRIFT-#33 verification-2 carry). Baseline",
         "(sed 2557->2558, the DRIFT-#33 verification-2 harness; DRIFT-#33 verification-3 carry). Baseline"),
        # P3: chain head — bump verification 2->3 AND insert c2557 = verification 2
        #     before the c2556 citation (chain-insertion pattern per the c2557 forecast note:
        #     post-sed the parenthetical starts at c2556-direct)
        ("c2558 = verification 2\n(c2556 = verification 1, DRIFT-#33 root;",
         "c2558 = verification 3\n(c2557 = verification 2; c2556 = verification 1, DRIFT-#33 root;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
        rebadged = rebadged.replace(old, new)
    with open(VAL58, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)} (carry-class, first pass, NO misses)")

    # residue check: code body must be clean of 2557 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2557" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2557 residue"

    r = subprocess.run([sys.executable, VAL58], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
