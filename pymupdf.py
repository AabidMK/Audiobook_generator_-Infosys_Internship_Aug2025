import fitz
pdf_path = "sample1.pdf"
output_txt="output_pymu.txt"
doc=fitz.open(pdf_path)
all_text = " "
for page_num in range(len(doc)):
	page = doc[page_num]
	text = page.get_text()
	all_text+=f"\n---page{page_num+1}---\n{text}"
with open(output_txt,"w",encoding="utf-8")as f:
	f.write(all_text)
doc.close()
print(f"done!")