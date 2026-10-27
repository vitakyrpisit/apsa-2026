#!/bin/bash
# Instrumented capture harness for cycle c2624 (DRIFT-#45 verification-2 candidate)
# STAGING LAW HELD thirteen consecutive cycles (c2612..c2624) — staged pre-POST this
# cycle, NO stray. The trigger template's step-2 curl is satisfied BY the
# captured-class POST itself (curl -o/-w) with display via python3 -m json.tool on
# the captured bytes afterward; the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 06:04:50 +08, keyed 06:04:44 (the arriving candidate
# CLAIMED on arrival — the dispatched 300-basis 05:49:44 primary AND both
# intervening scheduled candidates 05:54:44 / 05:59:44 were NEVER claimed: zero
# c2624 artifacts at dispatch and no c2624 worklog entry — GHOST bookings +3,
# ledger 35 -> 38); trigger-to-trigger 1201.000s by stamp (05:44:49 -> 06:04:50) /
# 1200.000s EXACT by candidate (05:44:44 -> 06:04:44) — the FIRST 1200-basis print
# of the post-restart run (a 3-slot fold, NOT a clean 600-basis pair); execution
# ~11 min past the stamp — queueing latency booked on the dd queue (dd#198);
# wobble +6.000s — NEW +6 series member 1 (the +5 series ended at member 2).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2624_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2624.json"

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
