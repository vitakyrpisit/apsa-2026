#!/bin/bash
# Official capture harness for cycle 2813 (Job ID 446189) — SINGLE-POST law.
# window-2813 open epoch 1793328988.217915386 (= the c2812 capture post-echo
# 1793328688.217915386 + 300.000 server contract; on-disk prophecy from the
# c2812 Next-block; ISO rendered FROM the EPOCH: 02:56:28.217915386 +0000 =
# 10:56:28.217915386 +08 — the c2778 Next-block window-2779 ISO misrender
# +380.000s lesson applied).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo. TEE-mode log.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2813_raw.json"
OUT_LOG="/home/z/my-project/scripts/capture_cycle2813.log"

echo "window-2813 open 1793328988.217915386 (c2812 Next-block prophecy, EPOCH-governs)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "raw_bytes=$(wc -c < "$OUT_RAW")" | tee -a "$OUT_LOG"
echo "raw_head=$(head -c 120 "$OUT_RAW")" | tee -a "$OUT_LOG"
