import pdfplumber
with pdfplumber.open("Sample1.pdf")as pdf:
	with open("output_pdfplumber.txt","w",encoding="utf-8")as f:
		for i,page in enumerate(pdf.pages,start=1):
			text=page.extract_text()
			f.write(f"---page{i}---\n")
			if text:
				f.write(text+"\n\n")
			else:
				f.write("[no text found on this page]\n\n")	
