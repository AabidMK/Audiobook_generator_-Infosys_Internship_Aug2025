# pdf_extract_with_metrics.py

import fitz  # PyMuPDF
import pdfplumber
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text

import Levenshtein
from jiwer import wer, cer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import pandas as pd

# -------- Extraction Functions --------
def extract_with_pypdf2(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def extract_with_pdfplumber(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()


def extract_with_pymupdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()


def extract_with_pdfminer(file_path):
    return extract_text(file_path).strip()


# -------- Evaluation Metrics --------
def evaluate_metrics(extracted_text, reference_text):
    extracted = extracted_text.strip()
    reference = reference_text.strip()

    metrics = {}

    # Sequence similarity (Levenshtein ratio)
    metrics["Sequence Similarity"] = round(Levenshtein.ratio(extracted, reference), 4)

    # Word Error Rate (WER)
    try:
        metrics["WER"] = round(wer(reference, extracted), 4)
    except:
        metrics["WER"] = None

    # Character Error Rate (CER)
    try:
        metrics["CER"] = round(cer(reference, extracted), 4)
    except:
        metrics["CER"] = None

    # BLEU Score
    ref_tokens = [reference.split()]
    cand_tokens = extracted.split()
    smoothie = SmoothingFunction().method4
    try:
        bleu = sentence_bleu(ref_tokens, cand_tokens, smoothing_function=smoothie)
    except:
        bleu = 0
    metrics["BLEU"] = round(bleu, 4)

    return metrics


# -------- Main Runner --------
if __name__ == "__main__":
    pdf_path = "Task2_source.pdf"           # Your PDF
    ground_truth_path = "Task2_metrics.txt"  # Ground truth text

    # Load reference text
    with open(ground_truth_path, "r", encoding="utf-8") as f:
        reference_text = f.read()

    # Define methods
    methods = {
        "PyPDF2": extract_with_pypdf2,
        "pdfplumber": extract_with_pdfplumber,
        "PyMuPDF": extract_with_pymupdf,
        "pdfminer.six": extract_with_pdfminer
    }

    results = []
    for name,func in methods.items():
        try :
            extracted = func(pdf_path)
            metrics = evaluate_metrics(extracted,reference_text)
            metrics["Library"]=name
            results.append(metrics)
        except Exception as e:
            results.append({"Library":name,"Error":str(e)})
    df = pd.DataFrame(results)
    cols = ["Library","Sequence Similarity","WER","CER","BLEU"] 
    df = df[cols]
    print("\n=== Metrics Comparison Table ===\n")
    print(df.to_string(index=False))
    df.to_csv("metrics_results.csv",index=False)
    print("\n Metrics saved to metrics_results,csv")
