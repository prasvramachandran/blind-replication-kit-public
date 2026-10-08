"""Build the blinded analyst folder for the Eski dataset (GEO GSE272484), and stage the round 2 adult data.

Never give the analyst the staging folder, this script, or anything in not-for-analyst/.

What it does
1. Downloads the processed GEO file (one 5.0 GB h5ad) into the staging folder, resuming if interrupted, and
   checks its size.
2. Reads only the integer raw counts (layers/counts), gene names and IDs, and the sample of each cell.
   Everything the authors derived is left behind: cell type labels, clusters, embeddings, neighbor graphs,
   doublet scores, normalized and scaled matrices, and all uns metadata. The GEO metadata CSV is not downloaded.
3. Renames samples to S01 to S07 and cell barcodes to neutral IDs (S01_c00001, ...), and writes one
   genes-by-cells table of raw counts per sample (S01.dge.txt.gz ...), the format the pipeline expects.
4. Copies the brief, sample sheet and environment list into the analyst folder, and writes a gene table to
   resources/.
5. Scans the analyst folder for study-identifying strings.
6. With --round2, downloads the three adult WT liver samples (GEO GSE181987, GSM5515731 to GSM5515733),
   which are unfiltered (about 6.8 million barcodes each), keeps the 10,000 barcodes with the most UMIs,
   renames them A01 to A03, and writes them to a separate folder. Copy that folder into the analyst folder
   as round2/ only after Part 1 is frozen.

Usage (from the top folder of the kit, on a machine with internet; needs Python 3.9+, h5py and numpy):
  python3 not-for-analyst/setup_eski.py --staging ~/blindtest_eski/staging --analyst ~/blindtest_eski/analyst
  python3 not-for-analyst/setup_eski.py --staging ~/blindtest_eski/staging --round2 ~/blindtest_eski/round2_hold

Test without downloading: --h5ad PATH uses a local file instead of the GEO download.
"""
import argparse, csv, gzip, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time

import numpy as np

H5AD_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE272nnn/GSE272484/suppl/GSE272484_CellCousin_final.h5ad"
H5AD_BYTES = 5033661376
SAMPLE_MAP = {  # GEO sample label -> neutral ID; order matches the brief's sample table
    "Control1": "S01", "Control2": "S02",
    "Mtz 0dppa": "S03", "Mtz 1dppa": "S04", "Mtz 9dppa": "S05",
    "PHx 4dpi": "S06", "PHx 11dpi": "S07",
}
ADULT = [  # GEO sample -> neutral ID
    ("GSM5515731", "WT1", "A01"), ("GSM5515732", "WT2", "A02"), ("GSM5515733", "WT3", "A03"),
]
ADULT_URL = "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM5515nnn/{gsm}/suppl/{gsm}_{tag}_{kind}"
TRANSGENES = ["mTagBFP2", "H2B-mGL", "mCherry-NTR"]
TOP_BARCODES = 10000  # adult round 2 data: barcodes kept per sample (the GEO matrices are unfiltered)
# Strings that must not appear in anything the analyst can read except the brief itself
FORBIDDEN = ["CellCousin", "GSE272484", "GSE181987", "GSM8403", "GSM5515", "Eski", "Singh", "Andersson",
             "Control1", "Control2", "Mtz 0dppa", "Mtz 1dppa", "Mtz 9dppa", "PHx 4dpi", "PHx 11dpi",
             "MPIMT", "Morrison", "Goessling", "Oderberg", "anno1", "leiden_res"]

KIT = pathlib.Path(__file__).resolve().parent.parent
FOR_AGENT = KIT / "for-agent"


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest, expected_bytes=None):
    dest = pathlib.Path(dest)
    if dest.exists() and expected_bytes and dest.stat().st_size == expected_bytes:
        log(f"already downloaded: {dest.name}")
        return
    log(f"downloading {url}")
    subprocess.run(["curl", "-fL", "--retry", "5", "-C", "-", "-o", str(dest), url], check=True)
    if expected_bytes and dest.stat().st_size != expected_bytes:
        sys.exit(f"size mismatch for {dest}: {dest.stat().st_size} != {expected_bytes}")


def decode(arr):
    return [x.decode() if isinstance(x, bytes) else str(x) for x in arr]


def unique_row_ids(symbols, ensembl):
    """Gene row IDs for the count tables: the symbol when it is unique, otherwise the Ensembl ID."""
    counts = {}
    for s in symbols:
        counts[s] = counts.get(s, 0) + 1
    ids = [s if counts[s] == 1 else e for s, e in zip(symbols, ensembl)]
    if len(set(ids)) != len(ids):
        sys.exit("gene row IDs are not unique even after falling back to Ensembl IDs")
    return ids


def write_dge(path, row_ids, barcodes, gene_idx, cell_idx, values):
    """Write a genes-by-cells table of integer counts: header GENE + barcodes, one row per gene."""
    n_cells = len(barcodes)
    order = np.lexsort((cell_idx, gene_idx))
    gene_idx, cell_idx, values = gene_idx[order], cell_idx[order], values[order]
    bounds = np.searchsorted(gene_idx, np.arange(len(row_ids) + 1))
    with gzip.open(path, "wt", compresslevel=6, newline="\n") as out:
        out.write("GENE\t" + "\t".join(barcodes) + "\n")
        row = np.zeros(n_cells, dtype=np.int64)
        for g, rid in enumerate(row_ids):
            a, b = bounds[g], bounds[g + 1]
            row[:] = 0
            if b > a:
                row[cell_idx[a:b]] = values[a:b]
            out.write(rid + "\t" + "\t".join(map(str, row.tolist())) + "\n")


def as_int_counts(values, label):
    v = np.asarray(values)
    if v.size and (v.min() < 0 or not np.all(np.equal(np.mod(v, 1), 0))):
        sys.exit(f"{label}: counts are not nonnegative integers")
    return v.astype(np.int64)


def build_round1(args):
    import h5py
    staging = pathlib.Path(args.staging).expanduser()
    analyst = pathlib.Path(args.analyst).expanduser()
    staging.mkdir(parents=True, exist_ok=True)
    if analyst.exists() and any(analyst.iterdir()):
        sys.exit(f"analyst folder {analyst} is not empty; use a fresh folder")
    analyst.mkdir(parents=True, exist_ok=True)
    (analyst / "resources").mkdir(exist_ok=True)
    private = staging / "private"
    private.mkdir(exist_ok=True)

    if args.h5ad:
        h5ad = pathlib.Path(args.h5ad).expanduser()
    else:
        h5ad = staging / "source.h5ad"
        download(H5AD_URL, h5ad, H5AD_BYTES)
    report = {"source": H5AD_URL if not args.h5ad else str(h5ad), "source_bytes": h5ad.stat().st_size}
    if not args.skip_hash:
        log("hashing source")
        report["source_sha256"] = sha256(h5ad)

    with h5py.File(h5ad, "r") as h:
        cats = decode(h["obs/Sample/categories"][:])
        codes = h["obs/Sample/codes"][:]
        if set(cats) != set(SAMPLE_MAP):
            sys.exit(f"unexpected sample labels: {cats}")
        symbols = decode(h["var/_index"][:])
        ensembl = decode(h["var/gene_ids"][:])
        for t in TRANSGENES:
            if t not in symbols:
                sys.exit(f"transgene feature {t} missing")
        g = h["layers/counts"]
        if g.attrs.get("encoding-type") != "csr_matrix":
            sys.exit("layers/counts is not a CSR matrix")
        n_cells, n_genes = (int(x) for x in g.attrs["shape"])
        indptr = g["indptr"][:].astype(np.int64)
        log(f"reading counts: {n_cells} cells x {n_genes} genes, {indptr[-1]} nonzero entries")
        data = as_int_counts(g["data"][:], "layers/counts")
        indices = g["indices"][:].astype(np.int64)

    row_ids = unique_row_ids(symbols, ensembl)
    with open(analyst / "resources" / "gene_features.tsv", "w") as f:
        f.write("row_id\tensembl_gene_id\tsymbol\n")
        for r, e, s in zip(row_ids, ensembl, symbols):
            f.write(f"{r}\t{e}\t{s}\n")

    cell_sample = np.array([cats[c] for c in codes])
    barcode_map = []
    per_sample = {}
    for label, sid in sorted(SAMPLE_MAP.items(), key=lambda kv: kv[1]):
        cells = np.flatnonzero(cell_sample == label)
        barcodes = [f"{sid}_c{i + 1:05d}" for i in range(len(cells))]
        starts, ends = indptr[cells], indptr[cells + 1]
        lens = ends - starts
        take = np.concatenate([np.arange(s, e) for s, e in zip(starts, ends)]) if len(cells) else np.array([], int)
        cell_local = np.repeat(np.arange(len(cells)), lens)
        out = analyst / f"{sid}.dge.txt.gz"
        log(f"writing {out.name}: {len(cells)} cells")
        write_dge(out, row_ids, barcodes, indices[take], cell_local, data[take])
        per_sample[sid] = {"cells": int(len(cells)), "umi_total": int(data[take].sum())}
        barcode_map += [(sid, b, int(c)) for b, c in zip(barcodes, cells)]

    with open(private / "barcode_map.tsv", "w") as f:
        f.write("sample\tneutral_barcode\tsource_row\n")
        for row in barcode_map:
            f.write("\t".join(map(str, row)) + "\n")
    with open(private / "sample_map.json", "w") as f:
        json.dump(SAMPLE_MAP, f, indent=1)

    # brief, sample sheet with file column, environment list
    shutil.copy(FOR_AGENT / "eski" / "analysis-brief.md", analyst / "analysis-brief.md")
    shutil.copy(FOR_AGENT / "environment.md", analyst / "environment.md")
    with open(FOR_AGENT / "eski" / "sample_sheet.csv") as f:
        rows = list(csv.DictReader(f))
    with open(analyst / "sample_sheet.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sample", "file"] + [k for k in rows[0] if k != "sample"])
        w.writeheader()
        for r in rows:
            w.writerow({"sample": r["sample"], "file": f"{r['sample']}.dge.txt.gz", **{k: v for k, v in r.items() if k != "sample"}})

    report.update({"per_sample": per_sample, "genes": n_genes, "transgenes_present": TRANSGENES})
    report["leak_scan"] = leak_scan(analyst, skip=["analysis-brief.md"])
    with open(staging / "setup_report.json", "w") as f:
        json.dump(report, f, indent=1)
    log(f"done. Report: {staging / 'setup_report.json'}")
    if report["leak_scan"]:
        sys.exit("LEAK SCAN FOUND STUDY-IDENTIFYING STRINGS; see the report and fix before any analyst sees this folder")


def leak_scan(folder, skip=()):
    hits = []
    for p in pathlib.Path(folder).rglob("*"):
        if not p.is_file() or p.name in skip:
            continue
        opener = gzip.open if p.suffix == ".gz" else open
        try:
            with opener(p, "rt", errors="replace") as f:
                head = f.read(2_000_000) if p.suffix != ".gz" else f.readline()
        except Exception as e:
            hits.append(f"{p.name}: unreadable ({e})")
            continue
        for s in FORBIDDEN:
            if s.lower() in head.lower():
                hits.append(f"{p.name}: contains '{s}'")
    return hits


def read_mtx(path):
    """Read an integer coordinate MatrixMarket file (genes x barcodes). Returns 0-based gene and barcode indices."""
    with gzip.open(path, "rt") as f:
        header = f.readline()
        if "coordinate" not in header or "integer" not in header:
            sys.exit(f"{path}: expected an integer coordinate MatrixMarket file, got {header.strip()}")
        line = f.readline()
        while line.startswith("%"):  # comment and metadata lines, including any software version line
            line = f.readline()
        n_rows, n_cols, nnz = (int(x) for x in line.split())
        arr = np.fromstring(f.read(), dtype=np.int64, sep=" ")
    if arr.size != 3 * nnz:
        sys.exit(f"{path}: expected {nnz} entries, read {arr.size / 3:.0f}")
    arr = arr.reshape(-1, 3)
    return n_rows, n_cols, arr[:, 0] - 1, arr[:, 1] - 1, arr[:, 2]


def unique_symbols(symbols):
    """Row IDs from symbols alone (no source gene IDs): repeats get a numbered suffix."""
    seen, ids = {}, []
    for s in symbols:
        seen[s] = seen.get(s, 0) + 1
        ids.append(s if seen[s] == 1 else f"{s}__{seen[s]}")
    if len(set(ids)) != len(ids):
        sys.exit("adult gene row IDs are not unique")
    return ids


def build_round2(args):
    staging = pathlib.Path(args.staging).expanduser()
    out = pathlib.Path(args.round2).expanduser()
    if out.exists() and any(out.iterdir()):
        sys.exit(f"round 2 folder {out} is not empty; use a fresh folder")
    out.mkdir(parents=True, exist_ok=True)
    src = staging / "adult_source"
    src.mkdir(parents=True, exist_ok=True)
    report = {}
    rows = []
    for gsm, tag, aid in ADULT:
        files = {}
        for kind in ["barcodes.tsv.gz", "features.tsv.gz", "matrix.mtx.gz"]:
            dest = src / f"{gsm}_{kind}"
            if not dest.exists():
                download(ADULT_URL.format(gsm=gsm, tag=tag, kind=kind), dest)
            files[kind] = dest
        with gzip.open(files["features.tsv.gz"], "rt") as f:
            feats = [line.rstrip("\n").split("\t") for line in f]
        sym = [x[1] if len(x) > 1 else x[0] for x in feats]
        n_rows, n_cols, gi, ci, v = read_mtx(files["matrix.mtx.gz"])
        if n_rows != len(feats):
            sys.exit(f"{gsm}: matrix has {n_rows} rows but {len(feats)} features")
        v = as_int_counts(v, gsm)
        # The GEO matrices are unfiltered (millions of barcodes). Keep the TOP_BARCODES barcodes with the most
        # UMIs, in descending UMI order, and leave cell calling to the analyst.
        umi = np.bincount(ci, weights=v, minlength=n_cols)
        keep = [b for b in np.argsort(-umi, kind="stable")[:TOP_BARCODES] if umi[b] > 0]
        newpos = np.full(n_cols, -1, dtype=np.int64)
        newpos[np.array(keep, dtype=np.int64)] = np.arange(len(keep))
        sel = newpos[ci] >= 0
        row_ids = unique_symbols(sym)
        barcodes = [f"{aid}_b{i + 1:05d}" for i in range(len(keep))]
        log(f"writing {aid}.dge.txt.gz: top {len(keep)} of {n_cols} barcodes")
        write_dge(out / f"{aid}.dge.txt.gz", row_ids, barcodes, gi[sel], newpos[ci[sel]], v[sel])
        with open(out / f"{aid}_gene_features.tsv", "w") as f:
            f.write("row_id\tsymbol\n")
            for r, sy in zip(row_ids, sym):
                f.write(f"{r}\t{sy}\n")
        kept_umi = umi[np.array(keep, dtype=np.int64)]
        report[aid] = {"source_barcodes": int(n_cols), "kept_barcodes": len(keep), "genes": int(n_rows),
                       "umi_at_last_kept_barcode": int(kept_umi[-1]) if len(keep) else 0,
                       "barcodes_over_500_umi": int((umi > 500).sum()), "barcodes_over_1000_umi": int((umi > 1000).sum())}
        rows.append({"sample": aid, "file": f"{aid}.dge.txt.gz", "group": "adult_uninjured_wildtype", "replicate": aid[-1]})
    with open(out / "adult_sample_sheet.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sample", "file", "group", "replicate"])
        w.writeheader()
        w.writerows(rows)
    report["leak_scan"] = leak_scan(out)
    with open(staging / "setup_round2_report.json", "w") as f:
        json.dump(report, f, indent=1)
    log(f"done. Report: {staging / 'setup_round2_report.json'}")
    if report["leak_scan"]:
        sys.exit("LEAK SCAN FOUND STUDY-IDENTIFYING STRINGS in the round 2 folder")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--staging", required=True, help="private folder for downloads, maps and reports")
    ap.add_argument("--analyst", help="fresh folder to become the analyst's sandbox (round 1)")
    ap.add_argument("--round2", help="fresh folder for the adult data, held back until Part 1 is frozen")
    ap.add_argument("--h5ad", help="use this local h5ad instead of downloading (for testing)")
    ap.add_argument("--skip-hash", action="store_true", help="skip hashing the 5 GB source file")
    args = ap.parse_args()
    if not args.analyst and not args.round2:
        ap.error("give --analyst, --round2 or both")
    if args.analyst:
        build_round1(args)
    if args.round2:
        build_round2(args)


if __name__ == "__main__":
    main()
