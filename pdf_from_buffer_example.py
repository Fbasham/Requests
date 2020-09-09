import pikepdf
import io
import pdfplumber

with io.BytesIO() as f:
    with pikepdf.open(r'C:\Users\BashamF\Documents\c06278453.pdf') as pdf:       
        pdf.save(f)

    with pdfplumber.load(f) as pdf:
        print(pdf.pages[0].extract_text())


