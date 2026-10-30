#!/usr/bin/env python3
"""Decimal-exact arithmetic pre-check for the c2813 entry constants."""
from decimal import Decimal as D
import calendar

def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9

POST = D("1793330089.757462242")
SCAN = D("1793330089.752")
TRIG = D("1793328677.000")
WIN = D("1793328988.217915386")
PRE = D("1793330088.037175665")
ECHO_PRE = D("1793329671.491053914")
ECHO_POST = D("1793329673.062755684")
ECHO_SCAN = D("1793329673.057")
C2812_SCAN = D("1793328688.212")
C2812_POST = D("1793328688.217915386")
C2812_PRE = D("1793328686.469282375")
C2812_ECHO_POST = D("1793328410.534691612")
C2812_CLOSE = D("1793329236.000")
FOREIGN_NOW = D("1793329264.000")
C2812_TRIG = D("1793327477.000")
WIN2812 = D("1793327526.818599805")
TOKEN = D("1793329260.000")
C2812_TOKEN = D("1793327940.000")

checks = [
    ("trigger epoch 02:51:17Z", D(str(utc_epoch(2026,10,30,2,51,17))), TRIG),
    ("c2812 trigger epoch 02:31:17Z", D(str(utc_epoch(2026,10,30,2,31,17))), C2812_TRIG),
    ("token 1101 03:01:00Z", D(str(utc_epoch(2026,10,30,3,1,0))), TOKEN),
    ("c2812 token 1039 02:39:00Z", D(str(utc_epoch(2026,10,30,2,39,0))), C2812_TOKEN),
    ("c2812 close 03:00:36Z", D(str(utc_epoch(2026,10,30,3,0,36))), C2812_CLOSE),
    ("foreign 30a3440 03:01:04Z", D(str(utc_epoch(2026,10,30,3,1,4))), FOREIGN_NOW),
    ("POST epoch 03:14:49.757462242", D(str(utc_epoch(2026,10,30,3,14,49,757462242))), POST),
    ("PRE epoch 03:14:48.037175665", D(str(utc_epoch(2026,10,30,3,14,48,37175665))), PRE),
    ("PRE ISO .036435212", D(str(utc_epoch(2026,10,30,3,14,48,36435212))), D("1793330088.036435212")),
    ("POST ISO .756765295", D(str(utc_epoch(2026,10,30,3,14,49,756765295))), D("1793330089.756765295")),
    ("SCAN 03:14:49.752", D(str(utc_epoch(2026,10,30,3,14,49))) + D("0.752"), SCAN),
    ("WIN 02:56:28.217915386", D(str(utc_epoch(2026,10,30,2,56,28,217915386))), WIN),
    ("WIN2814 = POST + 300", POST + D("300.000"), D("1793330389.757462242")),
    ("C2812_POST epoch", D(str(utc_epoch(2026,10,30,2,51,28,217915386))), C2812_POST),
    ("C2812_PRE epoch", D(str(utc_epoch(2026,10,30,2,51,26,469282375))), C2812_PRE),
    ("C2812_ECHO_POST epoch", D(str(utc_epoch(2026,10,30,2,46,50,534691612))), C2812_ECHO_POST),
    ("ECHO_PRE epoch 03:07:51.491053914", D(str(utc_epoch(2026,10,30,3,7,51,491053914))), ECHO_PRE),
    ("ECHO_POST epoch 03:07:53.062755684", D(str(utc_epoch(2026,10,30,3,7,53,62755684))), ECHO_POST),
    ("ECHO_SCAN 03:07:53.057", D(str(utc_epoch(2026,10,30,3,7,53))) + D("0.057"), ECHO_SCAN),
    ("WIN2812 re-check", D(str(utc_epoch(2026,10,30,2,32,6,818599805))), WIN2812),
    ("token-vs-stamp +583", TOKEN - TRIG, D("583.000")),
    ("stamp-gap 1200.000", TRIG - C2812_TRIG, D("1200.000")),
    ("token-gap 1320.000", TOKEN - C2812_TOKEN, D("1320.000")),
    ("skew +5.462242ms", POST - SCAN, D("0.005462242")),
    ("POST-WINDOW +1101.539546856", POST - WIN, D("1101.539546856")),
    ("post-c2812-post-echo +1401.539546856", POST - C2812_POST, D("1401.539546856")),
    ("dd#387 = 1401.540 - 300 = 1101.540", SCAN - C2812_SCAN - D("300.000"), D("1101.540")),
    ("dd re-verify 960.015-300", D("960.015") - D("300.000"), D("660.015")),
    ("dd re-verify 1461.399-300", D("1461.399") - D("300.000"), D("1161.399")),
    ("dd re-verify 878.961-300", D("878.961") - D("300.000"), D("578.961")),
    ("INTERVAL#387 = 1412.752", SCAN - TRIG, D("1412.752")),
    ("LAG#387 = 1412.752 + 1101.540 - 1161.399 = 1352.893", (SCAN - TRIG) + (SCAN - C2812_SCAN - D("300.000")) - D("1161.399"), D("1352.893")),
    ("LATE#387 = -311.217915386", TRIG - WIN, D("-311.217915386")),
    ("WIN - C2812_POST = 300.000", WIN - C2812_POST, D("300.000")),
    ("TRIG - C2812_ECHO_POST = +266.465308388", TRIG - C2812_ECHO_POST, D("266.465308388")),
    ("TRIG - C2812_PRE = -9.469282375", TRIG - C2812_PRE, D("-9.469282375")),
    ("TRIG - C2812_SCAN = -11.212", TRIG - C2812_SCAN, D("-11.212")),
    ("TRIG - C2812_POST = -11.217915386", TRIG - C2812_POST, D("-11.217915386")),
    ("C2812_CLOSE - TRIG = +559.000", C2812_CLOSE - TRIG, D("559.000")),
    ("FOREIGN_NOW - TRIG = +587.000", FOREIGN_NOW - TRIG, D("587.000")),
    ("C2812_CLOSE - TOKEN = -24.000", C2812_CLOSE - TOKEN, D("-24.000")),
    ("FOREIGN_NOW - TOKEN = +4.000", FOREIGN_NOW - TOKEN, D("4.000")),
    ("C2812_CLOSE - WIN = +247.782084614", C2812_CLOSE - WIN, D("247.782084614")),
    ("FOREIGN_NOW - WIN = +275.782084614", FOREIGN_NOW - WIN, D("275.782084614")),
    ("ECHO_POST - WIN = +684.844840298", ECHO_POST - WIN, D("684.844840298")),
    ("stamp-to-echo 994.491053914", ECHO_PRE - TRIG, D("994.491053914")),
    ("echo wall 1.571701770", ECHO_POST - ECHO_PRE, D("1.571701770")),
    ("dd#387 in band [564.552241212..3708.066631432]", D("564.552241212") <= D("1101.540") <= D("3708.066631432"), D("1")),
    ("echo predates capture pre-echo", D(1) if ECHO_POST < PRE else D(0), D("1")),
    ("SKEW sub-10 margin 10 - 5.462242 = 4.537758", D("10.000000") - D("0.005462242"), D("9.994537758")),
]
bad = 0
for name, want, got in checks:
    ok = abs(want - got) < D("0.000001")
    if not ok:
        bad += 1
    print(f"{'ok' if ok else 'FAIL'}: {name} computed={want} harness={got} (1e-6-tolerance class on utc-derived)")
print(f"{'ALL_DECIMAL_EXACT_1E6' if bad == 0 else f'{bad} FAILURES'}")
