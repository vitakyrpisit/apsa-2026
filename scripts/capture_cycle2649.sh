#!/bin/bash
# Instrumented capture harness for cycle c2649 (DRIFT-#45 verification-27 candidate,
# post-LOSS-#6 third carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2649 opens 09:50:06.986880081 +08; keyed candidate 09:54:44 (4500-basis,
# first in-window rung) — EARLY-claim shape if the stamp precedes the rung; the 09:49:44
# 4200b rung passed unclaimed (ghost #55); rungs 09:59:44+ stamp-governed.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2649_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2649.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (single) ==="
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
