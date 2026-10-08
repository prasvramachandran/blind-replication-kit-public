# Visuals instructions

You make two images that show the result of a blind test: an AI analyst re-analysed a published zebrafish liver single-cell dataset without seeing the paper. Run after grading is reconciled and Prasanna has reviewed `for_prasanna.md`.

## Inputs

- The analyst's summary figure (PDF or PNG) and report.
- `reconciled_scorecard.csv` and Prasanna's decisions in `for_prasanna_decided.md`. Where Prasanna decided a disputed item, use that verdict.
- `scoring-key.md` from the private repo, sections 5 and 6.
- The paper: Oderberg IM and Goessling W, JCI Insight 2023;8(1):e163929, https://insight.jci.org/articles/view/163929. You may use the internet to get its figure images. Never share anything with the analyst agent.

## 1. Side-by-side figure

- One row per match. Left: the analyst's panel, cropped from its summary figure, not redrawn or altered. Right: the matching panel from the paper.
- Use the figure pairs listed under "Figure pairs" in section 5 of `scoring-key.md`, and only where the analyst actually made a matching panel.
- Label each row with the item ID, a short plain-language name, and the final verdict (hit, partial, miss).
- Title: "Blind re-analysis vs published figures". Caption: the analyst never saw the paper; the right-hand panels are reproduced from Oderberg and Goessling 2023 for comparison.
- Mark it for internal use. Before anyone shows it outside the lab, check the journal's reuse license for the paper's figures.

## 2. Scorecard grid

- Rows: the items in the scorecard, core items first and marked. Columns: Part 1, Part 2.
- Cells: hit, partial or miss. Use a colorblind-safe palette and also a symbol in each cell, so it reads in grayscale.
- Banner at the top: go or no-go, core hits out of 6, Part 1 core hits, weighted score.
- Footer: one line each for major false claims (count), extra claims (counts by label), Part 3 score.

## Output

PDF and PNG of each, plus the script that made them.
