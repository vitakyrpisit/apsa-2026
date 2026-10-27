#!/usr/bin/env python3
"""Cycle 964 validation: parse raw scan (post-c923 new baseline 4318 bytes), verify fields, archive."""
import json, sys

RAW = "/home/z/my-project/scripts/scan_cycle964_raw.json"
OUT = "/home/z/my-project/scripts/scan_cycle964.json"
EXPECTED_BYTES = 4318  # new baseline since c923 composition change

with open(RAW, "rb") as f:
    body = f.read()

marker = b"---HTTP_META---"
if marker in body:
    body, _, trailer = body.partition(marker)
    print(f"http_meta_trailer_stripped=True")

print(f"clean_body_bytes={len(body)}")
assert len(body) == EXPECTED_BYTES, f"unexpected body size {len(body)} (expected {EXPECTED_BYTES})"

data = json.loads(body)
print("json_valid=true")
print(f"scanned_at={data.get('scanned_at')}")
print(f"scan_duration_ms={data.get('scan_duration_ms')}")

ba = data.get("basedagents") or {}
print(f"BA composition: total={ba.get('total_tasks')} honest_paid={ba.get('honest_paid')} "
      f"honest_free={ba.get('honest_free')} scam={ba.get('scam_pattern')} unknown={ba.get('unknown')}")

paid = ba.get("all_honest_paid") or []
print(f"all_honest_paid_len={len(paid)}")
for i, t in enumerate(paid):
    e = t.get("escrow") or {}
    print(f"  paid[{i}]: id={t.get('task_id')} escrow={e.get('status')} tx={(e.get('deposit_tx_hash') or '')[:8]}… "
          f"caps={t.get('matches_our_caps')} api_ev={t.get('estimated_ev_usd')} title={t.get('title')!r}")

tb = data.get("taskbounty") or {}
print(f"taskbounty: paid={tb.get('paid_missions')} best={tb.get('best_bounty')}")
print(f"clawlancer_present={'clawlancer' in data}")
print(f"auto_claim_pending={data.get('auto_claim_pending')}")

with open(OUT, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"archive_written={OUT}")
