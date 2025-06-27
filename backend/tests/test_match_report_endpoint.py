# File: backend/tests/test_api_endpoint.py

import pytest
from fastapi.testclient import TestClient
import os

# Adjust import according to your project structure
from backend.app.main import app

client = TestClient(app)

# Define paths to your NEW dummy files
TESTS_DIR = os.path.dirname(__file__)
TEST_FILES_DIR = os.path.join(TESTS_DIR, "test_files")
DUMMY_PDF_PATH = os.path.join(TEST_FILES_DIR, "sample_resume.pdf") # <-- Updated name
DUMMY_DOCX_PATH = os.path.join(TEST_FILES_DIR, "Job_Description_JohnDoe.docx")     # <-- Updated name

def test_match_files_endpoint_pdf_docx():
    # Ensure the test files exist before running
    assert os.path.exists(DUMMY_PDF_PATH), f"Test file not found: {DUMMY_PDF_PATH}"
    assert os.path.exists(DUMMY_DOCX_PATH), f"Test file not found: {DUMMY_DOCX_PATH}"

    # Read the dummy file contents as bytes
    with open(DUMMY_PDF_PATH, "rb") as f:
        resume_content = f.read()
    with open(DUMMY_DOCX_PATH, "rb") as f:
        jd_content = f.read()

    # Define the files dictionary with correct filenames and content types
    files = {
        "resume": ("resume.pdf", resume_content, "application/pdf"),
        "job_description": ("job_description.docx", jd_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    }

    response = client.post("/api/match-files", files=files)

    # Assertions remain the same...
    assert response.status_code == 200
    json_data = response.json()
    assert "match_score" in json_data
    # You can even check for the keywords you put in the files
    assert "python" in json_data["resume_keywords"]
    assert "python" in json_data["jd_keywords"]
    assert "developer" in json_data["jd_keywords"]
