#!/bin/bash
# Official capture harness for cycle 2774 (Job ID 446189) — SINGLE-POST law.
# window-2774 open epoch 1793303735.851108753 (= the c2773 post-echo
# 1793303435.851108753 + 300.000 server contract; on-disk prophecy from the
# c2773 Next-block).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo. TEE-mode log.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2774_raw.json"
OUT_LOG="/home/z/my-project/scripts/capture_cycle2774.log"

echo "window-2774 open 1793303735.851108753 (c2773 Next-block prophecy)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "raw_bytes=$(wc -c < "$OUT_RAW")" | tee -a "$OUT_LOG"
echo "raw_head=$(head -c 120 "$OUT_RAW")" | tee -a "$OUT_LOG"
