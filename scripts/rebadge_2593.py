#!/usr/bin/env python3
"""Rebadge validate_cycle2592.py -> validate_cycle2593.py (DRIFT-#40 verification-3, match-path + PLAIN-POST adaptation).

Per the c2592 Next block: sed 2592->2593 + header verification-2 CARRY -> verification-3
CARRY (rebadged-from 2591->2592) + chain insert c2593 = DRIFT-#40 verification 3 +
line-8 bump. c2573 LESSON (applied first-pass twenty cycles running): the P1 patch
pattern must match the source-file name AS IT EXISTS post-sed — post-sed the header
still names validate_cycle2591.py (unmigrated by the sed).

PLAIN-POST adaptation (c2593-specific, explicit): this cycle ran the trigger-verbatim
scan command with NO capture harness (no pre/post echo, no curl -o raw bytes). The
wire-size assertion is SKIPPED (not passed, not failed); the parsed-JSON assertions
run unchanged against scan_cycle2593.json. NO raw-bytes file is written or
reconstructed — anti-fabrication guard (scan_cycle2593_raw.json must stay ABSENT).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#40 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 9/9 (+1 SKIPPED) — c2593 = DRIFT-#40
verification 3, the root extends 2-fold -> 3-fold (five-tuple (24,0,3,18,3)
reproduced; wire size UNVERIFIED this cycle).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2592.py"
DST = "/home/z/my-project/scripts/validate_cycle2593.py"

text = open(SRC).read()

# 1) global sed 2592->2593
text = text.replace("2592", "2593")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#40 verification-2 CARRY (root declared 2026-10-27 ~02:28 +08): "
          "rebadged from validate_cycle2591.py")
p1_new = ("DRIFT-#40 verification-3 CARRY (root declared 2026-10-27 ~02:28 +08): "
          "rebadged from validate_cycle2592.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump
l8_old = "(24,0,3,18,3) @ 446B DRIFT-#40 root; c2593 = DRIFT-#40 verification 1"
l8_new = "(24,0,3,18,3) @ 446B DRIFT-#40 root; c2593 = DRIFT-#40 verification 3"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain-head bump + chain insert in ONE patch
ch_old = "(c2593 = DRIFT-#40 verification 2; c2591 = DRIFT-#40 verification 1, ROOT"
ch_new = ("(c2593 = DRIFT-#40 verification 3; c2592 = DRIFT-#40 verification 2; "
          "c2591 = DRIFT-#40 verification 1, ROOT")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

# 5) docstring size-note (plain-post skip documentation)
ds_old = "  - response size 446 bytes (band 446-447)\n"
ds_new = ("  - response size 446 bytes (band 446-447)\n"
          "    [c2593 PLAIN-POST: SKIPPED — no raw capture this cycle; not asserted,\n"
          "    not counted as a pass; scan_cycle2593_raw.json must stay ABSENT]\n")
c = text.count(ds_old)
assert c == 1, f"docstring pre-patch count != 1: {c}"
text = text.replace(ds_old, ds_new)

# 6) PLAIN-POST code swap — raw-bytes block -> parsed-JSON block
code_old = '''with open(RAW, "rb") as f:
    raw_bytes = f.read()
print(f"clean_body_bytes={len(raw_bytes)}")
check("size_matches_baseline_band", len(raw_bytes) in BASELINE_SIZE_BAND,
      f"{len(raw_bytes)}B vs band {BASELINE_SIZE_BAND}")

d = json.loads(raw_bytes)
'''
code_new = '''# c2593 PLAIN-POST adaptation: NO raw capture this cycle (trigger-verbatim pipe
# class; the captured-class staging streak ENDED at 7). Wire size NOT asserted this
# cycle — not passed, not failed, SKIPPED. All parsed-JSON assertions run unchanged
# against the saved response file. NO raw-bytes file is written or reconstructed
# (anti-fabrication).
_c = json.dumps(json.load(open(PRETTY)), sort_keys=True, separators=(",", ":")).encode()
print(f"plain_post_class=true (size_matches_baseline_band SKIPPED — no raw capture; "
      f"informational canonical-compact length={len(_c)}B, NOT the wire size)")

d = json.load(open(PRETTY))
'''
c = text.count(code_old)
assert c == 1, f"code-swap pre-patch count != 1: {c}"
text = text.replace(code_old, code_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2592 references post-rebadge
# (rebadged-from header + chain insert); 2591 keeps exactly 1 (chain history).
sites_92 = [m.start() for m in re.finditer("2592", text)]
sites_91 = [m.start() for m in re.finditer("2591", text)]
print(f"P-HIST 2592 refs = {len(sites_92)}")
for s in sites_92:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
print(f"P-HIST 2591 refs = {len(sites_91)} (chain history)")
if len(sites_92) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2592 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
