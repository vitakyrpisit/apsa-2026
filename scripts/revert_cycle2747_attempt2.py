#!/usr/bin/env python3
"""Byte-exact revert of the attempt-2 c2747 append (pre-commit recovery).

Attempt-2 landed a 12-line block that omitted the standard Task ID declaration
line (post-guard anchor_TaskID_post RED: 424 vs 425). The worklog is NOT yet
committed — this script strips the landed block byte-exactly (asserting the
current file == pre-state + landed-block concatenation), restoring the 8691-line
pre-append state so the corrected 13-line block can land under full guard.
All asserts precede the mutation; any failure -> REVERT_ABORTED, file untouched.
"""
import sys

WL = "/home/z/my-project/worklog.md"
LANDED = "/home/z/my-project/scripts/entry_cycle2747_attempt2_landed.txt"

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


landed = open(LANDED).read()
cur = open(WL).read()

guard("worklog_lines_now==8703", cur.count("\n") == 8703, f"got={cur.count(chr(10))}")
guard("cur_endswith_landed_block", cur.endswith(landed), "byte-exact suffix check")
pre = cur[: len(cur) - len(landed)]
guard("reverted_lines==8691", pre.count("\n") == 8691, f"got={pre.count(chr(10))}")
last = [l for l in pre.splitlines() if l.strip()][-1]
guard("reverted_tail_is_recon_next", last.endswith("first-job policy)."), repr(last[:40]))
guard("reverted_no_c2747", pre.count("c2747") == 0, f"c2747={pre.count('c2747')}")
tid = len([l for l in pre.splitlines() if l.startswith("Task ID:")])
gold = len([l for l in pre.splitlines() if l.startswith("- No gold yet")])
guard("reverted_TaskID==424", tid == 424, f"got={tid}")
guard("reverted_nogold==357", gold == 357, f"got={gold}")

if failures:
    print(f"REVERT_ABORTED: {len(failures)} guard failures - worklog UNTOUCHED")
    sys.exit(1)

with open(WL, "w") as f:
    f.write(pre)
post = open(WL).read()
guard("post_revert_lines==8691", post.count("\n") == 8691, f"got={post.count(chr(10))}")
if failures:
    print("REVERT_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print("REVERT_GREEN: attempt-2 block stripped byte-exact, worklog restored to 8691 (pre-append state)")
