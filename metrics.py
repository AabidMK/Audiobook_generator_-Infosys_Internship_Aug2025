import fitz  # PyMuPDF
from difflib import SequenceMatcher
import jiwer
from nltk.translate.bleu_score import sentence_bleu
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()
def evaluate_pdfs(gt_pdf, extracted_pdf):
    ground_truth = extract_text_from_pdf(gt_pdf)
    extracted_text = extract_text_from_pdf(extracted_pdf)
    accuracy = SequenceMatcher(None, ground_truth, extracted_text).ratio()
    wer = jiwer.wer(ground_truth, extracted_text)
    cer = jiwer.cer(ground_truth, extracted_text)
    reference = [ground_truth.split()]
    candidate = extracted_text.split()
    bleu_score = sentence_bleu(reference, candidate)

    return {
        "Sequence Similarity (%)": round(accuracy * 100, 2),
        "WER (%)": round(wer * 100, 2),
        "CER (%)": round(cer * 100, 2),
        "BLEU": round(bleu_score, 4)
    }

pdf_pairs = [
    ("sample1.pdf", "output_pypdf.txt"),
    ("sample1.pdf", "output_pdfplumber.txt"),
    ("sample1.pdf", "output_pdfminer.txt"),
    ("sample1.pdf", "output_pymu.txt")
]

for i, (gt, ext) in enumerate(pdf_pairs, start=1):
    print(f"\n📄 PDF Pair {i}: {gt} vs {ext}")
    results = evaluate_pdfs(gt, ext)
    for metric, value in results.items():
        print(f"{metric}: {value}")