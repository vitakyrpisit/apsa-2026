#!/bin/bash
# Instrumented capture harness for cycle c2653 (DRIFT-#45 verification-31 candidate,
# post-LOSS-#6 seventh carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2653 opens 10:38:52.562005109 +08; keyed candidate 10:39:44 (7200-basis,
# epoch 1793068784, first in-window rung) — deferred-servicing claim shape expected if the
# stamp lands after the rung (c2649/c2650/c2651/c2652 precedent, NORMAL), EARLY-claim if
# pre-rung (also NORMAL, c2649 precedent); the 10:34:44 6900b rung passed unclaimed at c2653
# arrival (pre-window-2653, no sibling keyed 10:34:4x — ghost candidate #60); the 10:44:44
# 7500b rung stamp-governed (ghost candidate #61 if elapsed unclaimed at stamp); 10:49:44+
# live for later cycles.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2653_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2653.json"

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
