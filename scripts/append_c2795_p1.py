#!/usr/bin/env python3
"""Guarded worklog append for the c2795 entry (12 lines).

Follows the append_cycle2794.py precedent — ALL asserts precede the
mutation; any failure -> APPEND_ABORTED, worklog UNTOUCHED. The Decimal-exact
guard design is the last line of defense (the c2766/c2767/c2769/c2770/c2773/
c2774/c2775/c2777-rebadge/c2777-append/c2778-append/c2780-append abort
precedent class). The ledger arithmetic stays in the DECIMAL class: every
ns-decomposition check is Decimal-exact or Decimal-with-1e-6-tolerance on the
utc-derived values. THE C2778 ABORT LESSON STRUCTURALIZED: every pre-counter
variable is assigned in the SAME statement block before any guard references
it (the c2778 attempt-1 NameError class is impossible here), and a REHEARSAL
mode (APPEND_REHEARSAL=1) runs the full guard battery against a
byte-identical temp copy BEFORE the real run — the attempt counter counts
REAL runs only. Guards: python-timegm epoch cross-verification (Decimal-class
checks incl. the dd/INTERVAL/LAG/LATE ledger arithmetic, all echo
decompositions, the stamp-gap/token-gap/token-vs-stamp cadence triple, the
window-2795 EPOCH-governs render check, the window-2796 prophecy check, and
the queue-print check — the c2766 attempt-1 abort lesson: the SKEW check must
use the EPOCH-governs print's own ns decomposition, the ISO/EPOCH clock reads
differ ~0.7ms on the post-echo), block structure (12 lines: separator, title,
standard Task ID line, Steps 1-7, no-gold, Next bullet), the FORWARD-token
guard (c2797 = 3 block births: the Step-7 rehearsal pre-count print 'the
c2797 pre==0 expectation' + the Next bullet's guard phrase 'c2796/c2797' AND
census-tuple sentence 'FORWARD token c2797' — the c2767..c2795 forward-token
lessons; NOTE the c2797 pre-count is 0 (unborn) while the c2796 pre-count is
3 (born: the c2794 Step-7 rehearsal print + TWICE inside the c2794
Next-block) — the c2783 c2788-pre==2 class EVOLVED: the c2796 forward token
was born THRICE across the c2794 block, measured at census time per-line
{9266: 1, 9268: 2}, NOT the unborn class), zero adds to the two standing
post-#6/post-#15 anchor series (OCCURRENCE counting — the standing method),
pre-state (9268 lines, tail = the c2795 Next bullet, zero serviced c2795
entries, c2795 mention census per-line {9254: 1, 9256: 2, 9260: 3, 9266: 1,
9268: 4} total 11, c2796 = 3 per-line {9266: 1, 9268: 2}, anchors 472/405/60/
28), post-state (9280 lines, tail = the c2796 Next bullet, anchors 473/406/
60/28). Zero mid-line writes (append at EOF only).
"""
import calendar
import os
import shutil
import sys
from decimal import Decimal as D

WL = "/home/z/my-project/worklog.md"
BLOCK = "/home/z/my-project/scripts/entry_cycle2795.txt"
REHEARSAL = os.environ.get("APPEND_REHEARSAL") == "1"
WL_TARGET = WL + ".rehearsal_tmp" if REHEARSAL else WL
EXPECT_BEFORE = 9268
EXPECT_AFTER = EXPECT_BEFORE + 12

failures = []
n_guards = 0


def guard(name, cond, detail=""):
    global n_guards
    n_guards += 1
    print(f"{'ok' if cond else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


print(f"{'*** REHEARSAL MODE (temp copy) ***' if REHEARSAL else '*** REAL RUN ***'}")
if REHEARSAL:
    shutil.copyfile(WL, WL_TARGET)
    print(f"temp copy staged: {WL_TARGET}")

# 1) python-timegm epoch cross-verification (Decimal-class checks)
def utc_epoch(y, mo, d, h, mi, s, ns=0):
    return calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0)) + ns / 1e9


POST = D("1793316379.170480455")    # c2795 post-echo (EPOCH-governs)
SCAN = D("1793316379.163")          # c2795 scanned_at (decimal)
TRIG = D("1793315471.000")          # c2795 trigger stamp (07:11:11 +08)
WIN = D("1793316092.663933005")     # window-2795 open (c2794 prophecy EPOCH)
ECHO = D("1793316141.062851709")    # loop echo #516 POST read (EPOCH-governs)
ECHO_ISO = D("1793316141.062208970")  # loop echo #516 ISO read FIRST (the bracket)
PRE = D("1793316377.499476469")     # c2795 capture pre-echo (EPOCH-governs)
C2794_SCAN = D("1793315792.658")    # c2794 scanned_at
C2794_POST = D("1793315792.663933005")  # c2794 post-echo
C2794_CLOSE = D("1793316031.000")   # c2794 close fb1d1d1 (23:20:31Z)
C2794_FOREIGN = D("1793316048.000")  # foreign 4207111 (23:20:48Z)
C2794_TRIG = D("1793314871.000")    # c2794 trigger stamp (07:01:11 +08)
C2794_ECHO = D("1793315790.726705467")  # c2794 loop echo #515 (23:16:30.726705467)
C2794_ECHO_ISO = D("1793315790.725965515")  # c2794 echo ISO bracket
C2794_PRE = D("1793315790.730105682")  # c2794 capture pre-echo (EPOCH-governs)
C2793_SCAN = D("1793315166.899")    # c2793 scanned_at
C2793_CLOSE = D("1793315434.000")   # c2793 close a27965c (23:10:34Z)
C2793_FOREIGN = D("1793315452.000")  # foreign 4477b73 (23:10:52Z)
TOKEN = D("1793316000.000")         # token 0720 (07:20:00 +08)
C2794_TOKEN = D("1793315400.000")   # token 0710 (07:10:00 +08)


def dec_epoch(y, mo, d, h, mi, s, ns=0):
    """utc_epoch routed through str() -> Decimal (1e-6-safe at this magnitude)."""
    return D(str(utc_epoch(y, mo, d, h, mi, s, ns)))


dec_checks = [
    ("trigger stamp 07:11:11 +08 = 1793315471.000", dec_epoch(2026, 10, 29, 23, 11, 11), TRIG),
    ("c2794 trigger stamp 07:01:11 +08 = 1793314871.000", dec_epoch(2026, 10, 29, 23, 1, 11), C2794_TRIG),
    ("stamp-gap 600.000s by stamp (07:01:11 -> 07:11:11; the 600 print REPEATS, 24 priors)", TRIG - C2794_TRIG, D("600.000")),
    ("token-gap 600.000s by token (0710 -> 0720; the 600 print REPEATS, 12 priors)", TOKEN - C2794_TOKEN, D("600.000")),
    ("token-vs-stamp +529.000 (07:11:11 -> 07:20:00; the +529 print REPEATS)", TOKEN - TRIG, D("529.000")),
    ("c2794 close fb1d1d1 23:20:31Z = 1793316031.000", dec_epoch(2026, 10, 29, 23, 20, 31), C2794_CLOSE),
    ("foreign 4207111 23:20:48Z = 1793316048.000", dec_epoch(2026, 10, 29, 23, 20, 48), C2794_FOREIGN),
    ("c2793 close a27965c 23:10:34Z = 1793315434.000", dec_epoch(2026, 10, 29, 23, 10, 34), C2793_CLOSE),
    ("foreign 4477b73 23:10:52Z = 1793315452.000", dec_epoch(2026, 10, 29, 23, 10, 52), C2793_FOREIGN),
    ("c2794 loop echo EPOCH 1793315790.726705467 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 30, 726705467), C2794_ECHO),
    ("c2794 echo ISO-bracket 1793315790.725965515 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 16, 30, 725965515), C2794_ECHO_ISO),
    ("c2794 capture pre-echo EPOCH 1793315790.730105682 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 30, 730105682), C2794_PRE),
    ("c2794 post-echo ISO 23:16:32.663244336 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 16, 32, 663244336), D("1793315792.663244336")),
    ("c2794 post-echo EPOCH 1793315792.663933005 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 16, 32, 663933005), C2794_POST),
    ("c2794 scanned_at 23:16:32.658 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 16, 32) + D("0.658"), C2794_SCAN),
    ("loop echo #516 ISO integer second 23:22:21 +0000", dec_epoch(2026, 10, 29, 23, 22, 21), D("1793316141.000")),
    ("loop echo #516 EPOCH 1793316141.062851709 (EPOCH-governs POST read)", dec_epoch(2026, 10, 29, 23, 22, 21, 62851709), ECHO),
    ("loop echo #516 ISO-bracket read 1793316141.062208970 (the ISO read FIRST)", dec_epoch(2026, 10, 29, 23, 22, 21, 62208970), ECHO_ISO),
    ("capture pre-echo EPOCH 1793316377.499476469 (epoch ns, EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 26, 17, 499476469), PRE),
    ("pre-echo ISO 23:26:17.498822768 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 26, 17, 498822768), D("1793316377.498822768")),
    ("post-echo ISO 23:26:19.169778054 +0000 (epoch ns)", dec_epoch(2026, 10, 29, 23, 26, 19, 169778054), D("1793316379.169778054")),
    ("post-echo EPOCH 1793316379.170480455 (EPOCH-governs)", dec_epoch(2026, 10, 29, 23, 26, 19, 170480455), POST),
    ("scanned_at 23:26:19.163 +0000 (decimal)", dec_epoch(2026, 10, 29, 23, 26, 19) + D("0.163"), SCAN),
    ("window-2795 open 07:21:32.663933005 +08 (EPOCH-governs render)", dec_epoch(2026, 10, 29, 23, 21, 32, 663933005), WIN),
    ("window-2796 open = post-echo + 300.000", POST + D("300.000"), D("1793316679.170480455")),
    ("echo post-c2794-post-echo +348.398818704", ECHO - C2794_POST, D("348.398818704")),
]
exact_checks = [
    ("skew decimal-exact +7.480455ms (EPOCH-governs decomposition; SUB-10 extends m3)", POST - SCAN, D("0.007480455")),
    ("echo_vs_window +48.398818704 (POST-WINDOW extends m2; the PRE-WINDOW flip did NOT fire)", ECHO - WIN, D("48.398818704")),
    ("dd#369 = +286.505000000 (interval 586.505 - 300 contract; single contract subtraction — the c2766 attempt-1 double-300 abort lesson; verified against the dd#367 print 444.746 - 300 = 144.746 and the dd#368 print 625.759 - 300 = 325.759)", SCAN - C2794_SCAN - D("300.000"), D("286.505")),
    ("dd formula re-verification: 444.746 - 300 = 144.746", D("444.746") - D("300.000"), D("144.746")),
    ("dd formula re-verification: 625.759 - 300 = 325.759", D("625.759") - D("300.000"), D("325.759")),
    ("INTERVAL#369 = 908.163", SCAN - TRIG, D("908.163")),
    ("LAG#369 = INTERVAL + dd - dd#368 = +868.909", (SCAN - TRIG) + (SCAN - C2794_SCAN - D("300.000")) - D("325.759"), D("868.909")),
    ("LATE#369 = trigger - window-open = -621.663933005", TRIG - WIN, D("-621.663933005")),
    ("CAPTURE_vs_window +286.506547450 (POST-WINDOW; echo POST — BOTH-POST extends m2)", POST - WIN, D("286.506547450")),
    ("capture-vs-echo +238.107628746", POST - ECHO, D("238.107628746")),
    ("capture post-c2794-post-echo +586.506547450", POST - C2794_POST, D("586.506547450")),
    ("echo post-c2794-close +110.062851709 (fb1d1d1 at 23:20:31)", ECHO - C2794_CLOSE, D("110.062851709")),
    ("echo post-foreign-4207111 +93.062851709 (23:20:48)", ECHO - C2794_FOREIGN, D("93.062851709")),
    ("stamp-to-echo 670.062851709 (the deepest print 1025.631018606 STANDS)", ECHO - TRIG, D("670.062851709")),
    ("trigger predates the c2794 loop echo #515 by 319.726705467s (the trigger landed INSIDE the c2794 servicing window, pre-echo pre-capture)", C2794_ECHO - TRIG, D("319.726705467")),
    ("trigger predates the c2794 capture pre-echo by 319.730105682s", C2794_PRE - TRIG, D("319.730105682")),
    ("trigger predates the c2794 post-echo by 321.663933005s", C2794_POST - TRIG, D("321.663933005")),
    ("trigger predates window-2795 open by 621.663933005s", WIN - TRIG, D("621.663933005")),
    ("c2794 close POSTDATES the trigger by 560.000s (fb1d1d1 at 23:20:31)", C2794_CLOSE - TRIG, D("560.000")),
    ("foreign 4207111 POSTDATES the trigger by 577.000s (23:20:48)", C2794_FOREIGN - TRIG, D("577.000")),
    ("trigger postdates c2793 close by 37.000s (a27965c at 23:10:34)", TRIG - C2793_CLOSE, D("37.000")),
    ("trigger postdates the foreign 4477b73 by 19.000s (23:10:52)", TRIG - C2793_FOREIGN, D("19.000")),
    ("c2794 close landed 31.000s AFTER the token second (23:20:31 vs 23:20:00)", C2794_CLOSE - TOKEN, D("31.000")),
    ("foreign 4207111 landed 48.000s AFTER the token second (23:20:48)", C2794_FOREIGN - TOKEN, D("48.000")),
]
for name, want, got in dec_checks:
    guard(f"timegm:{name}", abs(want - got) < D("0.000001"), f"computed={want} harness={got}")
for name, want, got in exact_checks:
    guard(f"timegm:{name}", want == got, f"computed={want} harness={got}")
