#!/bin/bash
# Instrumented capture harness for cycle c2658 (DRIFT-#45 verification-36 candidate,
# post-LOSS-#6 twelfth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2658 opens 11:39:46.095306980 +08; keyed candidate 11:44:44 (11100-basis,
# epoch 1793072684, first in-window rung) — deferred-servicing shape (rung elapsed at
# staging, stamp ~400s after the rung — NORMAL per c2649..c2657 precedent), EARLY-claim
# impossible (clock past the rung); the 11:39:44 10800b rung passed unclaimed (no sibling
# keyed 11:39:4x — ghost candidate #68); the 11:49:44 11400b rung elapsed at staging
# (ghost candidate #69, c2651 precedent class — stamp governs); the 11:54:44 11700b rung
# live for later cycles (WOBBLE RISK: if capture lands past 11:54:44 the stamp governs).
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2658_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2658.json"

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
