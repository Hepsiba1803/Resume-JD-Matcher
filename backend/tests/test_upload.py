import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from fastapi.testclient import TestClient
from app.main import app

BASE_DIR = os.path.dirname(__file__)
PDF_PATH = os.path.join(BASE_DIR, "test_files", "sample_resume.pdf")
DOCX_PATH = os.path.join(BASE_DIR, "test_files", "sample_resume.docx")

client = TestClient(app)

def test_upload_resume_pdf():
    with open(PDF_PATH, "rb") as file:
        response = client.post("/api/upload_resume/", files={"resume": ("sample_resume.pdf", file, "application/pdf")})
    assert response.status_code == 200
    assert "text_preview" in response.json()
    assert "uploaded_file" in response.json()

def test_upload_resume_docx():
    with open(DOCX_PATH, "rb") as file:
        response = client.post("/api/upload_resume/", files={"resume": ("sample_resume.docx", file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
    assert response.status_code == 200
    assert "text_preview" in response.json()
    assert "uploaded_file" in response.json()
