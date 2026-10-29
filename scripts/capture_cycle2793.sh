#!/bin/bash
# Official capture harness for cycle 2793 (Job ID 446189) — SINGLE-POST law.
# window-2793 open epoch 1793315022.218649965 (= the c2792 post-echo
# 1793314722.218649965 + 300.000 server contract; on-disk prophecy from the
# c2792 Next-block; ISO rendered FROM the EPOCH: 23:03:42.218649965 +0000 =
# 07:03:42.218649965 +08 — the c2778 Next-block window-2779 ISO misrender
# +380.000s lesson applied).
# Mandatory order: pre-echo -> curl -o/-w -> post-echo. TEE-mode log.
set -u
OUT_RAW="/home/z/my-project/scripts/scan_cycle2793_raw.json"
OUT_LOG="/home/z/my-project/scripts/capture_cycle2793.log"

echo "window-2793 open 1793315022.218649965 (c2792 Next-block prophecy, EPOCH-governs)" | tee "$OUT_LOG"
echo "PRE-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"

metrics=$(curl -s -X POST http://localhost:3000/api/marketplaces/scan \
  -o "$OUT_RAW" -w '%{http_code} %{time_total} %{size_download}')
rc=$?
echo "CURL_METRICS http_code_time_size='$metrics' rc=$rc" | tee -a "$OUT_LOG"

echo "POST-ECHO $(date '+%Y-%m-%dT%H:%M:%S.%N%z') epoch=$(date +%s.%N)" | tee -a "$OUT_LOG"
echo "raw_bytes=$(wc -c < "$OUT_RAW")" | tee -a "$OUT_LOG"
echo "raw_head=$(head -c 120 "$OUT_RAW")" | tee -a "$OUT_LOG"
