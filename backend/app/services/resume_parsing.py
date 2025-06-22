import pdfplumber
import docx
import tempfile
import os 

async def parse_resume(file):
    """
    Parses a resume file and extracts text from it.
    
    Args:
        file: The file object containing the resume.
    
    Returns:
        str: The extracted text from the resume.
    """
    if file.content_type == 'application/pdf':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp.flush()
            tmp_path = tmp.name
        try:
            with pdfplumber.open(tmp_path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        finally:
            os.remove(tmp_path)
        return text
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(await file.read())
            tmp.flush()
            tmp_path=tmp.name
            try:
                doc=docx.Document(tmp_path)
                text="\n".join(paragraph.text for paragraph in doc.paragraphs)
            finally:
                os.remove(tmp_path)
            return text
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
            
    