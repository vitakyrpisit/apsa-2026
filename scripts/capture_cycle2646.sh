#!/bin/bash
# Instrumented capture harness for cycle c2646 (DRIFT-#45 verification-24 candidate, post-LOSS-#6 recon cycle)
# Mandatory order: pre-echo -> curl -o/-w -> post-echo. SINGLE POST.
# LOSS EVENT #6 declared on arrival: disk rolled back to the c2576 exit state (worklog 8095 lines,
# HEAD 0159607); the c2577..c2645 ledger and scripts corpus are LOST (context-carried).
# Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2646_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2646.json"

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
