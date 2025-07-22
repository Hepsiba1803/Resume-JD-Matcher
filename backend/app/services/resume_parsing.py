import io
import docx
import pdfplumber
from fastapi import UploadFile

async def parse_file_content(file: UploadFile) -> str:
    """
    Parses the content of an uploaded file (PDF or DOCX) in memory.
    """
    content = await file.read()
    
    if file.content_type == 'application/pdf':
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                # Ensure text is not None before joining
                pages = [p.extract_text() for p in pdf.pages if p.extract_text()]
                return "\n".join(pages)
        except Exception as e:
            raise ValueError(f"Error parsing PDF file: {e}")
            
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        try:
            doc = docx.Document(io.BytesIO(content))
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error parsing DOCX file: {e}")
            
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")