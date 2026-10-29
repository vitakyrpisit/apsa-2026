#!/usr/bin/env python3
"""Decimal-exact watch-ledger arithmetic for cycle 2754.

python-timegm cross-verification of every epoch + Decimal-exact watches.
Constants (on-disk carry now: the c2753 entry + capture log):
  dd#327           = 606.783000000  (c2753 scan-to-scan gap)
  window-2754 open = 1793294373.978178395
  c2753 scanned_at = 1793294073.972 (2026-10-29T17:14:33.972Z)
  c2753 stamp      = 1793293265.000 (01:01:05 +08)
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


echo_loopopen = D("1793294558.150610926")
stamp_c2754 = tg(2026, 10, 29, 17, 11, 5)                      # 01:11:05 +08
pre_echo = D("1793294633.144103135")
post_echo = D("1793294634.964190626")
scanned_c2754 = tg(2026, 10, 29, 17, 23, 54) + D("0.957")      # .957 DECIMAL
scanned_c2753 = tg(2026, 10, 29, 17, 14, 33) + D("0.972")
stamp_c2753 = D("1793293265.000")
window2754 = D("1793294373.978178395")

guard("stamp_c2754==1793293865.000", stamp_c2754, D("1793293865.000"))
guard("scanned_c2754==1793294634.957", scanned_c2754, D("1793294634.957"))
guard("scanned_c2753==1793294073.972 (carry)", scanned_c2753, D("1793294073.972"))
guard("window2754==c2753_postecho+300.000", window2754, D("1793294073.978178395") + D("300.000"))

dd328 = scanned_c2754 - scanned_c2753
interval328 = scanned_c2754 - stamp_c2754
lag328 = interval328 + dd328 - D("606.783000000")
late328 = stamp_c2754 - window2754
collapse328 = post_echo - window2754
skew328_ms = (post_echo - scanned_c2754) * 1000
cadence_stamp = stamp_c2754 - stamp_c2753
cadence_token = D(600)  # 01:18:00 token - 01:08:00 token
echo_vs_window = echo_loopopen - window2754
echo_vs_stamp = echo_loopopen - stamp_c2754
window2755 = post_echo + D("300.000")

guard("dd328", dd328, D("560.985000000"))
guard("interval328", interval328, D("769.957000000"))
guard("lag328", lag328, D("724.159000000"))
guard("late328", late328, D("-508.978178395"))
guard("collapse328", collapse328, D("260.986012231"))
guard("skew328_ms", skew328_ms, D("7.190626000"))
guard("cadence328_stamp", cadence_stamp, D("600.000000000"))
guard("echo_vs_window", echo_vs_window, D("184.172432531"))
guard("echo_vs_stamp", echo_vs_stamp, D("693.150610926"))
guard("window2755==post_echo+300.000", window2755, D("1793294934.964190626"))

print("---")
print(f"dd328={dd328} < 564.552241212 -> SUB-BAND DRAIN re-opens m1 (the ESCALATION run m1-m5 terminates; the c2749 sub-band precedent class)")
print(f"lag328={lag328} POSITIVE -> POS extends m6 (@ +653.661 carried)")
print(f"late328={late328} NEGATIVE -> EARLY extends (magnitude rose 502.195530263 -> 508.978178395)")
print(f"skew328=+{skew328_ms}ms SUB-10 -> m9 (from m8 @ +6.178395ms)")
print("EP14 s344: server 1798 SUB-2.0 / client 1.809638 SUB-2.0 -> DUAL SUB-2.0 -> STALL extends m6")
print("SWEEP: client 1.809638 OUT 1.870339..2.030339 (below) / server 1798 OUT 1861..2021 (below) -> NOT both-in-band -> RE-CENTER k=423 (new band client 1.729638..1.889638 / server 1718..1878)")
print("ahead-print: token 0118 (01:18:00) vs stamp 01:11:05 = +415s AHEAD (series +622 -> -3.0 -> +476 -> +536 -> +476 -> +295 -> +536 -> +415 -> +415)")
print("cadence328=600s by stamp / 600s by token — the 600-class print by BOTH (the c2750 precedent)")
print("size 446B in-band -> size-446 m73")
print("rdiff span-1 MARKET_UNCHANGED 419-vs-419 -> the pass-2 observation REPEATS (DRIFT-#49 pass-3, movement repeat-class; fresh unchanged-count extends m2)")
print("echo attempt #475: in-batch echo TAKEN; vs window +184.172432531 ABOVE -> conservative MISS (criterion not disk-recoverable) -> 107-for-475")
print(f"window-2755 prophecy = {window2755} (the c2754 Next-block on-disk carry)")

if failures:
    print(f"LEDGER_ARITHMETIC_RED: {len(failures)} failures")
    raise SystemExit(1)
print("LEDGER_ARITHMETIC_GREEN: all epochs timegm-verified, all watches Decimal-exact")
