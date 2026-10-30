#!/usr/bin/env python3
"""Decimal-exact ledger derivation for the c2819 entry prints.
Every constant computed here lands in entry_cycle2819.txt verbatim."""
from decimal import Decimal as D
import calendar

def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9

POST = D("1793335756.357947395")    # c2819 capture post-echo (EPOCH-governs)
SCAN = D("1793335756.352")          # c2819 scanned_at (decimal)
TRIG = D("1793334678.000")          # c2819 trigger stamp (12:31:18 +08)
WIN = D("1793335216.503403091")     # window-2819 open (c2818 prophecy EPOCH)
PRE = D("1793335754.652641980")     # c2819 capture pre-echo (EPOCH-governs)
ECHO_PRE = D("1793335434.454358605")   # c2819 echo pre-echo (EPOCH-governs)
ECHO_POST = D("1793335436.153565649")  # c2819 echo post-echo (EPOCH-governs)
ECHO_SCAN = D("1793335436.147")        # c2819 echo scanned_at (decimal)
C2818_SCAN = D("1793334916.498")    # c2818 scanned_at
C2818_POST = D("1793334916.503403091")  # c2818 post-echo
C2818_PRE = D("1793334914.697021096")   # c2818 capture pre-echo
C2818_ECHO_PRE = D("1793334742.515107961")  # c2818 echo pre-echo
C2818_ECHO_POST = D("1793334744.168910915")  # c2818 echo post-echo
C2817_POST = D("1793334101.674751215")  # c2817 post-echo (window-2818 re-check)
WIN2818 = D("1793334401.674751215")  # window-2818 open (re-check)
C2818_CLOSE = D("1793335240.000")   # c2818 close 290adbb (04:40:40Z)
FOREIGN_NOW = D("1793335262.000")   # foreign 724e4a0 (04:41:02Z)
C2818_TRIG = D("1793334078.000")    # c2818 trigger stamp (12:21:18 +08)
TOKEN = D("1793335260.000")         # token 1241 (12:41:00 +08)
C2818_TOKEN = D("1793334420.000")   # token 1227 (12:27:00 +08)

print("=== epoch cross-checks (vs timegm) ===")
pairs = [
    ("trigger stamp 12:31:18 +08", utc_epoch(2026, 10, 30, 4, 31, 18), TRIG),
    ("c2818 trigger 12:21:18 +08", utc_epoch(2026, 10, 30, 4, 21, 18), C2818_TRIG),
    ("capture pre-echo EPOCH", utc_epoch(2026, 10, 30, 4, 49, 14, 652641980), PRE),
    ("pre-echo ISO .651999009", utc_epoch(2026, 10, 30, 4, 49, 14, 651999009), D("1793335754.651999009")),
    ("post-echo ISO .357316613", utc_epoch(2026, 10, 30, 4, 49, 16, 357316613), D("1793335756.357316613")),
    ("post-echo EPOCH", utc_epoch(2026, 10, 30, 4, 49, 16, 357947395), POST),
    ("echo pre-echo EPOCH", utc_epoch(2026, 10, 30, 4, 43, 54, 454358605), ECHO_PRE),
    ("echo post-echo EPOCH", utc_epoch(2026, 10, 30, 4, 43, 56, 153565649), ECHO_POST),
    ("scanned_at decimal", D(str(utc_epoch(2026, 10, 30, 4, 49, 16))) + D("0.352"), SCAN),
    ("echo scanned_at decimal", D(str(utc_epoch(2026, 10, 30, 4, 43, 56))) + D("0.147"), ECHO_SCAN),
    ("window-2819 open render", utc_epoch(2026, 10, 30, 4, 40, 16, 503403091), WIN),
    ("c2818 close 04:40:40Z", utc_epoch(2026, 10, 30, 4, 40, 40), C2818_CLOSE),
    ("foreign 04:41:02Z", utc_epoch(2026, 10, 30, 4, 41, 2), FOREIGN_NOW),
    ("token 1241 04:41:00Z", utc_epoch(2026, 10, 30, 4, 41, 0), TOKEN),
    ("c2818 token 1227 04:27:00Z", utc_epoch(2026, 10, 30, 4, 27, 0), C2818_TOKEN),
]
for name, want, got in pairs:
    ok = abs(D(str(want)) - got) < D("0.000001")
    print(f"{'ok' if ok else 'RED'}: {name} computed={D(str(want))} harness={got}")

print("=== exact ledger constants ===")
checks = [
    ("dd#393 = INTERVAL-between-scans - 300 = 839.854544304 - 300", (POST - C2818_POST) - D("300.000")),
    ("INTERVAL-between-scans#393 = POST - C2818_POST", POST - C2818_POST),
    ("INTERVAL#393 = SCAN - TRIG", SCAN - TRIG),
    ("LAG#393 = INTERVAL + dd - INTERVAL#392(838.498)", (SCAN - TRIG) + ((POST - C2818_POST) - D("300.000")) - D("838.498")),
    ("LATE#393 = TRIG - WIN", TRIG - WIN),
    ("SKEW = POST - SCAN", POST - SCAN),
    ("SKEW headroom (10 - 5.947395)", D("10.000000") - (POST - SCAN)),
    ("CAPTURE POST-WINDOW = POST - WIN", POST - WIN),
    ("capture post-c2818-post-echo", POST - C2818_POST),
    ("capture wall = POST - PRE", POST - PRE),
    ("stamp-to-capture-pre = PRE - TRIG", PRE - TRIG),
    ("echo wall = ECHO_POST - ECHO_PRE", ECHO_POST - ECHO_PRE),
    ("stamp-to-echo = ECHO_PRE - TRIG", ECHO_PRE - TRIG),
    ("echo POST-WINDOW = ECHO_POST - WIN", ECHO_POST - WIN),
    ("echo-side skew-analog = ECHO_POST - ECHO_SCAN", ECHO_POST - ECHO_SCAN),
    ("trigger PREDATES the c2818 echo pre-echo by (C2818_ECHO_PRE - TRIG)", C2818_ECHO_PRE - TRIG),
    ("trigger PREDATES the c2818 echo post-echo by (C2818_ECHO_POST - TRIG)", C2818_ECHO_POST - TRIG),
    ("c2818 capture pre PREDATED by trigger (PRE - TRIG)", C2818_PRE - TRIG),
    ("c2818 scanned_at PREDATED by trigger", C2818_SCAN - TRIG),
    ("c2818 capture post-echo PREDATED by trigger", C2818_POST - TRIG),
    ("c2818 close POSTDATES trigger by", C2818_CLOSE - TRIG),
    ("foreign POSTDATES trigger by", FOREIGN_NOW - TRIG),
    ("token-vs-stamp +582 (TOKEN - TRIG)", TOKEN - TRIG),
    ("stamp-gap 600 (TRIG - C2818_TRIG)", TRIG - C2818_TRIG),
    ("token-gap 840 (TOKEN - C2818_TOKEN)", TOKEN - C2818_TOKEN),
    ("c2818 close vs token-1241 second (TOKEN - CLOSE)", TOKEN - C2818_CLOSE),
    ("foreign vs token-1241 second (FOREIGN - TOKEN)", FOREIGN_NOW - TOKEN),
    ("c2818 close vs window-2819 open", C2818_CLOSE - WIN),
    ("foreign vs window-2819 open", FOREIGN_NOW - WIN),
    ("window-2820 open prophecy = POST + 300", POST + D("300.000")),
    ("LAG run-high distance (1712.596 - 779.708544304)", D("1712.596") - ((SCAN - TRIG) + ((POST - C2818_POST) - D("300.000")) - D("838.498"))),
    ("LATE magnitude grew (538.503403091 - 323.674751215)", (WIN - TRIG) - D("323.674751215")),
    ("SWEEP server miss (1711.000 - 1689.000)", D("1711.000") - D("1689.000")),
    ("DRAIN miss (564.552241212 - 539.854544304)", D("564.552241212") - ((POST - C2818_POST) - D("300.000"))),
    ("window-2818 re-check: WIN2818 - C2817_POST", WIN2818 - C2817_POST),
    ("dd#393 re-verify against dd#392 print: 814.829 - 300", D("814.829") - D("300.000")),
    ("echo PREDATED the capture pre-echo (order check)", PRE - ECHO_POST),
]
for name, val in checks:
    print(f"{name} = {val}")
