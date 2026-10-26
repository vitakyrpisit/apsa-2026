#!/bin/bash
# Instrumented capture harness for cycle c2612 (DRIFT-#42 verification-7 candidate)
# DOUBLE-REARM HONORED: staged pre-POST this cycle — NO stray. The trigger template's
# step-2 curl is satisfied BY the captured-class POST itself (curl -o/-w) with display
# via python3 -m json.tool on the captured bytes afterward; the literal template curl
# is NOT executed. Single-POST law REARMS: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 04:39:48 +08, keyed 04:39:44 (the 900-basis rung —
# the dispatched 04:29:44 PRIMARY and the 04:34:44 backup passed unclaimed, two ghosts);
# execution ~8 min past the stamp — queueing latency booked on the dd queue.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2612_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2612.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (official captured-class; single-POST law REARMED — cycle totals 1 POST) ==="
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
