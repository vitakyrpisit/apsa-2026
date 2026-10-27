#!/bin/bash
# Instrumented capture harness for cycle c2648 (DRIFT-#45 verification-26 candidate,
# post-LOSS-#6 second carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2648 opens 09:39:14.242813124 +08; keyed candidate 09:39:44 (3600-basis,
# first in-window rung) deferred-servicing claim; the 09:34:44 3300b rung passed unclaimed
# (ghost #53); rungs 09:44:44+ stamp-governed.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2648_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2648.json"

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
