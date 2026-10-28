#!/usr/bin/env python3
"""Append entry_cycle2663.txt to worklog.md (the c2663 ledger append).

Guards: pre-append worklog must be 8548 lines (the c2662 prophecy); the entry
file must be exactly 26 lines (the 26-line template); post-append must be 8574.
Exit non-zero on any guard failure, BEFORE any write.
"""
import sys

WORKLOG = "/home/z/my-project/worklog.md"
ENTRY = "/home/z/my-project/scripts/entry_cycle2663.txt"
PRE = 8548
ENTRY_LINES = 26
POST = PRE + ENTRY_LINES

with open(WORKLOG, "r", encoding="utf-8") as f:
    wl = f.read()
n_pre = wl.count("\n")
# wc -l equivalence: newline count (worklog ends with trailing newline)
if not wl.endswith("\n"):
    n_pre += 1
if n_pre != PRE:
    print(f"FAIL: pre-append worklog lines {n_pre} != prophecy {PRE}")
    sys.exit(1)
print(f"pre-append guard ok: {n_pre} lines == prophecy")

with open(ENTRY, "r", encoding="utf-8") as f:
    entry = f.read()
n_entry = entry.count("\n")
if not entry.endswith("\n"):
    n_entry += 1
if n_entry != ENTRY_LINES:
    print(f"FAIL: entry lines {n_entry} != template {ENTRY_LINES}")
    sys.exit(1)
print(f"entry template ok: {n_entry} lines")

if not entry.startswith("---\nTask ID: 446189-c2663\n"):
    print("FAIL: entry header malformed (separator/Task ID)")
    sys.exit(1)
print("entry header ok: separator + Task ID 446189-c2663")

if "446189-c2663" in wl:
    print("FAIL: sibling c2663 entry already present (dup guard)")
    sys.exit(1)
print("dup guard ok: no sibling c2663 entry")

with open(WORKLOG, "a", encoding="utf-8") as f:
    f.write(entry)

with open(WORKLOG, "r", encoding="utf-8") as f:
    wl2 = f.read()
n_post = wl2.count("\n")
if not wl2.endswith("\n"):
    n_post += 1
if n_post != POST:
    print(f"FAIL: post-append lines {n_post} != {POST}")
    sys.exit(1)
print(f"post-append ok: {n_post} lines (prophecy {PRE} + {ENTRY_LINES})")
print("APPEND COMPLETE: worklog 8548 -> 8574 lines (the 26-line template holds)")
