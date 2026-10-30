#!/bin/bash
# Loop echo #541 for cycle 2820 (Job ID 446189) — the standing echo prescription.
# window-2820 open epoch 1793336056.357947395 (c2819 Next-block prophecy,
# EPOCH-governs: the c2819 capture post-echo 1793335756.357947395 + 300.000
# server contract = 04:54:16.357947395 +0000 = 12:54:16.357947395 +08).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# Honest note: this echo lands MID-SESSION (the session opened with the
# state-verification batch — the first-command prescription slips a TWENTY-EIGHTH
# consecutive cycle); the echo-then-capture order class expected to extend m13.
set -u
OUT_LOG="/home/z/my-project/scripts/echo_cycle2820.log"
OUT_RAW="/home/z/my-project/scripts/echo_cycle2820_raw.json"

echo "window-2820 open 1793336056.357947395 (c2819 Next-block prophecy, EPOCH-governs)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "echo_scanned_at=$(python3 -c "import json;print(json.load(open('$OUT_RAW')).get('scanned_at'))" 2>/dev/null || echo PARSE_FAIL)" | tee -a "$OUT_LOG"
echo "server_scan_duration_ms=$(python3 -c "import json;print(json.load(open('$OUT_RAW')).get('scan_duration_ms'))" 2>/dev/null || echo PARSE_FAIL)" | tee -a "$OUT_LOG"
