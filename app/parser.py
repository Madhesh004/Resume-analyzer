import PyPDF2
import docx2txt
import tempfile
import os

def parse_resume(file):
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        text = docx2txt.process(tmp_path)
        os.remove(tmp_path)
        return text
    else:
        return "Unsupported file type"
