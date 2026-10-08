# Eski run instructions (for everyone except the analyst)

The Eski run repeats the blind replication test on a second public dataset, Eski et al. 2025 (GEO GSE272484). It then probes a new question, macrophages, which the paper does not analyze. Prasanna and Manjari set the design on Oct 8, 2026.

**Order of aims.** First, check that the agent independently recovers the paper's findings. Second, ask the new macrophage questions and judge whether the biology makes sense.

**Public and private.**
- **Public:** the brief, questions, sample sheet, setup script and these instructions can live in both repos.
- **Private repo only:** the answer key (`eski-scoring-key.md`), the scorecard, every grader, reconciler and comparison output, and all macrophage results. Never put them in the public repo, public Actions logs or public artifacts.

## Roles and order

| Step | Who | Network | Reads | Writes |
|---|---|---|---|---|
| E1 | Coordinator | Yes, for setup only | This file, `setup_eski.py` | Analyst folder, round 2 folder |
| E2 | Analyst, Part 1 | No | Only the analyst folder | `outputs/`, then frozen |
| E3 | Analyst, Parts 2 and 3 | No | Analyst folder plus `followup-questions.md` and `round2/` | More files in `outputs/` |
| E4 | Two graders, then a reconciler | No | Report, answer key | Scorecards, `for_prasanna.md` |
| E5 | Evidence reviewer | No | Packaged report | `evidence_review/` |
| E6 | Literature agent | PubMed and bioRxiv only | Packaged report | `literature/` |
| E7 | Macrophage comparison | No | Eski report, Run C report | `macrophage_comparison/` |
| E8 | Independence check (optional, lean) | No | Brief only | `contamination_checks/` |
| E9 | Prasanna, with Manjari | | `for_prasanna.md` | `for_prasanna_decided.md` |

Start every agent in a fresh session.

## E1. Coordinator: setup

1. **Machine and work folder.** Use a machine with internet, Python 3.9 or newer, `h5py` and `numpy`, about 12 GB of free disk and about 4 GB of free memory. Use a work folder outside any git repo, for example `~/blindtest_eski`.
2. **Round 1.** From the top folder of the kit, run:
   `python3 not-for-analyst/setup_eski.py --staging ~/blindtest_eski/staging --analyst ~/blindtest_eski/analyst`
   - **What it does:** downloads the 5.0 GB GEO h5ad (it resumes if interrupted) and keeps only the integer raw counts. It writes `S01.dge.txt.gz` to `S07.dge.txt.gz`, copies the brief, sample sheet and environment list, and writes `resources/gene_features.tsv`.
   - **Leak scan:** it ends with one, and it stops with an error if it finds study-identifying text.
   - **Timing:** expect about 5 minutes after the download.
3. **Round 2 (adult data).** Run:
   `python3 not-for-analyst/setup_eski.py --staging ~/blindtest_eski/staging --round2 ~/blindtest_eski/round2_hold`
   - **What it does:** downloads the three adult wild-type liver samples (GEO GSE181987, WT1 to WT3; about 150 MB). It writes `A01` to `A03` plus `adult_sample_sheet.csv`.
   - **Barcodes:** the GEO matrices are unfiltered, with about 6.8 million barcodes each, so the script keeps the 10,000 barcodes with the most UMIs per sample. Cell calling is left to the analyst.
   - **Check the report:** `setup_round2_report.json` lists how many barcodes exceed 500 and 1,000 UMIs. Each sample should have a few thousand cells, about 13,600 in total in the source paper.
   - **Keep `round2_hold` away from the analyst until Part 1 is frozen.**
4. **Keep private:** the staging folder holds the source file, the sample and barcode maps and both reports. The analyst must never see it.
5. **Sandbox:**
   - Same Docker image and offline references as Run A. Record the image ID.
   - Mount only the analyst folder, with the network off.
   - Use the same model and settings as Run A unless Bhadri decides otherwise, and record what was used.
6. **Pipeline config:** copy `pipeline/configs/run-a.json` to an Eski config. Set 7 samples, the pattern `S0[1-7].dge.txt.gz`, and the sample sheet columns. Then run `python3 -m pipeline validate --count-check full`.

## E2 and E3. Analyst

1. **Part 1.** Start a fresh analyst with the prompt: "Read analysis-brief.md and follow it. Save all outputs under outputs/."
2. **Freeze.** Freeze Part 1 with the pipeline's `freeze` and `verify` commands.
3. **Round 2.** Copy `round2_hold` into the analyst folder as `round2/`. Stage `for-agent/eski/followup-questions.md` with `stage-followup`, then prompt: "Read followup-questions.md and follow it."
4. **Package.** Package the report with the Part 2 and 3 files. If the runner refuses files added after the freeze, record exactly how `round2/` was staged.

## E4. Grading

Run two graders in separate fresh sessions, with no internet. Give each:
- the general grader instructions (`not-for-analyst/grader-instructions.md`),
- the Eski answer key (`eski-scoring-key.md`, private repo); its section 3 scoring rules override the totals in the general instructions,
- a fresh copy of `eski-scorecard.csv`,
- the packaged report.

Then run a reconciler as in Run A. It writes `reconciled_scorecard.csv` and `for_prasanna.md`.

Two things are scored only by the evidence review and by Prasanna, not by the key:
- the macrophage questions (18 to 21);
- the larval-versus-adult comparison beyond the key item.

## E5 and E6. Evidence review and literature

- **E5:** run the pipeline's default evidence review on the packaged report.
- **E6:** run a literature agent as in Run C, with these changes:
  - Read full text where a verdict depends on it.
  - Cite only papers it opened, marked "full text" or "abstract only".
  - It may read the Eski paper now, since the analyst has finished.

## E7. Macrophage comparison with Run C

A fresh agent compares the Eski macrophage states with Run C's five states. Run C is in the private repo, under `runs/2026-10-08-run-c-macrophage/`, with Claude's literature check in `run-c-review/updated-findings.md` in Prasanna's project.

**Questions for the agent:**
- Which states recur?
- Which are new?
- Which Run C states are missing?
- Did the dissociation stress and ambient RNA caveats behave the same way?

**Two cautions to pass on:**
- Eski's macrophages come from whole liver with a live-cell sort only. Run C's came from a lineage sort.
- The two datasets also differ in developmental stage (larval vs adult), injury and chemistry.

Output goes in `macrophage_comparison/`, private.

## E8. Independence check (optional)

Same as the lean check for Run A:
- **Closed-book baseline:** brief only, no data, graded by two graders on the core items.
- **Recognition probe:** three sessions.
- **Transcript text search:** for Eski, Singh, Andersson, CellCousin, Nature Communications, GSE272484, "previously reported", "the paper".

Rough cost: $3 to $12 at API rates.

## Cost and logging

Record time, tokens and cost for every stage in `run_log.md`. If cost is not available, record the billing basis. Claude's rough estimate, scaled from Run A's per-stage tokens:
- **Main run:** about $25 to $40 at API rates.
- **Extra stages:** the literature step and the macrophage comparison add a few dollars each.

## Where results go

Private repo, `runs/<date>-eski/`, laid out like Run A. Open a PR there.

## Never

- **Hidden from the analyst:** `not-for-analyst/`, the staging folder, `round2_hold` before Part 1 is frozen, the internet, any paper, and Run A or Run C results.
- **Never public:** the answer key, scorecards, grader outputs or macrophage results.
- **No lab data:** never add lab data that is not public. Prasanna checks with the institution first.
