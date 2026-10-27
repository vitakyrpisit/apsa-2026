#!/bin/bash
# Instrumented capture harness for cycle c2663 (DRIFT-#45 verification-41 candidate,
# post-LOSS-#6 seventeenth carry cycle, GAP-DISPATCH class). Mandatory order:
# pre-echo -> curl -o/-w -> post-echo. SINGLE POST. Claim classification:
# PENDING-CLASSIFICATION (no pre-written claim state).
# GAP-DISPATCH: trigger stamped 2026-10-28 00:00:09 +08 (epoch 1793116809.000) —
# 41413.000s by stamp after the c2662-serviced trigger (2026-10-27 12:29:56); 138
# slots passed unserviced during the operator-pause window. The c2662 Next-block
# keyed candidate (12:49:44 15000b, epoch 1793076584) and the live rungs 12:54:44
# (15300b, epoch 1793076884) / 12:59:44 (15600b, epoch 1793077184) are ALL elapsed
# at this stamp — bookable as ghosts #77/#78/#79 per the stamp-governs law (c2651
# precedent class), sibling-entry checks apply. The market state after the 11.5h
# gap is UNOBSERVED — post-capture scan data re-keys the live rung set; any honest
# (free OR paid) emergence = DRIFT-#46 two-pass; paid emergence = GOLD path
# (scam-check -> EV -> bounty <= $5 first-job policy) per protocol.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2663_raw.json"
OUT_PRETTY="/home/z/my-project/scripts/scan_cycle2663.json"

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
