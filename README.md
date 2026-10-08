# Blind test kit: can an AI agent re-derive a published single-cell study?

Prepared Oct 7, 2026 by Prasanna Ramachandran, with Claude.

**Two repos.** Run everything from the public repo, `prasvramachandran/blind-replication-kit-public`. Only two files are kept out of it: the answer key (`not-for-analyst/scoring-key.md`) and the scorecard template (`not-for-analyst/scorecard.csv`). They live in the private repo `prasvramachandran/blind-replication-kit` (it also holds a full copy of the kit) and are needed only for grading (step 5) and visuals (step 8, `scoring-key.md` only). Copy them into those agents' folders then. Never commit them to the public repo; its `.gitignore` blocks them.

**If you use GitHub Actions.** Logs and artifacts of a public repo are public. Grader outputs quote the answer key, so keep them out of public logs, artifacts and commits. To read the private files in a job, give it a read-only token as a repository secret and check out the private repo only in the grading job. Run B needs far more disk than a standard GitHub-hosted runner has, so use a larger or self-hosted runner for it.

**The idea.** An analyst agent gets public single-cell data from a zebrafish liver study, plus the experiment design, but not the paper. It analyses the data and answers questions. Grader agents then compare its answers with what the paper found. Prasanna checks only what needs a biologist.

**You do not need the biology.** Terms like UMI, Drop-seq and cell barcode are for the agents. GEO is the public NCBI archive that holds the data.

**Pass bar.** The analyst gets at least 3 of 6 core findings and makes no major false claim. The 6 core findings and the list of major false claims are in the answer key. They are not the same as the 6 questions in the brief. The graders judge both.

## If an agent runs this kit

You can point a runner agent at this repo and let it carry out the steps below. The runner may read everything here. Three rules keep the test valid:

1. **The runner never does the analysis itself.** It starts a fresh analyst agent for steps 3 and 4, with no access to this repo, its history, or the runner's context.
2. **The analyst's sandbox holds only the folder built in step 1,** plus `followup-questions.md` once Part 1 is frozen. No internet.
3. **Do not fine-tune or train any model on this repo.** That would bake the answers into the model.

The graders, reconciler and visuals agents may read the repo. Start each one fresh, so their judgments stay independent.

## What is where

| Path | What it is | Who reads it |
|---|---|---|
| `blind-test-brief.html` | One-page overview | You. Never the analyst. |
| `for-agent/` | Brief, sample sheet, follow-up questions, environment list; `run-b/` holds the raw-reads versions and transgene sequences | Copied into the analyst's folder for it (steps 1 and 4). The analyst never sees this folder itself. |
| `not-for-analyst/` | Setup scripts, sample map, grader, reconciler and visuals instructions; the answer key and scorecard template come from the private repo | You, graders, reconciler, visuals agent, Prasanna. **Never the analyst.** |
| `background/` | A plain-language primer on the project (`project-primer.html`, also as PDF), who else builds tools like this (`landscape.md`) and the closest startup, Novaflow (`novaflow.md`) | Optional reading for you. Never the analyst. |

## Choices you make

- **Tools and models.** Any agent that can read files and run code works, for example Claude Code. Use your strongest model for the analyst. Graders can use the same model, each in its own fresh session.
- **Work folder.** Pick one outside this git repo, for example `~/blindtest`, so data never gets committed. Suggested layout: `analyst/` (the sandbox), `part1_frozen/`, `report_A/`, `grader1/`, `grader2/`, `reconcile/`, `visuals/`, `transcripts/`.
- **Run log.** Record the tool, model and version, start and end time, and cost of every run in `run_log.md`. Time, cost and memory needs are not known yet; this first run will tell us.

## Steps

1. **Setup.** On a Mac or Linux machine with internet, from the top folder of the repo, run:
   `bash not-for-analyst/setup_data.sh ~/blindtest/analyst`
   Needs bash, curl, tar, gzip and awk. It downloads 59 MB from GEO, renames everything so the study cannot be identified, copies in `analysis-brief.md`, `sample_sheet.csv` and `environment.md`, checks for leftover identifiers, and writes `not-for-analyst/setup_report.txt`. That report is a format check for you and Prasanna; no agent needs it, and the analyst must never see it.
2. **Build the sandbox.** For example a Docker container. Install everything in `for-agent/environment.md`, and save the listed reference files into `~/blindtest/analyst/resources/`, while you still have internet. Then run it with the network off (`docker run --network none`) and mount only `~/blindtest/analyst`. The analyst cannot install anything once offline. Inside the sandbox, check that `curl https://example.com` fails and that only the analyst folder is visible.
3. **Analyst, Part 1.** Start the analyst agent in the sandbox. Prompt: "Read analysis-brief.md and follow it. Save all outputs under outputs/." When it finishes, freeze Part 1: copy `outputs/` to `~/blindtest/part1_frozen/`, outside the sandbox, and run `shasum -a 256 part1_frozen/* > part1_frozen/SHA256SUMS.txt`. This proves Part 1 was not changed later.
4. **Analyst, Parts 2 and 3.** Copy `for-agent/followup-questions.md` into `~/blindtest/analyst`. Continue the same agent session if you can. Prompt: "Read followup-questions.md and follow it." If you start a new session, add: "Your earlier work is in outputs/." Save the full transcript in `transcripts/`.
5. **Grading.** Make `~/blindtest/report_A/` holding copies of `part1_frozen/` and the final `outputs/` (not the count files). Run two grader agents in separate fresh sessions, no internet. Give each: `not-for-analyst/grader-instructions.md`, `scoring-key.md` and a fresh copy of `scorecard.csv` from the private repo, and `report_A/`. Each writes to its own folder (`grader1/`, `grader2/`).
6. **Reconcile.** Run one more fresh agent with both graders' outputs and the "Reconciler" section of `grader-instructions.md`. It writes `reconciled_scorecard.csv` and `for_prasanna.md`.
7. **Prasanna** writes a decision under each item in `for_prasanna.md` and saves it as `for_prasanna_decided.md`.
8. **Visuals.** Run an agent with `not-for-analyst/visuals-instructions.md`, `scoring-key.md` from the private repo (it needs sections 5 and 6), the analyst's summary figure and report, `reconciled_scorecard.csv` and `for_prasanna_decided.md`. This agent needs internet to fetch the paper's figures. That is safe because the analyst has finished.
9. **Optional comparison.** Reuse the same `analyst/` folder. Run steps 3 to 8 for one or two existing tools (for example Biomni, open source, or Edison Analysis, free academic tier), with a new neutral name each time (`report_B`, `report_C`) so graders cannot tell which system wrote it. If a tool needs internet, note that its run was not blind. Read each tool's terms before publishing any comparison: Novaflow's terms, for example, forbid publishing benchmark results without its written consent.

## Run B: the same test from raw reads (after Run A)

Run B repeats the test, but the analyst starts from the raw sequencing reads and must build the count tables itself. Run it after Run A, with a fresh analyst that has not seen anything from Run A.

- **Machines.** Simplest is one Linux machine with internet, at least 16 cores, 64 GB RAM and about 700 GB free disk. Setup uses about 100 GB: one raw sample at a time, about 90 GB of blinded reads and about 2 GB of references. The analyst needs the rest for its own files. Run setup with internet on, then start the sandbox with the network off. If you use two machines, copy only `~/blindtest_b/analyst` to the sandbox machine, for example with rsync. Never copy the staging folder. These are estimates; record what you actually used.
- **B1. Setup.** Use a new work folder, for example `~/blindtest_b`. Install pigz. From the top folder of the repo, test with one small sample, with THREADS set to your core count:
  `THREADS=16 bash not-for-analyst/setup_raw.sh ~/blindtest_b/staging ~/blindtest_b/analyst S20`
  Check the two S20 lines (R1 and R2) in `~/blindtest_b/staging/private/checks.tsv`: bad_headers and bad_plus must be 0, and reads must be the same on both lines. Then run the same command without `S20` to do all 28; finished samples are skipped. It downloads about 91 GB from ENA, one sample at a time, rewrites every read name to a plain number, fetches the reference files, and copies in the Run B brief from `for-agent/run-b/`. If the optional Lawson annotation fails to download, the script leaves it out and adjusts the analyst's environment list; note it in `run_log.md`. The staging folder holds identifiable files: never let the analyst see it, and delete it when done.
- **B2. Sandbox.** As in step 2 above, but install everything in `for-agent/run-b/environment.md` (adds STAR, samtools, Drop-seq tools) and save the same `resources/` files as for Run A. Mount only `~/blindtest_b/analyst`. Do this only after B1 has finished all 28 samples: if you rerun `setup_raw.sh` after adding these files, its final check stops with "Unexpected files". Move the added files out, rerun, then put them back.
- **B3 to B8.** Same as steps 3 to 8 above, in `~/blindtest_b`. The follow-up questions file is the same one. In step 5, copy only the analyst's reports, logs, code, figures and tables; leave out FASTQ, BAM, STAR index and count files, and make sure the processing log is included. Graders also score the Run B process items (see `grader-instructions.md`, step 6). Give the report a new neutral name.

## Eski: a second published dataset

A second blind replication test on a different public dataset: Eski et al. 2025, Nat Commun (GEO GSE272484). It covers larval zebrafish livers after partial hepatocyte ablation or partial hepatectomy. The analyst first answers open questions blind. In a targeted second round it gets an adult comparison dataset (GEO GSE181987) and new macrophage questions.

- **Steps:** `not-for-analyst/eski-run-instructions.md`.
- **Analyst files:** `for-agent/eski/`.
- **Setup:** `not-for-analyst/setup_eski.py` downloads the 5 GB processed file, keeps only the raw counts, renames everything and scans for leaks.
- **Private repo only:** the answer key, scorecard and review notes. Graders get them at grading time. Never commit them here; `.gitignore` blocks them.

## Never

- Never let the analyst see `not-for-analyst/`, `blind-test-brief.html`, `setup_report.txt`, the internet, GEO, or the paper.
- Never give the analyst `followup-questions.md` before Part 1 is frozen.
- Never let the analyst run the download. The GEO page names the paper, which would unblind the test.
- Never commit the dataset. Never put `scoring-key.md`, `scorecard.csv`, or any grader, reconciler or visuals output (filled scorecards, `for_prasanna*.md`, the side-by-side figure, the scorecard grid) in the public repo, and never make the private repo public: its history holds the answer key, and a public answer key could leak into future models.
- Never add lab data that is not public. Prasanna checks with the institution first.

Raw reads (about 91 GB) are for Run B. They go on your own machine or the cloud, never into this repo.
