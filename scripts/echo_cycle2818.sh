#!/bin/bash
# Loop echo #539 for cycle 2818 (Job ID 446189) — the standing echo prescription.
# window-2818 open epoch 1793334401.674751215 (c2817 Next-block prophecy,
# EPOCH-governs). Mandatory order: pre-echo -> curl -o/-w -> post-echo.
# Honest note: this echo lands MID-SESSION (the session opened with the
# state-verification batch — the first-command prescription slips a TWENTY-SIXTH
# consecutive cycle); the echo-then-capture order class expected to extend m13.
set -u
OUT_LOG="/home/z/my-project/scripts/echo_cycle2818.log"
OUT_RAW="/home/z/my-project/scripts/echo_cycle2818_raw.json"

echo "window-2818 open 1793334401.674751215 (c2817 Next-block prophecy, EPOCH-governs)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "echo_scanned_at=$(python3 -c "import json;print(json.load(open('$OUT_RAW')).get('scanned_at'))" 2>/dev/null || echo PARSE_FAIL)" | tee -a "$OUT_LOG"
echo "server_scan_duration_ms=$(python3 -c "import json;print(json.load(open('$OUT_RAW')).get('scan_duration_ms'))" 2>/dev/null || echo PARSE_FAIL)" | tee -a "$OUT_LOG"
