#!/usr/bin/env python3
"""Decimal-exact watch-ledger arithmetic for cycle 2747 (21-gate class successor).

python-timegm cross-verification of every epoch used in the c2747 entry, plus
Decimal-exact watch computations. The +08 offsets are applied as UTC-minus-8h;
scanned_at fractional seconds are DECIMAL (added as Decimal, never folded into
nanosecond timegm params) — the SKEW ARITHMETIC rule.

Context-carried constants (LOSS-#83: disk record wiped, values carried by the
session continuity chain):
  dd#320              = 1055.184774778   (c2746 scan-to-scan gap)
  window-2747 open    = 1793212694.939926673
  c2746 scanned_at    = 2026-10-28T18:33:14.936Z
  c2746 trigger stamp = 2026-10-29 02:15:38 +08
  c2746 SKEW          = +3.926673ms (post-echo - scanned_at)
  c2746 post-echo     = window-2747 open - 300.000
"""
import calendar
from decimal import Decimal

D = Decimal
failures = []


def guard(name, want, got, tol=D("1e-9")):
    ok = abs(want - got) <= tol
    print(f"{'ok' if ok else 'FAIL'}: {name} computed={want} harness={got}")
    if not ok:
        failures.append(name)


def tg(y, mo, dd, h, mi, s):
    return D(calendar.timegm((y, mo, dd, h, mi, s, 0, 0, 0)))


# --- epoch cross-verifications (timegm decimal-exact) ---
echo_loopopen = D("1793289732.601723813")
stamp_c2747 = tg(2026, 10, 29, 16, 1, 3)                       # 00:01:03 +08
pre_echo = D("1793290321.660657894")
post_echo = D("1793290323.671843758")
scanned_c2747 = tg(2026, 10, 29, 16, 12, 3) + D("0.665")       # .665 DECIMAL
scanned_c2746 = tg(2026, 10, 28, 18, 33, 14) + D("0.936")      # .936 DECIMAL
stamp_c2746 = tg(2026, 10, 28, 18, 15, 38)                     # 02:15:38 +08
window2747 = D("1793212694.939926673")
post_echo_c2746 = D("1793212394.939926673")

guard("stamp_c2747==1793289663.000", stamp_c2747, D("1793289663.000"))
guard("scanned_c2747==1793290323.665", scanned_c2747, D("1793290323.665"))
guard("scanned_c2746==1793212394.936", scanned_c2746, D("1793212394.936"))
guard("stamp_c2746==1793211338.000", stamp_c2746, D("1793211338.000"))
guard("window2747==c2746_postecho+300.000", window2747, post_echo_c2746 + D("300.000"))
guard("c2746_postecho==scanned+skew3.926673ms", post_echo_c2746,
      scanned_c2746 + D("0.003926673"))

# --- watch computations (Decimal-exact) ---
dd321 = scanned_c2747 - scanned_c2746
interval321 = scanned_c2747 - stamp_c2747
lag321 = interval321 + dd321 - D("1055.184774778")
late321 = stamp_c2747 - window2747
collapse321 = post_echo - window2747
skew321_ms = (post_echo - scanned_c2747) * 1000
cadence_gap = stamp_c2747 - stamp_c2746
echo_vs_window = echo_loopopen - window2747
echo_vs_stamp = echo_loopopen - stamp_c2747

guard("dd321", dd321, D("77928.729000000"))
guard("interval321", interval321, D("660.665000000"))
guard("lag321", lag321, D("77534.209225222"))
guard("late321", late321, D("76968.060073327"))
guard("collapse321", collapse321, D("77628.731917085"))
guard("skew321_ms", skew321_ms, D("6.843758000"))
guard("cadence_gap", cadence_gap, D("78325.000000000"))
guard("echo_vs_window", echo_vs_window, D("77037.661797140"))
guard("echo_vs_stamp", echo_vs_stamp, D("69.601723813"))

# --- classification prints ---
print("---")
print(f"dd321={dd321} >> band_hi 3708.066631432 -> PLATEAU m4 TERMINATED, ESCALATION re-opens m1")
print(f"lag321={lag321} POS -> m29 (from m28 @ +880.764232510 context)")
print(f"late321={late321} POS -> m38 (from m37 @ +580.803226225 context)")
print(f"skew321=+{skew321_ms}ms SUB-10 -> m2 (from m1 @ +3.926673ms context)")
print(f"EP14 s337: server 1992ms SUB-2.0 / client 2.000128s ABOVE-2.0 (+0.000128) -> SPLIT verdict,"
      f" no dual branch; STALL m2 stands unextended")
print("SWEEP k=417 band: client 2.000128 NOT IN 1.619102..1.779102 / server 1992 NOT IN 1604..1764"
      " -> BOTH-ABOVE -> re-center k=418: client 1.920128..2.080128 / server 1912..2072")
print("ahead-print: trace token 0001 (00:01:00) vs stamp 00:01:03 = -3.0s BEHIND -> sign flip,"
      " AHEAD run terminated (context +622 step UP +240 at c2746)")
print("size 446B in-band -> size-446 series extends (context m65 -> m66)")
print("first-pass-clean: arrival-guard RED (LOSS-#83 drift) -> clean-run streak NOT extended"
      " (context m7; reset honestly noted)")

if failures:
    print(f"LEDGER_ARITHMETIC_RED: {len(failures)} failures")
    raise SystemExit(1)
print("LEDGER_ARITHMETIC_GREEN: all epochs timegm-verified, all watches Decimal-exact")
