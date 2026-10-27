#!/bin/bash
# Instrumented capture harness for cycle c2662 (DRIFT-#45 verification-40 candidate,
# post-LOSS-#6 sixteenth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2662 opened 12:39:10.725569731 +08 (post-echo c2661 + 300.000 server
# contract); keyed candidate 12:39:44 (14400-basis, epoch 1793075984, first in-window rung,
# 33.274430269s in-window) — trigger stamped 12:29:56 PRE-rung: EARLY-claim shape if capture
# lands pre-rung (NORMAL per c2649..c2661 precedent, stamp governs); WOBBLE RISK: if capture
# lands past 12:39:44 the stamp governs — c2651 precedent class, elapsed non-candidate rungs
# booked at stamp (ghost #76 candidate) and the 12:44:44 14700b (epoch 1793076284) becomes
# the claimed rung; the 12:49:44 15000b (epoch 1793076584) live for later cycles. The
# 12:34:44 14100b rung was claimed by c2661 (EARLY, NORMAL); ghost #75 (12:29:44 13800b)
# carried booked.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2662_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2662.json"

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
