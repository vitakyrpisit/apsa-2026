#!/bin/bash
# Instrumented capture harness for cycle c2655 (DRIFT-#45 verification-33 candidate,
# post-LOSS-#6 ninth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2655 opens 10:56:42.593064427 +08; keyed candidate 10:59:44 (8400-basis,
# epoch 1793069984, first in-window rung) — deferred-servicing if the stamp lands after the
# rung (c2649..c2654 precedent, NORMAL), EARLY-claim if before (c2649 precedent, also
# NORMAL); the 10:54:44 8100b rung passed unclaimed (no sibling keyed 10:54:4x — ghost
# candidate #62); the 11:04:44 8700b rung stamp-governed (live for later cycles).
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2655_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2655.json"

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
