# Novaflow: what they offer, what the evidence shows, where the openings are

Researched Oct 7, 2026. Four research agents opened the sources below; a second agent re-opened each source and checked the claims. I (Claude, main session) read all reports in full but did not open the pages myself. Novaflow's numbers are its own marketing unless stated otherwise.

## What Novaflow is

- **Company.** YC Summer 2025, San Francisco, team of 4 (YC page). Pitch: "the AI data analyst for biology labs". Founders are listed on the YC page; the team includes a computational biologist. Funding: a July 2025 pre-seed of undisclosed size (aggregator); backers shown on the homepage are Y Combinator, BioRender and FCVC. Hiring 3 founding engineers and 4 interns. Gave a 15-minute company slot at BIO 2026. Sources: ycombinator.com/companies/novaflow, convention.bio.org (Novaflow session), novaflow.ai.
- **Product claims.** Upload data, describe the experiment, approve a plan, then the system runs analyses in R and Python and returns figures, notebooks, cited reports, methods text and supplementary tables. Claims to cover single-cell, ATAC/ChIP, spatial, bulk, CRISPR screens and reanalysis of GEO and CELLxGENE data. Every plan lists "three independent auditors", never explained. Source: novaflow.ai, novaflow.ai/pricing.
- **People in the loop.** The homepage says Novaflow computational biologists meet with your team throughout the project, and that the automated workflow is reviewed by their team. So it is partly a service, not just software. The homepage illustration shows a "NovaFlow team" comment in the shared workspace.
- **Pricing.** Free, Pro $20/month, Max $200/month, Enterprise custom. Same workflow on every plan; only usage differs.
- **Deployment.** Hosted service: data in US cloud storage; prompts, results, code and the first rows of datasets go to unnamed third-party AI model providers; not used for training (with a consent exception in the terms). No SOC 2 or HIPAA claim. Identifiable genetic data needs a separate agreement. A separate "standalone platform" can be deployed on-prem or on HPC. Sources: app.novaflow.ai/privacy, app.novaflow.ai/terms, novaflow.ai/services.
- **Terms of service.** Users may not publish benchmark or performance results about the service without Novaflow's written consent (terms, section 4).

## What the evidence shows

- **The homepage figures are illustrations.** The "How NovaFlow works" section draws its example UMAP, volcano plot and finding with page code (generated points and fixed text), not from a real analysis. That is common for marketing pages; it just means the figures say nothing about accuracy.
- **Accuracy on the public demo.** The demo uses a real public dataset (mouse pancreas, Bastidas-Ponce et al. 2019). Cell-type annotation accuracy is shown as 69.5% (marker rules), 79.0% (centroid step) and 77.0% after the "agentic self-correction" step. The homepage reports a 7.5-point gain measured from the first step.
- **No independent validation found.** We found no paper or preprint citing it (PubMed, Europe PMC, Google Scholar) and it does not appear in the benchmarks we checked (scBench, BixBench). We found no named customer case studies. Named institutions (UCSF, Mount Sinai, Berkeley, Harvard, Caltech) are self-reported and vary by page. Homepage metrics (12+ hours saved per week, 40% faster) have no method.
- **Species.** No page names any organism support. The only worked example is mouse. Their CLI blog post says it covers mainly human data for now.

## How crowded is this?

Crowded in general. The positioning agent's check of current pages found many products aimed at labs without a bioinformatician: Phylo's Biomni Lab (Free; Pro $100/month, $50 with .edu; claims SOC 2 and ISO 27001), Anthropic's Claude Science (desktop app, runs locally or on institutional HPC, reviewer agent), Edison Analysis and Kosmos (aimed at biopharma; the only vendor with a preprint reporting accuracy and rediscoveries), Pluto (pharma, customer-hosted), BigOmics (states over 290 species), aimed analytics (platform plus paid services), Lobster by Omics-OS (open source, can run offline), and newer entrants such as Ploid AI. See also landscape.md in this folder.

What looks open (not proof; searches are never exhaustive):
- No vendor publishes a blind replication of a specific published single-cell study.
- No vendor names zebrafish or other non-model organisms.
- No wet-lab-validated single-cell benchmark from any vendor.
- No single-cell-specific experiment planning (only general claims).
- Local and on-prem options exist, but nothing supports an academic institution's own approval step before data is uploaded.

Independent context: scBench (LatchBio, Feb 2026) found 29 to 53% accuracy on real single-cell tasks, with drops of 40+ points on less-documented platforms. A Cell Genomics perspective (Corpas et al., Jul 2026; seen via the author's page) argues the bottleneck in agentic genomics has moved from building pipelines to validation.

## Features worth having

1. A plan the user approves before anything runs.
2. Humans in the loop, said openly: an expert reviews and meets with the lab.
3. The stage framing: study design, analysis, interpretation, figures, next question. It ends where a lab actually wants to go.
4. Outputs a PI can use directly: publication-style figures, methods text, supplementary tables, notebooks.
5. A shared workspace with plain-English questions, analysis branches and recorded decisions.
6. Low price and an on-prem option.

## What we would do differently

1. Show figures from real analyses, labelled with their dataset.
2. Publish how each metric was measured.
3. Keep validation results public. (Novaflow's terms ask users not to publish benchmark results about the service without consent.)

## Openings for this project

1. **Validation as the product.** Blind tests on published datasets, scored against wet-lab-validated findings, published openly. The test kit built today is a first instance.
2. **Zebrafish and regeneration.** Organism-aware annotation, ortholog mapping for pathway databases, time-course and lineage-tracing designs.
3. **Experiment planning from the data,** scored against what authors actually did next.
4. **Academic data governance:** runs inside the institution, with an approval step before any lab data reaches an AI service.
5. **Honest uncertainty:** a confidence and evidence for every claim, and "the data cannot answer this" when true.
