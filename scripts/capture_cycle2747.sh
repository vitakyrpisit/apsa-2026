#!/bin/bash
# Official capture harness for cycle 2747 (Job ID 446189) — SINGLE-POST law.
# window-2747 open epoch 1793212694.939926673 (context-carried prophecy:
# c2746 post-echo + 300.000 server contract; the LOSS-#83 rollback destroyed
# the on-disk capture lineage, the prophecy is CONTEXT-CARRIED).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo. TEE-mode log.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2747_raw.json"
OUT_LOG="/home/z/my-project/scripts/capture_cycle2747.log"

echo "window-2747 open 1793212694.939926673 (context-carried prophecy)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "raw_bytes=$(wc -c < "$OUT_RAW")" | tee -a "$OUT_LOG"
echo "raw_head=$(head -c 120 "$OUT_RAW")" | tee -a "$OUT_LOG"
