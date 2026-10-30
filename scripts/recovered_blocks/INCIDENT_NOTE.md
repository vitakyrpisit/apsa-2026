# INCIDENT NOTE — workspace rollback discovered at the c2931 trigger (2026-10-30 22:41:30 +08)

## What happened

- Last verified-good state of this trigger stream: the c2930 close, commit `e4fbde1`,
  landed at 14:36:58 +08 with worklog 10900 lines EXACT, anchors 608/541, tree clean
  (verified by `git status --porcelain` empty at close).
- At the c2931 trigger pre-scan (22:41:41 +08) the workspace was found ROLLED BACK:
  - worklog.md = 9580 lines (the c2820 close state), anchors ^Task ID: 498 / ^- No gold yet: 431
  - git HEAD = `40957a2` ("4571051e-bd1d-4755-b385-ad7f4eceef0b-cron"), a foreign cron
    commit atop `ea1ef47` (the c2820 close, "concise-block convention adopted")
  - `.git/logs/HEAD` (reflog) ends at 2026-10-30T05:04:59Z — none of the c2821..c2930
    commits appear in it
- Working tree carried 1179 tracked restore artifacts (mostly scripts/__pycache__/*.pyc
  plus old-era append/rehearsal outputs), all reverted to the restored HEAD state with
  `git restore .` before any new work; worklog.md itself was clean vs the restored HEAD.

## Loss extent (measured, not assumed)

- Object database: every sampled close of the lost span — `341d427` (c2909), `cbebbfe`
  (c2910), `d77e39a` (c2911), `345b65f` (c2912), `6807d6f` (c2929), `6bbfd8d` (c2928),
  `e4fbde1` (c2930) — returns "fatal: Not a valid object name".
- `git fsck --unreachable` returns NOTHING (no dangling objects at all).
- `scripts/scan_cycle29*.json` for the lost span: absent from disk (Glob returned none).
- Conclusion: the c2821..c2930 git history and scan archives are UNRECOVERABLE from disk.

## What survives

1. `scripts/recovered_blocks/blocks_c2908_to_c2930.txt` — 23 verbatim 12-line blocks
   (c2908, c2909, c2910 read back from the ledger before the rollback was discovered;
   c2911..c2930 authored byte-for-byte by the serving session and still present in the
   session record).
2. The per-cycle data table below for c2880..c2907, retained from the serving session's
   summary record (trigger time +08, token offset, trigger->scan latency, scan duration,
   closing commit hash).
3. NOTHING survives for c2821..c2879 beyond the structural facts (each cycle appended
   exactly 12 lines and +1/+1 anchors; all no-gold; market frozen at 18 scam-pattern
   tasks). These blocks are NOT reconstructed — no surviving measured text exists, and
   fabricating them would violate the honest-report convention.

## Retained per-cycle table, c2880..c2907 (from the session summary record)

| cycle | trigger (+08) | offset | trigger->scan | scan_ms | close commit |
|-------|---------------|--------|---------------|---------|--------------|
| c2880 | 18:21:26 | -26s | +31.160s | 2389 | 6325ab1 |
| c2881 | 18:26:26 | -26s | +10.416s | 2585 | c5e9a0f |
| c2882 | 18:31:46 | -46s | +12.313s | 1725 | 6f942aa |
| c2883 | 18:41:27 | -27s | +16.501s | 1695 | dac8ab6 |
| c2884 | 18:46:27 | -27s | +12.288s | 2848 | 2d27c84 |
| c2885 | 18:51:26 | -26s | +10.733s | 1973 | 827b849 |
| c2886 | 18:56:26 | -26s | +10.101s | 2015 | b99015b |
| c2887 | 19:01:27 | -27s | +10.781s | 1956 | 16a3c0e |
| c2888 | 19:06:26 | -26s | +11.488s | 2301 | fd8a6ac |
| c2889 | 19:11:26 | -26s | +11.902s | 1908 | 187c475 |
| c2890 | 19:16:26 | -26s | +12.323s | 2226 | 640a8c4 |
| c2891 | 19:21:27 | -27s | +13.547s | 2935 | e825678 |
| c2892 | 19:26:27 | -27s | +10.939s | 1835 | 3dd45b4 |
| c2893 | 19:31:27 | -27s | +9.417s | 2119 | f7e8ea5 |
| c2894 | 19:36:27 | -27s | +11.287s | 2346 | 3c53c93 |
| c2895 | 19:41:27 | -27s | +12.622s | 2264 | 004a782 |
| c2896 | 19:46:27 | -27s | +12.602s | 1696 | e2fa6fe |
| c2897 | 19:51:27 | -27s | +12.945s | 2022 | bb6e43a |
| c2898 | 19:56:27 | -27s | +14.582s | 2186 | dbf8784 |
| c2899 | 20:01:27 | -27s | +13.003s | 2464 | 5fd66b9 |
| c2900 | 20:06:27 | -27s | +15.438s | 2092 | 60771ec |
| c2901 | 20:11:27 | -27s | +13.106s | 2058 | 63b923d |
| c2902 | 20:16:28 | -28s | +12.947s | 1932 | 3af5049 |
| c2903 | 20:21:28 | -28s | +13.638s | 2203 | 0fd7829 |
| c2904 | 20:26:28 | -28s | +13.136s | 2049 | beb8ad0 |
| c2905 | 20:31:29 | -29s | +16.570s | 1998 | e0219b5 |
| c2906 | 20:36:28 | -28s | +12.896s | 1945 | ec2622c |
| c2907 | 20:41:28 | -28s | +9.994s | 1912 | 6e6feae |

Known milestone markers of the lost span (from the same record): no-gold streak passed
500 anchor at c2889, 70 consecutive at c2890, 80 at c2900, 90 at c2910; ledger crossed
10600 at c2905; ledger progression across the span was +12 lines per cycle throughout,
all EXACT-verified at each close.

## Position on the numbering

The incident block is numbered c2931 because c2821..c2930 were all actually served in
the trigger stream (no cycle number was skipped); reusing c2821 would create a second,
false record for a number that already has history. The on-disk ledger's Next line
("c2821") belongs to the restored c2820-era snapshot and is superseded by this note.
Future prescans must check BOTH for external advance (c2879 precedent) AND for further
regression (this incident class).
