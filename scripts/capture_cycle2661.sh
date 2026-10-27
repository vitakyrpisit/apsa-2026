#!/bin/bash
# Instrumented capture harness for cycle c2661 (DRIFT-#45 verification-39 candidate,
# post-LOSS-#6 fifteenth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2661 opens 12:31:56.309321373 +08; keyed candidate 12:34:44 (14100-basis,
# epoch 1793075684, first in-window rung) — EARLY-claim shape (trigger stamped 12:24:56,
# pre-rung — NORMAL per c2649..c2660 precedent, stamp governs); the 12:29:44 13800b rung
# passed unclaimed (no sibling keyed 12:29:4x — ghost candidate #75, booked per the c2660
# Next-block dispatch instruction); the 12:39:44 14400b rung (WOBBLE RISK: if capture lands
# past 12:39:44 the stamp governs — c2651 precedent class, elapsed non-candidate rungs
# booked at stamp); the 12:44:44 14700b rung live for later cycles.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2661_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2661.json"

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
