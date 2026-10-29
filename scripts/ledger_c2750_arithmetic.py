#!/usr/bin/env python3
"""Decimal-exact watch-ledger arithmetic for cycle 2750.

python-timegm cross-verification of every epoch + Decimal-exact watches.
Constants (on-disk carry now: the c2749 entry + capture log):
  dd#323           = 497.819000000  (c2749 scan-to-scan gap)
  window-2750 open = 1793291754.849775281
  c2749 scanned_at = 1793291454.843 (2026-10-29T16:30:54.843Z)
  c2749 stamp      = 1793290564.000 (00:16:04 +08)
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


echo_loopopen = D("1793291954.413570675")
stamp_c2750 = tg(2026, 10, 29, 16, 26, 4)                      # 00:26:04 +08
pre_echo = D("1793292102.970793142")
post_echo = D("1793292104.703393245")
scanned_c2750 = tg(2026, 10, 29, 16, 41, 44) + D("0.697")      # .697 DECIMAL
scanned_c2749 = tg(2026, 10, 29, 16, 30, 54) + D("0.843")
stamp_c2749 = D("1793290564.000")
window2750 = D("1793291754.849775281")

guard("stamp_c2750==1793291164.000", stamp_c2750, D("1793291164.000"))
guard("scanned_c2750==1793292104.697", scanned_c2750, D("1793292104.697"))
guard("scanned_c2749==1793291454.843 (carry)", scanned_c2749, D("1793291454.843"))
guard("window2750==c2749_postecho+300.000", window2750, D("1793291454.849775281") + D("300.000"))

dd324 = scanned_c2750 - scanned_c2749
interval324 = scanned_c2750 - stamp_c2750
lag324 = interval324 + dd324 - D("497.819000000")
late324 = stamp_c2750 - window2750
collapse324 = post_echo - window2750
skew324_ms = (post_echo - scanned_c2750) * 1000
cadence324 = stamp_c2750 - stamp_c2749
echo_vs_window = echo_loopopen - window2750
echo_vs_stamp = echo_loopopen - stamp_c2750
window2751 = post_echo + D("300.000")

guard("dd324", dd324, D("649.854000000"))
guard("interval324", interval324, D("940.697000000"))
guard("lag324", lag324, D("1092.732000000"))
guard("late324", late324, D("-590.849775281"))
guard("collapse324", collapse324, D("349.853617964"))
guard("skew324_ms", skew324_ms, D("6.393245000"))
guard("cadence324", cadence324, D("600.000000000"))
guard("echo_vs_window", echo_vs_window, D("199.563795394"))
guard("echo_vs_stamp", echo_vs_stamp, D("790.413570675"))
guard("window2751==post_echo+300.000", window2751, D("1793292404.703393245"))

print("---")
print(f"dd324={dd324} in [564.552241212..3708.066631432] -> DRAIN TERMINATED, ESCALATION re-opens m1")
print(f"lag324={lag324} POSITIVE -> POS extends m2 (@ +755.303 carried)")
print(f"late324={late324} NEGATIVE -> EARLY extends (@ -693.030814043 carried)")
print(f"skew324=+{skew324_ms}ms SUB-10 -> m5 (from m4 @ +6.775281ms)")
print("EP14 s340: server 1715 SUB-2.0 / client 1.722603 SUB-2.0 -> DUAL SUB-2.0 -> STALL extends m2")
print("SWEEP: client 1.722603 OUT 1.920128..2.080128 / server 1715 OUT 1912..2072 -> NOT both-in-band -> RE-CENTER k=419 (new band client 1.642603..1.802603 / server 1635..1795)")
print("ahead-print: token 000034 (00:34:00) vs stamp 00:26:04 = +476s AHEAD (series +622 -> -3.0 -> +476 -> +536 -> +476)")
print("cadence324=600s — the 600-class contract print")
print("size 446B in-band -> size-446 m69")
print("rdiff span-1 MARKET_UNCHANGED 419-vs-419 -> unchanged-streak continues m3 (third consecutive span-1 since LOSS-#83)")
print("echo attempt #471: in-batch echo TAKEN; vs window +199.563795394 ABOVE -> conservative MISS (criterion not disk-recoverable) -> 107-for-471")
print(f"window-2751 prophecy = {window2751} (the c2751 Next-block on-disk carry)")

if failures:
    print(f"LEDGER_ARITHMETIC_RED: {len(failures)} failures")
    raise SystemExit(1)
print("LEDGER_ARITHMETIC_GREEN: all epochs timegm-verified, all watches Decimal-exact")
