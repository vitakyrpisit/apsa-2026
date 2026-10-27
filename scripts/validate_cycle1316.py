#!/usr/bin/env python3
"""Validator for scan cycle 1264 (Job 446189).

Rebuilt from scratch after environment rollback #4 (2026-10-18 00:00 +08:00)
which restored the 2026-10-13T12:29+08:00 snapshot (worklog tail = c664) and
wiped every 2026-10-17 artifact (validators c1114-c1263, recursive_diff.py,
scan raws/pretties c665+). This validator also establishes the NEW baseline
after drift event #6 (first paid-side change), REBASED at c1316 after drift event #7 (free erosion resumed):

    Drift #6 baseline (c1264-c1292, 446B): (26, 0, 7, 16, 3)
    REBASED baseline (c1316+):             (25, 0, 6, 16, 3)  @ 446 bytes
    - honest_free 7->6: single free task removed; erosion resumed after
      29-cycle pause (7 held c1264-c1292). Paid side still 0.
    - recursive_diff root cause: basedagents.honest_free 7->6,
      basedagents.total_tasks 26->25. All other sections byte-identical.

Usage: python3 validate_cycle1316.py [raw_json_path]
"""
import json
import sys

CYCLE = 1316
BASELINE = {"total": 25, "honest_paid": 0, "honest_free": 6, "scam": 16, "unknown": 3}
EXPECTED_BYTES = 446


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else (
        f"/home/z/my-project/scripts/scan_cycle{CYCLE}_raw.json")
    with open(path, "rb") as f:
        raw = f.read()
    print(f"clean_body_bytes={len(raw)}")
    size_ok = len(raw) == EXPECTED_BYTES
    print(f"size_matches_baseline={str(size_ok).lower()} ({len(raw)}B vs {EXPECTED_BYTES}B)")
    data = json.loads(raw)
    print("json_valid=true")
    print(f"scanned_at={data.get('scanned_at')}")
    print(f"scan_duration_ms={data.get('scan_duration_ms')}")

    ba = data.get("basedagents", {})
    comp = {
        "total": ba.get("total_tasks"),
        "honest_paid": ba.get("honest_paid"),
        "honest_free": ba.get("honest_free"),
        "scam": ba.get("scam_pattern"),
        "unknown": ba.get("unknown"),
    }
    print("BA composition: total=%s honest_paid=%s honest_free=%s scam=%s unknown=%s"
          % (comp["total"], comp["honest_paid"], comp["honest_free"],
             comp["scam"], comp["unknown"]))
    match = comp == BASELINE
    print(f"baseline_match_c{CYCLE}={str(match).lower()}")

    paid_list = ba.get("all_honest_paid") or []
    best = ba.get("best_paid_task")
    print(f"all_honest_paid_len={len(paid_list)}")
    print(f"best_paid_task={'null' if best is None else 'present'}")
    if best is not None:
        print("  paid[0]: id=%s escrow=%s bounty_raw=%s caps=%s api_ev=%s title='%s'"
              % (best.get("id"), best.get("escrow_status"), best.get("bounty_raw"),
                 best.get("matches_our_caps"), best.get("api_ev"), best.get("title")))

    tb = data.get("taskbounty", {})
    print("taskbounty: api_key=%s bounties=%s paid_missions=%s"
          % (str(tb.get("api_key_configured")).lower(),
             tb.get("total_bounties"), tb.get("paid_missions")))
    print(f"clawlancer_present={str('clawlancer' in data).lower()}")
    print(f"auto_claim_pending={str(data.get('auto_claim_pending')).lower()}")
    print(f"next_scan_in_seconds={data.get('next_scan_in_seconds')}")

    pretty_path = f"/home/z/my-project/scripts/scan_cycle{CYCLE}.json"
    with open(pretty_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"archive_written={pretty_path}")

    ok = match and size_ok and len(paid_list) == 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
