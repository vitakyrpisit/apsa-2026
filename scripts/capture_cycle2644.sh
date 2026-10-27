#!/bin/bash
# Instrumented capture harness for cycle c2644 (DRIFT-#45 verification-22 candidate)
# STAGING ORDER LAW: capture_cycle2644.sh + rebadge_2644.py staged pre-POST BEFORE any
# scan POST (targeting the THIRTY-THIRD consecutive staged cycle, c2612..c2644). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note (PENDING-CLASSIFICATION — do NOT pre-write claim status; classify from
# the server response after the POST): trigger stamp 08:09:52 +08, keyed 08:09:44 —
# the dispatched 300-basis PRIMARY candidate. EXECUTION DELAY ANOMALY: this instance
# resumed ~10 minutes after the trigger stamp; the 08:09:44 PRIMARY slot AND the
# 08:14:44 backup slot elapsed with no POST (ghost bookings PENDING, ledger expected
# 43 -> 45); the latest scheduled 300-basis candidate at POST time is 08:19:44
# (elapsed ~40-50s at expected POST) with 08:24:44 next. Post-POST classification
# MUST be derived from the server response (scanned_at / next_scan window), reported
# honestly per Protocol v5.0. Trigger-to-trigger stamp delta 08:04:51 -> 08:09:52 =
# 501s (NOT 300-exact, NOT 600-exact — cadence runs terminate; re-derive after POST).
# Queueing latency to be booked on dd#218 (expected era-high ~630s vs prior dd#214
# 527.467960158s — classify after actual measurement).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2644_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2644.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (official captured-class; single-POST law carries — cycle totals 1 POST) ==="
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
