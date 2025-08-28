import fitz  # PyMuPDF
import pdfminer.high_level
import pdfplumber
import PyPDF2
import docx
import re
import csv
from difflib import SequenceMatcher


# ---------- Text Utilities ----------
def normalize_text(s: str) -> str:
    s = s.replace("\u00A0", " ")  # non-breaking spaces
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\r?\n\s*", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def tokenize_words(s: str):
    return re.findall(r"\w+(?:'\w+)?|[^\w\s]", s, flags=re.UNICODE)


def levenshtein_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


def word_error_rate(ref, hyp):
    r, h = tokenize_words(ref), tokenize_words(hyp)
    d = [[0] * (len(h)+1) for _ in range(len(r)+1)]
    for i in range(len(r)+1): 
        d[i][0] = i
    for j in range(len(h)+1): 
        d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            cost = 0 if r[i-1] == h[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
    return d[len(r)][len(h)] / len(r) if len(r) else 0


def char_error_rate(ref, hyp):
    r, h = list(ref), list(hyp)
    d = [[0] * (len(h)+1) for _ in range(len(r)+1)]
    for i in range(len(r)+1): 
        d[i][0] = i
    for j in range(len(h)+1): 
        d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            cost = 0 if r[i-1] == h[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
    return d[len(r)][len(h)] / len(r) if len(r) else 0


# ---------- Extractors ----------
def extract_pymupdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_pdfminer(path):
    return pdfminer.high_level.extract_text(path)


def extract_pdfplumber(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_pypdf2(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def extract_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


# ---------- Evaluation ----------
def evaluate_extraction(ref, hyp, label, filetype):
    ref, hyp = normalize_text(ref), normalize_text(hyp)
    return {
        "File": filetype,
        "Library": label,
        "WER": round(word_error_rate(ref, hyp), 4),
        "CER": round(char_error_rate(ref, hyp), 4),
        "Similarity": round(levenshtein_ratio(ref, hyp), 4),
        "Coverage": round(len(hyp) / len(ref), 4) if len(ref) else 0
    }


def load_reference(reference_path):
    """Try multiple encodings for reading reference text."""
    try:
        with open(reference_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(reference_path, "r", encoding="latin-1") as f:
            return f.read()


def evaluate_files(file_paths, reference_path, save_csv=True):
    ref_text = load_reference(reference_path)
    all_results = []

    for file_path in file_paths:
        results = []
        if file_path.endswith(".pdf"):
            results.append(evaluate_extraction(ref_text, extract_pymupdf(file_path), "PyMuPDF", file_path))
            results.append(evaluate_extraction(ref_text, extract_pdfminer(file_path), "pdfminer.six", file_path))
            results.append(evaluate_extraction(ref_text, extract_pdfplumber(file_path), "PDFplumber", file_path))
            results.append(evaluate_extraction(ref_text, extract_pypdf2(file_path), "PyPDF2", file_path))
        elif file_path.endswith(".docx"):
            results.append(evaluate_extraction(ref_text, extract_docx(file_path), "python-docx", file_path))
        else:
            print(f"Unsupported file type: {file_path}")
            continue

        print(f"\nAccuracy Evaluation Results for {file_path}:")
        for r in results:
            print(r)

        all_results.extend(results)

    if save_csv:
        with open("results.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["File", "Library", "WER", "CER", "Similarity", "Coverage"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print("\nAll results saved to results.csv")


if __name__ == "__main__":
    # List of files to evaluate
    file_paths = ["sample.pdf", "sample.docx"]   # both PDF and DOCX
    reference_path = "reference.txt"            # ground truth
    evaluate_files(file_paths, reference_path)
