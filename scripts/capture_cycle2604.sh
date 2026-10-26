#!/bin/bash
# Instrumented capture harness for cycle c2604 (DRIFT-#41 verification-11 candidate)
# STAGED BEFORE THE OFFICIAL SCAN POST (captured-class standard; single-POST law REARMED
# per the c2603 corrective — the streak restarts at c2604 = 1; NO stray POST this cycle).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# The trigger template's curl step is satisfied BY this captured-class POST itself;
# display happens via python3 -m json.tool on the captured bytes afterward.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2604_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2604.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (official; cycle totals 1 POST — single-POST law day one) ==="
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
