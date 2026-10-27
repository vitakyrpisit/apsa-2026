#!/usr/bin/env python3
"""Cycle 900 validation: parse raw scan, verify all protocol fields, write pretty archive."""
import json, sys

RAW = "/home/z/my-project/scripts/scan_cycle900_raw.json"
OUT = "/home/z/my-project/scripts/scan_cycle900.json"

with open(RAW, "rb") as f:
    body = f.read()

# 1. Strip optional HTTP-meta trailer (seen in some cycles)
marker = b"---HTTP_META---"
meta = None
if marker in body:
    body, _, trailer = body.partition(marker)
    meta = trailer.strip().decode("utf-8", "replace")

print(f"clean_body_bytes={len(body)}")
assert len(body) == 9854, f"unexpected body size {len(body)}"

data = json.loads(body)
print("json_valid=true")
print(f"scanned_at={data.get('scanned_at')}")
print(f"scan_duration_ms={data.get('scan_duration_ms')}")

ba = data.get("basedagents") or {}
print(f"BA composition: total={ba.get('total_tasks')} honest_paid={ba.get('honest_paid')} "
      f"honest_free={ba.get('honest_free')} scam={ba.get('scam_pattern')} unknown={ba.get('unknown')}")

# 2. all_honest_paid deep check
paid = ba.get("all_honest_paid") or []
print(f"all_honest_paid_len={len(paid)}")
for i, t in enumerate(paid):
    tid = t.get("task_id")
    esc = t.get("escrow_status")
    tx = (t.get("escrow_tx") or "")[:8]
    caps = t.get("matches_our_caps")
    title = t.get("title")
    print(f"  paid[{i}]: id={tid} escrow={esc} tx={tx}… caps={caps} title={title!r}")

tb = data.get("taskbounty") or {}
print(f"taskbounty: paid={tb.get('paid_missions')} gold={tb.get('has_gold')} "
      f"best={tb.get('best_paid_task')}")

print(f"clawlancer_present={'clawlancer' in data}")
print(f"auto_claim_pending={data.get('auto_claim_pending')}")
if meta:
    print(f"http_meta_trailer_stripped=True ({len(meta)} chars)")

# 3. Pretty archive
with open(OUT, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"archive_written={OUT}")
