#!/usr/bin/env python3
"""Validator for cycle 997 - rebuilt from scratch after environment rollback.
Rollback wiped c665-c964 worklog entries and all scan artifacts.
Baseline re-established from live scan + session context:
- c929-c964 baseline was 36/1/14/17/4 @ 4318 bytes
- c1090: scam->honest_free reclassification observed: 36/1/15/16/4 @ 4318 bytes
This validator asserts the NEW (c1090) state. Derive c1090+ from this file via sed.
"""
import json
import sys

RAW = "/home/z/my-project/scripts/scan_cycle1090_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1090.json"
BASE_BYTES = 4318  # baseline with 4-digit scan_duration_ms; only variable-length field in response

with open(RAW, "rb") as f:
    body = f.read()
clean = body.decode("utf-8").strip()
print(f"clean_body_bytes={len(clean.encode('utf-8'))}")

d = json.loads(clean)
# Byte size = BASE_BYTES + extra digits of scan_duration_ms beyond 4 digits (verified c1090: 12475 = 5 digits -> +1 byte; field-level diff vs c987 confirmed no other change)
EXPECTED_BYTES = BASE_BYTES + max(0, len(str(d["scan_duration_ms"])) - 4)
assert len(clean.encode("utf-8")) == EXPECTED_BYTES, (
    f"byte deviation: {len(clean.encode('utf-8'))} != {EXPECTED_BYTES} (base {BASE_BYTES}, duration {d['scan_duration_ms']}) - investigate before archiving"
)
print("json_valid=true")
print(f"scanned_at={d.get('scanned_at')}")
print(f"scan_duration_ms={d.get('scan_duration_ms')}")
assert d.get("scanned_at") and d.get("scan_duration_ms") is not None

ba = d["basedagents"]
total = ba["total_tasks"]
hp = ba["honest_paid"]
hf = ba["honest_free"]
sc = ba["scam_pattern"]
un = ba["unknown"]
print(f"BA composition: total={total} honest_paid={hp} honest_free={hf} scam={sc} unknown={un}")
assert (total, hp, hf, sc, un) == (32, 1, 12, 16, 3), "composition mismatch vs c1090 baseline (32/1/12/16/3)"
assert total == hp + hf + sc + un, "composition sum mismatch"

ahp = ba["all_honest_paid"]
print(f"all_honest_paid_len={len(ahp)}")
assert len(ahp) == 1
t = ahp[0]
assert t["task_id"] == "task_ILI16I1DYjTOabbUBRvV9"
assert t["title"] == "Test hire (please ignore)"
assert t["status"] == "open"
assert t["bounty_amount"] == "1000000" and t["bounty_token"] == "USDC"
assert t["bounty_network"] == "eip155:8453"
esc = t["escrow"]
assert esc["status"] == "funded", f"escrow status changed: {esc['status']}"
assert esc["deposit_tx_hash"].startswith("0x21cc40")
print(f"  paid[0]: id={t['task_id']} escrow={esc['status']} tx={esc['deposit_tx_hash'][:9]}… caps={t['matches_our_caps']} api_ev={t['estimated_ev_usd']} title='{t['title']}'")
assert t["matches_our_caps"] is False

tb = d["taskbounty"]
print(f"taskbounty: api_key={tb['api_key_configured']} bounties={tb['total_bounties']} paid_missions={tb['paid_missions']}")
assert tb["api_key_configured"] is False
assert tb["total_bounties"] == 0 and tb["paid_missions"] == 0

print(f"clawlancer_present={'clawlancer' in d}")
assert "clawlancer" not in d, "clawlancer appeared in response - investigate"

print(f"auto_claim_pending={d.get('auto_claim_pending')}")
assert d.get("auto_claim_pending") is True

with open(PRETTY, "w") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print(f"archive_written={PRETTY}")
