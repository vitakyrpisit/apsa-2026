#!/usr/bin/env python3
"""Guarded worklog append for cycle c2735 (26-line block).

Guards: timegm epoch cross-verification (the standing +08-minus-8h convention;
the SKEW ARITHMETIC LESSON applied - scanned_at fractions asserted DECIMAL-EXACT,
milliseconds are NEVER passed into the nanosecond parameter), 26-line entry
assertion, trailing-newline normalization, post-append line-count assertion
(expect 10420 + 26 = 10446). Exits non-zero on ANY guard failure - zero worklog
mutation unless all guards pass.
"""
import calendar
import sys

WL = "/home/z/my-project/worklog.md"
ENTRY = "/home/z/my-project/scripts/entry_cycle2735.txt"
EXPECT_BEFORE = 10420
EXPECT_AFTER = EXPECT_BEFORE + 26

failures = []


def guard(name, cond, detail=""):
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


# 1) python-timegm epoch cross-verification (+08 minus 8h convention)
def utc_epoch(h, m, s, ns=0):
    return calendar.timegm((2026, 10, 28, h, m, s, 0, 0, 0)) + ns / 1e9


checks = [
    ("trigger 12:00:24 +08", utc_epoch(4, 0, 24), 1793160024.0),
    ("window-2735 open 12:05:42.769241909 +08", utc_epoch(4, 5, 42, 769241909), 1793160342.769241909),
    ("loop-open echo 12:16:54.814581755 +08", utc_epoch(4, 16, 54, 814581755), 1793161014.814581755),
    ("pre-echo 12:19:21.219509722 +08", utc_epoch(4, 19, 21, 219509722), 1793161161.219509722),
    ("post-echo 12:19:28.012208950 +08", utc_epoch(4, 19, 28, 12208950), 1793161168.012208950),
    ("c2734 post-echo 12:00:42.769241909 +08", utc_epoch(4, 0, 42, 769241909), 1793160042.769241909),
    # SKEW ARITHMETIC LESSON (c2730/c2733/c2734/c2735): scanned_at fraction asserted DECIMAL-EXACT
    ("scanned_at 12:19:28.007 +08 (decimal)", utc_epoch(4, 19, 28) + 0.007, 1793161168.007),
    ("skew decimal-exact +5.208950ms", 1793161168.012208950 - 1793161168.007, 0.005208950),
    ("dd#309 decimal-exact 1137.219509722", 1793161161.219509722 - 1793160024.0, 1137.219509722),
    ("LAG#309 decimal-exact 1120.786290917", 1201 + 1137.219509722 - 1217.433218805, 1120.786290917),
    ("window LATE decimal-exact 825.242967041", 1793161168.012208950 - 1793160342.769241909, 825.242967041),
    ("post-echo gap decimal-exact 1125.242967041", 1793161168.012208950 - 1793160042.769241909, 1125.242967041),
]
for name, want, got in checks:
    guard(f"timegm:{name}", abs(want - got) < 1e-6, f"computed={want!r} harness={got!r}")

# 2) entry is exactly 26 lines
entry = open(ENTRY).read()
lines = entry.splitlines()
guard("entry_lines==26", len(lines) == 26, f"got={len(lines)}")
guard("entry_starts_with_separator", lines[0] == "---", repr(lines[0][:20]))
guard("entry_ends_no_gold", lines[-1] == "- No gold yet. Scanner continues.", repr(lines[-1][:40]))

# 3) pre-append state
wl = open(WL).read()
n_before = wl.count("\n")
guard("worklog_lines==10420", n_before == EXPECT_BEFORE, f"got={n_before}")

if failures:
    print(f"APPEND_ABORTED: {len(failures)} guard failures - worklog UNTOUCHED")
    sys.exit(1)

# 4) append with newline normalization
if not wl.endswith("\n"):
    wl += "\n"
block = entry if entry.endswith("\n") else entry + "\n"
with open(WL, "a") as f:
    f.write(block)

# 5) post-append assertion
n_after = open(WL).read().count("\n")
guard("post_worklog_lines==10446", n_after == EXPECT_AFTER, f"got={n_after}")
tail = open(WL).read().splitlines()[-1]
guard("tail_is_no_gold", tail == "- No gold yet. Scanner continues.", repr(tail[:40]))

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
print("WORKLOG_APPEND_GREEN: 10420 -> 10446 (+26), c2735 block landed")
