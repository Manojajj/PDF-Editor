import streamlit as st
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Helper function to create a PDF with text
def create_pdf(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()
    buffer.seek(0)
    return buffer

# Helper function to read PDF and return text
def extract_text_from_first_page(pdf_file):
    pdf = PdfFileReader(pdf_file)
    first_page = pdf.getPage(0)
    return first_page.extract_text()

# Helper function to merge PDFs
def merge_pdfs(pdf_files):
    merged_pdf = PdfFileWriter()
    for pdf_file in pdf_files:
        reader = PdfFileReader(pdf_file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            merged_pdf.addPage(page)
    buffer = BytesIO()
    merged_pdf.write(buffer)
    buffer.seek(0)
    return buffer

# Helper function to split PDF into separate pages
def split_pdf(pdf_file):
    reader = PdfFileReader(pdf_file)
    pdf_files = []
    for page_num in range(reader.numPages):
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(page_num))
        buffer = BytesIO()
        writer.write(buffer)
        buffer.seek(0)
        pdf_files.append(buffer)
    return pdf_files

# Helper function to rotate PDF pages
def rotate_pdf(pdf_file, rotation):
    reader = PdfFileReader(pdf_file)
    writer = PdfFileWriter()
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        page.rotateClockwise(rotation)
        writer.addPage(page)
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer

# Helper function to add watermark to PDF
def add_watermark(pdf_file, watermark_text):
    reader = PdfFileReader(pdf_file)
    writer = PdfFileWriter()
    watermark_pdf = create_pdf(watermark_text)
    watermark_reader = PdfFileReader(watermark_pdf)
    watermark_page = watermark_reader.getPage(0)

    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        page.merge_page(watermark_page)
        writer.addPage(page)
    
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer

# Helper function to encrypt PDF
def encrypt_pdf(pdf_file, password):
    reader = PdfFileReader(pdf_file)
    writer = PdfFileWriter()
    
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        writer.addPage(page)
    
    writer.encrypt(password)
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer

# Helper function to decrypt PDF
def decrypt_pdf(pdf_file, password):
    reader = PdfFileReader(pdf_file)
    if reader.isEncrypted:
        reader.decrypt(password)
    
    writer = PdfFileWriter()
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        writer.addPage(page)
    
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer

def main():
    st.title("PDF Editor Tool")

    menu = ["Create PDF", "Extract Text", "Merge PDFs", "Split PDF", "Rotate PDF", 
            "Add Watermark", "Encrypt PDF", "Decrypt PDF"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create PDF":
        st.subheader("Create PDF")
        text = st.text_area("Enter text to add to PDF")
        if st.button("Create PDF"):
            pdf = create_pdf(text)
            st.download_button(
                label="Download PDF",
                data=pdf,
                file_name="created_pdf.pdf",
                mime="application/pdf"
            )

    elif choice == "Extract Text":
        st.subheader("Extract Text from PDF")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        if pdf_file is not None:
            text = extract_text_from_first_page(pdf_file)
            st.write("Extracted Text:")
            st.write(text)

    elif choice == "Merge PDFs":
        st.subheader("Merge PDFs")
        pdf_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if st.button("Merge PDFs"):
            merged_pdf = merge_pdfs(pdf_files)
            st.download_button(
                label="Download Merged PDF",
                data=merged_pdf,
                file_name="merged_pdf.pdf",
                mime="application/pdf"
            )

    elif choice == "Split PDF":
        st.subheader("Split PDF")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Split PDF"):
            split_files = split_pdf(pdf_file)
            for i, pdf in enumerate(split_files):
                st.download_button(
                    label=f"Download Page {i+1}",
                    data=pdf,
                    file_name=f"page_{i+1}.pdf",
                    mime="application/pdf"
                )

    elif choice == "Rotate PDF":
        st.subheader("Rotate PDF")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        rotation = st.selectbox("Rotation", [90, 180, 270])
        if st.button("Rotate PDF"):
            rotated_pdf = rotate_pdf(pdf_file, rotation)
            st.download_button(
                label="Download Rotated PDF",
                data=rotated_pdf,
                file_name="rotated_pdf.pdf",
                mime="application/pdf"
            )

    elif choice == "Add Watermark":
        st.subheader("Add Watermark to PDF")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        watermark_text = st.text_input("Enter watermark text")
        if st.button("Add Watermark"):
            watermarked_pdf = add_watermark(pdf_file, watermark_text)
            st.download_button(
                label="Download Watermarked PDF",
                data=watermarked_pdf,
                file_name="watermarked_pdf.pdf",
                mime="application/pdf"
            )

    elif choice == "Encrypt PDF":
        st.subheader("Encrypt PDF")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        password = st.text_input("Enter password", type="password")
        if st.button("Encrypt PDF"):
            encrypted_pdf = encrypt_pdf(pdf_file, password)
            st.download_button(
                label="Download Encrypted PDF",
                data=encrypted_pdf,
                file_name="encrypted_pdf.pdf",
                mime="application/pdf"
            )

    elif choice == "Decrypt PDF":
        st.subheader("Decrypt PDF")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        password = st.text_input("Enter password", type="password")
        if st.button("Decrypt PDF"):
            decrypted_pdf = decrypt_pdf(pdf_file, password)
            st.download_button(
                label="Download Decrypted PDF",
                data=decrypted_pdf,
                file_name="decrypted_pdf.pdf",
                mime="application/pdf"
            )

if __name__ == '__main__':
    main()
