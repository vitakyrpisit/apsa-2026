#!/bin/bash
# Instrumented capture harness for cycle c2635 (DRIFT-#45 verification-13 candidate)
# STAGING ORDER LAW: capture_cycle2635.sh + rebadge_2635.py staged pre-POST BEFORE any
# scan POST (targeting the TWENTY-FOURTH consecutive staged cycle, c2612..c2635). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 07:19:51 +08, keyed 07:19:44 — the dispatched 300-basis
# PRIMARY candidate CLAIMED on arrival — NORMAL, no ghost booking (zero intervening
# scheduled candidates since 07:14:44; the ledger HOLDS at 42). Trigger-to-trigger
# 300.000s EXACT both by stamp (07:14:51 -> 07:19:51) and by candidate
# (07:14:44 -> 07:19:44) — the 300-basis exact run RESTARTS at member 1 (the prior
# run broke at 2 when the 07:09:44 slot ghosted); wobble +7.000s — the +7 print
# EXTENDS member 1 -> 2 (c2634..c2635); the PRIMARY claim run RESTARTS at member 1
# (the backup-keyed claim run ENDED at member 1, c2634 alone). Queueing latency
# booked on dd#209.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2635_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2635.json"

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
