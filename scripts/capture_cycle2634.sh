#!/bin/bash
# Instrumented capture harness for cycle c2634 (DRIFT-#45 verification-12 candidate)
# STAGING ORDER LAW: capture_cycle2634.sh + rebadge_2634.py staged pre-POST BEFORE any
# scan POST (targeting the TWENTY-THIRD consecutive staged cycle, c2612..c2634). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 07:14:51 +08, keyed 07:14:44 — the dispatched 300-basis
# 07:09:44 PRIMARY elapsed unclaimed (ghost #42 booking; the ledger HOLDS 41 -> 42);
# the 600-basis 07:14:44 BACKUP candidate CLAIMED on arrival (c2631 precedent) —
# the PRIMARY claim run BREAKS at 2 (c2632->c2633); the backup-keyed claim run
# RESTARTS at member 1. Wobble +7.000s — the +6.000s series ENDS at 10 members
# (c2624..c2633), this is a +7 print (member 1). Trigger-to-trigger 600.000s EXACT
# by candidate (07:04:44 -> 07:14:44), 601.000s by stamp (07:04:50 -> 07:14:51) —
# the 300-basis exact run BREAKS at 2 (the 07:09:44 slot ghosted). Queueing latency
# booked on dd#208.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2634_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2634.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (official captured-class; single-POST law carries — cycle totals 1 POST) ==="
curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" \
  -w 'http=%{http_code} time_total=%{time_total}s size_download=%{size_download}B\n'

CURL_RC=$?
echo "curl_rc=$CURL_RC"

echo "=== POST-ECHO ==="
date '+post %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

if [ $CURL_RC -ne 0 ]; then
  echo "HARNESS ABORT: curl failed rc=$CURL_RC"
  exit 1
fi

echo "=== RAW BYTES ==="
wc -c "$OUT_RAW"

echo "=== PRETTY ==="
python3 -m json.tool "$OUT_RAW" > "$OUT_PRETTY" && echo "pretty written: $OUT_PRETTY ($(wc -c < "$OUT_PRETTY")B)"
