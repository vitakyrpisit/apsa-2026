#!/bin/bash
# Instrumented capture harness for cycle c2627 (DRIFT-#45 verification-5 candidate)
# STAGING ORDER LAW: capture_cycle2627.sh + rebadge_2627.py staged pre-POST BEFORE any
# scan POST (targeting the SIXTEENTH consecutive staged cycle, c2612..c2627). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 06:29:50 +08, keyed 06:29:44 — the Next-block-dispatched
# 600-basis backup CLAIMED as PRIMARY on arrival under the latest-elapsed-candidate law
# after the intervening 300-basis slot 06:24:44 elapsed UNCLAIMED -> booked as GHOST
# (ledger 39 -> 40). Trigger-to-trigger 300.000s EXACT both by stamp (06:19:50 ->
# 06:29:50) and by candidate (06:19:44 -> 06:29:44) — the 300-basis exact run RESTARTS
# at 1 after the c2626 600-basis 2-slot fold; wobble +6.000s — +6 series member 4
# (members 1-3 = c2624/c2625/c2626); queueing latency booked on the dd queue (dd#201).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2627_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2627.json"

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
