#!/usr/bin/env python3
"""Qualify a marketplace scan raw payload (rebuilt after ROLLBACK-#11).

Original was lost in ROLLBACK-#11 (ledger + tooling state restored to
c1858, 2026-10-21). Rebuilt at c2159 from session-verified output
format. Usage: python3 qualify_scan.py <raw_json_path>

Outputs:
  five_tuple=(total, honest_paid, honest_free, scam, unknown)
  best_paid_task=<task_id or None>
  taskbounty: api_key_configured=... total_bounties=... paid_missions=... best_bounty=...
  auto_claim_pending=...
  scanned_at=...
  scan_duration_ms=...
  next_scan_in_seconds=...
  PAID_FOUND=True/False
"""
import json
import sys


def main():
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)

    ba = d.get("basedagents", {}) or {}
    tb = d.get("taskbounty", {}) or {}

    five = (
        ba.get("total_tasks"),
        ba.get("honest_paid"),
        ba.get("honest_free"),
        ba.get("scam_pattern"),
        ba.get("unknown"),
    )
    print(f"five_tuple={five}")

    bpt = ba.get("best_paid_task")
    bpt_id = bpt.get("task_id") if isinstance(bpt, dict) else bpt
    print(f"best_paid_task={bpt_id}")

    print(
        f"taskbounty: api_key_configured={tb.get('api_key_configured')} "
        f"total_bounties={tb.get('total_bounties')} "
        f"paid_missions={tb.get('paid_missions')} "
        f"best_bounty={tb.get('best_bounty')}"
    )
    print(f"auto_claim_pending={d.get('auto_claim_pending')}")
    print(f"scanned_at={d.get('scanned_at')}")
    print(f"scan_duration_ms={d.get('scan_duration_ms')}")
    print(f"next_scan_in_seconds={d.get('next_scan_in_seconds')}")

    paid_found = bool(
        (ba.get("honest_paid") or 0) > 0
        or bpt_id is not None
        or (tb.get("paid_missions") or 0) > 0
    )
    print(f"PAID_FOUND={paid_found}")


if __name__ == "__main__":
    main()
