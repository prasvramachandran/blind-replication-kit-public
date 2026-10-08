#!/usr/bin/env bash
# Builds the blinded data folder for the agent. For Bhadri only; do not give this script to the agent.
# Usage: bash setup_data.sh <output_dir>
# Downloads about 59 MB (processed counts only, no raw reads).
# Copies only the Part 1 brief. Give followup-questions.md to the agent later, after Part 1 is saved.
set -euo pipefail

OUT="${1:?give an output directory}"
HERE="$(cd "$(dirname "$0")" && pwd)"
MAP="$HERE/rename_map.csv"
AGENT_DIR="$HERE/../for-agent"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
LEAK='GSM|GSE|LIB[0-9]|IO[0-9]{4}|20(18|19|20)[0-9]{4}'

mkdir -p "$OUT"
curl -fL -o "$TMP/raw.tar" "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE217nnn/GSE217839/suppl/GSE217839_RAW.tar"
tar -xf "$TMP/raw.tar" -C "$TMP"

tail -n +2 "$MAP" | while IFS=, read -r sample gsm library geo_file rest; do
  test -f "$TMP/$geo_file" || { echo "missing $geo_file" >&2; exit 1; }
  # Re-compress without the original file name or timestamp in the gzip header.
  gzip -dc "$TMP/$geo_file" | gzip -n > "$OUT/$sample.dge.txt.gz"
done

cp "$AGENT_DIR/analysis-brief.md" "$AGENT_DIR/sample_sheet.csv" "$AGENT_DIR/environment.md" "$OUT/"
mkdir -p "$OUT/resources"

# Leak checks: file names, gzip headers, and the first lines of each file.
if ls "$OUT" | grep -Eq "$LEAK"; then echo "leak in file names" >&2; exit 1; fi
if gzip -lN "$OUT"/S*.dge.txt.gz | awk 'NR>1 && $NF!="(totals)" {n=$NF; sub(/.*\//,"",n); print n}' | grep -Eq "$LEAK"; then echo "leak in gzip headers" >&2; exit 1; fi
for f in "$OUT"/S*.dge.txt.gz; do
  hdr="$(set +o pipefail; gzip -dc "$f" | head -n 5)"
  if printf '%s\n' "$hdr" | grep -Eq "$LEAK"; then echo "possible leak in header lines of $f; inspect and strip" >&2; exit 1; fi
done
# Format report for the graders and Prasanna. Not for the analyst.
REPORT="$HERE/setup_report.txt"
{
  echo "sample  barcode_columns  gene_rows  hash_header_lines  transgene_like_rows"
  for f in "$OUT"/S*.dge.txt.gz; do
    s="$(basename "$f" .dge.txt.gz)"
    stats="$(set +o pipefail; gzip -dc "$f" | awk -F'\t' '
      /^#/ {h++; next}
      !seen {cols=NF-1; seen=1; next}
      {rows++; g=tolower($1); if (g ~ /^(mcherry|egfp|gfp|cfp|ntr|nfsb|cre|creert2|cfp-ntr)$/) tg=tg $1 ","}
      END {printf "%s  %s  %s  %s", cols, rows, h+0, (tg=="" ? "none" : tg)}')"
    echo "$s  $stats"
  done
} > "$REPORT"

echo "Done. $(ls "$OUT"/S*.dge.txt.gz | wc -l | tr -d ' ') count files in $OUT"
echo "Format report written to $REPORT (do not show it to the analyst)."
