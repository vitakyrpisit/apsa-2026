#!/bin/bash
# Instrumented capture harness for cycle c2646 (DRIFT-#45 verification-24 candidate)
# STAGING ORDER LAW: capture_cycle2646.sh + rebadge_2646.py staged pre-POST BEFORE any
# scan POST (targeting the THIRTY-FIFTH consecutive staged cycle, c2612..c2646). The
# trigger template's step-2 curl is satisfied BY the captured-class POST itself
# (curl -o/-w) with display via python3 -m json.tool on the captured bytes afterward;
# the literal template curl is NOT executed.
# Single-POST law carries: cycle totals exactly 1 POST.
# Arrival note (PENDING-CLASSIFICATION — do NOT pre-write claim status; classify from
# the server response after the POST): trigger stamp 08:29:53 +08, keyed 08:39:44 —
# the dispatched 300-basis PRIMARY candidate (per the c2645 Next-block; 08:34:44 is
# UNREACHABLE, preceding window-2646 08:37:57.842165399 by 193.198165399s).
# NEGATIVE WOBBLE print #2: trigger 08:29:53 - keyed 08:39:44 = -591.000s (the trigger
# arrived BEFORE the keyed slot for the SECOND consecutive cycle; -292.000s run
# ENDS at member 1 (c2645), a -591.000s print starts member 1).
# Trigger-to-trigger 08:24:52 -> 08:29:53 = 301.000s (NOT 300-exact) — the 900-basis
# exact run ENDS at member 1 (c2644->c2645).
# EXECUTION PROFILE: instance resumed ~5.2 min past the trigger (third consecutive
# delay cycle) BUT the keyed 08:39:44 slot had NOT elapsed at staging time — the
# harness INTENTIONALLY WAITS and POSTs at keyed+~2s for a clean PRIMARY claim
# (planned pre-echo 08:39:45-46). This wait is a DELIBERATE claim-timing measure,
# NOT queueing latency: dd#220 is expected SMALL (keyed-to-pre-echo ~2s) — a
# first-in-era clean claim after three delay cycles if it lands as planned.
# Post-POST classification MUST be derived from the server response (scanned_at /
# next_scan window), reported honestly per Protocol v5.0.
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2646_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2646.json"

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
