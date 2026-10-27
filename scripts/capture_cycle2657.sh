#!/bin/bash
# Instrumented capture harness for cycle c2657 (DRIFT-#45 verification-35 candidate,
# post-LOSS-#6 eleventh carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2657 opens 11:28:59.776259755 +08; keyed candidate 11:29:44 (10200-basis,
# epoch 1793071784, first in-window rung) — deferred-servicing if the stamp lands after the
# rung (c2649..c2656 precedent, NORMAL), EARLY-claim if before (also NORMAL); the 11:24:44
# 9900b rung passed unclaimed (no sibling keyed 11:24:4x — ghost candidate #66); the
# 11:34:44 10500b rung stamp-governed (c2651 precedent class — elapsed non-candidate rungs
# booked at stamp); the 11:39:44 10800b rung live for later cycles.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2657_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2657.json"

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
