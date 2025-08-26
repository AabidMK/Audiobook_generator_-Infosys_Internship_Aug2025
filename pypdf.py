import PyPDF2
pdf_path = "sample1.pdf"
output_txt = "output_pypdf.py"
with open(pdf_path,"rb") as pdf_file:
	reader = PyPDF2.PdfReader(pdf_file)
	with open(output_txt,"w",encoding = "utf-8")as out:
		for i,page in enumerate(reader.pages,start=1):
			text = page.extract_text()
			if text:
				out.write(text)
			else:
				out.write(f"\n ---page{i}:no extractable text--\n")
print(f"done! saved to extracted_text.py")