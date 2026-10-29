#!/bin/bash
# Official capture harness for cycle 2779 (Job ID 446189) — SINGLE-POST law.
# window-2779 open epoch 1793306581.565781844 (= the c2778 post-echo
# 1793306281.565781844 + 300.000 server contract; on-disk prophecy from the
# c2778 Next-block. NOTE: the c2778 Next-block's ISO rendering "20:49:41..."
# misrenders the EPOCH by +380.000s — the EPOCH governs; the correct ISO is
# 20:43:01.565781844 +0000 = 04:43:01.565781844 +08).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo. TEE-mode log.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2779_raw.json"
OUT_LOG="/home/z/my-project/scripts/capture_cycle2779.log"

echo "window-2779 open 1793306581.565781844 (c2778 Next-block prophecy, EPOCH-governs)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "raw_bytes=$(wc -c < "$OUT_RAW")" | tee -a "$OUT_LOG"
echo "raw_head=$(head -c 120 "$OUT_RAW")" | tee -a "$OUT_LOG"
