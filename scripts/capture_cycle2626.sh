#!/bin/bash
# Instrumented capture harness for cycle c2626 (DRIFT-#45 verification-4 candidate)
# STAGING ORDER LAW: capture_cycle2626.sh + rebadge_2626.py staged pre-POST BEFORE any
# scan POST (targeting the FIFTEENTH consecutive staged cycle, c2612..c2626). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 06:19:50 +08, keyed 06:19:44 — the latest elapsed
# candidate CLAIMED on arrival (NORMAL, no ghost on the claim); the intervening
# 300-basis slot 06:14:44 elapsed UNCLAIMED -> booked as GHOST (ledger 38 -> 39).
# Trigger-to-trigger 600.000s EXACT both by stamp (06:09:50 -> 06:19:50) and by
# candidate (06:09:44 -> 06:19:44) — a 600-basis 2-slot fold (the 300-basis exact
# run breaks after one member at c2625); wobble +6.000s — +6 series member 3
# (members 1-2 = c2624/c2625); queueing latency booked on the dd queue (dd#200).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2626_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2626.json"

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
