#!/bin/bash
# Instrumented capture harness for cycle c2656 (DRIFT-#45 verification-34 candidate,
# post-LOSS-#6 tenth carry cycle; LOSS EVENT #15 git-object-loss recovery class).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2656 opens 11:14:26.592362760 +08; keyed candidate 11:14:44 (9300-basis,
# epoch 1793070884, first in-window rung) — deferred-servicing if the stamp lands after the
# rung (c2649..c2655 precedent, NORMAL), EARLY-claim if before (also NORMAL); the 11:09:44
# 9000b rung passed unclaimed (no sibling keyed 11:09:4x — ghost candidate #64); the
# 11:19:44 9600b rung stamp-governed (c2651 precedent class — elapsed non-candidate rungs
# booked at stamp); the 11:24:44 9900b rung live for later cycles.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2656_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2656.json"

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
