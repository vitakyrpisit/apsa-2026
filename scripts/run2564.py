#!/usr/bin/env python3
"""c2564 pipeline: DRIFT-#34 verification-2 (carry-class), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 26th consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2564_raw.json (genuine bytes, 446B)
  time_total = 2.315346s (EP14 s154 classification class)
  pre  = 10:43:25.177235625 +08 (epoch 1792982605.177235625)
  post = 10:43:27.500958665 +08 (epoch 1792982607.500958665)
  wall span 2.323723040
  server start 10:43:25.189 (scanned_at 10:43:27.497 - 2308ms): 12ms skew
  vs pre — proxy validated 26th consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11/10/11/12/11/12/12ms series)

DRIFT-#34 verification 2: five-tuple (21,0,0,18,3) == baseline (root c2563);
  verification 1 (c2563) -> 2 (c2564). honest inventory EMPTY continues
  (honest_free=0, honest_paid=0); scam 18 stable, unknown 3 stable;
  446B size band digit-width-stable. Recursive diff vs c2563: EXPECT EQUAL
  (MARKET_UNCHANGED — any differ would open DRIFT-#35 evaluation).
"""
import json
import subprocess
import sys

RAW64 = "/home/z/my-project/scripts/scan_cycle2564_raw.json"
RAW63 = "/home/z/my-project/scripts/scan_cycle2563.json"
VAL63 = "/home/z/my-project/scripts/validate_cycle2563.py"
VAL64 = "/home/z/my-project/scripts/validate_cycle2564.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW64, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n63, n64 = norm(RAW63), norm(RAW64)
    print(f"normalized={len(n64)}-vs-{len(n63)}")
    if n64 != n63:
        print("MARKET_DRIFT — unexpected at verification cycle (DRIFT-#35 evaluation)")
        sys.exit(3)
    print("MARKET_UNCHANGED — DRIFT-#34 streak 1-to-2, rc=0")

    # rebadge 2563->2564 (sed-equivalent), then carry-class provenance patches
    with open(VAL63, "r") as f:
        src = f.read()
    rebadged = src.replace("2563", "2564")

    # process generalization (c2559+): pre-verify patch sites BEFORE applying
    print("--- post-sed head (first 8 lines) ---")
    for ln in rebadged.splitlines()[:8]:
        print(ln)
    print("--- patch site pre-counts (expect 1x each) ---")

    patches = [
        # P1: header re-anchor -> carry advance (source header references validate_cycle2562.py —
        #     one behind, untouched by the sed; generalized P1 lesson; update carry class root->2
        #     and point the rebadged-from at 2563)
        ("DRIFT-#34 RE-ANCHOR: rebadged from validate_cycle2562.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#34 verification-2 CARRY: rebadged from validate_cycle2563.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2562->2563 into 2562->2564)
        ("(sed 2562->2564, the DRIFT-#33 verification-7 carry harness; DRIFT-#34 root re-anchor). Baseline",
         "(sed 2563->2564, the DRIFT-#34 verification-1 root harness; DRIFT-#34 verification-2 carry). Baseline"),
        # P3: chain head — bump verification 1->2 AND insert c2563 = verification 1, DRIFT-#34 root
        #     before the c2562 citation (regular chain-insertion pattern)
        ("(21,0,0,18,3) @ 446B DRIFT-#34 root; c2564 = verification 1\n(c2562 = verification 7, DRIFT-#33 final;",
         "(21,0,0,18,3) @ 446B DRIFT-#34 root; c2564 = verification 2\n(c2563 = verification 1, DRIFT-#34 root; c2562 = verification 7, DRIFT-#33 final;"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        print(f"  site_count={cnt} :: {old[:64]}")
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
    for old, new in patches:
        rebadged = rebadged.replace(old, new)
    with open(VAL64, "w") as f:
        f.write(rebadged)
    print(f"carry_patches_applied={len(patches)} (carry-class, first pass, NO misses)")

    # residue check: code body must be clean of 2563 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2563" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2563 residue"

    r = subprocess.run([sys.executable, VAL64], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
