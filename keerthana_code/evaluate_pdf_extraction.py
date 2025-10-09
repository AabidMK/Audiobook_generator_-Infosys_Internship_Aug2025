import argparse
import time
import re
from pathlib import Path
import pandas as pd

# --- Libraries for extraction & metrics ---
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as pdfminer_extract
import pdfplumber
import PyPDF2
from rapidfuzz import fuzz
import jiwer

# ------------------------
# Helpers: normalization
# ------------------------
def normalize_text(s: str) -> str:
    if s is None:
        return ""
    # Fix hyphenation at line ends: "exam-\nple" -> "example"
    s = re.sub(r"-\s*\n\s*", "", s)
    # Replace newlines/tabs with space
    s = re.sub(r"[\r\n\t]+", " ", s)
    # Collapse multiple spaces
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def to_lower_spaces_only(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def jaccard_char_ngrams(a: str, b: str, n: int = 5) -> float:
    def ngrams(s: str, n: int):
        s = re.sub(r"\s+", " ", s)
        return set(s[i:i+n] for i in range(max(0, len(s)-n+1)))
    A, B = ngrams(a, n), ngrams(b, n)
    if not A and not B:
        return 1.0
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)

# ------------------------
# Extractors
# ------------------------
def extract_pymupdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    out = []
    for page in doc:
        out.append(page.get_text("text"))  # plain text mode
    return "\n".join(out)

def extract_pdfminer(pdf_path: Path) -> str:
    return pdfminer_extract(str(pdf_path))

def extract_pdfplumber(pdf_path: Path) -> str:
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            out.append(txt)
    return "\n".join(out)

def extract_pypdf2(pdf_path: Path) -> str:
    out = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            txt = page.extract_text() or ""
            out.append(txt)
    return "\n".join(out)

EXTRACTORS = {
    "PyMuPDF": extract_pymupdf,
    "pdfminer.six": extract_pdfminer,
    "PDFplumber": extract_pdfplumber,
    "PyPDF2": extract_pypdf2,
}

# ------------------------
# Metrics
# ------------------------
def compute_metrics(ground_truth: str, candidate: str) -> dict:
    # Normalization for fair comparison
    gt_norm = normalize_text(ground_truth)
    cand_norm = normalize_text(candidate)

    # WER / CER with consistent transforms
    transform = jiwer.Compose([
        jiwer.Strip(),
        jiwer.ToLowerCase(),
        jiwer.RemoveMultipleSpaces(),
    ])
    wer = jiwer.wer(
        gt_norm, cand_norm,
        truth_transform=transform,
        hypothesis_transform=transform,
    )
    cer = jiwer.cer(
        gt_norm, cand_norm,
        truth_transform=transform,
        hypothesis_transform=transform,
    )

    # String similarities
    # RapidFuzz ratios return 0..100; convert to 0..1
    sim_ratio = fuzz.ratio(gt_norm, cand_norm) / 100.0
    sim_token_sort = fuzz.token_sort_ratio(gt_norm, cand_norm) / 100.0
    jaccard5 = jaccard_char_ngrams(gt_norm, cand_norm, n=5)

    return {
        "WER": wer,
        "CER": cer,
        "Similarity_Ratio": sim_ratio,
        "Similarity_TokenSort": sim_token_sort,
        "Jaccard_5gram": jaccard5,
    }

# ------------------------
# Main
# ------------------------
def main():
    parser = argparse.ArgumentParser(description="Evaluate PDF text extraction accuracy across libraries.")
    parser.add_argument("--pdf", required=True, help="Path to sample.pdf")
    parser.add_argument("--gt", required=True, help="Path to ground_truth.txt (UTF-8)")
    parser.add_argument("--out", default="results.csv", help="CSV output file")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    gt_path = Path(args.gt)
    out_path = Path(args.out)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not gt_path.exists():
        raise FileNotFoundError(f"Ground truth not found: {gt_path}")

    ground_truth = gt_path.read_text(encoding="utf-8", errors="ignore")

    rows = []
    for name, extractor in EXTRACTORS.items():
        try:
            t0 = time.perf_counter()
            text = extractor(pdf_path) or ""
            t1 = time.perf_counter()
            metrics = compute_metrics(ground_truth, text)
            rows.append({
                "Library": name,
                "Time_sec": round(t1 - t0, 4),
                "Chars_Extracted": len(text),
                **{k: round(v, 6) for k, v in metrics.items()},
            })
        except Exception as e:
            rows.append({
                "Library": name,
                "Time_sec": None,
                "Chars_Extracted": 0,
                "WER": 1.0,
                "CER": 1.0,
                "Similarity_Ratio": 0.0,
                "Similarity_TokenSort": 0.0,
                "Jaccard_5gram": 0.0,
            })
            print(f"[ERROR] {name}: {e}")

    df = pd.DataFrame(rows).sort_values(by=["WER", "CER", "Time_sec"], ascending=[True, True, True])
    df.to_csv(out_path, index=False)
    print("\n=== Extraction Accuracy Report ===")
    print(df.to_string(index=False))
    print(f"\nSaved CSV: {out_path.resolve()}")

if __name__ == "__main__":
    main()
