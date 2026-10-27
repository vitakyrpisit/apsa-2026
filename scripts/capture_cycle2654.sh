#!/bin/bash
# Instrumented capture harness for cycle c2654 (DRIFT-#45 verification-32 candidate,
# post-LOSS-#6 eighth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2654 opens 10:45:49.712362776 +08; keyed candidate 10:49:44 (7800-basis,
# epoch 1793069384, first in-window rung) — EARLY-claim shape expected if the stamp lands
# before the rung (c2649 precedent, NORMAL), deferred-servicing if after (c2649..c2653
# precedent, also NORMAL); the 10:44:44 7500b rung passed unclaimed at c2654 arrival
# (pre-window-2654, no sibling keyed 10:44:4x — ghost candidate #61); the 10:54:44
# 8100b rung stamp-governed (live for later cycles).
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2654_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2654.json"

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
