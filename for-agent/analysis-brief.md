# Analysis brief: adult zebrafish liver, single-cell time course after hepatocyte ablation

You are the lab's bioinformatician. A PI has handed you single-cell RNA-seq data from their own experiment and wants to know what is going on. Work like a careful analyst who will have to defend every claim.

## Rules

1. Use only the files in this folder. Do not use the internet. Do not try to identify the dataset or look up any related publication.
2. Show your work. Save your code, package versions and every figure or table you rely on.
3. Separate what you observed from what you infer. Give each claim a confidence: high, medium or low.
4. Say "I don't know" or "the data cannot answer this" when that is true. A wrong confident claim costs more than an honest gap.
5. Flag anything that could mislead the analysis, for example technical or biological confounders you find.

## The experiment

**Species and fish.** Zebrafish (Danio rerio), adults 6 to 18 months old, raised at 28.5 C. Fasted 24 h before experiments. The uninjured wild-type fish were adult males. For the transgenic fish, both sexes were used and the sex of each sample is not known. The number of fish per sample is not known. It is not known whether each replicate series was a separate ablation experiment.

**Arm A. Uninjured wild-type atlas (6 samples).** Wild-type (TU strain) livers. Whole liver dissociated; all live nucleated cells sorted (Hoechst positive, propidium iodide negative).

**Arm B. Lineage-traced transgenic fish (22 samples).** Each fish carries three transgenes:
- *Tp1:CreERT2*: tamoxifen-inducible Cre driven by a Notch-responsive element. In the liver, Cre is expressed in biliary epithelial cells.
- *ubi:Switch* (ubb:loxP-EGFP-loxP-mCherry): every cell is GFP+ until Cre acts. After recombination the cell and all its descendants are mCherry+ instead.
- *fabp10a:CFP-NTR*: hepatocytes express a CFP and nitroreductase fusion. Metronidazole (MTZ) kills nitroreductase-expressing cells.

Labeling: larvae were treated with 4-hydroxytamoxifen at 2 to 3 days post fertilization, then raised to adulthood. So in adults, mCherry+ cells descend from cells that were biliary epithelial cells at the time of labeling. GFP+ cells are unrecombined cells of any type.

Injury: adults were treated with 5 mM MTZ in system water with 0.5% DMSO for 16 h at room temperature in the dark, then recovered at 28.5 C. "dpa" means days post ablation, presumably counted from the end of MTZ exposure. "Mock" samples were not exposed to MTZ. The exact mock treatment and collection time were not recorded; presumably vehicle only (0.5% DMSO in system water).

Sorting for arm B: live cells (Hoechst positive, TO-PRO-3 negative) that were mCherry+ (most samples) or GFP+ (one uninjured sample).

**Dissociation.** Liver separated from other viscera, digested with Liberase TM at 37 C for 30 min with shaking, triturated, filtered at 40 um.

**Library method.** Drop-seq (Macosko 2015 protocol), Nextera XT libraries, about 1,000 cells targeted per library. Sequenced on Illumina NextSeq 500.

**Processing already done.** Reads were aligned to GRCz11 with STAR and counted with Drop-seq tools 2.4.0 (DigitalExpression, NUM_CORE_BARCODES=5000). The gene annotation release is not known; some gene symbols may look human-style. The reference may or may not include transgene sequences; check. Each file is a genes by barcodes table of UMI counts for one library. Files likely include thousands of barcodes per library, most of them empty or ambient droplets. **No cell calling and no ambient RNA correction have been done. Both are up to you.**

## Samples

| Sample | Arm | Group | Replicate | Sequencing run |
|---|---|---|---|---|
| S01 | A | uninjured, all live cells | 1 | run 1 |
| S02 | A | uninjured, all live cells | 2 | run 1 |
| S03 | A | uninjured, all live cells | 3 | run 1 |
| S04 | A | uninjured, all live cells | 4 | run 2 |
| S05 | A | uninjured, all live cells | 5 | run 2 |
| S06 | A | uninjured, all live cells | 6 | run 2 |
| S07 | B | uninjured, mCherry+ | 1 | run 3 |
| S08 | B | uninjured, mCherry+ | 2 | run 3 |
| S09 | B | uninjured, mCherry+ | 3 | run 3 |
| S10 | B | uninjured, GFP+ (single library) | 1 | run 3 |
| S11 | B | mock, mCherry+ | 1 | run 4 |
| S12 | B | 0 dpa, mCherry+ | 1 | run 4 |
| S13 | B | 1 dpa, mCherry+ | 1 | run 4 |
| S14 | B | 2 dpa, mCherry+ | 1 | run 4 |
| S15 | B | 3 dpa, mCherry+ | 1 | run 4 |
| S16 | B | 7 dpa, mCherry+ | 1 | run 4 |
| S17 | B | mock, mCherry+ | 2 | run 5 |
| S18 | B | 0 dpa, mCherry+ | 2 | run 5 |
| S19 | B | 1 dpa, mCherry+ | 2 | run 5 |
| S20 | B | 2 dpa, mCherry+ | 2 | run 5 |
| S21 | B | 3 dpa, mCherry+ | 2 | run 5 |
| S22 | B | 7 dpa, mCherry+ | 2 | run 5 |
| S23 | B | mock, mCherry+ | 3 | run 6 |
| S24 | B | 0 dpa, mCherry+ | 3 | run 6 |
| S25 | B | 1 dpa, mCherry+ | 3 | run 6 |
| S26 | B | 2 dpa, mCherry+ | 3 | run 6 |
| S27 | B | 3 dpa, mCherry+ | 3 | run 6 |
| S28 | B | 7 dpa, mCherry+ | 3 | run 6 |

Files are named `S01.dge.txt.gz` to `S28.dge.txt.gz`. The same table is in `sample_sheet.csv`. Installed software and reference files are listed in `environment.md`.

## Part 1 questions

Answer the Part 1 questions below and save your answers. You will get more questions after that. Do not change Part 1 answers later. If later work changes your mind, say so in the later answers.

1. **Data quality.** How did you call cells and handle ambient RNA? How many cells per sample did you keep? What problems do you see in the data?
2. **Uninjured liver.** What cell types are in the uninjured liver (arm A)? Give marker genes for each.
3. **The labeled lineage after injury.** Describe what happens to the mCherry+ cells over the time course. What cell states appear, when, and in what order?
4. **Programs and pathways.** Which gene programs and signaling pathways switch on or off over time, in which cells, and when?
5. **Cell-to-cell signaling.** Which cell types in these data might send signals to the mCherry+ lineage after injury, through which ligands and receptors, and when? How far can you trust this, given how the samples were collected?
6. **Anything else.** What else stands out? What would worry you about over-interpreting these data?

## What to hand back

1. A report that answers each question by number.
2. A numbered list of every claim you make, each with its evidence (figure or table name) and confidence. The scorer will mark each claim.
3. Your code, an environment record (package versions), and the figures and tables you cite.
4. One summary figure of your main findings, publication style, as PDF and PNG with a legend. Include at least: a 2D embedding of the cells colored by cell type or state, the same embedding colored by sample group, and a panel showing how the genes that best support your main conclusions vary across sample groups. Choose the remaining panels yourself.
