#!/bin/bash
# Instrumented capture harness for cycle c2659 (DRIFT-#45 verification-37 candidate,
# post-LOSS-#6 thirteenth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2659 opens 11:58:20.420285195 +08; keyed candidate 11:59:44 (12000-basis,
# epoch 1793073584, first in-window rung) — EARLY-claim shape (trigger stamped 11:49:56,
# pre-rung — NORMAL per c2649..c2658 precedent, stamp governs); the 11:54:44 11700b rung
# passed unclaimed (no sibling keyed 11:54:4x — ghost candidate #70, booked per the c2658
# Next-block dispatch instruction); the 12:04:44 12300b rung (WOBBLE RISK: if capture lands
# past 12:04:44 the stamp governs — c2651 precedent class, elapsed non-candidate rungs
# booked at stamp); the 12:09:44 12600b rung live for later cycles.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2659_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2659.json"

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
