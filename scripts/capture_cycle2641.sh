#!/bin/bash
# Instrumented capture harness for cycle c2641 (DRIFT-#45 verification-19 candidate)
# STAGING ORDER LAW: capture_cycle2641.sh + rebadge_2641.py staged pre-POST BEFORE any
# scan POST (targeting the THIRTIETH consecutive staged cycle, c2612..c2641). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 07:54:51 +08, keyed 07:54:44 — the dispatched 300-basis
# PRIMARY candidate CLAIMED on arrival — NORMAL, no ghost booking (zero intervening
# scheduled candidates since 07:49:44; the ledger HOLDS at 43). Trigger-to-trigger
# 300.000s EXACT BOTH by stamp (07:49:51 -> 07:54:51) and by candidate
# (07:49:44 -> 07:54:44) — the 600-basis exact run ENDS at member 1 (both bases, the
# c2640 print), a NEW 300-basis exact run STARTS at member 1 (both bases); wobble
# +7.000s — the +7 print EXTENDS member 7 -> 8 (c2634..c2641); the PRIMARY claim run
# EXTENDS member 1 -> 2 (c2640->c2641).
# Queueing latency booked on dd#215.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2641_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2641.json"

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
