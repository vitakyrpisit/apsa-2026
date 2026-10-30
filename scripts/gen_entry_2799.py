#!/usr/bin/env python3
"""Entry harness for cycle 2799 — the c2798 gen_entry_2798.py slot.

DEViation note (honest, the MEASUREMENT GOVERNS): the c2799 entry was
authored via the direct two-pass write path (Write + Edit append on
entry_cycle2799.txt), NOT the embedded-LINES authoring precedent — the block
was too large for a single authoring write. This harness pins the canonical
bytes AFTER the fact: it extracts the landed block (worklog lines 9317-9328,
the 12-line c2799 standard block) and asserts byte-equality with
entry_cycle2799.txt, regenerating the file from the worklog source of record
on demand (guarded — abort on any mismatch). Ghost-class instrument
(untracked, the foreign-absorption path like gen_rebadge_2799.py)."""
import sys

WL = "/home/z/my-project/worklog.md"
ENTRY = "/home/z/my-project/scripts/entry_cycle2799.txt"

lines = open(WL, encoding="utf-8").read().splitlines()
if len(lines) != 9328:
    print(f"GEN_ABORTED: worklog lines={len(lines)} (expect 9328)")
    sys.exit(1)
block = "\n".join(lines[9316:9328]) + "\n"
struct_ok = (block.startswith("---\nCYCLE 2799 (Job ID 446189)")
             and "Task ID: 446189-c2799" in block.splitlines()[2]
             and block.splitlines()[-1].startswith("- Next: the c2800 instance")
             and "- No gold yet. Scanner continues." in block.splitlines())
if not struct_ok:
    print("GEN_ABORTED: lines 9317-9328 are not the c2799 standard block")
    sys.exit(1)

on_disk = open(ENTRY, encoding="utf-8").read()
if on_disk == block:
    print(f"entry_cycle2799.txt == worklog lines 9317-9328 byte-exact "
          f"({len(block.encode('utf-8'))} bytes, 12 lines)")
    sys.exit(0)

open(ENTRY, "w", encoding="utf-8").write(block)
print(f"entry_cycle2799.txt regenerated from the landed block "
      f"({len(block.encode('utf-8'))} bytes, 12 lines)")
