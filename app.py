import streamlit as st
from pathlib import Path
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR'
# ✅ Add your poppler path here
POPPLER_PATH = r"C:\poppler\Library\bin"

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
    embedded_text_list = []
    for i, page in enumerate(doc):
        text = page.get_text()
        embedded_text_list.append(text)
        st.markdown(f"**Page {i+1}**")
        st.text(text)

    # ---- OCR Text from Images ----
    ocr_text_list = []
    if st.checkbox("🧠 Show OCR Text"):
        st.subheader("📷 OCR (Image-based Text)")
        images = convert_from_path(str(pdf_path), poppler_path=POPPLER_PATH)  # ✅ Poppler path added
        for i, img in enumerate(images):
            ocr_text = pytesseract.image_to_string(img)
            ocr_text_list.append(ocr_text)
            st.markdown(f"**Page {i+1}** (OCR):")
            st.text(ocr_text)

    # ---- Tamper Detection ----
    if st.checkbox("🕵️‍♀️ Run Tamper Detection"):
        st.subheader("⚠️ Tamper Detection Report")
        if not ocr_text_list:
            images = convert_from_path(str(pdf_path), poppler_path=POPPLER_PATH)  # ✅ Poppler path added
            for img in images:
                ocr_text_list.append(pytesseract.image_to_string(img))

        for i, (embedded, ocr) in enumerate(zip(embedded_text_list, ocr_text_list)):
            if embedded.strip() != ocr.strip():
                st.error(f"❗ Page {i+1} might be tampered! Text mismatch detected.")
            else:
                st.success(f"✅ Page {i+1} looks clean. No mismatch detected.")
