#!/bin/bash
# Official capture harness for cycle 2768 (Job ID 446189) — SINGLE-POST law.
# window-2768 open epoch 1793300766.703178724 (= the c2767 post-echo
# 1793300466.703178724 + 300.000 server contract; on-disk prophecy from the
# c2767 Next-block).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo. TEE-mode log.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2768_raw.json"
OUT_LOG="/home/z/my-project/scripts/capture_cycle2768.log"

echo "window-2768 open 1793300766.703178724 (c2767 Next-block prophecy)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "raw_bytes=$(wc -c < "$OUT_RAW")" | tee -a "$OUT_LOG"
echo "raw_head=$(head -c 120 "$OUT_RAW")" | tee -a "$OUT_LOG"
