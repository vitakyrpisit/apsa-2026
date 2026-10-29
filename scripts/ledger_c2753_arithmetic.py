#!/usr/bin/env python3
"""Decimal-exact watch-ledger arithmetic for cycle 2753.

python-timegm cross-verification of every epoch + Decimal-exact watches.
Constants (on-disk carry now: the c2752 entry + capture log):
  dd#326           = 762.094000000  (c2752 scan-to-scan gap)
  window-2753 open = 1793293767.195530263
  c2752 scanned_at = 1793293467.189 (2026-10-29T17:04:27.189Z)
  c2752 stamp      = 1793292364.000 (00:46:04 +08)
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


echo_loopopen = D("1793293963.737547825")
stamp_c2753 = tg(2026, 10, 29, 17, 1, 5)                       # 01:01:05 +08
pre_echo = D("1793294072.018187407")
post_echo = D("1793294073.978178395")
scanned_c2753 = tg(2026, 10, 29, 17, 14, 33) + D("0.972")      # .972 DECIMAL
scanned_c2752 = tg(2026, 10, 29, 17, 4, 27) + D("0.189")
stamp_c2752 = D("1793292364.000")
window2753 = D("1793293767.195530263")

guard("stamp_c2753==1793293265.000", stamp_c2753, D("1793293265.000"))
guard("scanned_c2753==1793294073.972", scanned_c2753, D("1793294073.972"))
guard("scanned_c2752==1793293467.189 (carry)", scanned_c2752, D("1793293467.189"))
guard("window2753==c2752_postecho+300.000", window2753, D("1793293467.195530263") + D("300.000"))

dd327 = scanned_c2753 - scanned_c2752
interval327 = scanned_c2753 - stamp_c2753
lag327 = interval327 + dd327 - D("762.094000000")
late327 = stamp_c2753 - window2753
collapse327 = post_echo - window2753
skew327_ms = (post_echo - scanned_c2753) * 1000
cadence_stamp = stamp_c2753 - stamp_c2752
cadence_token = D(780)  # 01:08:00 token - 00:55:00 token
echo_vs_window = echo_loopopen - window2753
echo_vs_stamp = echo_loopopen - stamp_c2753
window2754 = post_echo + D("300.000")

guard("dd327", dd327, D("606.783000000"))
guard("interval327", interval327, D("808.972000000"))
guard("lag327", lag327, D("653.661000000"))
guard("late327", late327, D("-502.195530263"))
guard("collapse327", collapse327, D("306.782648132"))
guard("skew327_ms", skew327_ms, D("6.178395000"))
guard("cadence327_stamp", cadence_stamp, D("901.000000000"))
guard("echo_vs_window", echo_vs_window, D("196.542017562"))
guard("echo_vs_stamp", echo_vs_stamp, D("698.737547825"))
guard("window2754==post_echo+300.000", window2754, D("1793294373.978178395"))

print("---")
print(f"dd327={dd327} in [564.552241212..3708.066631432] -> ESCALATION extends m4")
print(f"lag327={lag327} POSITIVE -> POS extends m5 (@ +1264.885 carried)")
print(f"late327={late327} NEGATIVE -> EARLY extends (magnitude fell 641.101509114 -> 502.195530263)")
print(f"skew327=+{skew327_ms}ms SUB-10 -> m8 (from m7 @ +6.530263ms)")
print("EP14 s343: server 1941 SUB-2.0 / client 1.950339 SUB-2.0 -> DUAL SUB-2.0 -> STALL extends m5")
print("SWEEP: client 1.950339 OUT 1.696010..1.856010 (above) / server 1941 OUT 1689..1849 (above) -> NOT both-in-band -> RE-CENTER k=422 (new band client 1.870339..2.030339 / server 1861..2021)")
print("ahead-print: token 0108 (01:08:00) vs stamp 01:01:05 = +415s AHEAD (series +622 -> -3.0 -> +476 -> +536 -> +476 -> +295 -> +536 -> +415)")
print("cadence327=901s by stamp / 780s by token — NEITHER the 600-class NOR the 300-class print (queueing-decomposed, honest)")
print("size 446B in-band -> size-446 m72")
print("rdiff span-1 MARKET_UNCHANGED 419-vs-419 -> the pass-1 observation REPEATS (DRIFT-#49 pass-2, movement repeat-class; fresh unchanged-count opens m1 post-termination)")
print("echo attempt #474: in-batch echo TAKEN; vs window +196.542017562 ABOVE -> conservative MISS (criterion not disk-recoverable) -> 107-for-474")
print(f"window-2754 prophecy = {window2754} (the c2753 Next-block on-disk carry)")

if failures:
    print(f"LEDGER_ARITHMETIC_RED: {len(failures)} failures")
    raise SystemExit(1)
print("LEDGER_ARITHMETIC_GREEN: all epochs timegm-verified, all watches Decimal-exact")
