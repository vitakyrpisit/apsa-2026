#!/bin/bash
# Instrumented capture harness for cycle c2645 (DRIFT-#45 verification-23 candidate)
# STAGING ORDER LAW: capture_cycle2645.sh + rebadge_2645.py staged pre-POST BEFORE any
# scan POST (targeting the THIRTY-FOURTH consecutive staged cycle, c2612..c2645). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note (PENDING-CLASSIFICATION — do NOT pre-write claim status; classify from
# the server response after the POST): trigger stamp 08:24:52 +08, keyed 08:29:44 —
# the dispatched 300-basis PRIMARY candidate (per the c2644 Next-block; 08:24:44 is
# UNREACHABLE, preceding window-2645 08:28:32.244336965 by 228.244336965s).
# NEGATIVE WOBBLE print: trigger 08:24:52 - keyed 08:29:44 = -292.000s (the trigger
# arrived BEFORE the keyed slot — dispatch drift; first negative print of the tracked
# era, member 1). EXECUTION DELAY ANOMALY (second consecutive): instance resumed ~6min
# past the trigger; the 08:29:44 keyed slot elapsed unclaimed (GHOST #47 PENDING,
# ledger expected 46 -> 47); the POST is expected OFF-GRID in the 08:29:44..08:34:44
# gap. Trigger-to-trigger 08:09:52 -> 08:24:52 = 900.000s EXACT (3x300) — a 900-basis
# exact run starts member 1 (stamp basis). Post-POST classification MUST be derived
# from the server response (scanned_at / next_scan window), reported honestly per
# Protocol v5.0. Queueing latency to be booked on dd#219 (keyed-candidate convention).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2645_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2645.json"

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
