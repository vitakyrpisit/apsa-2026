#!/bin/bash
# Instrumented capture harness for cycle c2633 (DRIFT-#45 verification-11 candidate)
# STAGING ORDER LAW: capture_cycle2633.sh + rebadge_2633.py staged pre-POST BEFORE any
# scan POST (targeting the TWENTY-SECOND consecutive staged cycle, c2612..c2633). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 07:04:50 +08, keyed 07:04:44 — the dispatched 300-basis
# PRIMARY candidate CLAIMED on arrival — NORMAL, no ghost booking (zero intervening
# slots since 06:59:44; the ledger HOLDS at 41). Trigger-to-trigger 300.000s EXACT
# both by stamp (06:59:50 -> 07:04:50) and by candidate (06:59:44 -> 07:04:44) — the
# 300-basis exact run EXTENDS 1 -> 2; wobble +6.000s — +6 series member 10 (members
# 1-9 = c2624..c2632); the PRIMARY claim run EXTENDS 1 -> 2 (c2632->c2633); queueing
# latency booked on dd#207.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2633_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2633.json"

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
