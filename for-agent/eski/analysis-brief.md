# Analysis brief: larval zebrafish liver, single-cell study of two partial liver injuries

You are the lab's bioinformatician. A PI has handed you single-cell RNA-seq data from their own experiment and wants to know what is going on. Work like a careful analyst who will have to defend every claim.

## Rules

1. Use only the files in this folder. Do not use the internet. Do not try to identify the dataset or look up any related publication.
2. Show your work. Save your code, package versions and every figure or table you rely on.
3. Separate what you observed from what you infer. Give each claim a confidence: high, medium or low.
4. Say "I don't know" or "the data cannot answer this" when that is true. A wrong confident claim costs more than an honest gap.
5. Flag anything that could mislead the analysis, for example technical or biological confounders you find.

## The experiment

**Fish.** Zebrafish (Danio rerio), outbred AB background. Until 5 days post fertilization (dpf), kept at 28.5 C, about 50 larvae per 30 ml of E3 medium. From 5 dpf, fed live rotifers daily, about 30 larvae per 500 ml of 5 ppt fish water. From 10 dpf, kept in tanks with water flow and fed dry flake food twice daily. Housing temperature after 5 dpf is not reported. Livers were collected between about 12 and 21 dpf. The number of fish pooled per sample is not known. Sex is not known.

**Transgenes.** All fish carry two transgenes, both driven by the hepatocyte promoter fabp10a:
- *fabp10a:CreER*: tamoxifen-inducible Cre in hepatocytes.
- *fabp10a:BB-NTR*: a multicolor reporter. In its default state it expresses nuclear mTagBFP2 (blue). When Cre acts, it switches at random to one of two other states: nuclear H2B-mGreenLantern (green, called H2B-mGL here) or mCherry-NTR (mCherry with nitroreductase). Some cells carry more than one copy of the reporter, so a single cell can switch to both states. Metronidazole (Mtz) kills cells that express mCherry-NTR.

Because the reporter is driven by fabp10a, it is only expressed in cells where that promoter is active. A cell that Cre has not switched expresses mTagBFP2.

**Labeling.** Injured fish were treated with 10 uM 4-hydroxytamoxifen (4-OHT) for 24 h, starting at 102 hours post fertilization. The two control samples were not treated with 4-OHT.

**Injury 1, partial ablation.** Labeled larvae were treated with 10 mM Mtz in 1% DMSO in E3, protected from light, for two 16 h periods at 10.5 and 11.5 dpf. Between the two periods they were rinsed and fed rotifers. "dppa" means days post partial ablation, counted from the end of the second Mtz period.

**Injury 2, partial hepatectomy.** At 10 dpf, under tricaine anesthesia, part of the left liver lobe was surgically removed through a small incision. "dpi" means days post injury.

**Controls.** Uninjured, not treated with 4-OHT, collected at 13 dpf. Whether controls received DMSO or any sham procedure is not known.

**Dissociation and sorting.** Whole livers were dissected and dissociated in TrypLE at 37 C for 15 minutes with shaking, filtered at 40 um, and stained with a live/dead dye (Calcein violet or Draq7). Live cells were collected by FACS with a live/dead gate. No reporter gate is reported.

**Library method.** 10x Genomics Chromium Single Cell 3' v3, about 7,000 cells targeted per sample. Sequenced on Illumina NextSeq 550.

**Processing already done.** Reads were aligned with Cell Ranger 7.1.0 to a custom GRCz11 Ensembl reference that also contains the three reporter sequences, with intronic reads excluded. The data providers then filtered the cells:
- Cells with fewer than 500 or more than 8,000 detected genes, or more than 15% mitochondrial reads, were removed.
- Doublets predicted by Scrublet, and clusters with high doublet scores, were removed.
- Genes detected in fewer than 3 cells were removed.

So you receive cells only, not all barcodes. Filtered barcodes cannot be recovered, and you cannot redo cell calling. You may still find doublets, damaged cells or ambient RNA the filter missed.

## Samples

| Sample | Group | Injury | Time after injury | Approximate age at collection | 4-OHT |
|---|---|---|---|---|---|
| S01 | Control | none | not applicable | 13 dpf | no |
| S02 | Control | none | not applicable | 13 dpf | no |
| S03 | Partial ablation | Mtz | 0 dppa | 12 dpf | yes |
| S04 | Partial ablation | Mtz | 1 dppa | 13 dpf | yes |
| S05 | Partial ablation | Mtz | 9 dppa | 21 dpf | yes |
| S06 | Partial hepatectomy | surgery | 4 dpi | 14 dpf | yes |
| S07 | Partial hepatectomy | surgery | 11 dpi | 21 dpf | yes |

Ages are approximate, worked out from the protocol. There is one library per sample. Age rises with time after injury, and the controls are a single age.

## Files

- `S01.dge.txt.gz` to `S07.dge.txt.gz`: one table per sample, genes by cells, raw UMI counts. Each file holds only the cells that passed the providers' filter. Rows are named by gene symbol, or by Ensembl gene ID where a symbol repeats. The three reporters are rows named `mTagBFP2`, `H2B-mGL` and `mCherry-NTR`.
- `resources/gene_features.tsv`: each row name with its Ensembl gene ID and symbol.
- `sample_sheet.csv`: the table above, with a `file` column.
- `environment.md` and `resources/`: installed software and offline reference files.

## Part 1 questions

Answer the Part 1 questions below and save your answers. You will get more questions after that. Do not change Part 1 answers later. If later work changes your mind, say so in the later answers.

1. **Data quality.** What problems do you see in these already-filtered cells? How many cells per sample do you keep after your own checks, and why?
2. **Uninjured liver.** What cell types are in the control livers? Give marker genes and rough proportions for each.
3. **Hepatocytes and other cells after injury.** After each injury, how does each cell type change over time, in number and in state? Do any cell states appear that are not in the controls? If so, in which samples? What do the three reporter transcripts show in each sample and cell type? What can you conclude from them, and what can you not?
4. **Programs and pathways.** Which gene programs and signaling pathways switch on or off after injury, in which cells, and when?
5. **Two injuries compared.** How do the responses to partial ablation and partial hepatectomy differ, and how are they alike?
6. **Cell-to-cell signaling.** Which cell types might send signals to the cells that change most after injury, through which ligands and receptors, and when? How far can you trust this?
7. **Anything else.** What else stands out? What would worry you about over-interpreting these data?

## What to hand back

1. A report that answers each question by number.
2. A numbered list of every claim you make, each with its evidence (figure or table name) and confidence. The scorer will mark each claim.
3. Your code, an environment record (package versions), and the figures and tables you cite.
4. One summary figure of your main findings, publication style, as PDF and PNG with a legend. Include at least: a 2D embedding of the cells colored by cell type or state, the same embedding colored by sample, and a panel showing how the genes that best support your main conclusions vary across samples. Choose the remaining panels yourself.
