#!/bin/bash
# Instrumented capture harness for cycle c2623 (DRIFT-#44 verification-5 candidate)
# STAGING LAW HELD twelve consecutive cycles (c2612..c2623) — staged pre-POST this cycle,
# NO stray. The trigger template's step-2 curl is satisfied BY the captured-class POST
# itself (curl -o/-w) with display via python3 -m json.tool on the captured bytes
# afterward; the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 05:44:49 +08, keyed 05:44:44 (the 600-basis backup
# candidate CLAIMED on arrival — the dispatched 300-basis 05:39:44 candidate was NEVER
# claimed: zero c2623 artifacts at dispatch and no c2623 worklog entry — GHOST booking
# +1, ledger 34 -> 35); trigger-to-trigger 600.000s EXACT by stamp and by candidate
# (05:34:49 -> 05:44:49 / 05:34:44 -> 05:44:44 — the first clean 600-basis fold of the
# post-restart run; c2622's fold carried +1s); execution ~16 min past the stamp —
# queueing latency booked on the dd queue (dd#197).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2623_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2623.json"

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
