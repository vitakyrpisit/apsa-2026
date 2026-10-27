#!/bin/bash
# Instrumented capture harness for cycle c2666 (DRIFT-#45 verification-44 candidate,
# post-LOSS-#6 twentieth carry cycle). Mandatory order: pre-echo -> curl -o/-w ->
# post-echo. SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written
# claim state).
# NO KEYED CANDIDATE: the rung-ladder phase remains UNREKEYED post-gap (aggregate-only
# payload; SLOT WATCH VACUOUS per the c2665 Next-block - any rung bookkeeping resumes
# only from newly observed evidence, zero unverifiable claims). Window-2666 opened
# 00:26:36.046808581 +08 (post-echo c2665 + 300.000 server contract); trigger stamped
# 00:20:09 +08 - PRE-window arrival by 387.046808581s (stamp governs, no rung keying).
# Any honest (free OR paid) emergence = DRIFT-#46 two-pass; paid emergence = GOLD
# path (scam-check -> EV -> bounty <= $5 first-job policy) per protocol.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2666_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2666.json"

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
