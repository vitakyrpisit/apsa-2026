#!/usr/bin/env python3
"""Inspector for anomalous c1506 response (48344B vs 446B drift-#8 baseline).

Dumps schema + key fields + any honest-paid/taskbounty details for gold check.
"""
import json

RAW = "/home/z/my-project/scripts/scan_cycle1506_raw.json"
raw = open(RAW, "rb").read()
clean = raw.strip()
print(f"clean_body_bytes={len(clean)}")

d = json.loads(clean)
print(f"top_keys={sorted(d.keys())}")
print(f"scanned_at={d.get('scanned_at')} duration_ms={d.get('scan_duration_ms')} next_scan_in_seconds={d.get('next_scan_in_seconds')}")
print(f"auto_claim_pending={d.get('auto_claim_pending')}")

ba = d.get("basedagents", {})
print(f"ba_keys={sorted(ba.keys())}")
for k in ["total_tasks", "honest_paid", "honest_free", "scam_pattern", "unknown"]:
    print(f"  {k}={ba.get(k)}")

bpt = ba.get("best_paid_task") if "best_paid_task" in ba else d.get("best_paid_task")
print(f"best_paid_task={'NULL' if bpt is None else json.dumps(bpt)[:600]}")

ahp = ba.get("all_honest_paid")
if ahp is None:
    ahp = d.get("all_honest_paid")
n = len(ahp) if isinstance(ahp, (list, dict)) else int(ahp or 0)
print(f"all_honest_paid_len={n}")
if isinstance(ahp, list) and ahp:
    for i, t in enumerate(ahp):
        print(f"  --- honest_paid[{i}] ---")
        print(json.dumps(t, indent=2)[:1500])

tb = d.get("taskbounty", {})
print(f"tb_keys={sorted(tb.keys()) if isinstance(tb, dict) else type(tb)}")
if isinstance(tb, dict):
    for k in ["api_key_configured", "total_bounties", "total_missions", "paid_missions", "scam_missions", "unpaid_missions"]:
        print(f"  {k}={tb.get(k)}")
    bb = tb.get("best_bounty")
    print(f"  best_bounty={'NULL' if bb is None else json.dumps(bb)[:600]}")
    for key in ["all_bounties", "all_missions"]:
        lst = tb.get(key) or []
        print(f"  {key}_len={len(lst)}")
        for i, t in enumerate(lst[:5]):
            print(f"  --- {key}[{i}] ---")
            print(json.dumps(t, indent=2)[:1200])

cl = d.get("clawlancer")
print(f"clawlancer={'ABSENT' if not cl else json.dumps(cl)[:600]}")
print(f"clawlancer_present_flag={d.get('clawlancer_present')}")

# Any unexpected top-level keys vs drift-#8 schema
known = {"scanned_at", "scan_duration_ms", "basedagents", "taskbounty", "next_scan_in_seconds", "auto_claim_pending", "clawlancer", "clawlancer_present", "best_paid_task", "all_honest_paid"}
extra = [k for k in d.keys() if k not in known]
print(f"extra_top_keys={extra}")
for k in extra:
    v = d[k]
    s = json.dumps(v)
    print(f"  --- extra[{k}] (len={len(s)}) ---")
    print(s[:2000])
