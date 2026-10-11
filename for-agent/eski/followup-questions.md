# Follow-up questions

Your Part 1 answers are saved. Do not change them. If this work changes your mind about a Part 1 answer, say so here.

The same rules apply: data in this folder only, no internet, show your work, give a confidence for each claim.

**New data in `round2/`.** Use these only where a question asks.
- `A01.dge.txt.gz` to `A03.dge.txt.gz`: uninjured adult zebrafish liver, one table per sample, genes by barcodes, raw UMI counts. These come from an independent public dataset made in a different lab.
- `adult_sample_sheet.csv` lists the samples.
- **The fish:** wild-type males, about 18 months old. The number of fish per sample is not known.
- **Processing:** whole livers were dissociated with collagenase and DNase, filtered at 70 um, and run on 10x Genomics Chromium Single Cell 3' v3. No sorting is reported. Reads were aligned to GRCz11 with Cell Ranger, version uncertain.
- **Cells have not been called.** Each table holds the 10,000 barcodes with the most UMIs, so it includes empty and ambient barcodes.
- **The gene annotation differs from the larval data.** It uses NCBI-style symbols, and some genes are missing, including the mitochondrial protein-coding genes. `A01_gene_features.tsv` and the matching files list each row name. Match genes across the two datasets by symbol and report how many match.

In these questions:
- **"BFP cells"** means any cell in a 4-OHT-treated sample that you judge truly expresses mTagBFP2, not ambient RNA. Say which cell types they fall in.
- If you find hepatocyte-like BFP cells, call them **"BFP hepatocytes"**.

Say how you called them and how confident you are.

## Part 2. Specific questions

### BFP cells

8. In each sample, how many BFP cells and BFP hepatocytes are there? Which cell types do they most resemble in each sample? Does this differ between time points or injuries? What alternative explanations for the BFP cells did you consider, and how did you test each?
9. For each injury, where do you think the BFP cells come from? Name the cell type or state. Do you see any intermediate state? If so, what defines it, and in which samples?
10. Take the cell type or state you named in Q9. Is it one population or more than one? What distinguishes them? Which of them, if any, connects to the BFP hepatocytes? If you named none, subcluster the control cell type you think is most relevant and say why you chose it.
11. Which cell types proliferate after each injury, and when, compared with the same cell type in the controls? Do switched (H2B-mGL or mCherry-NTR) hepatocytes in the injured samples proliferate more than control hepatocytes? Which genes support your answer?
12. If you found cells on a path to BFP hepatocytes, which transcription factors change in them? Which go up and which go down? Do any change before other identity changes you found?
13. Which genes best mark the earliest BFP cells? If you named a source population in Q9, which genes best mark it? Which of those genes would be good for tracing that population, and why?
14. Which intracellular signaling pathways are likely active or suppressed in the source population you named in Q9, if any, and in any cells you placed on a path to BFP hepatocytes? What in the data suggests it, and what can transcript data not tell you?
15. If you found cells on a path to BFP hepatocytes, which gene programs (for example GO terms) dominate them at each time point? Say what comparison you used for each.
16. At the last time point of each injury, how do your BFP cells compare with switched hepatocytes from the same sample and with control hepatocytes?

### Larvae compared with adults

17. Do the cell types match between the control larvae and the adult liver? Then compare the cholangiocytes in the control larvae with the cholangiocytes in the adult liver, pooled and within any subgroups you can match. Do the same for hepatocytes.
    - Which genes and signaling pathways differ?
    - What might these differences mean for how larval and adult livers regenerate?
    - Say how you handled the differences in lab, sequencer, processing, gene annotation and any chemistry difference you find between the two datasets.

### Macrophages

18. Identify the macrophages and separate them from other myeloid cells and doublets. Find macrophage states from the data first, without preset labels. For each state give marker genes and cell counts per sample. Then score each state for M1-like, M2-like and other programs: antigen presentation, lysosome and debris clearance, interferon response, proliferation, and a resting or tissue-resident profile. List the zebrafish genes you used for each program, say they come from prior knowledge, and give how many were detected. Do not force cells into M0, M1 or M2.
19. How do macrophage states and numbers change after each injury? Report counts, fractions and changes within each state separately. Remember there is one library per sample.
20. Which cell states do macrophages interact with directly, or send signals to, during and after injury and repair? Include the population you named in Q9, if any, any intermediate state, if you found one, and early and late BFP hepatocytes. Also include any other cell type, for example stellate cells, endothelial cells, neutrophils or other immune cells. For each macrophage state, give the receiving cell states, the ligands and receptors, and the time points.
    - Report contact-dependent interactions (membrane-bound ligand and receptor pairs, adhesion molecules) separately from secreted signals.
    - Report detection of the ligand, the main signaling receptor and any accessory receptor separately.
    - Do not rely only on a detection cutoff that favors abundant genes. Say how you tested ligands that few cells express.
    - Check that the zebrafish genes for every receptor you test are actually mapped. List pathways you could not test.
    - If you treat profiles that look like a macrophage captured together with another cell as possible evidence of physical contact, explain why random co-capture in the same droplet cannot explain them.
    - Say how far RNA co-expression can support a claim that two cells actually interact.
21. Could dissociation stress genes, ambient RNA or doublets drive any macrophage state you found? How did you check?

## Part 3. Next experiments

22. Propose up to 6 experiments to test the most important mechanisms you found, including at least one about macrophages. For each give: the hypothesis, the model and stage, the intervention, the readout, the timing, the expected result, and the result that would prove you wrong.
23. Which of your findings would you check first by imaging or staining, and how?

## What to hand back

Write your answers by question number in a new Part 2 and 3 report, and list your new claims in a new Part 2 claim list. Do not edit the Part 1 report or claim list. Mark each new claim as Part 2 or Part 3.
