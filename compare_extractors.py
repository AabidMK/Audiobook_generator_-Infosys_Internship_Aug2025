import os
from PyPDF2 import PdfReader
import pdfplumber
from pdfminer.high_level import extract_text
import fitz  
from jiwer import wer
from difflib import SequenceMatcher
import pandas as pd
from tabulate import tabulate 


def extract_with_pypdf2(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        return f"[PyPDF2 ERROR] {e}"


def extract_with_pdfplumber(file_path):
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"[pdfplumber ERROR] {e}"


def extract_with_pdfminer(file_path):
    try:
        return extract_text(file_path).strip()
    except Exception as e:
        return f"[pdfminer ERROR] {e}"


def extract_with_pymupdf(file_path):
    try:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text")
        return text.strip()
    except Exception as e:
        return f"[PyMuPDF ERROR] {e}"



def levenshtein_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1,
                           dp[i][j-1] + 1,
                           dp[i-1][j-1] + cost)
    return dp[m][n]

def character_error_rate(ref, hyp):
    return levenshtein_distance(ref, hyp) / max(1, len(ref))

def word_error_rate(ref, hyp):
    return wer(ref, hyp)

def similarity_ratio(ref, hyp):
    return SequenceMatcher(None, ref, hyp).ratio()


def evaluate_extractors(pdf_file):
    extractors = {
        "PyMuPDF": extract_with_pymupdf,
        "pdfminer.six": extract_with_pdfminer,
        "pdfplumber": extract_with_pdfplumber,
        "PyPDF2": extract_with_pypdf2,
    }

    results = {}
    for name, extractor in extractors.items():
        print(f"[INFO] Running {name}...")
        results[name] = extractor(pdf_file)

    
    reference_text = results["PyMuPDF"]

    eval_results = []
    for name, text in results.items():
        cer = character_error_rate(reference_text, text)
        wer_val = word_error_rate(reference_text, text)
        sim = similarity_ratio(reference_text, text)
        eval_results.append([name, f"{wer_val:.6f}", f"{cer:.6f}", f"{sim*100:.6f}"])

    
    headers = ["Extractor", "WER", "CER", "Text Similarity (%)"]
    print("\n==== Accuracy Evaluation Results (Reference = PyMuPDF) ====\n")
    print(tabulate(eval_results, headers=headers, tablefmt="pretty"))

    
    df = pd.DataFrame(eval_results, columns=headers)
    df.to_csv("evaluation_results.csv", index=False)
    print("\n[INFO] Results saved to evaluation_results.csv")



if __name__ == "__main__":
    pdf_file = "sample-tables.pdf"  
    if not os.path.exists(pdf_file):
        print(f"[ERROR] File not found: {pdf_file}")
    else:
        evaluate_extractors(pdf_file)
