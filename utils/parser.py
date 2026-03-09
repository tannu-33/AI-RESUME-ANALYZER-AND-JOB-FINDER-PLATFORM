import pdfplumber
import docx
import os


def extract_text(file):
    """
    Extract text from uploaded PDF or DOCX resume
    """
    text = ""

    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension == ".pdf":
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif file_extension == ".docx":
        doc = docx.Document(file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

    return text