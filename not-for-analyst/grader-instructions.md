# Grader instructions

You grade one blind analysis of a zebrafish liver single-cell dataset. Another AI agent (the analyst) did the analysis without seeing the paper. Your job is to compare what the analyst wrote against the answer key, item by item, and show your evidence.

You do not know which system produced the report. Do not guess. Another grader is grading the same report independently; do not look for or use their work.

## Inputs

- `scoring-key.md`: read sections 5, 6, 7 and 8 in full before you start.
- `scorecard.csv`: the template you fill in.
- For Run B: section 11 of `scoring-key.md` and the analyst's processing log.
- The analyst's outputs, in a folder such as `report_A/`: `part1_frozen/` (the Part 1 report and claim list as they were when Part 1 ended, with checksums) and the final `outputs/` (Part 2 and 3 answers, summary figure, code). Grade Part 1 from `part1_frozen/` only.

## Rules

1. Grade only what the analyst wrote. Quote the analyst's claim number and words for every hit or partial. Do not give credit for something a figure might show unless the analyst states it.
2. Do not use outside knowledge to fill gaps. The key is the reference. Do not look anything up.
3. When torn between hit and partial, choose partial and say why. When torn between partial and miss, choose miss and say why.
4. Grade Part 1 using only Part 1 answers and claims. Grade Part 2 using Part 2 answers. An item first hit in Part 1 is a Part 1 hit even if Part 2 repeats it.
5. A claim with low confidence still counts if the content is right. A correct claim the analyst later retracts does not count.
6. Do not run the analyst's code unless Bhadri asks. If code or outputs are missing, say so.

## Steps

1. **Items.** For each row in `scorecard.csv`, apply that item's "Hit" rule from section 6. Fill `part1_result` and `part2_result` with hit, partial or miss. In `notes`, give claim numbers and a one-line reason.
2. **Major false claims.** Check every analyst claim against the list in section 5. List each match with the claim number, quote, and which rule it breaks. If unsure, mark it "uncertain".
3. **Extra claims.** List every analyst claim not matched to an item. For each, propose plausible, wrong or unknown, with a one-line reason. Flag any that might be a major false claim.
4. **Part 3.** Score each proposed experiment (up to 5) against section 7: 2 if it matches one there in substance, 1 if plausible but not done (mark "needs Prasanna"), 0 if infeasible or not testing a stated claim.
5. **Totals.**
   - Core hits: number of the 6 core items listed in section 5 of `scoring-key.md` with a hit in Part 1 or Part 2.
   - Part 1 core hits: the same, Part 1 only.
   - Weighted score: sum of weights for hits, half weight for partials.
   - Go or no-go: go if core hits are 3 or more and there is no major false claim. If a possible major false claim is "uncertain", write "go pending Prasanna".

6. **Run B only.** If the analyst started from raw reads, also grade process items P1 to P5 in section 11 of the key: hit, partial, miss or n/a, with evidence from the processing log. Write them to `process.csv` (item, result, evidence, reason). They are reported separately and do not change the go or no-go.

## Outputs

Write these to the folder Bhadri gives you:

- `scorecard.csv`, filled in.
- `major_false_claims.csv`: claim number, quote, rule, certain or uncertain.
- `extra_claims.csv`: claim number, quote, proposed label, reason, possible major (yes or no).
- `part3.csv`: experiment number, short description, score, matched key item, needs Prasanna (yes or no).
- `process.csv` (Run B only): item, result (hit, partial, miss or n/a), evidence, reason.
- `summary.md`: one page in plain sentences. Go or no-go, core hits, Part 1 core hits, weighted score, the 3 strongest and 3 weakest points, and anything that needs Prasanna.

## Reconciler (a separate agent, run after both graders)

Inputs: both graders' outputs. Do not regrade from scratch.

1. Compare the two `scorecard.csv` files cell by cell. Where they agree, that is final. Where they differ, list the item, both verdicts, both reasons.
2. Merge the major false claim lists. Any claim either grader flagged goes to Prasanna.
3. Merge extra claims. Where the proposed labels differ, list both.
4. Merge Part 3 scores the same way.
5. Run B only: compare the two `process.csv` files the same way and list any disagreements in `for_prasanna.md`. They do not change the go or no-go.
6. Write `reconciled_scorecard.csv` (agreed cells filled, disagreements marked "disputed"), and `for_prasanna.md`. That file is a short list, in plain sentences, of everything that needs a biologist: disputed items, possible major false claims, extra claims, and Part 3 items marked "needs Prasanna". Put the most important first.
