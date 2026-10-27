#!/usr/bin/env python3
"""c2563 pipeline: drift-root RE-ANCHOR (DRIFT-#34), validator rebadge+run.

CAPTURED-CLASS cycle (standard instrumentation, 25th consecutive,
mandatory order held: pre-echo -> curl -o/-w -> post-echo):
  raw body  = curl -o scan_cycle2563_raw.json (genuine bytes, 446B)
  time_total = 2.010732s (EP14 s153 classification class)
  pre  = 10:25:36.834167839 +08 (epoch 1792981536.834167839)
  post = 10:25:38.853548095 +08 (epoch 1792981538.853548095)
  wall span 2.019380256
  server start 10:25:36.846 (scanned_at 10:25:38.849 - 2003ms): 12ms skew
  vs pre — proxy validated 25th consecutive
  (14/11/10/12/12/11/10/10/11/10/11/11/10/12/13/11/11/13/14/11/10/11/12/11/12ms series)

DRIFT ROOT: five-tuple (21,0,0,18,3) != DRIFT-#33 baseline (20,0,0,17,3)
  -> DRIFT-#33 closes at 7-fold (root c2556); DRIFT-#34 root c2563.
  Confirmation pass: old-baseline harness vs c2563 payload produced exactly
  one failure — baseline_match (9/10 ok, exit=1) — the algorithmic
  confirmation of DRIFT #34 (c2454/c2556 precedent).
  Delta: total 20->21, scam 17->18 (a scam-pattern task ENTERED the market),
  honest_free 0 stable, honest_paid 0 stable (NO GOLD — inventory EMPTY
  continues), unknown 3 stable; 446B size band digit-width-stable.
  Composition (21,0,0,18,3) exactly echoes the DRIFT-#29 root family (c2453).
"""
import json
import subprocess
import sys

RAW63 = "/home/z/my-project/scripts/scan_cycle2563_raw.json"
RAW62 = "/home/z/my-project/scripts/scan_cycle2562.json"
VAL62 = "/home/z/my-project/scripts/validate_cycle2562.py"
VAL63 = "/home/z/my-project/scripts/validate_cycle2563.py"


def norm(path):
    with open(path, "rb") as f:
        d = json.loads(f.read())
    d.pop("scanned_at", None)
    d.pop("scan_duration_ms", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def main():
    with open(RAW63, "rb") as f:
        raw_bytes = f.read()
    print(f"raw_bytes={len(raw_bytes)}")
    assert len(raw_bytes) == 446, f"SIZE BAND MISS: {len(raw_bytes)}"

    n62, n63 = norm(RAW62), norm(RAW63)
    print(f"normalized={len(n63)}-vs-{len(n62)}")
    if n63 == n62:
        print("MARKET_UNCHANGED — unexpected at claimed drift root")
        sys.exit(3)
    print("MARKET_DRIFT_CONFIRMED — DRIFT-#33 closes at 7-fold; DRIFT-#34 root c2563")

    # rebadge 2562->2563 (sed-equivalent), then drift-root RE-ANCHOR patches
    with open(VAL62, "r") as f:
        src = f.read()
    rebadged = src.replace("2562", "2563")

    # process generalization (c2559+): pre-verify patch sites BEFORE applying
    print("--- post-sed head (first 8 lines) ---")
    for ln in rebadged.splitlines()[:8]:
        print(ln)
    print("--- patch site pre-counts (expect 1x each) ---")

    patches = [
        # P1: header carry -> re-anchor (source header references 2561, the file IT
        #     was rebadged from — one behind, untouched by the sed; generalized P1 lesson)
        ("DRIFT-#33 verification-7 CARRY: rebadged from validate_cycle2561.py (drift-root precedent c2454/c2514/c2553/c2556)",
         "DRIFT-#34 RE-ANCHOR: rebadged from validate_cycle2562.py (drift-root precedent c2454/c2514/c2553/c2556)"),
        # P2: sed-line lineage fix (global sed corrupted 2561->2562 into 2561->2563)
        ("(sed 2561->2563, the DRIFT-#33 verification-6 harness; DRIFT-#33 verification-7 carry). Baseline",
         "(sed 2562->2563, the DRIFT-#33 verification-7 carry harness; DRIFT-#34 root re-anchor). Baseline"),
        # P3: chain head — flip to DRIFT-#34 root: c2563 = verification 1 with c2562
        #     final-7 inserted (post-sed chain head reads c2563 = verification 7, parenthetical at c2561)
        ("(20,0,0,17,3) @ 446B DRIFT-#33 root; c2563 = verification 7\n(c2561 = verification 6;",
         "(21,0,0,18,3) @ 446B DRIFT-#34 root; c2563 = verification 1\n(c2562 = verification 7, DRIFT-#33 final; c2561 = verification 6;"),
        # P4: baseline constants 20/17 -> 21/18
        ('BASELINE_COMP = {"total": 20, "honest_paid": 0, "honest_free": 0, "scam": 17, "unknown": 3}',
         'BASELINE_COMP = {"total": 21, "honest_paid": 0, "honest_free": 0, "scam": 18, "unknown": 3}'),
        # P5: DRIFT-#34 delta paragraph inserted ahead of the DRIFT-#33 history
        ("DRIFT-#33 delta vs DRIFT-#32: total 21->20, honest_free 1->0 (the LAST honest free task departed the market — honest inventory now EMPTY; honest_paid 0 throughout — no paid movement), scam 17 stable, unknown 3 stable. All other sentinels held: 446B size band (digit-width-stable change), all_honest_paid empty, best_paid_task None, taskbounty zeros, next_scan=300.",
         "DRIFT-#34 delta vs DRIFT-#33: total 20->21, scam 17->18 (a scam-pattern task ENTERED the market — first total movement since the DRIFT-#33 root; the resulting composition (21,0,0,18,3) exactly echoes the DRIFT-#29 root family c2453; honest inventory stays EMPTY — honest_free 0 stable, honest_paid 0 stable — NO GOLD condition, no honest movement), unknown 3 stable. All other sentinels held: 446B size band (digit-width-stable change), all_honest_paid empty, best_paid_task None, taskbounty zeros, next_scan=300.\n\nDRIFT-#33 delta vs DRIFT-#32: total 21->20, honest_free 1->0 (the LAST honest free task departed the market — honest inventory now EMPTY; honest_paid 0 throughout — no paid movement), scam 17 stable, unknown 3 stable. All other sentinels held: 446B size band (digit-width-stable change), all_honest_paid empty, best_paid_task None, taskbounty zeros, next_scan=300."),
        # P6: assertions-encode line
        ("Assertions encode the DRIFT-#33 baseline (20,0,0,17,3) @ 446B:",
         "Assertions encode the DRIFT-#34 baseline (21,0,0,18,3) @ 446B:"),
        # P7: composition bullet
        ("  - BA composition: total=20 honest_paid=0 honest_free=0 scam=17 unknown=3",
         "  - BA composition: total=21 honest_paid=0 honest_free=0 scam=18 unknown=3"),
    ]
    for old, new in patches:
        cnt = rebadged.count(old)
        print(f"  site_count={cnt} :: {old[:64]}")
        assert cnt == 1, f"PATCH SITE MISS ({cnt}x): {old[:60]}"
    for old, new in patches:
        rebadged = rebadged.replace(old, new)
    with open(VAL63, "w") as f:
        f.write(rebadged)
    print(f"reanchor_patches_applied={len(patches)} (drift-root class, first pass, NO misses)")

    # residue check: code body must be clean of 2562 refs
    code_part = rebadged.split("import json", 1)[1]
    residue = [ln for ln in code_part.splitlines() if "2562" in ln]
    print(f"code_residue_lines={len(residue)}")
    for ln in residue[:3]:
        print(f"  RESIDUE: {ln[:100]}")
    assert not residue, "code-body 2562 residue"

    r = subprocess.run([sys.executable, VAL63], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(f"VALIDATOR_EXIT={r.returncode}")
        print(r.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
