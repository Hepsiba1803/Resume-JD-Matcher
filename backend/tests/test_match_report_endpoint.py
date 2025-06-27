import pytest
from fastapi.testclient import TestClient

# importing fastapi object from the main app
from backend.app.main import app

client = TestClient(app)

def test_match_files_endpoint():
    resume_content = b"Experienced Python developer with AWS and Docker."
    jd_content = b"Looking for a Python developer with experience in AWS and Kubernetes."

    files = {
        "resume": ("resume.pdf", resume_content, "text"),
        "job_description": ("jd.pdf", jd_content, "text"),
    }b   

    response = client.post("/api/match-files", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert "match_score" in json_data
    assert "resume_keywords" in json_data
    assert "jd_keywords" in json_data
    assert isinstance(json_data["match_score"], (float, int))
    assert isinstance(json_data["resume_keywords"], list)
    assert isinstance(json_data["jd_keywords"], list)

if __name__ == "__main__":
    pytest.main(["-v"])
