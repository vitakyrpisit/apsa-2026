#!/bin/bash
# Instrumented capture harness for cycle c2622 (DRIFT-#44 verification-4 candidate)
# STAGING LAW HELD eleven consecutive cycles (c2612..c2622) — staged pre-POST this cycle,
# NO stray. The trigger template's step-2 curl is satisfied BY the captured-class POST
# itself (curl -o/-w) with display via python3 -m json.tool on the captured bytes
# afterward; the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 05:34:49 +08, keyed 05:34:44 (the 600-basis backup
# candidate CLAIMED on arrival — the dispatched 300-basis 05:29:44 candidate was NEVER
# claimed: zero c2622 artifacts at dispatch and no c2622 worklog entry — GHOST booking
# +1, ledger 33 -> 34); trigger-to-trigger 601.000s (05:24:48 -> 05:34:49, 600-basis
# fold +1s — the 300.000s-exact run BREAKS at nine); execution ~11 min past the stamp —
# queueing latency booked on the dd queue (dd#196).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2622_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2622.json"

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
