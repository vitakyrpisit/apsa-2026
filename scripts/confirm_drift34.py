#!/usr/bin/env python3
"""DRIFT-#34 algorithmic confirmation pass (c2454/c2556 root precedent).

Run the OLD-baseline harness (validate_cycle2562.py, DRIFT-#33 baseline
(20,0,0,17,3) @ 446B) against the c2563 payload (sed 2562->2563 so the RAW
path points at scan_cycle2563_raw.json). EXPECTED: exactly one failure —
baseline_match — 9/10 ok, exit=1. That single failure IS the algorithmic
confirmation of DRIFT-#34. Exits non-zero before any archive write (safe).
"""
import subprocess
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2562.py"
TMP = "/home/z/my-project/scripts/tmp_confirm_2563.py"

with open(SRC, "r") as f:
    src = f.read()
rebadged = src.replace("2562", "2563")
with open(TMP, "w") as f:
    f.write(rebadged)

r = subprocess.run([sys.executable, TMP], capture_output=True, text=True)
print(r.stdout.strip())
if r.stderr.strip():
    print("STDERR:", r.stderr.strip())
print(f"CONFIRM_PASS_EXIT={r.returncode}")

fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL:")]
oks = [ln for ln in r.stdout.splitlines() if ln.startswith("ok:")]
print(f"fail_count={len(fails)} ok_count={len(oks)}")
for ln in fails:
    print(f"  {ln}")

# Precedent expectations: exactly ONE failure (baseline_match), 9/10 ok, exit=1.
assert r.returncode == 1, f"unexpected exit {r.returncode} (expected 1)"
assert len(fails) == 1 and "baseline_match" in fails[0], f"unexpected failures: {fails}"
assert len(oks) == 9, f"unexpected ok count {len(oks)} (expected 9)"
print("DRIFT-#34 ALGORITHMICALLY CONFIRMED (single baseline_match failure, 9/10, exit=1)")
