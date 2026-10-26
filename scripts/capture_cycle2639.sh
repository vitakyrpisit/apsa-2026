#!/bin/bash
# Instrumented capture harness for cycle c2639 (DRIFT-#45 verification-17 candidate)
# STAGING ORDER LAW: capture_cycle2639.sh + rebadge_2639.py staged pre-POST BEFORE any
# scan POST (targeting the TWENTY-EIGHTH consecutive staged cycle, c2612..c2639). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 07:39:51 +08, keyed 07:39:44 — the dispatched 300-basis
# PRIMARY candidate CLAIMED on arrival — NORMAL, no ghost booking (zero intervening
# scheduled candidates since 07:34:44; the ledger HOLDS at 42). Trigger-to-trigger
# targets 300.000s EXACT both by stamp (07:34:51 -> 07:39:51) and by candidate
# (07:34:44 -> 07:39:44) — the 300-basis exact run targets EXTENSION member 4 -> 5;
# wobble +7.000s targets EXTENSION member 5 -> 6 (c2634..c2639); the PRIMARY
# claim run targets EXTENSION member 4 -> 5 (c2635..c2639).
# Queueing latency booked on dd#213.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2639_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2639.json"

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
