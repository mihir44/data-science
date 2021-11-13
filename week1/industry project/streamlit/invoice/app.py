import streamlit as st
import PyPDF2
import re

st.title("Total Amount Extraction App")
st.markdown(''' This app extracts the total amount mention on the invoice ''')
uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    text = PyPDF2.PdfFileReader(uploaded_file)
    pdf_text = ''
    pdf_text += text.getPage(0).extractText()

    amount = re.findall("\d+\.\d+", pdf_text)
    st.text("Total Amount: "+max(amount))