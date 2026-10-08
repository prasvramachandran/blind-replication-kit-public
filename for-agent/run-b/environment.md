# Analysis environment (raw reads)

The sandbox has no internet. Everything below was installed or saved before the network was turned off. If something you need is missing, say so in your report rather than working around it silently.

## Machine

At least 16 CPU cores, 64 GB RAM and 600 GB free disk were requested. Check what you actually have before you start.

## Read processing

STAR 2.7.11b, samtools, pigz, Java with Drop-seq tools 3.0.2 and Picard.

## Analysis

Python 3.11: scanpy, anndata, numpy, pandas, scipy, scikit-learn, statsmodels, matplotlib, seaborn, leidenalg, python-igraph, harmonypy, scrublet, pydeseq2, gseapy, decoupler, liana, jupyter.

R (optional): Seurat, edgeR, limma, clusterProfiler, org.Dr.eg.db, msigdbr (with its data package).

## Reference files in `resources/reference/`

- `Danio_rerio.GRCz11.dna.primary_assembly.fa.gz` and `Danio_rerio.GRCz11.116.gtf.gz`: Ensembl release 116. Chromosome names without a "chr" prefix.
- `danRer11.primary.fa` and `V4.3.2.validated.gtf`: the Lawson lab zebrafish annotation, V4.3.2, with its matching genome FASTA. UCSC "chr" names and their own gene IDs. Do not mix these files with the Ensembl ones.
- `transgenes.fa` and `transgenes.gtf`: one contig per transgene product, each a single exon. Append both to the genome and annotation of your choice if you want transgene counts.
  - `tg_EGFP`: EGFP coding sequence (GenBank U55762.1) plus an SV40 early polyA.
  - `tg_mCherry`: mCherry coding sequence (Tol2kit pME-mCherry) plus an SV40 late polyA.
  - `tg_CFP_NTR`: a CFP stand-in (Cerulean, Addgene 15214) fused to E. coli nitroreductase nfsB, plus an SV40 late polyA. The CFP variant and the 3' end are assumptions.
  - `tg_CreERT2`: Cre (GenBank X03453.1) fused to ERT2 (Addgene 184059), plus an SV40 late polyA.

## Other reference files in `resources/`

Zebrafish GO annotations, a zebrafish to human ortholog table, MSigDB Hallmark and GO gene sets, PROGENy and CollecTRI for decoupler, and a ligand-receptor resource. Check the folder for exact file names and versions.
