#!/usr/bin/env python3
"""Decimal-exact watch-ledger arithmetic for cycle 2751.

python-timegm cross-verification of every epoch + Decimal-exact watches.
Constants (on-disk carry now: the c2750 entry + capture log):
  dd#324           = 649.854000000  (c2750 scan-to-scan gap)
  window-2751 open = 1793292404.703393245
  c2750 scanned_at = 1793292104.697 (2026-10-29T16:41:44.697Z)
  c2750 stamp      = 1793291164.000 (00:26:04 +08)
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


echo_loopopen = D("1793292652.625061858")
stamp_c2751 = tg(2026, 10, 29, 16, 41, 5)                      # 00:41:05 +08
pre_echo = D("1793292703.225495481")
post_echo = D("1793292705.101509114")
scanned_c2751 = tg(2026, 10, 29, 16, 51, 45) + D("0.095")      # .095 DECIMAL
scanned_c2750 = tg(2026, 10, 29, 16, 41, 44) + D("0.697")
stamp_c2750 = D("1793291164.000")
window2751 = D("1793292404.703393245")

guard("stamp_c2751==1793292065.000", stamp_c2751, D("1793292065.000"))
guard("scanned_c2751==1793292705.095", scanned_c2751, D("1793292705.095"))
guard("scanned_c2750==1793292104.697 (carry)", scanned_c2750, D("1793292104.697"))
guard("window2751==c2750_postecho+300.000", window2751, D("1793292104.703393245") + D("300.000"))

dd325 = scanned_c2751 - scanned_c2750
interval325 = scanned_c2751 - stamp_c2751
lag325 = interval325 + dd325 - D("649.854000000")
late325 = stamp_c2751 - window2751
collapse325 = post_echo - window2751
skew325_ms = (post_echo - scanned_c2751) * 1000
cadence325 = stamp_c2751 - stamp_c2750
echo_vs_window = echo_loopopen - window2751
echo_vs_stamp = echo_loopopen - stamp_c2751
window2752 = post_echo + D("300.000")

guard("dd325", dd325, D("600.398000000"))
guard("interval325", interval325, D("640.095000000"))
guard("lag325", lag325, D("590.639000000"))
guard("late325", late325, D("-339.703393245"))
guard("collapse325", collapse325, D("300.398115869"))
guard("skew325_ms", skew325_ms, D("6.509114000"))
guard("cadence325", cadence325, D("901.000000000"))
guard("echo_vs_window", echo_vs_window, D("247.921668613"))
guard("echo_vs_stamp", echo_vs_stamp, D("587.625061858"))
guard("window2752==post_echo+300.000", window2752, D("1793293005.101509114"))

print("---")
print(f"dd325={dd325} in [564.552241212..3708.066631432] -> ESCALATION extends m2")
print(f"lag325={lag325} POSITIVE -> POS extends m3 (@ +1092.732 carried)")
print(f"late325={late325} NEGATIVE -> EARLY extends (@ -590.849775281 carried)")
print(f"skew325=+{skew325_ms}ms SUB-10 -> m6 (from m5 @ +6.393245ms)")
print("EP14 s341: server 1858 SUB-2.0 / client 1.866149 SUB-2.0 -> DUAL SUB-2.0 -> STALL extends m3")
print("SWEEP: client 1.866149 OUT 1.642603..1.802603 / server 1858 OUT 1635..1795 -> NOT both-in-band -> RE-CENTER k=420 (new band client 1.786149..1.946149 / server 1778..1938)")
print("ahead-print: token 000046 (00:46:00) vs stamp 00:41:05 = +295s AHEAD (series +622 -> -3.0 -> +476 -> +536 -> +476 -> +295)")
print("cadence325=901s by stamp / 720s by token — NEITHER the 600-class NOR the 300-class print (queueing-decomposed, honest)")
print("size 446B in-band -> size-446 m70")
print("rdiff span-1 MARKET_UNCHANGED 419-vs-419 -> unchanged-streak continues m4 (fourth consecutive span-1 since LOSS-#83)")
print("echo attempt #472: in-batch echo TAKEN; vs window +247.921668613 ABOVE -> conservative MISS (criterion not disk-recoverable) -> 107-for-472")
print(f"window-2752 prophecy = {window2752} (the c2752 Next-block on-disk carry)")

if failures:
    print(f"LEDGER_ARITHMETIC_RED: {len(failures)} failures")
    raise SystemExit(1)
print("LEDGER_ARITHMETIC_GREEN: all epochs timegm-verified, all watches Decimal-exact")
