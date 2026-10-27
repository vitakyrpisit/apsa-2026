#!/bin/bash
# Instrumented capture harness for cycle c2651 (DRIFT-#45 verification-29 candidate,
# post-LOSS-#6 fifth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2651 opens 10:07:23.273331908 +08; keyed candidate 10:09:44 (5400-basis,
# epoch 1793066984, first in-window rung) — deferred-servicing claim shape expected if the
# stamp lands after the rung (c2649/c2650 precedent, NORMAL), EARLY-claim if pre-rung (also
# NORMAL); the 10:04:44 5100b rung passed unclaimed at c2651 arrival (pre-window-2651, no
# sibling keyed 10:04:4x — ghost candidate #56); the 10:14:44 5700b rung stamp-governed
# (ghost candidate #57 if elapsed unclaimed at stamp); 10:19:44+ live for later cycles.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2651_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2651.json"

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
