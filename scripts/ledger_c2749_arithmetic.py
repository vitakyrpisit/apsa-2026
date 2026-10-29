#!/usr/bin/env python3
"""Decimal-exact watch-ledger arithmetic for cycle 2749.

python-timegm cross-verification of every epoch + Decimal-exact watches.
Constants (on-disk carry now: the c2748 entry + capture log):
  dd#322           = 633.359000000  (c2748 scan-to-scan gap)
  window-2749 open = 1793291257.030814043
  c2748 scanned_at = 1793290957.024 (2026-10-29T16:22:37.024Z)
  c2748 stamp      = 1793290264.000 (00:11:04 +08)
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


echo_loopopen = D("1793291376.446352251")
stamp_c2749 = tg(2026, 10, 29, 16, 16, 4)                      # 00:16:04 +08
pre_echo = D("1793291452.876852513")
post_echo = D("1793291454.849775281")
scanned_c2749 = tg(2026, 10, 29, 16, 30, 54) + D("0.843")      # .843 DECIMAL
scanned_c2748 = tg(2026, 10, 29, 16, 22, 37) + D("0.024")
stamp_c2748 = D("1793290264.000")
window2749 = D("1793291257.030814043")

guard("stamp_c2749==1793290564.000", stamp_c2749, D("1793290564.000"))
guard("scanned_c2749==1793291454.843", scanned_c2749, D("1793291454.843"))
guard("window2749==c2748_postecho+300.000", window2749, D("1793290957.030814043") + D("300.000"))

dd323 = scanned_c2749 - scanned_c2748
interval323 = scanned_c2749 - stamp_c2749
lag323 = interval323 + dd323 - D("633.359000000")
late323 = stamp_c2749 - window2749
collapse323 = post_echo - window2749
skew323_ms = (post_echo - scanned_c2749) * 1000
cadence323 = stamp_c2749 - stamp_c2748
echo_vs_window = echo_loopopen - window2749
echo_vs_stamp = echo_loopopen - stamp_c2749

guard("dd323", dd323, D("497.819000000"))
guard("interval323", interval323, D("890.843000000"))
guard("lag323", lag323, D("755.303000000"))
guard("late323", late323, D("-693.030814043"))
guard("collapse323", collapse323, D("197.818961238"))
guard("skew323_ms", skew323_ms, D("6.775281000"))
guard("cadence323", cadence323, D("300.000000000"))
guard("echo_vs_window", echo_vs_window, D("119.415538208"))
guard("echo_vs_stamp", echo_vs_stamp, D("812.446352251"))

print("---")
print(f"dd323={dd323} < 564.552241212 -> DRAIN m1 OPENS (first sub-band interval since the band stood)")
print(f"lag323={lag323} POSITIVE -> flip edge FIRES back: NEG m1 TERMINATED, POS re-opens m1 @ +755.303")
print(f"late323={late323} NEGATIVE -> EARLY m1 extends (@ -359.671843758 carried)")
print(f"skew323=+{skew323_ms}ms SUB-10 -> m4 (from m3 @ +6.814043ms)")
print("EP14 s339: server 1955 SUB-2.0 / client 1.962789 SUB-2.0 -> DUAL SUB-2.0 -> STALL re-opens m1 (the s338 OPEN line closes)")
print("SWEEP k=418: client 1.962789 IN 1.920128..2.080128 / server 1955 IN 1912..2072 -> both-in-band HOLD m2")
print("ahead-print: token 000025 (00:25:00) vs stamp 00:16:04 = +536s AHEAD (series +622 -> -3.0 -> +476 -> +536)")
print("cadence323=300s — the 300-class contract print")
print("size 446B in-band -> size-446 m68")
print("rdiff span-1 MARKET_UNCHANGED 419-vs-419 -> unchanged-streak continues m2 (consecutive-archive class)")
print("echo attempt #470: in-batch echo TAKEN; vs window +119.415538208 ABOVE -> conservative MISS (criterion not disk-recoverable) -> 107-for-470")

if failures:
    print(f"LEDGER_ARITHMETIC_RED: {len(failures)} failures")
    raise SystemExit(1)
print("LEDGER_ARITHMETIC_GREEN: all epochs timegm-verified, all watches Decimal-exact")
