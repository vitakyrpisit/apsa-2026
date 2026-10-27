#!/usr/bin/env python3
"""Extract decisive claim-decision fields from c1506 honest paid tasks."""
import json

RAW = "/home/z/my-project/scripts/scan_cycle1506_raw.json"
d = json.load(open(RAW))
tasks = d["basedagents"]["all_honest_paid"]

FIELDS = ["task_id", "title", "bounty", "bounty_amount", "bounty_network", "bounty_token",
          "escrow", "estimated_ev_usd", "matches_our_caps", "our_caps_overlap",
          "required_capabilities", "claimable", "status", "claimed_by_agent_id",
          "claim_expires_at", "auto_release_at", "expires_at", "created_at",
          "max_active_claims_per_agent", "classification", "reasons", "expected_output",
          "output_format", "review_state", "payment_status"]

print("===== DECISION FIELDS (all 5 tasks) =====")
for t in tasks:
    print(f"\n--- {t.get('task_id')} ---")
    for k in FIELDS:
        if k in t:
            print(f"{k}: {json.dumps(t[k], ensure_ascii=False)}")

print("\n===== FULL DESCRIPTION OF TASK[0] (chars 1200-end) =====")
print(tasks[0]["description"][1200:])
