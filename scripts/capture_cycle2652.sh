#!/bin/bash
# Instrumented capture harness for cycle c2652 (DRIFT-#45 verification-30 candidate,
# post-LOSS-#6 sixth carry cycle). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# SINGLE POST. Claim classification: PENDING-CLASSIFICATION (no pre-written claim state).
# Dispatch: window-2652 opens 10:27:58.783156199 +08; keyed candidate 10:29:44 (6600-basis,
# epoch 1793068184, first in-window rung) — deferred-servicing claim shape expected if the
# stamp lands after the rung (c2649/c2650/c2651 precedent, NORMAL), EARLY-claim if pre-rung
# (also NORMAL); the 10:24:44 6300b rung passed unclaimed at c2652 arrival (pre-window-2652,
# no sibling keyed 10:24:4x — ghost candidate #59); the 10:34:44 6900b rung stamp-governed
# (ghost candidate #60 if elapsed unclaimed at stamp); 10:39:44+ live for later cycles.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2652_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2652.json"

echo "=== PRE-ECHO ==="
date '+pre %H:%M:%S.%9N %z %a %b %d %Y (epoch %s.%9N)'

echo "=== SCAN POST (single) ==="
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
