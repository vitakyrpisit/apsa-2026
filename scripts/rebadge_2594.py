#!/usr/bin/env python3
"""Rebadge validate_cycle2593.py -> validate_cycle2594.py (DRIFT-#40 verification-4, match-path + CAPTURED-CLASS RESTORE).

Per the c2593 Next block: sed 2593->2594 + header verification-3 CARRY -> verification-4
CARRY (rebadged-from 2592->2593) + chain insert c2594 = DRIFT-#40 verification 4 +
line-8 bump. c2573 LESSON (applied first-pass twenty-one cycles running): the P1 patch
pattern must match the source-file name AS IT EXISTS post-sed — post-sed the header
still names validate_cycle2592.py (unmigrated by the sed).

CAPTURED-CLASS RESTORE (c2594-specific, explicit): c2593 ran PLAIN-POST (no raw
capture; wire size SKIPPED). c2594 RESUMES captured-class staging — the plain-post
adaptation block is swapped back to the standard raw-bytes path (open RAW, assert
wire size against band 446-447, parse raw bytes). The plain-post docstring skip-note
is likewise restored to the standard band line. scan_cycle2594_raw.json WILL EXIST
(written by capture_cycle2594.sh pre-echo -> curl -o -> post-echo, single POST).
NOTE: this is the MATCH-PATH rebadge (DRIFT-#40 baseline HOLD branch). The validator
run that follows is EXPECTED TO PASS 10/10 — c2594 = DRIFT-#40 verification 4, the
root extends 3-fold -> 4-fold (five-tuple (24,0,3,18,3) reproduced @ 446B, wire-size
verification resumed).
"""
import re
import sys

SRC = "/home/z/my-project/scripts/validate_cycle2593.py"
DST = "/home/z/my-project/scripts/validate_cycle2594.py"

text = open(SRC).read()

# 1) global sed 2593->2594
text = text.replace("2593", "2594")

# 2) P1 header patch — pattern AS IT EXISTS post-sed (source name unmigrated)
p1_old = ("DRIFT-#40 verification-3 CARRY (root declared 2026-10-27 ~02:28 +08): "
          "rebadged from validate_cycle2592.py")
p1_new = ("DRIFT-#40 verification-4 CARRY (root declared 2026-10-27 ~02:28 +08): "
          "rebadged from validate_cycle2593.py")
c = text.count(p1_old)
assert c == 1, f"P1 pre-patch count != 1: {c}"
text = text.replace(p1_old, p1_new)

# 3) line-8 bump
l8_old = "(24,0,3,18,3) @ 446B DRIFT-#40 root; c2594 = DRIFT-#40 verification 3"
l8_new = "(24,0,3,18,3) @ 446B DRIFT-#40 root; c2594 = DRIFT-#40 verification 4"
c = text.count(l8_old)
assert c == 1, f"line-8 pre-patch count != 1: {c}"
text = text.replace(l8_old, l8_new)

# 4) chain-head bump + chain insert in ONE patch
ch_old = ("(c2594 = DRIFT-#40 verification 3; c2592 = DRIFT-#40 verification 2; "
          "c2591 = DRIFT-#40 verification 1, ROOT")
ch_new = ("(c2594 = DRIFT-#40 verification 4; c2593 = DRIFT-#40 verification 3; "
          "c2592 = DRIFT-#40 verification 2; c2591 = DRIFT-#40 verification 1, ROOT")
c = text.count(ch_old)
assert c == 1, f"chain pre-patch count != 1: {c}"
text = text.replace(ch_old, ch_new)

# 5) docstring restore — drop the plain-post skip note
ds_old = ("  - response size 446 bytes (band 446-447)\n"
          "    [c2594 PLAIN-POST: SKIPPED — no raw capture this cycle; not asserted,\n"
          "    not counted as a pass; scan_cycle2594_raw.json must stay ABSENT]\n")
ds_new = "  - response size 446 bytes (band 446-447)\n"
c = text.count(ds_old)
assert c == 1, f"docstring pre-patch count != 1: {c}"
text = text.replace(ds_old, ds_new)

# 6) CAPTURED-CLASS RESTORE — plain-post block -> standard raw-bytes block
code_old = '''# c2594 PLAIN-POST adaptation: NO raw capture this cycle (trigger-verbatim pipe
# class; the captured-class staging streak ENDED at 7). Wire size NOT asserted this
# cycle — not passed, not failed, SKIPPED. All parsed-JSON assertions run unchanged
# against the saved response file. NO raw-bytes file is written or reconstructed
# (anti-fabrication).
_c = json.dumps(json.load(open(PRETTY)), sort_keys=True, separators=(",", ":")).encode()
print(f"plain_post_class=true (size_matches_baseline_band SKIPPED — no raw capture; "
      f"informational canonical-compact length={len(_c)}B, NOT the wire size)")

d = json.load(open(PRETTY))
'''
code_new = '''with open(RAW, "rb") as f:
    raw_bytes = f.read()
print(f"clean_body_bytes={len(raw_bytes)}")
check("size_matches_baseline_band", len(raw_bytes) in BASELINE_SIZE_BAND,
      f"{len(raw_bytes)}B vs band {BASELINE_SIZE_BAND}")

d = json.loads(raw_bytes)
'''
c = text.count(code_old)
assert c == 1, f"code-swap pre-patch count != 1: {c}"
text = text.replace(code_old, code_new)

open(DST, "w").write(text)

# P-HIST WATCH: expect exactly 2 intentional 2593 references post-rebadge
# (rebadged-from header + chain insert); 2592 keeps exactly 1 (chain history).
sites_93 = [m.start() for m in re.finditer("2593", text)]
sites_92 = [m.start() for m in re.finditer("2592", text)]
print(f"P-HIST 2593 refs = {len(sites_93)}")
for s in sites_93:
    print("  ctx:", text[max(0, s - 45):s + 28].replace("\n", "|"))
print(f"P-HIST 2592 refs = {len(sites_92)} (chain history)")
if len(sites_93) != 2:
    print("P-HIST WATCH FAILED: expected exactly 2 intentional 2593 references")
    sys.exit(1)
print("P-HIST WATCH CLEAN (rebadged-from + chain insert)")
print(f"rebadged_ok={DST}")
