#!/bin/bash
# Instrumented capture harness for cycle c2631 (DRIFT-#45 verification-9 candidate)
# STAGING ORDER LAW: capture_cycle2631.sh + rebadge_2631.py staged pre-POST BEFORE any
# scan POST (targeting the TWENTIETH consecutive staged cycle, c2612..c2631). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note: trigger stamp 06:54:50 +08, keyed 06:54:44 — the 600-basis BACKUP
# candidate CLAIMED on arrival (the dispatched 300-basis PRIMARY 06:49:44 elapsed
# UNDELIVERED — ghost #41 booked, ledger 40 -> 41; zero c2631 artifacts existed at
# dispatch — arrival-guard CLEAN). Trigger-to-trigger 600.000s EXACT both by stamp
# (06:44:50 -> 06:54:50) and by candidate (06:44:44 -> 06:54:44) — the 300-basis
# exact run BREAKS at 4 members (c2627->c2628->c2629->c2630); the 600-basis exact
# run RESTARTS at member 1; wobble +6.000s — +6 series member 8 (members 1-7 =
# c2624..c2630); the PRIMARY claim run (c2628->c2629->c2630) BREAKS — the
# backup-keyed claim run RESTARTS at member 1; queueing latency booked on dd#205.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2631_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2631.json"

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
