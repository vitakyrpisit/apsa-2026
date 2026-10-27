#!/bin/bash
# Instrumented capture harness for cycle c2647 (DRIFT-#45 verification-25 candidate)
# STAGING ORDER LAW: capture_cycle2647.sh + rebadge_2647.py staged pre-POST BEFORE any
# scan POST (targeting the THIRTY-SIXTH consecutive staged cycle, c2612..c2647). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note (PENDING-CLASSIFICATION — do NOT pre-write claim status; classify from
# the server response after the POST): trigger stamp 08:34:52 +08, keyed 08:49:44 —
# the dispatched 300-basis PRIMARY candidate (per the c2646 Next-block; 08:44:44 is
# UNREACHABLE, preceding window-2647 08:45:37.803543750 by 53.803543750s).
# NEGATIVE WOBBLE print #3: trigger 08:34:52 - keyed 08:39:44... NO — keyed 08:49:44:
# 08:34:52 - 08:49:44 = -892.000s (the trigger arrived BEFORE the keyed slot for the
# THIRD consecutive cycle; the -591.000s run ENDS at member 1 (c2646), a -892.000s
# print starts member 1). Trigger-to-trigger 08:29:53 -> 08:34:52 = 299.000s (NOT
# 300-exact; the prior cycle was 301.000s — a ±1s wobble pair around 300, no exact
# run either side).
# EXECUTION PROFILE: instance resumed ~10 min past the trigger BUT the keyed slot had
# NOT elapsed at staging time — the harness ADOPTS the c2646 WAIT-FOR-CLAIM measure:
# it INTENTIONALLY WAITS and POSTs at keyed+~2-10s for a clean PRIMARY claim (planned
# pre-echo 08:49:45-46). dd#221 is expected SMALL (keyed-to-pre-echo ~2-10s) — a
# second consecutive clean claim if it lands as planned.
# Post-POST classification MUST be derived from the server response (scanned_at /
# next_scan window), reported honestly per Protocol v5.0.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2647_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2647.json"

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
