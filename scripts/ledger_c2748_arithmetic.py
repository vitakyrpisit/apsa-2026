#!/usr/bin/env python3
"""Decimal-exact watch-ledger arithmetic for cycle 2748.

python-timegm cross-verification of every epoch + Decimal-exact watches.
Constants (on-disk carry now: the c2747 entry + capture log):
  dd#321           = 77928.729000000  (c2747 scan-to-scan gap)
  window-2748 open = 1793290623.671843758
  c2747 scanned_at = 1793290323.665 (2026-10-29T16:12:03.665Z)
  c2747 stamp      = 1793289663.000 (00:01:03 +08)
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


echo_loopopen = D("1793290847.543393112")
stamp_c2748 = tg(2026, 10, 29, 16, 11, 4)                      # 00:11:04 +08
pre_echo = D("1793290955.003916149")
post_echo = D("1793290957.030814043")
scanned_c2748 = tg(2026, 10, 29, 16, 22, 37) + D("0.024")      # .024 DECIMAL
scanned_c2747 = tg(2026, 10, 29, 16, 12, 3) + D("0.665")
stamp_c2747 = D("1793289663.000")
window2748 = D("1793290623.671843758")

guard("stamp_c2748==1793290264.000", stamp_c2748, D("1793290264.000"))
guard("scanned_c2748==1793290957.024", scanned_c2748, D("1793290957.024"))
guard("window2748==c2747_postecho+300.000", window2748, D("1793290323.671843758") + D("300.000"))

dd322 = scanned_c2748 - scanned_c2747
interval322 = scanned_c2748 - stamp_c2748
lag322 = interval322 + dd322 - D("77928.729000000")
late322 = stamp_c2748 - window2748
collapse322 = post_echo - window2748
skew322_ms = (post_echo - scanned_c2748) * 1000
cadence322 = stamp_c2748 - stamp_c2747
echo_vs_window = echo_loopopen - window2748
echo_vs_stamp = echo_loopopen - stamp_c2748

guard("dd322", dd322, D("633.359000000"))
guard("interval322", interval322, D("693.024000000"))
guard("lag322", lag322, D("-76602.346000000"))
guard("late322", late322, D("-359.671843758"))
guard("collapse322", collapse322, D("333.358970285"))
guard("skew322_ms", skew322_ms, D("6.814043000"))
guard("cadence322", cadence322, D("601.000000000"))
guard("echo_vs_window", echo_vs_window, D("223.871549354"))
guard("echo_vs_stamp", echo_vs_stamp, D("583.543393112"))

print("---")
print(f"dd322={dd322} IN-BAND [564.552241212..3708.066631432] -> ESCALATION extends m2")
print(f"lag322={lag322} NEGATIVE -> flip edge FIRES: POS m29 TERMINATED, NEG m1 opens")
print(f"late322={late322} NEGATIVE -> EARLY m1 opens (LATE POS m38 terminated on sign flip)")
print(f"skew322=+{skew322_ms}ms SUB-10 -> m3 (from m2 @ +6.843758ms)")
print("EP14 s338: server 2009 ABOVE-2.0 / client 2.016512 ABOVE-2.0 -> DUAL ABOVE-2.0 -> OPEN re-opens m1 (STALL m2 terminated)")
print("SWEEP k=418: client 2.016512 IN 1.920128..2.080128 / server 2009 IN 1912..2072 -> both-in-band HOLD m1")
print("ahead-print: token 0019 (00:19:00) vs stamp 00:11:04 = +476s AHEAD (sign flip back; series +622 -> -3.0 -> +476)")
print("cadence322=601s — the 600-class contract print returns")
print("size 446B in-band -> size-446 m67")
print("rdiff span-1 MARKET_UNCHANGED 419-vs-419 -> unchanged-streak RESUMED m1 (consecutive-archive class)")
print("echo attempt #469: in-batch echo TAKEN; vs window +223.871549354 ABOVE -> conservative MISS (criterion not disk-recoverable) -> 107-for-469")

if failures:
    print(f"LEDGER_ARITHMETIC_RED: {len(failures)} failures")
    raise SystemExit(1)
print("LEDGER_ARITHMETIC_GREEN: all epochs timegm-verified, all watches Decimal-exact")
