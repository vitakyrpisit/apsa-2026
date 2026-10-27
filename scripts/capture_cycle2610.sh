#!/bin/bash
# Instrumented capture harness for cycle c2610 (DRIFT-#42 verification-5 candidate)
# STRAY DISCLOSURE (honest report): the trigger template's step-2 curl WAS executed
# literally pre-stage this cycle — a naked, uncaptured POST (output observed in-session
# ONLY, never captured to disk; server scanned_at 2026-10-26T20:21:39.834Z,
# scan_duration_ms=1730, five-tuple (22,0,1,18,3), taskbounty all-zero, next_scan=300).
# STAGING ORDER LAW BROKE at six consecutive clean cycles; single-POST law BROKEN —
# the captured-class POST below is the OFFICIAL cycle POST and the cycle totals
# 2 POSTs (first stray since the c2603 corrective). REARM stance for c2611.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2610_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2610.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (official captured-class; cycle totals 2 POSTs — stray booked) ==="
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
