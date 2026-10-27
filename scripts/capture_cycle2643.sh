#!/bin/bash
# Instrumented capture harness for cycle c2643 (DRIFT-#45 verification-21 candidate)
# STAGING ORDER LAW: capture_cycle2643.sh + rebadge_2643.py staged pre-POST BEFORE any
# scan POST (targeting the THIRTY-SECOND consecutive staged cycle, c2612..c2643). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 08:04:51 +08, keyed 08:04:44 — the dispatched 300-basis
# PRIMARY candidate CLAIMED on arrival — NORMAL, no ghost booking (zero intervening
# scheduled candidates since 07:59:44; the ledger HOLDS at 43). Trigger-to-trigger
# 300.000s EXACT BOTH by stamp (07:59:51 -> 08:04:51) and by candidate
# (07:59:44 -> 08:04:44) — the 300-basis exact run EXTENDS member 2 -> 3 (both
# bases); wobble +7.000s — the +7 print EXTENDS member 9 -> 10 (c2634..c2643); the
# PRIMARY claim run EXTENDS member 3 -> 4 (c2640->c2641->c2642->c2643).
# Queueing latency booked on dd#217.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2643_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2643.json"

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
