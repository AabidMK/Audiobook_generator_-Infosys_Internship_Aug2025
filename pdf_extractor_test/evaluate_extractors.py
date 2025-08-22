import pdfplumber
import pandas as pd
import tabula

PDF_PATH = "sample-tables.pdf"

def extract_with_pdfplumber(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            extracted_tables = page.extract_tables()
            for t in extracted_tables:
                df = pd.DataFrame(t)
                tables.append((page_num, df))
    return tables

def extract_with_tabula(pdf_path):
    dfs = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    return [(i+1, dfs[i]) for i in range(len(dfs))]

def evaluate_extractors(pdf_path):
    print("="*40)
    print("Extracting tables using pdfplumber")
    print("="*40)
    plumber_tables = extract_with_pdfplumber(pdf_path)
    for page_num, df in plumber_tables:
        print(f"\n--- Table from page {page_num} (pdfplumber) ---")
        print(df.head(10).to_string(index=False))

    print("\n\n" + "="*40)
    print("Extracting tables using tabula")
    print("="*40)
    tabula_tables = extract_with_tabula(pdf_path)
    for idx, df in tabula_tables:
        print(f"\n--- Table {idx} (tabula) ---")
        print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    evaluate_extractors(PDF_PATH)
