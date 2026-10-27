#!/bin/bash
# Instrumented capture harness for cycle c2640 (DRIFT-#45 verification-18 candidate)
# STAGING ORDER LAW: capture_cycle2640.sh + rebadge_2640.py staged pre-POST BEFORE any
# scan POST (targeting the TWENTY-NINTH consecutive staged cycle, c2612..c2640). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 07:49:51 +08, keyed 07:49:44 — the 300-basis 07:44:44
# PRIMARY candidate elapsed UNCLAIMED (GHOST booking #43; the ledger HOLDS 42 -> 43,
# c2634 precedent) and the 600-basis 07:49:44 BACKUP candidate CLAIMED on arrival
# (c2631/c2634 precedent) — NORMAL handling, no unbooked ghost. Trigger-to-trigger
# 600.000s EXACT BOTH by stamp (07:39:51 -> 07:49:51) and by candidate
# (07:39:44 -> 07:49:44) — the 300-basis exact run ENDS at member 5 (both bases),
# a NEW 600-basis exact run STARTS at member 1 (both bases); wobble +7.000s —
# the +7 print EXTENDS member 6 -> 7 (c2634..c2640); the PRIMARY claim run RESTARTS
# at member 1 (the c2635..c2639 run ENDS at member 5 — the 07:44:44 slot ghosted).
# Queueing latency booked on dd#214.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2640_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2640.json"

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
