# Who else works on AI agents for single-cell analysis

Searched Oct 7, 2026. Four search agents opened the sources below. A second agent re-opened each source and checked the claims. I (Claude, main session) did not open these sources myself; I read the two agents' reports in full. "Checked" means the second agent confirmed it. "Partly" means some details could not be confirmed and are left out or flagged here. Vendor numbers are the vendor's own.

## Closest to our test: can an agent re-derive a paper's single-cell findings?

| Name | Who | What it tests | Result | Check |
|---|---|---|---|---|
| scBench-Long | LatchBio (startup) | Agents get raw or near-raw data from 5 published single-cell studies and must recover the conclusions, no methods given. 21 evaluations, includes ligand-receptor cell-cell communication. arXiv 2606.26563, Jun 25, 2026. | Best pair (Claude Opus 4.8 with Claude Code) passed 16 of 63 runs, 25.4%. Blog framing: agents often get correct intermediate results but fail to assemble the biological conclusion. | Checked |
| BixBench3 | Edison Scientific (FutureHouse spinout) | 20 whole-study tasks from raw data, 138 output artifacts graded against the paper. 16 of 20 are transcriptomics; number of single-cell tasks not stated. arXiv 2608.25286, Aug 26, 2026. | 13 models scored 0.00 to 0.48. 0.36 on datasets under 100 GB, 0.10 above. Mean run 6.8 h, $43 per task. | Checked |
| HeurekaBench (single-cell version) | Brbic lab, EPFL | Open-ended and multiple-choice questions grounded in published single-cell studies. arXiv 2601.01678, ICLR 2026. | Best open-ended correctness 2.58 of 5. The "41 insights from 13 Nature/Cell papers" figure was confirmed from the paper's HTML by one checker, but not in the abstract. | Checked |
| BAISBench | Zhang lab group (affiliation not shown) | 193 multiple-choice questions from conclusions in 41 published single-cell studies, answered from the real data. Baseline: six graduate-level bioinformaticians. arXiv 2505.08341. | Authors: AI scientists fall short of autonomous discovery. Scores not seen. Licence is non-commercial. | Checked |
| ELISA | Single author (O. Coser) | Agent tested on replicating findings in 6 published scRNA-seq datasets. Briefings in Bioinformatics, Sep 2026. | Self-reported mean score 0.88. Scoring method not confirmed. | Partly |
| CellVoyager | Zou lab, Stanford | Agent extends published analyses rather than re-deriving them. Nature Methods, Mar 2026. | Predicts which analyses authors ran, up to 23% better than GPT-4o and o3-mini. | Checked |
| Bersenev et al. | SBX BioSciences and Systems Biology Institute | Early multi-agent attempt to reproduce one scRNA-seq paper. bioRxiv Apr 2024. | Mostly unsuccessful beyond simple statistics. | Checked |

Related step-level benchmark: scBench (LatchBio, arXiv 2602.09063, Feb 2026). 394 single-step problems. 29 to 53% across 8 models. Accuracy dropped 40+ points on less-documented sequencing platforms. Differential expression tasks averaged 27%.

Related, synthetic data: GeneBench-Pro (OpenAI, Jun 30, 2026). Reports a "noticing versus acting" gap: models spot a warning sign but do not change the analysis.

## Products aimed at labs without a bioinformatician

- Novaflow (YC Summer 2025, team of 4): "AI data analyst for biology labs". Upload data, ask in plain English, get plots and notebooks. Users at UCSF, Mount Sinai, UC Berkeley, Harvard. Checked (partly: specific assay list not confirmed).
- Edison Scientific: Kosmos AI scientist ($200 per run, free academic tier, launched Nov 5, 2025) and Edison Analysis (notebook analysis agent, handles scRNA-seq, Nov 20, 2025). Vendor reports 79.4% of Kosmos statements accurate and 46% on BixBench for Edison Analysis. Checked.
- Phylo (Biomni Lab): Stanford spinout of the open-source Biomni agent. $13.5M seed, Feb 4, 2026, a16z and Menlo; Anthropic is an investor. Checked.
- Pluto Biosciences, BigOmics (Omics Playground), aimed analytics, Omics-OS (Lobster AI), BioTuring, Biostate AI (K-Dense), Seqera (bought tinybio): no-code or conversational omics analysis platforms of various sizes. Mostly checked.
- Elucidata (Polly Co-Scientist), Owkin (K Navigator): aimed at pharma; Owkin works on literature and its own data, not user uploads.
- Kepler AI: had a single-cell agent with TileDB and Tahoe (Oct 2025); now appears to have pivoted to finance software.
- None of these reported a test of re-deriving published findings.

## Big AI labs

- Anthropic: Claude for Life Sciences (Oct 20, 2025; 10x Genomics connector, single-cell-rna-qc skill). Claude Science desktop app beta (Jun 30, 2026). Partnerships with Allen Institute and HHMI (Feb 2, 2026). Checked, partly.
- OpenAI: GPT-Rosalind (Apr 2026, restricted access) and a free Codex Life Sciences plugin. Partly (main page returned 403; secondary source).
- Google: Gemini for Science (Co-Scientist, ERA), and Cell2Sentence-Scale open single-cell language models with Yale. Checked.
- NVIDIA: BioNeMo Agent Toolkit with GPU single-cell tools (Jun 30, 2026). Speed, not validation. Checked.
- Microsoft Discovery: general R&D agent platform, no single-cell features named. Checked.

## Nonprofits and institutes

- FutureHouse: built BixBench (2025); agents now commercialised through Edison.
- Biohub (Chan Zuckerberg): virtual cell models and rBio. Not data-analysis agents.
- Arc Institute: State virtual cell model, Virtual Cell Challenge 2026 (submissions due Nov 5, 2026). Perturbation prediction, not analysis.
- Ai2: Asta DataVoyager, free data-analysis agent for tables; no single-cell formats listed.

## What this means for us

1. Our test is not a new idea in general. LatchBio, Edison, EPFL and others already test whether agents re-derive published single-cell findings.
2. The best reported blind result is about 1 in 4 runs passing (scBench-Long). Our go bar (at least 3 of 6 core findings, no major false claim) is a different measure, so the two numbers do not compare directly.
3. Gaps we did not see covered in this search (not proof they don't exist): zebrafish or other non-mouse, non-human data; regeneration time courses; scoring weighted to wet-lab-validated findings; scoring the agent's proposed next experiments against what the authors did.
4. Risk for us: scBench found big accuracy drops on less-documented platforms. Zebrafish has thinner gene annotation and pathway databases than human or mouse, so expect it to be harder.
