#!/usr/bin/env bash
# Run B setup: builds the blinded raw-read folder for the analyst. For Bhadri or the runner agent only;
# never give this script, the staging folder or rename_map.csv to the analyst.
#
# Usage:   bash setup_raw.sh <staging_dir> <analyst_dir> [S20 ...]
#          With no sample names, all 28 samples are processed.
#          Test first with one small sample, for example S20 (about 40 million read pairs).
# Needs:   internet, bash, curl, awk, gzip (pigz is used if installed and is much faster),
#          md5sum or md5. Set THREADS to the number of cores pigz may use (default 4).
# Downloads: about 91 GB of raw reads from ENA (one sample at a time; raw files are deleted
#          after blinding unless KEEP_RAW=1) plus about 2 GB of reference files.
# Output:  <analyst_dir>/S01_R1.fastq.gz ... S28_R2.fastq.gz, resources/reference/, brief,
#          sample sheet, environment list. Read names become plain numbers.
#
# Untested end to end. The read-name rewrite and the checks were tested on the first kilobytes
# of three of these runs. Run one sample first and read its check line before running all 28.
set -euo pipefail

STAGE="${1:?give a staging directory (holds identifiable files)}"
OUT="${2:?give the analyst directory}"
shift 2
WANT="${*:-}"

HERE="$(cd "$(dirname "$0")" && pwd)"
MAP="$HERE/rename_map.csv"
RUNB="$HERE/../for-agent/run-b"
FOLLOW="$HERE/../for-agent/followup-questions.md"
THREADS="${THREADS:-4}"
for s in $WANT; do cut -d, -f1 "$MAP" | grep -qx "$s" || { echo "Unknown sample $s; use names like S20." >&2; exit 1; }; done

mkdir -p "$STAGE/private/raw" "$OUT/resources/reference"
STAGE="$(cd "$STAGE" && pwd)"
OUT="$(cd "$OUT" && pwd)"
case "$OUT/" in "$STAGE/"*) echo "The analyst directory must not be inside the staging directory." >&2; exit 1;; esac
case "$STAGE/" in "$OUT/"*) echo "The staging directory must not be inside the analyst directory." >&2; exit 1;; esac
PRIV="$STAGE/private"

if command -v pigz >/dev/null 2>&1; then ZIP=(pigz -n -p "$THREADS"); UNZIP=(pigz -dc); else ZIP=(gzip -n); UNZIP=(gzip -dc); fi
md5of() { if command -v md5sum >/dev/null 2>&1; then md5sum "$1" | cut -d' ' -f1; else md5 -q "$1"; fi; }
# Download to a temporary name and rename when complete, so an interrupted run never leaves a half file.
fetch() { [ -s "$2" ] && return 0; curl -fsS --retry 10 -C - -o "$2.part" "$1" && mv "$2.part" "$2"; }
LEAK='SRR|SRX|SRS|SRP|ERR|ERX|SAMN|GSM|GSE|PRJNA|LIB[0-9]|IO[0-9]{4}'

# Read-name rewrite: keep only the spot number from headers like "@SRR22266735.1 1/1".
# Stops with an error on any header it does not recognise.
REW='NR%4==1{ if ($1 ~ /^@/ && match($1,/\.[0-9]+/)) id=substr($1,RSTART+1,RLENGTH-1); else {print "bad header at line " NR > "/dev/stderr"; exit 2}; print "@" id; next} NR%4==3{ if ($0 !~ /^\+/) {print "bad plus line at line " NR > "/dev/stderr"; exit 2}; print "+"; next} {print}'

# Per-file check: reads, bad headers, bad plus lines, reads of unexpected length, first and last header.
CHK='NR%4==1{ if ($0 !~ /^@[0-9]+$/) h++; if (NR==1) first=$0; last=$0 } NR%4==3 && $0!="+"{p++} NR%4==2 && length($0)!=L{l++} END{ if (NR==0 || NR%4) p++; if (NR==0) first=last="none"; printf "%d %d %d %d %s %s\n", NR/4, h+0, p+0, l+0, first, last}'

echo "Fetching the run list from ENA."
curl -fsS --retry 5 "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA900999&result=read_run&fields=run_accession,fastq_ftp,fastq_md5&format=tsv" > "$PRIV/ena.tsv"
head -1 "$PRIV/ena.tsv" | grep -q "^run_accession" || { echo "The ENA run list did not download; rerun later." >&2; exit 1; }

LOG="$PRIV/checks.tsv"
[ -f "$LOG" ] || printf 'sample\tread\treads\tbad_headers\tbad_plus\twrong_length\tfirst\tlast\n' > "$LOG"

tail -n +2 "$MAP" | while IFS=, read -r sample gsm library geo_file srr rest; do
  if [ -n "$WANT" ] && ! printf ' %s ' $WANT | grep -q " $sample "; then continue; fi
  if [ -f "$PRIV/done_$sample" ] && [ -s "$OUT/${sample}_R1.fastq.gz" ] && [ -s "$OUT/${sample}_R2.fastq.gz" ]; then echo "$sample already done, skipping."; continue; fi
  row="$(awk -F'\t' -v r="$srr" '$1==r' "$PRIV/ena.tsv")"
  test -n "$row" || { echo "No ENA entry for $sample." >&2; exit 1; }
  urls="$(printf '%s' "$row" | cut -f2)"; sums="$(printf '%s' "$row" | cut -f3)"
  for i in 1 2; do
    url=""; sum=""
    for k in 1 2; do
      u="$(printf '%s' "$urls" | cut -d';' -f$k)"
      case "$u" in *_$i.fastq.gz) url="$u"; sum="$(printf '%s' "$sums" | cut -d';' -f$k)";; esac
    done
    test -n "$url" || { echo "No read $i file for $sample." >&2; exit 1; }
    raw="$PRIV/raw/$(basename "$url")"
    echo "$sample read $i: downloading."
    fetch "https://$url" "$raw"
    [ "$(md5of "$raw")" = "$sum" ] || { echo "Checksum mismatch for $sample read $i; delete $raw and rerun." >&2; exit 1; }
    echo "$sample read $i: rewriting read names."
    "${UNZIP[@]}" "$raw" | awk "$REW" | "${ZIP[@]}" > "$OUT/${sample}_R$i.fastq.gz.part"
    mv "$OUT/${sample}_R$i.fastq.gz.part" "$OUT/${sample}_R$i.fastq.gz"
    [ "${KEEP_RAW:-0}" = "1" ] || rm -f "$raw"
    L=$([ "$i" = 1 ] && echo 25 || echo 49)
    stats="$("${UNZIP[@]}" "$OUT/${sample}_R$i.fastq.gz" | awk -v L="$L" "$CHK")"
    set -- $stats
    printf '%s\tR%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$sample" "$i" "$1" "$2" "$3" "$4" "$5" "$6" >> "$LOG"
    if [ "$2" != 0 ] || [ "$3" != 0 ]; then rm -f "$OUT/${sample}_R$i.fastq.gz"; echo "$sample read $i failed the format check; see $LOG." >&2; exit 1; fi
    [ "$4" = 0 ] || echo "Note: $sample read $i has $4 reads that are not $L bases long (allowed, recorded in $LOG)."
  done
  r1="$(awk -F'\t' -v s="$sample" '$1==s && $2=="R1"' "$LOG" | tail -1 | cut -f3,7,8)"
  r2="$(awk -F'\t' -v s="$sample" '$1==s && $2=="R2"' "$LOG" | tail -1 | cut -f3,7,8)"
  [ "$r1" = "$r2" ] || { rm -f "$OUT/${sample}_R1.fastq.gz" "$OUT/${sample}_R2.fastq.gz"; echo "$sample: read 1 and read 2 do not pair up (count or names differ); see $LOG." >&2; exit 1; }
  touch "$PRIV/done_$sample"
  echo "$sample done."
done

echo "Fetching reference files."
REF="$OUT/resources/reference"
E=https://ftp.ensembl.org/pub/release-116
fetch "$E/fasta/danio_rerio/dna/Danio_rerio.GRCz11.dna.primary_assembly.fa.gz" "$REF/Danio_rerio.GRCz11.dna.primary_assembly.fa.gz"
fetch "$E/gtf/danio_rerio/Danio_rerio.GRCz11.116.gtf.gz" "$REF/Danio_rerio.GRCz11.116.gtf.gz"
L4=https://umms.dolphinnext.com/pub/umw_biocore/dnext_data/genome_data_other/cellranger/zebrafish/GRCz11_v4.3.2_cellranger_v6
fetch "$L4/V4.3.2.validated.gtf" "$REF/V4.3.2.validated.gtf" || { rm -f "$REF/V4.3.2.validated.gtf.part"; echo "Lawson annotation download failed; Ensembl files are enough. Note it in the run log."; }
fetch "$L4/danRer11.primary.fa" "$REF/danRer11.primary.fa" || { rm -f "$REF/danRer11.primary.fa.part"; echo "danRer11 download failed; Ensembl files are enough. Note it in the run log."; }
cp "$RUNB/transgenes.fa" "$RUNB/transgenes.gtf" "$REF/"
cp "$RUNB/analysis-brief.md" "$RUNB/sample_sheet.csv" "$RUNB/environment.md" "$OUT/"
# If the optional Lawson files are missing, do not tell the analyst they exist.
if [ ! -s "$REF/V4.3.2.validated.gtf" ] || [ ! -s "$REF/danRer11.primary.fa" ]; then
  rm -f "$REF/V4.3.2.validated.gtf" "$REF/danRer11.primary.fa"
  grep -v 'V4.3.2.validated.gtf' "$OUT/environment.md" > "$OUT/environment.md.tmp" && mv "$OUT/environment.md.tmp" "$OUT/environment.md"
  echo "Lawson files left out; environment.md adjusted. Note it in the run log."
fi

echo "Final leak check."
(cd "$OUT" && find . -mindepth 1 ! -type d | sed 's|^\./||') | grep -vE '^(S(0[1-9]|1[0-9]|2[0-8])_R[12]\.fastq\.gz|analysis-brief\.md|sample_sheet\.csv|environment\.md|resources/reference/(Danio_rerio\.GRCz11\.dna\.primary_assembly\.fa\.gz|Danio_rerio\.GRCz11\.116\.gtf\.gz|V4\.3\.2\.validated\.gtf|danRer11\.primary\.fa|transgenes\.fa|transgenes\.gtf))$' && { echo "Unexpected files in $OUT (listed above)." >&2; exit 1; }
for f in "$OUT"/S*_R*.fastq.gz; do
  flg="$(od -An -tx1 -j3 -N1 "$f" | tr -d ' \n')"
  case "$flg" in 00|01) ;; *) echo "$f stores extra gzip header fields (flag $flg); recompress with gzip -n." >&2; exit 1;; esac
done
if grep -rEl "$LEAK" "$OUT"/*.md "$OUT"/*.csv "$REF"/transgenes.* 2>/dev/null; then echo "Identifier found in the files listed above." >&2; exit 1; fi
test ! -e "$OUT/$(basename "$FOLLOW")" || { echo "followup-questions.md must not be in the analyst folder yet." >&2; exit 1; }

echo "Done. Check lines are in $LOG (staging only)."
echo "Give the analyst only $OUT. Delete $STAGE when you no longer need it."
