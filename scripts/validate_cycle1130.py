#!/usr/bin/env python3
"""Fresh validator for cycle 1114 - REBUILT from scratch after 2nd environment
rollback (filesystem restored to c664 snapshot; c665-c1113 records lost).
Establishes new baseline for future sed-derivation. Ground truth = live scan."""
import json, sys

RAW = "/home/z/my-project/scripts/scan_cycle1130_raw.json"
PRETTY = "/home/z/my-project/scripts/scan_cycle1130.json"

body = open(RAW, "rb").read()
print(f"clean_body_bytes={len(body)}")
d = json.loads(body)
print("json_valid=true")

print(f"scanned_at={d.get('scanned_at')}")
print(f"scan_duration_ms={d.get('scan_duration_ms')}")

ba = d["marketplaces"]["basedagents"] if "marketplaces" in d else d["basedagents"]
total = ba["total_tasks"]; hp = ba["honest_paid"]; hf = ba["honest_free"]
sc = ba["scam_pattern"]; un = ba["unknown"]
print(f"BA composition: total={total} honest_paid={hp} honest_free={hf} scam={sc} unknown={un}")

# NEW baseline established c1130 (post-rollback recovery):
# (33, 1, 13, 16, 3) = pre-rollback (32, 1, 12, 16, 3) +1 honest_free (MARKET_CHANGED at c1130)
EXPECTED = (33, 1, 13, 16, 3)
actual = (total, hp, hf, sc, un)
assert actual == EXPECTED, f"composition changed vs c1130 baseline: {actual}"
print("baseline_match_c1130=true")

ahp = ba["all_honest_paid"]
print(f"all_honest_paid_len={len(ahp)}")
assert hp == len(ahp), f"honest_paid count mismatch: {hp} vs {len(ahp)}"

for t in ahp:
    assert t["status"] == "open", f"status changed: {t['status']}"
    assert t["claimed_at"] is None, "task claimed!"
    assert t["claimed_by_agent_id"] is None, "task claimed!"
    esc = t["escrow"]
    assert esc["status"] == "funded", f"escrow status changed: {esc['status']}"
    amt = int(t["bounty_amount"])
    print(f"  paid[0]: id={t['task_id']} escrow={esc['status']} tx={esc['deposit_tx_hash'][:9]}\u2026 "
          f"caps={t['matches_our_caps']} api_ev={t['estimated_ev_usd']} title='{t['title']}'")
    print(f"    bounty={amt} raw ({amt/1e6:.2f} {t['bounty_token']}) net={t['bounty_network']} "
          f"payment_verified={t['payment_verified']} settled={t['payment_settled']}")
    assert t["matches_our_caps"] is False
    assert amt == 1000000, f"bounty changed: {amt}"

tb = d["marketplaces"]["taskbounty"] if "marketplaces" in d else d["taskbounty"]
tb_b = len(tb.get("bounties", [])); tb_pm = tb.get("paid_missions", 0)
print(f"taskbounty: api_key={tb.get('api_key_configured', False)} bounties={tb_b} paid_missions={tb_pm}")
assert tb_b == 0 and tb_pm == 0, "TaskBounty state changed!"

claw = d["marketplaces"].get("clawlancer", None) if "marketplaces" in d else d.get("clawlancer")
print(f"clawlancer_present={claw is not None}")

acp = d.get("auto_claim_pending", None)  # NOTE: top-level key, not inside basedagents
print(f"auto_claim_pending={acp}")
assert acp is True, f"auto_claim_pending changed: {acp}"
assert d.get("next_scan_in_seconds") == 300, "next_scan_in_seconds changed"

json.dump(d, open(PRETTY, "w"), indent=2, sort_keys=True)
print(f"archive_written={PRETTY}")

# Stale c664 snapshot comparison (expected to differ - 3 days drift)
try:
    old = json.load(open("/home/z/my-project/scripts/scan_cycle664.json"))
    oba = old["marketplaces"]["basedagents"] if "marketplaces" in old else old["basedagents"]
    ocomp = (oba["total_tasks"], oba["honest_paid"], oba["honest_free"], oba["scam_pattern"], oba["unknown"])
    print(f"stale_c664_composition={ocomp} (worklog snapshot era; drift expected)")
except Exception as e:
    print(f"stale_c664_compare_failed={e}")
