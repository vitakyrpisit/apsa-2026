#!/bin/bash
# Instrumented capture harness for cycle c2603 (DRIFT-#41 verification-10 candidate)
# STAGED BEFORE THE OFFICIAL SCAN POST (captured-class standard; staging streak carries
# at 10 from c2602). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# DEVIATION DISCLOSURE (c2603): ONE stray UNCAPTURED scan POST was executed earlier this
# cycle (03:37:43 +08 wall, second-resolution pre-mark; scanned_at 2026-10-26T19:37:45.350Z,
# scan_duration_ms=1998, five-tuple (23,0,2,18,3) — corroborating print, NOT validator
# evidence, NOT in any queue). This cycle therefore totals TWO POSTs (1 stray + 1 official):
# the single-POST law is BROKEN at c2603 and the single-POST streak CLOSES at 2602 cycles.
# The official capture below remains held to the full captured-class standard.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2603_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2603.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (official; cycle totals 2 POSTs — deviation logged) ==="
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
