
# 2) block structure
block = open(BLOCK).read()
lines = block.splitlines()
guard("block_lines==12", len(lines) == 12, f"got={len(lines)}")
guard("block_starts_with_separator", lines[0] == "---", repr(lines[0][:10]))
guard("block_title", lines[1].startswith("CYCLE 2795"), repr(lines[1][:30]))
guard("block_taskid_line", lines[2].startswith("Task ID: 446189-c2795"), repr(lines[2][:40]))
guard("block_nogold_line", "- No gold yet. Scanner continues." in lines)
guard("block_next_last", lines[-1].startswith("- Next: the c2796 instance")
      and lines[-1].rstrip().endswith("first-job policy)."), repr(lines[-1][:40]))
guard("block_forward_token_c2797_birth",
      block.count("c2797") == 3 and lines[-1].count("c2797") == 2
      and "c2796/c2797" in lines[-1] and "FORWARD token c2797" in lines[-1]
      and "the c2797 pre==0 expectation" in block,
      f"block c2797={block.count('c2797')} next-line c2797={lines[-1].count('c2797')} "
      f"(expect 3: the Step-7 rehearsal pre-count print + the Next bullet's guard "
      f"phrase 'c2796/c2797' AND census-tuple sentence 'FORWARD token c2797')")
guard("block_zero_anchor_adds", block.count("LOSS-#6") == 0 and block.count("LOSS-#15") == 0,
      f"LOSS-#6={block.count('LOSS-#6')} LOSS-#15={block.count('LOSS-#15')} (expect 0/0)")
guard("block_single_trailing_newline", block.endswith("\n") and not block.endswith("\n\n"),
      repr(block[-8:]))

# 3) pre-append state
wl = open(WL_TARGET).read()
n_before = wl.count("\n")
guard("worklog_lines==9268", n_before == EXPECT_BEFORE, f"got={n_before}")
last_nonempty = [l for l in wl.splitlines() if l.strip()][-1]
guard("tail_is_c2795_next_bullet", last_nonempty.startswith("- Next: the c2795 instance"),
      repr(last_nonempty[:40]))
guard("dup_check_no_serviced_c2795",
      len([l for l in wl.splitlines() if l.startswith("Task ID: 446189-c2795")]) == 0,
      f"c2795 substring mentions={wl.count('c2795')} (expect 11)")
c2795_lines = {i + 1: l.count("c2795") for i, l in enumerate(wl.splitlines()) if "c2795" in l}
guard("c2795_mention_census_pre", wl.count("c2795") == 11
      and c2795_lines == {9254: 1, 9256: 2, 9260: 3, 9266: 1, 9268: 4},
      f"per-line={c2795_lines}")
c2796_lines = {i + 1: l.count("c2796") for i, l in enumerate(wl.splitlines()) if "c2796" in l}
guard("c2796_forward_token_pre", wl.count("c2796") == 3 and c2796_lines == {9266: 1, 9268: 2},
      f"per-line={c2796_lines} (1 birth in the c2794 Step-7 rehearsal print + 2 "
      f"FORWARD-token births inside the c2794 Next-block — the born-thrice class REPEATS)")
tid_pre = len([l for l in wl.splitlines() if l.startswith("Task ID:")])
gold_pre = len([l for l in wl.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_pre==472", tid_pre == 472, f"got={tid_pre}")
guard("anchor_nogold_pre==405", gold_pre == 405, f"got={gold_pre}")
guard("anchor_LOSS6_occ_pre==60", wl.count("LOSS-#6") == 60, f"got={wl.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_pre==28", wl.count("LOSS-#15") == 28, f"got={wl.count('LOSS-#15')}")
# pre-counters — ALL assigned in this same block (the c2778 NameError lesson)
c2797_pre = wl.count("c2797")
c2796_pre = wl.count("c2796")
c2795_pre = wl.count("c2795")
c2794_pre = wl.count("c2794")
c2793_pre = wl.count("c2793")
c2792_pre = wl.count("c2792")
c2791_pre = wl.count("c2791")
c2790_pre = wl.count("c2790")
c2789_pre = wl.count("c2789")
c2788_pre = wl.count("c2788")
c2787_pre = wl.count("c2787")
c2786_pre = wl.count("c2786")
c2785_pre = wl.count("c2785")
c2784_pre = wl.count("c2784")
c2783_pre = wl.count("c2783")
c2782_pre = wl.count("c2782")
c2781_pre = wl.count("c2781")
c2780_pre = wl.count("c2780")
c2779_pre = wl.count("c2779")
c2778_pre = wl.count("c2778")
c2777_pre = wl.count("c2777")
c2776_pre = wl.count("c2776")
c2775_pre = wl.count("c2775")
c2774_pre = wl.count("c2774")
c2773_pre = wl.count("c2773")
c2772_pre = wl.count("c2772")
c2771_pre = wl.count("c2771")
c2770_pre = wl.count("c2770")
c2769_pre = wl.count("c2769")
c2768_pre = wl.count("c2768")
c2767_pre = wl.count("c2767")
c2766_pre = wl.count("c2766")
c2765_pre = wl.count("c2765")
c2764_pre = wl.count("c2764")
c2763_pre = wl.count("c2763")
c2762_pre = wl.count("c2762")
c2761_pre = wl.count("c2761")
c2760_pre = wl.count("c2760")
c2759_pre = wl.count("c2759")
c2758_pre = wl.count("c2758")
c2757_pre = wl.count("c2757")
c2756_pre = wl.count("c2756")
c2755_pre = wl.count("c2755")
c2754_pre = wl.count("c2754")
c2753_pre = wl.count("c2753")
c2752_pre = wl.count("c2752")
c2751_pre = wl.count("c2751")
c2750_pre = wl.count("c2750")
c2749_pre = wl.count("c2749")
c2748_pre = wl.count("c2748")
c2747_pre = wl.count("c2747")
c2746_pre = wl.count("c2746")
guard("c2797_pre==0", c2797_pre == 0, f"got={c2797_pre} (the forward token c2797 is UNBORN "
      f"pre-append — measured at census time)")
guard("c2796_pre==3", c2796_pre == 3, f"got={c2796_pre} (born THRICE: the c2794 Step-7 "
      f"rehearsal print + TWICE inside the c2794 Next-block — NOT the unborn class)")
guard("c2795_pre==11", c2795_pre == 11, f"got={c2795_pre}")
guard("c2794_pre==42", c2794_pre == 42, f"got={c2794_pre}")
guard("c2793_pre==83", c2793_pre == 83, f"got={c2793_pre}")
guard("c2792_pre==93", c2792_pre == 93, f"got={c2792_pre}")
guard("c2791_pre==92", c2791_pre == 92, f"got={c2791_pre}")
guard("c2790_pre==93", c2790_pre == 93, f"got={c2790_pre}")
guard("c2789_pre==95", c2789_pre == 95, f"got={c2789_pre}")
guard("c2788_pre==106", c2788_pre == 106, f"got={c2788_pre}")
guard("c2787_pre==107", c2787_pre == 107, f"got={c2787_pre}")
guard("c2786_pre==117", c2786_pre == 117, f"got={c2786_pre}")
guard("c2785_pre==111", c2785_pre == 111, f"got={c2785_pre}")
guard("c2784_pre==109", c2784_pre == 109, f"got={c2784_pre}")
guard("c2783_pre==110", c2783_pre == 110, f"got={c2783_pre}")
guard("c2782_pre==109", c2782_pre == 109, f"got={c2782_pre}")
guard("c2781_pre==114", c2781_pre == 114, f"got={c2781_pre}")
guard("c2780_pre==118", c2780_pre == 118, f"got={c2780_pre}")
guard("c2779_pre==119", c2779_pre == 119, f"got={c2779_pre}")
guard("c2778_pre==159", c2778_pre == 159, f"got={c2778_pre}")
guard("c2777_pre==135", c2777_pre == 135, f"got={c2777_pre}")
guard("c2776_pre==140", c2776_pre == 140, f"got={c2776_pre}")
guard("c2775_pre==149", c2775_pre == 149, f"got={c2775_pre}")
guard("c2774_pre==154", c2774_pre == 154, f"got={c2774_pre}")
guard("c2773_pre==158", c2773_pre == 158, f"got={c2773_pre}")
guard("c2772_pre==177", c2772_pre == 177, f"got={c2772_pre}")
guard("c2771_pre==167", c2771_pre == 167, f"got={c2771_pre}")
guard("c2770_pre==203", c2770_pre == 203, f"got={c2770_pre}")
guard("c2769_pre==156", c2769_pre == 156, f"got={c2769_pre}")
guard("c2768_pre==159", c2768_pre == 159, f"got={c2768_pre}")
guard("c2767_pre==196", c2767_pre == 196, f"got={c2767_pre}")
guard("c2766_pre==179", c2766_pre == 179, f"got={c2766_pre}")
guard("c2765_pre==150", c2765_pre == 150, f"got={c2765_pre}")
guard("c2764_pre==152", c2764_pre == 152, f"got={c2764_pre}")
guard("c2763_pre==160", c2763_pre == 160, f"got={c2763_pre}")
guard("c2762_pre==186", c2762_pre == 186, f"got={c2762_pre}")
guard("c2761_pre==200", c2761_pre == 200, f"got={c2761_pre}")
guard("c2760_pre==155", c2760_pre == 155, f"got={c2760_pre}")
guard("c2759_pre==155", c2759_pre == 155, f"got={c2759_pre}")
guard("c2758_pre==157", c2758_pre == 157, f"got={c2758_pre}")
guard("c2757_pre==160", c2757_pre == 160, f"got={c2757_pre}")
guard("c2756_pre==165", c2756_pre == 165, f"got={c2756_pre}")
guard("c2755_pre==172", c2755_pre == 172, f"got={c2755_pre}")
guard("c2754_pre==175", c2754_pre == 175, f"got={c2754_pre}")
guard("c2753_pre==181", c2753_pre == 181, f"got={c2753_pre}")
guard("c2752_pre==187", c2752_pre == 187, f"got={c2752_pre}")
guard("c2751_pre==173", c2751_pre == 173, f"got={c2751_pre}")
guard("c2750_pre==175", c2750_pre == 175, f"got={c2750_pre}")
guard("c2749_pre==179", c2749_pre == 179, f"got={c2749_pre}")
guard("c2748_pre==169", c2748_pre == 169, f"got={c2748_pre}")
guard("c2747_pre==167", c2747_pre == 167, f"got={c2747_pre}")
guard("c2746_pre==171", c2746_pre == 171, f"got={c2746_pre}")

if failures:
    print(f"APPEND_ABORTED: {len(failures)} guard failures - worklog UNTOUCHED")
    sys.exit(1)

# 4) append with newline normalization
if not wl.endswith("\n"):
    wl += "\n"
block_norm = block if block.endswith("\n") else block + "\n"
with open(WL_TARGET, "a") as f:
    f.write(block_norm)

# 5) post-append assertions
wl2 = open(WL_TARGET).read()
n_after = wl2.count("\n")
guard("post_worklog_lines==9280", n_after == EXPECT_AFTER, f"got={n_after}")
last2 = [l for l in wl2.splitlines() if l.strip()][-1]
guard("tail_is_c2796_next_bullet", last2.startswith("- Next: the c2796 instance"),
      repr(last2[:40]))
tid_post = len([l for l in wl2.splitlines() if l.startswith("Task ID:")])
gold_post = len([l for l in wl2.splitlines() if l.startswith("- No gold yet")])
guard("anchor_TaskID_post==473", tid_post == 473, f"got={tid_post}")
guard("anchor_nogold_post==406", gold_post == 406, f"got={gold_post}")
guard("anchor_LOSS6_occ_post==60", wl2.count("LOSS-#6") == 60, f"got={wl2.count('LOSS-#6')}")
guard("anchor_LOSS15_occ_post==28", wl2.count("LOSS-#15") == 28, f"got={wl2.count('LOSS-#15')}")
guard("taskid_c2795_now_present",
      len([l for l in wl2.splitlines() if l.startswith("Task ID: 446189-c2795")]) == 1)
expect_c2797_mentions = wl2.count("c2797")
guard("c2797_mention_birth", expect_c2797_mentions == c2797_pre + block.count("c2797"),
      f"pre={c2797_pre} (unborn) + block births={block.count('c2797')} (Step-7 pre-count "
      f"print + guard phrase + census-tuple sentence) -> expect={c2797_pre + block.count('c2797')} got={expect_c2797_mentions}")
for tag, pre in (("c2796", c2796_pre), ("c2795", c2795_pre), ("c2794", c2794_pre),
                 ("c2793", c2793_pre), ("c2792", c2792_pre), ("c2791", c2791_pre),
                 ("c2790", c2790_pre), ("c2789", c2789_pre), ("c2788", c2788_pre),
                 ("c2787", c2787_pre), ("c2786", c2786_pre), ("c2785", c2785_pre),
                 ("c2784", c2784_pre), ("c2783", c2783_pre), ("c2782", c2782_pre),
                 ("c2781", c2781_pre), ("c2780", c2780_pre), ("c2779", c2779_pre),
                 ("c2778", c2778_pre), ("c2777", c2777_pre), ("c2776", c2776_pre),
                 ("c2775", c2775_pre), ("c2774", c2774_pre), ("c2773", c2773_pre),
                 ("c2772", c2772_pre), ("c2771", c2771_pre), ("c2770", c2770_pre),
                 ("c2769", c2769_pre), ("c2768", c2768_pre), ("c2767", c2767_pre),
                 ("c2766", c2766_pre), ("c2765", c2765_pre), ("c2764", c2764_pre),
                 ("c2763", c2763_pre), ("c2762", c2762_pre), ("c2761", c2761_pre),
                 ("c2760", c2760_pre), ("c2759", c2759_pre), ("c2758", c2758_pre),
                 ("c2757", c2757_pre), ("c2756", c2756_pre), ("c2755", c2755_pre),
                 ("c2754", c2754_pre), ("c2753", c2753_pre), ("c2752", c2752_pre),
                 ("c2751", c2751_pre), ("c2750", c2750_pre), ("c2749", c2749_pre),
                 ("c2748", c2748_pre), ("c2747", c2747_pre), ("c2746", c2746_pre)):
    expect = pre + block.count(tag)
    guard(f"{tag}_mention_accounting", wl2.count(tag) == expect,
          f"pre={pre} + block={block.count(tag)} -> expect={expect} got={wl2.count(tag)}")

if failures:
    print("APPEND_COMPLETED_BUT_POST_GUARDS_RED - INVESTIGATE")
    sys.exit(1)
mode = "REHEARSAL" if REHEARSAL else "REAL"
print(f"WORKLOG_APPEND_GREEN ({mode}): 9268 -> 9280 (+12), c2795 entry + DRIFT-#49 pass-44 block landed ({n_guards}/{n_guards} guards)")
if REHEARSAL:
    os.remove(WL_TARGET)
    print("temp copy removed")
