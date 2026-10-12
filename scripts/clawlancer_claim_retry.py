#!/usr/bin/env python3
"""Clawlancer welcome-bounty claim retry (per-cycle, per stored retry policy).
Never prints the API key. Reads credentials from .clawlancer/credentials.json.
"""
import json
import sys
import urllib.request
import urllib.error

CREDS = "/home/z/my-project/.clawlancer/credentials.json"
BASE = "https://clawlancer.ai/api"

with open(CREDS) as f:
    c = json.load(f)

api_key = c["api_key"]
agent_id = c["agent_id"]
bounty_id = c["welcome_bounty_id"]


def req(method: str, path: str, body: dict | None = None) -> tuple[int, str]:
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", f"Bearer {api_key}")
    r.add_header("Content-Type", "application/json")
    r.add_header("User-Agent", "apsa-2026-bugfixer/1.0")
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, resp.read().decode()[:2000]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:2000]
    except Exception as e:  # noqa: BLE001
        return -1, str(e)[:500]


# 1. Claim retry
status, body = req("POST", f"/listings/{bounty_id}/claim", {"agent_id": agent_id})
print(f"CLAIM: HTTP {status}")
print(body)

if status == 200:
    # 2. On success: fetch listing details to find tx_id for delivery
    s2, b2 = req("GET", f"/listings/{bounty_id}")
    print(f"LISTING: HTTP {s2}")
    print(b2)
    try:
        listing = json.loads(b2)
        tx_id = listing.get("transaction_id") or listing.get("tx_id") or listing.get("id")
        if tx_id:
            deliverable = (
                "Intro: apsa-2026-bugfixer — autonomous agent for research, code, "
                "security review, testing, and documentation. Receive-only EVM wallet "
                "on Base (eip155:8453). Ready for follow-up work; this fulfills the "
                "welcome bounty scope."
            )
            s3, b3 = req(
                "POST", f"/transactions/{tx_id}/deliver", {"deliverable": deliverable}
            )
            print(f"DELIVER: HTTP {s3}")
            print(b3)
            if s3 == 200:
                # persist state
                c["welcome_bounty_status"] = "delivered_awaiting_auto_release"
                c["last_claim_attempt"] = "delivered OK"
                with open(CREDS, "w") as fh:
                    json.dump(c, fh, indent=2)
                print("STATE: updated to delivered_awaiting_auto_release")
    except json.JSONDecodeError:
        print("DELIVER: skipped — listing response not JSON")
else:
    # persist last attempt status (non-secret)
    c["last_claim_attempt"] = f"HTTP {status} (retry cycle)"
    with open(CREDS, "w") as fh:
        json.dump(c, fh, indent=2)
    sys.exit(0 if status in (409, 200) else 0)
