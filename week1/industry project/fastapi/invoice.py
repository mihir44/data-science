from fastapi import FastAPI
import PyPDF2
import re
# from pathlib import Path

app = FastAPI()

@app.get('/total-amount-extraction/{file}')
def total_amount_extraction(file:str):
    text = PyPDF2.PdfFileReader(file+".pdf")
    pdf_text = ''
    pdf_text += text.getPage(0).extractText()
    amount = re.findall("\d+\.\d+", pdf_text)
    return {"Amount": max(amount)}
