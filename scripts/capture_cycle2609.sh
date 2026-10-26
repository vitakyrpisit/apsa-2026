#!/bin/bash
# Instrumented capture harness for cycle c2609 (DRIFT-#42 verification-4 candidate)
# STAGED BEFORE THE OFFICIAL SCAN POST (captured-class standard; single-POST law carries
# — c2604..c2608 clean at 1 POST each; NO stray POST this cycle).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# The trigger template's curl step is satisfied BY this captured-class POST itself;
# display happens via python3 -m json.tool on the captured bytes afterward.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2609_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2609.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (official; cycle totals 1 POST — single-POST law carries) ==="
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
