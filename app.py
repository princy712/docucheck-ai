import streamlit as st
from pathlib import Path
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import os

st.set_page_config(page_title="DocuCheck AI", layout="wide")
st.title("📄 DocuCheck AI – PDF Verifier & Analyzer")

# Ensure uploads folder exists
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

if uploaded_file:
    pdf_path = UPLOAD_FOLDER / uploaded_file.name
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"PDF saved to {pdf_path}")

    # ---- Extract Embedded Text (PyMuPDF) ----
    doc = fitz.open(str(pdf_path))
    st.subheader("📘 Embedded Text Extraction")
    for i, page in enumerate(doc):
        st.markdown(f"**Page {i+1}**")
        st.text(page.get_text())

    # ---- OCR Text from Images ----
    if st.checkbox("🧠 Show OCR Text"):
        st.subheader("📷 OCR (Image-based Text)")
        images = convert_from_path(str(pdf_path))
        for i, img in enumerate(images):
            ocr_text = pytesseract.image_to_string(img)
            st.markdown(f"**Page {i+1}** (OCR):")
            st.text(ocr_text)
