#!/usr/bin/env python3
"""Decimal-exact ledger derivation for the c2818 entry prints.
Every constant computed here lands in entry_cycle2818.txt verbatim."""
from decimal import Decimal as D
import calendar

def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9

POST = D("1793334916.503403091")    # c2818 capture post-echo (EPOCH-governs)
SCAN = D("1793334916.498")          # c2818 scanned_at (decimal)
TRIG = D("1793334078.000")          # c2818 trigger stamp (12:21:18 +08)
WIN = D("1793334401.674751215")     # window-2818 open (c2817 prophecy EPOCH)
PRE = D("1793334914.697021096")     # c2818 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793334742.515107961")   # c2818 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793334744.168910915")  # c2818 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793334744.162")        # c2818 echo scanned_at (decimal)
C2817_SCAN = D("1793334101.669")    # c2817 scanned_at
C2817_POST = D("1793334101.674751215")  # c2817 post-echo
C2817_PRE = D("1793334100.184672197")   # c2817 capture pre-echo
C2817_ECHO_POST = D("1793333828.255033591")  # c2817 echo post-echo
C2816_POST = D("1793333244.708518331")  # c2816 post-echo (window-2817 re-check)
WIN2817 = D("1793333544.708518331")  # window-2817 open (re-check)
C2817_CLOSE = D("1793334414.000")   # c2817 close da7d469 (04:26:54Z)
FOREIGN_NOW = D("1793334429.000")   # foreign a009715 (04:27:09Z)
C2817_TRIG = D("1793333178.000")    # c2817 trigger stamp (12:06:18 +08)
TOKEN = D("1793334420.000")         # token 1227 (12:27:00 +08)
C2817_TOKEN = D("1793333580.000")   # token 1213 (12:13:00 +08)

print("=== epoch cross-checks (vs timegm) ===")
pairs = [
    ("trigger stamp 12:21:18 +08", utc_epoch(2026, 10, 30, 4, 21, 18), TRIG),
    ("c2817 trigger 12:06:18 +08", utc_epoch(2026, 10, 30, 4, 6, 18), C2817_TRIG),
    ("capture pre-echo EPOCH", utc_epoch(2026, 10, 30, 4, 35, 14, 697021096), PRE),
    ("pre-echo ISO .696389132", utc_epoch(2026, 10, 30, 4, 35, 14, 696389132), D("1793334914.696389132")),
    ("post-echo ISO .502777923", utc_epoch(2026, 10, 30, 4, 35, 16, 502777923), D("1793334916.502777923")),
    ("post-echo EPOCH", utc_epoch(2026, 10, 30, 4, 35, 16, 503403091), POST),
    ("echo pre-echo EPOCH", utc_epoch(2026, 10, 30, 4, 32, 22, 515107961), ECHO_PRE),
    ("echo post-echo EPOCH", utc_epoch(2026, 10, 30, 4, 32, 24, 168910915), ECHO_POST),
    ("scanned_at decimal", D(str(utc_epoch(2026, 10, 30, 4, 35, 16))) + D("0.498"), SCAN),
    ("echo scanned_at decimal", D(str(utc_epoch(2026, 10, 30, 4, 32, 24))) + D("0.162"), ECHO_SCAN),
    ("window-2818 open render", utc_epoch(2026, 10, 30, 4, 26, 41, 674751215), WIN),
    ("c2817 close 04:26:54Z", utc_epoch(2026, 10, 30, 4, 26, 54), C2817_CLOSE),
    ("foreign 04:27:09Z", utc_epoch(2026, 10, 30, 4, 27, 9), FOREIGN_NOW),
    ("token 1227 04:27:00Z", utc_epoch(2026, 10, 30, 4, 27, 0), TOKEN),
    ("c2817 token 1213 04:13:00Z", utc_epoch(2026, 10, 30, 4, 13, 0), C2817_TOKEN),
]
for name, want, got in pairs:
    ok = abs(D(str(want)) - got) < D("0.000001")
    print(f"{'ok' if ok else 'RED'}: {name} computed={D(str(want))} harness={got}")

print("=== exact ledger constants ===")
checks = [
    ("dd#392 = INTERVAL-between-scans - 300 = 814.828651876 - 300", (POST - C2817_POST) - D("300.000")),
    ("INTERVAL-between-scans#392 = POST - C2817_POST", POST - C2817_POST),
    ("INTERVAL#392 = SCAN - TRIG", SCAN - TRIG),
    ("LAG#392 = INTERVAL + dd - INTERVAL#391(923.669)", (SCAN - TRIG) + ((POST - C2817_POST) - D("300.000")) - D("923.669")),
    ("LATE#392 = TRIG - WIN", TRIG - WIN),
    ("SKEW = POST - SCAN", POST - SCAN),
    ("SKEW headroom (10 - 5.403091)", D("10.000000") - (POST - SCAN)),
    ("CAPTURE POST-WINDOW = POST - WIN", POST - WIN),
    ("capture post-c2817-post-echo", POST - C2817_POST),
    ("capture wall = POST - PRE", POST - PRE),
    ("stamp-to-capture-pre = PRE - TRIG", PRE - TRIG),
    ("echo wall = ECHO_POST - ECHO_PRE", ECHO_POST - ECHO_PRE),
    ("stamp-to-echo = ECHO_PRE - TRIG", ECHO_PRE - TRIG),
    ("echo POST-WINDOW = ECHO_POST - WIN", ECHO_POST - WIN),
    ("echo-side skew-analog = ECHO_POST - ECHO_SCAN", ECHO_POST - ECHO_SCAN),
    ("trigger POSTDATES c2817 echo post-echo by", TRIG - C2817_ECHO_POST),
    ("c2817 capture pre PREDATED by trigger (PRE - TRIG)", C2817_PRE - TRIG),
    ("c2817 scanned_at PREDATED by trigger", C2817_SCAN - TRIG),
    ("c2817 capture post-echo PREDATED by trigger", C2817_POST - TRIG),
    ("c2817 close POSTDATES trigger by", C2817_CLOSE - TRIG),
    ("foreign POSTDATES trigger by", FOREIGN_NOW - TRIG),
    ("token-vs-stamp +342 (TOKEN - TRIG)", TOKEN - TRIG),
    ("stamp-gap 900 (TRIG - C2817_TRIG)", TRIG - C2817_TRIG),
    ("token-gap 900 (TOKEN - C2817_TOKEN)", TOKEN - C2817_TOKEN),
    ("c2817 close vs token-1227 second (TOKEN - CLOSE)", TOKEN - C2817_CLOSE),
    ("foreign vs token-1227 second (FOREIGN - TOKEN)", FOREIGN_NOW - TOKEN),
    ("c2817 close vs window-2818 open", C2817_CLOSE - WIN),
    ("foreign vs window-2818 open", FOREIGN_NOW - WIN),
    ("window-2819 open prophecy = POST + 300", POST + D("300.000")),
    ("LAG run-high distance (1712.596 - 429.657651876)", D("1712.596") - ((SCAN - TRIG) + ((POST - C2817_POST) - D("300.000")) - D("923.669"))),
    ("LATE magnitude shrank (366.708518331 - 323.674751215)", D("366.708518331") - (WIN - TRIG)),
    ("SWEEP client miss (1.797099 - 1.599770)", D("1.797099") - D("1.599770")),
    ("SWEEP server miss (1791.000 - 1552.000)", D("1791.000") - D("1552.000")),
    ("window-2817 re-check: WIN2817 - C2816_POST", WIN2817 - C2816_POST),
    ("dd#392 re-verify against dd#391 print: 856.966 - 300", D("856.966") - D("300.000")),
]
for name, val in checks:
    print(f"{name} = {val}")
