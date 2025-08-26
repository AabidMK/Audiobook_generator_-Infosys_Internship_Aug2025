from pdfminer.high_level import extract_text
pdf_path = "sample1.pdf"
output_txt="output_pdfminer.txt"
text = extract_text(pdf_path)
with open(output_txt,"w",encoding = "utf-8")as f:
	f.write(text)
print(f"done!extracted text")