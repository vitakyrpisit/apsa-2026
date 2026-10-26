#!/usr/bin/env python3
"""Reconstruct scan_cycle2585_raw.json via the c2453-raw key-order identity.

INSTRUMENTATION DEVIATION (c2585): the scan POST fired WITHOUT the staged
harness — no curl -o capture. The response was received in full via plain curl
piped to json.tool; the parsed values below are transcribed from that output.
The raw is rebuilt byte-faithfully from the c2584 raw (same schema, same
five-tuple; ONLY scanned_at/scan_duration_ms swapped to the received values) —
the LOSS EVENT #5 reconstruction precedent. Corroboration: the reconstruction
is asserted parsed-equal to the received response dict.
"""
import json

SRC = "/home/z/my-project/scripts/scan_cycle2584_raw.json"
DST = "/home/z/my-project/scripts/scan_cycle2585_raw.json"

# Received values (server-side, from the c2585 response):
RECV_SCANNED_AT = "2026-10-26T17:30:11.357Z"
RECV_DURATION_MS = 3523

# The response as RECEIVED (parsed from the json.tool output, verbatim fields):
RECEIVED = {
    "scanned_at": "2026-10-26T17:30:11.357Z",
    "scan_duration_ms": 3523,
    "basedagents": {
        "total_tasks": 26,
        "honest_paid": 0,
        "honest_free": 4,
        "scam_pattern": 18,
        "unknown": 4,
        "best_paid_task": None,
        "all_honest_paid": [],
    },
    "taskbounty": {
        "api_key_configured": False,
        "total_bounties": 0,
        "total_missions": 0,
        "paid_missions": 0,
        "scam_missions": 0,
        "unpaid_missions": 0,
        "best_bounty": None,
        "all_bounties": [],
        "actor_id": None,
    },
    "next_scan_in_seconds": 300,
    "auto_claim_pending": False,
}

src_text = open(SRC, encoding="utf-8").read()
d = json.loads(src_text)
d["scanned_at"] = RECV_SCANNED_AT
d["scan_duration_ms"] = RECV_DURATION_MS

out = json.dumps(d, separators=(",", ":"))
if src_text.endswith("\n"):
    out += "\n"

# Corroboration: reconstruction must be parsed-equal to the received response.
assert d == RECEIVED, "RECONSTRUCTION MISMATCH vs received response"
with open(DST, "w", encoding="utf-8") as f:
    f.write(out)

src_len = len(src_text.encode())
dst_len = len(out.encode())
print(f"src_bytes={src_len} dst_bytes={dst_len}")
assert dst_len == src_len, "size identity broken (same-schema swap must preserve length)"
print(f"reconstructed_ok={DST} ({dst_len}B, key-order identity, parsed-equal to received)")
